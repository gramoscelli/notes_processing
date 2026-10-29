
## Segundo Caso: Command Injection — Concepto, demostración segura en DVWA y defensas

> **Introducción:** Este apunte explica qué es la inyección de comandos del sistema operativo (command injection), cómo observar su presencia desde la interfaz local de DVWA sin automatizaciones, y cómo proteger aplicaciones para evitarla. No contiene instrucciones operativas para explotar sistemas.



### 1. Objetivos

* Comprender qué es la inyección de comandos y sus riesgos.
* Observar señales de command injection desde la instalación local de DVWA (interacciones manuales en la UI).
* Analizar registros y evidencias.
* Implementar y evaluar mitigaciones: validación y filtrado, listas blancas, ejecución segura de procesos, principio de menor privilegio, escape y aislamiento.
* Identificar prácticas inseguras y cómo corregirlas.



### 2. ¿Qué es Command Injection?

La **inyección de comandos** ocurre cuando una aplicación incorpora datos controlados por el usuario en llamadas al sistema operativo (shell) sin validación o escape adecuados. Un atacante puede insertar operadores o fragmentos de comando para ejecutar órdenes arbitrarias en el servidor (por ejemplo listar archivos, leer datos, modificar ficheros), comprometiendo la integridad y confidencialidad del servidor.

Formas habituales de entrada peligrosa:

* Parámetros que la aplicación concatena en una cadena para `system()`, `exec()`, `shell_exec()` o similares.
* Valores usados para construir llamadas a utilidades del sistema (p. ej. `ping`, `ls`, `tar`) sin saneamiento.

Impacto potencial:

* Ejecución remota de código, extracción de datos, escalada de privilegios, pivoting en la red, borrado o manipulación de datos.



### 3. Condiciones y reglas para la práctica

* Usar **solo** la instalación local de DVWA accesible en sus máquinas/VMs.
* Abstenerse de ejecutar herramientas automáticas o payloads que intenten explotar la vulnerabilidad.
* El objetivo es **observar el fenómeno desde la UI** y aprender a **corregir** el código vulnerable.
* No realizar pruebas contra terceros ni servicios en Internet.



### 4. Demostración segura (solo interacciones manuales en la UI de DVWA)

> **Nota importante:** no hay ni habrá instrucciones para enviar payloads ni para explotar la vulnerabilidad. Solo describimos cómo observar comportamientos indicadores desde la interfaz de DVWA.

1. Abrir DVWA en el navegador (`http://localhost:8080/` o la URL local configurada).
2. Ir al módulo correspondiente (habitualmente **Command Injection** o módulo equivalente).
3. Registrar el nivel de seguridad actual (Low / Medium / High).
4. Interacciones manuales seguras:

   * Introducir únicamente valores inofensivos mediante la UI (por ejemplo, un nombre de host que exista en la red local).
   * Observar la respuesta: salida presentada en la página, tiempos de respuesta, errores mostrados.
   * Cambiar el nivel de seguridad y comparar qué información revela la aplicación en cada nivel (mensajes, errores, salida del sistema visible).
5. Revisar logs del servidor (Apache/Nginx, registros de la aplicación) y localizar entradas relacionadas con las peticiones realizadas.
6. Documentar las diferencias entre los niveles de seguridad y las trazas observadas en logs.



### 5. Actividades a realizar

1. Capturas de pantalla del módulo Command Injection en **Low** y en **High** mostrando la interfaz y la salida visible.
2. Fragmentos de logs del servidor que correspondan a sus peticiones (timestamps, endpoint, parámetros enviados).
3. Refactorización de un fragmento de código vulnerable para eliminar posibilidades de inyección — entregar el código corregido y una breve explicación de por qué es seguro.
4. Informe que compare comportamiento antes/después de la corrección: qué cambió en la UI, en la información expuesta y en los logs.

(ver [este artículo](https://medium.com/@shubamagrawal112/dvwa-csrf-c6d6cf1900c0))

### 6. Medidas de defensa y ejemplos (código defensivo)

Las siguientes medidas son **preventivas** y **correctivas**. Los ejemplos muestran cómo reescribir puntos peligrosos para eliminar el vector de inyección.

#### Principios generales

1. **Nunca** concatenar entrada de usuario dentro de comandos de shell.
2. **Validación estricta**: preferir listas blancas (whitelisting) sobre listas negras.
3. **Evitar llamadas al shell**: usar funciones o APIs nativas cuando sea posible.
4. **Ejecutar procesos con argumentos separados** y con `shell=False`/equivalente.
5. **Principio de menor privilegio**: el proceso que ejecuta comandos debe tener solo los permisos estrictamente necesarios.
6. **Registro y monitoreo**: loguear entradas sospechosas y alertar sobre patrones inusuales.
7. **Aislamiento**: si es imprescindible ejecutar comandos del sistema, hacerlo en contenedores o sandboxes con recursos y permisos limitados.



#### A) Validación por lista blanca (ejemplo conceptual)

Validar y permitir únicamente valores esperados (ej.: nombres de host predefinidos, opciones permitidas).

Pseudocódigo:

```text
allowed_hosts = ["host1.local", "host2.local", "127.0.0.1"]
if user_input in allowed_hosts:
  proceed()
else:
  reject_request("Parámetro no permitido")
```



#### B) Evitar shell: usar APIs en lugar de comandos (ejemplos prácticos)

**Node.js — usar `child_process.spawn` con argumentos (shell=false)**
Explicar: pasar los argumentos como array y no usar `shell: true`. Cuando sea posible, evitar totalmente ejecutar utilidades externas.

```js
import { spawn } from 'child_process';

// Ejemplo didáctico: ejecutar utilitario con argumentos controlados
function safePing(host, callback) {
  // validar host contra whitelist antes
  const proc = spawn('ping', ['-c', '3', host], { shell: false });

  let output = '';
  proc.stdout.on('data', (data) => { output += data.toString(); });
  proc.on('close', (code) => { callback(null, { code, output }); });
}
```

Comentario: el punto crítico es **no** construir la línea de comando concatenando strings y **no** usar `shell: true`. Además, validar `host` previamente.



**Python — usar `subprocess.run` con lista de args (shell=False)**

```py
import subprocess

def safe_ping(host):
    ## validar host contra whitelist
    result = subprocess.run(['ping', '-c', '3', host], capture_output=True, text=True, shell=False)
    return result.returncode, result.stdout
```



**PHP — evitar `shell_exec` y `system`; preferir funciones nativas o escapes y llamadas seguras**

* Evitar `exec()`, `system()`, `shell_exec()` si hay alternativas nativas.
* Si es imprescindible, **no** concatenar; validar y usar mecanismos que no invoquen el shell.

Ejemplo de enfoque seguro (conceptual):

```php
// Validar y permitir solo hosts concretos
$allowed = ['host1.local', '127.0.0.1'];
$host = $_POST['host'] ?? '';
if (!in_array($host, $allowed, true)) {
    http_response_code(400);
    echo "Parámetro no permitido";
    exit;
}

// Llamada fuera del shell: escapeshellarg como último recurso defensivo
$cmd = 'ping -c 3 ' . escapeshellarg($host);
$output = shell_exec($cmd);
echo nl2br(htmlspecialchars($output));
```

Comentario: usar `escapeshellarg` es una medida defensiva para escapar argumentos, pero la **mejor** estrategia es evitar shell por completo. Además, `escapeshellarg` no sustituye a una lista blanca.



#### C) Lista blanca de comandos y argumentos

Si la aplicación permite seleccionar una acción (por ejemplo `action=ping|traceroute`), mapear esas opciones internamente en lugar de usar el valor enviado por el usuario directamente.

```js
const actions = {
  ping: (host) => spawn('ping', ['-c','3', host]),
  // traceroute: ...
};

if (!actions[userAction]) return reject();
actions[userAction](validatedHost);
```



#### D) Aislar ejecución y principios de despliegue

* Ejecutar comandos en contenedores con permisos mínimos.
* Aislar procesos que manejen entradas no confiables.
* Aplicar AppArmor/SELinux para restringir lo que un proceso puede hacer.
* Desactivar funciones peligrosas en PHP (`disable_functions = exec,passthru,shell_exec,system`) cuando no sean necesarias.



#### E) Sanitización vs. Whitelisting

* **Whitelisting** (permitir solo valores conocidos) es preferible.
* Sanitizar (escape) es un complemento, no una solución única.



### 7. Detección y qué buscar en los logs

* Peticiones a endpoints que ejecutan utilidades del sistema: revisar parámetros enviados.
* Respuestas que incluyen salida de comandos (stdout) visibles en la página: indicar fuga de información.
* Picos de peticiones con parámetros inusuales (tuberías `|`, `;`, `&&`) — aunque no deben enseñarse como payloads, su aparición en logs es una señal de intento de exploit.
* Errores de la aplicación que muestran rutas de sistema o stack traces.

Ejemplo de líneas a recopilar en el informe (plantilla segura):

```
[2025-10-29 15:10:03] POST /vulnerable-endpoint param=127.0.0.1 ip=192.168.56.101
[2025-10-29 15:10:03] WARNING: salida de utilitario visible en respuesta
```



### 8. Actividades opcionales (avanzadas)

* Reescribir un endpoint vulnerable para que **no** llame al shell y usar librerías nativas que provean la funcionalidad.
* Diseñar una política de despliegue que minimice riesgos (disable_functions en PHP, contenedores, cuentas con pocos privilegios).
* Implementar detección basada en patrones de parámetros inusuales y generar alertas.
* Evaluar el impacto de devolver o no la salida de un comando en la respuesta HTTP (fuga de información).



### 9. Preguntas de autoevaluación

1. ¿Por qué concatenar variables de entrada en una cadena de comando es peligroso?
2. ¿Qué ventajas tiene ejecutar un proceso con `shell=False` y argumentos como array/lista?
3. ¿Por qué la lista blanca es superior a la lista negra en validación de entradas?
4. ¿Qué controles adicionales aplicarías si fuera imprescindible ejecutar comandos del sistema?
5. ¿Qué información no se debe mostrar al usuario en caso de error y por qué?



### 10. Recursos recomendados (seguros)

* OWASP Command Injection (descripción y contramedidas) — leer la sección de mitigaciones.
* Guías de `subprocess` en Python y `child_process` en Node.js (secciones sobre uso sin shell).
* Documentación de `escapeshellarg`/`escapeshellcmd` (uso defensivo y límites).
* Documentación de AppArmor/SELinux para confinamiento de procesos.


