# Introducción a Typescript

## Setup y convenciones

* **Requisitos**: Node LTS (>=18), npm (>=9), editor con soporte TS (VS Code recomendado).
* **Estructura base**:

  ```bash
  npm init -y
  npm i -D typescript @types/node ts-node
  npx tsc --init --strict
  mkdir src tests
  echo "console.log('Hello TS');" > src/index.ts
  ```
* **Scripts iniciales** (`package.json`):

  ```json
  {
    "type": "module",
    "scripts": {
      "dev": "ts-node src/index.ts",
      "typecheck": "tsc --noEmit",
      "build": "tsc -p tsconfig.json",
      "start": "node dist/index.js",
      "clean": "rimraf dist"
    }
  }
  ```


## Fundamentos y entorno de trabajo

**Objetivos**

* Entender TS → JS, configuración mínima de `tsconfig.json`, inferencia y anotaciones de tipos.

### 1) Teoría

#### 1.1 ¿Qué es TypeScript?

* **Superset de JavaScript** con **tipado estático opcional**.
* Se **transpila** (compila) a JavaScript estándar para ejecutarse en Node o el navegador.
* Beneficios: detección temprana de errores, autocompletado y refactors más seguros, documentación viva mediante tipos.

#### 1.2 Flujo de compilación TS → JS

1. Editas archivos `.ts` en `src/`.
2. El compilador `tsc` valida tipos y genera `.js` (por defecto en `dist/`).
3. Ejecutas el JS generado con Node (o sirves en el navegador).

> NOTA: En desarrollo podemos ejecutar TS directamente con utilidades como `ts-node` o `tsx` para iterar rápido.

#### 1.3 `tsconfig.json` (mínimos clave)

* `target`: versión de JS a generar (p. ej., `ES2022`).
* `module`: sistema de módulos de salida (p. ej., `ESNext` o `CommonJS`).
* `strict`: activa el modo estricto (recomendado).
* `outDir`: carpeta de salida (p. ej., `dist`).
* `moduleResolution`: cómo se resuelven importaciones (p. ej., `Bundler`, `Node`).
* `include`: qué carpetas/archivos compilar (p. ej., `src`).

#### 1.4 Tipos básicos y especiales

* **Primitivos**: `string`, `number`, `boolean`.
* **Especiales**: `null`, `undefined`, `void` (retorno de funciones sin valor).
* **`any`**: desactiva el chequeo de tipos (evitar salvo migraciones).
* **`unknown`**: dato de tipo desconocido que **obliga** a validar antes de usar.
* **`never`**: funciones que nunca retornan (p. ej., lanzan error) o código inalcanzable.

#### 1.5 Inferencia, anotaciones y aserciones

* **Inferencia**: TS deduce el tipo a partir del valor asignado.

  ```ts
  const x = 42; // number inferido
  ```
* **Anotación**: declaras el tipo explícitamente.

  ```ts
  let nombre: string = "Ada";
  ```
* **Aserciones** (no cambian el valor, solo dicen a TS cómo tratarlo):

  * `as Tipo` y `<>` (en TSX se usa solo `as`),
  * `as const` (vuelve literal/readonly),
  * **non-null assertion** `!` (afirma que no es `null`/`undefined`, usar con moderación).

  ```ts
  const el = document.getElementById("app");
  el!.innerHTML = "Hola"; // ¡solo si estás seguro de que existe!

  const status = "ok" as const; // tipo "ok", no string genérico
  ```

#### 1.6 Tipado estructural (idea clave)
**¿Qué es el Tipado Estructural?**
El principio fundamental del sistema de tipos de *TypeScript* es el tipado estructural, a veces llamado _"duck typing"_ ("si camina como un pato y grazna como un pato, entonces debe ser un pato"). Esto significa que _TypeScript_ no se fija en el nombre del tipo o en si fue explícitamente declarado de cierta manera, sino en la estructura o forma que tienen los datos. Al comparar dos tipos, _TypeScript_ solo considera los miembros (propiedades y métodos) que contienen.

* TS compara **formas** (propiedades/métodos) de los objetos, no sus nombres de tipo.
* Si dos objetos tienen la misma estructura requerida, son compatibles.



```ts
type Persona = { nombre: string };

const usuario = { nombre: "Ana", edad: 20 };

// OK: usuario tiene al menos { nombre: string }
const p: Persona = usuario;

// ERROR (excess property check): literal con extra "edad" directamente a Persona
const p2: Persona = { nombre: "Ana", edad: 20 }; // ❌

```

> **¿Por qué es correcto? ```const p: Persona = usuario;```**
Aquí se aplica el tipado estructural en su forma más pura.
>*   El tipo `Persona` exige que cualquier objeto compatible tenga una propiedad `nombre` de tipo `string`.
>*   La variable `usuario` es un objeto que tiene la propiedad `nombre` (y además la propiedad `edad`).
>*   Como `usuario` cumple con la "forma" mínima requerida por `Persona` (tiene un `nombre`), la asignación es válida. TypeScript simplemente ignora la propiedad adicional `edad`.
>Esta flexibilidad es muy potente, ya que permite que los objetos contengan más información de la requerida por un tipo sin generar errores.
Sin embargo, la asignación con arror (Chequeo de Propiedades Excesivas)

> **¿Por qué es incorrecto? ```const p2: Persona = { nombre: "Ana", edad: 20 };```**
A primera vista, esto parece inconsistente con el ejemplo anterior. Sin embargo, TypeScript aplica una regla más estricta llamada "chequeo de propiedades excesivas" cuando se asigna un objeto literal (un objeto definido directamente en el lugar de la asignación) a una variable con un tipo explícito.
El razonamiento de TypeScript es el siguiente:
>* Cuando creas un objeto literal y lo asignas directamente, es muy probable que tu intención sea que ese objeto se ajuste exactamente a la forma del tipo. Las propiedades adicionales suelen ser errores tipográficos o malentendidos sobre la estructura del tipo. En este caso:
Estás creando un objeto ```{ nombre: "Ana", edad: 20 }``` y asignándolo de inmediato a una variable de tipo ```Persona```.
_TypeScript_ detecta que el objeto literal tiene una propiedad edad que no está definida en el tipo Persona.
Para ayudarte a detectar un posible error, te avisa con un mensaje que indica que la propiedad edad no existe en el tipo ```Persona```.
Esta verificación especial solo se activa para **objetos literales**, lo que explica por qué el primer ejemplo, que utiliza una variable intermedia (usuario), sí funciona.
---

### 2) Parte práctica

#### 2.1 Preparación del proyecto

```bash
npm init -y
npm i -D typescript @types/node ts-node
npx tsc --init --strict
mkdir src
printf "console.log('Hello TS');
" > src/index.ts
```

**Scripts** en `package.json` (añade dentro de `scripts`):

```json
{
  "dev": "ts-node src/index.ts",
  "typecheck": "tsc --noEmit",
  "build": "tsc -p tsconfig.json",
  "start": "node dist/index.js",
  "watch": "tsc -w"
}
```

#### 2.2 Ejecución rápida

```bash
npm run dev        # Ejecuta TS directamente (ts-node)
npm run typecheck  # Verifica tipos sin emitir JS
npm run build      # Emite JS a dist/
node dist/index.js # Ejecuta salida compilada
```

#### 2.3 Archivo de ejercicios `src/01-types.ts`

Incluye ejemplos de cada concepto:

```ts
// 1) Inferencia vs anotación
const anio = 2025;            // number inferido
let curso: string = "TS";     // anotación explícita

// 2) any vs unknown
let a: any = JSON.parse("{}");
let u: unknown = JSON.parse("{\"n\":1}");
// a.n.toFixed();           // OK en tiempo de tipos (peligroso)
// (u as { n: number }).n.toFixed(); // validar/asertar antes

// 3) never
function fail(msg: string): never {
  throw new Error(msg);
}

// 4) as const y non-null assertion
const estado = "ok" as const; // tipo literal "ok"
const root = document.getElementById("app");
// root!.textContent = estado; // usar ! solo si estás seguro

// 5) Tipado estructural (ejemplo simple)
type Persona = { nombre: string; edad: number };
const p = { nombre: "Ada", edad: 36, extra: true };
const q: Persona = p; // compatible por forma
```
1) Inferencia vs anotación

**Idea**: TS infere tipos a partir del valor. Anotá solo cuando el tipo no sea obvio o lo quieras restringir.

**Regla mental**: Preferí inferencia; anota si la API pública o el contrato lo requieren.

**Trampa**: anotar de más puede “encorsetar” y forzar as innecesarios.


2) ```any``` vs ```unknown```

```any```: “apaga” el chequeo de tipos. Propaga incertidumbre y permite cualquier operación → peligroso.

```unknown```: “no sé qué es todavía”; obliga a narrowing/validación antes de usar.

La principal diferencia entre `any` y `unknown` en TypeScript radica en la **seguridad de tipos**: `unknown` es la alternativa segura a `any`.

Para entenderlo mejor, desglosemos sus características y comparémoslas.

---

**El Tipo `any`: La Vía de Escape (Insegura)**

Cuando declaras una variable con el tipo `any`, básicamente le dices al compilador de _TypeScript_: "No te preocupes por esta variable, yo sé lo que hago".

*   **Desactiva la verificación de tipos**: `any` elimina todas las ventajas de seguridad que ofrece TypeScript para esa variable.
*   **Permite cualquier operación**: Puedes acceder a cualquier propiedad, llamar a cualquier método o realizar cualquier operación sobre una variable de tipo `any` sin que TypeScript genere un error en tiempo de compilación, incluso si esa operación es incorrecta y causará un error en tiempo de ejecución.
*   **Se puede asignar a cualquier otro tipo**: Una variable `any` puede ser asignada a una variable de cualquier otro tipo (`string`, `number`, etc.), lo cual puede "contaminar" tu código y ocultar errores.

**Ejemplo con `any`:**
```typescript
let valor: any = "Hola Mundo";

// No hay errores en tiempo de compilación...
valor.toUpperCase(); // Funciona, valor es un string
valor.toFixed(2); // ¡ERROR en tiempo de ejecución! toFixed no existe en string.
                  // TypeScript no te advierte.

let numero: number;
numero = valor; // No hay error, aunque 'valor' sea un string.
```
**Cuándo usar `any`:**
Su uso debe ser muy limitado. Es principalmente útil durante la migración de un proyecto de JavaScript a TypeScript o al interactuar con bibliotecas de terceros que no tienen tipos definidos.

**El Tipo `unknown`: La Alternativa Segura**

`unknown` también te permite asignar cualquier tipo de valor a una variable. La gran diferencia es lo que te permite hacer *después*. `unknown` te obliga a verificar el tipo de la variable antes de poder realizar cualquier operación sobre ella.

*   **Mantiene la seguridad de tipos**: A diferencia de `any`, `unknown` no te deja realizar operaciones arbitrarias.
*   **No permite operaciones sin verificación**: TypeScript te mostrará un error si intentas acceder a propiedades o llamar a métodos en una variable `unknown`.
*   **No se puede asignar a otros tipos (sin validación)**: No puedes asignar una variable `unknown` a una variable con un tipo específico (`string`, `number`, etc.) a menos que primero confirmes su tipo mediante una comprobación.

Para trabajar con un valor `unknown`, debes "estrechar" (narrow) su tipo usando:
*   **Protectores de tipo (Type Guards)**: como `typeof`, `instanceof`.
*   **Aserciones de tipo (Type Assertions)**: usando la palabra clave `as`.

**Ejemplo con `unknown`:**
```ts
let valor: unknown = "Hola Mundo";

// ERROR: 'valor' es de tipo 'unknown'.
// valor.toUpperCase(); // ❌ TypeScript te detiene aquí.

// Forma correcta: verificar el tipo primero
if (typeof valor === 'string') {
  // Dentro de este bloque, TypeScript sabe que 'valor' es un string
  console.log(valor.toUpperCase()); // ✅ Correcto
}

let texto: string;
// ERROR: El tipo 'unknown' no se puede asignar al tipo 'string'.
// texto = valor; // ❌

// Forma correcta: usar aserción después de verificar
if (typeof valor === 'string') {
  texto = valor; // ✅ Correcto
}
```

**Tabla Comparativa: `any` vs. `unknown`**

| Característica | `any` | `unknown` |
| :--- | :--- | :--- |
| **Asignar cualquier valor** | ✅ Sí | ✅ Sí |
| **Seguridad de tipos** | ❌ No (desactiva el chequeo) | ✅ Sí (obliga a chequear) |
| **Acceder a propiedades** | ✅ Sí (sin verificación) | ❌ No (requiere verificación) |
| **Asignar a otros tipos** | ✅ Sí | ❌ No (requiere verificación) |
| **Caso de uso principal** | Migración de JS, librerías sin tipos. | Datos de fuentes externas (APIs, formularios). |
**Regla mental**: Si viene de JSON o input externo, usa unknown y valida.

**Patrón**: type guards, zod, in, typeof, Array.isArray, etc.

---

3) `never`: **(el arte de manejar lo imposible)**

El tipo `never` representa un valor que **nunca debería ocurrir**. No es `void` (que significa que una función no retorna un valor), sino que indica que la función **jamás termina su ejecución normal**.

Esto sucede principalmente en dos casos:

a.  Una función que siempre lanza un error (`throw new Error(...)`).

b.  Una función que contiene un bucle infinito (`while (true) {}`).

**Su uso más importante: Garantizar la exhaustividad**

La verdadera magia de `never` aparece al usarlo con uniones discriminadas para asegurar que has manejado todos los casos posibles en un `switch` o `if/else`.

**La técnica es simple**: en el bloque `default` (o el `else` final), intentas asignar la variable a un tipo `never`. Si has cubierto todos los casos, *Typescript* sabe que ese bloque es inalcanzable y el código es válido. Si olvidas un caso, el código dará un error.

**Ejemplo Práctico:**

```ts
type Estado = "cargando" | "exito" | "error";

function manejarEstado(estado: Estado) {
  switch (estado) {
    case "cargando":
      // ... lógica para cargando
      break;
    case "exito":
      // ... lógica para éxito
      break;
    // OLVIDAMOS MANEJAR EL CASO "error" INTENCIONADAMENTE
  
    default:
      // TypeScript ve que 'estado' aquí SÓLO puede ser "error".
      // Intentar asignarlo a 'never' causa un error de compilación.
      const casoImposible: never = estado; // ❌ Error: El tipo 'string' ("error") no se puede asignar al tipo 'never'.
  }
}
```

**Regla Mental:** Piensa en `never` como una afirmación. Al usarlo, le dices a *Typescript*: "Estoy seguro de que esta parte del código nunca se ejecutará". Si te equivocas (porque olvidaste un caso), *Typescript* te lo señalará con un error, salvándote de futuros bugs.

4) ```as const``` y ```non-null assertion``` (!)

```as const```: Convierte valores a literales y propiedades a readonly. Evita el “widening” ("ok" en vez de string, 1 en vez de number).

Útil para discriminantes, config y tuplas.

```! non-null```: Le decís a TS “sé que no es null/undefined”. No chequeará en runtime.

**Regla mental**: úsalo solo si realmente podés garantizarlo; preferí narrowing u opcional encadenado.

5) Tipado estructural

**Idea clave**: compatibilidad por forma, no por nombre. Si un objeto contiene lo que el tipo pide, es asignable.

**Extra fields**: no molestan salvo en excess property checks con literales directos.

**Regla mental**: A → B si A tiene al menos las props de B con tipos compatibles.

**Ejecuta**:

```bash
npm run dev
npm run typecheck
```

#### Ejercicios opcionales
1. **Inferencia**: declara 5 constantes con valores variados y describe qué tipo infiere TS.
2. **`unknown` vs `any`**: crea una función `parseoSeguro` que reciba `unknown` y devuelva un número validado o lance error.
3. **Aserciones**: convierte un objeto a literal con `as const` y verifica que sea `readonly`.
4. **`never`**: implementa una función `exhaustiveCheck(x: never): never` y úsala en un `switch` (simulación; *narrowing* se ve la sem 2).
5. **Build**: compila con `npm run build` y sube `dist/` al `.gitignore`.


### 3) Preguntas frecuentes

* **¿`any` es malo?** No siempre, pero reduce garantías. Prefiere `unknown` + validación.
* **¿Debo tipar todo?** No. Confía en la **inferencia** cuando el valor es claro.
* **¿Cuándo usar `!`?** Solo si has verificado la existencia por otra vía (p. ej., en HTML está el elemento). Úsalo con moderación.

## Documentación Básica de Estructuras de Control en TypeScript

TypeScript, al ser un superconjunto de JavaScript, comparte sus estructuras de control de flujo. Estas estructuras te permiten dirigir la ejecución de tu programa basándose en condiciones, repitiendo acciones y manejando errores.

### 1. Condicionales: Toma de Decisiones

Los condicionales ejecutan bloques de código solo si se cumplen ciertas condiciones.

#### `if / else / else if`

Es la estructura condicional más básica. Evalúa una condición y ejecuta un bloque de código si es verdadera. Opcionalmente, puede tener bloques `else if` para evaluar condiciones adicionales y un bloque `else` final que se ejecuta si ninguna de las condiciones anteriores es verdadera.

```ts
let temperatura: number = 25;

if (temperatura > 30) {
  console.log("Hace mucho calor.");
} else if (temperatura > 20) {
  console.log("El clima es agradable.");
} else {
  console.log("Hace frío.");
}
```

#### `switch`

Es útil cuando se necesita comparar una sola variable contra múltiples valores posibles. Es una alternativa más limpia a una cadena larga de `if/else if`.

Cada `case` se compara con el valor de la variable. La declaración `break` es crucial para salir del `switch` una vez que se encuentra una coincidencia. El bloque `default` es opcional y se ejecuta si ningún `case` coincide.

```ts
type NivelUsuario = "admin" | "editor" | "visitante";
let nivel: NivelUsuario = "admin";

switch (nivel) {
  case "admin":
    console.log("Acceso total.");
    break;
  case "editor":
    console.log("Puede editar contenido.");
    break;
  case "visitante":
    console.log("Solo puede ver el contenido.");
    break;
  default:
    console.log("Nivel de usuario no reconocido.");
}
```

### 2. Bucles: Ejecución Repetitiva

Los bucles te permiten ejecutar un bloque de código múltiples veces.

#### `for`

El bucle `for` tradicional es ideal cuando sabes de antemano cuántas veces quieres que se repita el bucle. Consta de tres partes: una inicialización, una condición y una expresión de incremento/decremento.

```ts
// Imprime los números del 0 al 4
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

#### `for...of`

Este bucle itera sobre los valores de objetos iterables como arrays, strings, Sets o Maps. Es la forma más moderna y legible de recorrer los elementos de una colección.

```ts
const frutas: string[] = ["manzana", "banana", "cereza"];

for (const fruta of frutas) {
  console.log(fruta);
}
```

#### `for...in`

Este bucle itera sobre las claves (o propiedades enumerables) de un objeto.

```ts
const usuario = {
  nombre: "Ana",
  edad: 30
};

for (const clave in usuario) {
  console.log(`${clave}: ${usuario[clave]}`);
}
```

#### `while`

El bucle `while` ejecuta un bloque de código mientras una condición especificada sea verdadera. La condición se evalúa *antes* de cada iteración.

```ts
let contador: number = 0;

while (contador < 3) {
  console.log("Hola");
  contador++;
}
```

#### `do...while`

Es similar al bucle `while`, pero con una diferencia clave: la condición se evalúa *después* de ejecutar el bloque de código. Esto garantiza que el bloque se ejecute al menos una vez.

```ts
let numero: number = 5;

do {
  console.log("Este mensaje se muestra al menos una vez.");
  numero++;
} while (numero < 5);
```

### 3. Control de Bucles

Estas declaraciones te permiten alterar el flujo normal de un bucle.

#### `break`

Termina la ejecución del bucle actual (o `switch`) de forma inmediata y transfiere el control a la siguiente instrucción después del bucle.

```ts
for (let i = 0; i < 10; i++) {
  if (i === 5) {
    break; // El bucle se detiene cuando i es 5
  }
  console.log(i); // Imprimirá de 0 a 4
}
```

#### `continue`

Omite el resto del código en la iteración actual y pasa directamente a la siguiente iteración del bucle.

```ts
for (let i = 0; i < 5; i++) {
  if (i === 2) {
    continue; // Se salta la iteración donde i es 2
  }
  console.log(i); // Imprimirá 0, 1, 3, 4
}
```

### 4. Manejo de Errores

Permite manejar errores de tiempo de ejecución de una manera controlada.

#### `try / catch / finally`

*   **`try`**: Encierra el código que podría lanzar una excepción.
*   **`catch`**: Captura y maneja la excepción si ocurre una en el bloque `try`.
*   **`finally`**: Este bloque se ejecuta siempre, independientemente de si se lanzó una excepción o no. Es útil para limpiar recursos.

```ts
try {
  // Intenta ejecutar un código que puede fallar
  let resultado = JSON.parse("{'nombre': 'Juan', 'edad': 30}"); // JSON inválido
  console.log(resultado);
} catch (error) {
  // Este bloque se ejecuta si hay un error en el 'try'
  console.error("Ocurrió un error al procesar el JSON:", error.message);
} finally {
  // Este bloque se ejecuta siempre
  console.log("La operación ha finalizado.");
}
```

## Construcción de tipos: `type` vs `interface`, *narrowing*, uniones/intersecciones

**Objetivos**

* Modelar datos con compatibilidad estructural, tuplas, `readonly`, `enum` (pros/contras).

### 1) Teoría

#### `type` vs. `interface` en TypeScript: ¿Cuál y Cuándo Usar?

Tanto `type` como `interface` son herramientas de TypeScript para definir "contratos" o "formas" que los datos deben cumplir. En muchos casos son intercambiables, pero tienen diferencias clave que los hacen más adecuados para ciertas situaciones.

### Semejanzas Fundamentales

Antes de ver las diferencias, es importante saber que ambos pueden:
*   Describir la forma de un objeto o una función.
*   Extenderse o heredar de otros tipos (usando `extends` en `interface` y uniones/intersecciones `&` en `type`).
*   Ser implementados por una clase (`class MiClase implements MiInterfaz {}`).
*   Usar genéricos (`<T>`), propiedades opcionales (`?`), de solo lectura (`readonly`) y firmas de índice (`[key: string]: any`).

##### Diferencias Clave

Aquí es donde la elección se vuelve importante.

###### 1. 🧩 Extensibilidad: `interface` se puede fusionar (*Declaration Merging*)

Una `interface` se puede definir varias veces en el mismo ámbito. TypeScript las combina automáticamente en una sola declaración. Esto es extremadamente útil para extender tipos existentes de forma segura.

**`interface` (se fusiona):**
```ts
// Declaración inicial
interface Usuario {
  id: string;
}

// En otro archivo o más abajo, la extendemos
interface Usuario {
  nombre: string;
}

// TypeScript la ve como una sola interfaz
const miUsuario: Usuario = {
  id: "abc-123",
  nombre: "Ana", // Ambas propiedades son requeridas
};
```
Esta característica hace que `interface` sea ideal para trabajar con tipos que pueden ser extendidos por terceros, como los tipos del DOM o en el desarrollo de librerías.

`type`, en cambio, no se puede reabrir. Si intentas declarar el mismo `type` dos veces, obtendrás un error.

###### 2. 🌀 Versatilidad: `type` puede ser un alias para cualquier tipo

Mientras que una `interface` solo puede describir la forma de un objeto o función, un `type` es un **alias** que puede representar cualquier tipo, incluyendo:
*   **Uniones**: `string | number`
*   **Tuplas**: `[number, number]`
*   **Tipos primitivos**: `string`, `boolean`
*   **Tipos avanzados**: *Mapped Types* y *Conditional Types*.

**`type` (alias versátil):**
```ts
// Un alias para una unión de tipos
type Id = string | number;

// Un alias para una tupla
type Coordenada = [x: number, y: number];

// Un alias para un tipo de función
type Callback = (data: string) => void;

// Usando tipos avanzados (imposible con interface)
type ClavesDeUsuario = keyof Usuario; // "id" | "nombre"
```

### Tabla Comparativa Rápida

| Característica | `interface` | `type` |
| :--- | :--- | :--- |
| **Describe objetos/funciones** | ✅ Sí | ✅ Sí |
| **Puede fusionarse (Merging)** | ✅ Sí | ❌ No |
| **Alias para uniones, tuplas, primitivos** | ❌ No | ✅ Sí |
| **Uso con Mapped/Conditional Types** | ❌ No | ✅ Sí |

### Recomendación Práctica: ¿Cuándo Usar Cada Uno?

Basado en estas diferencias, aquí tienes una guía simple:

➡️ **Usa `interface` cuando:**
*   Estás definiendo un contrato para un **objeto** o una **clase**.
*   Esperas que otros puedan extender tu contrato (por ejemplo, al crear una API pública o una librería).

➡️ **Usa `type` cuando:**
*   Necesitas definir un alias para un tipo primitivo, una unión, o una tupla.
*   Necesitas usar tipos avanzados como *mapped types* o *conditional types*.

**¿Y para el código de mi aplicación?**
Si no estás creando una librería, la elección entre `type` e `interface` para describir objetos es a menudo una cuestión de preferencia. Lo más importante es **ser consistente** dentro de tu proyecto.


#### 1.3 Uniones (`|`) e Intersecciones (`&`): Combinando Tipos en TypeScript

En _TypeScript_, las uniones y las intersecciones son dos herramientas fundamentales que te permiten crear tipos nuevos y flexibles a partir de otros ya existentes.

##### 1. Unión (`|`): El tipo "O"

Una unión crea un tipo que puede ser **uno de varios tipos posibles**. Piensa en el operador `|` como un "O" lógico. Un valor de este tipo debe satisfacer la forma de *al menos uno* de los tipos de la unión.

**¿Para qué es útil?**
Es perfecto para modelar situaciones donde un valor puede tener múltiples formas, como los diferentes estados de una aplicación, respuestas de una API o parámetros de una función.

**Ejemplo Práctico: Manejo de Estados**

Imagina que estás cargando datos. El estado solo puede ser `"cargando"`, `"exito"` o `"error"`. Una unión de tipos literales es la herramienta perfecta para esto.

```ts
// Define una unión de literales para representar los posibles estados
type EstadoDeCarga = "cargando" | "exito" | "error";

function mostrarMensaje(estado: EstadoDeCarga) {
  if (estado === "cargando") {
    console.log("Loading data...");
  } else if (estado === "exito") {
    console.log("¡Datos cargados correctamente!");
  } else {
    // Gracias a la unión, TypeScript sabe que la única opción restante es "error"
    console.error("Hubo un fallo en la carga.");
  }
}

mostrarMensaje("exito"); // Muestra: "¡Datos cargados correctamente!"
// mostrarMensaje("pendiente"); // ❌ Error: "pendiente" no es un valor válido para el tipo EstadoDeCarga.
```

##### 2. Intersección (`&`): El tipo "Y"

Una intersección crea un nuevo tipo que **combina todas las propiedades de los tipos existentes**. Piensa en el operador `&` como un "Y" lógico. Un valor de este tipo debe satisfacer las formas de *todos* los tipos de la intersección simultáneamente.

**¿Para qué es útil?**
Es ideal para componer tipos complejos a partir de piezas más pequeñas y reutilizables, como si estuvieras mezclando diferentes características.

**Ejemplo Práctico: Composición de Objetos**

Supongamos que en tu base de datos, cualquier registro tiene un `id`, y algunos también tienen marcas de tiempo (`timestamps`). Puedes modelar esto de forma muy limpia.

```ts
type ConIdentificador = {
  id: string;
};

type ConTimestamps = {
  createdAt: Date;
  updatedAt: Date;
};

// Un registro de la base de datos debe tener AMBAS cosas: un ID Y timestamps.
type RegistroDB = ConIdentificador & ConTimestamps;

const usuario: RegistroDB = {
  id: "user-123",
  createdAt: new Date(),
  updatedAt: new Date(), // Todas las propiedades son obligatorias.
};
```

##### Resumen Visual: `|` vs. `&`

| Característica | Unión (`A \| B`) | Intersección (`A & B`) |
| :--- | :--- | :--- |
| **Lógica** | "O" (es A o es B) | "Y" (es A y también es B) |
| **Propiedades (Objetos)**| Debe tener las propiedades comunes a A y B. | Debe tener **todas** las propiedades de A y de B. |
| **Caso de uso principal** | Modelar valores que pueden ser de diferentes tipos (ej: `string | number`, estados). | Componer y mezclar tipos de objetos para crear formas más complejas. |

#### 1.3 Tipos Literales y Uniones Discriminadas (*Discriminated Unions*)

Estos dos conceptos, al combinarse, crean uno de los patrones más potentes y seguros en *Typescript* para manejar datos que pueden tener diferentes "formas" o "estados".

*   **Tipos Literales**: Un tipo literal es un tipo tan específico que solo permite un valor exacto. En lugar de permitir cualquier `string`, puedes especificar que una variable *solo* puede ser el string `"ok"`, `"error"`, el número `1` o el booleano `true`. Esto aumenta enormemente la predictibilidad de tu código.

*   **Uniones Discriminadas**: Son un patrón avanzado que combina uniones (`|`) y tipos literales para crear tipos "inteligentes". La idea es usar una propiedad común con un tipo literal (el **discriminante**, usualmente llamado `kind`, `type` o `status`) para que *Typescript* pueda deducir ("estrechar" o *narrowing*) de forma exacta qué forma tiene el objeto dentro de un bloque de código.

**La Receta para una Unión Discriminada:**
1.  Define varios tipos de objeto.
2.  Añade a cada uno una propiedad común (ej. `kind`) con un valor literal **único**.
3.  Crea un tipo unión que agrupe a todos los anteriores.

**Ejemplo en acción:**

Imaginemos que queremos modelar el estado de un producto en un inventario.

```ts
// Cada "estado" tiene una forma diferente, pero comparte la propiedad "kind".
type Disponible = {
  kind: "disponible"; // El discriminante
  stock: number;
};

type Discontinuado = {
  kind: "discontinuado"; // El discriminante
  razon: string;
};

// 3. La unión que agrupa todos los posibles estados.
type EstadoProducto = Disponible | Discontinuado;
```

**La magia del _estrechamiento exhaustivo_ (*Exhaustive Narrowing*)**

Ahora, al usar una estructura de control como `switch`, *Typescript* puede identificar qué propiedades están disponibles en cada caso, eliminando por completo una categoría de errores.

```ts
function obtenerDetalleProducto(producto: EstadoProducto): string {
  switch (producto.kind) {
    case "disponible":
      // Dentro de este bloque, Typescript SABE que 'producto' es de tipo 'Disponible'.
      // Por eso, nos da autocompletado para `producto.stock`.
      return `Hay ${producto.stock} unidades en el inventario.`;

    case "discontinuado":
      // Aquí, Typescript SABE que 'producto' es de tipo 'Discontinuado'.
      // Acceder a `producto.stock` daría un error.
      return `Producto discontinuado por la siguiente razón: ${producto.razon}.`;
  }
}
```

Este patrón es extremadamente robusto. Si en el futuro añadieras un nuevo estado (ej. `type Proximamente = { kind: "proximamente"; fechaLanzamiento: Date }`) a la unión `EstadoProducto`, *Typescript* te daría un error en la función `obtenerDetalleProducto`, forzándote a manejar ese nuevo caso. Esto garantiza que nunca olvides actualizar tu lógica.

#### 1.4 Tuplas, `readonly` y la alternativa a los `enum`

Estos conceptos de *Typescript* te permiten crear estructuras de datos más estrictas, predecibles y seguras.

*   **Tuplas: Arrays con Estructura Fija**

    Una tupla es como un array con reglas muy estrictas: tiene una **longitud fija** y un **tipo de dato específico para cada posición**. Esto es ideal para representar datos que tienen una estructura interna, como un par de coordenadas o, en este caso, una cantidad monetaria.

    ```ts
    // Una tupla que SIEMPRE tendrá dos elementos: un número y luego un string.
    type ParCoordenada = [number, string];
    const miPar: ParCoordenada = [10, "Norte"]; // ✅ Válido
    // const otroPar: ParCoordenada = ["Sur", 20]; // ❌ Error de tipo
    // const parIncompleto: ParCoordenada = [10]; // ❌ Error de longitud
    ```

*   **`readonly`: Garantizando la Inmutabilidad**

    El modificador `readonly` se puede aplicar a propiedades de objetos, arrays o tuplas para evitar que sean modificados después de su creación. Esto ayuda a prevenir errores causados por mutaciones accidentales.

    ```ts
    const numeros: readonly number[] = [1, 2, 3];
    // numeros.push(4); // ❌ Error: La propiedad 'push' no existe en 'readonly number[]'.
    ```

*   **`enum` vs. Unión de Literales: La Alternativa Moderna**

    Tradicionalmente, para representar un conjunto de constantes con nombre, se usaban los `enum`. Sin embargo, los `enum` generan un objeto real en el JavaScript compilado, lo que puede tener implicaciones en el tamaño del paquete final y su optimización (*tree-shaking*).

    Hoy en día, la alternativa preferida en la mayoría de los casos es una **unión de tipos literales**. Es más ligera (desaparece en la compilación), más simple y a menudo más segura.

    ```ts
    // Alternativa con enum (genera código JS)
    enum MonedaEnum {
      ARS = "ARS",
      USD = "USD",
    }
    // Alternativa moderna con unión de literales (solo existe en tiempo de compilación)
    type MonedaLiteral = "ARS" | "USD";
    ```

**Ejemplo Combinado: Un Tipo de Dato Robusto**

Podemos combinar estos tres conceptos para crear un tipo `Dinero` que sea seguro, inmutable y descriptivo.

```ts
// Esta tupla:
// 1. Es `readonly`: no se puede modificar una vez creada.
// 2. Tiene una estructura fija: un número seguido de un string.
// 3. Usa etiquetas (`monto`, `moneda`) para mejorar la legibilidad.
// 4. Usa una unión de literales para restringir la moneda a valores válidos.
type Dinero = readonly [monto: number, moneda: "ARS" | "USD"];

const precio: Dinero = [2500, "ARS"];

// precio[0] = 3000; // ❌ Error: La tupla es de solo lectura.
// precio.push("EUR"); // ❌ Error: La tupla es de solo lectura y tiene longitud fija.
// const precioInvalido: Dinero = [100, "EUR"]; // ❌ Error: "EUR" no es un tipo de moneda válido.
```

#### 1.5 *Narrowing*: Cómo *Typescript* Entiende tu Código

*Narrowing* (o "estrechamiento") es el proceso que realiza *Typescript* para deducir un tipo más específico para una variable dentro de un bloque de código. Después de realizar una comprobación, *Typescript* es lo suficientemente inteligente como para saber que la variable tiene una forma más concreta, desbloqueando así el autocompletado y la seguridad de tipos.

Estas son las herramientas principales para lograrlo:

**1. `typeof`: Para Tipos Primitivos**

Es la forma más común de diferenciar entre tipos primitivos como `string`, `number`, `boolean`, etc.

```ts
function procesar(valor: string | number) {
  if (typeof valor === "string") {
    // Dentro de este bloque, TypeScript sabe que 'valor' es SÓLO un string.
    // Por lo tanto, `valor.toUpperCase()` es una operación segura.
    return valor.toUpperCase();
  }
  // Fuera del if, TypeScript deduce que 'valor' debe ser un number.
  return valor.toFixed(2);
}
```

**2. El operador `in`: Para Verificar Propiedades en Objetos**

Se utiliza para determinar si un objeto tiene una propiedad con un nombre específico. Es muy útil para diferenciar entre las distintas formas que puede tener un objeto en una unión.

```ts
type Disponible = { stock: number };
type Discontinuado = { razon: string };
type EstadoProducto = Disponible | Discontinuado;

function obtenerStock(producto: EstadoProducto): number {
  if ("stock" in producto) {
    // Si la propiedad "stock" existe, TypeScript sabe que 'producto' es de tipo 'Disponible'.
    return producto.stock;
  }
  // Si no, debe ser de tipo 'Discontinuado'.
  return 0;
}
```

**3. `instanceof`: Para Instancias de Clases**

Funciona de manera similar a `typeof`, pero en el mundo de las clases. Verifica si un objeto es una instancia de una clase específica (o de una que herede de ella).

```ts
class Caja {
  constructor(public valor: number) {}
}

function desempaquetar(item: number | Caja): number {
  if (item instanceof Caja) {
    // En este bloque, TypeScript sabe que 'item' es una instancia de 'Caja'.
    // Por lo tanto, `item.valor` es un acceso seguro.
    return item.valor;
  }
  // Si no es una instancia de Caja, debe ser un número.
  return item;
}
```

**4. Predicados de Tipo (`is`): Creando tus Propias Validaciones**

A veces, la lógica para validar un tipo es más compleja y necesitas encapsularla en una función. Un predicado de tipo es una firma de retorno especial (`parametro is Tipo`) que le dice a *Typescript*: "Si esta función devuelve `true`, puedes confiar en que el parámetro que le pasé es de este tipo más específico".

```ts
// Definimos de nuevo los tipos de producto, pero esta vez con un discriminante.
type Disponible = { kind: "disponible"; stock: number };
type Discontinuado = { kind: "discontinuado"; razon: string };
type EstadoProducto = Disponible | Discontinuado;

// La función predicado: su retorno le "enseña" a TypeScript.
function esDisponible(producto: EstadoProducto): producto is Disponible {
  return producto.kind === "disponible";
}

function manejarProducto(producto: EstadoProducto) {
  if (esDisponible(producto)) {
    // Gracias al predicado, TypeScript sabe que 'producto' es 'Disponible' aquí.
    console.log(`Tenemos ${producto.stock} en inventario.`);
  }
}
```
---

### 2) Práctica

Crea los archivos de esta semana dentro de `src/` y ejecuta `npm run typecheck` frecuentemente.

#### 2.1 Modelado básico (`src/02-modelado.ts`)

**Objetivo**: modelar un catálogo con tipos sólidos y hacer *narrowing* seguro.

```ts
// Identidades y literales
type SKU = `${string}-${number}`

type Moneda = "ARS" | "USD"
export type Dinero = readonly [monto: number, moneda: Moneda]

// Formas base
type BaseProducto = { sku: SKU; nombre: string; precio: Dinero }

type Disponible = { kind: "disp"; stock: number }
type Discontinuado = { kind: "disc"; razon: string }
export type EstadoProducto = Disponible | Discontinuado

export type Producto = BaseProducto & { estado: EstadoProducto }

// Guards y utilidades
export function esDisponible(e: EstadoProducto): e is Disponible {
  return e.kind === "disp"
}

export function precioEnARS([m, mon]: Dinero, tc: number): number {
  return mon === "USD" ? Math.round(m * tc) : m
}

export function puedeVender(p: Producto): boolean {
  if (esDisponible(p.estado)) return p.estado.stock > 0
  return false
}

// Ejemplos
const p1: Producto = {
  sku: "abc-101",
  nombre: "Teclado",
  precio: [100, "USD"],
  estado: { kind: "disp", stock: 5 }
}

const p2: Producto = {
  sku: "abc-102",
  nombre: "Mouse",
  precio: [15000, "ARS"],
  estado: { kind: "disc", razon: "Reemplazado por nuevo modelo" }
}

console.log("p1 en ARS:", precioEnARS(p1.precio, 1000))
console.log("¿p1 vendible?", puedeVender(p1))
console.log("¿p2 vendible?", puedeVender(p2))
```

**Explicación**:

 **Identidades y Literales**

Aquí se definen tipos básicos que actúan como "identidades" o valores específicos.

*   **`type SKU = `${string}-${number}``**

    *   `SKU` significa "Stock Keeping Unit" (unidad de mantenimiento de existencias).
    *   Este es un **tipo de cadena literal de plantilla**. Significa que un valor de `SKU` debe ser una cadena que comienza con cualquier cadena (`string`), seguida de un guion (`-`), y luego por cualquier número (`number`).

*   **`type Moneda = "ARS" | "USD"`**
       *   `Moneda` es un **tipo de unión literal de cadena**. Significa que una variable de tipo `Moneda` solo puede tener el valor `"ARS"` (pesos argentinos) o `"USD"` (dólares estadounidenses). No se permiten otros valores.

*   **`export type Dinero = readonly [monto: number, moneda: Moneda]`**
      *   `Dinero` es una **tupla `readonly`**.
   Una tupla es un array con un número fijo de elementos y tipos conocidos para cada elemento.
      *   `readonly` significa que una vez creada, no se pueden cambiar los elementos de la tupla.
 Tiene dos elementos:
        *   `monto`: Un `number` que representa la cantidad de dinero.
        *   `moneda`: Una `Moneda` (ya sea `"ARS"` o `"USD"`).
   Los nombres `monto` y `moneda` son etiquetas opcionales para mejorar la legibilidad, pero no cambian el tipo subyacente.

**Formas Base**
Estos tipos definen la estructura principal de un producto.

*   **`type BaseProducto = { sku: SKU; nombre: string; precio: Dinero }`**
Este es un **tipo de objeto** que define las propiedades comunes a cualquier producto.
      *   `sku`: De tipo `SKU` (nuestro formato `string-number`).
      *   `nombre`: Una `string` para el nombre del producto.
      *   `precio`: De tipo `Dinero` (nuestra tupla `[monto, moneda]`).
*   **`type Disponible = { kind: "disp"; stock: number }`**
      *   Este es un tipo de objeto que representa el estado de un producto **disponible**.
      *   `kind: "disp"`: Una **propiedad literal** que actúa como un "discriminador". Esto es clave para distinguir entre los diferentes estados de un producto. Si `kind` es `"disp"`, sabemos que es un producto disponible.
      *   `stock`: Un `number` que indica la cantidad de unidades en stock.
*   **`type Discontinuado = { kind: "disc"; razon: string }`**
      *   Similar a `Disponible`, pero para productos **discontinuados**.
      *   `kind: "disc"`: El discriminador para este estado.
      *   `razon`: Una `string` que explica por qué el producto fue discontinuado.
*   **`export type EstadoProducto = Disponible | Discontinuado`**
      *   Este es un **tipo de unión**. Un `EstadoProducto` puede ser *o* `Disponible` *o* `Discontinuado`.
      *   La propiedad `kind` (`"disp"` o `"disc"`) permite a TypeScript (y a nosotros) saber qué tipo específico de `EstadoProducto` estamos tratando en un momento dado, lo que habilita la **reducción de tipos (type narrowing)**.
*   **`export type Producto = BaseProducto & { estado: EstadoProducto }`**
      *   Este es un **tipo de intersección**. Combina las propiedades de `BaseProducto` con una nueva propiedad `estado`.
      *   Un `Producto` tiene `sku`, `nombre`, `precio` (de `BaseProducto`) y `estado` (que puede ser `Disponible` o `Discontinuado`).
**Guards y Utilidades**
Estas funciones ayudan a trabajar con los tipos definidos.
*   **`export function esDisponible(e: EstadoProducto): e is Disponible { return e.kind === "disp" }`**
      *   Esta es una **función guard de tipo (type guard)**.
      *   Toma un `EstadoProducto` (`e`).
      *   La parte `e is Disponible` es la clave: le dice a TypeScript que si esta función devuelve `true`, entonces `e` no es solo un `EstadoProducto` genérico, ¡sino que se ha reducido su tipo a `Disponible`!
     *   Internamente, verifica el discriminador `e.kind === "disp"`.
*   **`export function precioEnARS([m, mon]: Dinero, tc: number): number { return mon === "USD" ? Math.round(m * tc) : m }`**
    *   Esta función calcula el precio de un `Dinero` en Pesos Argentinos (ARS).
      *   `[m, mon]: Dinero`: Utiliza la **desestructuración de tuplas** directamente en los parámetros para extraer `m` (monto) y `mon` (moneda) de la tupla `Dinero`.
      *   `tc: number`: Es el tipo de cambio (tasa de conversión).
      *   Si la moneda es `"USD"`, convierte el monto multiplicándolo por el tipo de cambio y lo redondea. Si es `"ARS"`, devuelve el monto directamente.
*   **`export function puedeVender(p: Producto): boolean { if (esDisponible(p.estado)) return p.estado.stock  0 return false }`**
      *   Esta función determina si un `Producto` se puede vender.
      *   `if (esDisponible(p.estado))`: Aquí es donde entra en juego la función guard `esDisponible`. Dentro de este bloque `if`, TypeScript sabe que `p.estado` es de tipo `Disponible`, por lo que podemos acceder a `p.estado.stock` sin errores.
      *   Si el producto está disponible y tiene stock mayor que 0, se puede vender. De lo contrario, no.

**Ejemplos**

Finalmente, se muestran ejemplos de cómo usar los tipos y funciones.

*   **`const p1: Producto = { ... }`**
      *   Se crea un producto `p1` con un `sku` válido, nombre, precio en USD, y un estado `Disponible` con 5 unidades de stock.
*   **`const p2: Producto = { ... }`**
    *   Se crea un producto `p2` con un `sku` válido, nombre, precio en ARS, y un estado `Discontinuado` con una razón.
*   **`console.log("p1 en ARS:", precioEnARS(p1.precio, 1000))`**
    *   Llama a `precioEnARS` para `p1`. `p1.precio` es `[100, "USD"]`. Con un tipo de cambio de 1000, esto debería resultar en 100000.
*   **`console.log("¿p1 vendible?", puedeVender(p1))`**
    *   Llama a `puedeVender` para `p1`. Dado que `p1` está disponible y tiene `stock: 5`, debería devolver `true`.
*   **`console.log("¿p2 vendible?", puedeVender(p2))`**
    *   Llama a `puedeVender` para `p2`. Dado que `p2` está discontinuado (`kind: "disc"`), la función `esDisponible` devolverá `false`, y por lo tanto `puedeVender` devolverá `false`.

**Resumen de Conceptos Clave Utilizados**:

*   **Tipos Primitivos:** `string`, `number`, `boolean`.
*   **Literales de Tipo:** `"ARS"`, `"USD"`, `"disp"`, `"disc"`.
*   **Uniones (`|`):** Para combinar varios tipos (ej. `Moneda`, `EstadoProducto`).
*   **Intersecciones (`&`):** Para combinar propiedades de objetos (ej. `Producto`).
*   **Tuplas:** Arrays con longitud fija y tipos predefinidos por posición (ej. `Dinero`).
*   **Tuplas `readonly`:** Para asegurar que los elementos de la tupla no se modifiquen después de la creación.
*   **Tipos de Cadena Literal de Plantilla:** Para definir patrones de cadenas (ej. `SKU`).
*   **Discriminadores:** Propiedades literales que permiten a TypeScript reducir el tipo de una unión (ej. `kind` en `EstadoProducto`).
*   **Guards de Tipo (`is Type`):** Funciones que le indican a TypeScript cuándo un valor es de un tipo más específico.
*   **Desestructuración:** Para extraer valores de objetos o arrays/tuplas fácilmente.

**Ejecuta**:

```bash
npm run typecheck
npm run dev -- src/02-modelado.ts
```

> Si tu script `dev` no acepta ruta, usa `ts-node src/02-modelado.ts` o crea un script `"dev:file": "ts-node"` y ejecuta `npm run dev:file src/02-modelado.ts`.

#### 2.2 Tuplas y `readonly` (`src/02-tuplas.ts`)

**Objetivo**: forzar posiciones y evitar mutaciones accidentales.

```ts
export type Coordenada = readonly [lat: number, lon: number]
const casa: Coordenada = [ -38.72, -62.27 ]
// casa[0] = 0 // Error: readonly

// ejemplo de zip con tuplas
export function zip<T, U>(a: readonly T[], b: readonly U[]): ReadonlyArray<readonly [T, U]> {
  const len = Math.min(a.length, b.length)
  const r: Array<readonly [T, U]> = []
  for (let i = 0; i < len; i++) r.push([a[i], b[i]] as const)
  return r
}
```

#### 2.3 `enum` vs unión de literales (`src/02-enum-union.ts`)

**Objetivo**: comparar ergonomía y *DX*.

```ts
// Unión de literales
export type Rol = "admin" | "editor" | "viewer"

// enum (alternativa)
export enum RolEnum { Admin = "admin", Editor = "editor", Viewer = "viewer" }

export function puedeEditar(r: Rol | RolEnum) {
  const v = typeof r === "string" ? r : r.toString()
  return v === "admin" || v === "editor"
}
```

#### 2.4 Predicados y *exhaustiveness* (`src/02-guards.ts`)

**Objetivo**: usar *type predicates* y chequeo exhaustivo.

```ts
import { EstadoProducto } from "./02-modelado"

type Cargado = { k: "ok"; data: number[] }
type Cargando = { k: "load" }
type ErrorNet = { k: "err"; msg: string }

type Estado = Cargado | Cargando | ErrorNet

function esCargado(e: Estado): e is Cargado { return e.k === "ok" }

function assertNever(x: never): never { throw new Error("Estado desconocido: " + JSON.stringify(x)) }

export function render(e: Estado): string {
  if (esCargado(e)) return `items: ${e.data.length}`
  if (e.k === "load") return "cargando…"
  if (e.k === "err") return `error: ${e.msg}`
  return assertNever(e) // fuerza exhaustividad
}
```

---

### 3) Ejercicios opcionales

1. **`type` vs `interface`**: modela `Usuario` con ambos; extiende `interface` vía *merging* y crea un `type` unión `Activo | Suspendido`.
2. **Discriminated union**: `Pago` con `{ kind: "cash"|"card"|"mp" }` y funciones que procesen cada caso con *exhaustiveness*.
3. **Tuplas/readonly**: define `RangoFechas = readonly [inicio: Date, fin: Date]` y valida orden.
4. **Narrowing**: implementa `safeLength(x: string | { length: number } | null): number` sin usar `!`.
5. **Enum vs unión**: representa roles `admin/editor/viewer` de dos formas y comenta pros/contras en README.

---

### 4) Comandos útiles

```bash
npm run typecheck
npm run dev -- src/02-modelado.ts
npm run dev -- src/02-tuplas.ts
npm run dev -- src/02-enum-union.ts
npm run dev -- src/02-guards.ts
```
