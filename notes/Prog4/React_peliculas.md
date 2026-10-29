# Ejemplo 2: App de Películas con Búsqueda y Detalles

## Concepto del Ejemplo

**Speech:**
"Vamos a crear una aplicación donde buscaremos películas y al seleccionar una, mostraremos sus detalles. Este ejemplo demuestra cómo un estado (película seleccionada) depende de otro estado (búsqueda), y cómo un tercer estado (detalles) depende de la selección."

**APIs a usar:**
- Búsqueda: `https://www.omdbapi.com/?apikey=TU_API_KEY&s=QUERY`
- Detalles: `https://www.omdbapi.com/?apikey=TU_API_KEY&i=IMDB_ID`

**Nota:** Necesitarás obtener una API key gratuita en http://www.omdbapi.com/apikey.aspx

---

## Setup Inicial

**Speech:**
"Creamos un nuevo proyecto de la misma manera que el anterior."

**Comandos:**
```bash
npm create vite@latest movies-app -- --template vanilla-ts
cd movies-app
npm install
npm install react react-dom
npm install -D @types/react @types/react-dom @vitejs/plugin-react
```

---

## 1. Configurar Vite

**Archivo: `vite.config.ts`**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
```

---

## 2. Configurar TypeScript

**Archivo: `tsconfig.json` (modificar)**
```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    // ... resto de opciones
  }
}
```

---

## 3. Modificar HTML

**Archivo: `index.html`**
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Movies App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## 4. Crear main.tsx

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

## 5. Definir tipos TypeScript

**Speech:**
"Primero definimos los tipos para las películas que recibiremos de la API."

**Archivo: `src/App.tsx`**
```tsx
// Tipos para la respuesta de búsqueda
interface Movie {
  imdbID: string;
  Title: string;
  Year: string;
  Poster: string;
}

interface SearchResponse {
  Search: Movie[];
  totalResults: string;
  Response: string;
}

// Tipos para los detalles de una película
interface MovieDetails {
  Title: string;
  Year: string;
  Rated: string;
  Runtime: string;
  Genre: string;
  Director: string;
  Plot: string;
  Poster: string;
  imdbRating: string;
}

const API_KEY = 'TU_API_KEY'; // Reemplaza con tu API key
const API_URL = 'https://www.omdbapi.com/';

function App() {
  return (
    <main>
      <h1>Buscador de Películas</h1>
    </main>
  );
}

export default App;
```

---

## 6. Declarar los estados

**Speech:**
"Declaramos todos los estados que necesitamos: búsqueda, películas encontradas, película seleccionada, detalles, carga y error."

**Archivo: `src/App.tsx`**
```tsx
import { useState } from 'react';

// ... (tipos e interfaces)

const API_KEY = 'TU_API_KEY';
const API_URL = 'https://www.omdbapi.com/';

function App() {
  // Estado para la búsqueda del usuario
  const [searchQuery, setSearchQuery] = useState<string>('');
  
  // Estado para las películas encontradas
  const [movies, setMovies] = useState<Movie[]>([]);
  
  // Estado para la película seleccionada (solo ID)
  const [selectedMovieId, setSelectedMovieId] = useState<string | null>(null);
  
  // Estado para los detalles de la película seleccionada
  const [movieDetails, setMovieDetails] = useState<MovieDetails | null>(null);
  
  // Estados de UI
  const [loadingSearch, setLoadingSearch] = useState<boolean>(false);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <main>
      <h1>Buscador de Películas</h1>
    </main>
  );
}

export default App;
```

---

## 7. Crear el formulario de búsqueda

**Speech:**
"Creamos el formulario para buscar películas. Este actualiza el estado searchQuery."

**Archivo: `src/App.tsx`**
```tsx
// ... (imports, tipos, estados)

function App() {
  // ... (estados)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Por ahora solo mostramos en consola
      console.log('Buscando:', searchQuery);
    }
  };

  return (
    <main>
      <h1>Buscador de Películas</h1>
      
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar películas..."
        />
        <button type="submit" disabled={loadingSearch}>
          {loadingSearch ? 'Buscando...' : 'Buscar'}
        </button>
      </form>

      {error && <p>Error: {error}</p>}
    </main>
  );
}

export default App;
```

---

## 8. Primer useEffect: Buscar películas

**Speech:**
"Creamos un useEffect que se ejecuta cuando el usuario envía el formulario. Usamos un estado trigger para esto."

**Archivo: `src/App.tsx`**
```tsx
import { useState, useEffect } from 'react';

// ... (tipos)

const API_KEY = 'TU_API_KEY';
const API_URL = 'https://www.omdbapi.com/';

function App() {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [movies, setMovies] = useState<Movie[]>([]);
  const [selectedMovieId, setSelectedMovieId] = useState<string | null>(null);
  const [movieDetails, setMovieDetails] = useState<MovieDetails | null>(null);
  const [loadingSearch, setLoadingSearch] = useState<boolean>(false);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTrigger, setSearchTrigger] = useState<number>(0);

  // useEffect para buscar películas
  useEffect(() => {
    if (!searchQuery.trim()) return;

    setLoadingSearch(true);
    setError(null);
    setMovies([]);
    setSelectedMovieId(null);
    setMovieDetails(null);

    const fetchMovies = async () => {
      try {
        const url = `${API_URL}?apikey=${API_KEY}&s=${encodeURIComponent(searchQuery)}`;
        const res = await fetch(url);
        
        if (!res.ok) {
          throw new Error('Error en la búsqueda');
        }
        
        const data: SearchResponse = await res.json();
        
        if (data.Response === 'False') {
          throw new Error('No se encontraron películas');
        }
        
        setMovies(data.Search);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        setLoadingSearch(false);
      }
    };

    fetchMovies();
  }, [searchTrigger]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSearchTrigger(prev => prev + 1);
    }
  };

  return (
    <main>
      <h1>Buscador de Películas</h1>
      
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar películas..."
        />
        <button type="submit" disabled={loadingSearch}>
          {loadingSearch ? 'Buscando...' : 'Buscar'}
        </button>
      </form>

      {error && <p>Error: {error}</p>}
      
      {loadingSearch && <p>Cargando películas...</p>}
    </main>
  );
}

export default App;
```

---

## 9. Renderizar lista de películas

**Speech:**
"Mostramos las películas encontradas. Al hacer clic en una, actualizamos selectedMovieId."

**Archivo: `src/App.tsx`**
```tsx
// ... (todo lo anterior)

  return (
    <main>
      <h1>Buscador de Películas</h1>
      
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar películas..."
        />
        <button type="submit" disabled={loadingSearch}>
          {loadingSearch ? 'Buscando...' : 'Buscar'}
        </button>
      </form>

      {error && <p>Error: {error}</p>}
      
      {loadingSearch && <p>Cargando películas...</p>}

      {!loadingSearch && movies.length > 0 && (
        <div>
          <h2>Resultados:</h2>
          <ul>
            {movies.map(movie => (
              <li key={movie.imdbID}>
                <button onClick={() => setSelectedMovieId(movie.imdbID)}>
                  {movie.Title} ({movie.Year})
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
```

---

## 10. Segundo useEffect: Obtener detalles de película

**Speech:**
"Este es el punto clave: creamos un useEffect que depende de selectedMovieId. Cuando cambia, obtenemos los detalles de esa película."

**Archivo: `src/App.tsx`**
```tsx
import { useState, useEffect } from 'react';

// ... (tipos, constantes, estados anteriores)

function App() {
  // ... (estados)

  // useEffect para buscar películas (se mantiene igual)
  useEffect(() => {
    // ... (código anterior de búsqueda)
  }, [searchTrigger]);

  // useEffect para obtener detalles - DEPENDE de selectedMovieId
  useEffect(() => {
    if (!selectedMovieId) {
      setMovieDetails(null);
      return;
    }

    setLoadingDetails(true);
    setError(null);

    const fetchMovieDetails = async () => {
      try {
        const url = `${API_URL}?apikey=${API_KEY}&i=${selectedMovieId}`;
        const res = await fetch(url);
        
        if (!res.ok) {
          throw new Error('Error al obtener detalles');
        }
        
        const data: MovieDetails = await res.json();
        setMovieDetails(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        setLoadingDetails(false);
      }
    };

    fetchMovieDetails();
  }, [selectedMovieId]); // Dependencia clave

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSearchTrigger(prev => prev + 1);
    }
  };

  return (
    // ... (UI anterior)
  );
}

export default App;
```

---

## 11. Renderizar detalles de película

**Speech:**
"Finalmente mostramos los detalles de la película seleccionada."

**Archivo: `src/App.tsx` (return completo)**
```tsx
  return (
    <main>
      <h1>Buscador de Películas</h1>
      
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar películas..."
        />
        <button type="submit" disabled={loadingSearch}>
          {loadingSearch ? 'Buscando...' : 'Buscar'}
        </button>
      </form>

      {error && <p>Error: {error}</p>}
      
      {loadingSearch && <p>Cargando películas...</p>}

      {!loadingSearch && movies.length > 0 && (
        <div>
          <h2>Resultados:</h2>
          <ul>
            {movies.map(movie => (
              <li key={movie.imdbID}>
                <button onClick={() => setSelectedMovieId(movie.imdbID)}>
                  {movie.Title} ({movie.Year})
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {loadingDetails && <p>Cargando detalles...</p>}

      {!loadingDetails && movieDetails && (
        <div>
          <h2>Detalles de la Película</h2>
          <img 
            src={movieDetails.Poster !== 'N/A' ? movieDetails.Poster : ''} 
            alt={movieDetails.Title}
            style={{ maxWidth: '300px' }}
          />
          <h3>{movieDetails.Title}</h3>
          <p><strong>Año:</strong> {movieDetails.Year}</p>
          <p><strong>Clasificación:</strong> {movieDetails.Rated}</p>
          <p><strong>Duración:</strong> {movieDetails.Runtime}</p>
          <p><strong>Género:</strong> {movieDetails.Genre}</p>
          <p><strong>Director:</strong> {movieDetails.Director}</p>
          <p><strong>Rating IMDB:</strong> {movieDetails.imdbRating}</p>
          <p><strong>Sinopsis:</strong> {movieDetails.Plot}</p>
          <button onClick={() => setSelectedMovieId(null)}>
            Volver a resultados
          </button>
        </div>
      )}
    </main>
  );
```

---

## 12. Código completo sin estilos

**Speech:**
"Aquí está el código completo funcionando. Veamos cómo fluyen los estados."

**Archivo: `src/App.tsx` (versión completa)**
```tsx
import { useState, useEffect } from 'react';

interface Movie {
  imdbID: string;
  Title: string;
  Year: string;
  Poster: string;
}

interface SearchResponse {
  Search: Movie[];
  totalResults: string;
  Response: string;
}

interface MovieDetails {
  Title: string;
  Year: string;
  Rated: string;
  Runtime: string;
  Genre: string;
  Director: string;
  Plot: string;
  Poster: string;
  imdbRating: string;
}

const API_KEY = 'TU_API_KEY';
const API_URL = 'https://www.omdbapi.com/';

function App() {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [movies, setMovies] = useState<Movie[]>([]);
  const [selectedMovieId, setSelectedMovieId] = useState<string | null>(null);
  const [movieDetails, setMovieDetails] = useState<MovieDetails | null>(null);
  const [loadingSearch, setLoadingSearch] = useState<boolean>(false);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTrigger, setSearchTrigger] = useState<number>(0);

  useEffect(() => {
    if (!searchQuery.trim()) return;

    setLoadingSearch(true);
    setError(null);
    setMovies([]);
    setSelectedMovieId(null);
    setMovieDetails(null);

    const fetchMovies = async () => {
      try {
        const url = `${API_URL}?apikey=${API_KEY}&s=${encodeURIComponent(searchQuery)}`;
        const res = await fetch(url);
        
        if (!res.ok) {
          throw new Error('Error en la búsqueda');
        }
        
        const data: SearchResponse = await res.json();
        
        if (data.Response === 'False') {
          throw new Error('No se encontraron películas');
        }
        
        setMovies(data.Search);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        setLoadingSearch(false);
      }
    };

    fetchMovies();
  }, [searchTrigger]);

  useEffect(() => {
    if (!selectedMovieId) {
      setMovieDetails(null);
      return;
    }

    setLoadingDetails(true);
    setError(null);

    const fetchMovieDetails = async () => {
      try {
        const url = `${API_URL}?apikey=${API_KEY}&i=${selectedMovieId}`;
        const res = await fetch(url);
        
        if (!res.ok) {
          throw new Error('Error al obtener detalles');
        }
        
        const data: MovieDetails = await res.json();
        setMovieDetails(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        setLoadingDetails(false);
      }
    };

    fetchMovieDetails();
  }, [selectedMovieId]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSearchTrigger(prev => prev + 1);
    }
  };

  return (
    <main>
      <h1>Buscador de Películas</h1>
      
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar películas..."
        />
        <button type="submit" disabled={loadingSearch}>
          {loadingSearch ? 'Buscando...' : 'Buscar'}
        </button>
      </form>

      {error && <p>Error: {error}</p>}
      
      {loadingSearch && <p>Cargando películas...</p>}

      {!loadingSearch && movies.length > 0 && !selectedMovieId && (
        <div>
          <h2>Resultados:</h2>
          <ul>
            {movies.map(movie => (
              <li key={movie.imdbID}>
                <button onClick={() => setSelectedMovieId(movie.imdbID)}>
                  {movie.Title} ({movie.Year})
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {loadingDetails && <p>Cargando detalles...</p>}

      {!loadingDetails && movieDetails && (
        <div>
          <h2>Detalles de la Película</h2>
          {movieDetails.Poster !== 'N/A' && (
            <img 
              src={movieDetails.Poster} 
              alt={movieDetails.Title}
              style={{ maxWidth: '300px' }}
            />
          )}
          <h3>{movieDetails.Title}</h3>
          <p><strong>Año:</strong> {movieDetails.Year}</p>
          <p><strong>Clasificación:</strong> {movieDetails.Rated}</p>
          <p><strong>Duración:</strong> {movieDetails.Runtime}</p>
          <p><strong>Género:</strong> {movieDetails.Genre}</p>
          <p><strong>Director:</strong> {movieDetails.Director}</p>
          <p><strong>Rating IMDB:</strong> {movieDetails.imdbRating}</p>
          <p><strong>Sinopsis:</strong> {movieDetails.Plot}</p>
          <button onClick={() => setSelectedMovieId(null)}>
            Volver a resultados
          </button>
        </div>
      )}
    </main>
  );
}

export default App;
```

---

## Continuación: Agregar Bootstrap

**Speech:**
"Ahora vamos a agregar estilos con Bootstrap para mejorar la apariencia."

## 13. Agregar Bootstrap al HTML

**Archivo: `index.html`**
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Movies App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## 14. Crear estilos personalizados

**Archivo: `src/index.css`**
```css
body {
  margin: 0;
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #f8f9fa;
  font-family: 'Inter', sans-serif;
}

#app {
  width: 100%;
  padding: 2rem 0;
}

.movie-card {
  background-color: #2d2d2d;
  border: 1px solid #404040;
  transition: transform 0.2s, box-shadow 0.2s;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.movie-poster {
  height: 400px;
  object-fit: cover;
  width: 100%;
}

.details-card {
  background-color: #2d2d2d;
  border: 1px solid #404040;
}
```

---

## 15. Importar estilos en main.tsx

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

## 16. Aplicar Bootstrap - Contenedor principal

**Speech:**
"Empezamos aplicando clases de Bootstrap al contenedor principal y al título."

**Archivo: `src/App.tsx` - Estructura principal**
```tsx
  return (
    <div className="container">
      <div className="row">
        <div className="col-12">
          <h1 className="text-center my-4">🎬 Buscador de Películas</h1>
          
          {/* Aquí va el formulario */}
        </div>
      </div>
    </div>
  );
```

---

## 17. Estilizar el formulario de búsqueda

**Speech:**
"Aplicamos clases de Bootstrap al formulario para que se vea moderno."

**Archivo: `src/App.tsx` - Formulario**
```tsx
          <form onSubmit={handleSearch} className="mb-4">
            <div className="input-group input-group-lg">
              <input
                type="text"
                className="form-control"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Buscar películas..."
              />
              <button 
                className="btn btn-primary" 
                type="submit" 
                disabled={loadingSearch}
              >
                {loadingSearch ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    Buscando...
                  </>
                ) : '🔍 Buscar'}
              </button>
            </div>
          </form>
```

---

## 18. Estilizar mensajes de error y carga

**Speech:**
"Los mensajes de error y carga con clases de Bootstrap."

**Archivo: `src/App.tsx` - Error y Loading**
```tsx
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
          
          {loadingSearch && (
            <div className="text-center my-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Cargando...</span>
              </div>
            </div>
          )}
```

---

## 19. Estilizar lista de películas con cards

**Speech:**
"Mostramos las películas en un grid responsivo usando cards de Bootstrap."

**Archivo: `src/App.tsx` - Lista de películas**
```tsx
          {!loadingSearch && movies.length > 0 && !selectedMovieId && (
            <div>
              <h2 className="mb-3">Resultados de búsqueda:</h2>
              <div className="row g-4">
                {movies.map(movie => (
                  <div key={movie.imdbID} className="col-md-6 col-lg-4">
                    <div className="card movie-card h-100">
                      {movie.Poster !== 'N/A' && (
                        <img 
                          src={movie.Poster} 
                          className="card-img-top" 
                          alt={movie.Title}
                          style={{ height: '400px', objectFit: 'cover' }}
                        />
                      )}
                      <div className="card-body d-flex flex-column">
                        <h5 className="card-title">{movie.Title}</h5>
                        <p className="card-text text-muted">{movie.Year}</p>
                        <button 
                          className="btn btn-outline-primary mt-auto"
                          onClick={() => setSelectedMovieId(movie.imdbID)}
                        >
                          Ver detalles
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
```

---

## 20. Estilizar detalles de película

**Speech:**
"Finalmente, los detalles de la película con un diseño más elaborado."

**Archivo: `src/App.tsx` - Detalles**
```tsx
          {loadingDetails && (
            <div className="text-center my-5">
              <div className="spinner-border text-info" role="status">
                <span className="visually-hidden">Cargando detalles...</span>
              </div>
            </div>
          )}

          {!loadingDetails && movieDetails && (
            <div className="card details-card">
              <div className="row g-0">
                <div className="col-md-4">
                  {movieDetails.Poster !== 'N/A' && (
                    <img 
                      src={movieDetails.Poster} 
                      className="img-fluid rounded-start movie-poster" 
                      alt={movieDetails.Title}
                    />
                  )}
                </div>
                <div className="col-md-8">
                  <div className="card-body">
                    <h2 className="card-title mb-3">{movieDetails.Title}</h2>
                    
                    <div className="mb-3">
                      <span className="badge bg-primary me-2">{movieDetails.Year}</span>
                      <span className="badge bg-secondary me-2">{movieDetails.Rated}</span>
                      <span className="badge bg-info">{movieDetails.Runtime}</span>
                    </div>

                    <p className="card-text">
                      <strong>Género:</strong> {movieDetails.Genre}
                    </p>
                    <p className="card-text">
                      <strong>Director:</strong> {movieDetails.Director}
                    </p>
                    <p className="card-text">
                      <strong>Rating IMDB:</strong> 
                      <span className="badge bg-warning text-dark ms-2">
                        ⭐ {movieDetails.imdbRating}
                      </span>
                    </p>
                    <p className="card-text mt-3">
                      <strong>Sinopsis:</strong><br />
                      {movieDetails.Plot}
                    </p>

                    <button 
                      className="btn btn-outline-secondary mt-3"
                      onClick={() => setSelectedMovieId(null)}
                    >
                      ← Volver a resultados
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
```

---

## 21. Código completo con Bootstrap

**Speech:**
"Aquí está el código completo con todos los estilos de Bootstrap aplicados."

**Archivo: `src/App.tsx` (versión final completa con Bootstrap)**
```tsx
import { useState, useEffect } from 'react';

interface Movie {
  imdbID: string;
  Title: string;
  Year: string;
  Poster: string;
}

interface SearchResponse {
  Search: Movie[];
  totalResults: string;
  Response: string;
}

interface MovieDetails {
  Title: string;
  Year: string;
  Rated: string;
  Runtime: string;
  Genre: string;
  Director: string;
  Plot: string;
  Poster: string;
  imdbRating: string;
}

const API_KEY = 'TU_API_KEY';
const API_URL = 'https
```tsx
const API_URL = 'https://www.omdbapi.com/';

function App() {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [movies, setMovies] = useState<Movie[]>([]);
  const [selectedMovieId, setSelectedMovieId] = useState<string | null>(null);
  const [movieDetails, setMovieDetails] = useState<MovieDetails | null>(null);
  const [loadingSearch, setLoadingSearch] = useState<boolean>(false);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTrigger, setSearchTrigger] = useState<number>(0);

  useEffect(() => {
    if (!searchQuery.trim()) return;

    setLoadingSearch(true);
    setError(null);
    setMovies([]);
    setSelectedMovieId(null);
    setMovieDetails(null);

    const fetchMovies = async () => {
      try {
        const url = `${API_URL}?apikey=${API_KEY}&s=${encodeURIComponent(searchQuery)}`;
        const res = await fetch(url);
        
        if (!res.ok) {
          throw new Error('Error en la búsqueda');
        }
        
        const data: SearchResponse = await res.json();
        
        if (data.Response === 'False') {
          throw new Error('No se encontraron películas');
        }
        
        setMovies(data.Search);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        setLoadingSearch(false);
      }
    };

    fetchMovies();
  }, [searchTrigger]);

  useEffect(() => {
    if (!selectedMovieId) {
      setMovieDetails(null);
      return;
    }

    setLoadingDetails(true);
    setError(null);

    const fetchMovieDetails = async () => {
      try {
        const url = `${API_URL}?apikey=${API_KEY}&i=${selectedMovieId}`;
        const res = await fetch(url);
        
        if (!res.ok) {
          throw new Error('Error al obtener detalles');
        }
        
        const data: MovieDetails = await res.json();
        setMovieDetails(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error desconocido');
      } finally {
        setLoadingDetails(false);
      }
    };

    fetchMovieDetails();
  }, [selectedMovieId]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSearchTrigger(prev => prev + 1);
    }
  };

  return (
    <div className="container">
      <div className="row">
        <div className="col-12">
          <h1 className="text-center my-4">🎬 Buscador de Películas</h1>
          
          <form onSubmit={handleSearch} className="mb-4">
            <div className="input-group input-group-lg">
              <input
                type="text"
                className="form-control"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Buscar películas..."
              />
              <button 
                className="btn btn-primary" 
                type="submit" 
                disabled={loadingSearch}
              >
                {loadingSearch ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    Buscando...
                  </>
                ) : '🔍 Buscar'}
              </button>
            </div>
          </form>

          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
          
          {loadingSearch && (
            <div className="text-center my-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Cargando...</span>
              </div>
            </div>
          )}

          {!loadingSearch && movies.length > 0 && !selectedMovieId && (
            <div>
              <h2 className="mb-3">Resultados de búsqueda:</h2>
              <div className="row g-4">
                {movies.map(movie => (
                  <div key={movie.imdbID} className="col-md-6 col-lg-4">
                    <div className="card movie-card h-100">
                      {movie.Poster !== 'N/A' && (
                        <img 
                          src={movie.Poster} 
                          className="card-img-top" 
                          alt={movie.Title}
                          style={{ height: '400px', objectFit: 'cover' }}
                        />
                      )}
                      <div className="card-body d-flex flex-column">
                        <h5 className="card-title">{movie.Title}</h5>
                        <p className="card-text text-muted">{movie.Year}</p>
                        <button 
                          className="btn btn-outline-primary mt-auto"
                          onClick={() => setSelectedMovieId(movie.imdbID)}
                        >
                          Ver detalles
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {loadingDetails && (
            <div className="text-center my-5">
              <div className="spinner-border text-info" role="status">
                <span className="visually-hidden">Cargando detalles...</span>
              </div>
            </div>
          )}

          {!loadingDetails && movieDetails && (
            <div className="card details-card">
              <div className="row g-0">
                <div className="col-md-4">
                  {movieDetails.Poster !== 'N/A' && (
                    <img 
                      src={movieDetails.Poster} 
                      className="img-fluid rounded-start movie-poster" 
                      alt={movieDetails.Title}
                    />
                  )}
                </div>
                <div className="col-md-8">
                  <div className="card-body">
                    <h2 className="card-title mb-3">{movieDetails.Title}</h2>
                    
                    <div className="mb-3">
                      <span className="badge bg-primary me-2">{movieDetails.Year}</span>
                      <span className="badge bg-secondary me-2">{movieDetails.Rated}</span>
                      <span className="badge bg-info">{movieDetails.Runtime}</span>
                    </div>

                    <p className="card-text">
                      <strong>Género:</strong> {movieDetails.Genre}
                    </p>
                    <p className="card-text">
                      <strong>Director:</strong> {movieDetails.Director}
                    </p>
                    <p className="card-text">
                      <strong>Rating IMDB:</strong> 
                      <span className="badge bg-warning text-dark ms-2">
                        ⭐ {movieDetails.imdbRating}
                      </span>
                    </p>
                    <p className="card-text mt-3">
                      <strong>Sinopsis:</strong><br />
                      {movieDetails.Plot}
                    </p>

                    <button 
                      className="btn btn-outline-secondary mt-3"
                      onClick={() => setSelectedMovieId(null)}
                    >
                      ← Volver a resultados
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
```

---

## Resumen del flujo de estados interdependientes

**Speech final:**
"Perfecto. Ahora analicemos el flujo de estados en esta aplicación:

**Cadena de dependencias:**

1. **searchQuery → searchTrigger**: El usuario escribe y envía el formulario, esto incrementa searchTrigger

2. **searchTrigger → movies**: El primer useEffect se ejecuta cuando searchTrigger cambia, realizando la búsqueda y actualizando el array de movies

3. **movies → selectedMovieId**: El usuario hace clic en una película, actualizando selectedMovieId con el ID de esa película

4. **selectedMovieId → movieDetails**: El segundo useEffect detecta el cambio en selectedMovieId y obtiene los detalles completos de esa película

**Puntos clave de la interdependencia:**

- **Separación de responsabilidades**: Dos useEffect separados con dependencias distintas
- **Control de flujo**: El segundo useEffect tiene un guard clause `if (!selectedMovieId)` para evitar ejecuciones innecesarias
- **Estados de carga independientes**: `loadingSearch` y `loadingDetails` permiten mostrar feedback específico al usuario
- **Reseteo de estados**: Cuando se hace una nueva búsqueda, limpiamos selectedMovieId y movieDetails para evitar mostrar información obsoleta

**Clases de Bootstrap utilizadas:**

- `container`, `row`, `col-*`: Sistema de grid
- `card`, `card-body`, `card-title`, `card-text`: Componentes de tarjetas
- `input-group`, `form-control`: Formularios
- `btn`, `btn-primary`, `btn-outline-*`: Botones
- `badge`: Etiquetas informativas
- `spinner-border`: Indicadores de carga
- `alert`: Mensajes de error
- Utilidades: `mb-*`, `mt-*`, `me-*`, `text-center`, `g-*`

Este patrón de estados interdependientes es fundamental en React y se puede aplicar a muchos escenarios: filtros que afectan listas, categorías que determinan productos, ubicaciones que determinan el clima, etc."