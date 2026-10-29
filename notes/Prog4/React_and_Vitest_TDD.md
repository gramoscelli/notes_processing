# 🧪 TDD con React + Vite + TypeScript usando **Vitest**

## 1. Introducción

En el backend ya trabajamos con **Jest** para aplicar **TDD**:

1. Escribimos un test que falla.
2. Implementamos el código mínimo para hacerlo pasar.
3. Refactorizamos manteniendo todos los tests verdes.

En el frontend con **React** el proceso es el mismo.
La diferencia es que ahora probaremos **componentes de UI y hooks**, además de funciones puras.



## 2. Por qué Vitest

Vitest es un framework de testing moderno creado por el equipo de Vite.
Ventajas:

* Funciona de forma nativa con Vite y **ESM**, sin configuraciones complejas.
* Es compatible con gran parte de la API de Jest (describe, it/test, expect).
* Permite usar `@testing-library/react` sin configuraciones extra.
* Corre muy rápido gracias a Vite + ESBuild.



## 3. Stack de pruebas recomendado

* **Vitest** → motor de pruebas.
* **React Testing Library (RTL)** → para testear la UI como lo haría un usuario.
* **@testing-library/user-event** → para simular clicks, tipeos, etc.
* **@testing-library/jest-dom** → matchers como `toBeInTheDocument`, `toHaveStyle`, etc.



## 4. Configuración del proyecto

```bash
# 1. Crear proyecto React + TS con Vite
npm create vite@latest react-tdd-vitest -- --template react-ts
cd react-tdd-vitest

# 2. Instalar dependencias de test
npm install --save-dev vitest @testing-library/react \
  @testing-library/user-event @testing-library/jest-dom
```

### Configurar Vitest

Edita `vite.config.ts` para agregar la configuración de test:

```ts
/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
  },
})
```

Crea `src/setupTests.ts`:

```ts
import '@testing-library/jest-dom';
```

Agrega el script en `package.json`:

```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "test": "vitest",
  "test:ui": "vitest --ui"
}
```

> `vitest --ui` abre una interfaz gráfica para ver tests correr en el navegador.



## 5. Ejemplo integrador: **Lista de tareas (ToDo)**

Queremos construir una pequeña app de tareas para practicar **TDD**.

### Especificación

* Mostrar mensaje si no hay tareas.
* Agregar nuevas tareas con un input y botón.
* Marcar tareas como completadas al hacer click.



### 5.1 Test inicial: lista vacía

`src/TodoApp.test.tsx`

```tsx
import { render, screen } from '@testing-library/react';
import TodoApp from './TodoApp';

test('muestra mensaje cuando no hay tareas', () => {
  render(<TodoApp />);
  expect(screen.getByText(/no hay tareas/i)).toBeInTheDocument();
});
```



### 5.2 Implementación mínima

`src/TodoApp.tsx`

```tsx
import { useState } from 'react';

export default function TodoApp() {
  const [tasks] = useState<string[]>([]);

  if (tasks.length === 0) {
    return <p>No hay tareas</p>;
  }

  return <ul>{tasks.map((t, i) => <li key={i}>{t}</li>)}</ul>;
}
```

Ejecuta el test:

```bash
npm run test
```

Debería pasar ✅.



### 5.3 Test: agregar tareas

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TodoApp from './TodoApp';

test('permite agregar una tarea', async () => {
  render(<TodoApp />);
  const input = screen.getByPlaceholderText(/nueva tarea/i);
  const button = screen.getByRole('button', { name: /agregar/i });

  await userEvent.type(input, 'Comprar leche');
  await userEvent.click(button);

  expect(screen.getByText('Comprar leche')).toBeInTheDocument();
});
```



### 5.4 Implementación

```tsx
import { useState } from 'react';

export default function TodoApp() {
  const [tasks, setTasks] = useState<string[]>([]);
  const [text, setText] = useState('');

  const addTask = () => {
    if (text.trim() !== '') {
      setTasks([...tasks, text]);
      setText('');
    }
  };

  return (
    <div>
      {tasks.length === 0 && <p>No hay tareas</p>}
      <input
        placeholder="Nueva tarea"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={addTask}>Agregar</button>

      <ul>
        {tasks.map((t, i) => (
          <li key={i}>{t}</li>
        ))}
      </ul>
    </div>
  );
}
```



### 5.5 Test: marcar como completada

```tsx
test('permite marcar una tarea como completada', async () => {
  render(<TodoApp />);
  const input = screen.getByPlaceholderText(/nueva tarea/i);
  const button = screen.getByRole('button', { name: /agregar/i });

  await userEvent.type(input, 'Estudiar React');
  await userEvent.click(button);

  const task = screen.getByText('Estudiar React');
  await userEvent.click(task);

  expect(task).toHaveStyle({ textDecoration: 'line-through' });
});
```



### 5.6 Implementación

```tsx
import { useState } from 'react';

type Task = { text: string; done: boolean };

export default function TodoApp() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [text, setText] = useState('');

  const addTask = () => {
    if (text.trim()) {
      setTasks([...tasks, { text, done: false }]);
      setText('');
    }
  };

  const toggleTask = (index: number) => {
    setTasks(tasks.map((t, i) =>
      i === index ? { ...t, done: !t.done } : t
    ));
  };

  return (
    <div>
      {tasks.length === 0 && <p>No hay tareas</p>}
      <input
        placeholder="Nueva tarea"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={addTask}>Agregar</button>

      <ul>
        {tasks.map((t, i) => (
          <li
            key={i}
            onClick={() => toggleTask(i)}
            style={{
              textDecoration: t.done ? 'line-through' : 'none',
              cursor: 'pointer'
            }}
          >
            {t.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
```



## 6. Buenas prácticas

* Mantener tests **rápidos y aislados**.
* Testear **lo que ve el usuario**, no la implementación interna.
* Usar queries accesibles: `getByRole`, `getByText`, `getByPlaceholderText`.
* Ejecutar `vitest --ui` para ver resultados interactivos.
* Para flujos completos o pruebas cross-browser usar Cypress/Playwright.



## 7. Recursos recomendados

* [Vitest Docs](https://vitest.dev/)
* [React Testing Library Docs](https://testing-library.com/docs/react-testing-library/intro/)
* [@testing-library/user-event](https://testing-library.com/docs/user-event/intro)
* [@testing-library/jest-dom](https://github.com/testing-library/jest-dom)

