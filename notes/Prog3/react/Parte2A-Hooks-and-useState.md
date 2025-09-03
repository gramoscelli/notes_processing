# Parte 2A: Hooks y Estado (useState)
## 🪝 Introducción a los Hooks

### ¿Qué son los Hooks?

Los **Hooks** son funciones especiales que te permiten "engancharte" (hook into) a características de React desde componentes funcionales. Antes de los Hooks, solo las clases podían tener estado y métodos del ciclo de vida.

### ¿Por qué existen los Hooks?

**Problema antes de los Hooks:**
```jsx
// Componente de clase (forma antigua)
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }
  
  increment = () => {
    this.setState({ count: this.state.count + 1 });
  }
  
  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>+</button>
      </div>
    );
  }
}
```

**Solución con Hooks:**
```jsx
// Componente funcional con Hooks (forma moderna)
function Counter() {
  const [count, setCount] = useState(0);
  
  const increment = () => {
    setCount(count + 1);
  };
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
    </div>
  );
}
```

### Ventajas de los Hooks

✅ **Código más simple** - menos ceremonial que las clases  

✅ **Mejor reutilización** - lógica compartible entre componentes  

✅ **Más fácil de testear** - funciones son más fáciles de probar  

✅ **Performance mejorado** - menos overhead que las clases  

✅ **Mejor developer experience** - menos confusión con `this`

### Reglas de los Hooks

⚠️ **Reglas fundamentales que SIEMPRE debes seguir:**

1. **Solo llama Hooks en el nivel superior**
   ```jsx
   // ❌ Incorrecto - dentro de un bucle
   for (let i = 0; i < 3; i++) {
     const [count, setCount] = useState(0);
   }
   
   // ❌ Incorrecto - dentro de una condición
   if (condition) {
     const [name, setName] = useState('');
   }
   
   // ✅ Correcto - nivel superior del componente
   function MyComponent() {
     const [count, setCount] = useState(0);
     const [name, setName] = useState('');
     // ... resto del componente
   }
   ```

2. **Solo llama Hooks desde componentes React o custom hooks**
   ```jsx
   // ❌ Incorrecto - función regular
   function regularFunction() {
     const [state, setState] = useState(0);
   }
   
   // ✅ Correcto - componente React
   function MyComponent() {
     const [state, setState] = useState(0);
   }
   
   // ✅ Correcto - custom hook
   function useMyCustomHook() {
     const [state, setState] = useState(0);
     return [state, setState];
   }
   ```

### Hooks más Comunes

| Hook | Propósito | Ejemplo |
|------|-----------|---------|
| `useState` | Manejar estado local | `const [count, setCount] = useState(0)` |
| `useEffect` | Efectos secundarios | `useEffect(() => { ... }, [])` |
| `useContext` | Consumir contexto | `const value = useContext(MyContext)` |
| `useReducer` | Estado complejo | `const [state, dispatch] = useReducer(reducer, initial)` |
| `useMemo` | Memorización | `const value = useMemo(() => compute(), [deps])` |
| `useCallback` | Memorizar funciones | `const fn = useCallback(() => {}, [deps])` |

## 🏷️ useState - Manejo de Estado

### Estado Dinámico

En la **Parte 1** trabajamos con **datos estáticos**:
```jsx
// Módulo 1: Datos que no cambian
function Welcome() {
  const name = "Juan"; // Siempre será "Juan"
  const count = 0;     // Siempre será 0
  
  return <p>Hola {name}, contador: {count}</p>;
}
```

Ahora usaremos **datos dinámicos**:
```jsx
// Módulo 2: Datos que pueden cambiar
function Welcome() {
  const [name, setName] = useState("Juan");  // Puede cambiar
  const [count, setCount] = useState(0);     // Puede cambiar
  
  return (
    <div>
      <p>Hola {name}, contador: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Incrementar
      </button>
    </div>
  );
}
```

### ¿Qué es el Estado?

El **estado** es información que:

- 📊 **Puede cambiar** durante la vida del componente
- 🔄 **Causa re-renderizado** cuando cambia
- 💾 **Se mantiene** entre renders
- 🎯 **Es local** a cada instancia del componente

### Concepto Básico de useState

`useState` es como darle "memoria" a tu componente:

```jsx
import React, { useState } from 'react';

function Counter() {
  // Declarar una variable de estado llamada "count"
  const [count, setCount] = useState(0);
  //     │        │              │
  //     │        │              └── Valor inicial (0)
  //     │        └── Función para cambiar el valor
  //     └── Variable que contiene el valor actual
  
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

### Comparación: Sin Estado vs Con Estado

```jsx
// ❌ Sin estado - el botón no hace nada visible
function StaticCounter() {
  let count = 0; // Variable normal de JavaScript
  
  const increment = () => {
    count = count + 1; // Cambia la variable...
    console.log(count); // ...pero la interfaz no se actualiza
  };
  
  return (
    <div>
      <p>Count: {count}</p> {/* Siempre mostrará 0 */}
      <button onClick={increment}>+</button>
    </div>
  );
}

// ✅ Con estado - el botón actualiza la interfaz
function DynamicCounter() {
  const [count, setCount] = useState(0); // Estado de React
  
  const increment = () => {
    setCount(count + 1); // Cambia el estado Y actualiza la interfaz
  };
  
  return (
    <div>
      <p>Count: {count}</p> {/* Se actualiza automáticamente */}
      <button onClick={increment}>+</button>
    </div>
  );
}
```
### Diferentes Tipos de Estado

#### Estado Primitivo
```jsx
function PrimitiveStates() {
  const [count, setCount] = useState(0);             // Número
  const [name, setName] = useState('');              // String
  const [isVisible, setIsVisible] = useState(true);  // Boolean
  const [items, setItems] = useState([]);            // Array
  const [user, setUser] = useState(null);            // Objeto o null
  
  return (
    <div>
      <p>Contador: {count}</p>
      <p>Nombre: {name}</p>
      <p>Visible: {isVisible ? 'Sí' : 'No'}</p>
      <p>Items: {items.length}</p>
      <p>Usuario: {user ? user.name : 'No logueado'}</p>
    </div>
  );
}
```

#### Estado de Objeto
```jsx
function ObjectState() {
  const [user, setUser] = useState({
    name: '',
    email: '',
    age: 0
  });
  
  const updateName = (newName) => {
    setUser(prevUser => ({
      ...prevUser,        // Mantener propiedades existentes
      name: newName       // Actualizar solo la propiedad name
    }));
  };
  
  return (
    <div>
      <input 
        value={user.name}
        onChange={(e) => updateName(e.target.value)}
        placeholder="Nombre"
      />
      <p>Usuario: {user.name}</p>
    </div>
  );
}
```

#### Estado de Array
```jsx
function ArrayState() {
  const [todos, setTodos] = useState([]);
  
  const addTodo = (text) => {
    const newTodo = {
      id: Date.now(),
      text: text,
      completed: false
    };
    setTodos(prevTodos => [...prevTodos, newTodo]);
  };
  
  const removeTodo = (id) => {
    setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
  };
  
  const toggleTodo = (id) => {
    setTodos(prevTodos => 
      prevTodos.map(todo => 
        todo.id === id 
          ? { ...todo, completed: !todo.completed }
          : todo
      )
    );
  };
  
  return (
    <div>
      <button onClick={() => addTodo('Nueva tarea')}>
        Agregar Tarea
      </button>
      {todos.map(todo => (
        <div key={todo.id}>
          <span>{todo.text}</span>
          <button onClick={() => toggleTodo(todo.id)}>
            {todo.completed ? 'Desmarcar' : 'Marcar'}
          </button>
          <button onClick={() => removeTodo(todo.id)}>
            Eliminar
          </button>
        </div>
      ))}
    </div>
  );
}
```

### Actualizaciones de Estado son Asíncronas

⚠️ **Concepto crucial:** Las actualizaciones de estado NO ocurren inmediatamente.

```jsx
function AsyncStateDemo() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    console.log('🔍 Antes de setCount:', count);     // 0
    setCount(count + 1);
    console.log('🔍 Después de setCount:', count);   // Sigue siendo 0!
    
    // ❌ Esto NO funcionará como esperas
    setCount(count + 1); // count sigue siendo 0, así que será 0 + 1 = 1
    setCount(count + 1); // count sigue siendo 0, así que será 0 + 1 = 1
    setCount(count + 1); // count sigue siendo 0, así que será 0 + 1 = 1
    // Resultado final: count = 1 (no 3!)
  };
  
  // La actualización ocurrirá en el próximo render
  console.log('🎨 Durante render:', count);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={handleClick}>¿+3?</button>
    </div>
  );
}
```
**¿Por qué el Estado es Asíncrono?**

***El problema principal:*** Cuando llamas a `setCount(count + 1)` múltiples veces seguidas, la variable `count` ***no se actualiza inmediatamente***. Mantiene el mismo valor durante toda la ejecución de la función.

**Lo que realmente ocurre:**

1. ***React toma una "fotografía"*** del estado actual cuando la función se ejecuta
2. ***Todas las llamadas a*** `setCount` usan esa misma "fotografía" del valor original
3. ***React agrupa las actualizaciones*** y solo aplica la última al final
4. ***El componente se re-renderiza*** una sola vez con el nuevo valor

En términos simples, si `count` es 0 y llamas `setCount(count + 1)` cuatro veces, React ve cuatro instrucciones de "cambiar a 1" (no "cambiar a 1, luego a 2, luego a 3, luego a 4"). Por eso el resultado final es 1, no 4.

***La razón técnica:*** React optimiza el rendimiento agrupando múltiples actualizaciones de estado en una sola re-renderización. Esto evita renders innecesarios y mejora la performance, pero significa que el estado no se actualiza sincrónicamente dentro de la misma función.

**✅ Forma correcta para múltiples actualizaciones:**
```jsx
function CorrectMultipleUpdates() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    // Usar función que recibe el valor anterior
    setCount(prev => prev + 1);  // prev = 0, nuevo valor = 1
    setCount(prev => prev + 1);  // prev = 1, nuevo valor = 2  
    setCount(prev => prev + 1);  // prev = 2, nuevo valor = 3
    // Resultado final: count = 3 ✅
  };
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={handleClick}>+3</button>
    </div>
  );
}
```
**¿Por qué funciona usar una función en setCount?**
Por que cuando pasas una **función** a `setCount` en lugar de un valor directo, React ejecuta esa función **en secuencia** para cada actualización, pasándole siempre el **valor más reciente** como parámetro.

***La diferencia clave:*** En lugar de usar la "fotografía" del estado original, cada función recibe el **valor actualizado** de la llamada anterior.

***¿Por qué React hace esto?*** Las funciones de actualización le dicen a React "toma el valor más reciente y aplica esta transformación", mientras que pasar un valor directo le dice "cambia al valor X", sin importar qué otras actualizaciones hayan ocurrido.

***Resultado final:*** El contador efectivamente se incrementa 3 veces, mostrando `count = 3` en lugar de `count = 1`.
