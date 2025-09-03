
## Pruebas en TypeScript (Vitest) y pruebas HTTP

**Objetivos**

* Configurar y ejecutar pruebas unitarias/e2e mínimas.

# Semana 7 — Pruebas en TypeScript (Vitest + Cobertura) — Apunte + Práctica

> Objetivo: configurar un entorno de **tests en TypeScript** con **Vitest**, medir **cobertura** (V8), probar utilidades síncronas/asíncronas y realizar **tests de integración** de la mini API (Semana 6) usando `app.inject()` de Fastify.

---

## 1) Teoría mínima

### 1.1 Tipos de pruebas

* **Unitarias**: funciones puras/utilidades; rápidas y aisladas.
* **Integración**: interacción de componentes (p. ej., rutas + validación + repositorio en memoria).
* **End to End (E2E)**: flujo completo; costosas, ejecutar pocas.

### 1.2 ¿Por qué Vitest?

* API compatible con Jest (`describe`, `it`, `expect`, *spies*, *mocks*).
* Corre **nativamente en TS** sin transpilado previo.
* Cobertura con V8, *watch mode*, *fake timers*, *snapshot testing*.

### 1.3 Tests “type-aware”

* Usa `tsc --noEmit` en CI para verificar tipos.
* No confundir *type tests* (errores en compilación) con *runtime tests* (Vitest).

### 1.4 Dobles de prueba

* **Spies**: observar llamadas (p. ej., `vi.fn()`).
* **Mocks**: reemplazar dependencias.
* **Fake timers**: controlar `setTimeout`/`Date.now()`.

### 1.5 Cobertura

* Mide líneas/ramas/funciones ejecutadas.
* Establecé **umbrales** razonables (p. ej., líneas ≥ 60%).

### 1.6 Buenas prácticas

* Tests **deterministas** y repetibles.
* Un test = una idea. Nombres claros.
* Evitá *flaky tests* (dependencia de tiempo/red). Usa *mocks* o `app.inject()`.

---

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

## 3) Mini–katas (entregables)

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

---

## Rúbrica de evaluación

* **Prácticas semanales** (40%): cumplimiento + calidad de tipos.
* **Calidad del código** (20%): ESLint/Prettier/Husky configurados y vigentes.
* **Pruebas** (20%): cobertura mínima ≥ 60% líneas.
* **Proyecto final** (20%): documentación, DX (scripts npm), tipado end-to-end.

---