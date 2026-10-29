## Primer caso: Fuerza bruta — Concepto, demostración segura en DVWA y defensas

> **Introducción:** Este apunte explica qué es un ataque de fuerza bruta, cómo observarlo de forma segura en la interfaz local de DVWA (sin automatizaciones), y qué medidas implementar para proteger una aplicación. No contiene scripts ni instrucciones para automatizar ataques contra sistemas reales.



### 1. Objetivos

* Entender qué es un ataque de fuerza bruta y sus variantes.
* Observar el comportamiento de una aplicación vulnerable desde su propia instalación local de DVWA (interacciones manuales en la UI).
* Analizar registros del servidor para identificar intentos de acceso.
* Implementar y evaluar mitigaciones: rate limiting, bloqueo temporal, backoff, uso de hashing fuerte y MFA.



### 2. ¿Qué es un ataque de fuerza bruta?

Un **ataque de fuerza bruta** intenta adivinar credenciales (usuario/contraseña) probando muchas combinaciones. Variantes comunes:

* **Combinatorio**: prueba sistemáticamente combinaciones de caracteres.
* **Diccionario**: prueba contraseñas tomadas de listas comunes.
* **Credential stuffing**: intenta credenciales filtradas de otras brechas.

Consecuencias habituales: acceso no autorizado, bloqueo de cuentas legítimas por intentos repetidos, sobrecarga del servicio y posibilidad de fraude.



### 3. Condiciones y reglas de seguridad para la práctica

* Usar **solo** la instalación local de DVWA que ya tengan en sus computadoras/VMs.
* No ejecutar herramientas automáticas ni scripts que automaticen intentos.
* Nunca probar esto contra servicios externos o redes que no controlen y autoricen explícitamente.
* El objetivo es **observar y defender**, no automatizar ataques.



### 4. Demostración segura (interacciones manuales en la UI de DVWA)

> **Nota:** aquí sólo se describen pasos manuales para la interfaz de DVWA; no hay comandos ni explicaciones sobre cómo automatizar ataques.

1. Abrir DVWA en el navegador (ej.: `http://localhost:8080/`) y acceder al módulo **Brute Force**.
2. Anotar el **nivel de seguridad** actual (Low / Medium / High).
3. Con el nivel en **Low**, intentar manualmente (sin automatizar) unas pocas contraseñas para un usuario existente (por ejemplo `admin` si está presente).
4. Observar y anotar:

   * Mensajes que devuelve la aplicación tras cada intento.
   * Tiempo de respuesta entre intentos.
   * Si la aplicación muestra mensajes que diferencian “usuario inexistente” de “contraseña incorrecta”.
5. Cambiar el nivel a **Medium** y **High**, repetir los intentos manuales y comparar comportamientos y mensajes.
6. Abrir los logs del servidor web (por ejemplo, `apache`/`nginx`) y localizar las entradas correspondientes a sus intentos (timestamp, IP, endpoint, código HTTP). Guardar fragmentos como evidencia.



### 5. Actividades a realizar (entregables)

1. Capturas de pantalla de DVWA: módulo Brute Force en **Low** y en **High**.
2. Fragmentos de logs del servidor donde aparezcan sus intentos (con timestamps).
3. Implementación y pruebas de al menos una mitigación (ver sección 6) en la aplicación de práctica.
4. Breve informe que compare el comportamiento antes y después de aplicar la mitigación: ¿qué cambió en la UI y en los logs?

(ver [este artículo](https://medium.com/@waeloueslati18/exploring-dvwa-a-walkthrough-of-the-brute-force-challenge-part-1-d38241ee81da))

### 6. Medidas de defensa y ejemplos (solo código defensivo)

A continuación se describen medidas concretas y ejemplos de código para **proteger** la aplicación.

#### A) Bloqueo temporal de cuenta (account lockout)

Lógica: llevar un contador de fallos por cuenta y, al superar un umbral, bloquear la cuenta temporalmente o exigir verificación adicional (captcha, email).

Pseudocódigo lógico:

```text
on_login_attempt(user, password, ip):
  record_attempt(user, ip, timestamp)
  failures = count_recent_failures(user, window=15min)
  if failures >= 5:
    set_account_locked(user, until=now + 15min)
    notify_user_of_lock(user)
    return "Cuenta bloqueada temporalmente"
  else:
    if check_password(user, password):
      clear_failures(user)
      login_success()
    else:
      increment_failures(user)
      return "Credenciales incorrectas"
```

Consideración: combinar con mecanismos que eviten que un atacante bloquee cuentas de terceros (por ejemplo, aplicar también rate limiting por IP).



#### B) Rate limiting (por IP y/o por cuenta)

Evitar un alto volumen de peticiones al endpoint de login.

Ejemplo (Node/Express) — uso didáctico de `express-rate-limit`:

```js
import express from 'express';
import rateLimit from 'express-rate-limit';

const app = express();

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5, // máximo 5 intentos por IP en la ventana
  handler: (req, res) => {
    res.status(429).send('Demasiados intentos. Inténtalo más tarde.');
  }
});

app.post('/login', loginLimiter, (req, res) => {
  // lógica de autenticación
});
```

Comentario: en redes con NAT o proxies, el rate limiting por IP puede afectar a varios usuarios; por eso es recomendable aplicar también límites por cuenta y otros controles.



#### C) Backoff exponencial y captcha

Incrementar el tiempo de espera tras fallos sucesivos y/o exigir captcha tras X fallos:

* 1.º fallo → sin delay
* 2.º fallo → 1 s delay
* 3.º fallo → 2 s delay
* 4.º fallo → 4 s delay
* Tras N fallos → mostrar captcha

Esto hace más costoso el ataque sin bloquear permanentemente al usuario legítimo.



#### D) Almacenamiento seguro de contraseñas

Usar hashing fuerte (bcrypt, argon2) con salt por usuario.

Ejemplo (Node.js + bcrypt):

```js
import bcrypt from 'bcrypt';

async function createUser(username, plainPassword) {
  const saltRounds = 12;
  const hash = await bcrypt.hash(plainPassword, saltRounds);
  // almacenar 'hash' en la base de datos
}

async function checkPassword(plainPassword, storedHash) {
  return await bcrypt.compare(plainPassword, storedHash);
}
```



#### E) Autenticación multifactor (MFA)

Agregar un segundo factor (TOTP, SMS, push) reduce drásticamente el riesgo ante credenciales robadas o adivinadas.



#### F) Detección y monitoreo

* Registrar intentos fallidos en un sistema de logs centralizado.
* Generar alertas por picos inusuales (mismo IP probando muchas cuentas o muchas IPs intentando la misma cuenta).
* Mantener paneles de observabilidad que muestren tendencias de intentos de autenticación.



### 7. Qué buscar en los logs (ejemplo)

Fragmento de log de ejemplo (ficticio, para usar como plantilla):

```
[2025-10-29 14:03:12] POST /login 200 120ms user=admin ip=192.168.56.101
[2025-10-29 14:03:20] POST /login 401 10ms user=admin ip=192.168.56.101
[2025-10-29 14:03:28] POST /login 401 11ms user=admin ip=192.168.56.101
```

Extraer y anexar las líneas que correspondan a sus intentos.



### 8. Actividades opcionales (más avanzadas)

* Implementar una política híbrida: rate limiting por IP + contador por cuenta + captcha tras X fallos.
* Simular **credential stuffing** conceptualmente: analizar cómo detectar intentos masivos contra muchas cuentas y por qué el MFA y la detección por patrones de acceso lo mitigan.
* Evaluar impactos en usabilidad: diseñar una política equilibrada entre seguridad y experiencia del usuario.



### 9. Preguntas de autoevaluación

1. ¿Cuál es la diferencia entre un ataque por diccionario y uno combinatorio?
2. ¿Qué riesgos introduce un bloqueo permanente de cuentas como estrategia contra la fuerza bruta?
3. ¿Qué ventajas ofrece aplicar rate limiting por cuenta además de por IP?
4. ¿Por qué el hashing de contraseñas con salt es imprescindible?
5. ¿Cómo ayudaría la MFA a reducir el impacto de un credential stuffing?



### 10. Recursos recomendados (lecturas seguras)

* [**OWASP Authentication Cheat Sheet**](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.htmll) — buenas prácticas de autenticación.
* [**OWASP Rate Limiting Cheat Sheet**](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html#rate-limiting) — estrategias de limitación.
* Documentación de **bcrypt** y **argon2** para hashing de contraseñas.
