# Parte 2D: Custom Hooks y Patrones
## 🛠️ Custom Hooks

Los **Custom Hooks** son funciones que te permiten reutilizar lógica de estado entre componentes.

## 🛠️ Custom Hooks

### ¿Qué son los Custom Hooks?

Los **Custom Hooks** son funciones que te permiten **reutilizar lógica de estado** entre componentes. Son una de las características más poderosas de React.

### Reglas para Custom Hooks

1. **Nombre debe empezar con "use"** (convención obligatoria)
2. **Pueden usar otros Hooks** (useState, useEffect, etc.)
3. **Son funciones normales de JavaScript**
4. **Siguen las mismas reglas que los Hooks normales**

### Ejemplo Básico: useCounter

```jsx
// Custom Hook
function useCounter(initialValue = 0, step = 1) {
  const [count, setCount] = useState(initialValue);
  
  const increment = () => setCount(prev => prev + step);
  const decrement = () => setCount(prev => prev - step);
  const reset = () => setCount(initialValue);
  const setValue = (value) => setCount(value);
  
  return {
    count,
    increment,
    decrement,
    reset,
    setValue
  };
}

// Uso del Custom Hook en múltiples componentes
function CounterApp() {
  const likes = useCounter(0);           // Contador de likes
  const views = useCounter(100, 10);     // Contador de vistas (inicia en 100, incrementa de 10 en 10)
  const downloads = useCounter(0, 5);    // Contador de descargas (incrementa de 5 en 5)
  
  return (
    <div>
      <h2>📊 Estadísticas</h2>
      
      <div style={{ margin: '10px', padding: '10px', border: '1px solid #ccc' }}>
        <p>❤️ Likes: {likes.count}</p>
        <button onClick={likes.increment}>👍</button>
        <button onClick={likes.decrement}>👎</button>
        <button onClick={likes.reset}>Reset</button>
      </div>
      
      <div style={{ margin: '10px', padding: '10px', border: '1px solid #ccc' }}>
        <p>👀 Vistas: {views.count}</p>
        <button onClick={views.increment}>+10 vistas</button>
        <button onClick={views.reset}>Reset</button>
      </div>
      
      <div style={{ margin: '10px', padding: '10px', border: '1px solid #ccc' }}>
        <p>⬇️ Descargas: {downloads.count}</p>
        <button onClick={downloads.increment}>+5 descargas</button>
        <button onClick={() => downloads.setValue(1000)}>Set 1000</button>
      </div>
    </div>
  );
}
```

### Custom Hook Avanzado: useFetch

```jsx
function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (!url) return;
    
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [url]); // Se ejecuta cuando la URL cambia
  
  const refetch = () => {
    if (url) {
      setData(null);
      setError(null);
      // El useEffect se ejecutará automáticamente
    }
  };
  
  return { data, loading, error, refetch };
}

// Uso del Custom Hook useFetch
function UserProfile({ userId }) {
  const { data: user, loading, error, refetch } = useFetch(`/api/users/${userId}`);
  const { data: posts, loading: postsLoading } = useFetch(`/api/users/${userId}/posts`);
  
  if (loading) return <div>⏳ Cargando usuario...</div>;
  if (error) return <div>❌ Error: {error}</div>;
  if (!user) return <div>🤷‍♂️ Usuario no encontrado</div>;
  
  return (
    <div>
      <h2>👤 {user.name}</h2>
      <p>📧 {user.email}</p>
      <button onClick={refetch}>🔄 Actualizar</button>
      
      <h3>📝 Posts del usuario:</h3>
      {postsLoading ? (
        <p>⏳ Cargando posts...</p>
      ) : (
        <ul>
          {posts?.map(post => (
            <li key={post.id}>{post.title}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Custom Hook para LocalStorage: useLocalStorage

```jsx
function useLocalStorage(key, initialValue) {
  // Obtener valor inicial del localStorage o usar el valor por defecto
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });
  
  // Función para actualizar el estado y localStorage
  const setValue = (value) => {
    try {
      // Permitir que value sea una función como en useState
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  };
  
  return [storedValue, setValue];
}

// Uso del Custom Hook useLocalStorage
function SettingsApp() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  const [language, setLanguage] = useLocalStorage('language', 'es');
  const [notifications, setNotifications] = useLocalStorage('notifications', true);
  
  return (
    <div style={{ 
      backgroundColor: theme === 'dark' ? '#333' : '#fff',
      color: theme === 'dark' ? '#fff' : '#333',
      padding: '20px',
      minHeight: '200px'
    }}>
      <h2>⚙️ Configuraciones (se guardan automáticamente)</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <label>🎨 Tema: </label>
        <select value={theme} onChange={(e) => setTheme(e.target.value)}>
          <option value="light">Claro</option>
          <option value="dark">Oscuro</option>
        </select>
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label>🌍 Idioma: </label>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="es">Español</option>
          <option value="en">English</option>
          <option value="fr">Français</option>
        </select>
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label>
          <input 
            type="checkbox"
            checked={notifications}
            onChange={(e) => setNotifications(e.target.checked)}
          />
          <span style={{ marginLeft: '8px' }}>🔔 Notificaciones</span>
        </label>
      </div>
      
      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: 'rgba(0,0,0,0.1)' }}>
        <h4>Estado actual:</h4>
        <p>Tema: {theme}</p>
        <p>Idioma: {language}</p>
        <p>Notificaciones: {notifications ? 'Activadas' : 'Desactivadas'}</p>
        <small>💾 Estos valores se guardan automáticamente en localStorage</small>
      </div>
    </div>
  );
}
```

### Custom Hook para Toggle: useToggle

```jsx
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);
  
  const toggle = useCallback(() => {
    setValue(prev => !prev);
  }, []);
  
  const setTrue = useCallback(() => {
    setValue(true);
  }, []);
  
  const setFalse = useCallback(() => {
    setValue(false);
  }, []);
  
  return [value, { toggle, setTrue, setFalse }];
}

// Uso del Custom Hook useToggle
function ToggleDemo() {
  const [isModalOpen, modalControls] = useToggle(false);
  const [isDarkMode, darkModeControls] = useToggle(false);
  const [isNotificationsEnabled, notificationControls] = useToggle(true);
  
  return (
    <div style={{ 
      backgroundColor: isDarkMode ? '#333' : '#fff',
      color: isDarkMode ? '#fff' : '#333',
      padding: '20px'
    }}>
      <h2>🎛️ Demo de useToggle</h2>
      
      <div style={{ marginBottom: '10px' }}>
        <button onClick={modalControls.toggle}>
          {isModalOpen ? '❌ Cerrar Modal' : '📱 Abrir Modal'}
        </button>
        {isModalOpen && (
          <div style={{ 
            border: '2px solid #ccc', 
            padding: '20px', 
            margin: '10px 0',
            backgroundColor: 'rgba(0,0,0,0.1)'
          }}>
            <h3>📱 Modal Abierto</h3>
            <p>Este es el contenido del modal</p>
            <button onClick={modalControls.setFalse}>Cerrar</button>
          </div>
        )}
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <button onClick={darkModeControls.toggle}>
          {isDarkMode ? '☀️ Modo Claro' : '🌙 Modo Oscuro'}
        </button>
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <button onClick={notificationControls.toggle}>
          🔔 Notificaciones: {isNotificationsEnabled ? 'ON' : 'OFF'}
        </button>
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <h4>Controles directos:</h4>
        <button onClick={darkModeControls.setTrue}>🌙 Forzar oscuro</button>
        <button onClick={darkModeControls.setFalse}>☀️ Forzar claro</button>
      </div>
    </div>
  );
}
```

### Ventajas de los Custom Hooks

✅ **Reutilización de lógica** - Usar la misma lógica en múltiples componentes  
✅ **Separación de responsabilidades** - Componentes más simples  
✅ **Fácil testing** - Los hooks se pueden probar independientemente  
✅ **Composición** - Combinar múltiples hooks  
✅ **Abstracción** - Ocultar complejidad detrás de una interfaz simple

### Cuándo crear un Custom Hook

🤔 **Pregúntate:**

- ¿Estoy copiando y pegando la misma lógica en múltiples componentes?
- ¿Esta lógica es compleja y podría beneficiarse de ser abstraída?
- ¿Otros desarrolladores podrían beneficiarse de esta funcionalidad?
- ¿Quiero testear esta lógica independientemente?

Si respondes "Sí" a alguna de estas preguntas, ¡es hora de crear un Custom Hook!

## 🔧 Herramientas y Debugging

### React Developer Tools

1. **Instalar la extensión** en tu navegador
2. **Abrir DevTools** (F12)
3. **Ir a la pestaña "Components"**
4. **Inspeccionar estado y props** de componentes

### Debugging con useEffect

```jsx
function DebuggingComponent() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  
  // Debug: Ver cuándo se ejecuta el efecto
  useEffect(() => {
    console.log('🔄 Efecto ejecutado', { count, name });
  }, [count, name]);
  
  // Debug: Ver solo cambios de count
  useEffect(() => {
    console.log('📊 Count cambió:', count);
  }, [count]);
  
  // Debug: Solo una vez al montar
  useEffect(() => {
    console.log('🚀 Componente montado');
    
    return () => {
      console.log('💥 Componente desmontado');  
    };
  }, []);
  
  return (
    <div>
      <p>Count: {count}</p>
      <p>Name: {name}</p>
      <button onClick={() => setCount(count + 1)}>+Count</button>
      <input 
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Nombre"
      />
    </div>
  );
}
```

## 📚 Patrones Comunes

### 1. Loading States

Este patrón maneja los tres estados principales de una operación asíncrona: carga, error y éxito. Es esencial para dar feedback al usuario sobre el estado de las peticiones de datos.

```jsx
function DataComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchData()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return <div>No hay datos</div>;
  
  return <div>{/* Renderizar datos */}</div>;
}
```

### 2. Toggle State

Hook personalizado para manejar estados booleanos que se alternan (on/off, visible/oculto, abierto/cerrado). Útil para modales, menús desplegables, acordeones, etc.

```jsx
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);
  
  const toggle = useCallback(() => {
    setValue(prev => !prev);
  }, []);
  
  return [value, toggle];
}

// Uso
function ToggleComponent() {
  const [isVisible, toggleVisible] = useToggle(false);
  
  return (
    <div>
      <button onClick={toggleVisible}>
        {isVisible ? 'Ocultar' : 'Mostrar'}
      </button>
      {isVisible && <p>Contenido visible</p>}
    </div>
  );
}
```

### 3. Previous Value

Hook que permite acceder al valor anterior de una variable entre renders. Útil para comparaciones, detectar cambios y animaciones basadas en transiciones de estado.

```jsx
function usePrevious(value) {
  const ref = useRef();
  
  useEffect(() => {
    ref.current = value;
  });
  
  return ref.current;
}

// Uso
function CompareComponent({ count }) {
  const prevCount = usePrevious(count);
  
  return (
    <div>
      <p>Actual: {count}</p>
      <p>Anterior: {prevCount}</p>
      <p>Cambió: {count !== prevCount ? 'Sí' : 'No'}</p>
    </div>
  );
}
```

## 🎯 Puntos Clave para Recordar

1. **Hooks solo en componentes funcionales** y custom hooks
2. **Siempre en el nivel superior** del componente (nunca dentro de loops, condiciones o funciones anidadas)
3. **useState para estado que cambia** - diferente a variables normales de JavaScript
4. **useEffect con array de dependencias** para controlar cuándo se ejecuta
5. **Limpiar efectos** cuando sea necesario (timers, suscripciones, etc.)
6. **Estado es inmutable** - usar spread operator o funciones que no mutan
7. **Props son de solo lectura** - no modificar directamente
8. **Custom hooks** para reutilizar lógica entre componentes
9. **Componentes controlados** para formularios (React maneja el estado)
10. **Debugging** con React DevTools y console.log estratégicos

## 🔄 Resumen de Conceptos Clave

### useState
```jsx
const [state, setState] = useState(initialValue);
setState(newValue);              // Valor directo
setState(prev => prev + 1);      // Función con valor anterior
```

### useEffect
```jsx
useEffect(() => {}, []);         // Solo una vez (mount)
useEffect(() => {});             // En cada render
useEffect(() => {}, [count]);    // Cuando count cambia
useEffect(() => {
  return () => {};               // Función de limpieza
}, []);
```

### Comunicación
```jsx
// Padre → Hijo (Props)
<Child data={parentData} />

// Hijo → Padre (Callbacks)
<Child onAction={handleAction} />
```

### Formularios
```jsx
const [value, setValue] = useState('');
<input 
  value={value} 
  onChange={(e) => setValue(e.target.value)} 
/>
```

## 🏁 Próximos Pasos

En el próximo módulo aprenderemos:

- **useContext** para manejo de estado global
- **useReducer** para estado complejo
- **React Router** para navegación
- **Optimización de rendimiento**
- **Testing de componentes**

## ❓ Preguntas Frecuentes

**P: ¿Cuál es la diferencia entre useState y variables normales?**
R: `useState` causa re-renderizado cuando cambia, las variables normales no. React "recuerda" el estado entre renders.

**P: ¿Por qué mi estado no se actualiza inmediatamente después de setState?**
R: Las actualizaciones de estado son asíncronas. Usa la forma funcional `setState(prev => prev + 1)` para múltiples actualizaciones.

**P: ¿Cuándo usar useState vs useReducer?**
R: `useState` para estado simple, `useReducer` para estado complejo con múltiples acciones relacionadas.

**P: ¿Es malo tener muchos useEffect?**
R: No, es mejor tener varios `useEffect` específicos que uno que haga muchas cosas diferentes.

**P: ¿Cómo evito loops infinitos en useEffect?**
R: Siempre incluye un array de dependencias y asegúrate de que contenga todas las variables que usa el efecto.

**P: ¿Puedo usar Hooks en componentes de clase?**
R: No, los Hooks solo funcionan en componentes funcionales.

**P: ¿Cuándo debo crear un Custom Hook?**
R: Cuando tienes la misma lógica en múltiples componentes o cuando quieres abstraer lógica compleja.

**P: ¿Por qué debo limpiar los efectos?**
R: Para evitar memory leaks, efectos que se ejecuten después de que el componente se desmonte, y múltiples suscripciones.