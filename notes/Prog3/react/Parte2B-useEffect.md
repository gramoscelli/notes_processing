# Parte 2B: Efectos Secundarios (useEffect)
## ⚡ useEffect - Efectos Secundarios

### Conexión con el Módulo 1

Hasta ahora, todos nuestros componentes eran **puros**:
```jsx
// Módulo 1: Componente puro - solo recibe props y retorna JSX
function Welcome({ name }) {
  return <h1>Hola, {name}</h1>; // No hace nada más
}
```

Sin embargo, a veces necesitamos hacer **efectos secundarios**:
```jsx
// Módulo 2: Componente con efectos secundarios
function Welcome({ name }) {
  useEffect(() => {
    document.title = `Hola, ${name}`; // Modifica algo fuera del componente
  }, [name]);
  
  return <h1>Hola, {name}</h1>;
}
```

### ¿Qué son los Efectos Secundarios?

Los **efectos secundarios** son operaciones que **afectan algo fuera del componente**:

✅ **Ejemplos comunes de efectos secundarios:**

- 🌐 **Llamadas a APIs** (fetch, axios)
- 📄 **Modificar el DOM** directamente (document.title)
- ⏰ **Timers** (setTimeout, setInterval)
- 🔔 **Suscripciones** (WebSockets, eventos)
- 📊 **Logging** (console.log, analytics)
- 💾 **LocalStorage** (guardar/leer datos)

❌ **NO son efectos secundarios:**

- Calcular valores derivados
- Renderizar JSX
- Manejar eventos de usuario (onClick, onChange)

### Sintaxis Básica de useEffect

```jsx
import React, { useState, useEffect } from 'react';

function DocumentTitle() {
  const [count, setCount] = useState(0);
  
  // Efecto que se ejecuta después de cada render
  useEffect(() => {
    // Este código se ejecuta DESPUÉS de que el componente se renderiza
    document.title = `Clicks: ${count}`;
    console.log('📄 Título actualizado');
  });
  
  console.log('🎨 Renderizando componente'); // Se ejecuta ANTES que el efecto
  
  return (
    <div>
      <p>Has hecho clic {count} veces</p>
      <button onClick={() => setCount(count + 1)}>
        Hacer clic
      </button>
    </div>
  );
}
```

### Orden de Ejecución

Entender el **orden** es crucial:

```jsx
function ExecutionOrder() {
  const [count, setCount] = useState(0);
  
  console.log('1️⃣ Inicio del render');
  
  useEffect(() => {
    console.log('3️⃣ Efecto ejecutado');
  });
  
  console.log('2️⃣ Antes del return');
  
  return (
    <div>
      {console.log('2️⃣.5 Durante JSX')}
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}

// Orden de ejecución:
// 1️⃣ Inicio del render
// 2️⃣ Antes del return  
// 2️⃣.5 Durante JSX
// [Componente se renderiza en el DOM]
// 3️⃣ Efecto ejecutado
```

### Array de Dependencias - Concepto Clave

El **array de dependencias** controla **cuándo** se ejecuta tu efecto:

```jsx
function DependencyExamples() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  
  // 🔄 SIN array de dependencias - se ejecuta en CADA render
  useEffect(() => {
    console.log('🔄 En cada render - count:', count, 'name:', name);
  });
  
  // 🚀 Array VACÍO - se ejecuta SOLO UNA VEZ (al montar)
  useEffect(() => {
    console.log('🚀 Solo una vez al montar el componente');
    // Perfecto para: configuración inicial, suscripciones, APIs que no cambian
  }, []); // <- Array vacío es clave
  
  // 🎯 CON dependencias - se ejecuta solo cuando CAMBIAN las dependencias
  useEffect(() => {
    console.log('🎯 Solo cuando count cambia:', count);
  }, [count]); // <- Solo cuando count cambia
  
  // 🎯 MÚLTIPLES dependencias
  useEffect(() => {
    console.log('🎯 Cuando count O name cambian:', count, name);
  }, [count, name]); // <- Cuando cualquiera de estos cambie
  
  return (
    <div>
      <p>Count: {count}</p>
      <p>Name: {name}</p>
      <button onClick={() => setCount(count + 1)}>
        Incrementar Count
      </button>
      <input 
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Escribe tu nombre"
      />
    </div>
  );
}
```

### Tabla de Referencias Rápidas

| Array de Dependencias | Cuándo se ejecuta | Caso de uso típico |
|----------------------|-------------------|-------------------|
| Sin array | En cada render | Debugging, efectos que siempre deben ejecutarse |
| `[]` (vacío) | Solo una vez (mount) | APIs iniciales, suscripciones, configuración |
| `[count]` | Cuando `count` cambia | Reaccionar a cambios específicos |
| `[a, b, c]` | Cuando cualquiera cambia | Múltiples valores que afectan el efecto |

### Ejemplo Práctico: Título Dinámico

```jsx
function DynamicTitle() {
  const [pageTitle, setPageTitle] = useState('Mi App');
  const [count, setCount] = useState(0);
  
  // Actualizar título solo cuando pageTitle cambia
  useEffect(() => {
    document.title = pageTitle;
    console.log('📄 Título cambiado a:', pageTitle);
  }, [pageTitle]); // Solo cuando pageTitle cambie
  
  // Nota: count puede cambiar sin afectar el título
  
  return (
    <div>
      <input 
        value={pageTitle}
        onChange={(e) => setPageTitle(e.target.value)}
        placeholder="Título de la página"
      />
      <p>Contador: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}
```

### Limpieza de Efectos - Muy Importante

Algunos efectos necesitan **limpieza** para evitar problemas:

```jsx
function TimerComponent() {
  const [seconds, setSeconds] = useState(0);
  
  useEffect(() => {
    console.log('🚀 Iniciando timer');
    
    // Crear el timer
    const interval = setInterval(() => {
      setSeconds(prev => prev + 1);
    }, 1000);
    
    // 🧹 FUNCIÓN DE LIMPIEZA - MUY IMPORTANTE
    return () => {
      console.log('🧹 Limpiando timer');
      clearInterval(interval); // Detener el timer
    };
  }, []); // Solo se ejecuta una vez
  
  return <div>⏰ Segundos: {seconds}</div>;
}
```

### ¿Cuándo se ejecuta la limpieza?

```jsx
function CleanupTiming() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    console.log('✅ Efecto iniciado con count:', count);
    
    return () => {
      console.log('🧹 Limpieza del efecto anterior, count era:', count);
    };
  }, [count]);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}

// Secuencia al hacer clic:
// 1. 🧹 Limpieza del efecto anterior, count era: 0
// 2. ✅ Efecto iniciado con count: 1
```

### Ejemplo Completo: Suscripción a Eventos

```jsx
function WindowSizeTracker() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });
  
  useEffect(() => {
    console.log('🎧 Suscribiéndose al evento resize');
    
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };
    
    // Suscribirse al evento
    window.addEventListener('resize', handleResize);
    
    // 🧹 Limpieza: desuscribirse del evento
    return () => {
      console.log('🧹 Desuscribiéndose del evento resize');
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Solo una vez al montar
  
  return (
    <div>
      <h3>Tamaño de ventana:</h3>
      <p>Ancho: {windowSize.width}px</p>
      <p>Alto: {windowSize.height}px</p>
      <small>Redimensiona la ventana para ver los cambios</small>
    </div>
  );
}
```

### ⚠️ Problemas Comunes sin Limpieza

```jsx
// ❌ PROBLEMA: Sin limpieza
function BadTimer() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    setInterval(() => {
      setCount(prev => prev + 1);
    }, 1000);
    // ❌ Sin return - el timer nunca se detiene
  }, []);
  
  return <div>Count: {count}</div>;
}

// Problemas que causa:
// - Timer sigue ejecutándose aunque el componente se desmonte
// - Memory leaks
// - Múltiples timers si el componente se monta varias veces
```

### Patrones Comunes con useEffect

#### 1. Llamadas a API
```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
          throw new Error('Error al cargar usuario');
        }
        const userData = await response.json();
        setUser(userData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUser();
  }, [userId]); // Se ejecuta cuando userId cambia
  
  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>Usuario no encontrado</div>;
  
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}
```

#### 2. Suscripción a Eventos
```jsx
function WindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });
  
  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };
    
    window.addEventListener('resize', handleResize);
    
    // Limpieza
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);
  
  return (
    <div>
      Tamaño de ventana: {windowSize.width} x {windowSize.height}
    </div>
  );
}
```

#### 3. LocalStorage
```jsx
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });
  
  const setValue = (value) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };
  
  return [storedValue, setValue];
}

// Uso del custom hook
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  
  return (
    <div>
      <p>Tema actual: {theme}</p>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Cambiar tema
      </button>
    </div>
  );
}
```

