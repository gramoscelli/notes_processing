# GUÍA COMPLETA DE INTRODUCCIÓN A APP INVENTOR

## ¿Qué es App Inventor?

App Inventor es una plataforma de desarrollo creada inicialmente por Google y actualmente mantenida por el MIT (Instituto Tecnológico de Massachusetts) que permite a cualquier persona, incluso sin experiencia previa en programación, crear aplicaciones para dispositivos Android utilizando un sistema de programación visual basado en bloques.

La filosofía detrás de App Inventor es democratizar el desarrollo de aplicaciones, convirtiendo el proceso de creación en una actividad accesible y educativa que fomenta el pensamiento computacional y la resolución de problemas.

## Historia y evolución

- **2009**: Google lanza App Inventor como parte de Google Labs.
- **2011**: Google anuncia el cierre de Google Labs y transfiere App Inventor al MIT.
- **2012**: El MIT relanza la plataforma como "MIT App Inventor".
- **Actualidad**: Continúa evolucionando con actualizaciones regulares y una comunidad global de usuarios.

## Ventajas de App Inventor

- **Accesibilidad**: No requiere conocimientos previos de programación, lo que democratiza la creación de aplicaciones.
- **Enfoque visual**: Su interfaz intuitiva permite arrastrar y soltar bloques para crear aplicaciones.
- **Aprendizaje rápido**: La curva de aprendizaje es menos pronunciada que en la programación tradicional.
- **Gratuito y de código abierto**: Accesible para todos sin costo alguno.
- **Multiplataforma**: Funciona en navegadores web modernos sin necesidad de software especializado.
- **Desarrollo basado en la nube**: Los proyectos se guardan automáticamente en línea.
- **Comunidad activa**: Abundante documentación, tutoriales y ejemplos disponibles.
- **Enfoque educativo**: Ideal para enseñar conceptos de programación de manera práctica.
- **Posibilidad de publicación**: Las aplicaciones creadas pueden publicarse en Google Play Store.

## Entorno de desarrollo

App Inventor consta de dos partes fundamentales que trabajan de manera integrada para facilitar el desarrollo de aplicaciones:

### 3. Depuración

- **Usar etiquetas para mostrar valores**: Mostrar valores de variables en etiquetas para seguir su evolución.
- **Dividir problemas complejos**: Resolver y probar partes pequeñas antes de integrarlas.
- **Probar condiciones límite**: Verificar cómo se comporta la app con valores extremos o inesperados.
- **Buscar errores comunes**: Comprobar fuentes típicas de error como divisiones por cero o índices fuera de rango.
- **Usar el depurador**: App Inventor permite ver los valores de las variables durante la ejecución.

## Ejemplos completos de aplicaciones

### Ejemplo 1: Lista de tareas (To-Do List)

Esta aplicación permite añadir, eliminar y marcar como completadas tareas en una lista.

#### Componentes necesarios:
- TextBox (para introducir nuevas tareas)
- Button (para añadir tareas)
- ListView (para mostrar las tareas)
- CheckBox (para marcar tareas como completadas)
- TinyDB (para guardar las tareas de forma persistente)

#### Bloques principales:

1. **Inicialización de la pantalla**:
```
when Screen1.Initialize
    initialize global lista_tareas to call TinyDB1.GetValue with tag "tareas" valueIfTagNotThere make a list
    call actualizarListView
```

2. **Procedimiento para actualizar la lista visual**:
```
to procedure actualizarListView
    set ListView1.Elements to global lista_tareas
```

3. **Añadir una nueva tarea**:
```
when ButtonAñadir.Click
    if TextBoxTarea.Text ≠ "" then
        add items to list global lista_tareas item TextBoxTarea.Text
        call TinyDB1.StoreValue with tag "tareas" value global lista_tareas
        call actualizarListView
        set TextBoxTarea.Text to ""
    else
        call Notifier1.ShowAlert with message "Por favor, introduce una tarea"
```

4. **Eliminar una tarea**:
```
when ListView1.LongClick position
    initialize local tarea_seleccionada to select list item position from global lista_tareas
    call Notifier1.ShowChooseDialog with message join("¿Qué deseas hacer con la tarea: ", tarea_seleccionada, "?") title "Opciones" button1Text "Eliminar" button2Text "Cancelar"

when Notifier1.AfterChoosing choice
    if choice = "Eliminar" then
        initialize local indice to ListView1.Selection
        remove list item index indice from global lista_tareas
        call TinyDB1.StoreValue with tag "tareas" value global lista_tareas
        call actualizarListView
```

5. **Marcar tarea como completada**:
```
when ListView1.AfterPicking
    initialize local tarea_seleccionada to ListView1.Selection
    
    if starts with tarea_seleccionada "✓ " then
        replace all "✓ " at 1 in text tarea_seleccionada with ""
    else
        set tarea_seleccionada to join("✓ ", tarea_seleccionada)
    
    replace list item ListView1.SelectionIndex at global lista_tareas with tarea_seleccionada
    call TinyDB1.StoreValue with tag "tareas" value global lista_tareas
    call actualizarListView
```

### Ejemplo 2: Aplicación de quiz con múltiples pantallas

Esta aplicación presenta un quiz con preguntas de opción múltiple que se muestran en pantallas separadas.

#### Pantalla 1 (Inicio):
- **Componentes**: Label (título), Button (iniciar quiz), Button (ver puntuaciones)

#### Bloques para la Pantalla 1:
```
when ButtonIniciar.Click
    initialize global puntuacion to 0
    initialize global pregunta_actual to 1
    open another screen screenName "PantallaPregunta"

when ButtonPuntuaciones.Click
    open another screen screenName "PantallaPuntuaciones"
```

#### Pantalla 2 (PantallaPregunta):
- **Componentes**: Label (pregunta), 4 Buttons (opciones), TinyDB (para almacenar preguntas)

#### Bloques para cargar preguntas:
```
initialize global preguntas to make a list
initialize global respuestas_correctas to make a list

when PantallaPregunta.Initialize
    if length of global preguntas = 0 then
        call cargarPreguntas
    
    call mostrarPreguntaActual

to procedure cargarPreguntas
    add items to list global preguntas item "¿Cuál es la capital de Francia?"
    add items to list global preguntas item "¿En qué año se fundó Google?"
    add items to list global preguntas item "¿Cuál es el planeta más grande del sistema solar?"
    
    add items to list global respuestas_correctas item "París"
    add items to list global respuestas_correctas item "1998"
    add items to list global respuestas_correctas item "Júpiter"
    
    initialize global opciones_pregunta1 to make a list with items "Madrid" "París" "Roma" "Berlín"
    initialize global opciones_pregunta2 to make a list with items "1995" "1998" "2000" "2004"
    initialize global opciones_pregunta3 to make a list with items "Tierra" "Marte" "Júpiter" "Saturno"
```

#### Bloques para mostrar pregunta actual:
```
to procedure mostrarPreguntaActual
    set LabelPregunta.Text to select list item global pregunta_actual from global preguntas
    
    if global pregunta_actual = 1 then
        set global opciones_actuales to global opciones_pregunta1
    else if global pregunta_actual = 2 then
        set global opciones_actuales to global opciones_pregunta2
    else
        set global opciones_actuales to global opciones_pregunta3
    
    set Boton1.Text to select list item 1 from global opciones_actuales
    set Boton2.Text to select list item 2 from global opciones_actuales
    set Boton3.Text to select list item 3 from global opciones_actuales
    set Boton4.Text to select list item 4 from global opciones_actuales
```

#### Bloques para verificar respuesta:
```
when Boton1.Click
    call verificarRespuesta with opcion_seleccionada Boton1.Text

when Boton2.Click
    call verificarRespuesta with opcion_seleccionada Boton2.Text

when Boton3.Click
    call verificarRespuesta with opcion_seleccionada Boton3.Text

when Boton4.Click
    call verificarRespuesta with opcion_seleccionada Boton4.Text

to procedure verificarRespuesta opcion_seleccionada
    initialize local respuesta_correcta to select list item global pregunta_actual from global respuestas_correctas
    
    if opcion_seleccionada = respuesta_correcta then
        set global puntuacion to global puntuacion + 1
    
    set global pregunta_actual to global pregunta_actual + 1
    
    if global pregunta_actual > length of global preguntas then
        open another screen with start value screenName "PantallaResultado" value global puntuacion
    else
        call mostrarPreguntaActual
```

#### Pantalla 3 (PantallaResultado):
- **Componentes**: Label (puntuación), Button (reiniciar), Button (volver a inicio), TinyDB (para guardar puntuaciones)

#### Bloques para la Pantalla de Resultados:
```
when PantallaResultado.Initialize with start value value
    set LabelResultado.Text to join("Has acertado ", value, " de ", length of global preguntas, " preguntas!")
    
    initialize local puntuaciones to call TinyDB1.GetValue with tag "puntuaciones" valueIfTagNotThere make a list
    add items to list puntuaciones item value
    call TinyDB1.StoreValue with tag "puntuaciones" value puntuaciones

when BotonReiniciar.Click
    initialize global puntuacion to 0
    initialize global pregunta_actual to 1
    open another screen screenName "PantallaPregunta"

when BotonInicio.Click
    open another screen screenName "Screen1"
```

#### Pantalla 4 (PantallaPuntuaciones):
- **Componentes**: ListView (puntuaciones), Button (volver), TinyDB (para leer puntuaciones)

#### Bloques para la Pantalla de Puntuaciones:
```
when PantallaPuntuaciones.Initialize
    initialize local puntuaciones to call TinyDB1.GetValue with tag "puntuaciones" valueIfTagNotThere make a list
    initialize local lista_formateada to make a list
    
    foreach score in puntuaciones
        add items to list lista_formateada item join("Puntuación: ", score, " de ", length of global preguntas)
    
    set ListView1.Elements to lista_formateada

when BotonVolver.Click
    open another screen screenName "Screen1"
```

## Interacción con sensores y características del dispositivo

App Inventor permite acceder a varios sensores y características del dispositivo para crear aplicaciones más interactivas y funcionales.

### 1. Sensor de ubicación (LocationSensor)

Permite acceder al GPS del dispositivo para obtener la ubicación actual.

#### Ejemplo de uso del sensor de ubicación:
```
when LocationSensor1.LocationChanged latitude longitude altitude
    set LabelLatitud.Text to latitude
    set LabelLongitud.Text to longitude
    set LabelAltitud.Text to altitude
```

#### Ejemplo de aplicación para calcular distancia recorrida:
```
initialize global distancia_total to 0
initialize global ultima_lat to 0
initialize global ultima_lon to 0
initialize global registrando to false

when BotonIniciar.Click
    set global registrando to true
    set global distancia_total to 0
    call LocationSensor1.StartListening

when BotonDetener.Click
    set global registrando to false
    call LocationSensor1.StopListening

when LocationSensor1.LocationChanged latitude longitude altitude
    if global registrando then
        if global ultima_lat ≠ 0 and global ultima_lon ≠ 0 then
            initialize local distancia_actual to call LocationSensor1.DistanceInMeters with latitude1 global ultima_lat longitude1 global ultima_lon latitude2 latitude longitude2 longitude
            set global distancia_total to global distancia_total + distancia_actual
            set LabelDistancia.Text to join(global distancia_total / 1000, " km")
        
        set global ultima_lat to latitude
        set global ultima_lon to longitude
```

### 2. Sensor de acelerómetro (AccelerometerSensor)

Detecta el movimiento y la orientación del dispositivo.

#### Ejemplo de uso del acelerómetro:
```
when AccelerometerSensor1.AccelerationChanged xAccel yAccel zAccel
    set LabelX.Text to xAccel
    set LabelY.Text to yAccel
    set LabelZ.Text to zAccel
    
    if xAccel > 5 then
        set LabelEstado.Text to "¡Movimiento brusco detectado!"
        set LabelEstado.TextColor to "red"
```

#### Ejemplo de aplicación de nivel de burbuja:
```
when AccelerometerSensor1.AccelerationChanged xAccel yAccel zAccel
    set global rotacion to call atan2d with y yAccel x xAccel
    set ImageBurbuja.Rotation to global rotacion
    
    if yAccel > -0.1 and yAccel < 0.1 and xAccel > -0.1 and xAccel < 0.1 then
        set LabelEstado.Text to "¡NIVEL!"
        set LabelEstado.TextColor to "green"
    else
        set LabelEstado.Text to "No nivelado"
        set LabelEstado.TextColor to "red"
```

### 3. Cámara (Camera)

Permite tomar fotos y acceder a la cámara del dispositivo.

#### Ejemplo de uso de la cámara:
```
when BotonTomarFoto.Click
    call Camera1.TakePicture

when Camera1.AfterPicture image
    set Image1.Picture to image
    
    if CheckBoxGuardar.Checked then
        call guardarFoto with foto image
```

#### Ejemplo para guardar fotos con fecha y hora:
```
to procedure guardarFoto foto
    initialize local nombre_archivo to join("foto_", call Clock1.FormatDateTime with format "yyyyMMdd_HHmmss"), ".jpg")
    call File1.SaveFile with text foto fileName nombre_archivo
    
when File1.FileSaved fileName
    call Notifier1.ShowAlert with message join("Foto guardada como: ", fileName)
```

### 4. Bluetooth

Permite la comunicación con otros dispositivos Bluetooth, como Arduino o sistemas IoT.

#### Ejemplo de configuración Bluetooth:
```
when BotonConectar.Click
    call BluetoothClient1.Connect with address ListPickerDispositivos.Selection

when BluetoothClient1.Connected
    set LabelEstado.Text to "Conectado"
    set LabelEstado.TextColor to "green"
    
when BluetoothClient1.ConnectionFailed
    set LabelEstado.Text to "Conexión fallida"
    set LabelEstado.TextColor to "red"
```

#### Ejemplo de envío y recepción de datos:
```
when BotonEncender.Click
    call BluetoothClient1.SendText with text "1"

when BotonApagar.Click
    call BluetoothClient1.SendText with text "0"

when BluetoothClient1.BytesReceived number available
    set global datos_recibidos to call BluetoothClient1.ReceiveText with numberOfBytes number
    set LabelDatos.Text to global datos_recibidos
    
    if global datos_recibidos contains "TEMPERATURA" then
        initialize local temp to select list item 2 from split at ":" global datos_recibidos
        set LabelTemperatura.Text to join(temp, "°C")
```

## Publicación de aplicaciones

### 1. Preparación para la publicación

Antes de publicar tu aplicación, asegúrate de:

- **Probar exhaustivamente**: En diferentes dispositivos y condiciones.
- **Optimizar recursos**: Reducir el tamaño de imágenes y archivos multimedia.
- **Crear iconos y gráficos**: Diseñar un icono atractivo para la app.
- **Escribir una descripción clara**: Explicar las funciones y beneficios de la app.
- **Verificar permisos**: Asegurarte de que solo solicitas los permisos necesarios.

### 2. Exportación del APK

Para crear el archivo de instalación (APK):

1. En el menú, selecciona "Build" > "App (provide QR code for .apk)"
2. Escanea el código QR con tu dispositivo para instalar la app, o
3. Selecciona "Build" > "App (save .apk to my computer)" para guardar el APK

### 3. Opciones de distribución

- **Google Play Store**: La opción más común, requiere registro como desarrollador ($25 una sola vez).
- **Distribución directa**: Compartir el APK directamente o a través de un sitio web.
- **Tiendas alternativas**: F-Droid, Amazon Appstore, entre otras.

### 4. Requisitos para publicar en Google Play

- Crear una cuenta de desarrollador de Google.
- Proporcionar gráficos promocionales (capturas de pantalla, banner, etc.).
- Completar el cuestionario de clasificación de contenido.
- Proporcionar información de privacidad y cumplimiento.
- Pagar la tarifa única de registro ($25).

## Extensiones de App Inventor

App Inventor puede ampliarse con extensiones creadas por la comunidad que añaden funcionalidades no disponibles de forma nativa.

### 1. Ejemplos de extensiones populares

- **TextToSpeech**: Convierte texto en voz.
- **WebViewer**: Visualizador web mejorado.
- **FusionTables**: Para trabajar con Google Fusion Tables.
- **AndroidViewFlipper**: Para crear efectos de transición entre vistas.
- **Notification**: Crea notificaciones en la barra de estado.
- **PhoneCall**: Realiza llamadas telefónicas.
- **SMS**: Envía y recibe mensajes SMS.

### 2. Cómo usar extensiones

1. Descargar el archivo de extensión (.aix).
2. En App Inventor, ir a "Projects" > "Import extension".
3. Seleccionar el archivo descargado.
4. La extensión aparecerá en la Paleta, en la sección "Extensions".

### 3. Ejemplo de uso de la extensión TextToSpeech

```
when ButtonHablar.Click
    call TextToSpeech1.Speak with message TextBoxTexto.Text
    
when ButtonDetener.Click
    call TextToSpeech1.Stop
```

## Recursos avanzados para educadores

### 1. Materiales didácticos

- **Planes de lección**: Estructurados por niveles de dificultad.
- **Ejercicios prácticos**: Con soluciones paso a paso.
- **Proyectos guiados**: Con objetivos claros y evaluación.
- **Rúbricas de evaluación**: Para calificar aplicaciones creadas por estudiantes.

### 2. Estrategias pedagógicas

- **Aprendizaje basado en proyectos**: Los estudiantes crean aplicaciones que resuelven problemas reales.
- **Aprendizaje colaborativo**: Trabajo en equipos para desarrollar aplicaciones más complejas.
- **Gamificación**: Convertir el aprendizaje en un juego con desafíos y recompensas.
- **Desarrollo iterativo**: Enseñar a los estudiantes a mejorar gradualmente sus aplicaciones.

### 3. Progresión de aprendizaje recomendada

1. **Nivel Básico**:
   - Interfaz de usuario simple.
   - Eventos básicos (clicks, temporizadores).
   - Variables y operaciones sencillas.
   - Proyectos: calculadora, conversor, quiz simple.

2. **Nivel Intermedio**:
   - Múltiples pantallas.
   - Listas y persistencia de datos.
   - Procedimientos y funciones.
   - Proyectos: lista de tareas, juego de memoria, recetas.

3. **Nivel Avanzado**:
   - Sensores y hardware del dispositivo.
   - Comunicación con servicios web.
   - Bases de datos y almacenamiento en la nube.
   - Proyectos: rastreador de ejercicio, app de mapas, red social simple.

## Solución de problemas comunes

### 1. Problemas de conexión con el dispositivo

- **Verificar que el dispositivo y el ordenador estén en la misma red Wi-Fi**.
- **Comprobar que el companion de App Inventor esté instalado y actualizado**.
- **Reiniciar tanto el dispositivo como el navegador**.
- **Verificar que no haya restricciones de firewall bloqueando la conexión**.

### 2. Errores en la aplicación

- **"App Inventor is not responding"**: Reiniciar el navegador o borrar la caché.
- **"Communication error"**: Verificar la conexión a internet y recargar la página.
- **La app se cierra inesperadamente**: Comprobar posibles divisiones por cero o índices de lista fuera de rango.
- **Bloques desconectados**: Buscar bloques que deberían estar conectados pero se han separado.

### 3. Optimización de rendimiento

- **Reducir el uso de temporizadores**: Especialmente los que tienen intervalos muy cortos.
- **Optimizar imágenes**: Reducir el tamaño y resolución de las imágenes utilizadas.
- **Limitar la cantidad de pantallas**: Demasiadas pantallas pueden ralentizar la aplicación.
- **Limpiar variables y listas no utilizadas**: Para reducir el consumo de memoria.
- **Evitar bucles infinitos**: Asegurarse de que todas las estructuras repetitivas tengan condiciones de salida claras.

## Conclusión y siguientes pasos

App Inventor es una plataforma poderosa que permite a estudiantes y educadores adentrarse en el mundo del desarrollo de aplicaciones sin las barreras tradicionales de la programación. A través de su interfaz visual y su enfoque basado en bloques, facilita la comprensión de conceptos fundamentales de la programación y el pensamiento computacional.

### Siguientes pasos recomendados:

1. **Crear un proyecto personal**: Aplica lo aprendido en un proyecto que resuelva un problema o necesidad real.
2. **Explorar la comunidad**: Únete a foros y grupos de App Inventor para compartir y aprender.
3. **Participar en desafíos**: Muchas organizaciones realizan competencias de desarrollo con App Inventor.
4. **Avanzar a otras plataformas**: Cuando te sientas cómodo, puedes explorar otros lenguajes como Java (para Android nativo) o Swift (para iOS).
5. **Enseñar a otros**: Comparte tu conocimiento y ayuda a otros a descubrir el mundo de la programación.

---

## Apéndice: Glosario de términos de App Inventor

- **APK**: Android Package Kit, el formato de archivo para distribuir e instalar aplicaciones Android.
- **Bloques**: Elementos visuales que representan instrucciones en App Inventor.
- **Companion**: Aplicación para dispositivos Android que permite probar apps en desarrollo.
- **Componente**: Elemento funcional que se añade a una aplicación (botón, etiqueta, sensor, etc.).
- **Diseñador**: Parte de App Inventor donde se crea la interfaz de usuario.
- **Editor de Bloques**: Parte de App Inventor donde se programa la lógica de la aplicación.
- **Evento**: Acción que desencadena la ejecución de bloques (clic, temporizador, sensor, etc.).
- **Extensión**: Complemento que añade funcionalidades adicionales a App Inventor.
- **Paleta**: Conjunto de componentes disponibles organizados por categorías.
- **Procedimiento**: Conjunto de bloques que realizan una tarea específica y pueden reutilizarse.
- **Propiedad**: Característica configurable de un componente (color, tamaño, texto, etc.).
- **TinyDB**: Componente para almacenar datos de forma persistente en el dispositivo.
- **Visor**: Área que muestra cómo se verá la aplicación en el dispositivo.

---

¡Esperamos que esta guía completa te ayude a iniciar tu viaje en el desarrollo de aplicaciones con App Inventor! 1. Diseñador (Designer)

Es el espacio donde se crea la interfaz gráfica de la aplicación, permitiendo definir cómo se verá la app y qué componentes incluirá:

#### 1.1 Secciones principales del Diseñador:

- **Palette (Paleta)**: Contiene todos los componentes disponibles organizados por categorías.
- **Viewer (Visor)**: Muestra cómo se verá la pantalla de la aplicación.
- **Components (Componentes)**: Lista jerárquica de los componentes que has añadido a tu proyecto.
- **Properties (Propiedades)**: Permite modificar las características de cada componente seleccionado.
- **Media (Medios)**: Gestiona los archivos multimedia del proyecto (imágenes, sonidos, etc.).

#### 1.2 Categorías de componentes en la Paleta:

- **User Interface (Interfaz de Usuario)**:
  - Button (Botón): Para acciones que requieren clic del usuario.
  - Label (Etiqueta): Muestra texto no editable por el usuario.
  - TextBox (Caja de Texto): Permite al usuario introducir texto.
  - CheckBox (Casilla de Verificación): Para selecciones binarias (sí/no).
  - Image (Imagen): Muestra imágenes estáticas.
  - ListPicker (Selector de Lista): Despliega una lista de opciones.
  - Slider (Deslizador): Para seleccionar valores en un rango.
  - Notifier (Notificador): Muestra alertas y mensajes.
  - PasswordTextBox (Caja de Contraseña): Para entrada de texto oculto.
  - WebViewer (Visualizador Web): Muestra contenido de páginas web.
  - Switch (Interruptor): Alternativa visual al CheckBox.
  - DatePicker (Selector de Fecha): Para seleccionar fechas.
  - TimePicker (Selector de Hora): Para seleccionar horas.

- **Layout (Disposición)**:
  - HorizontalArrangement (Disposición Horizontal): Organiza componentes en fila.
  - VerticalArrangement (Disposición Vertical): Organiza componentes en columna.
  - TableArrangement (Disposición en Tabla): Organiza en filas y columnas.
  - ScrollArrangement (Disposición con Desplazamiento): Permite desplazarse cuando el contenido excede el tamaño de la pantalla.

- **Media (Multimedia)**:
  - Sound (Sonido): Reproduce archivos de audio.
  - Player (Reproductor): Reproduce archivos de video.
  - Camera (Cámara): Accede a la cámara del dispositivo.
  - ImagePicker (Selector de Imágenes): Permite elegir imágenes de la galería.
  - VideoPlayer (Reproductor de Video): Reproduce videos en la aplicación.
  - SoundRecorder (Grabadora de Sonido): Graba audio usando el micrófono.

- **Drawing and Animation (Dibujo y Animación)**:
  - Canvas (Lienzo): Área para dibujar y colocar elementos animados.
  - Ball (Pelota): Objeto circular que puede moverse y rebotar.
  - ImageSprite (Sprite de Imagen): Imagen que puede moverse en un Canvas.

- **Sensors (Sensores)**:
  - AccelerometerSensor (Sensor de Acelerómetro): Detecta movimiento del dispositivo.
  - LocationSensor (Sensor de Ubicación): Obtiene la ubicación geográfica.
  - OrientationSensor (Sensor de Orientación): Detecta la orientación del dispositivo.
  - ProximitySensor (Sensor de Proximidad): Detecta objetos cercanos.
  - LightSensor (Sensor de Luz): Mide el nivel de iluminación.
  - BarcodeSensor (Sensor de Código de Barras): Lee códigos QR y de barras.

- **Social (Social)**:
  - ContactPicker (Selector de Contactos): Accede a los contactos del dispositivo.
  - EmailPicker (Selector de Email): Facilita la selección de direcciones de correo.
  - PhoneCall (Llamada Telefónica): Realiza llamadas telefónicas.
  - Texting (Mensajería): Envía y recibe mensajes SMS.
  - PhoneNumberPicker (Selector de Número de Teléfono): Selecciona números de teléfono.

- **Storage (Almacenamiento)**:
  - TinyDB (Base de Datos Pequeña): Almacena datos persistentes en el dispositivo.
  - File (Archivo): Accede al sistema de archivos del dispositivo.
  - CloudDB (Base de Datos en la Nube): Almacena datos en la nube.
  - Firebase (Firebase): Conecta con la base de datos Firebase de Google.

- **Connectivity (Conectividad)**:
  - Web (Web): Realiza solicitudes HTTP a servidores web.
  - ActivityStarter (Iniciador de Actividad): Inicia otras aplicaciones Android.
  - BluetoothClient (Cliente Bluetooth): Conecta con dispositivos Bluetooth.
  - BluetoothServer (Servidor Bluetooth): Actúa como servidor Bluetooth.
  - NFC (NFC): Interactúa con etiquetas NFC.

- **LEGO® MINDSTORMS®**: Componentes para interactuar con robots LEGO.

- **Experimental (Experimental)**: Componentes en fase de prueba y desarrollo.

### 2. Editor de Bloques (Blocks Editor)

Es donde se programa el comportamiento de la aplicación, definiendo la lógica y las acciones que realizará la app:

#### 2.1 Características principales:

- **Interfaz de arrastrar y soltar**: Los bloques se conectan como piezas de rompecabezas.
- **Bloques codificados por colores**: Cada tipo de bloque tiene un color distintivo para su fácil identificación.
- **Área de trabajo expandible**: Espacio ilimitado para organizar los bloques.
- **Papelera**: Para eliminar bloques no deseados.
- **Menú de bloques disponibles**: Organizados por categorías y componentes específicos.
- **Backpack (Mochila)**: Permite copiar bloques entre proyectos.

## Fundamentos de programación con bloques

### 1. Tipos de bloques principales

#### 1.1 Bloques de evento (color amarillo)
Son los que inician una acción cuando algo sucede:

- **when Button.Click**: Se ejecuta cuando el usuario hace clic en un botón.
- **when Screen.Initialize**: Se ejecuta cuando la pantalla se carga por primera vez.
- **when Clock.Timer**: Se ejecuta periódicamente según el intervalo configurado.
- **when Slider.PositionChanged**: Se ejecuta cuando el usuario mueve un deslizador.
- **when LocationSensor.LocationChanged**: Se ejecuta cuando cambia la ubicación del dispositivo.
- **when TextBox.GotFocus/LostFocus**: Se ejecuta cuando un campo de texto recibe o pierde el foco.

Ejemplo de bloque de evento:
```
when Button1.Click
    do <acciones>
```

#### 1.2 Bloques de control (color marrón/café)
Permiten controlar el flujo de ejecución del programa:

##### 1.2.1 Estructuras condicionales:
- **if ... then**: Ejecuta código solo si se cumple una condición.
- **if ... then ... else**: Ejecuta un código si se cumple la condición y otro diferente si no se cumple.
- **if ... then ... else if ... then ... else**: Para múltiples condiciones secuenciales.

Ejemplo de condicional simple:
```
if TextBox1.Text = "" then
    set Label1.Text to "Por favor, introduce un valor"
```

Ejemplo de condicional con else:
```
if TextBox1.Number > 10 then
    set Label1.Text to "El número es mayor que 10"
else
    set Label1.Text to "El número es menor o igual a 10"
```

Ejemplo de condicional múltiple:
```
if TextBox1.Number < 0 then
    set Label1.Text to "El número es negativo"
else if TextBox1.Number = 0 then
    set Label1.Text to "El número es cero"
else
    set Label1.Text to "El número es positivo"
```

##### 1.2.2 Bucles (estructuras repetitivas):
- **foreach ... in list**: Repite acciones para cada elemento de una lista.
- **for range**: Repite acciones un número específico de veces.
- **while**: Repite acciones mientras se cumpla una condición.

Ejemplo de bucle foreach:
```
foreach item in list
    do <acciones con item>
```

Ejemplo de bucle for:
```
for number from 1 to 10 by 1
    set Label1.Text to Label1.Text & number & " "
```

Ejemplo de bucle while:
```
initialize local contador to 1
while contador <= 10
    set Label1.Text to Label1.Text & contador & " "
    set contador to contador + 1
```

#### 1.3 Bloques lógicos (color verde)
Evalúan condiciones y devuelven verdadero o falso:

- **equals (=)**: Comprueba si dos valores son iguales.
- **not equals (≠)**: Comprueba si dos valores son diferentes.
- **greater than (>)**: Comprueba si un valor es mayor que otro.
- **less than (<)**: Comprueba si un valor es menor que otro.
- **greater than or equal (≥)**: Comprueba si un valor es mayor o igual que otro.
- **less than or equal (≤)**: Comprueba si un valor es menor o igual que otro.
- **and**: Devuelve verdadero si ambas condiciones son verdaderas.
- **or**: Devuelve verdadero si al menos una condición es verdadera.
- **not**: Invierte un valor booleano (verdadero → falso, falso → verdadero).

Ejemplo de operación lógica compuesta:
```
if (TextBox1.Number > 0 and TextBox1.Number < 100) then
    set Label1.Text to "El número está entre 1 y 99"
```

#### 1.4 Bloques matemáticos (color azul)
Realizan operaciones matemáticas:

- **Operaciones básicas**: suma (+), resta (-), multiplicación (×), división (÷).
- **Funciones matemáticas**: random, raíz cuadrada, potencia, seno, coseno, etc.
- **Constantes**: pi, e (base del logaritmo natural).
- **Comparaciones numéricas**: mayor, menor, igual, etc.

Ejemplo de operación matemática:
```
set Label1.Text to TextBox1.Number + TextBox2.Number
```

#### 1.5 Bloques de texto (color rojo/púrpura)
Manipulan cadenas de texto:

- **text (cadena literal)**: Crea una cadena de texto.
- **join**: Concatena (une) textos.
- **length**: Obtiene la longitud de un texto.
- **is empty**: Comprueba si un texto está vacío.
- **contains**: Verifica si un texto contiene otro.
- **split at**: Divide un texto en partes según un separador.
- **segment**: Extrae una parte de un texto.
- **replace all**: Reemplaza ocurrencias de un texto por otro.
- **trim**: Elimina espacios al principio y final.
- **upcase/downcase**: Convierte a mayúsculas/minúsculas.

Ejemplo de manipulación de texto:
```
set Label1.Text to join("Hola ", TextBox1.Text, "!")
```

#### 1.6 Bloques de listas (color naranja)
Trabajan con listas (arrays) de elementos:

- **make a list**: Crea una nueva lista con los elementos especificados.
- **add items to list**: Añade elementos al final de una lista.
- **insert item into list**: Inserta un elemento en una posición específica.
- **select item from list**: Obtiene un elemento según su posición.
- **remove item from list**: Elimina un elemento de la lista.
- **length of list**: Obtiene el número de elementos de la lista.
- **is list empty**: Comprueba si la lista no tiene elementos.
- **is in list**: Verifica si un elemento está en la lista.
- **position in list**: Encuentra la posición de un elemento en la lista.

Ejemplo de uso de listas:
```
initialize global lista_nombres to make a list
add items to list lista_nombres item TextBox1.Text
set ListView1.Elements to lista_nombres
```

#### 1.7 Bloques de variables (color naranja/melocotón)
Permiten almacenar y manipular datos:

- **initialize global/local name**: Crea y asigna una variable global (accesible desde cualquier parte) o local (solo dentro del bloque donde se define).
- **get**: Obtiene el valor de una variable.
- **set to**: Asigna un nuevo valor a una variable existente.

Ejemplo de uso de variables:
```
initialize global contador to 0
set contador to contador + 1
set Label1.Text to contador
```

#### 1.8 Bloques de procedimientos (color morado)
Crean funciones reutilizables:

- **to procedure**: Define un procedimiento que no devuelve valor.
- **to procedure result**: Define una función que devuelve un valor.
- **call procedure**: Invoca un procedimiento o función.

Ejemplo de definición y uso de procedimiento:
```
to procedure saludarUsuario
    set Label1.Text to join("Hola ", TextBox1.Text, "!")

when Button1.Click
    call saludarUsuario
```

Ejemplo de función que devuelve un valor:
```
to sumarNumeros number1 number2 returns
    return number1 + number2

when Button1.Click
    set Label1.Text to call sumarNumeros with TextBox1.Number TextBox2.Number
```

#### 1.9 Bloques de componentes (varios colores según el tipo)
Son específicos para cada componente y permiten acceder a sus propiedades y métodos.

## Manejo de múltiples pantallas

App Inventor permite crear aplicaciones con varias pantallas, lo que facilita la organización de interfaces complejas y mejora la experiencia del usuario.

### 1. Creación de nuevas pantallas

Para añadir una nueva pantalla a tu proyecto:

1. En el menú principal, selecciona "Add Screen..."
2. Nombra la nueva pantalla (ejemplo: "Screen2" o "PantallaDetalles")
3. Selecciona si deseas una pantalla en blanco o utilizar una plantilla
4. Haz clic en "OK" para crear la pantalla

### 2. Navegación entre pantallas

Hay varias formas de navegar entre pantallas:

#### 2.1 Usando open another screen:
```
when Button1.Click
    open another screen screenName "Screen2"
```

#### 2.2 Pasando valores a otra pantalla:
```
when Button1.Click
    open another screen with start value screenName "Screen2" value TextBox1.Text
```

#### 2.3 Para recibir el valor en la pantalla destino:
```
when Screen2.Initialize with start value value
    set Label1.Text to value
```

#### 2.4 Para volver a la pantalla anterior:
```
when BotonVolver.Click
    close screen
```

#### 2.5 Para volver a la pantalla anterior devolviendo un valor:
```
when BotonGuardar.Click
    close screen with value TextBox1.Text
```

#### 2.6 Para recibir el valor devuelto:
```
when Screen1.OtherScreenClosed screenName result
    if screenName = "Screen2" then
        set Label1.Text to result
```

### 3. Organización de proyectos con múltiples pantallas

Recomendaciones para proyectos con varias pantallas:

- **Nombres descriptivos**: Usa nombres que indiquen claramente la función de cada pantalla.
- **Consistencia visual**: Mantén un estilo coherente entre pantallas (colores, fuentes, disposición).
- **Navegación intuitiva**: Incluye botones claros para navegar entre pantallas.
- **Independencia lógica**: Cada pantalla debe tener una función específica y bien definida.
- **Comunicación eficiente**: Planifica qué datos necesitas pasar entre pantallas.

## Almacenamiento de datos

App Inventor ofrece varias opciones para almacenar datos:

### 1. TinyDB

Almacena datos de forma persistente en el dispositivo usando un sistema de clave-valor.

Ejemplo de guardado en TinyDB:
```
when BotonGuardar.Click
    call TinyDB1.StoreValue with tag "nombre_usuario" value TextBox1.Text
```

Ejemplo de recuperación desde TinyDB:
```
when Screen1.Initialize
    set TextBox1.Text to call TinyDB1.GetValue with tag "nombre_usuario" valueIfTagNotThere ""
```

### 2. Firebase DB

Permite almacenar datos en la nube y sincronizarlos entre dispositivos.

Ejemplo de configuración:
```
when Screen1.Initialize
    call FirebaseDB1.FirebaseURL to "https://tu-proyecto.firebaseio.com/"
    call FirebaseDB1.ProjectBucket to "bucket"
```

Ejemplo de guardado en Firebase:
```
when BotonGuardar.Click
    call FirebaseDB1.StoreValue with tag "usuarios/" & TextBoxUsuario.Text value TextBoxDatos.Text
```

### 3. Archivos

Permite leer y escribir archivos en el almacenamiento del dispositivo.

Ejemplo de escritura en archivo:
```
when BotonGuardar.Click
    call File1.SaveFile with text TextBox1.Text fileName "datos.txt"
```

Ejemplo de lectura de archivo:
```
when BotonCargar.Click
    call File1.ReadFrom with fileName "datos.txt"
    
when File1.GotText text
    set TextBox1.Text to text
```

## Ejemplos prácticos con estructuras de control

### Ejemplo 1: Validación de formulario con IF

```
when BotonEnviar.Click
    if TextBoxNombre.Text = "" then
        call Notifier1.ShowAlert with message "Por favor, introduce tu nombre"
    else if TextBoxEdad.Number <= 0 then
        call Notifier1.ShowAlert with message "La edad debe ser un número positivo"
    else if not CheckBoxTerminos.Checked then
        call Notifier1.ShowAlert with message "Debes aceptar los términos y condiciones"
    else
        call EnviarFormulario
        set LabelEstado.Text to "¡Formulario enviado correctamente!"
        set LabelEstado.TextColor to "green"
```

### Ejemplo 2: Calculadora con estructura SWITCH (simulada con IF-ELSE)

```
when BotonCalcular.Click
    if ListPickerOperacion.Selection = "Suma" then
        set LabelResultado.Text to TextBoxNum1.Number + TextBoxNum2.Number
    else if ListPickerOperacion.Selection = "Resta" then
        set LabelResultado.Text to TextBoxNum1.Number - TextBoxNum2.Number
    else if ListPickerOperacion.Selection = "Multiplicación" then
        set LabelResultado.Text to TextBoxNum1.Number * TextBoxNum2.Number
    else if ListPickerOperacion.Selection = "División" then
        if TextBoxNum2.Number = 0 then
            set LabelResultado.Text to "Error: División por cero"
        else
            set LabelResultado.Text to TextBoxNum1.Number / TextBoxNum2.Number
```

### Ejemplo 3: Contador con bucle WHILE

```
to procedure contarHasta limite
    initialize local contador to 1
    initialize local resultado to ""
    
    while contador <= limite
        set resultado to join(resultado, contador, " ")
        set contador to contador + 1
        
    return resultado

when BotonContar.Click
    set LabelSecuencia.Text to call contarHasta with TextBoxLimite.Number
```

### Ejemplo 4: Procesamiento de lista con bucle FOREACH

```
when BotonProcesar.Click
    initialize local listaNumeros to call convertirTextoALista with TextBoxNumeros.Text
    initialize local suma to 0
    initialize local cantidad to length of list listaNumeros
    
    foreach numero in listaNumeros
        set suma to suma + numero
    
    if cantidad = 0 then
        set LabelPromedio.Text to "No hay números para promediar"
    else
        set LabelPromedio.Text to suma / cantidad

to convertirTextoALista texto returns
    initialize local lista to make a list
    initialize local numeros to split at spaces texto
    
    foreach texto_numero in numeros
        add items to list lista item call text_to_number with texto_numero
        
    return lista
    
to text_to_number texto returns
    initialize local result to 0
    
    if is number texto then
        set result to number texto
        
    return result
```

### Ejemplo 5: Juego de adivinar un número con FOR

```
initialize global numero_secreto to 0

when Screen1.Initialize
    call generarNumeroSecreto

to procedure generarNumeroSecreto
    set global numero_secreto to random integer from 1 to 100
    set LabelIntentos.Text to "Tienes 7 intentos"
    set global intentos_restantes to 7

when BotonAdivinar.Click
    if global intentos_restantes > 0 then
        set global intentos_restantes to global intentos_restantes - 1
        set LabelIntentos.Text to join("Te quedan ", global intentos_restantes, " intentos")
        
        if TextBoxNumero.Number = global numero_secreto then
            set LabelResultado.Text to "¡Felicidades! ¡Has adivinado el número!"
            set LabelResultado.TextColor to "green"
        else if TextBoxNumero.Number < global numero_secreto then
            set LabelResultado.Text to "El número es mayor"
            set LabelResultado.TextColor to "blue"
        else
            set LabelResultado.Text to "El número es menor"
            set LabelResultado.TextColor to "blue"
            
        if global intentos_restantes = 0 and TextBoxNumero.Number ≠ global numero_secreto then
            set LabelResultado.Text to join("¡Game Over! El número era ", global numero_secreto)
            set LabelResultado.TextColor to "red"
    
when BotonReiniciar.Click
    call generarNumeroSecreto
    set TextBoxNumero.Text to ""
    set LabelResultado.Text to "Adivina un número entre 1 y 100"
    set LabelResultado.TextColor to "black"
```

## Buenas prácticas de programación en App Inventor

### 1. Organización de bloques

- **Agrupar bloques relacionados**: Mantener juntos los bloques que realizan funciones relacionadas.
- **Usar procedimientos**: Encapsular funcionalidades repetidas en procedimientos reutilizables.
- **Comentar el código**: Usar bloques de comentario para explicar secciones complejas.
- **Nombrar variables descriptivamente**: Usar nombres que indiquen el propósito de cada variable.
- **Indentación visual**: Organizar los bloques con sangría para mostrar la estructura lógica.

### 2. Optimización

- **Evitar la duplicación de código**: Usar procedimientos para código repetitivo.
- **Minimizar variables globales**: Preferir variables locales cuando sea posible.
- **Limitar el uso de timers**: Los temporizadores consumen batería.
- **Liberar recursos**: Cerrar conexiones de base de datos, Bluetooth, etc. cuando no se usen.
- **Controlar el tamaño de las imágenes**: Usar imágenes optimizadas para móviles.
