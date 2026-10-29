# Tests End-to-End (E2E) en APIs con Node/TypeScript

## Objetivos

* Entender el alcance de un **test E2E** y sus diferencias con unit/integración.
* Aprender a configurar **Playwright Test** para correr tests contra un servidor real.
* Diseñar estrategias de **reset y seed** de datos para garantizar reproducibilidad.
* Generar **reportes y trazas** para depuración en local y CI.



¡Claro! Aquí tienes una explicación más detallada de qué es un test E2E (End-to-End), con ejemplos para clarificar cada punto:

### 1. ¿Qué es un test E2E (End-to-End)?

Un test E2E es un tipo de prueba de software que verifica la funcionalidad completa de una aplicación desde la perspectiva del usuario final. Simula el flujo de interacción de un usuario a través de la interfaz de la aplicación, interactuando con todos los componentes del sistema involucrados, desde el front-end hasta la base de datos y cualquier servicio externo. El objetivo es asegurar que todos los módulos y sistemas integrados trabajan juntos correctamente para lograr un resultado esperado.

**Recorrido completo: cliente → HTTP → middleware → rutas → servicios → persistencia.**

Imagina una aplicación web. Un test E2E simularía lo siguiente:

*   **Cliente:** Un usuario abre un navegador y navega a tu aplicación (por ejemplo, `www.mi-tienda.com`). El test automatizado interactúa con los elementos visuales (clics en botones, llenado de formularios) como lo haría un usuario real.
*   **HTTP:** Cuando el usuario hace clic en "Comprar", el navegador envía una solicitud HTTP (por ejemplo, `POST /api/ordenes`) a tu servidor. El test verifica que esta solicitud se envía correctamente y que el servidor la recibe.
*   **Middleware:** En el servidor, la solicitud HTTP pasa por varios "middlewares". Esto podría incluir autenticación (¿está el usuario logueado?), validación (¿son válidos los datos del pedido?) o logging. El test E2E asegura que estos pasos intermedios no impidan el flujo.
*   **Rutas:** La solicitud es dirigida a la ruta correcta en tu API (por ejemplo, el controlador `OrdenesController`).
*   **Servicios:** El controlador llama a los servicios de negocio necesarios (por ejemplo, `ServicioDePedidos.crearOrden(datosDelPedido)`). Estos servicios contienen la lógica principal de la aplicación.
*   **Persistencia:** Finalmente, el servicio interactúa con la base de datos (por ejemplo, guarda la nueva orden en la tabla `orders`) para almacenar o recuperar datos.

**Ejemplo:** Un test E2E para una aplicación de e-commerce podría:
1.  Navegar a la página de inicio.
2.  Buscar un producto específico.
3.  Añadir el producto al carrito.
4.  Proceder al checkout.
5.  Introducir los datos de envío y pago.
6.  Confirmar el pedido.
7.  Verificar que se muestra un mensaje de "Pedido exitoso" y que el pedido aparece en el historial de pedidos del usuario.
8.  Opcionalmente, podría verificar que la base de datos refleja la nueva orden y la reducción del stock del producto.

**Valida: wiring real, serialización JSON, códigos de estado, contratos expuestos.**

Los tests E2E son cruciales para validar aspectos que otras pruebas no pueden:

*   **Wiring real (conexiones reales):** Aseguran que todos los componentes (front-end, back-end, base de datos, caché, microservicios, etc.) están correctamente conectados e interactúan entre sí como se espera en un entorno de producción. Un test E2E descubriría si un servicio no puede comunicarse con la base de datos, o si el front-end no puede consumir una API.
    *   **Ejemplo:** Si tu front-end llama a `/api/users` y tu back-end expone `/v1/users`, un test E2E fallaría, indicando un problema en la conexión.
*   **Serialización JSON:** Verifican que los datos se envían y reciben en el formato correcto (generalmente JSON) entre el cliente y el servidor. Un error en la serialización podría significar que el servidor no entiende lo que el cliente envía, o viceversa.
    *   **Ejemplo:** Si el front-end envía un número como string (`"123"`) y el back-end espera un entero (`123`), el test E2E revelaría un error de validación o procesamiento.
*   **Códigos de estado HTTP:** Confirman que el servidor devuelve los códigos de estado HTTP apropiados (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error, etc.) en diferentes escenarios.
    *   **Ejemplo:** Si intentas acceder a un recurso sin autenticarte, el test E2E debería esperar un 401 Unauthorized y fallar si recibe un 200 OK. Si un registro se crea exitosamente, el test esperaría un 201 Created.
*   **Contratos expuestos (APIs):** Confirman que las APIs expuestas por el back-end cumplen con el "contrato" esperado por el front-end u otros consumidores. Esto incluye los nombres de los endpoints, los parámetros esperados y la estructura de la respuesta.
    *   **Ejemplo:** Si la API de productos solía devolver `{"id": 1, "nombre": "Producto A"}` y ahora devuelve `{"productId": 1, "productName": "Producto A"}`, un test E2E fallaría porque el front-end no encontraría las claves esperadas, incluso si la API sigue funcionando "internamente".

**No valida: ramas internas detalladas (eso es de unit/integración).**

Los tests E2E son como "cajas negras": les interesa el resultado final, no cómo se llegó a él internamente. No están diseñados para probar:

*   **Lógica de negocio compleja dentro de una función:** Si tienes una función que calcula descuentos con múltiples condiciones, un test E2E no la probará a fondo. Eso es trabajo de un test unitario o de integración.
*   **Casos borde específicos de algoritmos:** Un test E2E no explorará cada posible combinación de entradas para una función matemática.
*   **Ramas de código poco probables:** Se centran en los flujos principales. Si hay una rama de código que solo se activa bajo condiciones muy raras o específicas de configuración, es mejor probarla con tests unitarios.

**Ejemplo:** Si un servicio calcula un impuesto basado en la región del usuario, un test E2E se limitará a verificar que el precio final mostrado es correcto para un par de regiones. No probará cada combinación de impuesto y tipo de producto. Para eso, se usarían tests unitarios que prueben el `ServicioDeImpuestos.calcular(monto, region, tipoProducto)`.

**Costo: más lentos y frágiles → mantener pocos, enfocados en happy paths y errores contractuales.**

Los tests E2E tienen desventajas:

*   **Más lentos:** Requieren que toda la aplicación esté levantada y que se realicen operaciones de red y base de datos, lo que los hace significativamente más lentos que los tests unitarios o de integración.
    *   **Impacto:** Un suite de cientos de tests E2E puede tardar minutos o incluso horas en ejecutarse, ralentizando el ciclo de desarrollo.
*   **Más frágiles (flaky):** Son más susceptibles a fallos debido a factores externos o cambios menores. Un pequeño cambio en la interfaz de usuario (cambiar el ID de un botón) puede romper un test E2E, incluso si la funcionalidad subyacente sigue siendo correcta. Dependen de la estabilidad de muchos componentes.
    *   **Impacto:** Los tests "flaky" (que fallan aleatoriamente sin una razón clara) erosionan la confianza del equipo en las pruebas.
*   **Más caros de mantener:** Requieren más tiempo para escribirlos inicialmente y para actualizarlos cuando la aplicación cambia.

**Recomendación:**

*   **Mantener pocos:** No intentes cubrir el 100% de tu código con tests E2E. Es ineficiente.
*   **Enfocados en "happy paths":** Prioriza los flujos principales y exitosos que el usuario seguirá.
    *   **Ejemplo:** Crear cuenta, iniciar sesión, hacer una compra, publicar un comentario.
*   **Errores contractuales:** Prueba escenarios donde los contratos entre componentes podrían romperse.
    *   **Ejemplo:** ¿Qué pasa si intento crear un usuario con un email ya registrado? ¿La API devuelve un error 409 Conflict con el mensaje esperado?
*   **La "pirámide de pruebas"**: Generalmente, se recomienda tener muchos tests unitarios (rápidos, baratos), menos tests de integración y muy pocos tests E2E (lentos, caros). La mayoría de los problemas deben ser detectados por los tests más bajos en la pirámide.


**Visualización de la Pirámide de Pruebas:**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420" width="720" height="420" role="img" aria-labelledby="title desc">
<desc id="desc">Tres niveles apilados: base de tests unitarios, nivel medio de integración y cima de E2E. La base es la más ancha (más cantidad), la cima es la más angosta (menos cantidad y mayor costo).</desc>

  <defs>
    <style>
      .label{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; fill:#0f172a; font-weight:600; }
      .sub{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; fill:#334155; font-size:14px; }
      .hint{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; fill:#475569; font-size:13px; }
      .shadow{ filter:url(#shadow); }
    </style>
    <linearGradient id="gE2E" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#fecaca"/>
      <stop offset="100%" stop-color="#fca5a5"/>
    </linearGradient>
    <linearGradient id="gINT" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#fde68a"/>
      <stop offset="100%" stop-color="#fbbf24"/>
    </linearGradient>
    <linearGradient id="gUNIT" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#bbf7d0"/>
      <stop offset="100%" stop-color="#86efac"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000000" flood-opacity="0.15"/>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L9,3 L0,6 Z" fill="#475569"></path>
    </marker>
  </defs>

  <!-- Guías laterales -->
  <line x1="72" y1="360" x2="648" y2="360" stroke="#e2e8f0" stroke-width="2"/>
  <line x1="360" y1="40" x2="360" y2="360" stroke="#e2e8f0" stroke-width="2" stroke-dasharray="6 6"/>

  <!-- Niveles de la pirámide (de abajo hacia arriba) -->
  <!-- Base: Unitarios -->
  <polygon class="shadow" points="96,360 624,360 560,270 160,270" fill="url(#gUNIT)" stroke="#10b981" stroke-width="2"/>
  <!-- Medio: Integración -->
  <polygon class="shadow" points="160,270 560,270 500,195 220,195" fill="url(#gINT)" stroke="#f59e0b" stroke-width="2"/>
  <!-- Cima: E2E -->
  <polygon class="shadow" points="220,195 500,195 440,130 280,130" fill="url(#gE2E)" stroke="#ef4444" stroke-width="2"/>

  <!-- Etiquetas de cada nivel -->
  <!-- Unitarios -->
  <text x="360" y="320" text-anchor="middle" class="label" font-size="22">Tests unitarios</text>
  <text x="360" y="342" text-anchor="middle" class="sub">Rápidos, baratos, gran cobertura lógica</text>

  <!-- Integración -->
  <text x="360" y="235" text-anchor="middle" class="label" font-size="20">Integración</text>
  <text x="360" y="257" text-anchor="middle" class="sub">Módulos reales juntos, contratos y wiring</text>

  <!-- E2E -->
  <text x="360" y="165" text-anchor="middle" class="label" font-size="20">E2E</text>
  <text x="360" y="187" text-anchor="middle" class="sub">Recorrido completo por el sistema</text>

  <!-- Anotaciones laterales -->


  <text x="200" y="382" text-anchor="end" class="hint">↑ Más costo / fragilidad</text>
  <line x1="88" y1="360" x2="88" y2="130" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>

  
</svg>


```


## 2. Configuración inicial

### Instalación

```bash
npm i -D @playwright/test
```

### Scripts en package.json

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc -p tsconfig.json",
    "start:e2e": "cross-env NODE_ENV=test PORT=4000 node dist/server.js",
    "test:e2e": "playwright test",
    "report:e2e": "playwright show-report"
  }
}
```

### Estructura de carpetas

```
.
├─ src/              # API principal
├─ e2e/              # Tests E2E
│  ├─ api.books.e2e.spec.ts
│  └─ helpers.ts
├─ playwright.config.ts
└─ package.json
```

## 3. `playwright.config.ts`

El archivo `playwright.config.ts` es el corazón de la configuración de tus tests End-to-End (E2E) con Playwright. Aquí es donde defines cómo Playwright debe ejecutar tus pruebas, qué entornos usar, cómo reportar los resultados y cómo gestionar la aplicación bajo prueba.

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // Directorio donde Playwright buscará tus archivos de tests E2E.
  // Ejemplo: Si tienes un archivo 'e2e/auth.spec.ts', Playwright lo encontrará aquí.
  testDir: 'e2e',

  // Tiempo máximo que Playwright esperará para que un test individual termine de ejecutarse.
  // Si un test supera este tiempo, se marcará como fallido.
  // Es útil para evitar que tests "colgados" bloqueen la ejecución.
  // Ejemplo: Un test que navega por varias páginas y hace muchas interacciones; si alguna interacción
  // se queda esperando un elemento que nunca aparece por un bug, este timeout lo detectaría.
  timeout: 30_000, // 30 segundos

  // Número de veces que Playwright intentará re-ejecutar un test si falla por primera vez.
  // Esto es útil para tests E2E que pueden ser "flaky" (intermitentes) debido a factores externos
  // (problemas de red, latencia del servidor, etc.) pero que no representan un bug real.
  // Ejemplo: Un test falla una vez debido a un pico de latencia en la red, pero en el segundo intento
  // (la re-ejecución) pasa sin problemas. Si falla en la re-ejecución también, se reporta como un fallo.
  retries: 1,

  // Configuración de los "reporters", que son herramientas para visualizar los resultados de los tests.
  // Aquí se configuran dos:
  // 1. 'html': Genera un reporte HTML interactivo que puedes abrir en tu navegador para ver
  //    los detalles de cada test, capturas de pantalla, videos y logs. Muy útil para depurar.
  //    Ejemplo: Después de correr 'npx playwright test', puedes abrir el reporte HTML en './playwright-report'.
  // 2. 'list': Imprime los resultados de los tests directamente en la consola a medida que se ejecutan,
  //    mostrando cuáles pasaron, cuáles fallaron y un resumen al final.
  //    Ejemplo: Verás algo como:
  //      ✓  [1/2] e2e/auth.spec.ts: Login exitoso (5s)
  //      ✗  [2/2] e2e/profile.spec.ts: Cargar perfil (Error: Timeout) (30s)
  //      ...
  reporter: [['html'], ['list']],

  // Opciones base que se aplicarán a todos los proyectos de test que definas.
  use: {
    // La URL base para todos los tests. Puedes usar rutas relativas en tus tests
    // (ej. await page.goto('/login')) y Playwright las resolverá usando esta URL base.
    // Esto es crucial para no tener que escribir 'http://localhost:4000/login' en cada test.
    // Ejemplo: `await page.goto('/dashboard');` se traduce a `await page.goto('http://localhost:4000/dashboard');`
    baseURL: 'http://localhost:4000',

    // Configuración para la "trazabilidad" (tracing) de los tests.
    // 'on-first-retry': Playwright capturará un "trace" completo (capturas de pantalla, video, logs de red)
    // para los tests que fallan en el primer intento y luego son re-ejecutados. Esto es invaluable para
    // depurar tests flaky o fallos difíciles de reproducir.
    // Ejemplo: Si un test falla y se reintenta, Playwright guardará un archivo .zip con toda la información
    // del primer fallo para que puedas analizarlo con la herramienta de Playwright (npx playwright show-trace).
    trace: 'on-first-retry'
  },

  // Configuración para ejecutar un servidor web antes de iniciar los tests.
  // Esto es fundamental para los tests E2E, ya que necesitan una aplicación real funcionando
  // (tu front-end, tu back-end, o ambos) para interactuar con ella.
  webServer: {
    // El comando que se ejecutará para iniciar tu aplicación.
    // En este caso, 'npm run start:e2e' presumiblemente levanta tu servidor o front-end en modo E2E.
    // Ejemplo: Este comando podría iniciar un servidor Node.js y/o un servidor de desarrollo React/Angular/Vue.
    command: 'npm run start:e2e',

    // La URL que Playwright verificará para saber si tu servidor está listo y accesible.
    // Playwright esperará hasta que esta URL responda con un código 2xx antes de iniciar los tests.
    // Es común usar un endpoint de "salud" o "health check" para esto.
    // Ejemplo: Playwright enviará solicitudes GET a 'http://localhost:4000/health' hasta que obtenga
    // una respuesta exitosa, lo que indica que la aplicación está lista para recibir tráfico.
    url: 'http://localhost:4000/health',

    // Si es `true`, Playwright no intentará iniciar un nuevo servidor si ya hay uno escuchando
    // en la 'url' especificada. Esto es útil para el desarrollo local, donde podrías querer
    // ejecutar tus tests contra un servidor que ya tienes levantado.
    // `!process.env.CI`: Significa que `reuseExistingServer` será `true` a menos que
    // la variable de entorno `CI` esté establecida (típicamente en entornos de Integración Continua).
    // En CI, siempre se iniciará un nuevo servidor para asegurar un entorno limpio.
    reuseExistingServer: !process.env.CI,

    // Tiempo máximo que Playwright esperará a que el servidor web esté listo.
    // Si el servidor no responde en 'url' dentro de este tiempo, la ejecución de los tests fallará.
    // Ejemplo: Si tu aplicación tarda mucho en arrancar o tiene un bug que impide que el endpoint
    // /health responda, este timeout evitará que Playwright espere indefinidamente.
    timeout: 20_000 // 20 segundos
  }
});
```

---

En resumen, este archivo configura Playwright para:
*   Encontrar tus tests en el directorio `e2e`.
*   Darle a cada test 30 segundos para completarse y reintentar una vez si falla.
*   Generar reportes HTML y listarlos en la consola.
*   Usar `http://localhost:4000` como URL base.
*   Capturar "traces" para depuración cuando un test falla y se reintenta.
*   **Lo más importante para E2E:** Asegurarse de que tu aplicación (`npm run start:e2e`) esté funcionando en `http://localhost:4000` y responda en `/health` antes de ejecutar cualquier test. Esto es fundamental para que los tests tengan algo real con lo que interactuar.


## 4. Datos de Prueba y Gestión del Estado

Para que los tests E2E sean confiables y reproducibles, es fundamental controlar el estado de la aplicación, especialmente la base de datos. Cada test debe ejecutarse en un entorno limpio y predecible. Esto se logra mediante **endpoints de test especiales** en el servidor y una **función helper** en los tests.

### Endpoints de test en `app.ts` (Servidor/Backend)

Estos endpoints son **exclusivos para el entorno de testing** y se encargan de manipular la base de datos o el estado del servicio de una manera controlada. Es crucial que **solo estén activos cuando `NODE_ENV` sea `'test'`** para evitar que se expongan en producción.

```typescript
if (process.env.NODE_ENV === 'test') {
  // Endpoint para resetear la base de datos o el estado del servicio.
  // Recibe una solicitud POST y llama a un método `clear()` del servicio,
  // luego devuelve un estado 204 (No Content) para indicar éxito sin cuerpo de respuesta.
  app.post('/__test__/reset', (_req, res) => {
    service.clear?.(); // Llama a la función de limpieza del servicio (ej: vaciar DB)
    res.sendStatus(204); // Responde con 204 No Content
  });

  // Endpoint para "sembrar" (seed) la base de datos con datos de prueba específicos.
  // Crea algunos registros (aquí, dos libros) y devuelve los objetos creados.
  app.post('/__test__/seed', (_req, res) => {
    // Crea dos registros de libros usando el servicio.
    const a = service.create({ title: 'TDD', author: 'Beck', year: 2002 });
    const b = service.create({ title: 'DDD', author: 'Evans', year: 2003 });
    res.status(201).json({ created: [a, b] }); // Responde con 201 Created y los datos.
  });
}
```

*   **Propósito:** Estos endpoints permiten a los tests E2E interactuar directamente con el estado del servidor para inicializarlo o limpiarlo.
*   **Seguridad:** La condición `if (process.env.NODE_ENV === 'test')` es vital para que estos endpoints no estén disponibles en entornos de producción o staging, evitando manipulaciones no deseadas de la base de datos real.

### Helper en `e2e/helpers.ts` (Tests E2E)

Esta función helper centraliza la lógica para preparar el estado de la aplicación desde los tests, haciendo que los tests sean más legibles y DRY (Don't Repeat Yourself).

```typescript
import { request, expect } from '@playwright/test'; // Importa herramientas de Playwright

// Función asíncrona que reinicia y siembra la base de datos para los tests.
export async function resetAndSeed(baseURL: string) {
  // Crea un nuevo contexto de solicitud HTTP para interactuar con los endpoints de test.
  const ctx = await request.newContext({ baseURL });

  // Envía una solicitud POST al endpoint de reseteo.
  // Esto vacía o inicializa la base de datos.
  await ctx.post('/__test__/reset');

  // Envía una solicitud POST al endpoint de siembra.
  // Esto carga la base de datos con datos de prueba definidos.
  const res = await ctx.post('/__test__/seed');

  // Verifica que la siembra fue exitosa (código de estado 201 Created).
  expect(res.status()).toBe(201);

  // Parsea la respuesta JSON que contiene los datos creados.
  const data = await res.json();

  // Cierra el contexto de solicitud para liberar recursos.
  await ctx.dispose();

  // Devuelve los datos que fueron creados durante la siembra,
  // por si el test necesita usarlos.
  return data;
}
```

*   **Propósito:** Esta función es utilizada por los tests E2E (como en `test.beforeEach`) para garantizar que la aplicación bajo prueba siempre comience con un estado de datos conocido y consistente. Esto elimina la dependencia del orden de ejecución de los tests y evita "falsos positivos" o "falsos negativos" debido a estados de datos residuales de tests anteriores.
*   **Flujo:** Primero se llama a `/__test__/reset` para limpiar, y luego a `/__test__/seed` para poblar con datos controlados.
*   **Reutilización:** Permite reutilizar esta lógica de configuración en múltiples tests sin duplicar código.

---

En resumen, esta combinación de endpoints de test específicos en el backend y una función helper en el frontend crea un mecanismo robusto para la **gestión del estado de los datos en tests E2E**, haciendo que tus pruebas sean más confiables y fáciles de mantener.

### Helper en `e2e/helpers.ts`

```ts
import { request, expect } from '@playwright/test';

export async function resetAndSeed(baseURL: string) {
  const ctx = await request.newContext({ baseURL });
  await ctx.post('/__test__/reset');
  const res = await ctx.post('/__test__/seed');
  expect(res.status()).toBe(201);
  const data = await res.json();
  await ctx.dispose();
  return data;
}
```


## 5. Ejemplo de test E2E

Este código muestra un test E2E básico para una API de libros, usando Playwright:

```typescript
import { test, expect, request } from '@playwright/test'; // Importa herramientas de Playwright
import { resetAndSeed } from './helpers'; // Importa una función de ayuda para la base de datos

test.describe('E2E /books', () => { // Agrupa tests relacionados con la ruta '/books'

  // Antes de cada test, reinicia y "siembra" la base de datos con datos de prueba.
  // Esto asegura que cada test se ejecute en un estado conocido y limpio.
  test.beforeEach(async ({ baseURL }) => { await resetAndSeed(baseURL!); });

  // Define un test individual: "GET /books devuelve la semilla"
  test('GET /books devuelve la semilla', async ({ baseURL }) => {
    // Crea un nuevo contexto de solicitud HTTP para hacer llamadas a la API.
    const ctx = await request.newContext({ baseURL });

    // Realiza una solicitud GET a la ruta '/books'.
    const res = await ctx.get('/books');

    // Verifica que el código de estado de la respuesta sea 200 (OK).
    expect(res.status()).toBe(200);

    // Parsea la respuesta JSON.
    const items = await res.json();

    // Verifica que la lista de libros tenga al menos 2 elementos,
    // confirmando que los datos de prueba fueron devueltos.
    expect(items.length).toBeGreaterThanOrEqual(2);

    // Cierra el contexto de solicitud.
    await ctx.dispose();
  });
});
```

**En resumen:** Este test E2E simula una llamada HTTP a tu backend (`GET /books`), verifica que el servidor responde correctamente (código 200) y que los datos devueltos (los libros "sembrados") son los esperados. El `beforeEach` garantiza un estado inicial consistente de la base de datos para cada ejecución del test.



## 6. Buenas prácticas

* Pocos tests críticos.
* Independencia: reset + seed en cada test.
* Datos estables y predecibles.
* Idempotencia en paralelo.
* Validar status codes y contrato mínimo.
* Trazas y reportes activados.



## 7. Reportes y trazas

```bash
npm run build
npm run test:e2e
npm run report:e2e
```

Playwright genera **reportes HTML** y **trazas** para depuración.



## 8. Ejercicios propuestos

1. Validar que `year` ≤ año actual (400 si no se cumple).
2. Filtrar libros por autor en query string.
3. Implementar paginación y testear límites.
4. Probar rate limit con 429.
5. Idempotencia de DELETE.
6. Verificar headers (`Content-Type`, `Location`).
7. Traza de errores con `requestId`.



## 9. Extensiones

* Con BD real: usar migraciones + truncate/seed.
* Con autenticación: obtener token real en beforeEach.
* En staging: smoke tests tras deploy.
