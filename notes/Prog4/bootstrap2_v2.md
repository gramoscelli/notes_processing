# 🚀 Guía Bootstrap - Parte 2: Clases Utilitarias (Deep Dive)


## Antes de empezar: Cómo usar JSFiddle para correr los e|jemplos de Bootstrap

Para sacarle el máximo provecho a esta guía y entender realmente cómo funcionan las clases utilitarias de Bootstrap, te recomendamos que pruebes todos los ejemplos de código. La forma más sencilla y rápida de hacerlo, sin necesidad de configurar un proyecto local, es utilizando **JSFiddle**.

JSFiddle es un editor de código online que te permite escribir HTML, CSS y JavaScript, y ver el resultado en tiempo real en tu navegador. Es perfecto para experimentar con pequeños fragmentos de código y entender los conceptos de Bootstrap.

Sigue estos sencillos pasos para empezar a jugar con los ejemplos:

### Pasos para Usar JSFiddle con Bootstrap:

1.  **Abre JSFiddle:**
    *   Ve a [https://jsfiddle.net/](https://jsfiddle.net/) en tu navegador.
    *   Verás cuatro paneles principales: **HTML**, **CSS**, **JavaScript** y **Result**.

2.  **Configura Bootstrap:**
    *   En la barra lateral izquierda de JSFiddle, busca la sección "Frameworks & Extensions".
    *   Haz clic en el selector y busca "Bootstrap". Asegúrate de elegir una versión reciente (por ejemplo, **Bootstrap 5.3.x**).
    *   Al seleccionar Bootstrap, JSFiddle automáticamente enlazará los archivos CSS y JS necesarios para que Bootstrap funcione en tu panel de "Result".

    > **Nota:** Si por alguna razón no encuentras Bootstrap en el selector, puedes añadirlo manualmente en la sección "External Resources" (también en la barra lateral izquierda) añadiendo las CDN de Bootstrap. Solo pega estas dos URLs:
    > *   **CSS:** `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css`
    > *   **JS:** `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js`

3.  **Copia el Código HTML:**
    *   De cualquiera de los ejemplos en esta guía, copia el bloque de código HTML (el que empieza y termina con ````html`).
    *   Pégalo en el panel **HTML** de JSFiddle.

4.  **Copia el Código CSS (si aplica):**
    *   Para la mayoría de los ejemplos de utilidades, no necesitarás CSS adicional, ya que la idea es usar solo las clases de Bootstrap.
    *   Si un ejemplo incluye algún estilo `style="..."` directamente en el HTML, puedes dejarlo así, o si lo prefieres, podrías mover esos estilos al panel **CSS** de JSFiddle para mayor claridad (por ejemplo, `div { height: 200px; }`).

5.  **Ejecuta el Código:**
    *   Haz clic en el botón **"Run"** en la parte superior del editor de JSFiddle.
    *   Inmediatamente verás el resultado de tu código HTML estilizado con Bootstrap en el panel **Result**.

6.  **Experimenta y Modifica:**
    *   ¡Ahora viene la parte divertida! Modifica las clases de Bootstrap en tu HTML (o añade nuevas) y haz clic en "Run" de nuevo para ver cómo cambian los estilos.
    *   Por ejemplo, cambia `text-primary` por `text-danger`, o `m-3` por `m-5`. Observa los efectos.
    *   Intenta resolver los ejercicios propuestos directamente en JSFiddle.

**Consejo**
Para los ejemplos que usan la clase `min-vh-100` o `vh-100`, el panel "Result" de JSFiddle es más pequeño que una ventana de navegador completa. Puedes usar la opción "Open in new tab" (normalmente un icono de una flecha saliendo de un cuadrado en la esquina superior derecha del panel Result) para ver el ejemplo en una ventana completa y observar el efecto real de estas clases.

## ¿Qué son y por qué son tan útiles las Clases Utilitarias?

Imagina que quieres cambiar el color de un texto, añadir un margen o centrar un elemento. Tradicionalmente, tendrías que ir a tu archivo CSS y escribir:

```css
.mi-texto-azul {
  color: blue;
}

.mi-div-con-margen {
  margin-top: 16px;
}
```

Y luego aplicar estas clases a tu HTML. Con las **Clases Utilitarias** de Bootstrap, este proceso se simplifica drásticamente. Son clases CSS predefinidas (como `text-primary` o `m-3`) que ya vienen con estilos específicos. Solo necesitas agregarlas directamente a tus elementos HTML.

**¿Cuál es la magia?**

*   **Velocidad de Desarrollo:** Menos tiempo escribiendo CSS, más tiempo construyendo.
*   **Consistencia:** Aseguran que tus diseños mantengan una apariencia uniforme en todo tu proyecto.
*   **Reusabilidad:** Las mismas clases pueden aplicarse a diferentes elementos para lograr el mismo efecto.
*   **Código Limpio y Mantenible:** Reduce la cantidad de CSS personalizado, haciendo tu código más fácil de entender y actualizar.
*   **Diseño Responsivo Integrado:** Muchas utilidades ya incluyen variantes para diferentes tamaños de pantalla.


## 🎨 Colores: Dale vida a tus elementos

Bootstrap ofrece una paleta de colores semánticos y neutros que puedes aplicar tanto al texto como al fondo de tus elementos. Estos colores están pensados para comunicar un significado (éxito, peligro, información) y son personalizables a través de variables CSS si necesitas cambiar la paleta global de tu proyecto.

### Colores de Texto (`text-*`)

Estas clases establecen el `color` de un elemento. Son ideales para mensajes, encabezados o cualquier texto que necesite resaltar.

```html
<!-- Colores semánticos: Asocian un significado al color -->
<p class="text-primary">Este texto es azul, usualmente para acciones principales.</p>
<p class="text-secondary">Este texto es gris, para información menos destacada.</p>
<p class="text-success">¡Éxito! Este texto es verde.</p>
<p class="text-danger">¡Atención! Este texto es rojo, indica un peligro o error.</p>
<p class="text-warning">Cuidado, este texto amarillo es una advertencia.</p>
<p class="text-info">Este texto azul claro es para información adicional.</p>

<!-- Colores neutros y especiales -->
<p class="text-light bg-dark p-2">Texto gris claro (ideal sobre fondos oscuros).</p>
<p class="text-dark">Texto gris oscuro.</p>
<p class="text-body">Texto con el color por omisión del cuerpo (generalmente negro o gris oscuro).</p>
<p class="text-muted">Texto gris silenciado, para notas secundarias o detalles.</p>
<p class="text-white bg-dark p-2">Texto blanco (ideal sobre fondos oscuros).</p>

<!-- Con opacidad: La mitad de la transparencia del color negro o blanco -->
<p class="text-black-50">Texto negro con 50% de opacidad.</p>
<p class="text-white-50 bg-dark p-2">Texto blanco con 50% de opacidad.</p>
```

### Colores de Fondo (`bg-*`)

Estas clases controlan la propiedad `background-color` de un elemento. Recuerda combinarlas con clases de color de texto (`text-white`, `text-dark`) para asegurar un buen contraste y legibilidad. La clase `p-2` se usa aquí para añadir un poco de relleno y hacer los ejemplos más visibles.

```html
<!-- Fondos semánticos: Mismo concepto que los colores de texto -->
<div class="bg-primary text-white p-2 mb-2">Fondo azul primario con texto blanco.</div>
<div class="bg-secondary text-white p-2 mb-2">Fondo gris secundario con texto blanco.</div>
<div class="bg-success text-white p-2 mb-2">Fondo verde de éxito con texto blanco.</div>
<div class="bg-danger text-white p-2 mb-2">Fondo rojo de peligro con texto blanco.</div>
<div class="bg-warning text-dark p-2 mb-2">Fondo amarillo de advertencia con texto oscuro para mejor contraste.</div>
<div class="bg-info text-white p-2 mb-2">Fondo azul claro informativo con texto blanco.</div>
<div class="bg-light text-dark p-2 mb-2">Fondo gris claro con texto oscuro.</div>
<div class="bg-dark text-white p-2 mb-2">Fondo gris oscuro con texto blanco.</div>

<!-- Fondos neutros y especiales -->
<div class="bg-body text-dark p-2 mb-2">Fondo con el color por omisión del cuerpo.</div>
<div class="bg-white text-dark p-2 mb-2">Fondo blanco con texto oscuro.</div>
<div class="bg-transparent p-2 mb-2">Fondo completamente transparente.</div>

<!-- Fondos con gradientes: Añade un sutil gradiente lineal -->
<div class="bg-primary bg-gradient text-white p-2">Fondo azul con un elegante gradiente.</div>
```



## 📏 Espaciado: Organiza tus elementos con Márgenes y Rellenos

El espaciado es fundamental para la legibilidad y la estructura visual de tu diseño. Bootstrap proporciona un sistema de espaciado muy flexible y consistente.

### Sistema de Espaciado (Escala 0-5)

Bootstrap utiliza una escala numérica del 0 al 5 para definir los tamaños de espaciado. Estos valores se basan en la unidad `rem`, lo que significa que se adaptan bien si cambias el tamaño de fuente base de tu proyecto.

*   `0` = `0px` (Sin espaciado)
*   `1` = `0.25rem` (normalmente `4px`)
*   `2` = `0.5rem` (normalmente `8px`)
*   `3` = `1rem` (normalmente `16px`) - ¡Este es el valor por omisión más común!
*   `4` = `1.5rem` (normalmente `24px`)
*   `5` = `3rem` (normalmente `48px`)

### Márgenes (`m-*`)

Los márgenes son el espacio **fuera** del borde de un elemento. Sirven para separar un elemento de otros a su alrededor.

```html
<!-- Margen en todos los lados: `m-{tamaño}` -->
<div class="bg-light p-2 mb-2">
    <div class="m-0 bg-info text-white">Sin margen (m-0)</div>
</div>
<div class="bg-light p-2 mb-2">
    <div class="m-1 bg-info text-white">Margen pequeño (m-1)</div>
</div>
<div class="bg-light p-2 mb-2">
    <div class="m-3 bg-info text-white">Margen medio (m-3)</div>
</div>
<div class="bg-light p-2 mb-2">
    <div class="m-5 bg-info text-white">Margen grande (m-5)</div>
</div>
<div class="bg-light p-2 mb-2 d-flex justify-content-center">
    <div class="m-auto bg-info text-white">Margen automático (m-auto): Centra horizontalmente elementos de bloque con ancho definido.</div>
</div>

<!-- Márgenes específicos por lado/eje: `m{lado}-{tamaño}` o `m{eje}-{tamaño}` -->
<div class="bg-light p-2">
    <div class="mt-3 bg-success text-white">Solo margen superior (mt-3)</div>
</div>
<div class="bg-light p-2">
    <div class="mb-3 bg-danger text-white">Solo margen inferior (mb-3)</div>
</div>
<div class="bg-light p-2 d-flex">
    <div class="ms-3 bg-warning text-dark">Solo margen al inicio (ms-3, izquierda en LTR)</div>
</div>
<div class="bg-light p-2 d-flex justify-content-end">
    <div class="me-3 bg-info text-white">Solo margen al final (me-3, derecha en LTR)</div>
</div>
<div class="bg-light p-2">
    <div class="mx-3 bg-primary text-white">Margen horizontal (mx-3: izquierda y derecha)</div>
</div>
<div class="bg-light p-2">
    <div class="my-3 bg-secondary text-white">Margen vertical (my-3: arriba y abajo)</div>
</div>

<!-- Márgenes negativos: Útiles para superponer elementos o ajustar diseños -->
<div class="bg-light p-4">
    <div class="mb-3 bg-primary text-white p-2">Elemento con margen normal</div>
    <div class="mt-n2 bg-success text-white p-2">Elemento con margen superior negativo (-8px)</div>
</div>
```

### Relleno (Padding) (`p-*`)

El relleno es el espacio **dentro** del borde de un elemento, entre el contenido y el borde. Sirve para darle "aire" al contenido.

```html
<!-- Relleno en todos los lados: `p-{tamaño}` -->
<div class="border border-dark mb-2">
    <div class="p-0 bg-info text-white">Sin relleno (p-0)</div>
</div>
<div class="border border-dark mb-2">
    <div class="p-1 bg-info text-white">Relleno pequeño (p-1)</div>
</div>
<div class="border border-dark mb-2">
    <div class="p-3 bg-info text-white">Relleno medio (p-3)</div>
</div>
<div class="border border-dark mb-2">
    <div class="p-5 bg-info text-white">Relleno grande (p-5)</div>
</div>

<!-- Rellenos específicos por lado/eje: `p{lado}-{tamaño}` o `p{eje}-{tamaño}` -->
<div class="border border-dark mb-2">
    <div class="pt-3 bg-success text-white">Solo relleno superior (pt-3)</div>
</div>
<div class="border border-dark mb-2">
    <div class="pb-3 bg-danger text-white">Solo relleno inferior (pb-3)</div>
</div>
<div class="border border-dark mb-2">
    <div class="ps-3 bg-warning text-dark">Solo relleno al inicio (ps-3, izquierda en LTR)</div>
</div>
<div class="border border-dark mb-2">
    <div class="pe-3 bg-info text-white">Solo relleno al final (pe-3, derecha en LTR)</div>
</div>
<div class="border border-dark mb-2">
    <div class="px-3 bg-primary text-white">Relleno horizontal (px-3: izquierda y derecha)</div>
</div>
<div class="border border-dark mb-2">
    <div class="py-3 bg-secondary text-white">Relleno vertical (py-3: arriba y abajo)</div>
</div>
```

### Espaciado Responsivo: Adaptándose a la pantalla

Aquí es donde las utilidades de espaciado se vuelven realmente poderosas. Puedes especificar diferentes tamaños de margen o relleno para distintos puntos de ruptura (breakpoints).

```html
<!-- Margen responsivo: m-{breakpoint}-{tamaño} -->
<div class="bg-dark text-white p-3 mb-3">
    <p class="m-1 m-sm-2 m-md-3 m-lg-4 m-xl-5 bg-primary p-2">
        Observa cómo mi margen crece: 4px en móvil, 8px en SM, 16px en MD, 24px en LG, 48px en XL.
    </p>
</div>

<!-- Relleno responsivo: p-{breakpoint}-{tamaño} -->
<div class="bg-dark text-white p-3">
    <p class="p-2 p-md-4 p-lg-5 bg-success">
        Observa cómo mi relleno crece: 8px en móvil, 24px en MD, 48px en LG+.
    </p>
</div>
```



## 📱 Display: Controla cómo se muestran los elementos

Las clases de `display` (`d-*`) son fundamentales para controlar el comportamiento de los elementos en el flujo de tu diseño. Desde ocultar un elemento hasta convertirlo en un contenedor Flexbox o Grid.

### Valores de Display Básicos

```html
<!-- Ocultar/Mostrar: d-none es muy útil para alternar visibilidad con JavaScript -->
<div class="d-none bg-danger text-white p-2 mb-2">Este elemento está completamente oculto.</div>

<!-- Tipos de caja: Cómo interactúa el elemento con su entorno -->
<span class="d-inline bg-primary text-white p-1 me-2">Inline</span><span class="d-inline bg-primary text-white p-1">Inline</span>
<p class="text-muted">Los elementos `inline` fluyen uno al lado del otro.</p>

<div class="d-inline-block bg-success text-white p-2 me-2">Inline-Block</div><div class="d-inline-block bg-success text-white p-2">Inline-Block</div>
<p class="text-muted">`inline-block` permite ancho/alto y fluye en línea.</p>

<div class="d-block bg-info text-white p-2 mb-2">Block</div>
<div class="d-block bg-info text-white p-2">Block</div>
<p class="text-muted">`block` ocupa todo el ancho disponible y fuerza un salto de línea.</p>

<!-- Comportamientos avanzados: Para layouts complejos -->
<div class="d-flex bg-warning text-dark p-2 mb-2">Contenedor Flexbox</div>
<div class="d-grid bg-secondary text-white p-2 mb-2">Contenedor Grid (requiere más clases para funcionar)</div>
<div class="d-table bg-dark text-white p-2 mb-2">Comportamiento como tabla</div>
<div class="d-table-row bg-dark text-white p-2 mb-2">Comportamiento como fila de tabla</div>
<div class="d-table-cell bg-dark text-white p-2 mb-2">Comportamiento como celda de tabla</div>
```

### Display Responsivo: El poder de la adaptación

Esta es una de las utilidades más usadas. Permite mostrar u ocultar elementos en función del tamaño de la pantalla, lo que es esencial para un diseño *mobile-first*.

```html
<!-- Ocultar en ciertos breakpoints -->
<div class="d-none d-md-block bg-primary text-white p-2 mb-2">
    Oculto en móvil (<768px), visible en tablet y desktop (MD+).
</div>

<!-- Mostrar en ciertos breakpoints -->
<div class="d-block d-md-none bg-success text-white p-2 mb-2">
    Visible en móvil (<768px), oculto en tablet y desktop (MD+).
</div>

<!-- Visible solo en un rango específico de tamaños de pantalla -->
<div class="d-none d-sm-block d-lg-none bg-warning text-dark p-2 mb-2">
    Solo visible en tablets (entre 576px y 991px).
</div>

<!-- Para impresión: d-print-* -->
<div class="d-print-none bg-danger text-white p-2 mb-2">
    Este texto no se mostrará al imprimir la página.
</div>
<div class="d-none d-print-block bg-info text-white p-2 mb-2">
    Este texto solo se mostrará al imprimir la página.
</div>
```



## 🔄 Flexbox: Diseño flexible y potente

Flexbox es un módulo de CSS que permite diseñar interfaces de usuario complejas y alineadas de manera eficiente. Bootstrap facilita su uso con una serie de clases utilitarias.

### Contenedor Flex (`d-flex`)

Para que Flexbox funcione, primero debes definir un elemento como un contenedor flex.

```html
<div class="d-flex bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">Elemento 1</div>
    <div class="p-2 border bg-success text-white">Elemento 2</div>
    <div class="p-2 border bg-info text-white">Elemento 3</div>
</div>
<p class="text-muted">Los elementos flex se ajustan en una fila por omisión.</p>
```

### Dirección Flex (`flex-row`, `flex-column`, etc.)

Controla la dirección del eje principal (donde se organizan los elementos).

```html
<div class="d-flex flex-row bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">1</div>
    <div class="p-2 border bg-success text-white">2</div>
    <div class="p-2 border bg-info text-white">3</div>
</div>
<p class="text-muted">`flex-row` (por omisión): Horizontal de izquierda a derecha.</p>

<div class="d-flex flex-row-reverse bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">1</div>
    <div class="p-2 border bg-success text-white">2</div>
    <div class="p-2 border bg-info text-white">3</div>
</div>
<p class="text-muted">`flex-row-reverse`: Horizontal de derecha a izquierda.</p>

<div class="d-flex flex-column bg-light p-3 border mb-3" style="height: 120px;">
    <div class="p-2 border bg-primary text-white">1</div>
    <div class="p-2 border bg-success text-white">2</div>
    <div class="p-2 border bg-info text-white">3</div>
</div>
<p class="text-muted">`flex-column`: Vertical de arriba hacia abajo.</p>

<div class="d-flex flex-column-reverse bg-light p-3 border mb-3" style="height: 120px;">
    <div class="p-2 border bg-primary text-white">1</div>
    <div class="p-2 border bg-success text-white">2</div>
    <div class="p-2 border bg-info text-white">3</div>
</div>
<p class="text-muted">`flex-column-reverse`: Vertical de abajo hacia arriba.</p>

<!-- Direcciones responsivas: Cambia la dirección según el tamaño de pantalla -->
<div class="d-flex flex-column flex-md-row bg-secondary text-white p-3 mb-3">
    <div class="p-2 border me-md-2 mb-2 mb-md-0">Vertical en móvil</div>
    <div class="p-2 border me-md-2 mb-2 mb-md-0">Horizontal en MD+</div>
    <div class="p-2 border">¡Adaptable!</div>
</div>
```

### Justificación (Eje Principal) (`justify-content-*`)

Controla la alineación de los elementos flex a lo largo del eje principal.

```html
<div class="d-flex justify-content-start bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">A</div>
    <div class="p-2 border bg-success text-white">B</div>
</div>
<p class="text-muted">`justify-content-start`: Alineados al inicio.</p>

<div class="d-flex justify-content-end bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">A</div>
    <div class="p-2 border bg-success text-white">B</div>
</div>
<p class="text-muted">`justify-content-end`: Alineados al final.</p>

<div class="d-flex justify-content-center bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">A</div>
    <div class="p-2 border bg-success text-white">B</div>
</div>
<p class="text-muted">`justify-content-center`: Centrados.</p>

<div class="d-flex justify-content-between bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">A</div>
    <div class="p-2 border bg-success text-white">B</div>
</div>
<p class="text-muted">`justify-content-between`: Espacio uniforme *entre* los elementos.</p>

<div class="d-flex justify-content-around bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">A</div>
    <div class="p-2 border bg-success text-white">B</div>
</div>
<p class="text-muted">`justify-content-around`: Espacio uniforme *alrededor* de los elementos.</p>

<div class="d-flex justify-content-evenly bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white">A</div>
    <div class="p-2 border bg-success text-white">B</div>
</div>
<p class="text-muted">`justify-content-evenly`: Espacio uniforme entre los elementos *y* en los extremos.</p>

<!-- Justificación responsiva -->
<div class="d-flex justify-content-start justify-content-md-center bg-info text-white p-3 mb-3">
    <div class="p-2 border me-2">Móvil: inicio</div>
    <div class="p-2 border">MD+: centro</div>
</div>
```

### Alineación (Eje Secundario) (`align-items-*`)

Controla la alineación de los elementos flex a lo largo del eje secundario (perpendicular al eje principal).

```html
<div class="d-flex align-items-start bg-light p-3 border mb-3" style="height: 100px;">
    <div class="p-2 border bg-primary text-white">Corto</div>
    <div class="p-2 border bg-success text-white">Un poco más largo</div>
</div>
<p class="text-muted">`align-items-start`: Alineados al inicio del eje secundario (arriba en una fila).</p>

<div class="d-flex align-items-end bg-light p-3 border mb-3" style="height: 100px;">
    <div class="p-2 border bg-primary text-white">Corto</div>
    <div class="p-2 border bg-success text-white">Un poco más largo</div>
</div>
<p class="text-muted">`align-items-end`: Alineados al final del eje secundario (abajo en una fila).</p>

<div class="d-flex align-items-center bg-light p-3 border mb-3" style="height: 100px;">
    <div class="p-2 border bg-primary text-white">Corto</div>
    <div class="p-2 border bg-success text-white">Un poco más largo</div>
</div>
<p class="text-muted">`align-items-center`: Centrados en el eje secundario.</p>

<div class="d-flex align-items-baseline bg-light p-3 border mb-3" style="height: 100px;">
    <div class="p-2 border bg-primary text-white" style="font-size: 1.5rem;">Grande</div>
    <div class="p-2 border bg-success text-white">Pequeño</div>
</div>
<p class="text-muted">`align-items-baseline`: Alineados por la línea base del texto.</p>

<div class="d-flex align-items-stretch bg-light p-3 border mb-3" style="height: 100px;">
    <div class="p-2 border bg-primary text-white">Estira</div>
    <div class="p-2 border bg-success text-white">Para llenar</div>
</div>
<p class="text-muted">`align-items-stretch` (por omisión): Estira los elementos para llenar la altura del contenedor.</p>
```

### Auto-alineación de Elementos Flex (`align-self-*`)

Permite anular la alineación del contenedor para un elemento flex individual.

```html
<div class="d-flex bg-dark text-white p-3 border mb-3" style="height: 150px;">
    <div class="p-2 border bg-primary">Normal</div>
    <div class="align-self-start p-2 border bg-success">Auto-alineado arriba</div>
    <div class="align-self-center p-2 border bg-info">Auto-alineado al centro</div>
    <div class="align-self-end p-2 border bg-warning text-dark">Auto-alineado abajo</div>
</div>
```

### Flex Wrap (`flex-wrap`)

Controla si los elementos flex deben ajustarse a una nueva línea cuando no caben en una sola.

```html
<div class="d-flex flex-wrap bg-light p-3 border mb-3" style="width: 200px;">
    <div class="p-2 border bg-primary text-white w-50">Elemento largo 1</div>
    <div class="p-2 border bg-success text-white w-50">Elemento largo 2</div>
    <div class="p-2 border bg-info text-white w-50">Elemento largo 3</div>
</div>
<p class="text-muted">`flex-wrap`: Los elementos se ajustan a nuevas líneas.</p>

<div class="d-flex flex-nowrap overflow-auto bg-light p-3 border mb-3" style="width: 200px;">
    <div class="p-2 border bg-primary text-white">El</div>
    <div class="p-2 border bg-success text-white">contenido</div>
    <div class="p-2 border bg-info text-white">se</div>
    <div class="p-2 border bg-warning text-dark">desborda</div>
</div>
<p class="text-muted">`flex-nowrap` (por omisión): Los elementos no se ajustan y pueden desbordarse.</p>

<div class="d-flex flex-wrap-reverse bg-light p-3 border mb-3" style="width: 200px;">
    <div class="p-2 border bg-primary text-white w-50">1</div>
    <div class="p-2 border bg-success text-white w-50">2</div>
    <div class="p-2 border bg-info text-white w-50">3</div>
</div>
<p class="text-muted">`flex-wrap-reverse`: Se ajustan en orden inverso.</p>
```

### Crecimiento y Contracción (`flex-grow`, `flex-shrink`, `flex-fill`)

Controla cómo los elementos flex crecen o se contraen para llenar el espacio disponible.

```html
<div class="d-flex bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white flex-fill">`flex-fill` (ocupa todo el espacio restante)</div>
    <div class="p-2 border bg-success text-white">Normal</div>
</div>

<div class="d-flex bg-light p-3 border mb-3">
    <div class="p-2 border bg-primary text-white flex-grow-1">`flex-grow-1` (crece)</div>
    <div class="p-2 border bg-success text-white flex-grow-0">`flex-grow-0` (no crece)</div>
    <div class="p-2 border bg-info text-white">Normal</div>
</div>

<div class="d-flex bg-light p-3 border mb-3" style="width: 250px;">
    <div class="p-2 border bg-primary text-white flex-shrink-1" style="width: 150px;">`flex-shrink-1` (se contrae si es necesario)</div>
    <div class="p-2 border bg-success text-white flex-shrink-0" style="width: 150px;">`flex-shrink-0` (no se contrae)</div>
</div>
```



## 📐 Posicionamiento: Dónde colocar tus elementos

Las utilidades de posicionamiento (`position-*`) permiten controlar la forma en que un elemento se coloca en relación con su contenedor o con la ventana del navegador.

### Position (`position-*`)

```html
<div class="position-static bg-light p-2 mb-2 border">Posicionamiento estático (por omisión, ignora top/left/etc.)</div>

<div class="position-relative bg-light p-4 mb-5 border" style="height: 100px;">
    <p>Contenedor relativo.</p>
    <div class="position-absolute top-0 start-0 bg-primary text-white p-1">Absoluto (dentro del relativo)</div>
</div>
<p class="text-muted">`position-relative`: Permite que sus hijos `absolute` se posicionen con respecto a él.</p>
<p class="text-muted">`position-absolute`: Se posiciona en relación con el ancestro `relative` más cercano.</p>

<div class="position-fixed bottom-0 end-0 bg-success text-white p-2 m-3 shadow-lg" style="z-index: 1000;">
    Fijo (siempre visible)
</div>
<p class="text-muted">`position-fixed`: Se fija a la ventana del navegador, sin importar el scroll.</p>

<div class="bg-light p-5 mb-5 border" style="height: 200px;">
    <p>Scroll para ver sticky.</p>
    <div class="position-sticky top-0 bg-info text-white p-2" style="z-index: 999;">
        Pegajoso (sticky)
    </div>
    <p>Más contenido...</p><p>Más contenido...</p><p>Más contenido...</p>
</div>
<p class="text-muted">`position-sticky`: Se comporta como `relative` hasta que un umbral se cumple, luego como `fixed`.</p>
```

### Posiciones Específicas (`top-`, `bottom-`, `start-`, `end-`)

Estas clases, combinadas con `position-absolute` o `position-fixed`, te permiten colocar elementos en lugares precisos.

```html
<div class="position-relative bg-light p-5 border mb-5" style="height: 200px;">
    <div class="position-absolute top-0 start-0 bg-primary text-white p-1">Top-0 Start-0</div>
    <div class="position-absolute top-0 end-0 bg-success text-white p-1">Top-0 End-0</div>
    <div class="position-absolute bottom-0 start-0 bg-info text-white p-1">Bottom-0 Start-0</div>
    <div class="position-absolute bottom-0 end-0 bg-danger text-white p-1">Bottom-0 End-0</div>

    <!-- Valores porcentuales -->
    <div class="position-absolute top-50 start-50 bg-warning text-dark p-1">50% 50%</div>
</div>
```

### Transformaciones para Centrado (`translate-middle`)

Una de las utilidades más prácticas para centrar un elemento absolutamente en su contenedor.

```html
<div class="position-relative bg-dark text-white p-5 border mb-3" style="height: 200px;">
    <div class="position-absolute top-50 start-50 translate-middle bg-primary p-3 rounded">
        ¡Centrado perfectamente!
    </div>
    
    <div class="position-absolute top-0 start-50 translate-middle-x bg-success p-2 rounded">
        Centrado horizontalmente
    </div>
    
    <div class="position-absolute top-50 start-0 translate-middle-y bg-info p-2 rounded">
        Centrado verticalmente
    </div>
</div>
```



## 📝 Tipografía: Estiliza tu texto

Bootstrap ofrece una amplia gama de utilidades para controlar la apariencia del texto, desde el tamaño hasta la alineación y el peso de la fuente.

### Tamaños de Fuente (`fs-*`)

Utiliza una escala del `fs-1` (más grande) al `fs-6` (más pequeño) para tamaños de fuente semánticos y responsivos.

```html
<p class="fs-1">Título Grande (fs-1)</p>
<p class="fs-2">Título Mediano (fs-2)</p>
<p class="fs-3">Título Pequeño (fs-3)</p>
<p class="fs-4">Subtítulo (fs-4)</p>
<p class="fs-5">Texto Destacado (fs-5)</p>
<p class="fs-6">Texto Normal/Secundario (fs-6)</p>
```

### Peso de Fuente (`fw-*`)

Controla el `font-weight` del texto (negrita, ligera, etc.).

```html
<p class="fw-bold">Texto en negrita (fw-bold)</p>
<p class="fw-bolder">Texto aún más negrita (fw-bolder, si la fuente lo soporta)</p>
<p class="fw-semibold">Texto semi-negrita (fw-semibold)</p>
<p class="fw-medium">Texto peso medio (fw-medium)</p>
<p class="fw-normal">Texto peso normal (fw-normal, por omisión)</p>
<p class="fw-light">Texto ligero</p>
<p class="fw-lighter">Texto más ligero</p>
```

### Estilo de Fuente (`fst-*`)

Controla si el texto es `italic` (cursiva) o `normal`.

```html
<p class="fst-italic">Este es un texto en cursiva (fst-italic).</p>
<p class="fst-normal">Este texto es normal, sin cursiva (fst-normal).</p>
```

### Alineación de Texto (`text-*`)

Define cómo se alinea el texto dentro de su contenedor (izquierda, centro, derecha). En sistemas LTR (Left-to-Right, como el español), "start" es izquierda y "end" es derecha.

```html
<p class="text-start bg-light p-2 mb-2">Este texto está alineado al inicio (izquierda).</p>
<p class="text-center bg-light p-2 mb-2">Este texto está centrado.</p>
<p class="text-end bg-light p-2 mb-2">Este texto está alineado al final (derecha).</p>

<!-- Alineación responsiva: ¡Adapta la alineación a cada pantalla! -->
<p class="text-start text-md-center text-lg-end bg-info text-white p-2">
    En móviles: izquierda. En tablets (MD): centro. En desktops (LG): derecha.
</p>
```

### Transformación de Texto (`text-*`)

Cambia la capitalización del texto sin modificar el HTML original.

```html
<p class="text-lowercase bg-light p-2 mb-2">TEXTO EN minúsculas.</p>
<p class="text-uppercase bg-light p-2 mb-2">texto en MAYÚSCULAS.</p>
<p class="text-capitalize bg-light p-2 mb-2">texto con primera letra mayúscula de cada palabra.</p>
```

### Decoración de Texto (`text-decoration-*`)

Controla si el texto tiene subrayado, tachado, o ninguna decoración.

```html
<p class="text-decoration-none bg-light p-2 mb-2">Texto sin decoración (text-decoration-none).</p>
<p class="text-decoration-underline bg-light p-2 mb-2">Texto subrayado (text-decoration-underline).</p>
<p class="text-decoration-line-through bg-light p-2 mb-2">Texto tachado (text-decoration-line-through).</p>
```

### Altura de Línea (`lh-*`)

Ajusta el espacio vertical entre las líneas de texto, mejorando la legibilidad.

```html
<p class="lh-1 bg-light p-2 mb-2">Esta es una línea de texto con una altura de línea reducida (lh-1).</p>
<p class="lh-sm bg-light p-2 mb-2">Esta es una línea de texto con una altura de línea pequeña (lh-sm).</p>
<p class="lh-base bg-light p-2 mb-2">Esta es una línea de texto con una altura de línea base (lh-base, por omisión).</p>
<p class="lh-lg bg-light p-2 mb-2">Esta es una línea de texto con una altura de línea grande (lh-lg).</p>
```



## 📦 Bordes: Define los límites de tus elementos

Las utilidades de bordes te permiten añadir, quitar y personalizar los bordes de cualquier elemento HTML de forma rápida y sencilla.

### Bordes Básicos (`border`, `border-*0`)

Añade un borde a todos los lados o solo a lados específicos. Puedes usar `border-0` para quitar todos los bordes, o `border-{lado}-0` para quitar un lado específico.

```html
<div class="border p-3 mb-2 bg-light">Este div tiene un borde completo.</div>
<div class="border-top p-3 mb-2 bg-light">Solo borde superior.</div>
<div class="border-end p-3 mb-2 bg-light">Solo borde derecho.</div>
<div class="border-bottom p-3 mb-2 bg-light">Solo borde inferior.</div>
<div class="border-start p-3 mb-2 bg-light">Solo borde izquierdo.</div>
<div class="border-0 p-3 mb-2 bg-light">Sin bordes.</div>

<!-- Quitar bordes específicos de un elemento que ya tiene bordes -->
<div class="border border-top-0 p-3 mb-2 bg-dark text-white">Borde excepto el superior.</div>
<div class="border border-end-0 p-3 mb-2 bg-dark text-white">Borde excepto el derecho.</div>
```

### Colores de Borde (`border-*`)

Aplica colores temáticos a tus bordes, utilizando la misma paleta que los colores de texto y fondo.

```html
<div class="border border-primary p-3 mb-2 bg-light">Borde azul primario.</div>
<div class="border border-secondary p-3 mb-2 bg-light">Borde gris secundario.</div>
<div class="border border-success p-3 mb-2 bg-light">Borde verde de éxito.</div>
<div class="border border-danger p-3 mb-2 bg-light">Borde rojo de peligro.</div>
<div class="border border-warning p-3 mb-2 bg-light">Borde amarillo de advertencia.</div>
<div class="border border-info p-3 mb-2 bg-light">Borde azul claro informativo.</div>
<div class="border border-light p-3 mb-2 bg-dark text-white">Borde gris claro (sobre fondo oscuro).</div>
<div class="border border-dark p-3 mb-2 bg-light">Borde gris oscuro.</div>
<div class="border border-white p-3 mb-2 bg-dark text-white">Borde blanco (sobre fondo oscuro).</div>
```

### Grosor de Borde (`border-{1-5}`)

Ajusta el grosor del borde, desde `border-1` (más fino) hasta `border-5` (más grueso).

```html
<div class="border border-1 p-3 mb-2 bg-light">Borde grosor 1.</div>
<div class="border border-2 p-3 mb-2 bg-light">Borde grosor 2.</div>
<div class="border border-3 p-3 mb-2 bg-light">Borde grosor 3 (por omisión para `border`).</div>
<div class="border border-4 p-3 mb-2 bg-light">Borde grosor 4.</div>
<div class="border border-5 p-3 mb-2 bg-light">Borde grosor 5.</div>
```

### Esquinas Redondeadas (`rounded-*`)

Aplica diferentes niveles de `border-radius` para suavizar las esquinas de tus elementos, creando formas como círculos o píldoras.

```html
<div class="rounded p-3 mb-2 bg-primary text-white">Esquinas redondeadas normales (rounded).</div>
<div class="rounded-0 p-3 mb-2 bg-success text-white">Sin esquinas redondeadas (rounded-0).</div>
<div class="rounded-1 p-3 mb-2 bg-info text-white">Esquinas ligeramente redondeadas (rounded-1).</div>
<div class="rounded-2 p-3 mb-2 bg-warning text-dark">Esquinas medianamente redondeadas (rounded-2).</div>
<div class="rounded-3 p-3 mb-2 bg-danger text-white">Esquinas muy redondeadas (rounded-3).</div>
<div class="rounded-circle bg-dark text-white d-inline-block p-4 mb-2">Círculo perfecto (rounded-circle).</div>
<div class="rounded-pill bg-secondary text-white d-inline-block px-4 py-2 mb-2">Forma de píldora (rounded-pill).</div>

<!-- Esquinas específicas: redondea solo ciertos lados -->
<div class="rounded-top p-3 mb-2 bg-primary text-white">Solo esquinas superiores redondeadas.</div>
<div class="rounded-end p-3 mb-2 bg-success text-white">Solo esquinas derechas redondeadas.</div>
<div class="rounded-bottom p-3 mb-2 bg-info text-white">Solo esquinas inferiores redondeadas.</div>
<div class="rounded-start p-3 mb-2 bg-warning text-dark">Solo esquinas izquierdas redondeadas.</div>
```



## 🌊 Opacidad y Sombras: Detalles visuales que importan

Añade efectos visuales sutiles para mejorar la estética y la jerarquía de tus elementos.

### Opacidad (`opacity-{25|50|75|100}`)

Controla la transparencia de un elemento.

```html
<div class="bg-primary text-white p-3 mb-2">Fondo visible.</div>
<div class="opacity-75 bg-primary text-white p-3 mb-2">75% visible.</div>
<div class="opacity-50 bg-primary text-white p-3 mb-2">50% visible.</div>
<div class="opacity-25 bg-primary text-white p-3 mb-2">25% visible.</div>
<p class="text-muted">La opacidad afecta al elemento y a todo su contenido.</p>
```

### Sombras (`shadow-*`)

Añade diferentes niveles de sombras a los elementos, dándoles profundidad.

```html
<div class="shadow-none p-3 mb-3 bg-light rounded">Sin sombra (shadow-none).</div>
<div class="shadow-sm p-3 mb-3 bg-light rounded">Sombra pequeña (shadow-sm).</div>
<div class="shadow p-3 mb-3 bg-light rounded">Sombra normal (shadow).</div>
<div class="shadow-lg p-3 mb-3 bg-light rounded">Sombra grande (shadow-lg).</div>
```



## 📏 Dimensiones: Controla el tamaño de tus elementos

Las utilidades de dimensiones te permiten establecer anchos y alturas relativos y fijos, tanto para el contenido como para el viewport.

### Anchura (`w-*`)

Establece el `width` de un elemento como un porcentaje del ancho de su contenedor.

```html
<div class="bg-dark p-2 mb-2">
    <div class="w-25 bg-primary text-white p-2 mb-1">Ancho 25%</div>
    <div class="w-50 bg-success text-white p-2 mb-1">Ancho 50%</div>
    <div class="w-75 bg-info text-white p-2 mb-1">Ancho 75%</div>
    <div class="w-100 bg-danger text-white p-2 mb-1">Ancho 100%</div>
    <div class="w-auto bg-warning text-dark p-2">Ancho automático (w-auto, por omisión)</div>
</div>

<!-- Ancho máximo: mw-100 asegura que nunca exceda el ancho de su padre -->
<div class="bg-dark p-2">
    <img src="https://via.placeholder.com/600x150" class="mw-100 d-block border border-white" alt="Imagen de ejemplo">
    <small class="text-white-50">La imagen se adapta al ancho máximo del contenedor (mw-100).</small>
</div>
```

### Altura (`h-*`, `vh-*`)

Establece la `height` de un elemento. Para que las alturas porcentuales (`h-25`, `h-50`, etc.) funcionen, el elemento padre debe tener una altura definida. Las alturas `vh` se refieren al viewport.

```html
<div style="height: 200px; border: 1px solid black;" class="mb-3 d-flex flex-column justify-content-between">
    <div class="h-25 bg-primary text-white text-center">Altura 25%</div>
    <div class="h-50 bg-secondary text-white text-center">Altura 50%</div>
    <div class="h-auto bg-warning text-dark text-center">Altura automática</div>
</div>

<!-- Altura máxima: mh-100 asegura que nunca exceda la altura de su padre -->
<div style="height: 100px; overflow: auto; border: 1px dashed blue;" class="mb-3">
    <div class="mh-100 bg-info text-white p-2">
        Este contenido tiene una altura máxima del 100% del padre. Si el contenido es más largo, se desbordará según el overflow del padre.
        Lorem ipsum dolor sit amet, consectetur adipisicing elit.
    </div>
</div>

<!-- Altura de viewport: Se basa en la altura visible del navegador -->
<div class="vh-100 bg-success text-white p-5 d-flex align-items-center justify-content-center">
    Altura 100% del viewport (vh-100) - ¡Ocupa toda la pantalla verticalmente!
</div>
<div class="min-vh-100 bg-danger text-white p-5 d-flex align-items-center justify-content-center">
    Altura mínima 100% del viewport (min-vh-100). Crece si el contenido es mayor.
</div>
```



## 🔄 Overflow: Manejo de contenido que se desborda

Estas utilidades controlan qué sucede cuando el contenido de un elemento es demasiado grande para caber dentro de sus dimensiones.

### Control de Desbordamiento (`overflow-*`)

```html
<div class="overflow-auto bg-light p-3 mb-2 border" style="width: 250px; height: 100px;">
    Contenido muy muy largo que activará barras de scroll automático cuando sea necesario
    para evitar el desbordamiento visual del contenedor.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.
</div>
<p class="text-muted">`overflow-auto`: Barras de scroll solo si el contenido se desborda.</p>

<div class="overflow-hidden bg-light p-3 mb-2 border" style="width: 250px; height: 100px;">
    Contenido que será cortado y oculto si excede las dimensiones del contenedor.
    No se mostrarán barras de scroll. Esto es útil para diseños fijos.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.
</div>
<p class="text-muted">`overflow-hidden`: El contenido se corta y no es visible si excede el contenedor.</p>

<div class="overflow-visible bg-light p-3 mb-2 border" style="width: 250px; height: 100px;">
    Contenido que será visible incluso si excede las dimensiones del contenedor.
    Puede superponerse a otros elementos. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
</div>
<p class="text-muted">`overflow-visible`: El contenido desbordado es visible y puede invadir otros elementos.</p>

<div class="overflow-scroll bg-light p-3 mb-2 border" style="width: 250px; height: 100px;">
    Contenido con barras de scroll siempre visibles, sin importar si el contenido
    es lo suficientemente largo como para necesitarlas.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.
</div>
<p class="text-muted">`overflow-scroll`: Las barras de scroll siempre están presentes.</p>
```

### Overflow por Eje (`overflow-x-*`, `overflow-y-*`)

Controla el desbordamiento de manera independiente para el eje horizontal (`x`) y vertical (`y`).

```html
<div class="overflow-x-auto overflow-y-hidden bg-dark text-white p-3 mb-2 border" style="width: 200px; height: 100px; white-space: nowrap;">
    Este contenido es muy largo horizontalmente, así que permite scroll horizontal,
    pero el scroll vertical está oculto. Lorem ipsum dolor sit amet, consectetur
    adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
</div>
<p class="text-muted">`overflow-x-auto overflow-y-hidden`: Scroll horizontal, sin scroll vertical.</p>

<div class="overflow-x-hidden overflow-y-scroll bg-dark text-white p-3 mb-2 border" style="width: 200px; height: 100px;">
    Sin scroll horizontal, pero el scroll vertical siempre visible.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
</div>
<p class="text-muted">`overflow-x-hidden overflow-y-scroll`: Sin scroll horizontal, scroll vertical siempre visible.</p>
```



## 🎯 Interacciones del Usuario: Mejora la experiencia

Estas utilidades modifican cómo los usuarios pueden interactuar con ciertos elementos, especialmente con el texto y los eventos del ratón.

### Selección de Texto (`user-select-*`)

Controla si el usuario puede seleccionar el texto de un elemento.

```html
<p class="user-select-all bg-light p-2 mb-2">Todo este texto se selecciona al hacer clic (user-select-all).</p>
<p class="user-select-auto bg-light p-2 mb-2">Selección normal de texto (user-select-auto, por omisión).</p>
<p class="user-select-none bg-light p-2 mb-2">Este texto no se puede seleccionar (user-select-none).</p>
```

### Eventos de Puntero (`pe-*`)

Controla si un elemento reacciona a los eventos del puntero del ratón (clics, hover, etc.).

```html
<button class="btn btn-primary pe-none me-3">No clickeable (pe-none)</button>
<button class="btn btn-success pe-auto">Clickeable (pe-auto)</button>
<p class="text-muted mt-2">`pe-none` es útil para superposiciones o elementos decorativos que no deben ser interactivos.</p>
```



## 📱 Utilidades Responsivas: Adaptación sin esfuerzo

Las clases responsivas son la clave para crear diseños que se vean bien en cualquier dispositivo. Combinan las utilidades básicas con los prefijos de breakpoint (`-sm`, `-md`, `-lg`, etc.).

### Patrones Comunes de Responsividad

```html
<!-- Espaciado responsivo: El margen aumenta a medida que la pantalla es más grande -->
<div class="m-2 m-sm-3 m-md-4 m-lg-5 bg-dark text-white p-3">
    Margen que aumenta: `m-2` (móvil), `m-sm-3` (pequeño), `m-md-4` (mediano), `m-lg-5` (grande).
</div>
<p class="text-muted">Inspecciona este elemento en diferentes tamaños de pantalla para ver el efecto.</p>

<!-- Texto responsivo: El tamaño de la fuente crece con el viewport -->
<h1 class="fs-6 fs-sm-5 fs-md-4 fs-lg-3 fs-xl-2 fs-xxl-1 bg-primary text-white p-3 mt-4">
    Título que crece con el tamaño de pantalla.
</h1>
<p class="text-muted">`fs-6` en extra pequeño, `fs-5` en SM, y así sucesivamente hasta `fs-xxl-1`.</p>

<!-- Flexbox responsivo: Cambia la dirección y el espaciado de los elementos -->
<div class="d-flex flex-column flex-md-row bg-secondary text-white p-3 mt-4">
    <div class="p-2 border mb-3 mb-md-0 me-md-3">Elemento 1 (vertical en móvil, horizontal en MD+)</div>
    <div class="p-2 border">Elemento 2 (sin margen inferior en MD+)</div>
</div>
<p class="text-muted">`flex-column` en móvil, `flex-md-row` en MD+. Margenes `mb-3` en móvil, `mb-md-0` y `me-md-3` en MD+.</p>

<!-- Visibilidad responsiva: Muestra u oculta elementos según el breakpoint -->
<div class="d-block d-md-none bg-success text-white p-3 mt-4">
    Solo visible en dispositivos móviles.
</div>
<div class="d-none d-md-block d-xl-none bg-info text-white p-3 mt-4">
    Solo visible en tablets (SM a LG).
</div>
<div class="d-none d-xl-block bg-warning text-dark p-3 mt-4">
    Solo visible en desktops grandes (XL+).
</div>
<p class="text-muted">Prueba redimensionar tu navegador para ver cómo cambian los elementos.</p>
```



## 💡 Ejemplos Prácticos Combinando Utilidades

Aquí veremos cómo la combinación inteligente de utilidades puede construir componentes complejos y responsivos con muy poco código.

### Tarjeta Centrada y Responsiva (Formulario de Login)

```html
<div class="d-flex justify-content-center align-items-center min-vh-100 bg-light p-3">
    <div class="card shadow-lg border-0" style="width: 100%; max-width: 400px;">
        <div class="card-body p-4">
            <h5 class="card-title text-center mb-4 fs-3 fw-bold text-primary">Iniciar Sesión</h5>
            <form>
                <div class="mb-3">
                    <input type="email" class="form-control" placeholder="Email">
                </div>
                <div class="mb-4">
                    <input type="password" class="form-control" placeholder="Contraseña">
                </div>
                <button type="submit" class="btn btn-primary w-100 py-2 fs-5">Ingresar</button>
                <p class="text-center mt-3 text-muted fs-6">
                    ¿Olvidaste tu contraseña? <a href="#" class="text-info text-decoration-none">Recuperar</a>
                </p>
            </form>
        </div>
    </div>
</div>
```
**Explicación:**
*   `d-flex justify-content-center align-items-center min-vh-100`: Centra vertical y horizontalmente el contenido en toda la altura del viewport.
*   `card shadow-lg border-0`: Una tarjeta con una sombra grande y sin bordes.
*   `style="width: 100%; max-width: 400px;"`: Asegura que la tarjeta siempre ocupe el 100% del ancho disponible, pero no más de 400px.
*   `card-body p-4`: Relleno interior de la tarjeta.
*   `text-center mb-4 fs-3 fw-bold text-primary`: Texto centrado, margen inferior, tamaño de fuente grande, negrita y color primario.
*   `mb-3`, `mb-4`: Margen inferior entre los campos del formulario.
*   `w-100 py-2 fs-5`: Botón que ocupa todo el ancho, con padding vertical y tamaño de fuente grande.

### Lista Responsiva con Separadores y Badges

```html
<div class="container py-5 bg-dark">
    <div class="row">
        <div class="col-12 col-md-8 col-lg-6 mx-auto">
            <h4 class="text-white text-center mb-4">Mis Tareas</h4>
            <div class="list-group shadow">
                <div class="list-group-item d-flex justify-content-between align-items-center bg-light mb-2 rounded">
                    <div>
                        <h6 class="mb-1 fw-bold text-primary fs-5">Comprar víveres</h6>
                        <p class="mb-1 text-muted fs-6">Frutas, verduras, lácteos y pan.</p>
                    </div>
                    <span class="badge bg-danger rounded-pill fs-6 px-3 py-2">Urgente</span>
                </div>
                <div class="list-group-item d-flex justify-content-between align-items-center bg-light mb-2 rounded">
                    <div>
                        <h6 class="mb-1 fw-bold text-success fs-5">Preparar presentación</h6>
                        <p class="mb-1 text-muted fs-6">Revisar diapositivas y guion.</p>
                    </div>
                    <span class="badge bg-warning text-dark rounded-pill fs-6 px-3 py-2">Pendiente</span>
                </div>
                <div class="list-group-item d-flex justify-content-between align-items-center bg-light rounded">
                    <div>
                        <h6 class="mb-1 fw-bold text-secondary fs-5">Llamar a Juan</h6>
                        <p class="mb-1 text-muted fs-6">Confirmar reunión del lunes.</p>
                    </div>
                    <span class="badge bg-info rounded-pill fs-6 px-3 py-2">Programado</span>
                </div>
            </div>
        </div>
    </div>
</div>
```
**Explicación:**
*   `container`, `row`, `col-12 col-md-8 col-lg-6 mx-auto`: Estructura una columna centrada que se adapta a diferentes tamaños de pantalla.
*   `list-group shadow`: Un contenedor de lista con una sombra.
*   `list-group-item d-flex justify-content-between align-items-center`: Cada elemento de la lista es un contenedor flex que alinea el contenido (texto y badge) a los extremos y verticalmente al centro.
*   `mb-2 rounded`: Margen inferior y esquinas redondeadas para cada ítem.
*   `badge bg-danger rounded-pill fs-6 px-3 py-2`: Un "badge" (etiqueta) con color de peligro, forma de píldora, tamaño de fuente pequeño y padding.

### Botón Flotante (Action Button)

```html
<button class="btn btn-primary position-fixed bottom-0 end-0 m-4 rounded-circle shadow-lg" style="width: 60px; height: 60px; font-size: 1.5rem;">
    <!-- Icono de Bootstrap Icons, asegúrate de tenerlos enlazados -->
    <i class="bi bi-plus-lg d-flex justify-content-center align-items-center h-100"></i>
</button>
<p class="text-muted m-5">Desplázate hacia abajo para ver el botón flotante en la esquina inferior derecha.</p>
```
**Explicación:**
*   `position-fixed bottom-0 end-0 m-4`: Fija el botón a la ventana, en la esquina inferior derecha con un margen de 4 unidades.
*   `rounded-circle shadow-lg`: Le da forma de círculo y una sombra grande.
*   `style="width: 60px; height: 60px; font-size: 1.5rem;"`: Dimensiones fijas para el círculo y tamaño del icono.
*   `d-flex justify-content-center align-items-center h-100`: Usa Flexbox para centrar perfectamente el icono dentro del botón.

### Grid de Imágenes Responsivo

```html
<div class="container py-4 bg-light">
    <h3 class="text-center mb-4">Nuestra Galería</h3>
    <div class="row g-3">
        <div class="col-6 col-md-4 col-lg-3">
            <img src="https://via.placeholder.com/300x200/ADD8E6/000000?text=Imagen+1" class="img-fluid rounded shadow-sm w-100" alt="Imagen de galería 1">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="https://via.placeholder.com/300x200/FFD700/000000?text=Imagen+2" class="img-fluid rounded shadow-sm w-100" alt="Imagen de galería 2">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="https://via.placeholder.com/300x200/90EE90/000000?text=Imagen+3" class="img-fluid rounded shadow-sm w-100" alt="Imagen de galería 3">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="https://via.placeholder.com/300x200/DDA0DD/000000?text=Imagen+4" class="img-fluid rounded shadow-sm w-100" alt="Imagen de galería 4">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="https://via.placeholder.com/300x200/FFB6C1/000000?text=Imagen+5" class="img-fluid rounded shadow-sm w-100" alt="Imagen de galería 5">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="https://via.placeholder.com/300x200/87CEEB/000000?text=Imagen+6" class="img-fluid rounded shadow-sm w-100" alt="Imagen de galería 6">
        </div>
    </div>
</div>
```
**Explicación:**
*   `container`, `row g-3`: Define una cuadrícula con un espacio (`g-3`) entre las columnas.
*   `col-6 col-md-4 col-lg-3`: Define el ancho de cada columna según el tamaño de pantalla:
    *   `col-6`: 2 columnas por fila en móviles (cada imagen ocupa el 50% del ancho).
    *   `col-md-4`: 3 columnas por fila en tablets (cada imagen ocupa el 33.33%).
    *   `col-lg-3`: 4 columnas por fila en desktops (cada imagen ocupa el 25%).
*   `img-fluid rounded shadow-sm w-100`: Hace que la imagen sea responsiva, con esquinas redondeadas, una sombra pequeña y ocupe el 100% del ancho de su columna.



## 🔧 Consejos y Mejores Prácticas

Maximizar el uso de las utilidades de Bootstrap puede acelerar tu desarrollo y mejorar la consistencia de tu UI. Aquí tienes algunas pautas.

### ✅ Buenas Prácticas

1.  **Prioriza las utilidades sobre CSS personalizado:** Siempre que puedas lograr un efecto con una clase de utilidad de Bootstrap, úsala en lugar de escribir tu propio CSS. Esto reduce el tamaño del archivo CSS, mejora la mantenibilidad y garantiza la consistencia con el diseño de Bootstrap.
2.  **Usa espaciado consistente:** Adhiérete al sistema de espaciado de Bootstrap (0-5) para márgenes y rellenos. Evita valores arbitrarios en tu CSS personalizado.
3.  **Piensa *mobile-first*:** Al aplicar clases responsivas (ej. `d-none d-md-block`), empieza por el estilo que quieres en el tamaño de pantalla más pequeño y luego "sobrescribe" para tamaños más grandes.
4.  **Mantén la legibilidad del HTML:** Aunque las utilidades fomentan más clases en el HTML, intenta agruparlas lógicamente. Si un elemento acumula demasiadas clases y se vuelve ilegible, considera si puedes refactorizarlo o encapsularlo en un componente si es un patrón recurrente.
5.  **Documenta combinaciones complejas:** Si creas una combinación de utilidades particular para un componente específico, añade un comentario o una nota en tu documentación de desarrollo para referencia futura.
6.  **Utiliza variables CSS para personalización:** Si necesitas ajustar los valores por omisión (ej. los colores o los tamaños de espaciado), hazlo a través de las variables CSS de Bootstrap o personalizando los archivos Sass de Bootstrap, en lugar de sobrescribir clases con `!important`.

### ⚠️ Errores Comunes a Evitar

1.  **Abusar de `!important`:** No uses `!important` en tu CSS personalizado para sobrescribir las utilidades de Bootstrap. Esto rompe la cascada de CSS y dificulta el mantenimiento. Si necesitas sobrescribir, asegúrate de que tu CSS tiene una especificidad mayor o personaliza Bootstrap correctamente.
2.  **Mezclar sistemas de espaciado:** No combines arbitrariamente utilidades de espaciado de Bootstrap con propiedades `margin` o `padding` personalizadas en tu CSS. Esto lleva a resultados impredecibles y a un diseño inconsistente.
3.  **Olvidar la accesibilidad:** Al usar utilidades de color, asegúrate de que haya suficiente contraste entre el texto y el fondo. Para elementos ocultos (`d-none`), considera si es necesario proporcionar una alternativa para usuarios de tecnologías de asistencia.
4.  **Sobrecargar elementos con demasiadas clases:** Si un `div` tiene 15 clases de utilidad, puede ser un signo de que ese elemento podría ser un componente más complejo o que estás abusando de las utilidades. A veces, unas pocas líneas de CSS personalizado son más claras.

### 🎨 Orden Recomendado de Clases en el HTML

Aunque el orden de las clases CSS en el HTML generalmente no afecta el estilo (a menos que haya conflicto de especificidad, lo cual no es común con las utilidades de Bootstrap), un orden lógico puede mejorar la legibilidad del código. Una sugerencia es agruparlas por tipo:

```html
<!-- Orden lógico sugerido:
     1. Display (d-*, flex-*, grid-*)
     2. Posición (position-*, top-*, start-*, translate-*)
     3. Dimensiones (w-*, h-*, mw-*, mh-*, vh-*)
     4. Espaciado (p-*, m-*)
     5. Colores (bg-*, text-*)
     6. Bordes (border-*, rounded-*)
     7. Sombras (shadow-*)
     8. Tipografía (fs-*, fw-*, text-align-*)
     9. Otros (overflow-*, user-select-*, pe-*)
-->
<div class="d-flex position-relative w-100 h-auto p-3 m-2 bg-primary text-white rounded shadow-sm fs-5 fw-bold text-center overflow-hidden">
    Contenido con clases ordenadas lógicamente para una mejor lectura y comprensión.
</div>
<p class="text-muted mt-2">Este orden es una recomendación, no una regla estricta, pero ayuda a mantener la coherencia.</p>
```



# 📚 Referencia Rápida de Prefijos de Utilidades Bootstrap

Esta tabla resume los prefijos de las clases utilitarias de Bootstrap y los modificadores responsivos. Es una excelente herramienta para tener a mano cuando estés desarrollando.

## Tabla Completa de Clases Utilitarias por Prefijo

| Prefijo        | Propiedad CSS Principal                               | Ejemplo de Uso                                        | Descripción                                                           |
| :- | :- | :- | :-- |
| `m-`           | `margin`                                              | `m-3`, `mt-2`, `mx-auto`                              | Margen en todos los lados, superior, horizontal, etc.                 |
| `p-`           | `padding`                                             | `p-4`, `py-3`, `px-2`                                 | Relleno en todos los lados, vertical, horizontal, etc.                |
| `d-`           | `display`                                             | `d-flex`, `d-none`, `d-block`                         | Controla el tipo de visualización del elemento.                       |
| `flex-`        | Propiedades Flexbox (`flex-direction`, `flex-wrap`)   | `flex-column`, `flex-wrap`, `flex-grow-1`             | Dirección, envoltura, crecimiento y contracción de ítems flex.        |
| `justify-content-` | `justify-content` (eje principal de Flexbox)      | `justify-content-center`, `justify-content-between`   | Alineación de ítems flex en el eje principal.                         |
| `align-items-` | `align-items` (eje secundario de Flexbox)             | `align-items-start`, `align-items-center`             | Alineación de ítems flex en el eje secundario.                        |
| `align-self-`  | `align-self` (para un ítem flex individual)           | `align-self-end`, `align-self-center`                 | Anula la alineación del contenedor flex para un ítem específico.     |
| `text-`        | `color`, `text-align`, `text-transform`, `font-size` | `text-center`, `text-primary`, `text-uppercase`       | Color, alineación, transformación del texto, y atajos de tamaño.      |
| `bg-`          | `background-color`                                    | `bg-primary`, `bg-light`, `bg-gradient`               | Color de fondo del elemento, incluyendo gradientes.                   |
| `border`       | `border` (todos los lados)                            | `border`                                              | Añade un borde por defecto.                                           |
| `border-`      | `border-width`, `border-color`, `border-style`        | `border-2`, `border-primary`, `border-top-0`          | Grosor, color o eliminación de bordes específicos.                   |
| `rounded-`     | `border-radius`                                       | `rounded-3`, `rounded-circle`, `rounded-top`          | Redondeo de esquinas (todos los lados o específicos), círculos, píldoras. |
| `w-`           | `width`                                               | `w-100`, `w-50`, `w-auto`                             | Anchura porcentual o automática.                                      |
| `h-`           | `height`                                              | `h-100`, `h-25`, `vh-100`                             | Altura porcentual, automática o del viewport.                         |
| `position-`    | `position`                                            | `position-relative`, `position-absolute`, `position-fixed` | Tipo de posicionamiento del elemento.                                 |
| `top-`, `bottom-`, `start-`, `end-` | Propiedades de posicionamiento (`top`, `bottom`, `left`, `right`) | `top-0`, `bottom-50`, `start-0`                       | Ajusta la posición de un elemento posicionado.                       |
| `shadow-`      | `box-shadow`                                          | `shadow-sm`, `shadow-lg`, `shadow-none`               | Añade diferentes niveles de sombra o la elimina.                     |
| `opacity-`     | `opacity`                                             | `opacity-25`, `opacity-75`, `opacity-100`             | Controla la transparencia del elemento.                               |
| `fs-`          | `font-size`                                           | `fs-1`, `fs-4`, `fs-6`                                | Tamaños de fuente predefinidos (de más grande a más pequeño).        |
| `fw-`          | `font-weight`                                         | `fw-bold`, `fw-light`, `fw-normal`                    | Grosor (peso) de la fuente.                                           |
| `fst-`         | `font-style`                                          | `fst-italic`, `fst-normal`                            | Estilo de la fuente (cursiva o normal).                               |
| `lh-`          | `line-height`                                         | `lh-1`, `lh-base`, `lh-lg`                            | Altura de línea del texto.                                            |
| `overflow-`    | `overflow`                                            | `overflow-hidden`, `overflow-auto`, `overflow-x-scroll` | Controla cómo se maneja el contenido que desborda un contenedor.      |
| `user-select-` | `user-select`                                         | `user-select-none`, `user-select-all`                 | Controla si el texto es seleccionable por el usuario.                 |
| `pe-`          | `pointer-events`                                      | `pe-none`, `pe-auto`                                  | Controla si un elemento responde a eventos del puntero (clics, etc.). |
| `translate-`   | `transform` (`translate`)                             | `translate-middle`, `translate-middle-x`              | Centra elementos utilizando transformaciones CSS.                     |

## Modificadores Responsivos (Breakpoints)

Casi todas las utilidades pueden combinarse con los modificadores de breakpoint para aplicar estilos específicos según el tamaño de la pantalla.

| Breakpoint        | Sufijo   | Tamaño de Pantalla (min-width) | Dispositivos Típicos                          |
| :- | :- | :-- | :-- |
| Extra pequeño     | (ninguno) | `<576px`                        | Teléfonos pequeños, la mayoría de los móviles |
| Pequeño           | `-sm`    | `≥576px`                       | Teléfonos grandes, algunas tablets            |
| Mediano           | `-md`    | `≥768px`                       | Tablets, Laptops pequeñas                     |
| Grande            | `-lg`    | `≥992px`                       | Laptops, Desktops                             |
| Extra grande      | `-xl`    | `≥1200px`                      | Desktops grandes                              |
| Extra extra grande | `-xxl`   | `≥1400px`                      | Monitores muy grandes                         |

### Ejemplos de uso responsivo:

*   `d-none d-md-block` &rarr; Oculto por defecto, pero visible desde el tamaño de pantalla `md` (tablet y superior).
*   `text-center text-lg-start` &rarr; Texto centrado en pantallas pequeñas, pero alineado a la izquierda desde el tamaño `lg` (desktop y superior).
*   `p-2 p-md-4 p-lg-5` &rarr; Un `padding` de 2 unidades en móvil, 4 unidades en `md` y 5 unidades en `lg`.
*   `w-100 w-sm-75 w-lg-50` &rarr; Un elemento ocupa el 100% del ancho en móvil, el 75% en `sm` y el 50% en `lg`.



## 📝 Ejercicios Prácticos con Clases Utilitarias

A continuación, se presentan una serie de ejercicios que te ayudarán a consolidar lo aprendido sobre las clases utilitarias de Bootstrap. Intenta resolverlos utilizando solo las clases que hemos visto en esta guía.

**Instrucciones:**
*   Para cada ejercicio, crea un nuevo archivo HTML o trabaja en un entorno de desarrollo donde tengas Bootstrap enlazado (CDN recomendado para practicar rápidamente).
*   Intenta resolver cada problema usando la menor cantidad de código HTML posible y exclusivamente clases de utilidad de Bootstrap.
*   ¡No dudes en consultar la guía o la tabla de referencia si lo necesitas!



### Ejercicio 1: Tarjeta de Producto Simple

**Objetivo:** Crear una tarjeta básica para un producto con imagen, título, descripción y precio, aplicando estilos de espaciado, tipografía y bordes.

**Requisitos:**
1.  Un contenedor principal para la tarjeta (un `div`).
2.  Una imagen de producto (puedes usar un placeholder como `https://via.placeholder.com/200x150`).
3.  Un título de producto (`h5`).
4.  Una descripción corta del producto (`p`).
5.  Un precio destacado (`span`).
6.  La tarjeta debe tener un fondo blanco, una sombra ligera y esquinas redondeadas.
7.  El texto del título debe ser negrita y de color primario.
8.  La descripción debe ser de color secundario y ligeramente más pequeña.
9.  El precio debe ser grande y de color verde (success).
10. La imagen debe ser responsiva y ocupar todo el ancho disponible dentro de la tarjeta.
11. Asegúrate de que haya un buen relleno interno en la tarjeta y un margen inferior entre los elementos de texto.

**Código base (a completar):**

```html
<div class="[CLASES_TARJETA] [OTRAS_CLASES]">
    <img src="https://via.placeholder.com/200x150" alt="Producto" class="[CLASES_IMAGEN]">
    <div class="[CLASES_CUERPO_TARJETA]">
        <h5 class="[CLASES_TITULO]">Nombre del Producto</h5>
        <p class="[CLASES_DESCRIPCION]">Una descripción breve y atractiva del producto que lo hace irresistible.</p>
        <span class="[CLASES_PRECIO]">€29.99</span>
    </div>
</div>
```



### Ejercicio 2: Barra de Notificación Responsiva

**Objetivo:** Crear una barra de notificación que se adapte a diferentes tamaños de pantalla y muestre un mensaje de advertencia.

**Requisitos:**
1.  Un `div` que actúe como barra de notificación.
2.  Debe tener un fondo amarillo (`bg-warning`) y texto oscuro (`text-dark`).
3.  Debe tener un padding adecuado en todos los lados.
4.  El texto debe estar centrado en pantallas pequeñas y alineado a la izquierda en pantallas medianas y grandes.
5.  El mensaje debe decir: "¡Atención! Oferta especial por tiempo limitado."
6.  Debe tener un botón de "Cerrar" (`<button>X</button>`) alineado a la derecha en pantallas medianas y grandes, y centrado debajo del texto en pantallas pequeñas.
7.  El botón "Cerrar" debe tener un margen izquierdo en pantallas grandes para separarlo del texto.
8.  La barra completa debe tener un margen superior para separarla de otros elementos.

**Código base (a completar):**

```html
<div class="[CLASES_BARRA_NOTIFICACION] [OTRAS_CLASES_GLOBALES]">
    <div class="[CLASES_CONTENEDOR_MENSAJE_BOTON]">
        <p class="[CLASES_TEXTO_MENSAJE]">¡Atención! Oferta especial por tiempo limitado.</p>
        <button class="[CLASES_BOTON_CERRAR]">X</button>
    </div>
</div>
```
**Pista:** Usa `d-flex` y sus variantes responsivas para el contenedor de mensaje y botón.



### Ejercicio 3: Bloque de Texto con Efectos Visuales

**Objetivo:** Crear un bloque de texto con sombra, opacidad y bordes personalizados.

**Requisitos:**
1.  Un `div` que contenga un párrafo de texto.
2.  El `div` debe tener un fondo azul (`bg-info`) y texto blanco.
3.  Debe tener un relleno de tamaño medio (`p-3`).
4.  Añade un borde de color secundario (`border-secondary`) y grosor `border-3`.
5.  Las esquinas deben ser muy redondeadas (`rounded-3`).
6.  Aplica una sombra grande (`shadow-lg`).
7.  Establece la opacidad al 75% (`opacity-75`).
8.  El párrafo de texto dentro debe ser de tamaño de fuente `fs-5` y tener la altura de línea `lh-lg`.

**Código base (a completar):**

```html
<div class="[CLASES_CONTENEDOR]">
    <p class="[CLASES_TEXTO]">
        Este es un bloque de contenido con varios estilos visuales aplicados usando clases utilitarias de Bootstrap.
        Observa cómo la combinación de clases puede crear un efecto distintivo y atractivo.
    </p>
</div>
```



### Ejercicio 4: Elemento Centrado y Adhesivo

**Objetivo:** Crear un elemento que se centre horizontalmente en la parte superior de la página y permanezca "pegado" al hacer scroll, con un tamaño específico.

**Requisitos:**
1.  Un `div` con el texto "Elemento Adhesivo".
2.  Debe tener un fondo oscuro (`bg-dark`) y texto blanco.
3.  Debe tener un relleno adecuado (`p-2`).
4.  El texto debe estar centrado.
5.  El elemento debe tener un ancho del 75% del contenedor en móvil y del 50% en pantallas medianas y grandes.
6.  Debe centrarse horizontalmente (`mx-auto` solo funciona en elementos de bloque con ancho definido, o puedes usar `d-flex justify-content-center` en el padre).
7.  El elemento debe comportarse como `sticky` en la parte superior de la ventana (`top-0`).
8.  Añade algo de contenido debajo para que puedas probar la funcionalidad `sticky` al hacer scroll.

**Código base (a completar):**

```html
<div class="[CLASES_ELEMENTO_ADHESIVO]">
    Elemento Adhesivo
</div>

<!-- Contenido para hacer scroll -->
<div style="height: 1000px;" class="bg-light p-5">
    <p>Desplázate hacia abajo para ver cómo el elemento se queda pegado.</p>
    <!-- Más contenido aquí para forzar el scroll -->
</div>
```
**Pista:** Para el centrado responsivo, puedes envolver el elemento con un `div` flex.



### Ejercicio 5: Galería de Avatares

**Objetivo:** Crear una fila de avatares de usuario con forma circular, espaciados uniformemente y responsivos.

**Requisitos:**
1.  Un contenedor `div` que use Flexbox para organizar los avatares.
2.  Cada avatar debe ser una imagen (puedes usar placeholders como `https://via.placeholder.com/60x60`) dentro de un `div`.
3.  Cada imagen de avatar debe ser circular (`rounded-circle`).
4.  Los avatares deben estar distribuidos uniformemente con espacio alrededor de ellos (`justify-content-around`).
5.  En pantallas muy pequeñas, los avatares deben estar centrados.
6.  Cada avatar debe tener un borde delgado de color blanco (`border border-white border-2`) para resaltarse sobre un fondo oscuro.
7.  El contenedor principal de los avatares debe tener un fondo oscuro (`bg-dark`) y un relleno vertical (`py-3`).

**Código base (a completar):**

```html
<div class="[CLASES_CONTENEDOR_AVATARES]">
    <div class="[CLASES_AVATAR]">
        <img src="https://via.placeholder.com/60x60/FF6347/FFFFFF?text=A1" alt="Avatar 1" class="[CLASES_IMAGEN_AVATAR]">
    </div>
    <div class="[CLASES_AVATAR]">
        <img src="https://via.placeholder.com/60x60/4682B4/FFFFFF?text=A2" alt="Avatar 2" class="[CLASES_IMAGEN_AVATAR]">
    </div>
    <div class="[CLASES_AVATAR]">
        <img src="https://via.placeholder.com/60x60/32CD32/FFFFFF?text=A3" alt="Avatar 3" class="[CLASES_IMAGEN_AVATAR]">
    </div>
    <div class="[CLASES_AVATAR]">
        <img src="https://via.placeholder.com/60x60/8A2BE2/FFFFFF?text=A4" alt="Avatar 4" class="[CLASES_IMAGEN_AVATAR]">
    </div>
</div>
```
