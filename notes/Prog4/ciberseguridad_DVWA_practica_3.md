## Apunte: CSRF (Cross-Site Request Forgery) — Concepto, demostración segura en DVWA y defensas

> **Introducción:** Este apunte explica qué es CSRF, cómo observar indicios desde la instalación local de DVWA sin automatizaciones, y qué medidas aplicar para prevenirlo. No contiene instrucciones para explotar vulnerabilidades.



### 1. Objetivos

* Comprender el ataque CSRF y por qué es peligroso para acciones con estado (transferencias, cambios de contraseña, etc.).
* Observar desde la UI local de DVWA cómo una aplicación vulnerable permite solicitudes forjadas.
* Aprender e implementar defensas efectivas: tokens CSRF, SameSite cookies, comprobación de Origin/Referer, evitar el uso de cookies para APIs, y buenas prácticas de diseño.
* Analizar logs y señales de intento de CSRF.



### 2. ¿Qué es CSRF?

Un **Cross-Site Request Forgery (CSRF)** obliga a un navegador autenticado a enviar una petición no deseada a una aplicación web en la que el usuario está autenticado. Si la aplicación confía únicamente en cookies de sesión para autenticar peticiones y no verifica que la petición sea intencional, una página maliciosa puede causar que el navegador del usuario haga acciones en su nombre (por ejemplo: cambiar su dirección de email, transferir dinero, borrar datos).

Características clave:

* Aprovecha la confianza que el sitio A tiene en el navegador del usuario (cookies de sesión).
* Afecta a peticiones **state-changing** (POST/PUT/DELETE), aunque también puede aprovechar GET si la aplicación realiza cambios con GET (mala práctica).
* No requiere que el atacante conozca las cookies de sesión; basta con inducir al navegador a enviar la petición.



### 3. Condiciones y reglas para la práctica

* Usar **solo** la instalación local de DVWA en su máquina/VM.
* No crear ni visitar páginas externas diseñadas para explotar CSRF en entornos que no sean controlados.
* Evitar automatizaciones o scripts que lancen peticiones maliciosas. La demostración debe ser observacional y defensiva desde la UI.



### 4. Demostración segura (solo interacción en la UI de DVWA)

> No se indican payloads ni pasos para explotar. Solo se describe cómo observar.

1. Abrir DVWA en el navegador (`http://localhost/dvwa`) y acceder al módulo **CSRF** o al endpoint que DVWA exponga para esa vulnerabilidad.
2. Registrar el nivel de seguridad (Low/Medium/High).
3. Con nivel **Low**, inspeccionar la forma HTML del formulario (por ejemplo, un formulario para cambiar la contraseña) desde la UI. Observar si existe **un token oculto** en el formulario o no.
4. Enviar manualmente valores desde la UI y observar respuestas y mensajes.
5. Cambiar a **High** y comprobar si aparece un token CSRF o controles adicionales (captcha, token en formulario, encabezados esperados).
6. Revisar logs del servidor para las peticiones realizadas (endpoint, parámetros, código HTTP) y guardar fragmentos como evidencia.



### 5. Actividades a realizar

1. Capturas de pantalla del formulario vulnerable en **Low** y del formulario protegido en **High** (si DVWA lo muestra).
2. Fragmento de logs con la petición POST al endpoint vulnerable (timestamp, endpoint, parámetros).
3. Implementación de una protección CSRF en un ejemplo de aplicación (código defensivo provisto abajo) y comprobación de que la petición sin token es rechazada.
4. Explicación breve de por qué la protección elegida evita CSRF.



### 6. Medidas de defensa y ejemplos (solo código defensivo)

#### Principios generales

* **No** confiar únicamente en cookies para autorizar acciones sensibles.
* Insertar una verificación **única** por sesión o por petición que el atacante no pueda precomputar desde otro dominio.
* **Preferir** SameSite cookies y diseño de APIs token-based (Bearer) para endpoints consumidos por clientes JavaScript.
* Usar comprobación de **Origin/Referer** como medida adicional donde aplique.



#### A) Token CSRF (server-side token en formulario)

Generar un token aleatorio por sesión o por formulario; insertarlo en formularios como campo oculto y verificarlo en el servidor al recibir la petición.

**Node/Express — con `csurf` (ejemplo didáctico)**:

```js
import express from 'express';
import cookieParser from 'cookie-parser';
import csurf from 'csurf';

const app = express();
app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));

// CSRF tokens en cookies + comprobación automática
const csrfProtection = csurf({ cookie: true });

app.get('/change-email', csrfProtection, (req, res) => {
  // En la vista insertar: <input type="hidden" name="_csrf" value="{{req.csrfToken()}}">
  res.send(`<form method="POST"><input name="email"><input type="hidden" name="_csrf" value="${req.csrfToken()}"><button>Enviar</button></form>`);
});

app.post('/change-email', csrfProtection, (req, res) => {
  // Si token inválido, csurf rechazará antes de llegar aquí
  res.send('Email cambiado (simulación)');
});
```

> `csurf` lanza un error si el token falta o es inválido. Es buena práctica manejar errores y registrar intentos fallidos.



#### B) Double-submit cookie (si no hay session server side)

Enviar un token CSRF en una cookie y además incluirlo en un campo del formulario; el servidor verifica que ambos coincidan. Es menos robusto que un token ligado a sesión en el servidor, pero útil en situaciones sin almacenamiento server-side.

Concepto:

1. Al autenticar, servidor setea `Set-Cookie: csrf=RANDOM`.
2. Formulario incluye campo oculto `_csrf` con el mismo valor.
3. En POST, servidor compara cookie `csrf` con campo `_csrf`.



#### C) SameSite cookies

Configurar la cookie de sesión con `SameSite=Lax` o `SameSite=Strict` para prevenir el envío de cookies en peticiones cross-site:

* `Strict` = no enviar la cookie en peticiones iniciadas desde otro sitio (más seguro pero puede afectar UX).
* `Lax` = permite cookies en algunas transiciones de navegación (compromiso razonable).
* `None` = enviar en todos los contextos (necesita `Secure`).

Ejemplo (Express):

```js
app.use(session({
  secret: 'secreto',
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'lax' // o 'strict' según necesidades
  }
}));
```



#### D) Comprobación de Origin / Referer

Para peticiones sensibles (POST), comprobar que el encabezado `Origin` o `Referer` corresponde al dominio esperado. `Origin` es preferible porque está presente en peticiones CORS y es menos manipulable por el navegador.

Pseudocódigo:

```text
if request.method in ["POST","PUT","DELETE"]:
  origin = request.headers.get('Origin') or request.headers.get('Referer')
  if not origin or not origin.startswith("https://misitio.local"):
    reject_request(403)
```

Limitación: algunos proxies o navegadores pueden omitir `Referer` por privacidad; no lo use como única defensa, combínelo con tokens.



#### E) Evitar usar cookies para APIs públicas / usar tokens Bearer

Si la API debe ser consumida cross-origin por SPAs u otras aplicaciones, usar tokens en encabezados `Authorization: Bearer <token>` en lugar de confiar en cookies de sesión automáticas. Los tokens almacenados en `localStorage` o gestionados por el cliente (con cuidado) evitan el vector CSRF porque se requiere JavaScript del propio sitio para inyectarlos (aunque esto introduce otros riesgos XSS si no se gestiona bien).



#### F) Buenas prácticas adicionales

* Evitar cambios de estado con GET. Siempre usar métodos HTTP adecuados (POST/PUT/DELETE) para acciones que modifican datos.
* Minimizar la exposición de endpoints sensibles y exigir re-autenticación para operaciones críticas.
* Diseñar flujos con confirmación explícita (captcha, re-enter password) para operaciones de alto riesgo.



### 7. Detección y qué buscar en los logs

* Peticiones POST con referer/origin ausente o que provienen de dominios externos.
* Picos de peticiones a endpoints que cambian estado desde distintas IPs pero con cookies válidas (señal de CSRF dirigido a usuarios autenticados).
* Errores de validación de token CSRF: registrar IP, user-agent, timestamp y parámetros relevantes para análisis forense.
* Alertas: múltiples rechazos CSRF para la misma cuenta en corto periodo — podría indicar que un sitio externo intenta inducir acciones.

Ejemplo de entrada de log a recopilar:

```
[2025-10-29 16:12:05] POST /transfer 403 CSRF_TOKEN_MISSING user=sessionId=abc123 ip=192.168.56.101
```



### 8. Actividades opcionales (avanzadas)

* Implementar `csurf` (o equivalente) en una aplicación sencilla y demostrar que una petición sin token es rechazada.
* Probar distintas configuraciones de `SameSite` y documentar efectos en escenarios de navegación.
* Diseñar una política segura para formularios de alto riesgo: token + re-autenticación + CAPTCHA.
* Integrar logs que alerten al equipo de seguridad si hay un aumento de rechazos CSRF.



### 9. Preguntas de autoevaluación

1. ¿Por qué CSRF no requiere que el atacante conozca la cookie de sesión?
2. ¿Qué ventajas y limitaciones tiene `SameSite` frente a los tokens CSRF?
3. ¿En qué casos es preferible usar comprobación de `Origin`/`Referer` y cuándo no?
4. ¿Por qué las APIs públicas a menudo usan tokens Bearer y evitan cookies para prevenir CSRF?
5. ¿Qué medidas combinarías para proteger un endpoint de transferencia de dinero?



### 10. Recursos recomendados (seguros)

* **OWASP CSRF Prevention Cheat Sheet** — prácticas y patrones para prevenir CSRF.
* Documentación de frameworks (Django, Rails, Express) sobre protección CSRF integrada.
* Artículos sobre `SameSite` cookies y sus implicaciones en compatibilidad.
