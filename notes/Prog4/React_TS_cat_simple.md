# Guión para desarrollar la App de Gatos (versión simplificada)

## Setup Inicial

**Speech:**
"Vamos a crear una aplicación que muestre hechos aleatorios sobre gatos y una imagen relacionada. Empezaremos desde cero con Vite y TypeScript, pero sin Bootstrap, lo más simple posible."

**Comandos:**
```bash
npm create vite@latest cats-app -- --template vanilla-ts
cd cats-app
npm install
npm install react react-dom
npm install -D @types/react @types/react-dom @vitejs/plugin-react
```

---

## 1. Configurar Vite para React

**Speech:**
"Primero necesitamos configurar Vite para que entienda React. Creamos el archivo de configuración."

**Archivo: `vite.config.ts`**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
```

---

## 2. Configurar TypeScript para JSX

**Speech:**
"Ahora configuramos TypeScript para que procese JSX. Modificamos el tsconfig."

**Archivo: `tsconfig.json` (modificar compilerOptions)**
```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    // ... resto de opciones que ya están
  }
}
```

---

## 3. Modificar el HTML

**Speech:**
"Modificamos el HTML para tener nuestro punto de montaje de React."

**Archivo: `index.html`**
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Cats App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## 4. Crear el punto de entrada de React

**Speech:**
"Renombramos main.ts a main.tsx y configuramos React."

**Renombrar:** `src/main.ts` → `src/main.tsx`

**Archivo: `src/main.tsx`**
```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

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

## 5. Crear componente App básico

**Speech:**
"Creamos nuestro componente principal. Por ahora solo un título."

**Archivo: `src/App.tsx`**
```tsx
function App() {
  return (
    <main>
      <h1>Curiosidades Gatunas</h1>
    </main>
  );
}

export default App;
```

**Probar:**
```bash
npm run dev
```

---

## 6. Agregar las constantes de las APIs

**Speech:**
"Definimos las URLs de las APIs que vamos a usar."

**Archivo: `src/App.tsx`**
```tsx
const CAT_FACT_API_URL = 'https://catfact.ninja/fact';
const CAT_IMAGE_PREFIX_URL = 'https://cataas.com';
const CAT_IMAGE_API_URL = `${CAT_IMAGE_PREFIX_URL}/cat/says`;

function App() {
  return (
    <main>
      <h1>Curiosidades Gatunas</h1>
    </main>
  );
}

export default App;
```

---

## 7. Declarar los estados

**Speech:**
"Ahora declaramos los estados que necesitamos: el hecho del gato, la URL de la imagen, un estado de carga y uno para errores."

**Archivo: `src/App.tsx`**
```tsx
import { useState } from 'react';

const CAT_FACT_API_URL = 'https://catfact.ninja/fact';
const CAT_IMAGE_PREFIX_URL = 'https://cataas.com';
const CAT_IMAGE_API_URL = `${CAT_IMAGE_PREFIX_URL}/cat/says`;

function App() {
  const [fact, setFact] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  return (
    <main>
      <h1>Curiosidades Gatunas</h1>
    </main>
  );
}

export default App;
```

---

## 8. Renderizar los estados en la UI

**Speech:**
"Mostramos condicionalmente los estados: carga, error, el hecho y la imagen."

**Archivo: `src/App.tsx`**
```tsx
import { useState } from 'react';

const CAT_FACT_API_URL = 'https://catfact.ninja/fact';
const CAT_IMAGE_PREFIX_URL = 'https://cataas.com';
const CAT_IMAGE_API_URL = `${CAT_IMAGE_PREFIX_URL}/cat/says`;

function App() {
  const [fact, setFact] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  return (
    <main>
      <h1>Curiosidades Gatunas</h1>
      
      {loading && <p>Cargando...</p>}
      
      {error && <p>Error: {error}</p>}
      
      {!loading && fact && <p>{fact}</p>}
      
      {!loading && imageUrl && (
        <img src={imageUrl} alt="Gato" />
      )}
    </main>
  );
}

export default App;
```

---

## 9. Primer useEffect: obtener el hecho

**Speech:**
"Creamos el primer useEffect que se ejecutará al montar el componente para obtener el hecho del gato."

**Archivo: `src/App.tsx`**
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

  useEffect(() => {
    setLoading(true);
    setError(null);

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
  }, []);

  return (
    <main>
      <h1>Curiosidades Gatunas</h1>
      
      {loading && <p>Cargando...</p>}
      
      {error && <p>Error: {error}</p>}
      
      {!loading && fact && <p>{fact}</p>}
      
      {!loading && imageUrl && (
        <img src={imageUrl} alt="Gato" />
      )}
    </main>
  );
}

export default App;
```

---

## 10. Segundo useEffect: obtener la imagen basada en el hecho

**Speech:**
"Ahora el punto clave: creamos un segundo useEffect que depende del fact. Cada vez que fact cambie, obtendremos una imagen con la primera palabra del hecho."

**Archivo: `src/App.tsx`**
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

  useEffect(() => {
    setLoading(true);
    setError(null);

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
  }, []);

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

  return (
    <main>
      <h1>Curiosidades Gatunas</h1>
      
      {loading && <p>Cargando...</p>}
      
      {error && <p>Error: {error}</p>}
      
      {!loading && fact && <p>{fact}</p>}
      
      {!loading && imageUrl && (
        <img src={imageUrl} alt="Gato" />
      )}
    </main>
  );
}

export default App;
```

---

## 11. Agregar botón para generar nuevo hecho

**Speech:**
"Finalmente, agregamos un botón para generar un nuevo hecho. Usamos un estado trigger que forzará la re-ejecución del primer useEffect."

**Archivo: `src/App.tsx` (versión final)**
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
    <main>
      <h1>Curiosidades Gatunas</h1>
      
      <button onClick={handleNewFact} disabled={loading}>
        {loading ? 'Cargando...' : 'Nueva Curiosidad'}
      </button>
      
      {loading && <p>Cargando...</p>}
      
      {error && <p>Error: {error}</p>}
      
      {!loading && fact && <p>{fact}</p>}
      
      {!loading && imageUrl && (
        <img src={imageUrl} alt="Gato" style={{ maxWidth: '400px' }} />
      )}
    </main>
  );
}

export default App;
```

---

## Resumen del flujo

**Speech final:**
"Y listo. Veamos qué tenemos:

1. Al montar el componente, el primer useEffect obtiene un hecho aleatorio
2. Cuando el fact cambia (pasa de null a tener valor), el segundo useEffect se activa
3. Este segundo useEffect toma la primera palabra del hecho y solicita una imagen
4. El botón incrementa refetchTrigger, lo que hace que el primer useEffect se ejecute de nuevo
5. Y el ciclo se repite: nuevo hecho → nueva imagen

La clave está en la interdependencia: un useEffect depende del array vacío (se ejecuta una vez), y el otro depende de fact (se ejecuta cuando fact cambia). Así logramos que la imagen esté sincronizada con el hecho."