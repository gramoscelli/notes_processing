# Prácticas de Seguridad en Código Web para Desarrolladores *Junior*

En esta sección se propone una serie de **prácticas de laboratorio
enfocadas en vulnerabilidades de código** comunes en aplicaciones web.
El objetivo es que estudiantes próximos a graduarse en programación web
adquieran nociones de ciberseguridad defensiva **entendiendo cómo
ocurren las fallas en el código y cómo corregirlas**. Las actividades
están pensadas para realizarse en equipos personales (por ejemplo,
montando aplicaciones web vulnerables en *localhost*), sin requerir
servidores externos. Se organizan las prácticas por tipo de
vulnerabilidad, cubriendo ejemplos concretos como inyección SQL, XSS,
CSRF, validación insuficiente de datos y autenticación insegura, entre
otras. Cada sección incluye ejercicios prácticos (usando aplicaciones
abiertas como **DVWA**, **OWASP Juice Shop**, **WebGoat**, etc., o
pequeños ejercicios en HTML/JS/PHP) y destaca las técnicas de mitigación
correspondientes.

## Inyección SQL (SQLi)

La **inyección SQL** ocurre cuando una aplicación incorpora entradas del
usuario en consultas SQL sin la debida sanitización o validación,
permitiendo al atacante alterar la consulta
original ([[1]](https://asawl.org/vulnerabilidades/01-inyeccion-sql), [[2]](https://asawl.org/vulnerabilidades/01-inyeccion-sql)).
Esto puede llevar a **bypassear autenticaciones** o manipular la base de
datos. Por ejemplo, en un formulario de inicio de sesión vulnerable, un
atacante podría ingresar como nombre de usuario la cadena `admin' --` (o
`' OR 1=1 --`) y cualquier contraseña; si el código concatena
directamente estos valores en la consulta SQL, la sentencia `OR 1=1`
hará que la condición siempre sea verdadera, otorgando acceso sin
credenciales
válidas[[3]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=Ejemplo%3A%20Si%20un%20sitio%20web,acceso%20sin%20una%20contrase%C3%B1a%20v%C3%A1lida), [[4]](https://asawl.org/vulnerabilidades/01-inyeccion-sql#:~:text=%27%20OR%201%3D1%20).

**Práctica propuesta:** Montar el escenario de un formulario de login
vulnerable y explotar la inyección SQL, **luego implementar la solución
segura**. Esto puede hacerse de dos formas:

- **Usando una aplicación vulnerable existente:** Por ejemplo, desplegar
  **Damn Vulnerable Web Application (DVWA)** en modo *low security* para
  el módulo *SQL Injection*. DVWA es una aplicación PHP/MySQL
  deliberadamente insegura (con niveles de dificultad) diseñada para
  practicar fallas como inyecciones SQL, XSS,
  etc.[[5]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=No%20se%20debe%20confundir%20con,SQL%20y%20otros%20ataques%20comunes).
  Intentar el ataque mencionado (`' OR 1=1`) u otras
  técnicas de SQLi en DVWA y observar cómo logran extraer datos o evadir
  la autenticación. Después, se les puede guiar para subir el nivel de
  seguridad de DVWA a *medium/high* e intentar modificar el código
  fuente para aplicar protecciones (DVWA incluye pistas de qué cambia
  entre niveles).

- **Ejercicio auto-contenido en código:** Proporcionar un simple código
  en PHP (o el stack que manejen) que tenga una consulta vulnerable, por
  ejemplo:

```

    // Ejemplo didáctico de código inseguro
    $usuario = $_POST['user'];
    $pass   = $_POST['pass'];
    $query  = "SELECT * FROM users WHERE username='$usuario' AND password='$pass'";
    $result = mysqli_query($conn, $query);
```
En este código, ingresar `user = admin' --` *bypassa* la verificación.
El ejercicio sería reproducir el ataque y luego **corregir el código**
usando **consultas preparadas** (con parámetros) u otras mitigaciones
apropiadas.

**¿Por qué ocurre?** La causa principal es no validar ni sanitizar
correctamente los datos de entrada antes de usarlos en la
consulta[[1]](https://asawl.org/vulnerabilidades/01-inyeccion-sql#:~:text=La%20inyecci%C3%B3n%20SQL%20en%20Laravel,o%20utilizar%20consultas%20sin%20parametrizar)[[6]](https://asawl.org/vulnerabilidades/01-inyeccion-sql#:~:text=).
El motor SQL interpreta las comillas y operadores inyectados como parte
de la consulta. En el ejemplo, la aplicación confía ciegamente en
`usuario` y `pass` recibidos.

**Cómo mitigar:** Se enfatizará la importancia de usar **consultas
parametrizadas o preparadas** (evitando la concatenación directa de
entradas)[[7]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,a%20la%20base%20de%20datos).
Asimismo, implementar **validación de entrada rigurosa** (rechazar
caracteres o patrones inesperados) y aplicar *escapado* de caracteres
especiales si es necesario. Otras buenas prácticas incluyen aplicar
**principio de mínimos privilegios** en la base de datos (de modo que
incluso si ocurre una inyección, el daño esté
limitado)[[8]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=abstracci%C3%B3n%20que%20protege%20contra%20inyecciones,caso%20de%20una%20inyecci%C3%B3n%20exitosa).
Usar *ORMs* o frameworks que manejan la capa de datos también ayuda a
prevenir inyecciones al abstraer las
consultas[[7]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,a%20la%20base%20de%20datos).
Tras aplicar la solución, los estudiantes deben comprobar que el ataque
`' OR 1=1` u otras variantes ya no funcionan.

## Cross-Site Scripting (XSS)

Los ataques de **Cross-Site Scripting (XSS)** consisten en inyectar
código JavaScript o HTML malicioso en una página web para que sea
ejecutado por el navegador de otros
usuarios[[9]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=Los%20ataques%20XSS%20son%20una,luego%20ejecutados%20por%20otros%20usuarios).
Esto ocurre típicamente cuando la aplicación muestra contenidos
ingresados por usuarios (por ejemplo, comentarios, campos de búsqueda,
etc.) sin sanitizarlos ni validar su formato. Un ejemplo clásico es
escribir un comentario que contiene una etiqueta
`<script>alert('XSS')</script>` en un foro vulnerable; al ver ese
comentario, el navegador de cualquier usuario ejecutará el `alert` (o un
script malicioso realista que podría robar *cookies* de sesión,
redirigir al usuario,
etc.)[[10]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=Ejemplo%3A%20Un%20usuario%20podr%C3%ADa%20insertar,redirigiendo%20a%20sitios%20web%20maliciosos).
XSS puede ser **reflejado** (el payload viaja en la petición y es
devuelto inmediatamente, p. ej. en el resultado de un formulario) o
**almacenado** (el payload se guarda en la base de datos y afecta a
cualquier usuario que visite posteriormente esa página). También existe
XSS de tipo **DOM** (manipulación del documento en el lado del cliente).

**Práctica propuesta:** Explorar un caso de XSS reflejado y otro de XSS
almacenado, identificando la causa y aplicando defensas en el código.

- **Con DVWA u otra app vulnerable:** DVWA incluye retos de XSS
  reflejado y almacenado en distintos niveles de seguridad. Usar el módulo *Reflected XSS* en nivel bajo para
  insertar un script sencillo (como un `alert`) en un campo de entrada y
  observar cómo se ejecuta en la
  respuesta[[11]](https://tatisbuild.medium.com/explorando-vulnerabilidades-en-owasp-juice-shop-6ab8ff69ed6f#:~:text=1,Juice%20Shop%20simula%20configuraciones%20incorrectas).
  Luego, pueden intentar algo más elaborado como robar la cookie de
  sesión (DVWA suele mostrarla en pantalla para facilitar el ejercicio).
  Para XSS almacenado, DVWA tiene una sección donde se pueden dejar
  comentarios o mensajes que otros usuarios (o el mismo usuario al
  recargar) verán, permitiendo persistir un `<script>` malicioso. Tras
  explotar ambos casos, el reto es modificar el código fuente o
  configuraciones para neutralizar el ataque, y probar nuevamente.
  *(Nota: En DVWA niveles* medium/high*, el mismo ejercicio muestra qué
  contramedidas se van añadiendo, como funciones de sanitización o*
  escaping*.)*

- **Ejercicio autónomo HTML/JS:** Como alternativa, se puede
  proporcionar un par de archivos sencillos: una página HTML con un
  formulario que envía parámetros (por GET o POST) a un segundo archivo
  (PHP/HTML) que simplemente imprime lo recibido. Sin ninguna
  prevención, el segundo archivo podría hacer `echo $_GET['input']`
  directamente, reproduciendo la vulnerabilidad. El alumnado inserta un
  payload (`<script>...`) en el formulario y ve el efecto. Luego, debe
  corregir el código introduciendo **filtros o sanitización** (por
  ejemplo, en PHP usar `htmlspecialchars()` o eliminar etiquetas
  HTML)[[12]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,ejecuci%C3%B3n%20de%20scripts%20no%20autorizados),
  y validar que ya no se ejecutan las etiquetas de script.

**¿Por qué ocurre?** La vulnerabilidad XSS se debe a **falta de
validación/sanitización de la entrada del usuario antes de incorporarla
en la página de
respuesta**[[13]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,XSS).
El navegador no distingue si el script viene del desarrollador o de un
atacante si este logró inyectarlo en la página; por ello, es
responsabilidad del código del lado servidor (o incluso defensas del
lado cliente) asegurarse de que entradas de usuario no contengan scripts
ejecutables.

**Cómo mitigar:** Las defensas incluyen **sanitizar o codificar (escape)
cualquier dato dinámico antes de insertarlo en
HTML**[[12]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,ejecuci%C3%B3n%20de%20scripts%20no%20autorizados).
Por ejemplo, convertir `<` en `&lt;` y así sucesivamente, o remover
etiquetas sospechosas. Implementar **validación estricta de datos**
(rechazar entrada que contenga `<script>` u otras cargas sospechosas si
no son esperadas) también
ayuda[[14]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=potencialmente%20peligrosos%20antes%20de%20mostrarlos,para%20que%20sean%20accesibles%20solo).
Otra capa es usar **Content Security Policy (CSP)** para restringir qué
scripts puede cargar el navegador desde la
página[[15]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=cumplan%20con%20un%20formato%20esperado%2C,scripts%2C%20utilizando%20la%20bandera%20HttpOnly).
Adicionalmente, configurar cookies **HttpOnly** (para que no sean
accesibles vía JS) y usar correctos atributos de contexto (por ejemplo,
si un dato de usuario se inserta en un atributo HTML, escapar comillas,
etc.). Después de aplicar estas mitigaciones en el ejercicio, los
estudiantes deberían comprobar que el código malicioso ya no se ejecuta
y discutir qué filtrado implementaron.

## Cross-Site Request Forgery (CSRF)

La vulnerabilidad de **Cross-Site Request Forgery (Falsificación de
Solicitud en Sitio Cruzado)** permite a un atacante inducir al navegador
de un usuario autenticado a enviar peticiones no deseadas en su nombre,
aprovechando la sesión activa de la
víctima[[16]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,CSRF).
En otras palabras, un usuario inicia sesión en una aplicación web (por
ejemplo, su banco en línea) y luego, sin cerrar sesión, visita un sitio
malicioso; este sitio puede contener un código (por ejemplo, un
formulario autoejecutado, una imagen *\<img\>* o *fetch()* invisible)
que envía una petición al sitio legítimo (el banco) usando las *cookies*
de sesión del usuario víctima. Si la aplicación vulnerable no distingue
entre una petición legítima del usuario y una forzada externamente, el
atacante podría lograr acciones como transferir dinero, cambiar la
contraseña del usuario, etc., sin su
consentimiento[[17]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=En%20un%20ataque%20CSRF%2C%20el,web%20controlado%20por%20el%20atacante)[[18]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=Ejemplo%3A%20Supongamos%20que%20un%20usuario,trata%20la%20solicitud%20como%20leg%C3%ADtima).

**Práctica propuesta:** Simular un ataque CSRF y luego implementar la
protección con *tokens* o verificaciones de origen en el código de la
aplicación.

- **Usando DVWA (CSRF):** DVWA posee un módulo de CSRF con niveles de
  seguridad. En nivel bajo, típicamente hay una función (por ejemplo,
  cambiar la contraseña del usuario administrador) implementada
  simplemente con una petición POST sin medidas anti-CSRF. Los
  estudiantes pueden crear una página HTML maliciosa (puede ser local,
  incluso un simple archivo `.html` abierto en el navegador) que
  contenga un formulario oculto o un script JavaScript que, al abrirse,
  envíe automáticamente una petición POST al endpoint vulnerable de DVWA
  (por ejemplo, */vulnerabilities/csrf/*) para cambiar la contraseña del
  admin. Si el estudiante está autenticado en DVWA en otra pestaña, al
  cargar la página maliciosa logrará la acción (notarán que la
  contraseña del admin cambió sin utilizar el formulario legítimo). Este
  experimento les permite *entender la facilidad con que un atacante
  puede explotar sesiones activas*. Luego se les pide inspeccionar cómo
  se podría evitar: al subir el nivel de seguridad de DVWA o consultando
  documentación, descubrirán que la defensa típica es incluir un **token
  anti-CSRF** impredecible en el formulario legítimo y verificarlo en el
  servidor[[19]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=%2A%20Tokens%20Anti,seguridad%20est%C3%A1ndar%20en%20navegadores%20web).
  Pueden intentar implementar un token sencillo en el código fuente de
  DVWA nivel bajo (o en un código proporcionado) y comprobar que con esa
  modificación, la petición forjada desde la página maliciosa ya no
  surte efecto (porque carece del token correcto).

- **Ejercicio casero simplificado:** Proporcionar dos archivos:
  *victima.php* (simula la aplicación vulnerable) y *atacante.html*. En
  *victima.php*, tener una acción sensible, ej. *resetear contraseña* o
  *cambiar email*, que tome parámetros vía POST. Sin protección, los
  alumnos verán que *atacante.html* (con un pequeño formulario que hace
  POST automático a *victima.php*) logra ejecutar la acción. La tarea es
  modificar *victima.php* para requerir un **token CSRF** en cada
  formulario (generar un token aleatorio por sesión y verificarlo), o al
  menos verificar la cabecera *Referer/Origin*. Al repetir el ataque con
  el token implementado, la acción debe fallar. Esto refuerza el
  concepto de que la aplicación debe asegurarse de que cada solicitud
  provenga intencionalmente del usuario
  legítimo[[20]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=Proteger%20una%20aplicaci%C3%B3n%20web%20contra,provienen%20efectivamente%20del%20usuario%20leg%C3%ADtimo).

**¿Por qué ocurre?** CSRF es posible cuando **la aplicación confía
únicamente en la credencial de sesión (cookie) para autorizar
solicitudes, sin pasos adicionales de verificación**. El navegador envía
automáticamente las cookies guardadas en cada petición al dominio
correspondiente; un atacante aprovecha esto creando una solicitud desde
otro sitio/herramienta de manera que el navegador de la víctima incluya
las cookies válidas. Si el servidor no tiene forma de distinguir una
solicitud legítima desde la propia aplicación de una fabricada en otra
parte, ejecutará la acción pensando que fue el
usuario[[16]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,CSRF).

**Cómo mitigar:** La defensa principal son los **tokens anti-CSRF**:
cadenas aleatorias únicas que la aplicación genera y entrega al cliente
(por ejemplo, como campo oculto en formularios o parámetro en la URL) y
espera recibir de vuelta. Solo las páginas legítimas de la aplicación
poseen el token correcto, por lo que una petición forjada (que el
atacante no puede decorar con el token secreto de la víctima) será
rechazada[[19]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=%2A%20Tokens%20Anti,seguridad%20est%C3%A1ndar%20en%20navegadores%20web).
Otras medidas complementarias incluyen verificar la **cabecera
Referer/Origin** de las peticiones (deben coincidir con el dominio de la
aplicación) y asegurarse de usar métodos HTTP adecuados (ej. muchas apps
requieren *POST* para operaciones de estado cambiante, aunque esto por
sí solo no frena CSRF completamente). Las **políticas de mismo origen
(Same-Origin Policy)** del navegador ya impiden que un script de un
sitio lea respuestas de otro dominio, pero no evitan que se envíen
peticiones; por ello, el token sigue siendo
necesario[[21]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,seguridad%20est%C3%A1ndar%20en%20navegadores%20web).
Una vez implementadas estas protecciones en el ejercicio, los alumnos
comprobarán que el ataque ya no es posible y habrán aprendido cómo
incorporar esta defensa en sus futuros desarrollos.

## Validación de Entrada Débil o Insuficiente

Las **fallas de validación de entrada** ocurren cuando una aplicación no
verifica o filtra correctamente los datos ingresados por el usuario
antes de
procesarlos[[22]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=Un%20fallo%20de%20validaci%C3%B3n%20de,cumple%20con%20el%20formato%20esperado).
Esto abarca casos donde la validación está ausente, es demasiado laxa o
se confía solo en el lado cliente. Una validación débil **abre la puerta
a multitud de ataques**, ya que inputs inesperados o maliciosos pueden
desencadenar comportamientos no
previstos[[23]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=Los%20fallos%20de%20validaci%C3%B3n%20de,una%20variedad%20de%20ataques%2C%20incluyendo).
Por ejemplo, muchos ataques como inyecciones SQL o XSS son posibles
*gracias a* que no hay validaciones limitando longitud, formato o
caracteres
permitidos[[24]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=,atacante%20podr%C3%ADa%20enviar%20una%20gran).
Asimismo, sin validaciones robustas podrían ocurrir otros problemas,
como permitir **carga de archivos peligrosos** (subir un *.php* como
imagen, logrando ejecución remota) o provocar errores lógicos/caídas
(incluso DoS al enviar cargas excesivamente
grandes)[[25]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=%2A%20Cross,nombres%20de%20usuario%2C%20contrase%C3%B1as%20o).
Un caso común es confiar únicamente en la **validación del lado cliente
(JavaScript)**: un atacante puede deshabilitar o manipular esa
validación usando las herramientas de desarrollador del navegador,
enviando datos inválidos que el servidor procesará si este no realiza su
propia
verificación[[26]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=Los%20fallos%20de%20validaci%C3%B3n%20de,entrada%20suelen%20ocurrir%20debido%20a).

**Práctica propuesta:** Analizar un módulo de la aplicación con
validaciones insuficientes, explotarlo y luego fortalecer esas
validaciones en el código.

- **Ejercicio de bypass de validación cliente-servidor:** Preparar una
  pequeña página con un formulario (por ejemplo, registro de usuario con
  campos de email, edad, etc.) donde la única validación aplicada sea en
  HTML5/JS (por ejemplo, campos `required`, tipo `number` para edad,
  longitud máxima en el input, etc.), pero **sin validación en el
  servidor**. Montar un script en el servidor que simplemente muestra lo
  enviado o lo inserta en una base de datos sin comprobar. Los
  estudiantes inicialmente ven que al usar el formulario de manera
  normal, se impide enviar datos mal formados (por ejemplo, el campo
  email requiere `@`, la edad debe ser número). Luego se les guía para
  **burlar esas validaciones del lado cliente**: por ejemplo, usando las
  DevTools para habilitar el botón de submit aunque el formulario esté
  inválido, o enviando manualmente la petición HTTP modificada (con un
  proxy o una herramienta sencilla). De este modo, logran enviar datos
  completamente erróneos (texto en el campo numérico, script en el campo
  nombre, etc.) y el servidor los acepta. Esta actividad les demuestra
  la necesidad de no depender solo del cliente.

- **Validación robusta en servidor:** A continuación, se indica a los
  alumnos que implementen en el código servidor comprobaciones
  estrictas: por ejemplo, usar expresiones regulares para validar
  formato de email, asegurar que la edad sea un número dentro de cierto
  rango, eliminar o escapar caracteres HTML en campos de texto, etc. Si
  se permite subir archivos en algún ejercicio, asegurarse de validar la
  extensión/MIME y tamaño en el servidor. Un recurso útil es seguir las
  recomendaciones OWASP de validar tipo, tamaño, formato y rango de
  todos los datos
  ingresados[[27]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,y%20an%C3%A1lisis%20de%20c%C3%B3digo%20est%C3%A1tico).
  Se puede hacer referencia a frameworks de desarrollo que facilitan
  estas validaciones (por ejemplo, si están familiarizados con algún
  *framework* como Laravel, mostrarles cómo usar las reglas de
  validación del framework en lugar de confiar en el
  frontend)[[28]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=Para%20aplicar%20la%20validaci%C3%B3n%20de,Form%20Request%20Validation)[[29]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=%24validateData%20%3D%20%24request).
  Por último, repetir el intento de enviar datos maliciosos tras
  endurecer la validación y verificar que ahora son rechazados o
  limpiados correctamente.

**¿Por qué ocurre?** A menudo los desarrolladores novatos confían en que
\"el usuario no ingresará algo raro\" o que las validaciones de la
interfaz son suficientes, lo cual es un error. Los **fallos de
validación** suelen darse por: no validar nada, validar de forma
incompleta (ej. chequear solo si el campo no está vacío pero no su
contenido), validar incorrectamente (lógica equivocada que se puede
evadir) o suponer que el *frontend* ya se
encargó[[26]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=Los%20fallos%20de%20validaci%C3%B3n%20de,entrada%20suelen%20ocurrir%20debido%20a).
Un atacante siempre puede modificar la petición al nivel HTTP, por lo
que cualquier lógica de validación debe repetirse del lado servidor.

**Cómo mitigar:** La regla de oro es **\"no confíes en el usuario\"**:
**toda entrada debe ser tratada como no confiable hasta verificarla**.
Esto implica implementar validaciones en el servidor para *cada* dato
recibido: asegurarse de tipo (p.ej., que un ID numérico realmente sea
numérico), longitud (no aceptar cadenas excesivamente largas donde no se
esperan), formato (por ejemplo fechas válidas, emails con sintaxis
correcta) y contenido (filtrar caracteres especiales si no son
necesarios)[[27]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,y%20an%C3%A1lisis%20de%20c%C3%B3digo%20est%C3%A1tico).
Un enfoque práctico es utilizar **listas blancas** de valores o patrones
permitidos[[30]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=hacer%20en%20caso%20de%20una,usuarios%2C%20permitiendo%20s%C3%B3lo%20caracteres%20espec%C3%ADficos),
en lugar de listas negras de caracteres prohibidos, ya que es más seguro
definir exactamente qué es válido. Además, utilizar funciones de
sanitización/escape proporcionadas por el lenguaje o framework para
tratar cualquier caracter especial o potencialmente peligroso. Si la
aplicación requiere ciertas entradas potencialmente peligrosas (ej.
contenido HTML de usuarios en un editor de texto enriquecido), entonces
aplicar sanitizadores HTML que remuevan etiquetas/script indeseados. En
resumen, robustecer la validación de entrada cerrará la puerta a muchos
vectores de ataque que aprovechan entradas
maliciosas[[23]](https://asawl.org/vulnerabilidades/03-fallos-validacion-de-entrada#:~:text=Los%20fallos%20de%20validaci%C3%B3n%20de,una%20variedad%20de%20ataques%2C%20incluyendo).

## Autenticación Insegura y Gestión de Sesiones

La categoría de **autenticación insegura** abarca múltiples debilidades
en cómo una aplicación maneja la identificación de usuarios y la
protección de sus cuentas. Incluye problemas como **credenciales
débiles** (uso de contraseñas triviales o por defecto, falta de
requisitos de complejidad), **almacenamiento inseguro de contraseñas**
(guardarlas en texto plano o con hashes débiles), falta de controles
anti-*brute force*, sesiones expuestas o mal protegidas, y lógica de
autorización incorrecta, entre
otros[[31]](https://asawl.org/vulnerabilidades/04-autenticacion-autorizacion-insegura#:~:text=,validar%20adecuadamente%20los%20datos%20de).
Un sistema de login mal implementado puede permitir que atacantes
accedan sin permiso o escalen privilegios. Por ejemplo, si una
aplicación no limita los intentos de login, un atacante puede probar
miles de contraseñas hasta acertar (*fuerza bruta*). DVWA, en su módulo
*Brute Force*, ilustra esto permitiendo múltiples intentos de
contraseña; los estudiantes pueden usar una lista de contraseñas comunes
para demostrar lo fácil que sería adivinar una credencial débil cuando
no hay bloqueo de cuenta. Otro ejemplo: **almacenar contraseñas en texto
plano** en la base de datos. Si los estudiantes exploran una app
vulnerable (como **OWASP Juice Shop** o analizan el esquema de DVWA),
pueden ver que algunas implementaciones intencionalmente inseguras
guardan las contraseñas sin cifrar o con hashes fácilmente revertibles
(e.g., MD5 sin *salt*). Esto les permite experimentar extrayendo hashes
y *crackeándolos* con diccionarios para entender el riesgo.

**Práctica propuesta:** Revisar la implementación de autenticación de
una aplicación vulnerable, explotar sus fallos, y luego aplicar mejoras
de seguridad en el código.

- **Caso DVWA/Mutillidae (fuerza bruta y credenciales por defecto):**
  Los estudiantes pueden usar DVWA *low security* para el reto de fuerza
  bruta. DVWA tiene un usuario admin con password conocida (`password`
  por defecto). La práctica consiste en escribir o usar una pequeña
  herramienta (incluso un simple script o **Burp Intruder** si
  estuvieran usando herramientas, aunque aquí quizás manual o con
  código) que pruebe múltiples contraseñas al endpoint de login.
  Comprobarán que pueden descubrir la contraseña en poco tiempo debido a
  la falta de restricciones. Tras esto, discutir **cómo debería
  mitigarse**: imponer *captcha* tras X intentos fallidos, bloqueo
  temporal de cuenta, monitorizar IP, etc. *(Si no se desea usar
  herramientas automáticas, el instructor puede simplemente demostrar
  qué tan rápido cae una contraseña débil sabiendo que es
  \"password\").* También, muchas aplicaciones de prácticas tienen
  credenciales por defecto (admin/admin), lo cual es otro tema para
  mencionar: instar a cambiar contraseñas por defecto en entornos
  reales.

- **Caso almacenamiento de contraseñas:** Montar un pequeño escenario
  donde las credenciales de usuario se almacenan en formato legible. Por
  ejemplo, en **Mutillidae** o **bWAPP** existen páginas de
  administración que muestran usuarios y contraseñas almacenadas
  (deliberadamente inseguro) para ilustrar riesgos. Alternativamente,
  proveer a los alumnos un volcado de base de datos con contraseñas MD5
  y ver si pueden descifrarlas usando herramientas en línea o
  diccionarios comunes. Tras este ejercicio de **explotación**, pedirles
  que cambien el código para almacenar las contraseñas de forma segura:
  usando **algoritmos de hash fuertes con *salt*** (p. ej., BCrypt,
  Argon2) en lugar de texto plano o hashes
  rápidos[[32]](https://asawl.org/vulnerabilidades/04-autenticacion-autorizacion-insegura#:~:text=factores.%20,validar%20adecuadamente%20los%20datos%20de).
  Asimismo, recalcar la necesidad de **políticas de contraseñas
  fuertes** (mínimo de longitud, complejidad, no reutilización) y
  posiblemente **autenticación de dos factores** en sistemas reales
  críticos.

- **Gestión de sesión:** Otra práctica es examinar cómo la app maneja
  las sesiones de usuario. Un ejemplo sencillo es verificar si el ID de
  sesión es predecible o expira apropiadamente. En **WebGoat** o **Juice
  Shop** hay lecciones donde, por ejemplo, se roba una cookie de sesión
  (usando XSS) y se reutiliza en otra máquina para suplantar al usuario,
  destacando la importancia de marcar cookies como HttpOnly y Secure. Un
  ejercicio complementario podría ser modificar la configuración para
  añadir dichas banderas o reducir el tiempo de expiración de sesión y
  ver el efecto.

**¿Por qué ocurre?** Muchas de estas fallas provienen de una
implementación simplista de la autenticación. Por ejemplo,
desarrolladores inexpertos podrían almacenar contraseñas directamente
\"porque es más fácil\", o no imaginar que alguien intente miles de
combinaciones de contraseña. La falta de *hashing* robusto significa que
si la base de datos es comprometida, las contraseñas caen en texto claro
inmediatamente[[32]](https://asawl.org/vulnerabilidades/04-autenticacion-autorizacion-insegura#:~:text=factores.%20,validar%20adecuadamente%20los%20datos%20de).
La ausencia de bloqueo de fuerza bruta asume que \"nadie intentará
tantas contraseñas\", cosa que en la realidad automatizada es trivial.
Sesiones inseguras (IDs secuenciales, no expiración) asumen que un
atacante no podrá robar o adivinar un identificador, lo cual no es
cierto.

**Cómo mitigar:** Seguir prácticas de **desarrollo seguro en
autenticación**. Algunas mejoras clave:  
- **Enforce** políticas de contraseñas fuertes y únicas (y educar a los
usuarios a no reutilizarlas).  
- **Almacenar contraseñas cifradas con hash seguro** y *salt* aleatorio
por usuario (nunca guardar en
plano)[[33]](https://asawl.org/vulnerabilidades/04-autenticacion-autorizacion-insegura#:~:text=factores.%20,o%20tokens%20de%20sesi%C3%B3n%20impredecibles).  
- Implementar **protecciones contra fuerza bruta**: limitar intentos,
añadir retrasos crecientes, CAPTCHA tras varios fallos, etc.  
- **Gestionar sesiones de forma segura:** usar identificadores
aleatorios de suficiente longitud, marcarlos con HttpOnly y Secure,
regenerar el ID tras login, establecer expiración y *logout* inactivo.  
- **Autorización robusta:** Asegurarse de que cada función verifica los
permisos del usuario (evitar *escalada de privilegios* por omisión de
controles). Esto significa tener comprobaciones de roles en cada acción
crítica en el código, para prevenir que un usuario normal acceda a
funciones de administrador, por
ejemplo[[34]](https://asawl.org/vulnerabilidades/04-autenticacion-autorizacion-insegura#:~:text=tokens%20de%20sesi%C3%B3n%20impredecibles.%20,que%20no%20deber%C3%ADan%20tener%20acceso).

Estas medidas deben integrarse en el código del aplicativo y/o mediante
frameworks que provean módulos de autenticación ya probados. Los
estudiantes, tras implementar algunas de estas mejoras en la práctica
(por ejemplo, reemplazar almacenamiento plano por hash BCrypt en el
ejercicio dado, o añadir un contador de intentos fallidos), comprenderán
cómo se elevó significativamente la seguridad de la aplicación. Además,
OWASP provee guías de verificación (ASVS) que listan requisitos de
seguridad en autenticación que pueden explorarse para profundizar.

## **Recursos de Práctica Recomendados**

Para realizar las prácticas sugeridas, se recomienda utilizar
aplicaciones deliberadamente vulnerables de código abierto, las cuales
permiten experimentar de forma segura con todas estas fallas. A
continuación se listan algunas de las más utilizadas (todas se pueden
ejecutar localmente en el equipo del alumno, por ejemplo mediante
XAMPP/WAMP, Docker, etc., sin necesidad de acceso a servidores
externos):

- **Damn Vulnerable Web Application (DVWA):** Aplicación web PHP-MySQL
  intencionalmente vulnerable, con múltiples niveles de seguridad.
  Incluye ejercicios de inyección SQL, XSS, CSRF, inclusión de archivos,
  comandos del sistema, fuerza bruta, entre
  otros[[5]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=No%20se%20debe%20confundir%20con,SQL%20y%20otros%20ataques%20comunes)[[35]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=Actualmente%2C%20contiene%2020%20vulnerabilidades%20en,Fuerza%20Bruta%2C%20CSRF%2C%20entre%20otras).
  Es ideal para practicar tanto la explotación de cada vulnerabilidad en
  nivel *Low* como la defensa al aumentar el nivel (observando qué
  contramedidas se
  implementan)[[36]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=seguridad%20por%20igual,SQL%20y%20otros%20ataques%20comunes).
  Disponible para descarga en su sitio oficial (o via contenedores
  Docker).

- **OWASP Juice Shop:** Aplicación moderna (JavaScript/Node.js) que
  simula una tienda en línea vulnerable. Cubre **todas las
  vulnerabilidades OWASP Top 10** y más, incluyendo inyecciones
  SQL/NoSQL, XSS reflejado y almacenado, *broken auth*, exposición de
  datos sensibles,
  etc.[[37]](https://tatisbuild.medium.com/explorando-vulnerabilidades-en-owasp-juice-shop-6ab8ff69ed6f#:~:text=OWASP%20Juice%20Shop%20es%20un,habilidades%20en%20pruebas%20de%20penetraci%C3%B3n)[[11]](https://tatisbuild.medium.com/explorando-vulnerabilidades-en-owasp-juice-shop-6ab8ff69ed6f#:~:text=1,Juice%20Shop%20simula%20configuraciones%20incorrectas).
  Trae desafíos gamificados con una \"tabla de puntuación\" para
  encontrar las fallas. Es muy adecuada para alumnos, pues muestra de
  forma didáctica cómo se explotan las fallas y da pistas para
  corregirlas. Se ejecuta fácilmente en local (por Node o Docker).

- **OWASP WebGoat:** Plataforma educativa mantenida por OWASP. Consiste
  en una aplicación JEE intencionalmente insegura, estructurada en
  **lecciones interactivas** sobre distintas vulnerabilidades web
  (inyección SQL, XSS, CSRF, errores de configuración,
  etc.)[[38]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=Otra%20entrada%20de%20OWASP%20en,testing)[[39]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=,Codificaci%C3%B3n%20Unicode).
  Cada lección ofrece teoría y un ejercicio práctico donde el estudiante
  debe explotar la vulnerabilidad en la app y luego implementar la
  solución. WebGoat proporciona un entorno guiado excelente para
  autoaprendizaje, ejecutable en Windows, Linux o Mac (vía Java o un
  contenedor).

- **bWAPP (Buggy Web Application):** Aplicación web PHP/MySQL con más de
  **100 vulnerabilidades** basadas en OWASP Top
  10[[40]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=Lo%20que%20hace%20%C3%BAnico%20a,Algunas%20de%20las%20vulnerabilidades%20son).
  Incluye XSS, CSRF, inyecciones de diversos tipos (SQL, comandos OS,
  LDAP, etc.), sesiones, subida de archivos, DoS, entre otras. Es muy
  completa para explorar fallas menos comunes también. Se instala
  localmente (entorno LAMP) o se puede usar su VM llamada *BeeBox*.

- **OWASP Mutillidae II:** Otra aplicación PHP/MySQL vulnerable, fácil
  de desplegar sobre XAMPP/WAMP. Contiene más de **40 vulnerabilidades,
  cubriendo la mayoría del Top 10
  OWASP**[[41]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=https%3A%2F%2Fgithub).
  Viene con una interfaz didáctica que incluso muestra consejos y ayuda
  para cada vulnerabilidad. Ideal para practicar explotación y luego
  refactorizar el código con medidas correctivas.

> **Nota:** Antes de empezar con estas herramientas, es recomendable
> recordar a los estudiantes que **solo deben practicar en entornos
> controlados y con aplicaciones diseñadas para tal fin**. Probar estas
> técnicas en sistemas ajenos sin autorización es ilegal. Los recursos
> mencionados (DVWA, Juice Shop, WebGoat, bWAPP, Mutillidae) están
> creados específicamente para aprendizaje, proporcionando un entorno
> legal y seguro para
> experimentar[[42]](https://esgeeks.com/sitios-web-vulnerables-pentesting/#:~:text=principales%20vulnerabilidades%20de%20OWASP,pueden%20practicar%20el%20hacking%20web).

Cada práctica realizada debe ir acompañada de una reflexión sobre cómo
habría que integrar esas defensas en proyectos reales de desarrollo web.
Con estos ejercicios, los alumnos comprenderán en la práctica *por qué*
surgen las vulnerabilidades y *cómo* evitarlas mediante buenas prácticas
de codificación
segura[[43]](https://tatisbuild.medium.com/explorando-vulnerabilidades-en-owasp-juice-shop-6ab8ff69ed6f#:~:text=2,pueden%20escribir%20c%C3%B3digo%20m%C3%A1s%20seguro).
Al finalizar el curso, habrán fortalecido su mentalidad defensiva,
pudiendo identificar en su propio código patrones peligrosos y aplicar
mitigaciones antes de que se conviertan en brechas de seguridad.

**Referencias:** Estas prácticas se basan en vulnerabilidades conocidas
del OWASP Top 10 y en laboratorios abiertos mencionados. Para mayor
profundidad teórica, se pueden consultar recursos como la documentación
de OWASP (ej. **OWASP Cheat Sheets** sobre cada vulnerabilidad) y guías
de seguridad nacionales (INCIBE en España, etc.), que complementan la
parte práctica con recomendaciones
formales[[44]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=)[[45]](https://ciberseguridad.comillas.edu/inyecciones-sql-csrf-y-xss/#:~:text=,INCIBE).

