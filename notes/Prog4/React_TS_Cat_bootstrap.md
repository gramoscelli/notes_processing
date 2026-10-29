# Pasos para agregar Bootstrap al proyecto

## 12. Agregar Bootstrap via CDN

**Speech:**
"Ahora vamos a darle estilo a nuestra aplicación usando Bootstrap. La forma más sencilla es agregar el CDN de Bootstrap en nuestro HTML."

**Archivo: `index.html`**
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Cats App</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## 13. Crear archivo de estilos personalizados

**Speech:**
"Creamos un archivo CSS para personalizar algunos estilos globales y darle un tema oscuro a nuestra aplicación."

**Archivo: `src/index.css`**
```css
body {
  margin: 0;
  min-height: 100vh;
  background-color: #242424;
  color: #f8f9fa;
  font-family: 'Inter', sans-serif;
}

#app {
  width: 100%;
}

.card {
  max-width: 600px;
  margin: 2rem auto;
  background-color: #343a40;
  color: #f8f9fa;
  border: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card-img-top {
  width: 100%;
  height: auto;
  object-fit: cover;
}
```

---

## 14. Importar los estilos en main.tsx

**Speech:**
"Importamos nuestro archivo de estilos personalizados en el punto de entrada."

**Archivo: `src/main.tsx`**
```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const rootElement = document.getElementById('app');

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
}
```

---

## 15. Aplicar clases de Bootstrap al componente - Estructura principal

**Speech:**
"Ahora aplicamos las clases de Bootstrap. Empezamos con el contenedor principal usando un container con flexbox para centrar todo."

**Archivo: `src/App.tsx` - Solo el return (parte 1)**
```tsx
  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card shadow-lg p-3 mb-5 bg-dark text-white rounded">
        <div className="card-body text-center">
          <h1 className="card-title mb-4">Curiosidades Gatunas</h1>
          
          {/* Aquí continuaremos con el resto */}
        </div>
      </div>
    </div>
  );
```

---

## 16. Estilizar el botón

**Speech:**
"Damos estilo al botón con clases de Bootstrap. Agregamos un spinner dentro del botón cuando está cargando."

**Archivo: `src/App.tsx` - Botón**
```tsx
          <button 
            onClick={handleNewFact} 
            disabled={loading} 
            className="btn btn-primary mb-4"
          >
            {loading ? (
              <>
                <span 
                  className="spinner-border spinner-border-sm me-2" 
                  role="status" 
                  aria-hidden="true"
                ></span>
                Cargando...
              </>
            ) : 'Nueva Curiosidad'}
          </button>
```

---

## 17. Estilizar el spinner de carga principal

**Speech:**
"Mejoramos el mensaje de carga general con un spinner de Bootstrap más vistoso."

**Archivo: `src/App.tsx` - Spinner**
```tsx
          {loading && (
            <div className="spinner-border text-info" role="status">
              <span className="visually-hidden">Cargando...</span>
            </div>
          )}
```

---

## 18. Estilizar los mensajes de error

**Speech:**
"Los mensajes de error los mostramos con la clase alert de Bootstrap para que resalten."

**Archivo: `src/App.tsx` - Error**
```tsx
          {error && (
            <p className="alert alert-danger mt-3">{error}</p>
          )}
```

---

## 19. Estilizar el texto del hecho

**Speech:**
"El hecho del gato lo mostramos con la clase lead de Bootstrap para darle más prominencia."

**Archivo: `src/App.tsx` - Hecho**
```tsx
          {!loading && fact && (
            <p className="lead mt-3">"{fact}"</p>
          )}
```

---

## 20. Estilizar la imagen

**Speech:**
"Finalmente, la imagen del gato con clases de Bootstrap para que se vea bien y responsiva."

**Archivo: `src/App.tsx` - Imagen**
```tsx
          {!loading && imageUrl && (
            <img 
              src={imageUrl} 
              className="card-img-top mt-3 rounded" 
              alt={`Gato con el texto: ${fact?.split(' ')[0]}`}
            />
          )}
```

---

## 21. Código completo con Bootstrap

**Speech:**
"Aquí está el código completo con todos los estilos de Bootstrap aplicados."

**Archivo: `src/App.tsx` (versión final con Bootstrap)**
```tsx
import { useState, useEffect } from 'react';

const CAT_FACT_API_URL = 'https://catfact.ninja/fact';
const CAT_IMAGE_PREFIX_URL = 'https://cataas.com';
const CAT_IMAGE_API_URL = `${CAT_IMAGE_PREFIX_URL}/cat/says`;

function App() {
  const [fact, setFact] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [refetchTrigger, setRefetchTrigger] = useState<number>(0);

  useEffect(() => {
    setLoading(true);
    setError(null);
    setFact(null);
    setImageUrl(null);

    const fetchCatFact = async () => {
      try {
        const res = await fetch(CAT_FACT_API_URL);
        if (!res.ok) {
          throw new Error('Error al obtener el hecho del gato');
        }
        const data = await res.json();
        setFact(data.fact);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      }
    };

    fetchCatFact();
  }, [refetchTrigger]);

  useEffect(() => {
    if (!fact) {
      setLoading(false);
      return;
    }

    const fetchCatImage = async () => {
      try {
        const firstWord = fact.split(' ')[0];
        const encodedWord = encodeURIComponent(firstWord);
        const apiUrl = `${CAT_IMAGE_API_URL}/${encodedWord}?json=true`;
        
        const res = await fetch(apiUrl);
        if (!res.ok) {
          throw new Error('Error al obtener la imagen');
        }
        const data = await res.json();
        setImageUrl(`${CAT_IMAGE_PREFIX_URL}${data.url}`);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        setLoading(false);
      }
    };

    fetchCatImage();
  }, [fact]);

  const handleNewFact = () => {
    setRefetchTrigger(prev => prev + 1);
  };

  return (
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
      <div className="card shadow-lg p-3 mb-5 bg-dark text-white rounded">
        <div className="card-body text-center">
          <h1 className="card-title mb-4">Curiosidades Gatunas</h1>
          
          <button 
            onClick={handleNewFact} 
            disabled={loading} 
            className="btn btn-primary mb-4"
          >
            {loading ? (
              <>
                <span 
                  className="spinner-border spinner-border-sm me-2" 
                  role="status" 
                  aria-hidden="true"
                ></span>
                Cargando...
              </>
            ) : 'Nueva Curiosidad'}
          </button>
          
          {loading && (
            <div className="spinner-border text-info" role="status">
              <span className="visually-hidden">Cargando...</span>
            </div>
          )}

          {error && (
            <p className="alert alert-danger mt-3">{error}</p>
          )}

          {!loading && fact && (
            <p className="lead mt-3">"{fact}"</p>
          )}

          {!loading && imageUrl && (
            <img 
              src={imageUrl} 
              className="card-img-top mt-3 rounded" 
              alt={`Gato con el texto: ${fact?.split(' ')[0]}`}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
```

---

## Resumen de clases Bootstrap utilizadas

**Speech final:**
"Hemos usado varias clases de Bootstrap:

**Layout y contenedor:**
- `container`: contenedor responsivo
- `d-flex`, `justify-content-center`, `align-items-center`: para centrar con flexbox
- `min-vh-100`: altura mínima del 100% del viewport

**Tarjeta (Card):**
- `card`: componente tarjeta de Bootstrap
- `shadow-lg`: sombra grande
- `bg-dark`, `text-white`: tema oscuro
- `rounded`: bordes redondeados
- `card-body`, `card-title`: partes de la tarjeta

**Botón:**
- `btn btn-primary`: botón con estilo primario
- `mb-4`: margen inferior

**Spinner:**
- `spinner-border`: spinner animado
- `spinner-border-sm`: versión pequeña
- `text-info`: color azul/info
- `visually-hidden`: oculta texto pero accesible

**Alertas y textos:**
- `alert alert-danger`: alerta de error
- `lead`: texto destacado
- `mt-3`: margen superior
- `me-2`: margen derecho

**Imagen:**
- `card-img-top`: imagen en la parte superior de la tarjeta

Y con esto tenemos una aplicación completamente funcional y con un diseño profesional gracias a Bootstrap."