# Fetch vs Axios en React: Guía Comparativa

## Introducción

Tanto `fetch()` como `Axios` son herramientas populares para realizar peticiones HTTP en aplicaciones React. Cada una tiene sus ventajas y desventajas según el contexto de uso.

## ¿Qué es fetch()?

`fetch()` es una API nativa del navegador que proporciona una interfaz para realizar peticiones HTTP. Es parte del estándar web y no requiere instalación de dependencias externas.

## ¿Qué es Axios?

Axios es una librería externa basada en Promises para realizar peticiones HTTP. Ofrece una API más rica y funcionalidades adicionales comparado con fetch().

## Comparación Detallada

### 1. Instalación y Configuración

**Fetch:**

- No requiere instalación - es nativo del navegador
- Disponible directamente

**Axios:**
```bash
npm install axios
```

```javascript
import axios from 'axios';
```

### 2. Sintaxis Básica

**Fetch - GET Request:**
```javascript
import React, { useState, useEffect } from 'react';

function UserListFetch() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('https://jsonplaceholder.typicode.com/users');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Usuarios (Fetch)</h2>
      {users.map(user => (
        <div key={user.id}>{user.name} - {user.email}</div>
      ))}
    </div>
  );
}
```

**Axios - GET Request:**
```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserListAxios() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('https://jsonplaceholder.typicode.com/users');
        setUsers(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Usuarios (Axios)</h2>
      {users.map(user => (
        <div key={user.id}>{user.name} - {user.email}</div>
      ))}
    </div>
  );
}
```

### 3. POST Requests

**Fetch - POST:**
```javascript
import React, { useState } from 'react';

function CreateUserFetch() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('https://jsonplaceholder.typicode.com/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const newUser = await response.json();
      console.log('Usuario creado:', newUser);
      
      // Limpiar formulario
      setName('');
      setEmail('');
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Crear Usuario (Fetch)</h2>
      <input
        type="text"
        placeholder="Nombre"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Creando...' : 'Crear Usuario'}
      </button>
    </form>
  );
}
```

**Axios - POST:**
```javascript
import React, { useState } from 'react';
import axios from 'axios';

function CreateUserAxios() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post('https://jsonplaceholder.typicode.com/users', {
        name,
        email
      });

      console.log('Usuario creado:', response.data);
      
      // Limpiar formulario
      setName('');
      setEmail('');
    } catch (error) {
      console.error('Error:', error.response?.data || error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Crear Usuario (Axios)</h2>
      <input
        type="text"
        placeholder="Nombre"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Creando...' : 'Crear Usuario'}
      </button>
    </form>
  );
}
```

### 4. Manejo de Errores Avanzado

**Fetch - Manejo de Errores:**
```javascript
import React, { useState } from 'react';

function ErrorHandlingFetch() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');
      
      // fetch no rechaza automáticamente para códigos de estado HTTP como 404 o 500
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Recurso no encontrado');
        } else if (response.status === 500) {
          throw new Error('Error interno del servidor');
        } else {
          throw new Error(`Error HTTP: ${response.status}`);
        }
      }

      const result = await response.json();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err.message);
      setData(null);
    }
  };

  return (
    <div>
      <h2>Manejo de Errores - Fetch</h2>
      <button onClick={fetchData}>Obtener Datos</button>
      {error && <div style={{color: 'red'}}>Error: {error}</div>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}
```

**Axios - Manejo de Errores:**
```javascript
import React, { useState } from 'react';
import axios from 'axios';

function ErrorHandlingAxios() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const response = await axios.get('https://jsonplaceholder.typicode.com/posts/1');
      setData(response.data);
      setError(null);
    } catch (err) {
      if (err.response) {
        // El servidor respondió con un código de estado fuera del rango 2xx
        setError(`Error ${err.response.status}: ${err.response.data.message || 'Error del servidor'}`);
      } else if (err.request) {
        // La petición fue hecha pero no se recibió respuesta
        setError('No se pudo conectar con el servidor');
      } else {
        // Algo pasó al configurar la petición
        setError(err.message);
      }
      setData(null);
    }
  };

  return (
    <div>
      <h2>Manejo de Errores - Axios</h2>
      <button onClick={fetchData}>Obtener Datos</button>
      {error && <div style={{color: 'red'}}>Error: {error}</div>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}
```

### 5. Interceptores y Configuración Global

**Axios - Interceptores:**
```javascript
import axios from 'axios';

// Crear una instancia personalizada de Axios
const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor de petición
apiClient.interceptors.request.use(
  (config) => {
    // Agregar token de autenticación si existe
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log('Enviando petición:', config);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de respuesta
apiClient.interceptors.response.use(
  (response) => {
    console.log('Respuesta recibida:', response);
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Redirigir a login si no está autorizado
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Componente usando la instancia personalizada
function InterceptorExample() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await apiClient.get('/users');
        setUsers(response.data);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      <h2>Usuarios con Interceptores</h2>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

**Fetch - Configuración Global (Custom Hook):**
```javascript
import { useState, useEffect } from 'react';

// Custom hook para fetch con configuración global
function useCustomFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Configuración por defecto
        const defaultOptions = {
          headers: {
            'Content-Type': 'application/json',
          },
          signal: controller.signal,
        };

        // Agregar token si existe
        const token = localStorage.getItem('authToken');
        if (token) {
          defaultOptions.headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, { ...defaultOptions, ...options });

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem('authToken');
            window.location.href = '/login';
            return;
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}

// Componente usando el custom hook
function CustomFetchExample() {
  const { data: users, loading, error } = useCustomFetch('https://jsonplaceholder.typicode.com/users');

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Usuarios con Custom Hook</h2>
      {users?.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

## Tabla Comparativa

| Característica | Fetch | Axios |
|---|---|---|
| **Tamaño** | 0 KB (nativo) | ~13 KB |
| **Compatibilidad** | Moderno (IE no soportado) | Amplia compatibilidad |
| **Sintaxis** | Más verbosa | Más concisa |
| **Manejo de JSON** | Manual (.json()) | Automático |
| **Manejo de Errores** | Manual para códigos HTTP | Automático para códigos HTTP |
| **Interceptores** | No nativo | Sí |
| **Timeout** | Manual (AbortController) | Configuración simple |
| **Request/Response Transform** | Manual | Automático |
| **Cancelación** | AbortController | CancelToken/AbortController |
| **Configuración Global** | Custom hooks/funciones | Instancias |

## Ventajas y Desventajas

### Fetch()

**Ventajas:**
- Nativo del navegador (sin dependencias)
- Ligero (0 KB adicionales)
- Moderno y basado en Promises
- Soporte para streaming
- Control granular sobre la petición

**Desventajas:**
- Sintaxis más verbosa
- Manejo manual de JSON
- No rechaza automáticamente errores HTTP
- Sin interceptores nativos
- Configuración de timeout más compleja

### Axios

**Ventajas:**
- Sintaxis más limpia y concisa
- Manejo automático de JSON
- Interceptores integrados
- Mejor manejo de errores
- Configuración global fácil
- Transformación automática de datos
- Amplia compatibilidad con navegadores

**Desventajas:**
- Dependencia externa (~13 KB)
- Menos control granular
- Puede ser excesivo para proyectos simples

## Recomendaciones de Uso

### Usa Fetch cuando:
- Quieras mantener el bundle pequeño
- Necesites control granular sobre las peticiones
- El proyecto es simple y no requiere funcionalidades avanzadas
- Quieras evitar dependencias externas

### Usa Axios cuando:
- Necesites interceptores y configuración global
- Quieras una sintaxis más limpia y concisa
- Requieras compatibilidad con navegadores antiguos
- El proyecto sea complejo con muchas peticiones HTTP
- Necesites transformación automática de datos

## Conclusión

Tanto fetch() como Axios son excelentes opciones para realizar peticiones HTTP en React. La elección depende de las necesidades específicas del proyecto. Para aplicaciones simples, fetch() puede ser suficiente, mientras que para aplicaciones complejas con muchas peticiones HTTP, Axios ofrece más funcionalidades y una mejor experiencia de desarrollo.