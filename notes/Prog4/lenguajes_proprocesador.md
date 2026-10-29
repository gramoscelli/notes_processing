# Lenguajes Preprocesadores CSS

## ¿Qué son los preprocesadores CSS?

Los preprocesadores CSS son lenguajes que extienden las capacidades de CSS estándar, añadiendo funcionalidades como variables, anidamiento, mixins, funciones y más. Estos lenguajes se compilan a CSS puro que los navegadores pueden entender.

---

## Cómo Probar los Ejemplos Online

Antes de profundizar en la teoría, es importante que sepas cómo probar los ejemplos de preprocesadores CSS sin instalar nada en tu computadora. Existen editores online que soportan Sass, Less y Stylus.

### 🚀 Editores Online Recomendados

#### 1. **CodePen** (Más versátil - Recomendado)
- **URL**: https://codepen.io/pen/
- **Soporte**: Sass/SCSS, Less, Stylus
- **Ventajas**: Compilación automática, fácil de compartir, gran comunidad

**Cómo configurar Sass/SCSS en CodePen:**
1. Ve a CodePen y crea una nueva "Pen"
2. En la sección CSS, haz clic en el ⚙️ (Settings)
3. En "CSS Preprocessor", selecciona "SCSS" o "Sass"
4. Clic en "Save & Close"
5. ¡Ahora puedes escribir SCSS/Sass y se compilará automáticamente!

**Cómo configurar Less en CodePen:**
1. En CSS Settings, selecciona "Less"
2. Todo lo demás es igual

**Cómo configurar Stylus en CodePen:**
1. En CSS Settings, selecciona "Stylus"
2. Listo para usar

#### 2. **SassMeister** (Especializado en Sass)
- **URL**: https://www.sassmeister.com/
- **Soporte**: Solo Sass/SCSS
- **Ventajas**: Interface simple, comparación lado a lado del código compilado

#### 3. **Less2CSS** (Especializado en Less)
- **URL**: http://lesscss.org/less-preview/
- **Soporte**: Solo Less
- **Ventajas**: Compilador oficial de Less online

#### 4. **CodeSandbox**
- **URL**: https://codesandbox.io/
- **Soporte**: Sass/SCSS, Less, Stylus
- **Ventajas**: Entorno completo de desarrollo

### 📋 Plantillas Base para Cada Preprocesador

#### Plantilla HTML Base
Usa esta estructura HTML en cualquier editor para probar los ejemplos:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Probando Preprocesadores CSS</title>
    <!-- Los estilos se compilarán automáticamente -->
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="container">
            <ul>
                <li><a href="#home">Inicio</a></li>
                <li><a href="#about">Acerca</a></li>
                <li><a href="#services">Servicios</a></li>
                <li><a href="#contact">Contacto</a></li>
            </ul>
        </div>
    </nav>

    <!-- Header -->
    <header class="header">
        <div class="container">
            <h1>Probando Preprocesadores</h1>
            <p>Experimenta con Sass, Less y Stylus</p>
        </div>
    </header>

    <!-- Cards Section -->
    <section class="cards-section">
        <div class="container">
            <h2>Tarjetas de Ejemplo</h2>
            <div class="cards-grid">
                <div class="card">
                    <div class="card-header">
                        <h3>Tarjeta Normal</h3>
                    </div>
                    <div class="card-body">
                        <p>Esta es una tarjeta básica.</p>
                    </div>
                </div>

                <div class="card active">
                    <div class="card-header">
                        <h3>Tarjeta Activa</h3>
                    </div>
                    <div class="card-body">
                        <p>Esta tarjeta tiene la clase "active".</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Buttons Section -->
    <section class="buttons-section">
        <div class="container">
            <h2>Botones</h2>
            <button class="btn btn-primary">Primario</button>
            <button class="btn btn-secondary">Secundario</button>
            <button class="btn btn-success">Éxito</button>
        </div>
    </section>
</body>
</html>
```

#### CSS Base (Opcional)
Agrega este CSS base si quieres partir con algunos estilos básicos:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}
```

### 🎯 Guía Paso a Paso para CodePen

**Para SCSS/Sass:**
1. Ve a https://codepen.io/pen/
2. Pega el HTML base en la sección HTML
3. En CSS, clic en ⚙️ → CSS Preprocessor → "SCSS"
4. Pega cualquier ejemplo de SCSS de esta guía
5. ¡Ve el resultado compilado inmediatamente!

**Ejemplo rápido para probar:**
```scss
// Pega esto en CSS (con SCSS configurado)
$primary-color: #3498db;
$secondary-color: #e74c3c;

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  
  &.btn-primary {
    background: $primary-color;
    color: white;
    
    &:hover {
      background: darken($primary-color, 10%);
    }
  }
  
  &.btn-secondary {
    background: $secondary-color;
    color: white;
    
    &:hover {
      background: darken($secondary-color, 10%);
    }
  }
}
```

### 🎨 Comparación Visual de Compilación

Los editores online te permiten ver **lado a lado** cómo tu código preprocesador se convierte en CSS:

**Tu código SCSS:**
```scss
$primary: #3498db;

.button {
  background: $primary;
  
  &:hover {
    background: darken($primary, 10%);
  }
}
```

**CSS compilado automáticamente:**
```css
.button {
  background: #3498db;
}

.button:hover {
  background: #2980b9;
}
```

### 💡 Consejos para Experimentar

1. **Comienza con ejemplos simples**: Prueba primero variables y anidamiento
2. **Cambia valores**: Modifica colores y tamaños para ver el impacto
3. **Observa la compilación**: Mira cómo tu código se convierte en CSS
4. **Prueba diferentes preprocesadores**: Compara Sass vs Less vs Stylus
5. **Usa la consola**: Si algo no funciona, revisa la consola de errores

### 🔧 Troubleshooting

**❌ "Mi código no se compila"**
- Verifica que seleccionaste el preprocesador correcto
- Revisa la sintaxis (puntos y comas, llaves, etc.)
- Mira la consola de errores del editor

**❌ "No veo diferencias visuales"**
- Asegúrate de que el HTML incluye las clases que estás estilizando
- Verifica que el CSS compilado se está aplicando

**❌ "Error de sintaxis"**
- Cada preprocesador tiene reglas diferentes
- Sass: sin llaves ni puntos y comas
- SCSS: con llaves y puntos y comas
- Less: similar a CSS con extensiones

### 📚 Experimentos Sugeridos

**Experimento 1 - Variables:**
```scss
$color-primario: #e74c3c;    // Cambia este color
$color-secundario: #3498db;  // Y este también

.header {
  background: $color-primario;
  color: white;
}

.button {
  background: $color-secundario;
}
```

**Experimento 2 - Anidamiento:**
```scss
.navbar {
  background: #333;
  
  ul {
    list-style: none;
    
    li {
      display: inline-block;
      
      a {
        color: white;
        text-decoration: none;
        
        &:hover {
          color: #3498db;
        }
      }
    }
  }
}
```

**Experimento 3 - Mixins:**
```scss
@mixin button($bg-color) {
  padding: 10px 20px;
  background: $bg-color;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  
  &:hover {
    background: darken($bg-color, 10%);
  }
}

.btn-primary { @include button(#3498db); }
.btn-success { @include button(#27ae60); }
.btn-danger { @include button(#e74c3c); }
```

¡Ahora puedes experimentar con todos los ejemplos de preprocesadores sin instalar nada en tu computadora!

---

## 1. Sass (Syntactically Awesome Style Sheets)

### Historia
- **Creado en 2006** por Hampton Catlin
- **Desarrollado inicialmente en Ruby**
- Primer preprocesador CSS ampliamente adoptado
- Inspiró el desarrollo de otros preprocesadores

### Dos sintaxis:
- **Sass** (indentada, sin llaves ni puntos y comas)
- **SCSS** (similar a CSS, con llaves y puntos y comas)

### Herramientas de compilación:
- **Dart Sass** (implementación oficial actual)
- **Node Sass** (deprecated, basado en LibSass)
- **Ruby Sass** (implementación original, deprecated)
- **Vite, Webpack, Parcel** (bundlers con soporte integrado)

### Ejemplos:

#### Variables
```scss
// SCSS
$color-primary: #3498db;
$font-size-base: 16px;
$margin-default: 20px;

.header {
  color: $color-primary;
  font-size: $font-size-base;
  margin: $margin-default;
}
```

```sass
// Sass (indentada)
$color-primary: #3498db
$font-size-base: 16px
$margin-default: 20px

.header
  color: $color-primary
  font-size: $font-size-base
  margin: $margin-default
```

#### Anidamiento
```scss
.navbar {
  background: #333;
  
  ul {
    list-style: none;
    margin: 0;
    
    li {
      display: inline-block;
      
      a {
        text-decoration: none;
        color: white;
        
        &:hover {
          color: #3498db;
        }
      }
    }
  }
}
```

#### Mixins
```scss
@mixin button-style($bg-color, $text-color: white) {
  background-color: $bg-color;
  color: $text-color;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  
  &:hover {
    background-color: darken($bg-color, 10%);
  }
}

.btn-primary {
  @include button-style(#3498db);
}

.btn-danger {
  @include button-style(#e74c3c);
}
```

#### Funciones
```scss
@function calculate-rem($px) {
  @return #{$px / 16}rem;
}

.title {
  font-size: calculate-rem(24); // Resultado: 1.5rem
}
```

---

## 2. Less (Leaner Style Sheets)

### Historia
- **Creado en 2009** por Alexis Sellier
- **Desarrollado en JavaScript** (Node.js)
- Sintaxis muy similar a CSS
- Popular en proyectos como Bootstrap (versiones anteriores)

### Herramientas de compilación:
- **Less.js** (compilador oficial)
- **lessc** (herramienta de línea de comandos)
- **Webpack, Vite** (soporte a través de loaders)
- **Compilación en el navegador** (less.js en cliente)

### Ejemplos:

#### Variables
```less
@color-primary: #3498db;
@font-size-base: 16px;
@margin-default: 20px;

.header {
  color: @color-primary;
  font-size: @font-size-base;
  margin: @margin-default;
}
```

#### Anidamiento y operador &
```less
.card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  
  .card-header {
    background: #f8f9fa;
    padding: 15px;
    border-bottom: 1px solid #ddd;
    
    h3 {
      margin: 0;
      color: #333;
    }
  }
  
  .card-body {
    padding: 15px;
  }
  
  &.active {
    border-color: @color-primary;
  }
  
  &:hover {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
}
```

#### Mixins
```less
.border-radius(@radius: 4px) {
  border-radius: @radius;
  -webkit-border-radius: @radius;
  -moz-border-radius: @radius;
}

.button-variant(@bg-color; @text-color: white) {
  background-color: @bg-color;
  color: @text-color;
  border: 1px solid darken(@bg-color, 5%);
  
  &:hover {
    background-color: darken(@bg-color, 10%);
  }
}

.btn {
  .border-radius(4px);
  padding: 8px 16px;
  cursor: pointer;
  
  &.btn-primary {
    .button-variant(#3498db);
  }
  
  &.btn-success {
    .button-variant(#27ae60);
  }
}
```

#### Operaciones matemáticas
```less
@base-font-size: 14px;
@line-height-ratio: 1.5;

.text {
  font-size: @base-font-size;
  line-height: @base-font-size * @line-height-ratio;
  margin-bottom: @base-font-size / 2;
}

@container-width: 1200px;
.sidebar {
  width: @container-width / 4; // 300px
}
```

---

## 3. Stylus

### Historia
- **Creado en 2010** por TJ Holowaychuk
- **Desarrollado en JavaScript** (Node.js)
- Sintaxis muy flexible (llaves y puntos y comas opcionales)
- Influenciado por Sass y Python

### Herramientas de compilación:
- **Stylus CLI** (herramienta oficial de línea de comandos)
- **Webpack** (stylus-loader)
- **Vite** (soporte integrado)
- **Gulp, Grunt** (plugins disponibles)

### Ejemplos:

#### Variables y sintaxis flexible
```stylus
// Con sintaxis similar a CSS
color-primary = #3498db;
font-size-base = 16px;

.header {
  color: color-primary;
  font-size: font-size-base;
}

// Sintaxis sin llaves ni puntos y comas
color-secondary = #e74c3c
border-radius-default = 4px

.button
  background color-primary
  border-radius border-radius-default
  padding 10px 20px
  
  &:hover
    background darken(color-primary, 10%)
```

#### Funciones y mixins
```stylus
// Función
border-radius(radius = 4px)
  -webkit-border-radius radius
  -moz-border-radius radius
  border-radius radius

// Mixin más complejo
button-style(bg-color, text-color = white)
  background-color bg-color
  color text-color
  padding 10px 20px
  border none
  border-radius(4px)
  cursor pointer
  transition all 0.3s ease
  
  &:hover
    background-color darken(bg-color, 15%)
    transform translateY(-1px)

// Uso
.btn-primary
  button-style(#3498db)

.btn-secondary  
  button-style(#95a5a6, #333)
```

#### Interpolación y operadores
```stylus
vendors = webkit moz official

border-radius(radius)
  for vendor in vendors
    if vendor == official
      border-radius radius
    else
      -{vendor}-border-radius radius

// Operadores lógicos
responsive(size)
  if size == 'mobile'
    max-width 768px
  else if size == 'tablet'
    max-width 1024px
  else
    max-width 1200px

.container
  responsive('desktop')
  margin 0 auto
```

#### Bucles y condicionales avanzados
```stylus
// Generar clases utilitarias
sizes = 1 2 3 4 5

for size in sizes
  .m-{size}
    margin unit(size * 0.25, 'rem')
  
  .p-{size}
    padding unit(size * 0.25, 'rem')

// Resultado: .m-1, .m-2, etc. con margins de 0.25rem, 0.5rem, etc.

// Colores con bucle
colors = {
  primary: #3498db,
  success: #27ae60,
  warning: #f39c12,
  danger: #e74c3c
}

for name, color in colors
  .text-{name}
    color color
  
  .bg-{name}
    background-color color
    color white
```

---

## Comparación Rápida

| Característica | Sass/SCSS | Less | Stylus |
|---------------|-----------|------|--------|
| **Año de creación** | 2006 | 2009 | 2010 |
| **Lenguaje base** | Ruby→Dart | JavaScript | JavaScript |
| **Variables** | `$variable` | `@variable` | `variable = value` |
| **Anidamiento** | ✅ | ✅ | ✅ |
| **Mixins** | `@mixin/@include` | `.mixin()` | `mixin()` |
| **Sintaxis flexible** | Solo Sass | No | ✅ |
| **Funciones** | ✅ | Limitadas | ✅ Avanzadas |
| **Popularidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

## Instalación y Uso Básico

### Sass
```bash
# Instalación
npm install -g sass

# Compilación
sass input.scss output.css

# Modo watch
sass --watch input.scss:output.css
```

### Less
```bash
# Instalación
npm install -g less

# Compilación
lessc input.less output.css

# Con source map
lessc --source-map input.less output.css
```

### Stylus
```bash
# Instalación
npm install -g stylus

# Compilación
stylus input.styl

# Especificar output
stylus input.styl -o output.css
```

---

## Plantilla HTML para Probar los Ejemplos

Aquí tienes una plantilla HTML básica que puedes usar para probar todos los ejemplos de los preprocesadores:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplos Preprocesadores CSS</title>
    <!-- Enlaza aquí tu archivo CSS compilado -->
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="container">
            <ul>
                <li><a href="#home">Inicio</a></li>
                <li><a href="#about">Acerca</a></li>
                <li><a href="#services">Servicios</a></li>
                <li><a href="#contact">Contacto</a></li>
            </ul>
        </div>
    </nav>

    <!-- Header -->
    <header class="header">
        <div class="container">
            <h1>Ejemplos de Preprocesadores CSS</h1>
            <p>Plantilla para probar Sass, Less y Stylus</p>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container">
        <!-- Cards Section -->
        <section class="cards-section">
            <h2>Tarjetas de Ejemplo</h2>
            <div class="cards-grid">
                <div class="card">
                    <div class="card-header">
                        <h3>Tarjeta Normal</h3>
                    </div>
                    <div class="card-body">
                        <p>Esta es una tarjeta básica para demostrar los estilos.</p>
                    </div>
                </div>

                <div class="card active">
                    <div class="card-header">
                        <h3>Tarjeta Activa</h3>
                    </div>
                    <div class="card-body">
                        <p>Esta tarjeta tiene la clase "active" aplicada.</p>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3>Tarjeta con Hover</h3>
                    </div>
                    <div class="card-body">
                        <p>Pasa el mouse por encima para ver el efecto hover.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Buttons Section -->
        <section class="buttons-section">
            <h2>Botones de Ejemplo</h2>
            <div class="buttons-group">
                <button class="btn btn-primary">Botón Primario</button>
                <button class="btn btn-secondary">Botón Secundario</button>
                <button class="btn btn-success">Botón Éxito</button>
                <button class="btn btn-danger">Botón Peligro</button>
                <button class="btn btn-warning">Botón Advertencia</button>
            </div>
        </section>

        <!-- Typography Section -->
        <section class="typography-section">
            <h2>Tipografía</h2>
            <div class="text-examples">
                <h1 class="title">Título Principal</h1>
                <h2 class="subtitle">Subtítulo</h2>
                <p class="text">Texto normal con el tamaño base definido en las variables.</p>
                <p class="text text-primary">Texto con color primario</p>
                <p class="text text-success">Texto con color de éxito</p>
                <p class="text text-warning">Texto con color de advertencia</p>
                <p class="text text-danger">Texto con color de peligro</p>
            </div>
        </section>

        <!-- Utility Classes (para ejemplos de Stylus) -->
        <section class="utilities-section">
            <h2>Clases Utilitarias</h2>
            <div class="utility-examples">
                <div class="bg-primary p-3 m-2">Background primario con padding 3 y margin 2</div>
                <div class="bg-success p-4 m-3">Background éxito con padding 4 y margin 3</div>
                <div class="bg-warning p-5 m-4">Background advertencia con padding 5 y margin 4</div>
            </div>
        </section>

        <!-- Sidebar Layout Example -->
        <section class="layout-section">
            <h2>Ejemplo de Layout</h2>
            <div class="layout-container">
                <aside class="sidebar">
                    <h3>Barra Lateral</h3>
                    <ul>
                        <li><a href="#">Enlace 1</a></li>
                        <li><a href="#">Enlace 2</a></li>
                        <li><a href="#">Enlace 3</a></li>
                    </ul>
                </aside>
                <main class="main-content">
                    <h3>Contenido Principal</h3>
                    <p>Este es el área de contenido principal que demuestra el layout con sidebar.</p>
                </main>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Ejemplos de Preprocesadores CSS. Plantilla de demostración.</p>
        </div>
    </footer>
</body>
</html>
```

### Estructura de archivos recomendada:

```
proyecto/
├── index.html          (plantilla HTML)
├── src/
│   ├── styles.scss     (para Sass)
│   ├── styles.less     (para Less)
│   └── styles.styl     (para Stylus)
└── css/
    └── styles.css      (archivo compilado)
```

### CSS base adicional para la plantilla:

Si quieres agregar algunos estilos base que funcionen con cualquier preprocesador, puedes añadir esto al inicio de tus archivos:

#### Para SCSS:
```scss
// Reset básico y estilos base
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.buttons-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 20px 0;
}

.layout-container {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.footer {
  margin-top: 40px;
  padding: 20px 0;
  background: #f8f9fa;
  text-align: center;
}
```

---

## Recomendaciones

- **Para principiantes**: SCSS (sintaxis familiar)
- **Para proyectos grandes**: Sass/SCSS (mejor ecosistema)
- **Para sintaxis mínima**: Stylus
- **Para compatibilidad**: Less (si ya tienes experiencia)

Todos estos preprocesadores mejoran significativamente la experiencia de escribir CSS, añadiendo funcionalidades que CSS puro no tiene nativamente.