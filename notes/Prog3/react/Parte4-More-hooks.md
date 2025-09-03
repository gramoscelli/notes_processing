# Parte 4: Hooks Avanzados - useContext, useReducer, useMemo y useCallback

## 🌐 useContext - Manejo de Estado Global

### ¿Qué es el Contexto?

El **contexto** en React es una forma de **compartir datos entre componentes** sin tener que pasar props manualmente a través de cada nivel del árbol de componentes. Es la solución al problema del "prop drilling".

### Problema: Prop Drilling

```jsx
// ❌ Problema: Pasando props por muchos niveles
function App() {
  const [user, setUser] = useState({ name: 'Juan', theme: 'dark' });
  
  return <Header user={user} />;
}

function Header({ user }) {
  return <Navigation user={user} />; // Solo pasa la prop
}

function Navigation({ user }) {
  return <UserMenu user={user} />; // Solo pasa la prop
}

function UserMenu({ user }) {
  return <div>Hola, {user.name}!</div>; // Finalmente la usa
}
```

### Solución: useContext

```jsx
import { createContext, useContext, useState } from 'react';

// 1️⃣ Crear el contexto
const UserContext = createContext();

// 2️⃣ Crear el Provider
function UserProvider({ children }) {
  const [user, setUser] = useState({ name: 'Juan', theme: 'dark' });
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

// 3️⃣ Hook personalizado para usar el contexto
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser debe usarse dentro de UserProvider');
  }
  return context;
}

// 4️⃣ Uso en componentes
function App() {
  return (
    <UserProvider>
      <Header />
    </UserProvider>
  );
}

function Header() {
  return <Navigation />; // ✅ No necesita pasar props
}

function Navigation() {
  return <UserMenu />; // ✅ No necesita pasar props
}

function UserMenu() {
  const { user, setUser } = useUser(); // ✅ Acceso directo al contexto
  
  return (
    <div>
      <p>Hola, {user.name}!</p>
      <button onClick={() => setUser(prev => ({ ...prev, name: 'Ana' }))}>
        Cambiar usuario
      </button>
    </div>
  );
}
```

### Ejemplo Completo: Tema y Autenticación

```jsx
import { createContext, useContext, useState, useEffect } from 'react';

// 🎨 Contexto de Tema
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };
  
  // Aplicar tema al body
  useEffect(() => {
    document.body.className = theme;
  }, [theme]);
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// 👤 Contexto de Autenticación
const AuthContext = createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Simular carga inicial del usuario
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);
  
  const login = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };
  
  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };
  
  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

// 🪝 Custom hooks
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme debe usarse dentro de ThemeProvider');
  }
  return context;
}

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
}

// 🎯 Componentes que usan el contexto
function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <div style={{ minHeight: '100vh', padding: '20px' }}>
          <Header />
          <Main />
        </div>
      </AuthProvider>
    </ThemeProvider>
  );
}

function Header() {
  const { theme, toggleTheme } = useTheme();
  const { user, logout } = useAuth();
  
  return (
    <header style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center',
      padding: '10px 20px',
      backgroundColor: theme === 'dark' ? '#333' : '#fff',
      color: theme === 'dark' ? '#fff' : '#333',
      borderBottom: '1px solid #ccc'
    }}>
      <h1>Mi App</h1>
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
        <button onClick={toggleTheme}>
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
        {user ? (
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <span>Hola, {user.name}!</span>
            <button onClick={logout}>Cerrar sesión</button>
          </div>
        ) : (
          <LoginButton />
        )}
      </div>
    </header>
  );
}

function LoginButton() {
  const { login } = useAuth();
  
  const handleLogin = () => {
    login({ name: 'Usuario', email: 'user@example.com' });
  };
  
  return <button onClick={handleLogin}>Iniciar sesión</button>;
}

function Main() {
  const { theme } = useTheme();
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div>Cargando...</div>;
  }
  
  return (
    <main style={{ 
      padding: '20px',
      backgroundColor: theme === 'dark' ? '#222' : '#f5f5f5',
      color: theme === 'dark' ? '#fff' : '#333',
      minHeight: '80vh'
    }}>
      <h2>Contenido Principal</h2>
      <p>Tema actual: {theme}</p>
      <p>Usuario: {user ? user.name : 'No autenticado'}</p>
    </main>
  );
}
```



## 🔄 useReducer - Estado Complejo

### ¿Cuándo usar useReducer?

Usa `useReducer` cuando:

- Tienes **lógica de estado compleja**
- El **próximo estado depende del anterior**
- Tienes **múltiples valores de estado relacionados**
- Quieres **centralizar la lógica de actualización**

### Comparación: useState vs useReducer

```jsx
// ❌ useState para estado complejo - se vuelve difícil de manejar
function CounterWithUseState() {
  const [count, setCount] = useState(0);
  const [step, setStep] = useState(1);
  const [history, setHistory] = useState([0]);
  
  const increment = () => {
    const newCount = count + step;
    setCount(newCount);
    setHistory(prev => [...prev, newCount]);
  };
  
  const decrement = () => {
    const newCount = count - step;
    setCount(newCount);
    setHistory(prev => [...prev, newCount]);
  };
  
  const reset = () => {
    setCount(0);
    setStep(1);
    setHistory([0]);
  };
  
  // ... más lógica compleja
}
```

```jsx
// ✅ useReducer para estado complejo - más organizado
const initialState = {
  count: 0,
  step: 1,
  history: [0]
};

function counterReducer(state, action) {
  switch (action.type) {
    case 'INCREMENT': {
      const newCount = state.count + state.step;
      return {
        ...state,
        count: newCount,
        history: [...state.history, newCount]
      };
    }
    
    case 'DECREMENT': {
      const newCount = state.count - state.step;
      return {
        ...state,
        count: newCount,
        history: [...state.history, newCount]
      };
    }
    
    case 'SET_STEP':
      return {
        ...state,
        step: action.payload
      };
    
    case 'RESET':
      return initialState;
    
    case 'UNDO': {
      if (state.history.length <= 1) return state;
      const newHistory = state.history.slice(0, -1);
      return {
        ...state,
        count: newHistory[newHistory.length - 1],
        history: newHistory
      };
    }
    
    default:
      throw new Error(`Acción no reconocida: ${action.type}`);
  }
}

function CounterWithUseReducer() {
  const [state, dispatch] = useReducer(counterReducer, initialState);
  
  return (
    <div>
      <h2>Contador con useReducer</h2>
      <p>Valor: {state.count}</p>
      <p>Paso: {state.step}</p>
      
      <div>
        <button onClick={() => dispatch({ type: 'INCREMENT' })}>
          +{state.step}
        </button>
        <button onClick={() => dispatch({ type: 'DECREMENT' })}>
          -{state.step}
        </button>
        <button onClick={() => dispatch({ type: 'RESET' })}>
          Reset
        </button>
        <button onClick={() => dispatch({ type: 'UNDO' })}>
          Deshacer
        </button>
      </div>
      
      <div>
        <label>
          Paso: 
          <input 
            type="number"
            value={state.step}
            onChange={(e) => dispatch({ 
              type: 'SET_STEP', 
              payload: parseInt(e.target.value) || 1 
            })}
          />
        </label>
      </div>
      
      <div>
        <h3>Historial:</h3>
        <p>{state.history.join(' → ')}</p>
      </div>
    </div>
  );
}
```

### Ejemplo Avanzado: Carrito de Compras

```jsx
const initialCartState = {
  items: [],
  total: 0,
  discountCode: null,
  discountAmount: 0
};

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingItem = state.items.find(item => item.id === action.payload.id);
      
      let newItems;
      if (existingItem) {
        newItems = state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        newItems = [...state.items, { ...action.payload, quantity: 1 }];
      }
      
      const newTotal = newItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
      
      return {
        ...state,
        items: newItems,
        total: newTotal - state.discountAmount
      };
    }
    
    case 'REMOVE_ITEM': {
      const newItems = state.items.filter(item => item.id !== action.payload.id);
      const newTotal = newItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
      
      return {
        ...state,
        items: newItems,
        total: newTotal - state.discountAmount
      };
    }
    
    case 'UPDATE_QUANTITY': {
      const newItems = state.items.map(item =>
        item.id === action.payload.id
          ? { ...item, quantity: Math.max(0, action.payload.quantity) }
          : item
      ).filter(item => item.quantity > 0);
      
      const newTotal = newItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
      
      return {
        ...state,
        items: newItems,
        total: newTotal - state.discountAmount
      };
    }
    
    case 'APPLY_DISCOUNT': {
      const discount = action.payload.type === 'percentage' 
        ? (state.total * action.payload.value / 100)
        : action.payload.value;
        
      return {
        ...state,
        discountCode: action.payload.code,
        discountAmount: discount,
        total: state.total - discount
      };
    }
    
    case 'CLEAR_CART':
      return initialCartState;
    
    default:
      throw new Error(`Acción no reconocida: ${action.type}`);
  }
}

function ShoppingCart() {
  const [cartState, dispatch] = useReducer(cartReducer, initialCartState);
  
  const products = [
    { id: 1, name: 'Laptop', price: 999 },
    { id: 2, name: 'Mouse', price: 25 },
    { id: 3, name: 'Teclado', price: 75 }
  ];
  
  const addToCart = (product) => {
    dispatch({ type: 'ADD_ITEM', payload: product });
  };
  
  const removeFromCart = (product) => {
    dispatch({ type: 'REMOVE_ITEM', payload: product });
  };
  
  const updateQuantity = (id, quantity) => {
    dispatch({ type: 'UPDATE_QUANTITY', payload: { id, quantity } });
  };
  
  const applyDiscount = () => {
    dispatch({ 
      type: 'APPLY_DISCOUNT', 
      payload: { code: 'DESCUENTO10', type: 'percentage', value: 10 }
    });
  };
  
  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      {/* Productos */}
      <div style={{ flex: 1 }}>
        <h3>Productos</h3>
        {products.map(product => (
          <div key={product.id} style={{ 
            border: '1px solid #ccc', 
            padding: '10px', 
            margin: '10px 0' 
          }}>
            <h4>{product.name}</h4>
            <p>${product.price}</p>
            <button onClick={() => addToCart(product)}>
              Agregar al carrito
            </button>
          </div>
        ))}
      </div>
      
      {/* Carrito */}
      <div style={{ flex: 1 }}>
        <h3>Carrito ({cartState.items.length} items)</h3>
        
        {cartState.items.length === 0 ? (
          <p>Carrito vacío</p>
        ) : (
          <>
            {cartState.items.map(item => (
              <div key={item.id} style={{ 
                display: 'flex', 
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '10px',
                border: '1px solid #eee',
                margin: '5px 0'
              }}>
                <div>
                  <span>{item.name}</span>
                  <br />
                  <small>${item.price} x {item.quantity}</small>
                </div>
                <div style={{ display: 'flex', gap: '5px', alignItems: 'center' }}>
                  <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>
                    -
                  </button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>
                    +
                  </button>
                  <button onClick={() => removeFromCart(item)}>
                    🗑️
                  </button>
                </div>
              </div>
            ))}
            
            <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f5f5f5' }}>
              {cartState.discountAmount > 0 && (
                <p>Descuento ({cartState.discountCode}): -${cartState.discountAmount}</p>
              )}
              <h3>Total: ${cartState.total}</h3>
              
              <div style={{ marginTop: '10px' }}>
                <button onClick={applyDiscount} disabled={cartState.discountCode}>
                  Aplicar descuento 10%
                </button>
                <button onClick={() => dispatch({ type: 'CLEAR_CART' })}>
                  Vaciar carrito
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
```

## ⚡ useMemo - Memorización de Valores

### ¿Qué es useMemo?

`useMemo` es un hook que **memoriza el resultado de un cálculo costoso** y solo lo recalcula cuando sus dependencias cambian. Es una optimización de rendimiento.

### Cuándo usar useMemo

✅ **Usar cuando:**

- Tienes **cálculos costosos** que no quieres repetir
- El **resultado depende de valores específicos**
- Quieres **evitar re-renderizados innecesarios** de componentes hijos

❌ **No usar cuando:**

- El cálculo es **simple y rápido**
- Las dependencias **cambian en cada render**
- Estás **optimizando prematuramente**

### Ejemplo Sin useMemo vs Con useMemo

```jsx
// ❌ Sin optimización - cálculo en cada render
function ExpensiveComponent({ items, filter }) {
  console.log('🔄 Calculando items filtrados...'); // Se ejecuta en cada render
  
  // Cálculo costoso que se ejecuta siempre
  const filteredItems = items.filter(item => {
    // Simulamos un proceso costoso
    for (let i = 0; i < 1000000; i++) {
      // Operación costosa
    }
    return item.category === filter;
  });
  
  const [count, setCount] = useState(0); // Estado que causa re-renders
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Contador: {count}
      </button>
      <p>Items filtrados: {filteredItems.length}</p>
    </div>
  );
}
```

```jsx
// ✅ Con useMemo - cálculo solo cuando es necesario
function OptimizedComponent({ items, filter }) {
  console.log('🎨 Componente renderizado');
  
  // Cálculo memorizado - solo se ejecuta cuando items o filter cambian
  const filteredItems = useMemo(() => {
    console.log('🔄 Calculando items filtrados...');
    
    return items.filter(item => {
      // Simulamos un proceso costoso
      for (let i = 0; i < 1000000; i++) {
        // Operación costosa
      }
      return item.category === filter;
    });
  }, [items, filter]); // Solo recalcula cuando estas dependencias cambian
  
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Contador: {count} {/* Esto NO recalcula filteredItems */}
      </button>
      <p>Items filtrados: {filteredItems.length}</p>
    </div>
  );
}
```

### Ejemplo Práctico: Lista de Productos con Búsqueda

```jsx
function ProductList() {
  const [products] = useState([
    { id: 1, name: 'Laptop Dell', category: 'electronics', price: 999, rating: 4.5 },
    { id: 2, name: 'iPhone 14', category: 'electronics', price: 799, rating: 4.8 },
    { id: 3, name: 'Silla Gaming', category: 'furniture', price: 299, rating: 4.2 },
    { id: 4, name: 'Mesa de Oficina', category: 'furniture', price: 199, rating: 4.0 },
    { id: 5, name: 'Auriculares Sony', category: 'electronics', price: 149, rating: 4.6 }
  ]);
  
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [count, setCount] = useState(0); // Estado que no afecta los productos
  
  // 🔍 Productos filtrados - solo recalcula cuando cambian las dependencias relevantes
  const filteredProducts = useMemo(() => {
    console.log('🔍 Filtrando productos...');
    
    return products
      .filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
        return matchesSearch && matchesCategory;
      });
  }, [products, searchTerm, selectedCategory]);
  
  // 📊 Productos ordenados - solo recalcula cuando filteredProducts o sortBy cambian
  const sortedProducts = useMemo(() => {
    console.log('📊 Ordenando productos...');
    
    return [...filteredProducts].sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'price':
          return a.price - b.price;
        case 'rating':
          return b.rating - a.rating; // Mayor rating primero
        default:
          return 0;
      }
    });
  }, [filteredProducts, sortBy]);
  
  // 💰 Estadísticas - solo recalcula cuando sortedProducts cambia
  const statistics = useMemo(() => {
    console.log('💰 Calculando estadísticas...');
    
    if (sortedProducts.length === 0) {
      return { total: 0, average: 0, min: 0, max: 0 };
    }
    
    const prices = sortedProducts.map(p => p.price);
    const total = prices.reduce((sum, price) => sum + price, 0);
    
    return {
      total: sortedProducts.length,
      average: (total / sortedProducts.length).toFixed(2),
      min: Math.min(...prices),
      max: Math.max(...prices)
    };
  }, [sortedProducts]);
  
  return (
    <div style={{ padding: '20px' }}>
      <h2>Lista de Productos</h2>
      
      {/* Controles que NO afectan los cálculos memoizados */}
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setCount(count + 1)}>
          Contador: {count} (esto no recalcula productos)
        </button>
      </div>
      
      {/* Controles que SÍ afectan los cálculos memoizados */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Buscar productos..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ padding: '8px', flex: 1 }}
        />
        
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          style={{ padding: '8px' }}
        >
          <option value="all">Todas las categorías</option>
          <option value="electronics">Electrónicos</option>
          <option value="furniture">Muebles</option>
        </select>
        
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{ padding: '8px' }}
        >
          <option value="name">Ordenar por nombre</option>
          <option value="price">Ordenar por precio</option>
          <option value="rating">Ordenar por rating</option>
        </select>
      </div>
      
      {/* Estadísticas */}
      <div style={{ 
        backgroundColor: '#f5f5f5', 
        padding: '15px', 
        marginBottom: '20px',
        borderRadius: '5px'
      }}>
        <h3>📊 Estadísticas</h3>
        <p>Total de productos: {statistics.total}</p>
        <p>Precio promedio: ${statistics.average}</p>
        <p>Precio mínimo: ${statistics.min}</p>
        <p>Precio máximo: ${statistics.max}</p>
      </div>
      
      {/* Lista de productos */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '15px' }}>
        {sortedProducts.map(product => (
          <div key={product.id} style={{ 
            border: '1px solid #ddd', 
            padding: '15px', 
            borderRadius: '5px' 
          }}>
            <h4>{product.name}</h4>
            <p>Categoría: {product.category}</p>
            <p>Precio: ${product.price}</p>
            <p>Rating: ⭐ {product.rating}</p>
          </div>
        ))}
      </div>
      
      {sortedProducts.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666' }}>
          No se encontraron productos
        </p>
      )}
    </div>
  );
}
```

## 🔗 useCallback - Memorización de Funciones

### ¿Qué es useCallback?

`useCallback` es un hook que **memoriza una función** y solo la recrea cuando sus dependencias cambian. Previene que los componentes hijos se re-rendericen innecesariamente.

### Problema: Funciones recreadas en cada render

```jsx
// ❌ Problema: La función se recrea en cada render
function Parent() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  
  // Esta función se recrea en CADA render del Parent
  const handleClick = (id) => {
    console.log(`Clicked item ${id}`);
  };
  
  return (
    <div>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
      
      {/* Child se re-renderiza cada vez porque handleClick es una nueva función */}
      <Child onItemClick={handleClick} />
    </div>
  );
}

const Child = React.memo(({ onItemClick }) => {
  console.log('🔄 Child re-rendered'); // Se ejecuta en cada cambio del parent
  
  return (
    <div>
      <button onClick={() => onItemClick(1)}>Item 1</button>
      <button onClick={() => onItemClick(2)}>Item 2</button>
    </div>
  );
});
```

### Solución: useCallback

```jsx
// ✅ Solución: Memorizar la función con useCallback
function Parent() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  
  // La función solo se recrea si sus dependencias cambian
  const handleClick = useCallback((id) => {
    console.log(`Clicked item ${id}`);
    // Si la función usara 'count', tendríamos que agregarlo a las dependencias
  }, []); // Array vacío = la función nunca cambia
  
  return (
    <div>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
      
      {/* Child NO se re-renderiza porque handleClick no cambia */}
      <Child onItemClick={handleClick} />
    </div>
  );
}

const Child = React.memo(({ onItemClick }) => {
  console.log('🔄 Child re-rendered'); // Solo se ejecuta una vez
  
  return (
    <div>
      <button onClick={() => onItemClick(1)}>Item 1</button>
      <button onClick={() => onItemClick(2)}>Item 2</button>
    </div>
  );
});
```

### Ejemplo Completo: Lista de Tareas Optimizada

```jsx
import { useState, useCallback, useMemo } from 'react';
import React from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Aprender React', completed: false },
    { id: 2, text: 'Hacer ejercicios', completed: true },
    { id: 3, text: 'Estudiar hooks', completed: false }
  ]);
  
  const [filter, setFilter] = useState('all'); // all, active, completed
  const [newTodo, setNewTodo] = useState('');
  
  // 🔄 Funciones memoizadas con useCallback
  const addTodo = useCallback((text) => {
    if (text.trim()) {
      setTodos(prev => [...prev, {
        id: Date.now(),
        text: text.trim(),
        completed: false
      }]);
    }
  }, []);
  
  const toggleTodo = useCallback((id) => {
    setTodos(prev => prev.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  }, []);
  
  const deleteTodo = useCallback((id) => {
    setTodos(prev => prev.filter(todo => todo.id !== id));
  }, []);
  
  const editTodo = useCallback((id, newText) => {
    setTodos(prev => prev.map(todo =>
      todo.id === id ? { ...todo, text: newText } : todo
    ));
  }, []);
  
  // 📊 Todos filtrados - memoizados con useMemo
  const filteredTodos = useMemo(() => {
    console.log('🔍 Filtrando todos...');
    
    switch (filter) {
      case 'active':
        return todos.filter(todo => !todo.completed);
      case 'completed':
        return todos.filter(todo => todo.completed);
      default:
        return todos;
    }
  }, [todos, filter]);
  
  // 📈 Estadísticas - memoizadas con useMemo
  const stats = useMemo(() => {
    console.log('📈 Calculando estadísticas...');
    
    const total = todos.length;
    const completed = todos.filter(todo => todo.completed).length;
    const active = total - completed;
    
    return { total, completed, active };
  }, [todos]);
  
  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    addTodo(newTodo);
    setNewTodo('');
  }, [newTodo, addTodo]);
  
  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>📝 Lista de Tareas Optimizada</h1>
      
      {/* Estadísticas */}
      <div style={{ 
        backgroundColor: '#f5f5f5', 
        padding: '15px', 
        marginBottom: '20px',
        borderRadius: '5px',
        display: 'flex',
        justifyContent: 'space-around'
      }}>
        <span>Total: {stats.total}</span>
        <span>Activas: {stats.active}</span>
        <span>Completadas: {stats.completed}</span>
      </div>
      
      {/* Formulario para agregar todos */}
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Nueva tarea..."
          style={{ 
            padding: '10px', 
            width: '70%', 
            marginRight: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px'
          }}
        />
        <button type="submit" style={{ 
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}>
          Agregar
        </button>
      </form>
      
      {/* Filtros */}
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={() => setFilter('all')}
          style={{ 
            marginRight: '10px',
            backgroundColor: filter === 'all' ? '#007bff' : '#f8f9fa',
            color: filter === 'all' ? 'white' : 'black'
          }}
        >
          Todas
        </button>
        <button 
          onClick={() => setFilter('active')}
          style={{ 
            marginRight: '10px',
            backgroundColor: filter === 'active' ? '#007bff' : '#f8f9fa',
            color: filter === 'active' ? 'white' : 'black'
          }}
        >
          Activas
        </button>
        <button 
          onClick={() => setFilter('completed')}
          style={{ 
            backgroundColor: filter === 'completed' ? '#007bff' : '#f8f9fa',
            color: filter === 'completed' ? 'white' : 'black'
          }}
        >
          Completadas
        </button>
      </div>
      
      {/* Lista de todos */}
      <div>
        {filteredTodos.map(todo => (
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggle={toggleTodo}
            onDelete={deleteTodo}
            onEdit={editTodo}
          />
        ))}
      </div>
      
      {filteredTodos.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666', fontStyle: 'italic' }}>
          {filter === 'all' ? 'No hay tareas' : `No hay tareas ${filter === 'active' ? 'activas' : 'completadas'}`}
        </p>
      )}
    </div>
  );
}

// 🎯 Componente hijo optimizado con React.memo
const TodoItem = React.memo(({ todo, onToggle, onDelete, onEdit }) => {
  console.log(`🔄 Renderizando TodoItem ${todo.id}`); // Solo se ejecuta cuando las props cambian
  
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);
  
  const handleSave = () => {
    onEdit(todo.id, editText);
    setIsEditing(false);
  };
  
  const handleCancel = () => {
    setEditText(todo.text);
    setIsEditing(false);
  };
  
  if (isEditing) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        padding: '10px',
        border: '1px solid #ddd',
        marginBottom: '5px',
        borderRadius: '4px',
        backgroundColor: '#fff3cd'
      }}>
        <input
          type="text"
          value={editText}
          onChange={(e) => setEditText(e.target.value)}
          style={{ flex: 1, padding: '5px', marginRight: '10px' }}
          autoFocus
        />
        <button onClick={handleSave} style={{ marginRight: '5px' }}>
          💾
        </button>
        <button onClick={handleCancel}>
          ❌
        </button>
      </div>
    );
  }
  
  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      padding: '10px',
      border: '1px solid #ddd',
      marginBottom: '5px',
      borderRadius: '4px',
      backgroundColor: todo.completed ? '#d4edda' : '#ffffff'
    }}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        style={{ marginRight: '10px' }}
      />
      <span
        style={{
          flex: 1,
          textDecoration: todo.completed ? 'line-through' : 'none',
          color: todo.completed ? '#6c757d' : '#000'
        }}
      >
        {todo.text}
      </span>
      <button
        onClick={() => setIsEditing(true)}
        style={{ marginRight: '5px', background: 'none', border: 'none', cursor: 'pointer' }}
      >
        ✏️
      </button>
      <button
        onClick={() => onDelete(todo.id)}
        style={{ background: 'none', border: 'none', cursor: 'pointer' }}
      >
        🗑️
      </button>
    </div>
  );
});
```



## 📊 Comparación de Hooks

| Hook | Propósito | Cuándo usar | Ejemplo |
||--|||
| `useState` | Estado local simple | Valores que cambian | `const [count, setCount] = useState(0)` |
| `useEffect` | Efectos secundarios | API calls, suscripciones | `useEffect(() => {}, [deps])` |
| `useContext` | Estado global | Evitar prop drilling | `const value = useContext(MyContext)` |
| `useReducer` | Estado complejo | Múltiples acciones relacionadas | `const [state, dispatch] = useReducer(reducer, initial)` |
| `useMemo` | Memorizar valores | Cálculos costosos | `const value = useMemo(() => compute(), [deps])` |
| `useCallback` | Memorizar funciones | Evitar re-renders de hijos | `const fn = useCallback(() => {}, [deps])` |



## ⚡ Patrones de Optimización

### 1. Combinando useMemo y useCallback

```jsx
function OptimizedComponent({ data, onItemClick }) {
  const [sortBy, setSortBy] = useState('name');
  const [filterTerm, setFilterTerm] = useState('');
  
  // 📊 Datos procesados - useMemo para el cálculo
  const processedData = useMemo(() => {
    return data
      .filter(item => item.name.includes(filterTerm))
      .sort((a, b) => a[sortBy].localeCompare(b[sortBy]));
  }, [data, filterTerm, sortBy]);
  
  // 🔗 Función memoizada - useCallback para la función
  const handleItemClick = useCallback((id) => {
    // Hacer algo con el ID
    onItemClick(id);
  }, [onItemClick]);
  
  return (
    <div>
      <input 
        value={filterTerm}
        onChange={(e) => setFilterTerm(e.target.value)}
        placeholder="Filtrar..."
      />
      
      {processedData.map(item => (
        <OptimizedItem 
          key={item.id}
          item={item}
          onClick={handleItemClick}
        />
      ))}
    </div>
  );
}

const OptimizedItem = React.memo(({ item, onClick }) => {
  return (
    <div onClick={() => onClick(item.id)}>
      {item.name}
    </div>
  );
});
```

### 2. Custom Hook con Optimización

```jsx
function useOptimizedApi(url, params) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Memoizar la URL completa para evitar efectos innecesarios
  const fullUrl = useMemo(() => {
    const searchParams = new URLSearchParams(params);
    return `${url}?${searchParams.toString()}`;
  }, [url, params]);
  
  // Función memoizada para refetch
  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(fullUrl);
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [fullUrl]);
  
  useEffect(() => {
    refetch();
  }, [refetch]);
  
  return { data, loading, error, refetch };
}
```



## 💻 Ejercicios Prácticos

### Ejercicio 1: Contexto de Tema Global

Crea un sistema de tema global que permita cambiar entre claro/oscuro y se mantenga en localStorage:

```jsx
// Implementa ThemeProvider con:
// - Estado de tema (light/dark)
// - Función para cambiar tema
// - Persistencia en localStorage
// - Aplicación automática de clases CSS

function ThemeProvider({ children }) {
  // Tu implementación aquí
}

function useTheme() {
  // Tu implementación aquí
}

// Úsalo en una aplicación completa
```

### Ejercicio 2: Carrito de Compras con useReducer

Implementa un carrito de compras completo usando useReducer:

```jsx
// Acciones requeridas:
// - ADD_ITEM
// - REMOVE_ITEM  
// - UPDATE_QUANTITY
// - APPLY_COUPON
// - CLEAR_CART

const initialState = {
  items: [],
  total: 0,
  coupon: null,
  discount: 0
};

function cartReducer(state, action) {
  // Tu implementación aquí
}
```

### Ejercicio 3: Buscador Optimizado

Crea un componente de búsqueda que use useMemo y useCallback para optimizar el rendimiento:

```jsx
// Características requeridas:
// - Búsqueda en tiempo real con debounce
// - Filtros múltiples (categoría, precio, rating)
// - Ordenamiento
// - Estadísticas calculadas
// - Componentes hijos optimizados con React.memo
```



## 🎯 Mejores Prácticas

### useContext
✅ **Hacer:**

- Crear custom hooks para cada contexto
- Separar contextos por responsabilidad
- Validar que el contexto existe antes de usarlo

❌ **Evitar:**

- Poner demasiados valores en un solo contexto
- Usar contexto para estado que cambia frecuentemente
- Anidar muchos providers

### useReducer
✅ **Hacer:**

- Usar para estado complejo con múltiples acciones
- Tipos de acción como constantes
- Validar acciones en el reducer

❌ **Evitar:**

- Usar para estado simple
- Mutar el estado directamente
- Lógica compleja fuera del reducer

### useMemo
✅ **Hacer:**

- Solo para cálculos realmente costosos
- Incluir todas las dependencias
- Medir el rendimiento antes y después

❌ **Evitar:**

- Optimización prematura
- Cálculos simples
- Dependencias que siempre cambian

### useCallback
✅ **Hacer:**

- Funciones pasadas a componentes hijos memoizados
- Funciones con dependencias específicas
- Combinar con React.memo

❌ **Evitar:**

- Todas las funciones por defecto
- Funciones sin dependencias complejas
- Cuando los hijos no están memoizados



## 🔄 Resumen

### Cuándo usar cada Hook:

- **useContext**: Compartir estado global, evitar prop drilling
- **useReducer**: Estado complejo con múltiples acciones relacionadas  
- **useMemo**: Cálculos costosos que no quieres repetir
- **useCallback**: Funciones pasadas a componentes hijos memoizados

### Orden de optimización:

1. **Primero**: Escribe código que funcione
2. **Segundo**: Identifica problemas de rendimiento reales
3. **Tercero**: Aplica optimizaciones específicas
4. **Cuarto**: Mide el impacto de las optimizaciones

### Regla de oro:
> "Haz que funcione, luego haz que sea rápido, pero solo si realmente lo necesitas"



## 🏁 Próximos Pasos

En el siguiente módulo aprenderemos:

- **React Router** para navegación entre páginas
- **Custom Hooks avanzados** para lógica reutilizable  
- **Testing** de componentes y hooks
- **Patrones avanzados** de composición
- **Performance profiling** con React DevTools

## ❓ Preguntas Frecuentes

**P: ¿Debo usar useContext para todo el estado global?**
R: No, solo para estado que necesitan muchos componentes. Para estado complejo, considera bibliotecas como Redux o Zustand.

**P: ¿Cuál es la diferencia entre useMemo y useCallback?**
R: `useMemo` memoriza valores/objetos, `useCallback` memoriza funciones. `useCallback(fn, deps)` es equivalente a `useMemo(() => fn, deps)`.

**P: ¿useReducer es mejor que useState?**
R: Depende. `useReducer` es mejor para estado complejo con múltiples acciones relacionadas. `useState` es más simple para estado básico.

**P: ¿Cómo sé si necesito optimizar con useMemo/useCallback?**
R: Usa React DevTools Profiler para identificar componentes que se re-renderizan frecuentemente sin necesidad.

**P: ¿Puedo usar múltiples contextos?**
R: Sí, es una buena práctica separar contextos por responsabilidad (ej: AuthContext, ThemeContext, etc.).