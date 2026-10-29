# Objetivos del ejemplo

* Entender la **pirámide de testing** (unitario → integración → end‑to‑end) aplicada a una API.
* Montar un proyecto **TypeScript + Express** listo para testear con **Jest** y **Supertest**.
* Escribir tests **unitarios** para la capa de servicio y **de integración** para las rutas.
* Medir **cobertura** y aplicar TDD en un pequeño incremento.

> Público objetivo: alumnos que manejan TypeScript, Node, Express, ts-node/ts-node-dev.


## 1) Bootstrapping del proyecto

**Estructura de carpetas**

```
.
├─ src/
│  ├─ app.ts            # Express app (sin listen)
│  ├─ server.ts         # Punto de entrada (listen)
│  ├─ models/Book.ts    # Tipos
│  ├─ services/bookService.ts
│  └─ routes/books.ts
├─ tests/
│  ├─ unit/bookService.test.ts
│  └─ integration/books.routes.test.ts
├─ tsconfig.json
├─ jest.config.ts
└─ package.json
```

**package.json** (CommonJS + ts-jest)

```json
{
  "name": "ts-express-testing-class",
  "version": "1.0.0",
  "main": "dist/server.js",
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc -p tsconfig.json",
    "start": "node dist/server.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "coverage": "jest --coverage"
  },
  "dependencies": {
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/supertest": "^2.0.16",
    "jest": "^29.7.0",
    "supertest": "^6.3.4",
    "ts-jest": "^29.2.5",
    "ts-node-dev": "^2.0.0",
    "typescript": "^5.4.0"
  }
}
```

**tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "rootDir": "src",
    "outDir": "dist",
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

**jest.config.ts**

```ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  moduleFileExtensions: ['ts', 'js', 'json'],
  collectCoverageFrom: ['src/**/*.ts', '!src/server.ts'],
  coverageDirectory: 'coverage'
};

export default config;
```

Instalación rápida:

```bash
npm i
```

## 2) Código de la API (mínimo viable)

**src/models/Book.ts**

```ts
export interface Book {
  id: string;
  title: string;
  author: string;
  year: number;
}
```

**src/services/bookService.ts**

```ts
import { Book } from '../models/Book';
import { randomUUID } from 'crypto';

export class BookService {
  private books: Book[] = [];

  list(): Book[] {
    return this.books;
  }

  get(id: string): Book | undefined {
    return this.books.find(b => b.id === id);
  }

  create(data: Omit<Book, 'id'>): Book {
    const book: Book = { id: randomUUID(), ...data };
    this.books.push(book);
    return book;
  }

  update(id: string, patch: Partial<Omit<Book, 'id'>>): Book | undefined {
    const b = this.get(id);
    if (!b) return undefined;
    Object.assign(b, patch);
    return b;
  }

  remove(id: string): boolean {
    const idx = this.books.findIndex(b => b.id === id);
    if (idx === -1) return false;
    this.books.splice(idx, 1);
    return true;
  }

  clear() {
    this.books = [];
  }
}
```

**src/routes/books.ts**

> Enrutable *inyectable* para poder crear un router con un `BookService` fresco en tests.

```ts
import { Router } from 'express';
import { z } from 'zod';
import { BookService } from '../services/bookService';

export function makeBooksRouter(service = new BookService()) {
  const router = Router();

  const bookSchema = z.object({
    title: z.string().min(1),
    author: z.string().min(1),
    year: z.number().int().min(0)
  });

  router.get('/', (_req, res) => {
    res.json(service.list());
  });

  router.get('/:id', (req, res) => {
    const b = service.get(req.params.id);
    if (!b) return res.status(404).json({ error: 'Not found' });
    res.json(b);
  });

  router.post('/', (req, res) => {
    const parsed = bookSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ error: 'Invalid data', details: parsed.error.flatten() });
    }
    const book = service.create(parsed.data);
    res.status(201).json(book);
  });

  router.patch('/:id', (req, res) => {
    const patchSchema = bookSchema.partial();
    const parsed = patchSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ error: 'Invalid data', details: parsed.error.flatten() });
    }
    const updated = service.update(req.params.id, parsed.data);
    if (!updated) return res.status(404).json({ error: 'Not found' });
    res.json(updated);
  });

  router.delete('/:id', (req, res) => {
    const ok = service.remove(req.params.id);
    if (!ok) return res.status(404).json({ error: 'Not found' });
    res.status(204).send();
  });

  return router;
}

// Router por defecto para app real
const defaultRouter = makeBooksRouter();
export default defaultRouter;
```

**src/app.ts**

```ts
import express from 'express';
import booksRouter from './routes/books';

const app = express();
app.use(express.json());

app.get('/health', (_req, res) => res.json({ status: 'ok' }));
app.use('/books', booksRouter);

export default app;
```

**src/server.ts**

```ts
import app from './app';

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

Correr en desarrollo:

```bash
npm run dev
# GET http://localhost:3000/health
```

## 3) Tests unitarios (capa de servicio)

**tests/unit/bookService.test.ts**

```ts
import { BookService } from '../../src/services/bookService';

describe('BookService', () => {
  let service: BookService;

  beforeEach(() => {
    service = new BookService();
  });

  it('crea y lista libros', () => {
    const a = service.create({ title: 'TDD', author: 'Beck', year: 2002 });
    const b = service.create({ title: 'Clean Code', author: 'Martin', year: 2008 });

    expect(service.list()).toHaveLength(2);
    expect(service.get(a.id)?.title).toBe('TDD');
    expect(service.get(b.id)?.author).toBe('Martin');
  });

  it('actualiza parcialmente', () => {
    const a = service.create({ title: 'Foo', author: 'Bar', year: 2020 });
    const updated = service.update(a.id, { title: 'Foo 2' });
    expect(updated?.title).toBe('Foo 2');
  });

  it('elimina por id', () => {
    const a = service.create({ title: 'X', author: 'Y', year: 1999 });
    const ok = service.remove(a.id);
    expect(ok).toBe(true);
    expect(service.get(a.id)).toBeUndefined();
  });

  it('update/remove de id inexistente devuelve undefined/false', () => {
    expect(service.update('nope', { title: 'N/A' })).toBeUndefined();
    expect(service.remove('nope')).toBe(false);
  });
});
```

Correr:

```bash
npm test
```

## 4) Tests de integración (rutas Express con Supertest)

**Idea:** montar un `express()` *nuevo* para cada suite e inyectar un `BookService` limpio a `makeBooksRouter()`.

Puedes encontrar una guía rápida de cómo usar *supertest* en [el repositorio del proyecto](https://github.com/forwardemail/supertest).

**tests/integration/books.routes.test.ts**

```ts
import request from 'supertest';
import express from 'express';
import { makeBooksRouter } from '../../src/routes/books';
import { BookService } from '../../src/services/bookService';

function makeApp() {
  const app = express();
  app.use(express.json());
  const service = new BookService();
  app.use('/books', makeBooksRouter(service));
  app.get('/health', (_req, res) => res.json({ status: 'ok' }));
  return { app, service };
}

describe('Books routes', () => {
  it('GET /health responde ok', async () => {
    const { app } = makeApp();
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: 'ok' });
  });

  it('POST /books valida y crea, luego GET /books/:id', async () => {
    const { app } = makeApp();

    const create = await request(app)
      .post('/books')
      .send({ title: 'DDD', author: 'Evans', year: 2003 });

    expect(create.status).toBe(201);
    expect(create.body).toHaveProperty('id');

    const id = create.body.id as string;
    const get = await request(app).get(`/books/${id}`);
    expect(get.status).toBe(200);
    expect(get.body.title).toBe('DDD');
  });

  it('POST /books con payload inválido → 400', async () => {
    const { app } = makeApp();
    const res = await request(app).post('/books').send({ title: '', author: 'X' });
    expect(res.status).toBe(400);
    expect(res.body).toHaveProperty('error');
  });

  it('PATCH y DELETE manejan 404', async () => {
    const { app } = makeApp();
    expect((await request(app).patch('/books/zzz').send({ title: 'N/A' })).status).toBe(404);
    expect((await request(app).delete('/books/zzz')).status).toBe(404);
  });
});
```

Correr integración:

```bash
npm test
```

## 5) Cobertura, reporte y ejercicios

* **Cobertura**:

```bash
npm run coverage
# Ver carpeta coverage/ y abrir coverage/lcov-report/index.html
```

* **Ejercicio 1 (TDD):** agregar la regla “`year` no puede ser mayor al año actual”.

  1. Escribe primero el test (unitario en `bookService.test.ts` o integración al intentar crear vía POST).
  2. Hazlo fallar.
  3. Implementa la validación (en `zod` del router y/o en el servicio) y vuelve a correr.

* **Ejercicio 2:** agregar búsqueda por `?author=` en `GET /books` y testear filtrado.

* **Ejercicio 3:** agregar paginación `?page=&pageSize=` (chequear que los límites sean válidos en tests).


## 6) Buenas prácticas rápidas

* **Separar app de server** (facilita testear sin abrir puertos).
* **Inyección de dependencias** ligera (p.ej., `makeBooksRouter(service)`) para aislar estado.
* **Fixtures/Factories**: helpers para crear datos de prueba repetibles.
* **Nombrar** tests con intención y mantener 1‑2 casos por test.
* **Velocidad**: tests unitarios ≫ integración ≫ e2e.
