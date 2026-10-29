# Guía práctica para generar y ejecutar tests en TypeScript
> Objetivo: dejarte una **ruta completa** para montar tests en TypeScript con ejemplos funcionales, mocks y un **script que genera archivos de test** (esqueletos) automáticamente.

---

## 1) Guías prácticas con ejemplos paso a paso

A continuación, dos setups mínimos: **Vitest** (rápido y moderno) y **Jest** (maduro y popular).

### 1.1 Inicializar proyecto con Vitest

```bash
mkdir ts-testing-vitest && cd ts-testing-vitest
npm init -y
npm i -D typescript vitest @vitest/coverage-v8 @types/node ts-node
npx tsc --init
```

### 1.2 Inicializar proyecto con Jest

```bash
mkdir ts-testing-jest && cd ts-testing-jest
npm init -y
npm i -D typescript jest ts-jest @types/jest @types/node
npx tsc --init
npx ts-jest config:init
```

Esto genera `jest.config.js` listo para usar con TypeScript.

### 1.3 `tsconfig.json` (mínimo sugerido)

```json
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "ESNext",
    "moduleResolution": "Node",
    "rootDir": "src",
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true,
    "types": ["node"]
  },
  "include": ["src", "test", "scripts"]
}
```

### 1.4 Scripts en `package.json`

**Vitest**

```json
{
  "scripts": {
    "build": "tsc -p .",
    "test": "vitest run",
    "test:ui": "vitest",
    "coverage": "vitest run --coverage"
  }
}
```

**Jest**

```json
{
  "scripts": {
    "build": "tsc -p .",
    "test": "jest",
    "coverage": "jest --coverage"
  }
}
```

### 1.5 Ejemplo de código + test

**`src/math.ts`**

```ts
export function sum(a: number, b: number) {
  return a + b;
}

export async function fetchUser(id: number) {
  return { id, name: `user-${id}` };
}
```

**Vitest – `test/math.spec.ts`**

```ts
import { sum, fetchUser } from "../src/math";

describe("math (vitest)", () => {
  it("suma números", () => {
    expect(sum(2, 3)).toBe(5);
  });

  it("fetchUser devuelve objeto con id y name", async () => {
    const u = await fetchUser(7);
    expect(u).toEqual({ id: 7, name: "user-7" });
  });
});
```

**Jest – `test/math.jest.spec.ts`**

```ts
import { sum, fetchUser } from "../src/math";

describe("math (jest)", () => {
  test("suma números", () => {
    expect(sum(2, 3)).toBe(5);
  });

  test("fetchUser devuelve objeto con id y name", async () => {
    const u = await fetchUser(7);
    expect(u).toEqual({ id: 7, name: "user-7" });
  });
});
```

**Ejecución**

```bash
npm run test
```

---

## 2) Herramientas y estrategias de mocking en Vitest y Jest

### 2.1 Vitest (`vi.fn` y `vi.spyOn`)

**`src/userService.ts`**

```ts
export interface UserRepo {
  getById(id: number): Promise<{ id: number; name: string } | null>;
  save(user: { id: number; name: string }): Promise<void>;
}

export class UserService {
  constructor(private repo: UserRepo) {}

  async register(id: number, name: string) {
    const existing = await this.repo.getById(id);
    if (existing) throw new Error("User exists");
    await this.repo.save({ id, name });
    return true;
  }
}
```

**Vitest – `test/userService.spec.ts`**

```ts
import { UserService, UserRepo } from "../src/userService";

function createRepoMock(): UserRepo {
  return {
    getById: vi.fn(),
    save: vi.fn(),
  };
}

describe("UserService (vitest)", () => {
  it("registra cuando no existe previamente", async () => {
    const repo = createRepoMock();
    (repo.getById as any).mockResolvedValue(null);

    const svc = new UserService(repo);
    const ok = await svc.register(1, "Ada");

    expect(ok).toBe(true);
    expect(repo.getById).toHaveBeenCalledWith(1);
    expect(repo.save).toHaveBeenCalledWith({ id: 1, name: "Ada" });
  });

  it("falla si el usuario ya existe", async () => {
    const repo = createRepoMock();
    (repo.getById as any).mockResolvedValue({ id: 1, name: "Ada" });

    const svc = new UserService(repo);
    await expect(svc.register(1, "Ada"))
      .rejects.toThrowError(/exists/);
  });
});
```

**Jest – `test/userService.jest.spec.ts`**

```ts
import { UserService, UserRepo } from "../src/userService";

describe("UserService (jest)", () => {
  const createRepoMock = (): jest.Mocked<UserRepo> => ({
    getById: jest.fn(),
    save: jest.fn(),
  });

  it("registra cuando no existe previamente", async () => {
    const repo = createRepoMock();
    repo.getById.mockResolvedValue(null);

    const svc = new UserService(repo);
    const ok = await svc.register(1, "Ada");

    expect(ok).toBe(true);
    expect(repo.getById).toHaveBeenCalledWith(1);
    expect(repo.save).toHaveBeenCalledWith({ id: 1, name: "Ada" });
  });

  it("falla si el usuario ya existe", async () => {
    const repo = createRepoMock();
    repo.getById.mockResolvedValue({ id: 1, name: "Ada" });

    const svc = new UserService(repo);
    await expect(svc.register(1, "Ada"))
      .rejects.toThrowError(/exists/);
  });
});
```

### 2.2 Mock de módulos

**Vitest – `test/fileOps.spec.ts`**

```ts
import { readConfig } from "../src/fileOps";

vi.mock("node:fs/promises", () => ({
  readFile: vi.fn().mockResolvedValue('{"env":"dev"}')
}));

describe("readConfig (vitest)", () => {
  it("lee JSON desde fs mockeado", async () => {
    const cfg = await readConfig("./config.json");
    expect(cfg).toEqual({ env: "dev" });
  });
});
```

**Jest – `test/fileOps.jest.spec.ts`**

```ts
import { readConfig } from "../src/fileOps";

jest.mock("node:fs/promises", () => ({
  readFile: jest.fn().mockResolvedValue('{"env":"dev"}')
}));

describe("readConfig (jest)", () => {
  it("lee JSON desde fs mockeado", async () => {
    const cfg = await readConfig("./config.json");
    expect(cfg).toEqual({ env: "dev" });
  });
});
```

---

## 3) Automatización de generación de archivos de test (esqueletos)

*(idéntico para ambos entornos, Vitest o Jest)*

Incluye dos variantes: **(A) sin dependencias** y **(B) con `ts-morph`** para análisis de AST. (Ver código en secciones anteriores.)

---

### Notas finales

* Puedes combinar el generador con **GitHub Copilot** u otra IA para **auto-rellenar** los casos.
* Añade **husky** + **lint-staged** para correr tests/lint en pre-commit.
* Integra **coverage** en CI (GitHub Actions) y **badges** en README.

---

## Apéndice: Alternativa con **Jest** (setup + ejemplos)

> Si preferís Jest en lugar de Vitest, este es un flujo equivalente con TypeScript, mocks y cobertura. Usa **ts-jest** para compilar TS al vuelo y mantener una DX sencilla.

### A) Instalación

```bash
npm i -D typescript jest ts-jest @types/jest @types/node
npx ts-jest config:init   # genera jest.config.ts
npx tsc --init            # si aún no lo tenés
```

### B) `jest.config.ts` (generado por ts-jest, con pequeños ajustes)

```ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/test', '<rootDir>/src'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'json'],
  collectCoverage: true,
  coverageProvider: 'v8',
  // opcional: mapea paths de tsconfig
  // moduleNameMapper: { '^@src/(.*)$': '<rootDir>/src/$1' }
};
export default config;
```

### C) `tsconfig.json` (añadir tipos de jest)

```json
{
  "compilerOptions": {
    "target": "ES2021",
    "module": "CommonJS",
    "moduleResolution": "Node",
    "rootDir": "src",
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true,
    "types": ["jest", "node"]
  },
  "include": ["src", "test", "scripts"]
}
```

> Nota: Jest funciona más directo en **CommonJS**. Si usás ESM, podés mantener `module: "ESNext"` y agregar `extensionsToTreatAsEsm: ['.ts']` en Jest + `transform` con ts-jest, pero CJS es el camino simple.

### D) Scripts en `package.json`

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "coverage": "jest --coverage"
  }
}
```

### E) Ejemplos 1: código + test básico

**`src/math.ts`**

```ts
export function sum(a: number, b: number) { return a + b; }
export async function fetchUser(id: number) { return { id, name: `user-${id}` }; }
```

**`test/math.spec.ts`**

```ts
import { sum, fetchUser } from '../src/math';

describe('math (jest)', () => {
  it('suma números', () => {
    expect(sum(2, 3)).toBe(5);
  });

  it('fetchUser devuelve objeto con id y name', async () => {
    await expect(fetchUser(7)).resolves.toEqual({ id: 7, name: 'user-7' });
  });
});
```

### F) Ejemplos 2: mocks de dependencias (repos) con `jest.fn` y `jest.spyOn`

**`src/userService.ts`** (igual que en la sección de Vitest)

```ts
export interface UserRepo {
  getById(id: number): Promise<{ id: number; name: string } | null>;
  save(user: { id: number; name: string }): Promise<void>;
}
export class UserService {
  constructor(private repo: UserRepo) {}
  async register(id: number, name: string) {
    const existing = await this.repo.getById(id);
    if (existing) throw new Error('User exists');
    await this.repo.save({ id, name });
    return true;
  }
}
```

**`test/userService.spec.ts`**

```ts
import { UserService, UserRepo } from '../src/userService';

function createRepoMock(): UserRepo {
  return {
    getById: jest.fn(),
    save: jest.fn(),
  };
}

describe('UserService (jest)', () => {
  it('registra cuando no existe', async () => {
    const repo = createRepoMock();
    (repo.getById as jest.Mock).mockResolvedValue(null);

    const svc = new UserService(repo);
    await expect(svc.register(1, 'Ada')).resolves.toBe(true);

    expect(repo.getById).toHaveBeenCalledWith(1);
    expect(repo.save).toHaveBeenCalledWith({ id: 1, name: 'Ada' });
  });

  it('falla si ya existe', async () => {
    const repo = createRepoMock();
    (repo.getById as jest.Mock).mockResolvedValue({ id: 1, name: 'Ada' });

    const svc = new UserService(repo);
    await expect(svc.register(1, 'Ada')).rejects.toThrow(/exists/);
  });
});
```

**Espiar funciones reales con `jest.spyOn`**

```ts
import * as math from '../src/math';

describe('spyOn (jest)', () => {
  it('espía sum', () => {
    const spy = jest.spyOn(math, 'sum');
    const r = math.sum(2, 5);
    expect(r).toBe(7);
    expect(spy).toHaveBeenCalledTimes(1);
    spy.mockRestore();
  });
});
```

### G) Ejemplos 3: mock de módulos (fs/promises, fetch)

**`src/fileOps.ts`**

```ts
import { readFile } from 'node:fs/promises';
export async function readConfig(path: string) {
  const txt = await readFile(path, 'utf8');
  return JSON.parse(txt);
}
```

**`test/fileOps.spec.ts`** – mock de `fs/promises`

```ts
jest.mock('node:fs/promises', () => ({
  readFile: jest.fn().mockResolvedValue('{"env":"dev"}')
}));

import { readConfig } from '../src/fileOps';
import { readFile } from 'node:fs/promises';

describe('readConfig (jest)', () => {
  it('lee JSON desde fs mockeado', async () => {
    await expect(readConfig('./config.json')).resolves.toEqual({ env: 'dev' });
    expect(readFile).toHaveBeenCalled();
  });
});
```

**Mock global de `fetch`**

```ts
declare const global: any; // o usa types adecuados según tu setup

describe('fetch mock (jest)', () => {
  beforeAll(() => {
    global.fetch = jest.fn().mockResolvedValue({
      json: async () => ({ ok: true })
    });
  });
  afterAll(() => {
    jest.restoreAllMocks();
  });

  it('usa fetch mockeado', async () => {
    const res = await global.fetch('https://api.test');
    const data = await res.json();
    expect(data).toEqual({ ok: true });
  });
});
```

### H) Cobertura

```bash
npm run coverage
```

Genera reporte con provider **v8** (texto + carpeta `coverage/`).

### I) Compatibilidad con los generadores de tests

Los scripts de generación de tests de la sección 3 (regex o `ts-morph`) **funcionan igual** con Jest: sólo cambian los imports y los matchers/mocks (`vi.*` → `jest.*`). Puedes crear una variante de plantilla para Jest, por ejemplo:

```ts
function buildSpecTemplateJest(srcPath: string, exported: string[]) {
  const importPath = /* …ruta relativa sin .ts… */ '';
  const names = exported.length ? `{ ${exported.join(', ')} }` : '* as mod';
  return `import ${names} from '${importPath}';

describe('${/* nombre archivo */''}', () => {
  it('TODO (jest)', () => { expect(true).toBe(true); });
});
`;
}
```

> Con esto podés mantener **Vitest y/o Jest** en el mismo repo si querés comparar; lo usual es elegir uno y estandarizar.


### **2.1 `vi.fn()` y `vi.spyOn()` (Vitest) / `jest.fn()` y `jest.spyOn()` (Jest)**

Estas son las herramientas fundamentales para la creación de "simulaciones" de funciones y métodos, permitiéndote controlar su comportamiento y espiar sus interacciones.

#### **`vi.fn()` / `jest.fn()`: Funciones Mock**

*   **Propósito:** Crear una función completamente simulada. Es útil cuando necesitas una función que no haga nada por defecto, pero que puedas controlar su retorno, resolver promesas o espiar sus llamadas.
*   **Creación:**
    *   `const myMockFn = vi.fn();`
    *   `const myJestMockFn = jest.fn();`
*   **Configuración del Comportamiento:**
    *   **Retorno Fijo:** `myMockFn.mockReturnValue('valor');` o `myJestMockFn.mockReturnValue('valor');`
    *   **Retorno Promesa:** `myMockFn.mockResolvedValue('valor asíncrono');` o `myJestMockFn.mockResolvedValue('valor asíncrono');`
    *   **Implementación Personalizada:** `myMockFn.mockImplementation((a, b) => a + b);` o `myJestMockFn.mockImplementation((a, b) => a + b);`
*   **Espionaje (Matchers):** Permiten verificar cómo fue llamada la función.
    *   `expect(myMockFn).toHaveBeenCalled();`
    *   `expect(myMockFn).toHaveBeenCalledWith(arg1, arg2);`
    *   `expect(myMockFn).toHaveBeenCalledTimes(3);`
    *   `expect(myMockFn).toHaveReturnedWith('valor');`
*   **Ejemplo de tu guía (`UserService`):** Aquí se usa `vi.fn()` / `jest.fn()` para simular los métodos `getById` y `save` del `UserRepo`, lo que permite controlar si un usuario "existe" o no para el test.
    ```typescript
    // Vitest
    function createRepoMock(): UserRepo {
      return {
        getById: vi.fn(), // <--- vi.fn()
        save: vi.fn(),    // <--- vi.fn()
      };
    }
    (repo.getById as any).mockResolvedValue(null); // Configura el retorno
    // Jest
    const createRepoMock = (): jest.Mocked<UserRepo> => ({
      getById: jest.fn(), // <--- jest.fn()
      save: jest.fn(),    // <--- jest.fn()
    });
    repo.getById.mockResolvedValue(null); // Configura el retorno
    ```

#### **`vi.spyOn()` / `jest.spyOn()`: Espías de Métodos**

*   **Propósito:** Monitorear llamadas a métodos existentes de un objeto sin alterar su comportamiento por defecto, o cambiar su implementación temporalmente.
*   **Creación:** `vi.spyOn(objeto, 'nombreMetodo');` o `jest.spyOn(objeto, 'nombreMetodo');`
*   **Comportamiento por Defecto:** Un espía por defecto sigue llamando al método original.
*   **Alteración Temporal (Opcional):** Puedes usar `mockReturnValue`, `mockResolvedValue`, `mockImplementation` de la misma forma que con `vi.fn()`/`jest.fn()`. El comportamiento original se puede restaurar con `spy.mockRestore()` (Vitest) o `spy.mockRestore()` / `jest.restoreAllMocks()` (Jest).
*   **Ejemplo de tu guía (`math.ts` con Jest):**
    ```typescript
    import * as math from '../src/math';

    describe('spyOn (jest)', () => {
      it('espía sum', () => {
        const spy = jest.spyOn(math, 'sum'); // <-- jest.spyOn
        const r = math.sum(2, 5);
        expect(r).toBe(7);
        expect(spy).toHaveBeenCalledTimes(1);
        spy.mockRestore(); // Restaura el método original
      });
    });
    ```
    *Para Vitest, el uso sería idéntico, reemplazando `jest.spyOn` por `vi.spyOn`.*

---

### **2.2 `vi.mock()` (Vitest) / `jest.mock()` (Jest): Mocks de Módulos Completos y Parciales**

Estas funciones son las herramientas más poderosas para simular módulos enteros, interceptando cómo se importan en el código bajo test.

#### **Concepto General:**

*   **Interceptación:** `vi.mock()` / `jest.mock()` permiten interceptar las dependencias de tus módulos antes de que se carguen. Cuando otro módulo hace un `import` del `path` especificado, no obtendrá la implementación original, sino la versión simulada que defines.
*   **Hoisting (Elevación):** Todas las llamadas a `vi.mock()` / `jest.mock()` se "elevan" al principio del archivo de test. Esto significa que las simulaciones se configuran *antes* de que cualquier `import` en el test se resuelva.
    *   **¡Importante!** La función *factory* (la que define el mock) no se eleva. Se ejecuta cuando el módulo simulado es importado por primera vez.
    *   **Restricción:** No se pueden llamar dentro de bloques `describe` o `it`/`test`.

#### **Sintaxis Básica:**

```typescript
vi.mock(path, factoryFunction);
// o
jest.mock(path, factoryFunction);
```

*   **`path` (string):** La ruta del módulo a simular. Puede ser una ruta relativa (`../src/fileOps`), un alias de Vite (configurado en `vite.config.ts`), o el nombre de un paquete `node_modules` (`node:fs/promises`).
*   **`factoryFunction` (función):** Una función que devuelve la implementación simulada del módulo.

#### **Tipos de Mocks con `vi.mock()` / `jest.mock()`:**

**1. Módulos Completamente Simulados (Full Mocks):**
    *   **Propósito:** Reemplazar un módulo entero con una implementación personalizada, ignorando la original. Esto es útil cuando el módulo original tiene efectos secundarios no deseados, es costoso de inicializar o simplemente quieres tener control total sobre su comportamiento.
    *   **Ejemplo de tu guía (`fileOps.ts` con `node:fs/promises`):**
        ```typescript
        // Vitest
        vi.mock("node:fs/promises", () => ({
          readFile: vi.fn().mockResolvedValue('{"env":"dev"}')
        }));

        // Jest
        jest.mock("node:fs/promises", () => ({
          readFile: jest.fn().mockResolvedValue('{"env":"dev"}')
        }));
        ```
        En ambos casos, cuando `readConfig` intente importar `readFile` de `node:fs/promises`, recibirá la versión simulada que siempre resuelve con el JSON de `{"env":"dev"}`.

**2. Módulos Parcialmente Simulados (Partial Mocks):**
    *   **Propósito:** Mantener el comportamiento original de la mayoría de las exportaciones de un módulo, simulando solo algunas específicas. Esto es ideal para módulos grandes donde solo unas pocas funciones o propiedades necesitan ser modificadas.
    *   **Uso con `vi.importActual()` / `jest.requireActual()`:**
        Dentro de la `factoryFunction`, necesitas importar la implementación real del módulo para poder incluirla en tu mock.
        *   **Vitest:** Usa `await vi.importActual(path)` (es asíncrono).
        *   **Jest:** Usa `jest.requireActual(path)` (síncrono).
    *   **Ejemplo (conceptual, aplicando a un módulo con `add` y `multiply`):**
        ```typescript
        // utils.ts (módulo original)
        export const add = (a: number, b: number) => a + b;
        export const multiply = (a: number, b: number) => a * b;

        // test/some.spec.ts
        // Vitest
        vi.mock('./utils', async () => {
          const actual = await vi.importActual('./utils') as typeof import('./utils');
          return {
            ...actual, // Incluye el 'add' original
            multiply: vi.fn((a, b) => a * b * 10), // Mockea solo 'multiply'
          };
        });

        // Jest
        jest.mock('./utils', () => {
          const actual = jest.requireActual('./utils') as typeof import('./utils');
          return {
            ...actual, // Incluye el 'add' original
            multiply: jest.fn((a, b) => a * b * 10), // Mockea solo 'multiply'
          };
        });
        ```
        En este caso, cualquier código que importe `./utils` obtendrá la función `add` original, pero la función `multiply` simulada que multiplica por 10.

**3. Mocks Automáticos (`vi.mock(path)` / `jest.mock(path)` sin factory):**
    *   **Propósito:** Cuando solo proporcionas el `path` sin una `factoryFunction`, el framework intentará simular automáticamente el módulo.
    *   **Comportamiento:**
        *   Las funciones exportadas (con nombre) serán reemplazadas por `vi.fn()` / `jest.fn()` vacías.
        *   Las exportaciones `default` (si son funciones) también se convierten en mocks.
        *   Las primitivas (strings, numbers) y objetos/arrays complejos se mantienen tal cual.
    *   **Uso:** Útil para módulos con muchas exportaciones donde solo necesitas espiar si se llaman, pero no te importa su implementación por defecto o quieres que no hagan nada.
    *   **Ejemplo:** `vi.mock('./some-analytics-sdk');` o `jest.mock('./some-analytics-sdk');`

#### **Mock Global de `fetch` (Jest):**

Tu guía presenta un excelente ejemplo de cómo mockear `fetch` globalmente en Jest:

```typescript
declare const global: any;

describe('fetch mock (jest)', () => {
  beforeAll(() => {
    global.fetch = jest.fn().mockResolvedValue({
      json: async () => ({ ok: true })
    });
  });
  afterAll(() => {
    jest.restoreAllMocks(); // Limpia los mocks después de todos los tests
  });

  it('usa fetch mockeado', async () => {
    const res = await global.fetch('https://api.test');
    const data = await res.json();
    expect(data).toEqual({ ok: true });
  });
});
```
*Para Vitest, un enfoque similar sería posible, aunque Vitest típicamente opera en un entorno de Node.js donde `fetch` global podría no estar presente por defecto, requiriendo un polyfill o el uso de una librería como `node-fetch` que luego podrías mockear.* Si usas `environment: 'jsdom'` o `environment: 'happy-dom'` en Vitest, `fetch` ya podría estar en el global y el mocking sería idéntico.

#### **Control del Estado de Mocks:**

Es crucial limpiar o restablecer el estado de los mocks entre tests para evitar interacciones no deseadas.

*   **`vi.clearAllMocks()` / `jest.clearAllMocks()`:** Borra el historial de llamadas de todos los mocks, pero mantiene su implementación.
*   **`vi.resetAllMocks()` / `jest.resetAllMocks()`:** Restablece todos los mocks a su implementación inicial (antes de `mockImplementation`), y borra su historial de llamadas.
*   **`vi.restoreAllMocks()` / `jest.restoreAllMocks()`:** Restaura los espías (`spyOn`) a su implementación original y resetea los demás mocks.
*   **Configuración en `package.json` o `jest.config.ts` / `vite.config.ts`:**
    Puedes configurar Vitest o Jest para que ejecuten estas funciones automáticamente antes de cada test o archivo de test, por ejemplo:
    *   **Jest (`jest.config.ts`):** `clearMocks: true`, `resetMocks: true`, `restoreMocks: true`.
    *   **Vitest (`vite.config.ts` en `test`):** `clearMocks: true`, `mockReset: true`, `restoreMocks: true`.

---

### **Conclusión de Mocks**

Dominar `vi.fn`/`jest.fn`, `vi.spyOn`/`jest.spyOn` y `vi.mock`/`jest.mock` es esencial para escribir tests unitarios robustos en TypeScript. Te permite aislar el código bajo prueba de sus dependencias, asegurando que tus tests sean rápidos, predecibles y solo fallen por problemas en el código que realmente estás intentando validar.