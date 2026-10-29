## Módulos, resolución, *barrels*, `exports` y declaraciones `.d.ts`

**Objetivos**

* Entender resolución de módulos, *barrels*, *module augmentation* y tipados de terceros.

### 1) Teoría
#### 1.1 ES Modules (ESM) vs. CommonJS (CJS): Los Dos Sistemas de Módulos

En el ecosistema de JavaScript, coexisten dos sistemas principales para organizar y compartir código entre archivos. Entenderlos es clave para configurar correctamente tu paquete.

*   **CommonJS (CJS): El Sistema Histórico de Node.js**
    *   **Sintaxis:** Usa `require()` para importar y `module.exports` para exportar.
    *   **Características:** Es un sistema dinámico y síncrono. Cuando Node.js encuentra un `require()`, detiene la ejecución, carga y ejecuta el archivo, y luego continúa. Es el sistema tradicional del ecosistema Node.js y sigue siendo muy común.

*   **ES Modules (ESM): El Estándar Moderno de JavaScript**
    *   **Sintaxis:** Usa `import` y `export`.
    *   **Características:** Es el estándar oficial de JavaScript, soportado tanto en navegadores como en versiones modernas de Node.js. Su naturaleza estática (las importaciones y exportaciones se resuelven en tiempo de compilación/análisis, no en ejecución) permite optimizaciones como el **tree-shaking**, donde los bundlers (como Webpack o Vite) pueden eliminar de forma segura el código que no se utiliza, resultando en paquetes más pequeños.

> **En la práctica:** Las librerías serias suelen publicar su código en **ambos formatos** para ser compatibles con la mayor cantidad de proyectos posible.

---

#### 1.2 Campos Clave en `package.json` para Módulos y Tipos

El archivo `package.json` es el cerebro de tu paquete. Los siguientes campos le indican a herramientas como Node.js, bundlers y *TypeScript* cómo encontrar y utilizar tu código.

*   **`type`**: El interruptor principal.
    *   `"module"`: Le dice a Node.js que los archivos `.js` de tu proyecto deben ser tratados como ES Modules por defecto.
    *   `"commonjs"`: (Valor por defecto si no se especifica) Los archivos `.js` se tratan como CommonJS.

*   **`main`**, **`module`**: Los Puntos de Entrada "Legados".
    *   `"main"`: El punto de entrada principal para el entorno CommonJS. Es el que Node.js usaba tradicionalmente al hacer `require('mi-paquete')`.
    *   `"module"`: Un campo no oficial pero ampliamente adoptado por bundlers para encontrar la versión ESM de tu paquete. Ha sido mayormente reemplazado por `exports`.

*   **`exports`**: La Solución Moderna y Recomendada.
    Este campo es un "mapa de entradas" que le permite a tu paquete exponer diferentes archivos para diferentes entornos de forma explícita y controlada. Resuelve la ambigüedad de los campos anteriores y ofrece un control mucho más granular.

    ```json
    {
      "exports": {
        // Punto de entrada principal (ej: `import 'mi-paquete'`)
        ".": {
          "types": "./dist/index.d.ts",   // Para TypeScript
          "import": "./dist/index.js",    // Para `import` (ESM)
          "require": "./dist/index.cjs"   // Para `require` (CJS)
        },
        // Punto de entrada secundario (ej: `import 'mi-paquete/utils'`)
        "./utils": {
          "types": "./dist/utils.d.ts",
          "import": "./dist/utils.js",
          "require": "./dist/utils.cjs"
        }
      }
    }
    ```
    **Ventaja:** `exports` es la única fuente de verdad. Si un archivo no está listado aquí, no se puede importar desde fuera del paquete, lo que mejora la encapsulación.

*   **`types`** (o `typings`): El Punto de Entrada de Tipos.
    *   Indica la ubicación de tu archivo principal de declaración de tipos (`.d.ts`). Es crucial para que los usuarios de *TypeScript* obtengan autocompletado y seguridad de tipos.
    *   **Nota:** Si usas el campo `exports`, la forma moderna es definir los tipos dentro de cada entrada con `"types"`, como se ve en el ejemplo anterior.

*   **`files`**: El "Whitelist" de Publicación.
    *   Es un array de archivos y directorios que se incluirán cuando publiques tu paquete en npm. Esto evita que publiques archivos innecesarios (como tests, configuraciones, etc.).
    *   Ejemplo: `["dist/", "README.md", "LICENSE"]`.

*   **`sideEffects`**: Una Pista para la Optimización.
    *   Este campo le dice a los bundlers si tu código tiene "efectos secundarios" (por ejemplo, si un archivo modifica variables globales o importa un CSS solo por existir).
    *   Al configurarlo como `"sideEffects": false`, garantizas que tus módulos son puros. Esto le da permiso al bundler para aplicar el *tree-shaking* de forma mucho más agresiva, ya que puede eliminar un import si no se usa directamente, sabiendo que no romperá nada.

#### 1.3 Resolución de módulos en TS

* `moduleResolution`: `Bundler` (recomendado con Vite/tsup), `NodeNext` (Node ESM/CJS), o `Node` (legacy).
* `baseUrl`/`paths`: alias de importación (no confundir con `exports`).

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@lib/*": ["src/*"] }
  }
}
```

  > Los alias **no** cambian el runtime; bundlers o tsconfig-paths deben resolverlos.

#### 1.4 *Barrels* (archivos `index.ts`)

* Re-exportan símbolos desde un "paquete" interno para simplificar imports.
* Preferí **`export type`** para re-exportar **solo tipos** y evitar importaciones en runtime.
* Cuidado con **ciclos** de imports al encadenar muchos *barrels*.

#### 1.5 Declaraciones `.d.ts`

* Se generan automáticamente con `tsc` (`"declaration": true`) o con bundlers (p. ej., `tsup --dts`).
* **Ambient declarations**: agregan tipos sin importar un módulo concreto.

```ts
// global.d.ts
declare global { interface Window { appVersion?: string } }
export {} // convierte el archivo en módulo y aplica las globals
```
* **Module declarations**: tipar módulos JS sin tipos:

```ts
// types/untyped-lib.d.ts
declare module "untyped-lib" { export function greet(n: string): string }
```
* **Module augmentation**: extender tipos existentes de una lib:

```ts
// types/fastify.d.ts
declare module "fastify" { interface FastifyRequest { userId?: string } }
```

#### 1.6 `import type` / `export type`

* Eliminan importaciones **solo de tipos** en JS emitido, reduciendo sobrecarga y ciclos.

#### 1.7 Estrategias de publicación

* Monopackage simple: compilar a `dist/` con ESM/CJS + d.ts.
* Verificá **consumo dual** (ESM y CJS) y los tipos en un proyecto *consumer*.
* Publicación real: `npm publish` (usar `npm pack` y `files` para previsualizar el contenido).

---

### 2) Práctica con npm

> Carpeta `lib/` (librería) y carpeta `consumer/` (proyecto de prueba). Asumimos `tsup` instalado.

#### 2.1 Estructura

```
lib/
  src/
    index.ts
    utils.ts
  tsconfig.json
  package.json
consumer/
  src/demo.ts
  tsconfig.json
  package.json
```

#### 2.2 Configuración de la librería (`lib/`)

**`lib/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "declaration": true,
    "emitDeclarationOnly": false,
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "baseUrl": ".",
    "paths": { "@lib/*": ["src/*"] }
  },
  "include": ["src", "types"]
}
```

**`lib/package.json`** (fragmento)

```json
{
  "name": "@demo/ts-lib",
  "version": "0.1.0",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    },
    "./utils": {
      "types": "./dist/utils.d.ts",
      "import": "./dist/utils.js",
      "require": "./dist/utils.cjs"
    }
  },
  "files": ["dist", "README.md", "LICENSE"],
  "sideEffects": false,
  "scripts": {
    "typecheck": "tsc --noEmit",
    "build": "tsup src/index.ts src/utils.ts --format esm,cjs --dts --sourcemap",
    "clean": "rimraf dist"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "typescript": "^5.5.0",
    "rimraf": "^5.0.0"
  }
}
```

**`lib/src/utils.ts`**

```ts
export type NonEmpty<T extends string> = T extends "" ? never : T
export function greet<T extends string>(name: NonEmpty<T>) {
  return `Hello, ${name}!`
}
export const sum = (a: number, b: number) => a + b
```

**`lib/src/index.ts`**

```ts
export { greet, sum } from "./utils"
export type { NonEmpty } from "./utils" // export type evita emitir import en JS
```

**Augmentación opcional** (`lib/types/fastify.d.ts`)

```ts
declare module "fastify" { interface FastifyRequest { userId?: string } }
```

**Build**

```bash
cd lib
npm run typecheck
npm run build
```

#### 2.3 Publicación local y consumo

**Crear paquete y consumirlo**

```bash
cd lib
npm pack                   # genera @demo-ts-lib-0.1.0.tgz
cd ../consumer
npm init -y
npm i -D typescript ts-node
npm i ../lib/@demo-ts-lib-0.1.0.tgz
```

**`consumer/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

**`consumer/src/demo.ts`**

```ts
import { greet, sum, type NonEmpty } from "@demo/ts-lib"

const n: NonEmpty<"Ada"> = "Ada"
console.log(greet(n))
console.log(sum(2, 3))
```

**Ejecución**

```bash
npx ts-node src/demo.ts
```

> Probá también importar subruta: `import { greet } from "@demo/ts-lib/utils"`.

#### 2.4 Aliases vs `exports`

* Si usás `paths` (`@lib/*`) dentro de **lib**, configurá el bundler o usa `tsconfig-paths` para runtime.
* El **consumer** no ve tus `paths`; expone rutas estables vía `exports`.

#### 2.5 Buenas prácticas

* `export type` / `import type` para evitar emisiones innecesarias.
* `files` + `sideEffects: false` para paquetes limpios y *tree-shakeables*.
* Verificá el **contenido del tarball**: `npm pack --dry-run`.
* Evitá ciclos en *barrels*; si aparecen, rompe el ciclo o convierte re-exports a `import type`.

---

### 3) Ejercicios opcionales

1. Agregá un subpath `"./math"` en `exports` que exponga solo `sum` con sus `.d.ts`.
2. Creá una declaración de módulo para una lib JS ficticia `"legacy-date"` con `parseDate(s: string): Date` y usala en `consumer`.
3. Añadí `sideEffects: false` y verificá que no haya inicializaciones globales en tus módulos.
4. Cambiá `moduleResolution` a `NodeNext` y comprobá diferencias de resolución con `package.json` `type`.
5. Configurá `files` para incluir únicamente `dist/` y verificá el resultado de `npm pack --dry-run`.

---

### 4) Comandos útiles

```bash
# en lib
npm run clean && npm run build
npm pack --dry-run

# en consumer
npx ts-node src/demo.ts
```

## Asincronía, validación y mini API (ruta backend opcional)

**Objetivos**

* Tipar `Promise`, `async/await`, resultados `Result` y validación de datos.

> Objetivo: dominar `async/await`, modelar errores con tipos, validar entrada/salida con Zod y exponer una **mini API** tipada en Fastify.

---

### 1) Teoría

#### 1.1 Promesas y `async/await`

* Una función `async` **siempre** retorna `Promise<T>` (donde `T` es el tipo del `return`).
* `await` suspende hasta que la promesa se resuelva o rechace.
* Buenas prácticas: usar `try/catch/finally` para **limpieza de recursos** y mapeo de errores.

```ts
async function leer(): Promise<string> {
  // ...
  return "ok" // Promise<string>
}
```

#### 1.2 Tipado de errores

* El canal de error de una `Promise` es **no tipado**. En TS, `catch (e)` es `unknown`.
* Preferí **modelar errores** en el tipo de retorno (`Result`/`Either`) o normalizar `unknown` a un error propio.

```ts
function toError(e: unknown): Error {
  return e instanceof Error ? e : new Error(String(e))
}
```

#### 1.3 Concurrencia

* `Promise.all`: falla rápido si una falla (rechazo corto).
* `Promise.allSettled`: nunca lanza; reporta estados.
* `Promise.race`: primero en resolver/rechazar.
* **No confundir** concurrencia (varias promesas en curso) con paralelismo (varios núcleos).

#### 1.4 Timeouts y cancelación

* `AbortController` + `fetch` (Node ≥18) para cancelación.
* `Promise.race` para implementar *timeouts* de alto nivel.

#### 1.5 Validación como contrato

* Esquemas (Zod) para **entrada** (`req.body`, `params`, `query`) y **salida** (`response`).
* Tipos inferidos de los esquemas → **tipado end-to-end**.

#### 1.6 Endpoints tipados en Fastify

* `fastify-type-provider-zod` conecta Zod con Fastify: valida y **tipa** `req` y `reply`.
* Manejo centralizado de errores; respuestas con **uniones discriminadas** (p. ej., `{ ok: true, data } | { ok: false, error }`).

---

### 2) Práctica

#### 2.1 Instalación

```bash
npm i fastify zod
npm i -D tsx fastify-type-provider-zod
```

**Scripts** (`package.json`):

```json
{
  "scripts": {
    "serve": "tsx watch src/server.ts",
    "typecheck": "tsc --noEmit",
    "build": "tsc -p tsconfig.json",
    "start": "node dist/server.js"
  }
}
```

#### 2.2 Utilidades de asincronía (`src/lib/async.ts`)

```ts
export class TimeoutError extends Error { constructor(msg = "Timeout") { super(msg) } }

export async function withTimeout<T>(p: Promise<T>, ms: number): Promise<T> {
  let t: NodeJS.Timeout
  const timeout = new Promise<never>((_, rej) => (t = setTimeout(() => rej(new TimeoutError()), ms)))
  try { return await Promise.race([p, timeout]) } finally { clearTimeout(t!) }
}

export function toError(e: unknown): Error { return e instanceof Error ? e : new Error(String(e)) }
```

#### 2.3 Esquemas de dominio (`src/schemas.ts`)

```ts
import { z } from "zod"

export const Item = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  price: z.number().nonnegative()
})
export const NewItem = Item.omit({ id: true })
export const IdParam = z.object({ id: z.string().uuid() })

export type TItem = z.infer<typeof Item>
export type TNewItem = z.infer<typeof NewItem>
```

#### 2.4 Repositorio en memoria (`src/lib/repo.ts`)

```ts
import type { TItem, TNewItem } from "../schemas"

export class ItemRepo {
  #m = new Map<string, TItem>()
  list(): TItem[] { return [...this.#m.values()] }
  get(id: string) { return this.#m.get(id) }
  create(data: TNewItem): TItem {
    const id = crypto.randomUUID()
    const item = { id, ...data }
    this.#m.set(id, item)
    return item
  }
  update(id: string, data: TNewItem): TItem | undefined {
    if (!this.#m.has(id)) return undefined
    const item = { id, ...data }
    this.#m.set(id, item)
    return item
  }
  remove(id: string) { return this.#m.delete(id) }
}
```

#### 2.5 Rutas (`src/routes/items.ts`)

```ts
import { z } from "zod"
import { Item, NewItem, IdParam } from "../schemas"
import type { FastifyPluginAsync } from "fastify"

const ItemsRoutes: FastifyPluginAsync = async (app) => {
  app.get("/items", { schema: { response: { 200: z.array(Item) } } }, async () => {
    return app.repo.list()
  })

  app.get("/items/:id", { schema: { params: IdParam, response: { 200: Item } } }, async (req, reply) => {
    const item = app.repo.get(req.params.id)
    if (!item) return reply.code(404).send()
    return item
  })

  app.post("/items", { schema: { body: NewItem, response: { 201: Item } } }, async (req, reply) => {
    const created = app.repo.create(req.body)
    return reply.code(201).send(created)
  })

  app.put("/items/:id", { schema: { params: IdParam, body: NewItem, response: { 200: Item } } }, async (req, reply) => {
    const updated = app.repo.update(req.params.id, req.body)
    if (!updated) return reply.code(404).send()
    return updated
  })

  app.delete("/items/:id", { schema: { params: IdParam } }, async (req, reply) => {
    const ok = app.repo.remove(req.params.id)
    return reply.code(ok ? 204 : 404).send()
  })
}

export default ItemsRoutes
```

#### 2.6 Servidor (`src/server.ts`)

```ts
import Fastify from "fastify"
import { ZodTypeProvider, serializerCompiler, validatorCompiler } from "fastify-type-provider-zod"
import ItemsRoutes from "./routes/items"
import { ItemRepo } from "./lib/repo"
import { toError } from "./lib/async"

declare module "fastify" {
  interface FastifyInstance { repo: ItemRepo }
}

const app = Fastify({ logger: true }).withTypeProvider<ZodTypeProvider>()
app.setValidatorCompiler(validatorCompiler)
app.setSerializerCompiler(serializerCompiler)
app.decorate("repo", new ItemRepo())

app.get("/health", async () => ({ ok: true }))
app.register(ItemsRoutes)

app.setErrorHandler((err, _req, reply) => {
  const e = toError(err)
  app.log.error(e)
  reply.code(500).send({ ok: false, error: e.message })
})

const port = Number(process.env.PORT ?? 3000)
app.listen({ port, host: "0.0.0.0" }).catch((e) => {
  app.log.error(e); process.exit(1)
})
```

#### 2.7 Cliente con cancelación (`src/client.ts`)

```ts
import { withTimeout, toError } from "./lib/async"

export async function getJson<T>(url: string, ms = 3000): Promise<T> {
  const ctrl = new AbortController()
  const p = (async () => {
    const res = await fetch(url, { signal: ctrl.signal })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return (await res.json()) as T
  })()
  try { return await withTimeout(p, ms) } catch (e) { ctrl.abort(); throw toError(e) }
}

// Demo: getJson<{ ok: boolean }>("http://localhost:3000/health").then(console.log)
```

---

### 3) Mini–katas (entregables)

1. Agregá `GET /search?minPrice&maxPrice` con validación de `querystring` (Zod) y retorno `200: Item[]`.
2. Añadí un **middleware** que mida duración de cada request y la registre en el logger.
3. Implementá `getJson` con `retry` exponencial (máx. 3 intentos) manteniendo tipos del genérico `T`.
4. Tipá un resultado discriminado `{ ok: true; data: T } | { ok: false; error: string }` y usalo en `client.ts`.
5. Extraé el contrato de `/items` a un archivo de tipos y usalo tanto en el servidor como en el cliente (*compile-time contract*).

---

### 4) Comandos útiles

```bash
npm run serve         # desarrollo con recarga
npm run typecheck     # verificación de tipos
npm run build && npm start
curl -s http://localhost:3000/health | jq
```


## Apéndices

### A. `tsconfig.json` mínimo estricto

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "forceConsistentCasingInFileNames": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

### B. Plantilla de `package.json` (scripts clave)

```json
{
  "type": "module",
  "scripts": {
    "dev": "ts-node src/index.ts",
    "watch": "tsc -w",
    "typecheck": "tsc --noEmit",
    "build": "tsup src/index.ts --format cjs,esm --dts --sourcemap",
    "start": "node dist/index.js",
    "clean": "rimraf dist",
    "lint": "eslint . --ext .ts",
    "lint:fix": "eslint . --ext .ts --fix",
    "format": "prettier -w .",
    "format:check": "prettier -c .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:cov": "vitest run --coverage",
    "serve": "tsx watch src/server.ts",
    "ci": "npm run typecheck && npm run lint && npm run test && npm run build",
    "prepublishOnly": "npm run typecheck && npm run build"
  },
  "lint-staged": {
    "**/*.{ts,tsx}": ["prettier -w", "eslint --fix"]
  }
}
```

### C. Estructura sugerida de carpetas

```
├─ src/
│  ├─ lib/
│  ├─ server.ts
│  ├─ index.ts
│  ├─ 01-types.ts
│  ├─ 02-modelado.ts
│  └─ 04-generics.ts
├─ tests/
│  └─ server.test.ts
├─ dist/
├─ tsconfig.json
├─ package.json
└─ README.md
```
