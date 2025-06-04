# Uso de localStorage en React

## ✅ ¿Qué es localStorage?

`localStorage` es una API del navegador que permite **guardar datos en pares clave-valor como texto**, y esos datos **persisten** aunque el usuario recargue la página o cierre el navegador.

### Métodos principales:
```js
localStorage.setItem('clave', 'valor');      // Guardar
localStorage.getItem('clave');               // Leer
localStorage.removeItem('clave');            // Eliminar clave específica
localStorage.clear();                        // Eliminar todo el almacenamiento
```

## ✅ Cómo usarlo en React

Aunque `localStorage` es independiente de React, lo usamos en combinación con los hooks `useState` y `useEffect` para integrarlo de forma reactiva.

### Ejemplo: guardar el nombre del usuario
```jsx
import { useState, useEffect } from 'react';

function App() {
  const [nombre, setNombre] = useState('');

  // Cargar desde localStorage al iniciar
  useEffect(() => {
    const nombreGuardado = localStorage.getItem('nombre');
    if (nombreGuardado) {
      setNombre(nombreGuardado);
    }
  }, []);

  // Guardar en localStorage cuando cambia
  useEffect(() => {
    if (nombre) {
      localStorage.setItem('nombre', nombre);
    }
  }, [nombre]);

  return (
    <div>
      <input
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        placeholder="Escribe tu nombre"
      />
      <p>Hola, {nombre}!</p>
    </div>
  );
}
```

---

## ✅ Custom Hook: `useLocalStorage`

Para reutilizar fácilmente la lógica de lectura y escritura en `localStorage`, podemos crear un hook personalizado:

```jsx
import { useState, useEffect } from 'react';

function useLocalStorage(key, valorInicial) {
  const [valor, setValor] = useState(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : valorInicial;
    } catch (error) {
      console.error('Error leyendo localStorage', error);
      return valorInicial;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(valor));
    } catch (error) {
      console.error('Error guardando en localStorage', error);
    }
  }, [key, valor]);

  return [valor, setValor];
}
```

### Ejemplo usando el custom hook

```jsx
function AppConHook() {
  const [nombre, setNombre] = useLocalStorage('nombre', '');

  return (
    <div>
      <input
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        placeholder="Tu nombre"
      />
      <p>Hola, {nombre}!</p>
    </div>
  );
}

export default AppConHook;
```

---

## 🧠 Consejos útiles

- `localStorage` **solo guarda strings**. Si querés guardar objetos, usá `JSON.stringify` y `JSON.parse`.
- No intentes usar `localStorage` en el **servidor** (por ejemplo en Next.js con SSR), ya que solo existe en el navegador.

