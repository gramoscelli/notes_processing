# Guía de Bootstrap con Ejemplos

## ¿Qué es Bootstrap?

Bootstrap es el toolkit de código abierto más popular del mundo para el desarrollo front-end, que incluye variables y mixins de Sass, un sistema de grillas responsivo, una extensa biblioteca de componentes preconstruidos y potentes plugins de JavaScript. Permite a los desarrolladores diseñar y personalizar rápidamente sitios web responsivos con enfoque mobile-first.



## Cómo Probar los Ejemplos

Antes de comenzar con la teoría, es importante que sepas cómo probar todos los ejemplos de código que aparecen en esta guía. Puedes usar editores de HTML en línea que te permiten ver los resultados inmediatamente.

### 🚀 Editores Recomendados (Gratuitos)

#### 1. **CodePen** (Más popular)
- **URL**: https://codepen.io/pen/
- **Ventajas**: Comunidad activa, muchos ejemplos, fácil de compartir
- **Cómo usar**: 
  1. Ve a CodePen y crea una nueva "Pen"
  2. En la pestaña HTML, pega el código HTML del ejemplo
  3. En la pestaña CSS, agrega estilos personalizados si es necesario
  4. En Settings > CSS, agrega Bootstrap desde CDN

#### 2. **JSFiddle**
- **URL**: https://jsfiddle.net/
- **Ventajas**: Interfaz simple, fácil de usar
- **Cómo usar**:
  1. Ve a JSFiddle
  2. En el panel HTML, pega tu código
  3. En External Resources, agrega Bootstrap CDN

#### 3. **CodeSandbox**
- **URL**: https://codesandbox.io/
- **Ventajas**: Entorno más completo, similar a VS Code
- **Ideal para**: Proyectos más complejos

#### 4. **Replit**
- **URL**: https://replit.com/
- **Ventajas**: Incluye terminal, múltiples archivos
- **Ideal para**: Desarrollo más avanzado

### 📋 Plantilla Base para Copiar y Pegar

Copia este código base en cualquiera de los editores y luego agrega los ejemplos dentro del `<body>`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bootstrap Ejemplo</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons (opcional) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    
    <!-- Estilos personalizados (opcional) -->
    <style>
        /* Aquí puedes agregar CSS personalizado */
        .demo-spacing {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container my-5">
        <h1 class="text-center mb-4">Probando Bootstrap</h1>
        
        <!-- 👇 AGREGA LOS EJEMPLOS AQUÍ 👇 -->
        
        <!-- Ejemplo de botón -->
        <button type="button" class="btn btn-primary">Mi primer botón Bootstrap</button>
        
        <!-- 👆 FIN DE LOS EJEMPLOS 👆 -->
    </div>

    <!-- Bootstrap JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 🎯 Guía Paso a Paso para CodePen

**Paso 1**: Ve a https://codepen.io/pen/

**Paso 2**: Configura Bootstrap
- Clic en el ⚙️ (Settings) en la sección CSS
- En "Add External Stylesheets/Pens", agrega:
  ```
  https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css
  ```
- Clic en "Save & Close"

**Paso 3**: Configura Bootstrap JavaScript
- Clic en el ⚙️ (Settings) en la sección JS
- En "Add External Scripts/Pens", agrega:
  ```
  https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js
  ```
- Clic en "Save & Close"

**Paso 4**: Agrega HTML básico
En la sección HTML, pega:
```html
<div class="container my-5">
  <h1 class="text-center mb-4">Probando Bootstrap</h1>
  
  <!-- Aquí van tus ejemplos -->
  <button type="button" class="btn btn-primary">¡Funciona!</button>
</div>
```

**Paso 5**: ¡Experimenta!
Ahora puedes copiar cualquier ejemplo de esta guía y verlo funcionar inmediatamente.

### 💡 Consejos para Probar Ejemplos

1. **Comienza simple**: Prueba primero un botón o una tarjeta básica
2. **Un ejemplo a la vez**: No agregues todo junto al principio
3. **Usa el inspector**: Clic derecho > "Inspeccionar elemento" para ver cómo funciona el CSS
4. **Modifica valores**: Cambia clases como `btn-primary` por `btn-success` para ver diferencias
5. **Guarda tus experimentos**: Crea una cuenta en el editor para guardar tus pruebas

### 🔧 Troubleshooting (Solución de Problemas)

**❌ "No veo los estilos de Bootstrap"**
- Verifica que agregaste correctamente el CDN de CSS
- Revisa que no haya errores en la consola del navegador

**❌ "Los componentes JavaScript no funcionan"**
- Asegúrate de incluir el CDN de Bootstrap JavaScript
- Verifica que los atributos `data-bs-*` estén correctos

**❌ "El sitio se ve raro en móvil"**
- Confirma que tienes la etiqueta viewport: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

### 📱 Vista Responsiva

Los editores online te permiten ver cómo se ve tu código en diferentes tamaños:
- **CodePen**: Usa el botón "Change View" para ver móvil/tablet/desktop
- **JSFiddle**: Redimensiona la ventana de resultado
- **CodeSandbox**: Incluye vista responsiva integrada

¡Ahora estás listo para experimentar con todos los ejemplos de esta guía!



## Personalización de Bootstrap

La **personalización** es el proceso de modificar Bootstrap para adaptarlo a las necesidades específicas de tu proyecto, cambiando colores, tipografías, espaciados y otros aspectos visuales para crear una identidad única.

### ¿Por qué personalizar Bootstrap?

**Problema**: Bootstrap por defecto se ve genérico y todos los sitios que lo usan tienen un aspecto similar.

**Solución**: La personalización te permite:
- ✅ Crear una identidad visual única para tu marca
- ✅ Adaptar colores corporativos
- ✅ Cambiar tipografías según tu estilo
- ✅ Ajustar espaciados y tamaños
- ✅ Eliminar componentes innecesarios para optimizar el tamaño

### Métodos de Personalización

#### 1. CSS Personalizado (Método Básico)
Escribes CSS adicional que sobrescribe los estilos de Bootstrap:

```css
/* Archivo: mi-estilo-personalizado.css */
/* Cargar DESPUÉS de Bootstrap */

/* Cambiar color del botón primario */
.btn-primary {
    background-color: #ff6b35; /* Naranja corporativo */
    border-color: #ff6b35;
    font-weight: 600;
}

.btn-primary:hover {
    background-color: #e55a2b; /* Naranja más oscuro al hacer hover */
    border-color: #e55a2b;
}

/* Personalizar navbar */
.navbar {
    background-color: #2c3e50 !important; /* Azul oscuro corporativo */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Cambiar tipografía principal */
body {
    font-family: 'Roboto', Arial, sans-serif;
}
```

**Ventajas**: Fácil de implementar, no requiere herramientas adicionales
**Desventajas**: Puede generar CSS duplicado, difícil de mantener en proyectos grandes

#### 2. Variables CSS (CSS Custom Properties) - Recomendado
Bootstrap 5 incluye variables CSS que puedes modificar fácilmente:

```css
/* Archivo: variables-personalizadas.css */
/* Cargar ANTES que Bootstrap */

:root {
    /* Colores principales */
    --bs-primary: #ff6b35;           /* Naranja corporativo */
    --bs-secondary: #2c3e50;         /* Azul oscuro */
    --bs-success: #27ae60;           /* Verde personalizado */
    --bs-danger: #e74c3c;            /* Rojo personalizado */
    --bs-warning: #f39c12;           /* Amarillo personalizado */
    --bs-info: #3498db;              /* Azul información */
    
    /* Tipografía */
    --bs-font-sans-serif: "Roboto", "Helvetica Neue", Arial, sans-serif;
    --bs-font-size-base: 1rem;
    --bs-line-height-base: 1.6;
    
    /* Espaciados */
    --bs-spacer: 1rem;
    
    /* Bordes */
    --bs-border-radius: 8px;
    --bs-border-radius-sm: 4px;
    --bs-border-radius-lg: 12px;
    
    /* Sombras */
    --bs-box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    --bs-box-shadow-sm: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --bs-box-shadow-lg: 0 1rem 3rem rgba(0, 0, 0, 0.175);
}
```

**Ejemplo de implementación**:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Sitio Personalizado</title>
    
    <!-- 1. Primero cargar las variables personalizadas -->
    <link rel="stylesheet" href="variables-personalizadas.css">
    
    <!-- 2. Luego cargar Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- 3. Finalmente CSS adicional si es necesario -->
    <link rel="stylesheet" href="estilos-adicionales.css">
</head>
<body>
    <button class="btn btn-primary">Botón con color personalizado</button>
    <div class="card">
        <div class="card-body">
            Tarjeta con esquinas redondeadas personalizadas
        </div>
    </div>
</body>
</html>
```

#### 3. Personalización con Sass (Método Avanzado)
Para proyectos complejos, usa Sass para compilar Bootstrap con tus variables:

```scss
// Archivo: mi-bootstrap-personalizado.scss

// 1. Definir variables personalizadas ANTES de importar Bootstrap
$primary: #ff6b35;                    // Naranja corporativo
$secondary: #2c3e50;                  // Azul oscuro
$success: #27ae60;                    // Verde personalizado
$font-family-base: "Roboto", sans-serif;
$font-size-base: 1rem;
$line-height-base: 1.6;
$border-radius: 8px;
$box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);

// 2. Importar solo las partes de Bootstrap que necesites
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

// Componentes específicos (opcional - para optimizar tamaño)
@import "bootstrap/scss/root";
@import "bootstrap/scss/reboot";
@import "bootstrap/scss/type";
@import "bootstrap/scss/grid";
@import "bootstrap/scss/buttons";
@import "bootstrap/scss/forms";
@import "bootstrap/scss/navbar";
@import "bootstrap/scss/card";
@import "bootstrap/scss/utilities";

// 3. Agregar estilos personalizados adicionales
.mi-clase-personalizada {
    background: linear-gradient(135deg, $primary, $secondary);
    color: white;
    padding: 2rem;
    border-radius: $border-radius;
}
```

### Ejemplo Práctico: Empresa "NaranjaWeb"

Supongamos que trabajas para "NaranjaWeb" con estos colores de marca:
- **Primario**: Naranja (#ff6b35)
- **Secundario**: Azul oscuro (#2c3e50)
- **Fuente**: Roboto

#### Antes de personalizar:
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <button class="btn btn-primary">Contactar</button>
</nav>
```
**Resultado**: Navbar y botón azul genérico de Bootstrap

#### Después de personalizar:
```css
:root {
    --bs-primary: #ff6b35;
    --bs-secondary: #2c3e50;
    --bs-font-sans-serif: "Roboto", sans-serif;
}
```
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <button class="btn btn-primary">Contactar</button>
</nav>
```
**Resultado**: Navbar y botón naranja que coinciden con la marca

### Consejos para una Buena Personalización

#### ✅ Mejores Prácticas:
1. **Planifica tu paleta de colores** antes de comenzar
2. **Usa variables CSS** para cambios simples
3. **Mantén la accesibilidad** (contraste adecuado)
4. **Prueba en diferentes dispositivos**
5. **Documenta tus personalizaciones**

#### ❌ Errores Comunes:
1. **No sobreescribir directamente** las clases de Bootstrap en producción
2. **Evitar** usar `!important` innecesariamente
3. **No ignorar** las mejores prácticas de accesibilidad
4. **No personalizar** todo - mantén la consistencia

### Herramientas para Personalización

1. **Bootstrap Customizer**: Herramienta web oficial para generar CSS personalizado
2. **Sass/SCSS**: Para personalizaciones avanzadas
3. **Bootstrap Studio**: Editor visual con personalización integrada
4. **Themestr.app**: Generador de temas Bootstrap online

La personalización transforma Bootstrap de un framework genérico en una herramienta que refleja perfectamente la identidad de tu proyecto o marca.



## Patrones Comunes

### Sección Hero
```html
<section class="bg-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center min-vh-100">
            <div class="col-lg-6">
                <h1 class="display-4">Título Hero</h1>
                <p class="lead">Descripción del hero</p>
                <a href="#" class="btn btn-light btn-lg">Llamada a la Acción</a>
            </div>
        </div>
    </div>
</section>
```

### Grilla de Tarjetas
```html
<div class="container">
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div class="col">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">Título de tarjeta</h5>
                    <p class="card-text">Contenido de la tarjeta</p>
                </div>
            </div>
        </div>
        <!-- Repetir para más tarjetas -->
    </div>
</div>
```

### Tabla Responsiva
```html
<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead class="table-dark">
            <tr>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Juan Pérez</td>
                <td>juan@ejemplo.com</td>
                <td>Administrador</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary">Editar</button>
                    <button class="btn btn-sm btn-outline-danger">Eliminar</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### Breadcrumb (Migas de Pan)
```html
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="#">Inicio</a></li>
        <li class="breadcrumb-item"><a href="#">Biblioteca</a></li>
        <li class="breadcrumb-item active" aria-current="page">Datos</li>
    </ol>
</nav>
```

### Paginación
```html
<nav aria-label="Navegación de páginas">
    <ul class="pagination justify-content-center">
        <li class="page-item disabled">
            <a class="page-link">Anterior</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item active" aria-current="page">
            <a class="page-link" href="#">2</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item">
            <a class="page-link" href="#">Siguiente</a>
        </li>
    </ul>
</nav>
```

### Acordeón
```html
<div class="accordion" id="accordionExample">
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne">
                Elemento de Acordeón #1
            </button>
        </h2>
        <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
            <div class="accordion-body">
                <strong>Este es el cuerpo del acordeón del primer elemento.</strong> Se muestra por defecto.
            </div>
        </div>
    </div>
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo">
                Elemento de Acordeón #2
            </button>
        </h2>
        <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
            <div class="accordion-body">
                <strong>Este es el cuerpo del acordeón del segundo elemento.</strong> Está oculto por defecto.
            </div>
        </div>
    </div>
</div>
```

### Carrusel
```html
<div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="0" class="active"></button>
        <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="1"></button>
        <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="2"></button>
    </div>
    <div class="carousel-inner">
        <div class="carousel-item active">
            <img src="https://via.placeholder.com/800x400" class="d-block w-100" alt="Slide 1">
            <div class="carousel-caption d-none d-md-block">
                <h5>Primera diapositiva</h5>
                <p>Descripción de la primera diapositiva.</p>
            </div>
        </div>
        <div class="carousel-item">
            <img src="https://via.placeholder.com/800x400" class="d-block w-100" alt="Slide 2">
            <div class="carousel-caption d-none d-md-block">
                <h5>Segunda diapositiva</h5>
                <p>Descripción de la segunda diapositiva.</p>
            </div>
        </div>
        <div class="carousel-item">
            <img src="https://via.placeholder.com/800x400" class="d-block w-100" alt="Slide 3">
            <div class="carousel-caption d-none d-md-block">
                <h5>Tercera diapositiva</h5>
                <p>Descripción de la tercera diapositiva.</p>
            </div>
        </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
        <span class="carousel-control-prev-icon"></span>
        <span class="visually-hidden">Anterior</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
        <span class="carousel-control-next-icon"></span>
        <span class="visually-hidden">Siguiente</span>
    </button>
</div>
```



## Componentes JavaScript

### Tooltips
```html
<!-- Activar tooltips en JavaScript -->
<script>
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
</script>

<!-- HTML para tooltips -->
<button type="button" class="btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="top" title="Tooltip en la parte superior">
    Tooltip en arriba
</button>
<button type="button" class="btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="right" title="Tooltip a la derecha">
    Tooltip a la derecha
</button>
<button type="button" class="btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Tooltip en la parte inferior">
    Tooltip abajo
</button>
<button type="button" class="btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="left" title="Tooltip a la izquierda">
    Tooltip a la izquierda
</button>
```

### Popovers
```html
<!-- Activar popovers en JavaScript -->
<script>
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})
</script>

<!-- HTML para popovers -->
<button type="button" class="btn btn-lg btn-danger" data-bs-toggle="popover" title="Título del Popover" data-bs-content="Y aquí hay contenido sorprendente. Es muy atractivo. ¿Verdad?">
    Clic para activar popover
</button>
```

### Offcanvas
```html
<!-- Botón que activa offcanvas -->
<button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample">
    Abrir offcanvas
</button>

<!-- Offcanvas -->
<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title">Offcanvas</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
    </div>
    <div class="offcanvas-body">
        <div>
            Algún texto como contenido de marcador de posición para el offcanvas.
        </div>
        <div class="dropdown mt-3">
            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                Botón dropdown
            </button>
            <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Acción</a></li>
                <li><a class="dropdown-item" href="#">Otra acción</a></li>
                <li><a class="dropdown-item" href="#">Algo más aquí</a></li>
            </ul>
        </div>
    </div>
</div>
```



## Utilidades Avanzadas

### Espaciado Responsivo
```html
<!-- Márgenes responsivos -->
<div class="m-2 m-md-3 m-lg-4">Margen responsivo</div>
<div class="mt-1 mt-sm-2 mt-md-3 mt-lg-4 mt-xl-5">Margen superior responsivo</div>

<!-- Relleno responsivo -->
<div class="p-2 p-md-4 p-lg-5">Relleno responsivo</div>
```

### Posicionamiento
```html
<div class="position-relative">
    <div class="position-absolute top-0 start-0">Esquina superior izquierda</div>
    <div class="position-absolute top-0 end-0">Esquina superior derecha</div>
    <div class="position-absolute bottom-0 start-0">Esquina inferior izquierda</div>
    <div class="position-absolute bottom-0 end-0">Esquina inferior derecha</div>
</div>

<!-- Posición sticky -->
<div class="position-sticky top-0">Elemento sticky</div>

<!-- Posición fixed -->
<div class="position-fixed bottom-0 end-0 p-3">
    <button class="btn btn-primary">Botón flotante</button>
</div>
```

### Sombras
```html
<div class="shadow-none p-3 mb-5 bg-light rounded">Sin sombra</div>
<div class="shadow-sm p-3 mb-5 bg-body rounded">Sombra pequeña</div>
<div class="shadow p-3 mb-5 bg-body rounded">Sombra regular</div>
<div class="shadow-lg p-3 mb-5 bg-body rounded">Sombra grande</div>
```

### Overflow
```html
<div class="overflow-auto" style="max-width: 260px; max-height: 100px;">
    Contenido muy largo que activará el scroll automático cuando sea necesario.
</div>

<div class="overflow-hidden" style="max-width: 260px; max-height: 100px;">
    Contenido que será cortado y oculto.
</div>

<div class="overflow-scroll" style="max-width: 260px; max-height: 100px;">
    Contenido con barras de scroll siempre visibles.
</div>
```



## Integración con JavaScript

### Eventos de Bootstrap
```javascript
// Event listeners para modales
document.getElementById('exampleModal').addEventListener('show.bs.modal', function (event) {
    console.log('Modal está a Historia y Evolución

- **2011**: Creado por Mark Otto y Jacob Thornton en Twitter
- **Bootstrap 2 (2012)**: Se agregó funcionalidad responsiva
- **Bootstrap 3 (2013)**: Enfoque mobile-first, diseño plano
- **Bootstrap 4 (2018)**: Grid con Flexbox, nuevos componentes
- **Bootstrap 5 (2021)**: Se eliminó la dependencia de jQuery, utilidades actualizadas



## Primeros Pasos

### Instalación por CDN
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo Bootstrap</title>
    <!-- CSS de Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Tu contenido aquí -->
    
    <!-- JS de Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Instalación por NPM
```bash
npm install bootstrap
```



## Sistema de Grillas de Bootstrap

Bootstrap utiliza un sistema de grillas de 12 columnas con contenedores, filas y columnas.

### Estructura Básica de la Grilla
```html
<div class="container">
    <div class="row">
        <div class="col-md-4">Columna 1</div>
        <div class="col-md-4">Columna 2</div>
        <div class="col-md-4">Columna 3</div>
    </div>
</div>
```

### Ejemplos de Grilla Responsiva
```html
<!-- Columnas de igual ancho -->
<div class="container">
    <div class="row">
        <div class="col">Columna 1</div>
        <div class="col">Columna 2</div>
        <div class="col">Columna 3</div>
    </div>
</div>

<!-- Columnas responsivas mixtas -->
<div class="container">
    <div class="row">
        <div class="col-12 col-md-6 col-lg-4">
            <!-- Ancho completo en móvil, mitad en tablet, tercio en escritorio -->
        </div>
        <div class="col-12 col-md-6 col-lg-8">
            <!-- Ancho completo en móvil, mitad en tablet, dos tercios en escritorio -->
        </div>
    </div>
</div>

<!-- Columnas con desplazamiento -->
<div class="container">
    <div class="row">
        <div class="col-md-4 offset-md-2">Contenido centrado</div>
    </div>
</div>
```

### Puntos de Ruptura
| Punto de Ruptura | Infijo de clase | Dimensiones |
||--|-|
| Extra pequeño | (ninguno) | <576px |
| Pequeño | sm | ≥576px |
| Mediano | md | ≥768px |
| Grande | lg | ≥992px |
| Extra grande | xl | ≥1200px |
| Extra extra grande | xxl | ≥1400px |



## Tipografía

### Encabezados
```html
<h1 class="display-1">Display 1</h1>
<h1 class="display-2">Display 2</h1>
<h1 class="display-3">Display 3</h1>
<h1 class="display-4">Display 4</h1>
<h1 class="display-5">Display 5</h1>
<h1 class="display-6">Display 6</h1>

<h1>Encabezado 1 <small class="text-muted">Texto secundario</small></h1>
<h2>Encabezado 2</h2>
<h3>Encabezado 3</h3>
```

### Utilidades de Texto
```html
<p class="text-start">Texto alineado a la izquierda.</p>
<p class="text-center">Texto alineado al centro.</p>
<p class="text-end">Texto alineado a la derecha.</p>

<p class="text-primary">Texto primario</p>
<p class="text-secondary">Texto secundario</p>
<p class="text-success">Texto de éxito</p>
<p class="text-danger">Texto de peligro</p>
<p class="text-warning">Texto de advertencia</p>
<p class="text-info">Texto informativo</p>

<p class="fw-bold">Texto en negrita</p>
<p class="fw-light">Texto ligero</p>
<p class="fst-italic">Texto en cursiva</p>
<p class="text-decoration-underline">Texto subrayado</p>
```



## Componentes

### Botones
```html
<!-- Botones básicos -->
<button type="button" class="btn btn-primary">Primario</button>
<button type="button" class="btn btn-secondary">Secundario</button>
<button type="button" class="btn btn-success">Éxito</button>
<button type="button" class="btn btn-danger">Peligro</button>
<button type="button" class="btn btn-warning">Advertencia</button>
<button type="button" class="btn btn-info">Información</button>
<button type="button" class="btn btn-light">Claro</button>
<button type="button" class="btn btn-dark">Oscuro</button>

<!-- Botones con contorno -->
<button type="button" class="btn btn-outline-primary">Primario</button>
<button type="button" class="btn btn-outline-secondary">Secundario</button>

<!-- Tamaños de botones -->
<button type="button" class="btn btn-primary btn-lg">Botón grande</button>
<button type="button" class="btn btn-primary">Botón normal</button>
<button type="button" class="btn btn-primary btn-sm">Botón pequeño</button>

<!-- Botón de bloque -->
<div class="d-grid">
    <button class="btn btn-primary" type="button">Botón de bloque</button>
</div>
```

### Tarjetas
```html
<div class="card" style="width: 18rem;">
    <img src="https://via.placeholder.com/300x200" class="card-img-top" alt="...">
    <div class="card-body">
        <h5 class="card-title">Título de la tarjeta</h5>
        <p class="card-text">Un texto de ejemplo rápido para construir sobre el título de la tarjeta.</p>
        <a href="#" class="btn btn-primary">Ir a algún lugar</a>
    </div>
</div>

<!-- Tarjeta con encabezado y pie -->
<div class="card">
    <div class="card-header">
        Destacado
    </div>
    <div class="card-body">
        <h5 class="card-title">Tratamiento especial del título</h5>
        <p class="card-text">Con texto de apoyo debajo.</p>
        <a href="#" class="btn btn-primary">Ir a algún lugar</a>
    </div>
    <div class="card-footer text-muted">
        Hace 2 días
    </div>
</div>

<!-- Grupo de tarjetas -->
<div class="card-group">
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Tarjeta 1</h5>
            <p class="card-text">Contenido de la tarjeta 1</p>
        </div>
    </div>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Tarjeta 2</h5>
            <p class="card-text">Contenido de la tarjeta 2</p>
        </div>
    </div>
</div>
```

### Navegación
```html
<!-- Navbar básica -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="#">Marca</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link active" href="#">Inicio</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Acerca</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        Servicios
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Diseño Web</a></li>
                        <li><a class="dropdown-item" href="#">Desarrollo</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="#">Consultoría</a></li>
                    </ul>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Contacto</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!-- Navegación con píldoras -->
<ul class="nav nav-pills">
    <li class="nav-item">
        <a class="nav-link active" href="#">Activo</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">Enlace</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">Otro enlace</a>
    </li>
</ul>
```

### Formularios
```html
<form>
    <!-- Controles básicos de formulario -->
    <div class="mb-3">
        <label for="email" class="form-label">Dirección de correo electrónico</label>
        <input type="email" class="form-control" id="email" placeholder="nombre@ejemplo.com">
    </div>
    
    <div class="mb-3">
        <label for="password" class="form-label">Contraseña</label>
        <input type="password" class="form-control" id="password">
    </div>
    
    <!-- Select -->
    <div class="mb-3">
        <label for="country" class="form-label">País</label>
        <select class="form-select" id="country">
            <option selected>Elegir...</option>
            <option value="1">Estados Unidos</option>
            <option value="2">Canadá</option>
            <option value="3">México</option>
        </select>
    </div>
    
    <!-- Textarea -->
    <div class="mb-3">
        <label for="message" class="form-label">Mensaje</label>
        <textarea class="form-control" id="message" rows="3"></textarea>
    </div>
    
    <!-- Checkboxes -->
    <div class="mb-3">
        <div class="form-check">
            <input class="form-check-input" type="checkbox" id="newsletter">
            <label class="form-check-label" for="newsletter">
                Suscribirse al boletín
            </label>
        </div>
    </div>
    
    <!-- Botones de radio -->
    <div class="mb-3">
        <div class="form-check">
            <input class="form-check-input" type="radio" name="gender" id="male" value="male">
            <label class="form-check-label" for="male">Masculino</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="gender" id="female" value="female">
            <label class="form-check-label" for="female">Femenino</label>
        </div>
    </div>
    
    <!-- Grupo de entrada -->
    <div class="mb-3">
        <label for="username" class="form-label">Nombre de usuario</label>
        <div class="input-group">
            <span class="input-group-text">@</span>
            <input type="text" class="form-control" id="username" placeholder="Nombre de usuario">
        </div>
    </div>
    
    <button type="submit" class="btn btn-primary">Enviar</button>
</form>

<!-- Etiquetas flotantes -->
<div class="form-floating mb-3">
    <input type="email" class="form-control" id="floatingInput" placeholder="nombre@ejemplo.com">
    <label for="floatingInput">Dirección de correo electrónico</label>
</div>
```

### Alertas
```html
<div class="alert alert-primary" role="alert">
    ¡Una alerta primaria simple, échale un vistazo!
</div>
<div class="alert alert-secondary" role="alert">
    ¡Una alerta secundaria simple, échale un vistazo!
</div>
<div class="alert alert-success" role="alert">
    ¡Una alerta de éxito simple, échale un vistazo!
</div>
<div class="alert alert-danger" role="alert">
    ¡Una alerta de peligro simple, échale un vistazo!
</div>

<!-- Alerta desechable -->
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    <strong>¡Santo guacamole!</strong> Deberías revisar algunos de esos campos a continuación.
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>

<!-- Alerta con contenido adicional -->
<div class="alert alert-success" role="alert">
    <h4 class="alert-heading">¡Bien hecho!</h4>
    <p>Aww sí, leíste exitosamente este importante mensaje de alerta.</p>
    <hr>
    <p class="mb-0">Siempre que lo necesites, asegúrate de usar utilidades de margen.</p>
</div>
```

### Modal
```html
<!-- Botón que activa el modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
    Lanzar modal de demostración
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Título del modal</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>El texto del cuerpo del modal va aquí.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                <button type="button" class="btn btn-primary">Guardar cambios</button>
            </div>
        </div>
    </div>
</div>

<!-- Modal grande -->
<div class="modal fade" id="largeModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <!-- Contenido del modal -->
        </div>
    </div>
</div>
```



## Clases Utilitarias

### Espaciado
```html
<!-- Utilidades de margen -->
<div class="m-0">Margen 0</div>
<div class="m-1">Margen 1</div>
<div class="m-2">Margen 2</div>
<div class="m-3">Margen 3</div>
<div class="m-4">Margen 4</div>
<div class="m-5">Margen 5</div>

<!-- Lados específicos -->
<div class="mt-3">Margen superior 3</div>
<div class="mb-3">Margen inferior 3</div>
<div class="ms-3">Margen inicio (izquierda) 3</div>
<div class="me-3">Margen final (derecha) 3</div>
<div class="mx-3">Margen horizontal 3</div>
<div class="my-3">Margen vertical 3</div>

<!-- Utilidades de relleno -->
<div class="p-3">Relleno 3</div>
<div class="pt-3">Relleno superior 3</div>
<div class="pb-3">Relleno inferior 3</div>
```

### Visualización
```html
<div class="d-none">Elemento oculto</div>
<div class="d-block">Elemento de bloque</div>
<div class="d-inline">Elemento en línea</div>
<div class="d-inline-block">Elemento inline-block</div>
<div class="d-flex">Contenedor flex</div>

<!-- Visualización responsiva -->
<div class="d-none d-md-block">Oculto en pequeño, visible en mediano y mayor</div>
<div class="d-block d-md-none">Visible en pequeño, oculto en mediano y mayor</div>
```

### Flexbox
```html
<div class="d-flex justify-content-start">
    <div>Elemento flex 1</div>
    <div>Elemento flex 2</div>
</div>

<div class="d-flex justify-content-center">
    <div>Elementos centrados</div>
</div>

<div class="d-flex justify-content-between">
    <div>Elemento 1</div>
    <div>Elemento 2</div>
</div>

<div class="d-flex align-items-center" style="height: 100px;">
    <div>Centrado verticalmente</div>
</div>

<div class="d-flex flex-column">
    <div>Elemento 1</div>
    <div>Elemento 2</div>
</div>
```

### Colores
```html
<!-- Colores de texto -->
<p class="text-primary">Texto primario</p>
<p class="text-secondary">Texto secundario</p>
<p class="text-success">Texto de éxito</p>
<p class="text-danger">Texto de peligro</p>
<p class="text-warning">Texto de advertencia</p>
<p class="text-info">Texto informativo</p>
<p class="text-light bg-dark">Texto claro</p>
<p class="text-dark">Texto oscuro</p>
<p class="text-white bg-dark">Texto blanco</p>

<!-- Colores de fondo -->
<div class="bg-primary text-white p-3">Fondo primario</div>
<div class="bg-secondary text-white p-3">Fondo secundario</div>
<div class="bg-success text-white p-3">Fondo de éxito</div>
<div class="bg-light text-dark p-3">Fondo claro</div>
```



## Plantilla de Ejemplo Completa

Aquí tienes una plantilla HTML completa que muestra varios componentes de Bootstrap:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo Completo de Bootstrap</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>
    <!-- Navegación -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="bi bi-bootstrap"></i> Demo Bootstrap
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#inicio">Inicio</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#acerca">Acerca</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#servicios">Servicios</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#contacto">Contacto</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Sección Hero -->
    <section class="bg-light py-5" id="inicio">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <h1 class="display-4 fw-bold">Bienvenido a Bootstrap</h1>
                    <p class="lead">Construye sitios responsivos y rápidos con Bootstrap, el toolkit front-end de código abierto más popular del mundo.</p>
                    <button class="btn btn-primary btn-lg me-3">Comenzar</button>
                    <button class="btn btn-outline-secondary btn-lg">Aprender Más</button>
                </div>
                <div class="col-lg-6">
                    <img src="https://via.placeholder.com/500x300" class="img-fluid rounded" alt="Imagen Hero">
                </div>
            </div>
        </div>
    </section>

    <!-- Sección de Características -->
    <section class="py-5" id="acerca">
        <div class="container">
            <div class="row text-center mb-5">
                <div class="col">
                    <h2 class="display-5">¿Por qué elegir Bootstrap?</h2>
                    <p class="lead">Características poderosas que hacen el desarrollo más rápido y fácil</p>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-4 mb-4">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <i class="bi bi-phone display-1 text-primary mb-3"></i>
                            <h5 class="card-title">Responsivo</h5>
                            <p class="card-text">Diseño responsivo mobile-first que se adapta a cualquier tamaño de pantalla.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <i class="bi bi-puzzle display-1 text-success mb-3"></i>
                            <h5 class="card-title">Componentes</h5>
                            <p class="card-text">Extensa biblioteca de componentes preconstruidos listos para usar.</p>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-4">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body text-center">
                            <i class="bi bi-palette display-1 text-warning mb-3"></i>
                            <h5 class="card-title">Personalizable</h5>
                            <p class="card-text">Fácil de personalizar con variables Sass y clases utilitarias.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Formulario de Contacto -->
    <section class="bg-light py-5" id="contacto">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <h2 class="text-center mb-4">Ponte en Contacto</h2>
                    <form>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="firstName" class="form-label">Nombre</label>
                                <input type="text" class="form-control" id="firstName" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="lastName" class="form-label">Apellido</label>
                                <input type="text" class="form-control" id="lastName" required>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Correo Electrónico</label>
                            <input type="email" class="form-control" id="email" required>
                        </div>
                        <div class="mb-3">
                            <label for="subject" class="form-label">Asunto</label>
                            <select class="form-select" id="subject">
                                <option selected>Elegir...</option>
                                <option value="general">Consulta General</option>
                                <option value="support">Soporte</option>
                                <option value="business">Negocios</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="message" class="form-label">Mensaje</label>
                            <textarea class="form-control" id="message" rows="4" required></textarea>
                        </div>
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary btn-lg">Enviar Mensaje</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Pie de página -->
    <footer class="bg-dark text-white py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Demo Bootstrap</h5>
                    <p>Un ejemplo completo que muestra componentes y utilidades de Bootstrap.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <h5>Síguenos</h5>
                    <a href="#" class="text-white me-3"><i class="bi bi-facebook"></i></a>
                    <a href="#" class="text-white me-3"><i class="bi bi-twitter"></i></a>
                    <a href="#" class="text-white me-3"><i class="bi bi-instagram"></i></a>
                    <a href="#" class="text-white"><i class="bi bi-linkedin"></i></a>
                </div>
            </div>
            <hr class="my-3">
            <div class="text-center">
                <p class="mb-0">&copy; 2025 Demo Bootstrap. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```



## Iconos de Bootstrap

Bootstrap Icons es una biblioteca de iconos gratuita, de alta calidad y de código abierto con más de 1,800 iconos.

### Instalación
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
```

### Ejemplos de Uso
```html
<i class="bi bi-heart"></i>
<i class="bi bi-star-fill text-warning"></i>
<i class="bi bi-check-circle text-success"></i>
<i class="bi bi-exclamation-triangle text-danger"></i>

<!-- Con tamaños -->
<i class="bi bi-house fs-1"></i>
<i class="bi bi-house fs-3"></i>
<i class="bi bi-house"></i>
```



## Mejores Prácticas

### 1. Siempre Usa el Sistema de Grillas
```html
<!-- Bueno -->
<div class="container">
    <div class="row">
        <div class="col-md-6">Contenido</div>
    </div>
</div>

<!-- Evitar -->
<div style="width: 50%; float: left;">Contenido</div>
```

### 2. Usa Clases Utilitarias
```html
<!-- Bueno -->
<div class="text-center mb-4 p-3">Contenido centrado</div>

<!-- Evitar CSS personalizado cuando existen utilidades -->
<div style="text-align: center; margin-bottom: 1.5rem; padding: 1rem;">
```

### 3. Enfoque Mobile-First
```html
<!-- Bueno: Comienza con móvil, agrega puntos de ruptura más grandes -->
<div class="col-12 col-md-6 col-lg-4">

<!-- Evitar: No comiences con escritorio -->
<div class="col-lg-4 col-md-6 col-12">
```

### 4. Usa HTML Semántico
```html
<!-- Bueno -->
<nav class="navbar">
<main class="container">
<section class="py-5">

<!-- Evitar -->
<div class="navbar">
<div class="container">
```

