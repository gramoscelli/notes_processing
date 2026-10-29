### Guion de Clase: Prácticas de Seguridad en Código Web 

#### **Introducción**

1.  **Bienvenida y Contexto (5 min)**
    *   Iniciar la clase comentando la importancia de la ciberseguridad en el desarrollo web. "No basta con que la app funcione, ¡tiene que ser segura!"
    *   Explicar que el objetivo es entender las vulnerabilidades *desde el código* para poder prevenirlas y corregirlas.
    *   Enfoque práctico: "Vamos a ensuciarnos las manos".
    *   **Advertencia Crucial:** Recalcar la importancia de practicar *solo* en entornos controlados (DVWA, Juice Shop, etc.). "¡Nunca intenten esto en sistemas ajenos sin autorización!"

2.  **Visión General de Vulnerabilidades (5-10 min)**
    *   Mencionar que se cubrirán las más comunes (OWASP Top 10).
    *   Hacer un breve listado: SQLi, XSS, CSRF, Validación Débil, Autenticación Insegura.
    *   "Estas son las puertas de entrada más comunes para un atacante. Nuestro trabajo es cerrarlas."

---

#### **Módulo 1: Inyección SQL (SQLi) (45-60 min)**

1.  **Teoría y Concepto (10 min)**
    *   **¿Qué es?** Inyectar código SQL malicioso a través de entradas del usuario. "Piensen en la app como un traductor; si el usuario da una instrucción maliciosa, el traductor la ejecuta sin pensar."
    *   **¿Por qué ocurre?** Concatena directamente entradas de usuario en consultas SQL.
    *   **Ejemplo clásico:** `admin' --` o `' OR 1=1 --` en un login. Mostrar cómo `SELECT * FROM users WHERE username='admin' --' AND password='cualquiercosa'` se convierte en `SELECT * FROM users WHERE username='admin'` (todo lo demás es comentario).
    *   **Consecuencias:** Bypassear autenticación, extraer datos sensibles, manipular base de datos.

2.  **Práctica Guiada (30-40 min)**
    *   **Opción A (DVWA):**
        *   Instrucciones para montar DVWA (si no está hecho).
        *   Navegar a la sección de SQL Injection (Low Security).
        *   **Demostración:** El instructor muestra cómo inyectar `' OR 1=1 --` o similar en el campo de usuario/ID y lograr acceso/obtener información. 
        *   **Ejercicio para alumnos:** Que lo repliquen. "Ahora es su turno, intenten 'engañar' a la aplicación."
        *   **Guía para solución:** Discutir cómo se mitiga. Mostrar cómo subir el nivel de seguridad de DVWA y ver los cambios en el código, o usar el código de ejemplo.
    *   **Opción B (Código Autocontenido PHP/JS):**
        *   Distribuir el código PHP vulnerable.
        *   **Demostración:** Mostrar la línea vulnerable (`$query = "..."`) y cómo un input `admin' --` cambia la lógica de la consulta.
        *   **Ejercicio para alumnos:** Reproducir el ataque.
        *   **Guía para solución:** Corregir el código usando **consultas preparadas (PDO/MySQLi)**. Explicar `bindParam`, `execute`.
            ```php
            // Ejemplo de código seguro (PHP con PDO)
            $stmt = $conn->prepare("SELECT * FROM users WHERE username = :user AND password = :pass");
            $stmt->bindParam(':user', $usuario);
            $stmt->bindParam(':pass', $pass);
            $stmt->execute();
            ```
            "¡Ahora el motor de la base de datos sabe qué es dato y qué es código!"
    *   **Reflexión Post-práctica:** Verificar que el ataque ya no funciona. ¿Por qué las consultas preparadas lo evitan?

3.  **Mitigación Clave (5 min)**
    *   **Consultas Preparadas / Parametrizadas:** ¡La solución principal!
    *   Validación de entrada (filtrado de caracteres).
    *   Principio de mínimos privilegios en la BD.
    *   Usar ORMs que gestionen esto automáticamente (pero entender la base).

---

#### **Módulo 2: Cross-Site Scripting (XSS) (45-60 min)**

1.  **Teoría y Concepto (10 min)**
    *   **¿Qué es?** Inyectar código JavaScript o HTML malicioso en la página, ejecutado en el navegador de otros usuarios. "El atacante hace que *tu navegador* ejecute su código, no el servidor."
    *   **Tipos:** Reflejado, Almacenado, DOM. Brevemente explicar la diferencia.
    *   **¿Por qué ocurre?** La aplicación muestra contenido de usuario sin sanitizar/escapar.
    *   **Ejemplo:** `<script>alert('XSS')</script>` en un comentario o campo de búsqueda.
    *   **Consecuencias:** Robo de cookies/sesiones, redirecciones, defacing, spam.

2.  **Práctica Guiada (30-40 min)**
    *   **Opción A (DVWA/Juice Shop):**
        *   Navegar a la sección de XSS Reflected (Low Security).
        *   **Demostración:** Instructor inyecta `<script>alert(document.cookie)</script>` o similar en el campo de búsqueda. Mostrar cómo se ejecuta el alert. 
        *   **Ejercicio para alumnos:** Que repliquen. "Intenten robar la cookie de DVWA o al menos ejecutar un `alert`."
        *   Navegar a XSS Stored.
        *   **Demostración:** Instructor inyecta un script en un campo de comentario y recarga la página. Mostrar cómo persiste. 
        *   **Ejercicio para alumnos:** Replicar el XSS almacenado.
        *   **Guía para solución:** Subir nivel de seguridad o usar el código de ejemplo.
    *   **Opción B (Código Autocontenido HTML/JS/PHP):**
        *   Distribuir los archivos HTML/PHP vulnerables (ej. `echo $_GET['input']`).
        *   **Demostración:** Ingresar `<script>alert('¡Soy un XSS!')</script>` en el formulario y ver la ejecución.
        *   **Ejercicio para alumnos:** Reproducir los ataques.
        *   **Guía para solución:** Corregir el código PHP usando `htmlspecialchars()` o librerías de sanitización.
            ```php
            // Ejemplo de código seguro (PHP)
            echo htmlspecialchars($_GET['input'], ENT_QUOTES, 'UTF-8');
            ```
            "Con `htmlspecialchars`, `<` se convierte en `&lt;`, ¡así no se ejecuta como código!"
    *   **Reflexión Post-práctica:** Verificar que los scripts ya no se ejecutan.

3.  **Mitigación Clave (5 min)**
    *   **Sanitizar y Codificar (Escape):** SIEMPRE codificar la salida antes de mostrarla en HTML.
    *   Validación estricta de entrada.
    *   Content Security Policy (CSP).
    *   Cookies HttpOnly.

---

#### **Módulo 3: Cross-Site Request Forgery (CSRF) (45-60 min)**

1.  **Teoría y Concepto (10 min)**
    *   **¿Qué es?** Un atacante induce al navegador de un usuario autenticado a enviar una petición no deseada. "El navegador es leal a la víctima, pero lo engañan para que haga algo en secreto."
    *   **¿Por qué ocurre?** La aplicación confía ciegamente en las cookies de sesión y no verifica el origen de la petición.
    *   **Ejemplo:** Sitio malicioso con un `<img src="banco.com/transfer?cantidad=1000&destino=atacante">` o un formulario POST oculto.
    *   **Consecuencias:** Transferencias de dinero, cambio de contraseñas, eliminación de cuentas (todo bajo la identidad de la víctima).

2.  **Práctica Guiada (30-40 min)**
    *   **Opción A (DVWA):**
        *   Navegar a la sección de CSRF (Low Security). (Normalmente un cambio de contraseña de admin).
        *   **Demostración:** Instructor muestra la URL o el formulario POST legítimo. Luego abre una página HTML maliciosa (local) que envía la petición POST automáticamente. Mostrar cómo, estando autenticado en DVWA, la acción se ejecuta sin interacción. 
        *   **Ejercicio para alumnos:** Replicar el ataque. "¡Imaginen que es su banco y esto ocurre!"
        *   **Guía para solución:** Discutir la necesidad de un token anti-CSRF. Subir nivel de seguridad de DVWA para ver cómo se genera y verifica.
    *   **Opción B (Código Autocontenido PHP/HTML):**
        *   Distribuir *victima.php* (acción sensible sin protección) y *atacante.html*.
        *   **Demostración:** Mostrar cómo *atacante.html* fuerza una petición a *victima.php*.
        *   **Ejercicio para alumnos:** Replicar el ataque.
        *   **Guía para solución:** Modificar *victima.php* para **generar y verificar un token CSRF**.
            ```php
            // En el formulario legítimo (generar token):
            session_start();
            if (empty($_SESSION['csrf_token'])) {
                $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
            }
            // En el HTML:
            echo '<input type="hidden" name="csrf_token" value="' . $_SESSION['csrf_token'] . '">';

            // En el controlador (verificar token):
            if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
                die('CSRF Token inválido');
            }
            // Procede con la acción si el token es válido
            ```
            "Ahora, el sitio malicioso no puede adivinar este token, ¡la aplicación sabe que la petición es de su propio formulario!"
    *   **Reflexión Post-práctica:** Verificar que el ataque ya no es posible.

3.  **Mitigación Clave (5 min)**
    *   **Tokens Anti-CSRF:** ¡La defensa principal!
    *   Verificar cabeceras `Referer`/`Origin`.
    *   Usar métodos HTTP adecuados (POST para cambios de estado).
    *   Asegurarse de que el token sea *por usuario y por sesión*.

---

#### **Módulo 4: Validación de Entrada Débil (45-60 min)**

1.  **Teoría y Concepto (10 min)**
    *   **¿Qué es?** No verificar o filtrar correctamente los datos del usuario. "Si no revisamos lo que nos dan, ¡nos pueden dar cualquier cosa!"
    *   **¿Por qué ocurre?** Confianza en el usuario, solo validación en frontend, validación incompleta.
    *   **Ejemplo:** Campo de edad acepta texto, campo de email acepta "cualquiera", subir un `.php` disfrazado de imagen.
    *   **Consecuencias:** SQLi/XSS (si no se valida antes de usar), carga de archivos maliciosos, errores lógicos, DoS.

2.  **Práctica Guiada (30-40 min)**
    *   **Ejercicio de Bypass de Validación Cliente-Servidor:**
        *   Distribuir una página HTML con formulario (email, edad) con validación HTML5/JS (ej. `type="email"`, `min="18"`). Servidor simplemente hace `echo` o inserta sin validar.
        *   **Demostración:** Instructor muestra que el frontend bloquea inputs inválidos. Luego, usando DevTools (deshabilitar JS, remover `required`, etc.) o un proxy HTTP (Burp Suite o similar), muestra cómo enviar datos claramente inválidos (`edad="hola"`, `email="<script>..."`). El servidor los acepta. 
        *   **Ejercicio para alumnos:** Replicar el bypass. "¡Demostremos que la validación solo en el frontend es inútil para un atacante!"
        *   **Guía para solución:** Implementar **validación estricta en el servidor**.
            ```php
            // Ejemplo de validación en PHP
            $email = $_POST['email'];
            $age   = $_POST['age'];

            if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
                die("Email inválido.");
            }
            if (!is_numeric($age) || $age < 0 || $age > 120) {
                die("Edad inválida.");
            }
            // Si todo es válido, procesar...
            ```
            "El servidor debe ser el último y más confiable guardián de nuestros datos."
    *   **Reflexión Post-práctica:** Verificar que el servidor ahora rechaza los datos inválidos.

3.  **Mitigación Clave (5 min)**
    *   **Validar SIEMPRE en el servidor:** Tipo, longitud, formato, rango, contenido.
    *   **Listas Blancas:** Definir qué *está permitido*, no qué *está prohibido*.
    *   Sanitizar/Escapar *todos* los datos dinámicos.
    *   Nunca confiar en la validación del frontend.

---

#### **Módulo 5: Autenticación Insegura y Gestión de Sesiones (45-60 min)**

1.  **Teoría y Concepto (10 min)**
    *   **¿Qué es?** Debilidades en la identificación de usuarios y protección de cuentas. "Es el candado de la puerta de nuestra casa; si es débil, ¡adiós seguridad!"
    *   **¿Por qué ocurre?** Almacenamiento inseguro de contraseñas, falta de anti-fuerza bruta, sesiones mal gestionadas.
    *   **Ejemplo:** Contraseñas en texto plano, sin bloqueo de cuenta por intentos fallidos, IDs de sesión predecibles.
    *   **Consecuencias:** Robo de cuentas, escalada de privilegios.

2.  **Práctica Guiada (30-40 min)**
    *   **Caso 1: Fuerza Bruta / Credenciales Débiles (DVWA)**
        *   Navegar a Brute Force (Low Security).
        *   **Demostración:** Instructor muestra cómo probar contraseñas (ej. `password`, `123456`). Mencionar que un script automático lo haría en segundos. 
        *   **Ejercicio para alumnos:** Intentar adivinar la contraseña de un usuario de prueba sin restricciones.
        *   **Guía para solución:** Discutir e implementar (o simular) un contador de intentos fallidos con bloqueo temporal o CAPTCHA.
    *   **Caso 2: Almacenamiento Inseguro de Contraseñas (Código Autocontenido)**
        *   Distribuir código o una "base de datos" (CSV/TXT) con contraseñas en texto plano o MD5 sin salt.
        *   **Demostración:** Mostrar la base de datos y cómo una contraseña MD5 puede "crackearse" fácilmente online. 
        *   **Ejercicio para alumnos:** Crackear una contraseña simple si la tienen en MD5.
        *   **Guía para solución:** Modificar el código de registro/login para usar **hashing seguro con salt** (BCrypt, Argon2).
            ```php
            // Al registrar (PHP):
            $hashed_password = password_hash($plain_password, PASSWORD_BCRYPT);
            // Al verificar (PHP):
            if (password_verify($plain_password_input, $stored_hashed_password)) {
                // Login exitoso
            }
            ```
            "¡Nunca guardes contraseñas en texto plano! Usa algoritmos que las hagan imposibles de revertir."
    *   **Caso 3: Gestión de Sesión (Conceptual/WebGoat/Juice Shop)**
        *   Discutir IDs de sesión predecibles o cookies sin HttpOnly.
        *   **Demostración (si es posible en WebGoat/Juice Shop):** Mostrar cómo se roba una cookie de sesión (usando XSS de una práctica anterior) y se usa para suplantar.
        *   **Guía para solución:** Marcar cookies como `HttpOnly` y `Secure`, regenerar ID de sesión tras login, establecer expiración adecuada.

3.  **Mitigación Clave (5 min)**
    *   **Hashing seguro con salt:** BCrypt, Argon2 (¡nunca MD5 sin salt!).
    *   **Protección anti-fuerza bruta:** Limitar intentos, CAPTCHA, bloqueo.
    *   **Políticas de contraseñas fuertes.**
    *   **Gestión de sesiones segura:** IDs aleatorios, HttpOnly, Secure, expiración, regeneración tras login.
    *   **Autorización robusta:** Siempre verificar permisos en el servidor para cada acción.

---

#### **Cierre y Recursos (10-15 min)**

1.  **Recursos de Práctica Recomendados (5 min)**
    *   Recordar las herramientas: **DVWA, OWASP Juice Shop, WebGoat, bWAPP, Mutillidae II**.
    *   "Estas son sus 'cajas de arena' para seguir experimentando de forma segura."
    *   Enfatizar la instalación local (XAMPP, Docker) para cada alumno.

2.  **Filosofía de Desarrollo Seguro (5 min)**
    *   "No confíen en el usuario."
    *   "La seguridad es un proceso, no un evento."
    *   "Piensen como un atacante, pero construyan como un defensor."
    *   "Cada vulnerabilidad es una oportunidad para aprender y escribir mejor código."
    *   Animar a investigar más (OWASP Cheat Sheets).

3.  **Preguntas y Respuestas (5 min)**
    *   Abrir el espacio para dudas.

