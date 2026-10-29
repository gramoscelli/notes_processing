## Apunte: File Inclusion (LFI / RFI) — Concepto, demostración segura en DVWA y defensas

> **Lectura dirigida a ustedes.** Este apunte explica qué es la inclusión de archivos (local y remota), cómo detectar indicios desde la instalación local de DVWA sin automatizaciones, y cómo proteger aplicaciones. No contiene instrucciones operativas para explotar sistemas.



### 1. Objetivos

* Comprender las diferencias entre **Local File Inclusion (LFI)** y **Remote File Inclusion (RFI)** y sus riesgos.
* Observar señales de inclusión de archivos desde la instalación local de DVWA (interacciones manuales en la UI).
* Analizar logs y evidencias.
* Implementar y evaluar mitigaciones: listas blancas de rutas, normalización y verificación de rutas, deshabilitar inclusión remota, principio de menor privilegio, controles de permisos, y evitar exposición de información sensible.
* Redactar y entregar código corregido que elimine la posibilidad de inclusión arbitraria.



### 2. ¿Qué es File Inclusion?

* **LFI (Local File Inclusion):** la aplicación incluye archivos que existen en el sistema del servidor (logs, ficheros de configuración, etc.) usando, directa o indirectamente, un parámetro controlado por el usuario. Si no se valida la entrada, el atacante puede lograr leer, y en algunos casos ejecutar, archivos sensibles.
* **RFI (Remote File Inclusion):** la aplicación permite incluir recursos remotos (ej. por URL). Si está habilitado, un atacante puede forzar que la aplicación haga `include`/`require` de contenido remoto controlado por el atacante, llevándolo a ejecutar código arbitrario en el servidor.

Impactos típicos:

* Exposición de archivos sensibles (contraseñas, claves, configuraciones).
* Ejecución remota de código (RCE) si se incluyen/ejecutan contenidos maliciosos.
* Escalada de ataque: exfiltración, pivoting, persistencia.



### 3. Condiciones y reglas para la práctica

* Usar **solo** la instalación local de DVWA en su máquina/VM.
* No ejecutar herramientas automáticas ni visitar recursos remotos diseñados para explotar la vulnerabilidad fuera del entorno controlado.
* No incluir ni publicar en los informes payloads o rutas de explotación. El objetivo es **observar** y **proteger**.



### 4. Demostración segura (solo interacción manual en la UI de DVWA)

> No se muestran ni se describen payloads. Solo se explica cómo observar y registrar.

1. Abrir DVWA en el navegador (`http://localhost/dvwa`) y acceder al módulo **File Inclusion** (o módulo equivalente).
2. Anotar el nivel de seguridad (Low / Medium / High).
3. Introducir mediante la UI valores inocuos (por ejemplo, nombres de archivos intencionalmente creados para la práctica dentro de la instalación local) y observar la respuesta (salida, errores, tiempos).
4. Comparar comportamientos entre niveles (¿se expone la ruta completa? ¿hay mensajes de error que revelan rutas o stack traces?).
5. Revisar logs del servidor y de la aplicación para las peticiones realizadas y registrar fragmentos como evidencia.
6. Proveer un código vulnerable y entregar una versión corregida que evite inclusión arbitraria.



### 5. Actividades a realizar

1. Capturas de pantalla del módulo File Inclusion en **Low** y en **High** (salida visible en la UI).
2. Fragmentos de logs relevantes (timestamp, endpoint, parámetros, código HTTP).
3. Código original (vulnerable) y versión corregida con explicación de por qué la corrección es segura.
4. Breve informe comparando el comportamiento antes/después de la corrección y análisis de riesgo residual.



### 6. Medidas de defensa y ejemplos (solo código defensivo)

#### Principios generales

1. **Nunca** incluir archivos basados directamente en entrada del usuario sin validación.
2. **Preferir listas blancas** de recursos permitidos (nombres o rutas predefinidas) en vez de intentar filtrar cadenas peligrosas.
3. **Deshabilitar** la inclusión remota en la configuración del intérprete (p. ej. `allow_url_include = Off` en PHP).
4. **Normalizar y resolver rutas absolutas** con `realpath()` o equivalentes y comprobar que están dentro de un directorio base seguro.
5. **Principio de menor privilegio**: archivos sensibles (config, keys) deben tener permisos estrictos y no estar disponibles para el proceso web.
6. **Evitar mostrar errores/paths en producción**; registrar internamente sin exponer al cliente.



#### A) Whitelist (lista blanca) — la solución preferida

Mapear nombres de recursos permitidos a rutas internas y no usar rutas arbitrarias enviadas por el cliente.

**PHP — ejemplo didáctico (lista blanca):**

```php
// Mapear identificadores permitidos a archivos internos
$pages = [
  'home' => '/var/www/app/pages/home.php',
  'about' => '/var/www/app/pages/about.php',
  'help' => '/var/www/app/pages/help.php'
];

$page = $_GET['page'] ?? 'home';

if (!array_key_exists($page, $pages)) {
  http_response_code(404);
  echo "Página no encontrada";
  exit;
}

include $pages[$page]; // inclusión controlada
```

Comentario: el cliente sólo puede elegir entre entradas del mapa; nunca controla la ruta completa.



#### B) Normalización y validación de ruta (cuando se trabaja con rutas)

Si se necesita permitir rutas relativas dentro de un directorio seguro, normalizar y comprobar que la ruta resultante esté contenida en el directorio base.

**Node.js — ejemplo didáctico (validación con path.normalize):**

```js
import path from 'path';
import fs from 'fs';

const BASE_DIR = '/var/www/app/pages';

function safeInclude(requested) {
  const normalized = path.normalize(requested);             // elimina componentes redundantes
  const fullPath = path.join(BASE_DIR, normalized);         // construye ruta dentro del base
  const resolved = path.resolve(fullPath);

  // Verificar que la ruta resuelta empiece por el BASE_DIR (evita traversal)
  if (!resolved.startsWith(path.resolve(BASE_DIR) + path.sep)) {
    throw new Error('Ruta no permitida');
  }
  return fs.readFileSync(resolved, 'utf8'); // ejemplo: leer, no ejecutar
}
```

Explicación: se construye la ruta absoluta y se verifica que permanezca dentro de `BASE_DIR`. Así se evita que entradas crafteadas salgan fuera del directorio autorizado.



#### C) PHP — configuraciones seguras

* En `php.ini`:

  ```
  allow_url_fopen = Off
  allow_url_include = Off
  ```

  Estas directivas evitan que `include`/`require` traiga contenido a través de URLs remotas.
* Evitar `include($_GET['file'])` sin control. Si se necesita incluir, usar whitelist o mapping.

**PHP — ejemplo con realpath (complementario):**

```php
$base = '/var/www/app/pages';
$file = $_GET['file'] ?? 'home.php';
$path = realpath($base . DIRECTORY_SEPARATOR . $file);

if ($path === false || strpos($path, realpath($base)) !== 0) {
  http_response_code(400);
  echo "Ruta inválida";
  exit;
}

include $path;
```

Nota: `realpath` resuelve symlinks y normaliza; la comprobación asegura que la ruta quede dentro del `base`.



#### D) Evitar ejecución de contenido incluido — separar lectura vs ejecución

Si la aplicación solo necesita mostrar el contenido de un archivo (p. ej. logs o plantillas), **no** incluir/ejecutar el archivo como código; en su lugar, leer su contenido y tratarlo como datos (sanitizar antes de renderizar).

Ejemplo conceptual:

```py
## Python: leer y mostrar archivo como texto seguro
with open(resolved_path, 'r', encoding='utf-8') as f:
    content = f.read()
## escapar contenido antes de mostrar en HTML
```



#### E) Restricciones de despliegue y permisos

* Archivos de configuración sensibles deben tener permisos que impidan lectura por el usuario del proceso web cuando no sea necesario.
* Ejecutar el servidor web con un usuario con privilegios limitados.
* Aplicar mecanismos de confinamiento: chroot, contenedores, AppArmor/SELinux.



#### F) Desactivar funciones peligrosas

En entornos donde no se requieren funciones de shell o inclusión remota, deshabilitarlas (ej.: `disable_functions` en PHP) para reducir la superficie de ataque.



### 7. Detección y qué buscar en los logs

Señales que pueden indicar intentos o explotación:

* Peticiones con parámetros inusuales dirigidos a endpoints de inclusión (registro del parámetro `page`, `file`, `include`, etc.).
* Respuestas que exponen contenido de archivos del sistema (configuración, rutas) o que devuelven grandes fragmentos de texto que no deberían estar accesibles.
* Errores con paths absolutos o traces que revelen estructura del filesystem.
* Picos de peticiones a endpoints de inclusión desde la misma IP o varias IPs intentando distintos parámetros.

Ejemplo de línea de log a recopilar:

```
[2025-10-29 17:05:12] GET /vulnerable.php?file=... 200 ip=192.168.56.101 user-agent=...
```

(Registrar los parámetros tal como aparecen y el contexto; en informes pedagógicos pueden anonimizarse).



### 8. Actividades opcionales (avanzadas)

* Reescribir un endpoint vulnerable para usar lista blanca y/o normalización de rutas; demostrar que accesos fuera del directorio base son rechazados.
* Revisar permisos de archivos y demostrar (conceptualmente) qué archivos podían haberse expuesto antes de la corrección.
* Diseñar una política de despliegue que minimice riesgos: `allow_url_include=Off`, contenedores, cuentas sin privilegios, logs centralizados.
* Implementar detecciones que alerten sobre accesos inusuales a endpoints de inclusión.



### 9. Preguntas de autoevaluación

1. ¿Cuál es la diferencia principal entre LFI y RFI?
2. ¿Por qué `allow_url_include = Off` es importante en entornos PHP?
3. ¿Por qué una lista blanca es preferible a filtrar secuencias peligrosas?
4. ¿Qué comprobación se debe hacer después de usar `realpath()` y por qué?
5. ¿Qué archivos del sistema suelen ser objetivo de LFI y cómo evitar exponerlos?



### 10. Recursos recomendados (seguros)

* OWASP File Inclusion / Directory Traversal — explicaciones y recomendaciones.
* Guía de configuración segura de PHP (`php.ini`) — `allow_url_include`, `disable_functions`.
* Documentación de `path.normalize` / `path.resolve` (Node), `realpath()` (PHP/Python) para manejo seguro de rutas.
* Artículos sobre permisos y confinamiento (chroot, AppArmor, SELinux).

