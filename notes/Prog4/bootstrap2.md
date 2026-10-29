# Guía Bootstrap - Parte 2: Clases Utilitarias

## ¿Qué son las Clases Utilitarias?

Las **clases utilitarias** de Bootstrap son clases CSS predefinidas que modifican propiedades específicas de los elementos HTML sin necesidad de escribir CSS personalizado. Cada clase tiene un propósito específico y se puede combinar con otras para lograr el diseño deseado.

**Ventaja principal**: Desarrollo más rápido y código más limpio.



## 🎨 Colores

### Colores de Texto
```html
<!-- Colores semánticos -->
<p class="text-primary">Texto azul primario</p>
<p class="text-secondary">Texto gris secundario</p>
<p class="text-success">Texto verde de éxito</p>
<p class="text-danger">Texto rojo de peligro</p>
<p class="text-warning">Texto amarillo de advertencia</p>
<p class="text-info">Texto azul claro informativo</p>
<p class="text-light">Texto gris claro (usar con fondo oscuro)</p>
<p class="text-dark">Texto gris oscuro</p>
<p class="text-body">Texto color del cuerpo por defecto</p>
<p class="text-muted">Texto gris silenciado</p>
<p class="text-white">Texto blanco (usar con fondo oscuro)</p>
<p class="text-black-50">Texto negro con 50% transparencia</p>
<p class="text-white-50">Texto blanco con 50% transparencia</p>
```

### Colores de Fondo
```html
<!-- Fondos semánticos -->
<div class="bg-primary text-white p-2">Fondo azul primario</div>
<div class="bg-secondary text-white p-2">Fondo gris secundario</div>
<div class="bg-success text-white p-2">Fondo verde de éxito</div>
<div class="bg-danger text-white p-2">Fondo rojo de peligro</div>
<div class="bg-warning text-dark p-2">Fondo amarillo de advertencia</div>
<div class="bg-info text-white p-2">Fondo azul claro informativo</div>
<div class="bg-light text-dark p-2">Fondo gris claro</div>
<div class="bg-dark text-white p-2">Fondo gris oscuro</div>
<div class="bg-body text-dark p-2">Fondo color del cuerpo</div>
<div class="bg-white text-dark p-2">Fondo blanco</div>
<div class="bg-transparent p-2">Fondo transparente</div>

<!-- Gradientes (requieren la clase .bg-gradient) -->
<div class="bg-primary bg-gradient text-white p-2">Fondo con gradiente</div>
```



## 📏 Espaciado

### Sistema de Espaciado
Bootstrap usa un sistema de espaciado basado en `rem` con valores de 0 a 5:
- `0` = 0px
- `1` = 0.25rem (4px por defecto)
- `2` = 0.5rem (8px por defecto)  
- `3` = 1rem (16px por defecto)
- `4` = 1.5rem (24px por defecto)
- `5` = 3rem (48px por defecto)

### Márgenes
```html
<!-- Margen en todos los lados -->
<div class="m-0">Sin margen</div>
<div class="m-1">Margen pequeño (4px)</div>
<div class="m-2">Margen medio-pequeño (8px)</div>
<div class="m-3">Margen medio (16px)</div>
<div class="m-4">Margen medio-grande (24px)</div>
<div class="m-5">Margen grande (48px)</div>
<div class="m-auto">Margen automático (centrar elementos)</div>

<!-- Márgenes específicos por lado -->
<div class="mt-3">Margen superior (margin-top)</div>
<div class="mb-3">Margen inferior (margin-bottom)</div>
<div class="ms-3">Margen inicio/izquierda (margin-start)</div>
<div class="me-3">Margen final/derecha (margin-end)</div>
<div class="mx-3">Margen horizontal (izquierda y derecha)</div>
<div class="my-3">Margen vertical (arriba y abajo)</div>

<!-- Márgenes negativos -->
<div class="mt-n1">Margen superior negativo</div>
<div class="mb-n2">Margen inferior negativo</div>
```

### Relleno (Padding)
```html
<!-- Relleno en todos los lados -->
<div class="p-0">Sin relleno</div>
<div class="p-1">Relleno pequeño (4px)</div>
<div class="p-2">Relleno medio-pequeño (8px)</div>
<div class="p-3">Relleno medio (16px)</div>
<div class="p-4">Relleno medio-grande (24px)</div>
<div class="p-5">Relleno grande (48px)</div>

<!-- Rellenos específicos por lado -->
<div class="pt-3">Relleno superior (padding-top)</div>
<div class="pb-3">Relleno inferior (padding-bottom)</div>
<div class="ps-3">Relleno inicio/izquierda (padding-start)</div>
<div class="pe-3">Relleno final/derecha (padding-end)</div>
<div class="px-3">Relleno horizontal (izquierda y derecha)</div>
<div class="py-3">Relleno vertical (arriba y abajo)</div>
```

### Espaciado Responsivo
```html
<!-- Espaciado que cambia según el tamaño de pantalla -->
<div class="m-1 m-sm-2 m-md-3 m-lg-4 m-xl-5">
    Margen responsivo: 4px en móvil, 8px en SM, 16px en MD, 24px en LG, 48px en XL
</div>

<div class="p-2 p-md-4 p-lg-5">
    Relleno responsivo: 8px en móvil, 24px en MD, 48px en LG+
</div>
```



## 📱 Display (Visualización)

### Valores de Display
```html
<!-- Display básico -->
<div class="d-none">Elemento completamente oculto</div>
<div class="d-inline">Elemento en línea (como <span>)</div>
<div class="d-inline-block">Elemento inline-block</div>
<div class="d-block">Elemento de bloque (como <div> por defecto)</div>
<div class="d-grid">Contenedor grid</div>
<div class="d-table">Comportamiento como tabla</div>
<div class="d-table-row">Comportamiento como fila de tabla</div>
<div class="d-table-cell">Comportamiento como celda de tabla</div>
<div class="d-flex">Contenedor flexbox</div>
<div class="d-inline-flex">Contenedor flexbox en línea</div>
```

### Display Responsivo
```html
<!-- Ocultar/mostrar en diferentes tamaños -->
<div class="d-none d-md-block">
    Oculto en móvil y tablet, visible en desktop
</div>

<div class="d-block d-md-none">
    Visible en móvil y tablet, oculto en desktop
</div>

<div class="d-none d-sm-block d-lg-none">
    Solo visible en tablets (SM a LG)
</div>

<!-- Para impresión -->
<div class="d-print-none">No se muestra al imprimir</div>
<div class="d-none d-print-block">Solo se muestra al imprimir</div>
```



## 🔄 Flexbox

### Contenedor Flex
```html
<div class="d-flex">
    <!-- Elementos flex van aquí -->
    <div>Elemento 1</div>
    <div>Elemento 2</div>
    <div>Elemento 3</div>
</div>
```

### Dirección Flex
```html
<div class="d-flex flex-row">Dirección horizontal (por defecto)</div>
<div class="d-flex flex-row-reverse">Horizontal invertida</div>
<div class="d-flex flex-column">Dirección vertical</div>
<div class="d-flex flex-column-reverse">Vertical invertida</div>

<!-- Direcciones responsivas -->
<div class="d-flex flex-column flex-md-row">
    Vertical en móvil, horizontal en escritorio
</div>
```

### Justificación (Eje Principal)
```html
<div class="d-flex justify-content-start">Alineación al inicio</div>
<div class="d-flex justify-content-end">Alineación al final</div>
<div class="d-flex justify-content-center">Centrado</div>
<div class="d-flex justify-content-between">Espacio entre elementos</div>
<div class="d-flex justify-content-around">Espacio alrededor de elementos</div>
<div class="d-flex justify-content-evenly">Espacio uniforme</div>

<!-- Justificación responsiva -->
<div class="d-flex justify-content-start justify-content-md-center">
    Inicio en móvil, centro en desktop
</div>
```

### Alineación (Eje Secundario)
```html
<div class="d-flex align-items-start" style="height: 200px;">
    <div>Alineado arriba</div>
</div>

<div class="d-flex align-items-end" style="height: 200px;">
    <div>Alineado abajo</div>
</div>

<div class="d-flex align-items-center" style="height: 200px;">
    <div>Centrado verticalmente</div>
</div>

<div class="d-flex align-items-baseline">
    <div>Alineado por línea base</div>
</div>

<div class="d-flex align-items-stretch" style="height: 200px;">
    <div>Se estira para llenar la altura</div>
</div>
```

### Auto-alineación de Elementos
```html
<div class="d-flex" style="height: 200px;">
    <div class="align-self-start">Auto-alineado arriba</div>
    <div class="align-self-center">Auto-alineado al centro</div>
    <div class="align-self-end">Auto-alineado abajo</div>
</div>
```

### Flex Wrap
```html
<div class="d-flex flex-wrap">
    <!-- Los elementos se ajustan a nuevas líneas -->
</div>

<div class="d-flex flex-nowrap">
    <!-- Los elementos no se ajustan (por defecto) -->
</div>

<div class="d-flex flex-wrap-reverse">
    <!-- Se ajustan en orden inverso -->
</div>
```

### Crecimiento y Contracción
```html
<div class="d-flex">
    <div class="flex-fill">Llena el espacio disponible</div>
    <div class="flex-grow-1">Crece proporcionalmente</div>
    <div class="flex-shrink-1">Se contrae si es necesario</div>
    <div class="flex-grow-0">No crece</div>
    <div class="flex-shrink-0">No se contrae</div>
</div>
```



## 📐 Posicionamiento

### Position
```html
<div class="position-static">Posicionamiento estático (por defecto)</div>
<div class="position-relative">Posicionamiento relativo</div>
<div class="position-absolute">Posicionamiento absoluto</div>
<div class="position-fixed">Posicionamiento fijo</div>
<div class="position-sticky">Posicionamiento pegajoso</div>
```

### Posiciones Específicas
```html
<div class="position-relative">
    <div class="position-absolute top-0 start-0">Esquina superior izquierda</div>
    <div class="position-absolute top-0 end-0">Esquina superior derecha</div>
    <div class="position-absolute top-50 start-50 translate-middle">Centro absoluto</div>
    <div class="position-absolute bottom-0 start-0">Esquina inferior izquierda</div>
    <div class="position-absolute bottom-0 end-0">Esquina inferior derecha</div>
</div>

<!-- Valores porcentuales -->
<div class="position-absolute top-0">Pegado arriba</div>
<div class="position-absolute top-50">50% desde arriba</div>
<div class="position-absolute start-0">Pegado a la izquierda</div>
<div class="position-absolute start-50">50% desde la izquierda</div>
```

### Transformaciones para Centrado
```html
<div class="position-relative" style="height: 200px;">
    <div class="position-absolute top-50 start-50 translate-middle">
        Centrado perfectamente
    </div>
    
    <div class="position-absolute top-0 start-50 translate-middle-x">
        Centrado horizontalmente, pegado arriba
    </div>
    
    <div class="position-absolute top-50 start-0 translate-middle-y">
        Centrado verticalmente, pegado a la izquierda
    </div>
</div>
```



## 📝 Tipografía

### Tamaños de Fuente
```html
<p class="fs-1">Fuente tamaño 1 (más grande)</p>
<p class="fs-2">Fuente tamaño 2</p>
<p class="fs-3">Fuente tamaño 3</p>
<p class="fs-4">Fuente tamaño 4</p>
<p class="fs-5">Fuente tamaño 5</p>
<p class="fs-6">Fuente tamaño 6 (más pequeña)</p>
```

### Peso de Fuente
```html
<p class="fw-bold">Texto en negrita</p>
<p class="fw-bolder">Texto más negrita</p>
<p class="fw-semibold">Texto semi-negrita</p>
<p class="fw-medium">Texto peso medio</p>
<p class="fw-normal">Texto peso normal</p>
<p class="fw-light">Texto ligero</p>
<p class="fw-lighter">Texto más ligero</p>
```

### Estilo de Fuente
```html
<p class="fst-italic">Texto en cursiva</p>
<p class="fst-normal">Texto normal (sin cursiva)</p>
```

### Alineación de Texto
```html
<p class="text-start">Texto alineado al inicio (izquierda en LTR)</p>
<p class="text-center">Texto centrado</p>
<p class="text-end">Texto alineado al final (derecha en LTR)</p>

<!-- Alineación responsiva -->
<p class="text-start text-md-center text-lg-end">
    Izquierda en móvil, centro en tablet, derecha en desktop
</p>
```

### Transformación de Texto
```html
<p class="text-lowercase">TEXTO EN minúsculas</p>
<p class="text-uppercase">texto en MAYÚSCULAS</p>
<p class="text-capitalize">texto con Primera Letra Mayúscula</p>
```

### Decoración de Texto
```html
<p class="text-decoration-none">Texto sin decoración</p>
<p class="text-decoration-underline">Texto subrayado</p>
<p class="text-decoration-line-through">Texto tachado</p>
```

### Altura de Línea
```html
<p class="lh-1">Altura de línea 1</p>
<p class="lh-sm">Altura de línea pequeña</p>
<p class="lh-base">Altura de línea base</p>
<p class="lh-lg">Altura de línea grande</p>
```



## 📦 Bordes

### Bordes Básicos
```html
<div class="border p-3">Borde completo</div>
<div class="border-top p-3">Solo borde superior</div>
<div class="border-end p-3">Solo borde derecho</div>
<div class="border-bottom p-3">Solo borde inferior</div>
<div class="border-start p-3">Solo borde izquierdo</div>
<div class="border-0 p-3">Sin bordes</div>

<!-- Quitar bordes específicos -->
<div class="border border-top-0 p-3">Borde excepto arriba</div>
<div class="border border-end-0 p-3">Borde excepto derecha</div>
```

### Colores de Borde
```html
<div class="border border-primary p-3">Borde azul primario</div>
<div class="border border-secondary p-3">Borde gris secundario</div>
<div class="border border-success p-3">Borde verde</div>
<div class="border border-danger p-3">Borde rojo</div>
<div class="border border-warning p-3">Borde amarillo</div>
<div class="border border-info p-3">Borde azul claro</div>
<div class="border border-light p-3">Borde gris claro</div>
<div class="border border-dark p-3">Borde oscuro</div>
<div class="border border-white p-3">Borde blanco</div>
```

### Grosor de Borde
```html
<div class="border border-1 p-3">Borde grosor 1</div>
<div class="border border-2 p-3">Borde grosor 2</div>
<div class="border border-3 p-3">Borde grosor 3</div>
<div class="border border-4 p-3">Borde grosor 4</div>
<div class="border border-5 p-3">Borde grosor 5</div>
```

### Esquinas Redondeadas
```html
<div class="rounded p-3">Esquinas redondeadas normales</div>
<div class="rounded-0 p-3">Sin esquinas redondeadas</div>
<div class="rounded-1 p-3">Esquinas ligeramente redondeadas</div>
<div class="rounded-2 p-3">Esquinas medianamente redondeadas</div>
<div class="rounded-3 p-3">Esquinas muy redondeadas</div>
<div class="rounded-circle p-3">Círculo perfecto</div>
<div class="rounded-pill p-3">Forma de píldora</div>

<!-- Esquinas específicas -->
<div class="rounded-top p-3">Solo esquinas superiores</div>
<div class="rounded-end p-3">Solo esquinas derechas</div>
<div class="rounded-bottom p-3">Solo esquinas inferiores</div>
<div class="rounded-start p-3">Solo esquinas izquierdas</div>
```



## 🌊 Opacidad y Sombras

### Opacidad
```html
<div class="opacity-25 p-3">25% visible</div>
<div class="opacity-50 p-3">50% visible</div>
<div class="opacity-75 p-3">75% visible</div>
<div class="opacity-100 p-3">100% visible (por defecto)</div>
```

### Sombras
```html
<div class="shadow-none p-3">Sin sombra</div>
<div class="shadow-sm p-3">Sombra pequeña</div>
<div class="shadow p-3">Sombra normal</div>
<div class="shadow-lg p-3">Sombra grande</div>
```



## 📏 Dimensiones

### Anchura
```html
<div class="w-25 p-3">Ancho 25%</div>
<div class="w-50 p-3">Ancho 50%</div>
<div class="w-75 p-3">Ancho 75%</div>
<div class="w-100 p-3">Ancho 100%</div>
<div class="w-auto p-3">Ancho automático</div>

<!-- Ancho máximo -->
<div class="mw-100 p-3">Ancho máximo 100%</div>
```

### Altura
```html
<div style="height: 200px;">
    <div class="h-25 bg-primary">Altura 25%</div>
    <div class="h-50 bg-secondary">Altura 50%</div>
    <div class="h-75 bg-success">Altura 75%</div>
    <div class="h-100 bg-danger">Altura 100%</div>
    <div class="h-auto bg-warning">Altura automática</div>
</div>

<!-- Altura máxima -->
<div class="mh-100">Altura máxima 100%</div>

<!-- Altura de viewport -->
<div class="vh-100">Altura 100% del viewport</div>
<div class="min-vh-100">Altura mínima 100% del viewport</div>
```



## 🔄 Overflow

### Control de Desbordamiento
```html
<div class="overflow-auto" style="width: 200px; height: 100px;">
    Contenido muy largo que activará scroll automático cuando sea necesario para evitar el desbordamiento del contenedor.
</div>

<div class="overflow-hidden" style="width: 200px; height: 100px;">
    Contenido que será cortado y oculto si excede las dimensiones del contenedor.
</div>

<div class="overflow-visible" style="width: 200px; height: 100px;">
    Contenido que será visible incluso si excede las dimensiones del contenedor.
</div>

<div class="overflow-scroll" style="width: 200px; height: 100px;">
    Contenido con barras de scroll siempre visibles, sin importar si es necesario o no.
</div>
```

### Overflow por Eje
```html
<div class="overflow-x-auto overflow-y-hidden" style="width: 200px; height: 100px;">
    Scroll horizontal, sin scroll vertical
</div>

<div class="overflow-x-hidden overflow-y-scroll" style="width: 200px; height: 100px;">
    Sin scroll horizontal, scroll vertical siempre visible
</div>
```



## 🎯 Interacciones del Usuario

### Selección de Texto
```html
<p class="user-select-all">Todo este texto se selecciona al hacer clic</p>
<p class="user-select-auto">Selección normal de texto (por defecto)</p>
<p class="user-select-none">Este texto no se puede seleccionar</p>
```

### Eventos de Puntero
```html
<p class="pe-none">Sin eventos de puntero (no clickeable)</p>
<p class="pe-auto">Con eventos de puntero (clickeable)</p>
```



## 📱 Utilidades Responsivas

### Patrones Comunes de Responsividad
```html
<!-- Espaciado responsivo -->
<div class="m-2 m-sm-3 m-md-4 m-lg-5">
    Margen que aumenta con el tamaño de pantalla
</div>

<!-- Texto responsivo -->
<h1 class="fs-6 fs-sm-5 fs-md-4 fs-lg-3 fs-xl-2 fs-xxl-1">
    Título que crece con el tamaño de pantalla
</h1>

<!-- Flexbox responsivo -->
<div class="d-flex flex-column flex-md-row">
    <div class="mb-3 mb-md-0 me-md-3">Elemento 1</div>
    <div>Elemento 2</div>
</div>

<!-- Visibilidad responsiva -->
<div class="d-block d-md-none">Solo visible en móvil</div>
<div class="d-none d-md-block d-xl-none">Solo visible en tablet</div>
<div class="d-none d-xl-block">Solo visible en desktop grande</div>
```



## 💡 Ejemplos Prácticos Combinando Utilidades

### Tarjeta Centrada y Responsiva
```html
<div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-lg" style="width: 100%; max-width: 400px;">
        <div class="card-body p-4">
            <h5 class="card-title text-center mb-4">Iniciar Sesión</h5>
            <form>
                <div class="mb-3">
                    <input type="email" class="form-control" placeholder="Email">
                </div>
                <div class="mb-3">
                    <input type="password" class="form-control" placeholder="Contraseña">
                </div>
                <button class="btn btn-primary w-100">Ingresar</button>
            </form>
        </div>
    </div>
</div>
```

### Lista Responsiva con Separadores
```html
<div class="container">
    <div class="row">
        <div class="col-12 col-md-8 col-lg-6 mx-auto">
            <div class="list-group shadow">
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1 fw-bold">Elemento 1</h6>
                        <p class="mb-1 text-muted">Descripción del elemento</p>
                    </div>
                    <span class="badge bg-primary rounded-pill">14</span>
                </div>
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1 fw-bold">Elemento 2</h6>
                        <p class="mb-1 text-muted">Otra descripción</p>
                    </div>
                    <span class="badge bg-success rounded-pill">7</span>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Botón Flotante
```html
<button class="btn btn-primary position-fixed bottom-0 end-0 m-4 rounded-circle shadow-lg" style="width: 60px; height: 60px;">
    <i class="bi bi-plus-lg"></i>
</button>
```

### Grid de Imágenes Responsivo
```html
<div class="container">
    <div class="row g-3">
        <div class="col-6 col-md-4 col-lg-3">
            <img src="imagen1.jpg" class="img-fluid rounded shadow-sm w-100">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="imagen2.jpg" class="img-fluid rounded shadow-sm w-100">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="imagen3.jpg" class="img-fluid rounded shadow-sm w-100">
        </div>
        <div class="col-6 col-md-4 col-lg-3">
            <img src="imagen4.jpg" class="img-fluid rounded shadow-sm w-100">
        </div>
    </div>
</div>
```



## 🔧 Consejos y Mejores Prácticas

### ✅ Buenas Prácticas
1. **Combina utilidades** en lugar de escribir CSS personalizado cuando sea posible
2. **Usa espaciado consistente** siguiendo el sistema de Bootstrap (0-5)
3. **Piensa mobile-first** al aplicar clases responsivas
4. **Mantén la legibilidad** - no abuse de demasiadas clases en un elemento
5. **Documenta combinaciones complejas** para futura referencia

### ⚠️ Errores Comunes
1. **No usar** `!important` innecesariamente
2. **No mezclar** sistemas de spacing (evita CSS personalizado mezclado con utilidades)
3. **No olvidar** la accesibilidad (contraste de colores, tamaños de fuente legibles)
4. **No sobrecargar** elementos con demasiadas clases utilitarias

### 🎨 Orden Recomendado de Clases
```html
<!-- Orden lógico: Display → Posición → Tamaño → Espaciado → Colores → Otros -->
<div class="d-flex position-relative w-100 h-auto p-3 m-2 bg-primary text-white rounded shadow">
    Contenido ordenado lógicamente
</div>
```



# Referencia Rápida de Prefijos Bootstrap

## Tabla Completa de Clases Utilitarias

| Prefijo | Propiedad CSS | Ejemplo |
|-|-|-|
| `m-` | margin | `m-3`, `mt-2`, `mx-auto` |
| `p-` | padding | `p-4`, `py-3`, `px-2` |
| `d-` | display | `d-flex`, `d-none`, `d-block` |
| `flex-` | flex properties | `flex-column`, `flex-wrap` |
| `justify-content-` | justify-content | `justify-content-center` |
| `align-items-` | align-items | `align-items-start` |
| `text-` | text properties | `text-center`, `text-primary` |
| `bg-` | background | `bg-primary`, `bg-light` |
| `border-` | border | `border-2`, `border-primary` |
| `rounded-` | border-radius | `rounded-3`, `rounded-circle` |
| `w-` | width | `w-100`, `w-50`, `w-auto` |
| `h-` | height | `h-100`, `h-25`, `vh-100` |
| `position-` | position | `position-relative`, `position-absolute` |
| `top-`, `bottom-`, `start-`, `end-` | positioning | `top-0`, `bottom-50`, `start-0` |
| `shadow-` | box-shadow | `shadow-sm`, `shadow-lg` |
| `opacity-` | opacity | `opacity-25`, `opacity-75` |
| `fs-` | font-size | `fs-1`, `fs-4` |
| `fw-` | font-weight | `fw-bold`, `fw-light` |
| `fst-` | font-style | `fst-italic`, `fst-normal` |
| `lh-` | line-height | `lh-1`, `lh-lg` |
| `overflow-` | overflow | `overflow-hidden`, `overflow-auto` |
| `user-select-` | user-select | `user-select-none`, `user-select-all` |
| `pe-` | pointer-events | `pe-none`, `pe-auto` |
| `translate-` | transform | `translate-middle`, `translate-middle-x` |

## Modificadores Responsivos

Todos los prefijos anteriores pueden combinarse con breakpoints:

| Breakpoint | Sufijo | Tamaño de Pantalla |
|--|--|--|
| Extra pequeño | (ninguno) | `<576px` |
| Pequeño | `-sm` | `≥576px` |
| Mediano | `-md` | `≥768px` |
| Grande | `-lg` | `≥992px` |
| Extra grande | `-xl` | `≥1200px` |
| Extra extra grande | `-xxl` | `≥1400px` |

### Ejemplos de uso responsivo:
- `d-none d-md-block` → Oculto en móvil, visible desde tablet
- `text-center text-lg-start` → Centrado en móvil, alineado izquierda en desktop
- `p-2 p-md-4 p-lg-5` → Padding crece con el tamaño de pantalla