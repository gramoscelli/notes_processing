
## Pruebas en TypeScript (Vitest) y pruebas HTTP

> Objetivo: configurar un entorno de **tests en TypeScript** con **Vitest**, medir **cobertura** (V8), probar utilidades síncronas/asíncronas y realizar **tests de integración** de la mini API (Semana 6) usando `app.inject()` de Fastify.

---

### 1) Teoría mínima

#### 1.1 La Estrategia de Pruebas: La Pirámide

No todas las pruebas son iguales. Una estrategia de testing robusta se visualiza comúnmente como una pirámide, donde cada nivel representa un tipo de prueba con un propósito, costo y velocidad diferentes. La idea es tener muchas pruebas rápidas y baratas en la base y muy pocas pruebas lentas y costosas en la cima.

```svg
<svg width="500" height="400" viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <style>
    .layer-text {
      font-size: 22px;
      font-weight: bold;
      text-anchor: middle;
      dominant-baseline: middle;
      fill: #1f2937;
    }
    .desc-text {
      font-size: 14px;
      font-style: italic;
      text-anchor: middle;
      dominant-baseline: middle;
      fill: #4b5563;
    }
  </style>

  <!-- Capa Base: Pruebas Unitarias -->
  <polygon points="10,390 490,390 390,260 110,260" fill="#a7f3d0" stroke="#10b981" stroke-width="2"/>
  <text x="250" y="310" class="layer-text">Pruebas Unitarias</text>
  <text x="250" y="340" class="desc-text">Muchas, Rápidas, Aisladas</text>

  <!-- Capa Media: Pruebas de Integración -->
  <polygon points="110,260 390,260 320,130 180,130" fill="#fde68a" stroke="#f59e0b" stroke-width="2"/>
  <text x="250" y="180" class="layer-text">Pruebas de Integración</text>
  <text x="250" y="210" class="desc-text">Bastantes, Velocidad Media</text>

  <!-- Capa Superior: Pruebas E2E -->
  <polygon points="180,130 320,130 280,30 220,30" fill="#fecaca" stroke="#ef4444" stroke-width="2"/>
  <text x="250" y="70" class="layer-text">Pruebas E2E</text>
  <text x="250" y="100" class="desc-text">Pocas, Lentas, Costosas</text>
</svg>
```


#### 1.1.2 Pruebas Unitarias (*Unit Tests*): La Base de la Pirámide

**Analogía:** Probar un solo ladrillo de LEGO para asegurar que tiene el color y la forma correctos antes de construir nada.

*   **Propósito:** Verificar que la **unidad más pequeña y aislada** de código funciona como se espera. Una "unidad" suele ser una función, un método de una clase o un componente de UI en completo aislamiento.
*   **Características:**
    *   **Aisladas:** No dependen de otras partes del sistema como bases de datos, redes o el DOM. Las dependencias externas se "simulan" (*mocking*).
    *   **Rápidas:** Se ejecutan en milisegundos. Puedes tener miles de ellas y ejecutarlas en segundos.
    *   **Abundantes:** Forman la gran mayoría de tus pruebas.
*   **Ejemplo práctico:**
    *   Probar que una función `sumar(2, 3)` devuelve `5`.
    *   Probar que una función `validarEmail("texto@dominio.com")` devuelve `true`.


#### 1.1.3 Pruebas de Integración (*Integration Tests*): El Nivel Intermedio

**Analogía:** Probar que dos o tres ladrillos de LEGO encajan correctamente entre sí.

*   **Propósito:** Verificar que **varios componentes (unidades) interactúan correctamente** cuando se combinan. El objetivo es encontrar errores en las "costuras" o interfaces entre los módulos.
*   **Características:**
    *   **Combinadas:** Prueban un flujo corto que involucra a varios módulos.
    *   **Más lentas:** Tardan más que las pruebas unitarias porque involucran más código y, a veces, sistemas reales (como una base de datos en memoria).
    *   **Menos numerosas:** Tienes menos pruebas de integración que unitarias.
*   **Ejemplo práctico:**
    *   Probar que al llamar a la ruta de una API (`/api/usuarios`), el controlador interactúa correctamente con el servicio de validación y este con un repositorio (usando una base de datos en memoria o de prueba) para devolver la lista de usuarios.
    *   Probar que al hacer clic en un botón "Añadir al Carrito" en un componente, el estado global de la aplicación se actualiza correctamente.


#### 1.1.4 Pruebas de Extremo a Extremo (*End-to-End* o E2E): La Cima de la Pirámide

**Analogía:** Construir el castillo de LEGO completo y asegurarse de que se parece a la imagen de la caja.

*   **Propósito:** Verificar un **flujo de usuario completo** a través de la aplicación, simulando el comportamiento de un usuario real. Es la prueba definitiva de que el sistema funciona como un todo.
*   **Características:**
    *   **Completas:** Involucran toda la pila tecnológica: el frontend en un navegador real, el backend, la base de datos, servicios externos, etc.
    *   **Lentas y costosas:** Son las más lentas de ejecutar (pueden tardar segundos o minutos por prueba) y las más frágiles (pueden fallar por problemas de red o cambios menores en la UI).
    *   **Escasas:** Debes tener solo unas pocas pruebas E2E que cubran los flujos más críticos de tu aplicación (ej. registro, inicio de sesión, proceso de compra).
*   **Ejemplo práctico:**
    *   Automatizar un navegador (con herramientas como Cypress o Playwright) para que:
        1.  Abra la página de inicio de sesión.
        2.  Rellene el formulario con un usuario y contraseña.
        3.  Haga clic en "Iniciar sesión".
        4.  Verifique que es redirigido al panel de control y que su nombre de usuario aparece en la pantalla.

---

### 1.2 ¿Por Qué Elegir Vitest?

Vitest se ha posicionado como el framework de testing de nueva generación para el ecosistema de Vite (y más allá), ofreciendo una experiencia de desarrollo superior por varias razones clave. No es solo una alternativa a Jest, sino una mejora fundamental en velocidad y simplicidad.

#### 1.2.1 API Familiar y Compatible con Jest

Para cualquiera que venga del ecosistema de Jest, la transición a Vitest es increíblemente fluida. Vitest adopta la misma API que ha sido el estándar durante años, por lo que no necesitas reaprender a escribir pruebas.

*   **Sintaxis Conocida:** Utiliza las mismas funciones globales que ya conoces y aprecias: `describe()` para agrupar pruebas, `it()` (o `test()`) para definir un caso de prueba individual, y `expect()` para las aserciones.
*   **Funcionalidades Avanzadas:** Incluye soporte completo para herramientas esenciales como *spies* y *mocks* (para simular dependencias), haciendo que la migración de una base de código existente sea un proceso de copiar y pegar en la mayoría de los casos.

#### 1.2.2 Rendimiento Superior y Soporte Nativo para TypeScript

Esta es la ventaja más significativa de Vitest. Aprovecha la arquitectura de Vite para ofrecer una velocidad y una experiencia de desarrollo que las herramientas tradicionales no pueden igualar.

*   **Ejecución Nativa:** A diferencia de Jest, que requiere configuraciones complejas con `ts-jest` o Babel para transpilar tu código antes de ejecutarlo, Vitest procesa tus archivos de TypeScript y JSX **al instante y de forma nativa**.
*   **Velocidad Extrema:** Utiliza el poder de **esbuild** (a través de Vite) para la transformación de código, que es órdenes de magnitud más rápido que el transpilador de JavaScript tradicional. El resultado es un arranque casi instantáneo y una re-ejecución de pruebas ultrarrápida en *watch mode*.

#### 1.2.3 Ecosistema Moderno y Completo

Vitest no sacrifica funcionalidades por velocidad. Viene con todas las herramientas que esperarías de un framework de testing moderno, listas para usar.

*   **Cobertura de Código Integrada:** Utiliza las capacidades nativas de V8 para generar reportes de cobertura, lo que lo hace mucho más rápido que las soluciones basadas en instrumentación de Babel (como Istanbul).
*   **Watch Mode Inteligente:** Su modo de observación es increíblemente rápido, ya que se integra con el grafo de módulos de Vite para saber exactamente qué pruebas necesita volver a ejecutar cuando un archivo cambia.
*   **Funcionalidades Estándar:** Ofrece soporte completo para *Snapshot Testing*, *Fake Timers* (para controlar `setTimeout`, `setInterval`, etc.), y mucho más, asegurando que no pierdas ninguna herramienta al migrar desde Jest.

En resumen, Vitest combina una API familiar y potente con un rendimiento de última generación, eliminando la complejidad de configuración y permitiéndote enfocarte en lo que realmente importa: escribir buenas pruebas.

### 1.3 Tests “type-aware”


#### Aprovechando el Compilador: Pruebas de Tipos (Type-Aware Testing)

Antes de escribir una sola prueba en Vitest, ya tienes la herramienta de testing más fundamental y de más alto rendimiento a tu disposición: **el propio compilador de TypeScript**. Las "pruebas de tipos" no son pruebas en el sentido tradicional; son la garantía de que tu código se adhiere a los contratos que has definido, eliminando una categoría entera de errores antes de que el programa se ejecute.

#### Los Dos Mundos del Testing: Compilación vs. Ejecución

Es crucial no confundir estos dos tipos de validación. Son dos capas de seguridad complementarias, no excluyentes.

*   **1. Mundo de Tipos (Compile-Time): El Plano Arquitectónico**
    *   **Herramienta:** El compilador de TypeScript (`tsc`).
    *   **¿Qué verifica?:** La **corrección estructural** de tu código. ¿Estás pasando un `string` a una función que espera un `number`? ¿Estás accediendo a una propiedad que no existe? ¿Has olvidado un `case` en un `switch` exhaustivo?
    *   **¿Cuándo ocurre?:** Antes de que se genere el JavaScript, durante el desarrollo o en un paso de CI. El código nunca llega a ejecutarse si hay un error de tipo.

*   **2. Mundo de Ejecución (Runtime): El Edificio en Funcionamiento**
    *   **Herramienta:** Un framework de testing como Vitest o Jest.
    *   **¿Qué verifica?:** El **comportamiento lógico** de tu código. Si llamas a `sumar(2, 2)`, ¿devuelve `4` o devuelve `5`? ¿Al hacer clic en un botón, se actualiza el estado correctamente?
    *   **¿Cuándo ocurre?:** Después de que el código ha sido compilado a JavaScript y se está ejecutando en un entorno (como Node.js).

#### La Práctica: `tsc --noEmit` en Integración Continua (CI)

La forma estándar de ejecutar tus "pruebas de tipos" es con este comando:
```bash
tsc --noEmit
```
*   **`tsc`**: Invoca al compilador de TypeScript.
*   **`--noEmit`**: Le dice al compilador: "Analiza todo el proyecto y busca errores de tipo, pero **no generes ningún archivo JavaScript**".

Este comando es increíblemente rápido y es la primera barrera de calidad que deberías poner en tu pipeline de CI. Si `tsc --noEmit` falla, significa que hay un error de tipo, y no tiene sentido gastar tiempo y recursos en ejecutar las pruebas de Vitest, que son más lentas.

| Característica | Pruebas de Tipos (Compile-time) | Pruebas de Ejecución (Runtime) |
| :--- | :--- | :--- |
| **Herramienta** | `tsc` | `Vitest`, `Jest`, etc. |
| **Propósito** | Validar la corrección estructural y de tipos. | Validar la lógica y el comportamiento del código. |
| **Ejemplo de error** | `const x: number = "hola";` | `function sumar(a, b) { return a - b; }` |
| **Cuándo se ejecuta**| Antes de la ejecución. | Durante la ejecución del código. |

**En resumen:** Piensa en `tsc --noEmit` como la prueba unitaria más rápida y barata que puedes ejecutar. Si pasa, ganas confianza en que tu código es estructuralmente sólido, y entonces puedes pasar a Vitest para verificar que también se comporta como esperas.

### 1.4 Dobles de Prueba: Controlando el Entorno de Tus Tests

En el testing, a menudo necesitamos que nuestro código interactúe con otras partes del sistema (dependencias). Sin embargo, para que una prueba sea rápida, predecible y aislada, no queremos depender de una base de datos real, una API externa o incluso de un módulo complejo.

Aquí es donde entran los **Dobles de Prueba** (*Test Doubles*). Son objetos o funciones "impostoras" que se hacen pasar por las dependencias reales, dándonos control total sobre el entorno de la prueba. Piensa en ellos como los dobles de acción en una película: parecen reales y hacen el trabajo necesario para la escena, pero sin el riesgo del actor principal.

Vitest ofrece varias herramientas para crear estos dobles:

##### 1.4.1 Spies: El Observador

**Analogía:** Un espía o un informante que observa y toma notas de lo que sucede, pero **sin interferir** con la operación original.

*   **¿Para qué sirven?** Para verificar **interacciones**. Quieres saber *si* una función fue llamada, *cuántas veces* fue llamada y *con qué argumentos* fue llamada, pero dejando que la función original se ejecute normalmente.
*   **En Vitest:** Se crean con `vi.fn()` (para una función genérica) o `vi.spyOn(objeto, 'metodo')` para "envolver" un método existente.

```typescript
// Ejemplo: ¿Se está llamando correctamente al sistema de logging?
const logger = {
  log: (message: string) => {
    console.log(message); // Comportamiento original
  }
};

it('debería llamar al logger con el mensaje correcto', () => {
  // 1. Creamos un espía que envuelve el método `log`
  const logSpy = vi.spyOn(logger, 'log');

  // 2. Ejecutamos el código que queremos probar
  function registrarUsuario(nombre: string) {
    logger.log(`Usuario ${nombre} registrado.`);
  }
  registrarUsuario('Ana');

  // 3. Verificamos la interacción con el espía
  expect(logSpy).toHaveBeenCalledTimes(1);
  expect(logSpy).toHaveBeenCalledWith('Usuario Ana registrado.');
});
```

##### 1.4.2 Mocks: El Reemplazo

**Analogía:** Un actor impostor que reemplaza completamente al actor real. Tú le das el guion y él dirá exactamente lo que le pidas.

*   **¿Para qué sirven?** Para **aislar** el código que estás probando de sus dependencias. Reemplazas un módulo o función completo con una versión controlada que devuelve los datos que tú quieras, evitando llamadas a APIs, bases de datos, etc.
*   **En Vitest:** Se usa `vi.mock('ruta/al/modulo')` para reemplazar un módulo entero.

```typescript
// Módulo a mockear (ej: api.ts)
export const fetchUsuario = (id: number) => {
  // En la vida real, esto haría una llamada de red...
  return fetch(`https://api.ejemplo.com/users/${id}`).then(res => res.json());
}

// Archivo de prueba (ej: servicio.test.ts)
import { fetchUsuario } from './api';
import { obtenerNombreDeUsuario } from './servicio';

// 1. Reemplazamos el módulo './api' completo ANTES de que se ejecuten las pruebas
vi.mock('./api');

it('debería obtener el nombre del usuario desde la API mockeada', async () => {
  // 2. Damos un comportamiento a la función mockeada para esta prueba
  vi.mocked(fetchUsuario).mockResolvedValue({ id: 1, name: 'Juan' });
  
  // 3. Ejecutamos nuestra lógica, que internamente llama a `fetchUsuario`
  const nombre = await obtenerNombreDeUsuario(1);
  
  // 4. Verificamos que nuestro servicio procesó la respuesta del mock
  expect(nombre).toBe('Juan');
});
```

##### 1.4.3 Fake Timers: El Controlador del Tiempo

**Analogía:** Un control remoto para una máquina del tiempo. Puedes pausar, adelantar o retroceder el tiempo a tu antojo.

*   **¿Para qué sirven?** Para probar código que depende del paso del tiempo (como `setTimeout`, `setInterval` o `Date`) de forma **instantánea y predecible**, sin tener que esperar realmente.
*   **En Vitest:** Se activan con `vi.useFakeTimers()` y se controlan con funciones como `vi.advanceTimeByTime()`.

```typescript
it('debería ejecutar el callback después de 5 segundos', () => {
  // 1. Activamos los temporizadores falsos
  vi.useFakeTimers();
  const callback = vi.fn(); // Un spy para verificar si se llama

  // 2. Ejecutamos el código que usa un temporizador
  setTimeout(callback, 5000);

  // 3. En lugar de esperar, "adelantamos el reloj"
  vi.advanceTimeByTime(5000);

  // 4. Verificamos que el callback fue llamado
  expect(callback).toHaveBeenCalledTimes(1);
  
  // Limpieza (buena práctica)
  vi.useRealTimers();
});
```

### 1.5 Cobertura de Código: El Mapa de Tus Pruebas

La cobertura de código (*code coverage*) es una métrica que te indica qué porcentaje de tu código fuente ha sido ejecutado mientras corrían tus pruebas.

Piensa en ella no como una medida de la *calidad* de tus pruebas, sino como un **mapa de las zonas que no has probado**. La pregunta que responde no es "¿mi código funciona?", sino "**¿qué partes de mi código he probado y cuáles he ignorado?**".

#### ¿Qué Mide Exactamente?

Las herramientas de cobertura, como la que viene integrada en Vitest, suelen reportar varias métricas:

| Métrica | Descripción | Ejemplo de Falla |
| :--- | :--- | :--- |
| **Líneas** | Porcentaje de líneas de código ejecutables que fueron ejecutadas. | Una línea dentro de un `if` que nunca se cumplió. |
| **Funciones** | Porcentaje de funciones que fueron llamadas al menos una vez. | Una función de utilidad que ninguna prueba invocó. |
| **Ramas** | Porcentaje de "caminos" lógicos que se tomaron. | Probar solo el `if` de una condición, pero nunca el `else`. |

La métrica de **ramas** es a menudo la más reveladora. Puedes tener un 100% de cobertura de líneas en una función, pero si solo probaste un camino de una bifurcación `if/else` compleja, tu cobertura de ramas será baja, indicando que hay escenarios lógicos que no has verificado.

#### Estableciendo Umbrales (`Thresholds`): La Red de Seguridad

Una práctica común en la Integración Continua (CI) es establecer **umbrales de cobertura**. Esto significa que si el porcentaje de cobertura de tu código cae por debajo de un cierto número, el pipeline de CI fallará, impidiendo que se integre código que no ha sido mínimamente probado.

**El Peligro de Perseguir el 100%**

Es tentador establecer umbrales muy altos (90%-100%), pero esto a menudo es contraproducente. Perseguir un número puede llevar a los equipos a escribir pruebas de baja calidad que simplemente "tocan" el código para aumentar la métrica, pero no verifican su comportamiento de forma significativa.

Esto se conoce como la **Ley de Goodhart**: "Cuando una medida se convierte en un objetivo, deja de ser una buena medida".

**La Estrategia Razonable:**

1.  **Establece un umbral base y razonable:** Un punto de partida común es establecer un umbral de líneas entre el **60% y el 80%**. Esto actúa como una red de seguridad para evitar que se añadan grandes cantidades de código sin probar.
2.  **Enfócate en la Calidad, no en la Cantidad:** Usa el reporte de cobertura no para celebrar un número alto, sino para **identificar las partes críticas de tu aplicación que tienen baja cobertura**.
3.  **Prioriza:** ¿El módulo de pagos tiene un 40% de cobertura? ¡Es una señal de alerta! ¿Un script de utilidad simple tiene un 70%? Quizás no sea tan urgente.

> **Regla Mental:** La cobertura del 0% es una señal de alarma. La cobertura del 100% no garantiza nada. Utiliza la métrica para encontrar puntos ciegos en tus pruebas y aumentar tu **confianza** en el código, no para perseguir un porcentaje.


### 1.6 Ejemplo Práctico: Generando un Reporte de Cobertura con Vitest

Vamos a ver cómo funciona la cobertura en la práctica. Crearemos un módulo simple con una lógica condicional, escribiremos pruebas que **intencionadamente no cubren todos los casos**, generaremos el reporte, lo analizaremos y finalmente arreglaremos nuestras pruebas para alcanzar el 100% de cobertura.

#### Paso 1: Configurar Vitest para la Cobertura

Primero, necesitamos decirle a Vitest que queremos recolectar datos de cobertura.

**En tu archivo `vitest.config.ts` (o `vite.config.ts`), añade la sección `test.coverage`:**

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // ...otras configuraciones de test...
    coverage: {
      // El proveedor de cobertura. 'v8' es rápido y nativo.
      provider: 'v8', 
      // Reporteros para generar el informe. 'text' en consola, 'html' para un informe visual.
      reporter: ['text', 'html'],
      // Opcional: Establecer umbrales. El build fallará si no se alcanzan.
      thresholds: {
        lines: 60,
        branches: 60,
        functions: 60,
        statements: 60,
      },
    },
  },
});
```

**En tu `package.json`, añade un script para la cobertura:**

```json
{
  "scripts": {
    "test": "vitest",
    "coverage": "vitest run --coverage"
  }
}
```
*   `vitest run`: Ejecuta las pruebas una vez y sale (ideal para CI).
*   `--coverage`: Activa la recolección de cobertura.

#### Paso 2: El Código que Vamos a Probar

Crea un archivo `src/math.ts`. Nota que la función `dividir` tiene una rama lógica (un `if`) que maneja la división por cero.

```typescript
// src/math.ts
export function sumar(a: number, b: number): number {
  return a + b;
}

export function dividir(a: number, b: number): number {
  if (b === 0) {
    throw new Error("No se puede dividir por cero");
  }
  return a / b;
}
```

#### Paso 3: Las Pruebas (Incompletas)

Ahora, crea un archivo de prueba `src/math.test.ts`, pero solo probaremos el "camino feliz" de la función `dividir`.

```typescript
// src/math.test.ts
import { describe, it, expect } from 'vitest';
import { sumar, dividir } from './math';

describe('Funciones matemáticas', () => {
  it('debería sumar dos números correctamente', () => {
    expect(sumar(2, 3)).toBe(5);
  });

  // Solo probamos el caso exitoso de la división
  it('debería dividir dos números correctamente', () => {
    expect(dividir(10, 2)).toBe(5);
  });
});
```

#### Paso 4: Ejecutar y Analizar el Reporte de Cobertura

Ahora, ejecuta el comando en tu terminal:

```bash
npm run coverage
```

Vitest ejecutará las pruebas y te mostrará un reporte de cobertura en la consola similar a este:

```bash
---------------------|---------|----------|---------|---------|-------------------
File                 | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
---------------------|---------|----------|---------|---------|-------------------
All files            |   85.71 |       50 |     100 |   85.71 |                   
 src/math.ts         |   85.71 |       50 |     100 |   85.71 | 7                 
---------------------|---------|----------|---------|---------|-------------------
```

**Análisis del Reporte:**

*   **`% Stmts` (Statements)**: 85.71% de las declaraciones fueron ejecutadas.
*   **`% Branch` (Ramas)**: **¡Solo el 50%!** Esta es la pista clave. Significa que de las 2 posibles ramas en nuestro código (el `if` y el `else` implícito), solo una fue probada.
*   **`% Funcs` (Funciones)**: 100%. Ambas funciones (`sumar` y `dividir`) fueron llamadas.
*   **`% Lines` (Líneas)**: 85.71% de las líneas fueron ejecutadas.
*   **`Uncovered Line #s`**: **`7`**. Vitest nos dice exactamente qué línea no se ejecutó: la línea 7, que es `throw new Error(...)`.

Además, Vitest habrá creado una carpeta `coverage/` en tu proyecto. Si abres el archivo `coverage/index.html` en un navegador, verás un reporte visual detallado que resalta en rojo las líneas no cubiertas.

#### Paso 5: Mejorar las Pruebas para Alcanzar el 100%

El reporte nos ha mostrado exactamente dónde está el punto ciego de nuestras pruebas. Ahora, vamos a añadir el caso de prueba que falta en `src/math.test.ts`.

```typescript
// src/math.test.ts
import { describe, it, expect } from 'vitest';
import { sumar, dividir } from './math';

describe('Funciones matemáticas', () => {
  it('debería sumar dos números correctamente', () => {
    expect(sumar(2, 3)).toBe(5);
  });

  it('debería dividir dos números correctamente', () => {
    expect(dividir(10, 2)).toBe(5);
  });

  // AÑADIMOS ESTA NUEVA PRUEBA
  it('debería lanzar un error al dividir por cero', () => {
    // Verificamos que llamar a la función con estos argumentos lanza un error.
    expect(() => dividir(5, 0)).toThrow("No se puede dividir por cero");
  });
});
```

#### Paso 6: Volver a Ejecutar la Cobertura

Ejecuta de nuevo:
```bash
npm run coverage
```

Ahora, el reporte será mucho más satisfactorio:

```bash
---------------------|---------|----------|---------|---------|-------------------
File                 | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
---------------------|---------|----------|---------|---------|-------------------
All files            |     100 |      100 |     100 |     100 |                   
 src/math.ts         |     100 |      100 |     100 |     100 |                   
---------------------|---------|----------|---------|---------|-------------------
```

¡Éxito! Al añadir la prueba para el caso de error, hemos cubierto la otra rama lógica, y ahora tenemos un 100% de cobertura, lo que nos da mucha más confianza en que nuestra función `dividir` se comporta como esperamos en todos los escenarios.


### 1.7 Buenas Prácticas para Escribir Tests de Calidad

Escribir pruebas no es solo cuestión de aumentar la cobertura; es cuestión de crear una red de seguridad que te dé **confianza** para refactorizar y añadir nuevas funcionalidades. Una suite de pruebas de baja calidad puede convertirse en una carga en lugar de una ayuda. Aquí se presentan tres principios fundamentales para mantener tus pruebas robustas y mantenibles.

#### 1. La Regla de Hierro: Determinismo y Repetibilidad

Un test debe comportarse como un experimento científico: dadas las mismas condiciones de entrada, **siempre debe producir el mismo resultado**.

*   **Principio:** Si ejecutas la suite de pruebas 100 veces sin cambiar el código, las 100 veces debe pasar. Si una prueba falla, debe ser porque se ha introducido un bug real, no por azar.
*   **¿Por qué es crucial?** La confianza es la moneda de cambio de una suite de pruebas. Si los tests fallan de forma intermitente, el equipo empezará a ignorarlos ("*Ah, es solo el test frágil de siempre, ejecútalo de nuevo*"). Una suite de pruebas en la que no se confía es una suite de pruebas inútil.

#### 2. Claridad y Enfoque: Un Test, Una Idea

Cada bloque `it(...)` debe ser fácil de leer, fácil de entender y debe probar **una sola cosa**.

*   **Principio:** Un test debe verificar un único comportamiento o resultado. Su nombre debe describir claramente ese comportamiento, siguiendo un patrón como "debería [hacer algo] cuando [ocurre una condición]".
*   **¿Por qué es crucial?** Cuando un test falla, su nombre debería decirte exactamente qué se rompió sin necesidad de leer el código. Si un test llamado `it('prueba el servicio de usuario')` falla, no tienes ni idea de cuál de las 10 aserciones que contiene es la que falló.

**Estructura Recomendada: Arrange-Act-Assert (AAA)**

| Fase | Propósito | Ejemplo |
| :--- | :--- | :--- |
| **Arrange (Preparar)** | Configura el estado inicial y las dependencias (mocks, datos de entrada). | `const usuario = { esAdmin: false };` |
| **Act (Actuar)** | Ejecuta la función o el método que quieres probar. | `const puedeAcceder = puedeAccederAlPanel(usuario);` |
| **Assert (Verificar)** | Comprueba que el resultado es el esperado. | `expect(puedeAcceder).toBe(false);` |

```typescript
// Mal nombre, múltiples ideas
it('funciona', () => {
  expect(sumar(2, 2)).toBe(4);
  expect(sumar(-1, 1)).toBe(0);
});

// Buen nombre, una sola idea, estructura AAA
it('debería devolver 0 cuando se suman un número positivo y su negativo', () => {
  // Arrange
  const a = -5;
  const b = 5;

  // Act
  const resultado = sumar(a, b);

  // Assert
  expect(resultado).toBe(0);
});
```

#### 3. Aislamiento: Protegiéndote de la Fragilidad (*Flaky Tests*)

Un test "frágil" (*flaky*) es aquel que a veces pasa y a veces falla sin cambios en el código. La causa principal es la dependencia de factores externos que no puedes controlar.

*   **Principio:** Aísla tus pruebas de dependencias externas como la red, la base de datos, el sistema de archivos o el tiempo real.
*   **¿Por qué es crucial?** Estas dependencias hacen que tus pruebas sean lentas y no deterministas. Si una prueba falla porque la API de un tercero está caída, no es un error en tu código, es ruido que te hace perder tiempo y confianza.

**Soluciones Comunes:**

*   **Dependencia de Red/APIs:** No hagas llamadas `fetch` reales. Usa **mocks** con `vi.mock()` para simular las respuestas de la API.
*   **Dependencia de Base de Datos:** No te conectes a una base de datos real. Usa una base de datos en memoria (como SQLite en modo memoria) o mockea la capa de repositorio.
*   **Dependencia del Tiempo:** No dependas de `setTimeout` o `new Date()`. Usa **Fake Timers** con `vi.useFakeTimers()` para controlar el tiempo a tu antojo.
*   **Testing de APIs (Backend):** En lugar de levantar un servidor y hacer una llamada HTTP real (que depende de la red local), usa herramientas de **inyección de peticiones** como `app.inject()` (en Fastify) o `supertest`. Estas herramientas llaman a tus manejadores de ruta directamente en memoria, haciendo la prueba miles de veces más rápida y 100% fiable.

## 2) Práctica con npm

> Se asume el proyecto de la Semana 6. Vamos a **refactorizar** para testear mejor la API.

### 2.1 Dependencias y scripts

```bash
npm i -D vitest @vitest/coverage-v8
```

**`package.json`** (fragmento)

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:cov": "vitest run --coverage",
    "typecheck": "tsc --noEmit"
  }
}
```

### 2.2 Configuración de Vitest

**`vitest.config.ts`**

```ts
import { defineConfig } from "vitest/config"

export default defineConfig({
  test: {
    environment: "node",
    globals: true,
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
      all: true,
      thresholds: { lines: 0.6, functions: 0.6, branches: 0.5, statements: 0.6 }
    }
  }
})
```

> `thresholds` en proporciones (0–1). Ajustá a tu realidad.

**Tip TS**: agregá Vitest a los *ambient types* en `tsconfig.json` para autocompletado:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

### 2.3 Refactor del servidor para pruebas

Creamos una **fábrica de app** y dejamos `server.ts` solo para *listen*.

**`src/app.ts`**

```ts
import Fastify from "fastify"
import { ZodTypeProvider, serializerCompiler, validatorCompiler } from "fastify-type-provider-zod"
import ItemsRoutes from "./routes/items"
import { ItemRepo } from "./lib/repo"

export function buildApp() {
  const app = Fastify({ logger: false }).withTypeProvider<ZodTypeProvider>()
  app.setValidatorCompiler(validatorCompiler)
  app.setSerializerCompiler(serializerCompiler)
  app.decorate("repo", new ItemRepo())
  app.get("/health", async () => ({ ok: true as const }))
  app.register(ItemsRoutes)
  return app
}
```

**`src/server.ts`** (ajustado)

```ts
import { buildApp } from "./app"
const app = buildApp()
const port = Number(process.env.PORT ?? 3000)
app.listen({ port, host: "0.0.0.0" }).catch((e) => { console.error(e); process.exit(1) })
```

### 2.4 Setup global de tests

**`tests/setup.ts`**

```ts
import { afterAll, beforeAll } from "vitest"
import { buildApp } from "../src/app"

export const t = { app: buildApp() }

beforeAll(async () => { await t.app.ready() })
afterAll(async () => { await t.app.close() })
```

### 2.5 Tests de utilidades síncronas/asíncronas

**`tests/async.test.ts`**

```ts
import { withTimeout, TimeoutError } from "../src/lib/async"

it("resuelve antes del timeout", async () => {
  const p = new Promise<number>(res => setTimeout(() => res(42), 50))
  await expect(withTimeout(p, 200)).resolves.toBe(42)
})

it("lanza TimeoutError cuando excede", async () => {
  const p = new Promise<number>(res => setTimeout(() => res(42), 200))
  await expect(withTimeout(p, 50)).rejects.toBeInstanceOf(TimeoutError)
})
```

### 2.6 Tests de esquemas (Zod)

**`tests/schemas.test.ts`**

```ts
import { Item, NewItem } from "../src/schemas"

it("valida Item y NewItem", () => {
  const good = { name: "Teclado", price: 100 }
  expect(() => NewItem.parse(good)).not.toThrow()
  const bad = { name: "", price: -1 }
  expect(() => NewItem.parse(bad as any)).toThrow()
})
```

### 2.7 Tests de integración con `app.inject()`

**`tests/app.test.ts`**

```ts
import { t } from "./setup"

it("/health responde ok", async () => {
  const res = await t.app.inject({ method: "GET", url: "/health" })
  expect(res.statusCode).toBe(200)
  expect(res.json()).toEqual({ ok: true })
})
```

**`tests/items.routes.test.ts`**

```ts
import { t } from "./setup"

async function crear(name = "Mouse", price = 10) {
  const r = await t.app.inject({ method: "POST", url: "/items", payload: { name, price } })
  expect(r.statusCode).toBe(201)
  return r.json() as { id: string; name: string; price: number }
}

it("CRUD de items", async () => {
  // create
  const created = await crear("Teclado", 100)
  // list
  const list = await t.app.inject({ method: "GET", url: "/items" })
  expect(list.statusCode).toBe(200)
  expect(Array.isArray(list.json())).toBe(true)
  // get
  const got = await t.app.inject({ method: "GET", url: `/items/${created.id}` })
  expect(got.statusCode).toBe(200)
  expect(got.json().name).toBe("Teclado")
  // update
  const upd = await t.app.inject({ method: "PUT", url: `/items/${created.id}` , payload: { name: "Teclado M", price: 120 } })
  expect(upd.statusCode).toBe(200)
  expect(upd.json().price).toBe(120)
  // delete
  const del = await t.app.inject({ method: "DELETE", url: `/items/${created.id}` })
  expect(del.statusCode).toBe(204)
})
```

### 2.8 Spies y *fake timers*

**`tests/timers.test.ts`**

```ts
it("usa fake timers", async () => {
  vi.useFakeTimers()
  const spy = vi.fn()
  setTimeout(spy, 1000)
  vi.advanceTimersByTime(1000)
  expect(spy).toHaveBeenCalledTimes(1)
  vi.useRealTimers()
})
```

---

## 3) Mini–katas (ejemplos opcionales)

1. Agregá **umbrales** de cobertura ≥ 70% líneas y ≥ 60% ramas; obtené reporte HTML.
2. Mockeá el repo en `items.routes.test.ts` para simular un error y verificá `500` con mensaje coherente.
3. Añadí test de validación: `POST /items` con `name: ""` → `400`.
4. Medí tiempo de cada request con un *plugin* y testeá que se loguea (usá `vi.spyOn(app.log, 'info')`).
5. Creá un test de *property-based* con `@fast-check/vitest` para `sum`.

---

## 4) Comandos útiles

```bash
npm run test:watch
npm run test
npm run test:cov   # reporte texto + html en coverage/
npm run typecheck
```

---

## 5) Checklist de la semana

* [ ] Vitest configurado (setup, globals, coverage V8).
* [ ] Tests unitarios de utilidades y esquemas.
* [ ] Tests de integración con `app.inject()` (CRUD completo).
* [ ] *Spies* y *fake timers* demostrados.
* [ ] Umbrales de cobertura definidos y cumplidos.

---

## 6) Entregables

* `vitest.config.ts`, `tests/setup.ts`.
* `tests/*.test.ts` (al menos: `async.test.ts`, `schemas.test.ts`, `app.test.ts`, `items.routes.test.ts`, `timers.test.ts`).
* README con comandos de test y ubicación de cobertura.


## Automatización de calidad: Husky + lint-staged + tipo estricto

**Objetivos**

* Asegurar calidad en commits y CI local.

**Teoría mínima**

* Hooks de Git, pipelines locales.

**Práctica con npm**

1. Instalar y configurar:

   ```bash
   npm i -D husky lint-staged
   npm pkg set scripts.prepare="husky"
   npm run prepare
   npx husky add .husky/pre-commit "npm run typecheck && npm run lint && npx lint-staged"
   ```
2. `package.json`:

   ```json
   {
     "lint-staged": {
       "**/*.{ts,tsx}": ["prettier -w", "eslint --fix"]
     }
   }
   ```
3. Probar commit con cambio con errores y verificar bloqueo del hook.

**Entrega**: video corto o gif del hook funcionando (opcional) + commit válido.

---

## Ruta Frontend (opcional): React + TS con Vite

**Objetivos**

* Tipar Props/State, eventos, formularios con Zod.

**Práctica con npm**

1. Crear app:

   ```bash
   npm create vite@latest frontend -- --template react-ts
   cd frontend && npm i zod
   npm run dev
   ```
2. Añadir form tipado con Zod y *discriminated unions* para estados.
3. Scripts relevantes (ya provistos por Vite): `dev`, `build`, `preview`.

**Entrega**: demo con validación y estados tipados.

---

## Ruta Backend (alternativa): API tipada y documentación

**Objetivos**

* Diseñar endpoints con esquemas y generar documentación.

**Práctica con npm**

1. Añadir OpenAPI (opcional):

   ```bash
   npm i -D zod-to-openapi
   ```
2. Generar `openapi.json` desde esquemas Zod (script `npm run openapi`).
3. Validar en Swagger UI (local o dockerizado).

**Entrega**: `openapi.json` válido y endpoints alineados.

---

## Capstone y entrega final

**Objetivos**

* Integrar tooling: `typecheck` + `lint` + `test` + `build` en un solo comando.

**Práctica con npm**

1. Script "ci" y flujo de release:

   ```json
   {
     "scripts": {
       "ci": "npm run typecheck && npm run lint && npm run test && npm run build",
       "release:dry": "npm pack"
     }
   }
   ```
2. Preparar README con instrucciones de uso/instalación.
3. (Opcional) Publicación privada: `npm publish --access=public|restricted` (usar `dry-run` primero).

**Entrega**: repositorio con CI local funcionando y tag de versión (`npm version patch`).
