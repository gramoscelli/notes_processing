# 🔗 Tests de Integración con React, Vitest y RTL

## 1. Qué son los tests de integración

En el apartado anterior trabajamos principalmente con **tests unitarios** de componentes (cada test verificaba un componente o una función aislada).
Los **tests de integración** se enfocan en comprobar que **varios componentes, hooks y servicios colaboren correctamente** para cumplir un flujo funcional más amplio.

En React, un test de integración puede incluir:

* Varias piezas de UI que interactúan entre sí.
* Comunicación con un **contexto global** (ej. `React.Context`).
* Uso de un **estado global** como Redux/Zustand o una API simulada.
* Interacción con **routing** (React Router) o **efectos secundarios**.

El objetivo es verificar que las piezas se integran bien sin llegar a ejecutar la aplicación completa en un navegador real (eso sería E2E).



## 2. Herramientas necesarias

Además de **Vitest** y **React Testing Library** ya configuradas:

* **msw (Mock Service Worker)**: para simular llamadas HTTP reales durante los tests sin necesidad de un servidor.
* **React Router** (opcional): si quieres probar flujos de navegación.

Instala `msw` si vas a testear componentes que consumen APIs:

```bash
npm install --save-dev msw
```



## 3. Caso práctico: ToDo App con API y contexto

Vamos a extender la ToDo App del apunte anterior para que:

1. Obtenga tareas iniciales desde una API.
2. Use un **Contexto** para compartir el estado entre componentes.
3. Permita agregar nuevas tareas que se envían a la API.

### 3.1 Creando el contexto

```tsx
// src/TodoContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

type Task = { id: number; text: string; done: boolean };
type TodoContextType = {
  tasks: Task[];
  addTask: (text: string) => void;
  toggleTask: (id: number) => void;
};

const TodoContext = createContext<TodoContextType | undefined>(undefined);

export function TodoProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);

  const addTask = (text: string) => {
    setTasks([...tasks, { id: Date.now(), text, done: false }]);
  };

  const toggleTask = (id: number) => {
    setTasks(tasks.map(t => (t.id === id ? { ...t, done: !t.done } : t)));
  };

  return (
    <TodoContext.Provider value={{ tasks, addTask, toggleTask }}>
      {children}
    </TodoContext.Provider>
  );
}

export function useTodos() {
  const ctx = useContext(TodoContext);
  if (!ctx) throw new Error('useTodos debe usarse dentro de TodoProvider');
  return ctx;
}
```



### 3.2 Componente principal que consume API

```tsx
// src/TodoApp.tsx
import { useEffect } from 'react';
import { useTodos } from './TodoContext';

export default function TodoApp() {
  const { tasks, addTask, toggleTask } = useTodos();

  useEffect(() => {
    // Simulación de fetch inicial
    fetch('/api/tasks')
      .then(res => res.json())
      .then(data => {
        data.forEach((t: { text: string }) => addTask(t.text));
      });
  }, [addTask]);

  return (
    <div>
      {tasks.length === 0 && <p>No hay tareas</p>}
      <ul>
        {tasks.map(t => (
          <li
            key={t.id}
            onClick={() => toggleTask(t.id)}
            style={{ textDecoration: t.done ? 'line-through' : 'none' }}
          >
            {t.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
```



### 3.3 Configuración de `msw` para mockear la API

```ts
// src/test/mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/tasks', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([{ text: 'Aprender React' }, { text: 'Configurar Vitest' }])
    );
  }),
];
```

```ts
// src/test/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

En `src/setupTests.ts` agrega:

```ts
import { server } from './test/mocks/server';
import '@testing-library/jest-dom';

// Inicia MSW antes de las pruebas
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```



### 3.4 Test de integración

```tsx
// src/test/TodoIntegration.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { TodoProvider } from '../TodoContext';
import TodoApp from '../TodoApp';

describe('TodoApp integración', () => {
  test('carga tareas desde la API y permite interactuar', async () => {
    render(
      <TodoProvider>
        <TodoApp />
      </TodoProvider>
    );

    // Espera que las tareas iniciales aparezcan
    await waitFor(() => {
      expect(screen.getByText('Aprender React')).toBeInTheDocument();
      expect(screen.getByText('Configurar Vitest')).toBeInTheDocument();
    });

    // Simulamos click para completar tarea
    const task = screen.getByText('Aprender React');
    task.click();
    expect(task).toHaveStyle({ textDecoration: 'line-through' });
  });
});
```



## 4. Buenas prácticas para tests de integración

* **Usar MSW** para simular APIs reales en lugar de mockear `fetch` manualmente.
* Mantén **el renderizado cercano a la experiencia real del usuario**: envolver el componente con `TodoProvider`, `Router`, etc.
* No abuses de los tests de integración: úsalos para validar flujos clave, mientras la lógica interna se cubre con tests unitarios.
* Mantén los tests rápidos; evita esperas innecesarias con `waitFor`.



## 5. Próximos pasos

Una vez dominados los tests de integración, el siguiente nivel son los **tests end-to-end (E2E)** con herramientas como **Cypress** o **Playwright**, donde pruebas la aplicación completa corriendo en un navegador real.



¿Quieres que genere este nuevo apunte como un archivo editable (por ejemplo, en formato **Markdown** listo para descargar como `.md`), para que puedas unirlo con tu documento original?
