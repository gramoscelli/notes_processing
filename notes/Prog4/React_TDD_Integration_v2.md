# 🔗 Tests de Integración con React, Vitest y RTL

## 1. Qué son los tests de integración

En el apartado anterior trabajamos principalmente con **tests unitarios** de componentes (cada test verificaba un componente o una función aislada).
Los **tests de integración** se enfocan en comprobar que **varios componentes, hooks y servicios colaboren correctamente** para cumplir un flujo funcional más amplio.

Imagina que tienes los engranajes de un reloj. Un test unitario probaría que cada engranaje gira correctamente por sí solo. Un test de integración verificaría que, al unir varios engranajes, el mecanismo completo (por ejemplo, el minutero y el horario) funciona como se espera.


En React, un test de integración puede incluir:

*   **Varias piezas de UI que interactúan entre sí:** Por ejemplo, un formulario de entrada que añade elementos a una lista.
*   **Comunicación con un contexto global:** Como `React.Context` para compartir datos o funcionalidades entre componentes.
*   **Uso de un estado global:** Gestionado por librerías como Redux o Zustand.
*   **Simulación de interacción con APIs:** Comprobando que los componentes reaccionan adecuadamente a los datos obtenidos o enviados a un backend simulado.
*   **Interacción con routing:** Asegurando que la navegación entre diferentes rutas o páginas funciona correctamente (si usas librerías como React Router).
*   **Efectos secundarios:** Como llamadas a APIs o manejo de suscripciones.

El objetivo es verificar que las piezas se integran bien sin llegar a ejecutar la aplicación completa en un navegador real (eso sería E2E o End-to-End).

## 2. Herramientas necesarias

Además de **Vitest** y **React Testing Library** ya configuradas, necesitaremos una herramienta clave para simular la capa de red:

*   **msw (Mock Service Worker)**: Esta es una herramienta fantástica para simular llamadas HTTP reales durante los tests sin necesidad de un servidor backend real. A diferencia de `jest.mock('global-fetch')` o similar, `msw` intercepta las solicitudes de red a un nivel más bajo, haciendo que tus tests se sientan mucho más cercanos a cómo la aplicación interactúa con una API real. ¡Es una pieza crucial para tests de integración robustos!
*   **React Router** (opcional): Si vas a probar flujos de navegación complejos, es bueno tenerlo presente.

### ¿Por qué `msw` y no un mock de `fetch`?

Cuando "mockeas" `fetch` o Axios directamente en tus tests, estás reemplazando la implementación de la función en JavaScript. Esto funciona, pero tiene limitaciones:

1.  **Menos realista:** Tu test no está probando la pila de red real de tu aplicación, sino tu mock JavaScript.
2.  **Acoplamiento:** Tienes que mockear `fetch` en cada test o en cada setup, lo que puede ser repetitivo y propenso a errores.
3.  **Comportamiento inconsistente:** Si un componente usa una librería de terceros para hacer peticiones, tu mock de `fetch` no la afectará.

`msw` resuelve esto de forma elegante:

*   **Intercepción a nivel de red:** `msw` utiliza Service Workers (en el navegador) o interceptores de Node.js (en Vitest/Node.js) para interceptar las solicitudes HTTP *antes* de que salgan de tu aplicación.
*   **Transparencia:** Tus componentes y cualquier librería de terceros ven y usan `fetch` o `XMLHttpRequest` de forma normal. `msw` simplemente responde a esas solicitudes con los datos que tú defines, sin que tu código de aplicación sepa que está siendo "mockeado".
*   **Reutilizable:** Defines tus "manejadores" de API una vez y los usas en todos tus tests, lo que reduce la duplicación y mejora la mantenibilidad.

¡Es como tener un servidor backend local que solo existe para tus tests!



Instala `msw` si vas a testear componentes que consumen APIs:

```bash
npm install --save-dev msw
```

## 3. Caso práctico: ToDo App con API y contexto

Vamos a extender la ToDo App del apunte anterior para que:

1.  Obtenga tareas iniciales desde una API.
2.  Use un **Contexto** para compartir el estado entre componentes.
3.  Permita agregar nuevas tareas que se envían a la API (aunque en este ejemplo nos centraremos en la lectura y el toggle).

### 3.1 Creando el contexto (`TodoContext.tsx`)

Escribamos un contexto que gestione las tareas (obtener, añadir, alternar estado `done`). En esta parte conviene repasar el _hook_ `useContext()` visto el [semestre pasado](https://aulavirtual.frbb.utn.edu.ar/mod/page/view.php?id=410652#usecontext-manejo-de-estado-global). El contexto es crucial para nuestros tests de integración, ya que varios componentes podrían depender de él.

```tsx
// src/TodoContext.tsx
import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';

// Tipos para las tareas
type Task = { id: number; text: string; done: boolean };

// Tipos para el contexto (lo que proveemos a los consumidores)
type TodoContextType = {
  tasks: Task[];
  addTask: (text: string) => void;
  toggleTask: (id: number) => void;
  // Añadimos una función para cargar tareas iniciales, útil para el efecto secundario
  loadInitialTasks: (initialTasks: Task[]) => void;
};

// Creamos el contexto. Inicialmente es undefined.
const TodoContext = createContext<TodoContextType | undefined>(undefined);

// El proveedor de contexto, que gestionará el estado y las funciones
export function TodoProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);

  // Función para añadir una tarea
  const addTask = useCallback((text: string) => {
    setTasks(prevTasks => [...prevTasks, { id: Date.now(), text, done: false }]);
  }, []); // useCallback para estabilidad si se pasa como prop

  // Función para alternar el estado 'done' de una tarea
  const toggleTask = useCallback((id: number) => {
    setTasks(prevTasks =>
      prevTasks.map(t => (t.id === id ? { ...t, done: !t.done } : t))
    );
  }, []); // useCallback para estabilidad

  // Función para cargar tareas iniciales, por ejemplo desde una API
  const loadInitialTasks = useCallback((initialTasks: Task[]) => {
    setTasks(initialTasks);
  }, []); // useCallback para estabilidad

  // El valor que se proveerá a los componentes hijos
  const contextValue = { tasks, addTask, toggleTask, loadInitialTasks };

  return (
    <TodoContext.Provider value={contextValue}>
      {children}
    </TodoContext.Provider>
  );
}

// Hook personalizado para consumir el contexto de forma segura
export function useTodos() {
  const ctx = useContext(TodoContext);
  if (!ctx) {
    // Es un error común olvidar envolver el componente con el Provider
    throw new Error('useTodos debe usarse dentro de TodoProvider');
  }
  return ctx;
}
```

**Explicación:**

*   **`TodoContextType`**: Define la forma de los datos que el contexto compartirá.
*   **`createContext`**: Crea el objeto Contexto.
*   **`TodoProvider`**: Este componente es el "envoltorio". Mantiene el estado `tasks` y las funciones `addTask`, `toggleTask`, `loadInitialTasks`. Todo componente dentro de `TodoProvider` tendrá acceso a estos valores.
*   **`useTodos`**: Un hook personalizado que simplifica el consumo del contexto y añade una comprobación para asegurar que el componente que lo usa está dentro de un `TodoProvider`.

### 3.2 Componente principal que consume API (`TodoApp.tsx`)

Este componente usará el contexto para mostrar y manipular las tareas. También realizará una llamada inicial a una API simulada.

```tsx
// src/TodoApp.tsx
import { useEffect } from 'react';
import { useTodos } from './TodoContext';

// Este componente mostrará la lista de tareas y manejará la carga inicial
export default function TodoApp() {
  const { tasks, addTask, toggleTask, loadInitialTasks } = useTodos();

  useEffect(() => {
    // Simulación de fetch inicial para obtener tareas
    fetch('/api/tasks')
      .then(res => {
        if (!res.ok) { // Manejo básico de errores de red
          throw new Error('Error al cargar las tareas');
        }
        return res.json();
      })
      .then((data: { id: number; text: string; done: boolean }[]) => {
        // En lugar de addTask individualmente, cargamos todas las tareas de golpe
        loadInitialTasks(data);
      })
      .catch(error => {
        console.error("Hubo un error al obtener las tareas:", error);
        // Aquí podríamos establecer un estado de error en el contexto o en el componente
      });
  }, [loadInitialTasks]); // Dependencia del efecto: loadInitialTasks del contexto

  return (
    <div>
      <h1>Mis Tareas</h1>
      {tasks.length === 0 && <p>No hay tareas</p>}
      <ul>
        {tasks.map(t => (
          <li
            key={t.id}
            onClick={() => toggleTask(t.id)}
            style={{
              textDecoration: t.done ? 'line-through' : 'none',
              cursor: 'pointer', // Indicamos que es clickable
              marginBottom: '5px'
            }}
          >
            {t.text} {t.done ? '(Completada)' : ''}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**Cambios y Explicación:**

*   Hemos añadido `loadInitialTasks` al contexto para una carga más limpia de las tareas iniciales.
*   El `useEffect` ahora usa `fetch` para `'/api/tasks'`. Este es el punto clave donde `msw` interceptará la petición.
*   Se ha añadido un `catch` para manejar errores básicos de la petición.
*   Mejoras estéticas y de accesibilidad al `li` para indicar que es interactivo.

### 3.3 Configuración de `msw` para mockear la API

Ahora, vamos a configurar `msw` para que cada vez que `TodoApp` intente hacer un `fetch` a `'/api/tasks'`, `msw` intercepte esa llamada y devuelva nuestros datos "mockeados" en lugar de intentar ir a un servidor real.

```ts
// src/test/mocks/handlers.ts
import { rest } from 'msw';

// Definimos los manejadores de las peticiones que queremos interceptar
export const handlers = [
  // Intercepta peticiones GET a '/api/tasks'
  rest.get('/api/tasks', (req, res, ctx) => {
    // req: contiene información sobre la petición entrante
    // res: función para construir la respuesta mockeada
    // ctx: utilidades para la respuesta (status, json, delay, etc.)
    return res(
      ctx.status(200), // Estado HTTP 200 (OK)
      ctx.json([ // Cuerpo de la respuesta en formato JSON
        { id: 1, text: 'Aprender React', done: false },
        { id: 2, text: 'Configurar Vitest', done: true }, // Una tarea completada
        { id: 3, text: 'Integrar con MSW', done: false },
      ]),
      ctx.delay(150) // Simula un pequeño retardo de red (opcional, para realismo)
    );
  }),
  // Podrías añadir más manejadores para POST, PUT, DELETE, etc.
  // Ejemplo: Interceptar POST para añadir tareas
  // rest.post('/api/tasks', (req, res, ctx) => {
  //   const newTask = req.body; // El cuerpo de la petición POST
  //   console.log('Nueva tarea recibida en el mock:', newTask);
  //   return res(
  //     ctx.status(201), // Estado 201 (Created)
  //     ctx.json({ id: Date.now(), ...newTask })
  //   );
  // }),
];
```

```ts
// src/test/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Configura el servidor de MSW con nuestros manejadores definidos
export const server = setupServer(...handlers);
```

**Explicación:**

*   **`handlers.ts`**: Aquí definimos las "reglas" para interceptar peticiones.
    *   `rest.get('/api/tasks', ...)`: Le dice a `msw` que, si se hace una petición GET a `/api/tasks`, la intercepte.
    *   `res(ctx.status(200), ctx.json([...]), ctx.delay(150))`: Define la respuesta que `msw` debe devolver. En este caso, un status 200, un JSON con tres tareas (una ya completada) y un pequeño retraso para simular una red real.
*   **`server.ts`**: Inicializa `msw` con los manejadores definidos.

Finalmente, necesitamos integrar `msw` en el ciclo de vida de nuestras pruebas en Vitest. Esto se hace en el archivo de configuración global de Vitest, `src/setupTests.ts` (o donde tengas configurado `setupFiles`).

```ts
// src/setupTests.ts
import { server } from './test/mocks/server';
import '@testing-library/jest-dom'; // Para los matchers extendidos de RTL

// **Ciclo de vida de MSW en Vitest:**

// 1. Antes de todas las pruebas (una vez por ejecución de test suite):
beforeAll(() => {
  server.listen(); // Inicia el servidor de MSW
  // Esto permite que MSW intercepte las peticiones HTTP desde el inicio.
  console.log('MSW server started');
});

// 2. Después de cada prueba individual:
afterEach(() => {
  server.resetHandlers(); // Resetea los manejadores de MSW
  // Esto asegura que cada prueba es independiente; si una prueba cambia los manejadores,
  // se restauran a su estado original para la siguiente prueba.
});

// 3. Después de todas las pruebas (una vez por ejecución de test suite):
afterAll(() => {
  server.close(); // Cierra el servidor de MSW
  // Libera los recursos de red utilizados por MSW.
  console.log('MSW server closed');
});
```

**Explicación del `setupTests.ts`:**

*   `beforeAll(() => server.listen())`: Antes de que se ejecute *cualquier* test, `msw` empieza a escuchar las peticiones de red.
*   `afterEach(() => server.resetHandlers())`: Después de *cada* test, `msw` resetea sus manejadores. Esto es crucial para la aislación de tests. Si un test modifica el comportamiento de una API, este reset asegura que el siguiente test empiece con los manejadores originales definidos en `handlers.ts`.
*   `afterAll(() => server.close())`: Después de que *todos* los tests han terminado, `msw` se detiene y libera los recursos.

### 3.4 Test de integración (`src/test/TodoIntegration.test.tsx`)

Ahora que tenemos el contexto, el componente y `msw` configurados, podemos escribir nuestro test de integración para verificar que todo funciona en conjunto.

```tsx
// src/test/TodoIntegration.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event'; // Para simular interacciones de usuario
import { TodoProvider } from '../TodoContext';
import TodoApp from '../TodoApp';

// userEvent es útil para simular interacciones más realistas
const user = userEvent.setup();

describe('TodoApp integración con API simulada y Contexto', () => {
  test('carga tareas desde la API y permite interactuar con ellas', async () => {
    // 1. Renderizamos el componente principal dentro de su contexto
    // Esto simula cómo se usaría en la aplicación real
    render(
      <TodoProvider>
        <TodoApp />
      </TodoProvider>
    );

    // 2. Esperamos que las tareas iniciales (mockeadas por MSW) aparezcan en la pantalla
    // `waitFor` es clave para esperar por operaciones asíncronas (como la llamada a la API)
    await waitFor(() => {
      expect(screen.getByText('Aprender React')).toBeInTheDocument();
      expect(screen.getByText('Configurar Vitest')).toBeInTheDocument();
      expect(screen.getByText('Integrar con MSW')).toBeInTheDocument();
    }, { timeout: 3000 }); // Opcional: aumentar el timeout si el delay de MSW es alto

    // Verificamos que 'Configurar Vitest' ya aparece como completada desde el mock
    const configuredTask = screen.getByText('Configurar Vitest', { exact: false });
    expect(configuredTask).toHaveStyle({ textDecoration: 'line-through' });
    expect(configuredTask).toHaveTextContent('(Completada)');

    // 3. Simulamos una interacción de usuario: hacemos click para completar una tarea
    const learnReactTask = screen.getByText('Aprender React');
    await user.click(learnReactTask); // Usamos userEvent para un click más realista

    // 4. Verificamos que la UI se actualiza correctamente tras la interacción
    // El contexto debe haber manejado el cambio de estado y el componente re-renderizado
    expect(learnReactTask).toHaveStyle({ textDecoration: 'line-through' });
    expect(learnReactTask).toHaveTextContent('(Completada)');

    // 5. Verificamos que al hacer click de nuevo, la tarea se descompleta
    await user.click(learnReactTask);
    expect(learnReactTask).not.toHaveStyle({ textDecoration: 'line-through' });
    expect(learnReactTask).not.toHaveTextContent('(Completada)');
  });

  test('muestra "No hay tareas" si la API devuelve una lista vacía', async () => {
    // Sobreescribir el manejador de MSW solo para este test
    // Esto demuestra cómo `server.resetHandlers()` es útil y cómo puedes adaptar mocks
    server.use(
      rest.get('/api/tasks', (req, res, ctx) => {
        return res(ctx.status(200), ctx.json([])); // Devuelve un array vacío
      })
    );

    render(
      <TodoProvider>
        <TodoApp />
      </TodoProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('No hay tareas')).toBeInTheDocument();
    });

    // Asegurarse de que no aparecen tareas que no deberían
    expect(screen.queryByText('Aprender React')).not.toBeInTheDocument();
  });
});
```

**Explicación del Test:**

*   **`render(<TodoProvider><TodoApp /></TodoProvider>)`**: Es fundamental renderizar `TodoApp` dentro de `TodoProvider`, porque `TodoApp` usa el hook `useTodos` y necesita el contexto para funcionar. Esto hace que el test sea una "integración" real.
*   **`await waitFor(...)`**: Dado que la llamada a la API es asíncrona (incluso si es mockeada), necesitamos `waitFor` para esperar a que los elementos aparezcan en el DOM. Si no usáramos `waitFor`, el test podría fallar porque `screen.getByText` se ejecutaría antes de que la respuesta de `msw` haya sido procesada y el componente re-renderizado.
*   **`userEvent.setup()` y `user.click()`**: `userEvent` proporciona una forma más robusta y realista de simular interacciones del usuario (clicks, escribir en inputs, etc.) en comparación con los métodos básicos como `element.click()`. Imita mejor el comportamiento del navegador.
*   **`toHaveStyle({ textDecoration: 'line-through' })`**: Verificamos los estilos CSS para confirmar que la tarea se marcó visualmente como completada.
*   **`server.use(...)`**: Demuestra una buena práctica. Si necesitas un comportamiento de API diferente para un test específico (por ejemplo, una lista vacía), puedes sobrescribir temporalmente un manejador de `msw` usando `server.use()`. Gracias a `afterEach(() => server.resetHandlers())` en `setupTests.ts`, este cambio solo afectará al test actual y el manejador original se restaurará para el siguiente test.
*   **`screen.queryByText`**: Usado para afirmar que un elemento *no* está presente en el documento, ya que `getByText` lanzaría un error si no lo encuentra.

## 4. Buenas prácticas para tests de integración

*   **Usar MSW (Mock Service Worker)**: Como hemos visto, es la mejor manera de simular APIs reales de forma transparente y realista. ¡Evita mockear `fetch` o Axios manualmente si puedes usar MSW!
*   **Mantén el renderizado cercano a la experiencia real del usuario**: Siempre que sea posible, envuelve el componente que estás testeando con los Providers (Context, Redux, Router, etc.) que usaría en la aplicación real. Esto asegura que la integración de estos "bloques de construcción" fundamentales se pruebe adecuadamente.
*   **No abuses de los tests de integración**: Son más lentos y complejos que los unitarios. Úsalos para validar flujos clave de la aplicación (ej. "el usuario puede iniciar sesión", "el usuario puede añadir un ítem al carrito y este aparece"), mientras que la lógica interna y los componentes individuales se cubren con tests unitarios. Piensa en la "pirámide de tests" (muchos unitarios, menos de integración, pocos E2E).
*   **Mantén los tests rápidos**: Evita esperas innecesarias. Usa `waitFor` solo cuando sea estrictamente necesario para esperar a que se resuelvan operaciones asíncronas.
*   **Enfócate en el comportamiento del usuario**: `React Testing Library` te anima a interactuar con los elementos de la misma manera que lo haría un usuario (buscar por texto visible, labels de formularios, roles ARIA) en lugar de buscar por nombres de clases o IDs internos. Esto hace que tus tests sean más robustos a cambios de implementación.
*   **Aísla los tests**: Usa `afterEach` para limpiar cualquier estado o mock (como `server.resetHandlers()` de `msw`) para asegurar que cada test sea independiente y su resultado no afecte a otros tests.
