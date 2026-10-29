
# Fundamentos de Testing en Aplicaciones TypeScript + Express

Este apunte resume los conceptos teóricos de **testing de software** aplicados a proyectos de Node.js/Express con TypeScript. La idea es que al comprender estos fundamentos, se puedan aplicar para hacer testing de APIs.


## 1. ¿Qué es el Testing?

El testing de software es el conjunto de técnicas para verificar que un programa se comporte como se espera. No es sólo “buscar bugs”, sino también:

*   **Verificación**: ¿El sistema cumple lo especificado?
*   **Validación**: ¿El sistema satisface la necesidad del usuario?
*   **Confianza**: aumenta la calidad y permite refactorizar sin miedo.

En un equipo profesional, los tests se ejecutan automáticamente en cada cambio de código (integración continua). Esto se logra mediante herramientas de CI/CD (Continuous Integration/Continuous Deployment) como GitHub Actions, GitLab CI o Jenkins.

## 2. Tipos de tests

### 2.1. Unitarios

*   Prueban funciones o clases **aisladas**, sin dependencias externas. Esto se consigue "mockeando" o "stubbeando" las dependencias.
*   Son rápidos y fáciles de correr.
*   Ejemplo: `BookService.create()` y `BookService.list()`.

**Ejemplo de Test Unitario (Jest)**:

Imaginemos un `BookService` simple:

```typescript
// src/services/bookService.ts
export interface Book {
  id: string;
  title: string;
  author: string;
  year: number;
}

class BookService {
  private books: Book[] = [];
  private nextId = 1;

  create(title: string, author: string, year: number): Book {
    const newBook = { id: String(this.nextId++), title, author, year };
    this.books.push(newBook);
    return newBook;
  }

  list(): Book[] {
    return [...this.books]; // Devolver una copia para evitar mutaciones externas
  }

  findById(id: string): Book | undefined {
    return this.books.find(book => book.id === id);
  }
}

export const bookService = new BookService(); // Exportar una instancia singleton
```

Ahora, un test unitario para `BookService`:

```typescript
// tests/unit/bookService.test.ts
import { BookService } from '../../src/services/bookService'; // Asumimos que BookService es una clase exportada

describe('BookService (Unit Test)', () => {
  let service: BookService;

  beforeEach(() => {
    // Inicializar un nuevo servicio para cada test, asegurando aislamiento
    service = new BookService();
  });

  test('should create a new book', () => {
    const book = service.create('The Hobbit', 'J.R.R. Tolkien', 1937);
    expect(book).toBeDefined();
    expect(book.title).toBe('The Hobbit');
    expect(book.author).toBe('J.R.R. Tolkien');
    expect(book.year).toBe(1937);
    expect(service.list()).toHaveLength(1);
  });

  test('should list all created books', () => {
    service.create('Book 1', 'Author 1', 2000);
    service.create('Book 2', 'Author 2', 2001);
    const books = service.list();
    expect(books).toHaveLength(2);
    expect(books[0].title).toBe('Book 1');
    expect(books[1].title).toBe('Book 2');
  });

  test('should find a book by its ID', () => {
    const createdBook = service.create('Test Book', 'Test Author', 2023);
    const foundBook = service.findById(createdBook.id);
    expect(foundBook).toEqual(createdBook);
  });

  test('should return undefined if book ID is not found', () => {
    const foundBook = service.findById('non-existent-id');
    expect(foundBook).toBeUndefined();
  });
});
```

### 2.2. Integración

*   Comprueban cómo interactúan varias partes del sistema. Esto incluye la comunicación entre módulos, la base de datos (o un mock de ella) y la capa de red.
*   En una API, significa montar rutas de Express y verificar peticiones/respuestas. Se usa Supertest para simular estas peticiones sin levantar un servidor HTTP real.
*   Ejemplo: `POST /books` crea un libro y luego `GET /books/:id` lo recupera.

**Ejemplo de Test de Integración (Jest + Supertest)**:

Primero, necesitamos una aplicación Express.

```typescript
// src/routes/bookRoutes.ts
import { Router } from 'express';
import { bookService } from '../services/bookService';

const router = Router();

router.post('/books', (req, res) => {
  const { title, author, year } = req.body;
  if (!title || !author || !year) {
    return res.status(400).json({ message: 'Missing required fields' });
  }
  const newBook = bookService.create(title, author, year);
  res.status(201).json(newBook);
});

router.get('/books', (req, res) => {
  res.status(200).json(bookService.list());
});

router.get('/books/:id', (req, res) => {
  const book = bookService.findById(req.params.id);
  if (book) {
    res.status(200).json(book);
  } else {
    res.status(404).json({ message: 'Book not found' });
  }
});

export default router;
```

```typescript
// src/app.ts (la aplicación Express principal)
import express from 'express';
import bookRoutes from './routes/bookRoutes';

const app = express();
app.use(express.json()); // Middleware para parsear JSON en el body

app.use('/api', bookRoutes); // Prefijo para las rutas de libros

export default app; // Exportar la app para que Supertest pueda usarla
```

Ahora, el test de integración:

```typescript
// tests/integration/bookApi.test.ts
import request from 'supertest';
import app from '../../src/app'; // La app Express que exportamos
import { bookService } from '../../src/services/bookService'; // Para resetear el estado

describe('Book API (Integration Test)', () => {
  // Limpiar los libros antes de cada test para asegurar un estado limpio
  beforeEach(() => {
    // Esto es un "hack" para un servicio singleton, en una app real usarías un mock o limpiarías la DB.
    (bookService as any).books = [];
    (bookService as any).nextId = 1;
  });

  test('POST /api/books should create a new book', async () => {
    const newBook = { title: '1984', author: 'George Orwell', year: 1949 };
    const response = await request(app)
      .post('/api/books')
      .send(newBook)
      .expect(201);

    expect(response.body).toMatchObject(newBook);
    expect(response.body.id).toBeDefined();

    const books = bookService.list();
    expect(books).toHaveLength(1);
    expect(books[0]).toMatchObject(newBook);
  });

  test('GET /api/books should return all books', async () => {
    bookService.create('Book A', 'Author A', 2000);
    bookService.create('Book B', 'Author B', 2001);

    const response = await request(app)
      .get('/api/books')
      .expect(200);

    expect(response.body).toHaveLength(2);
    expect(response.body[0].title).toBe('Book A');
    expect(response.body[1].title).toBe('Book B');
  });

  test('GET /api/books/:id should return a specific book', async () => {
    const createdBook = bookService.create('Test Book', 'Test Author', 2023);

    const response = await request(app)
      .get(`/api/books/${createdBook.id}`)
      .expect(200);

    expect(response.body).toMatchObject(createdBook);
  });

  test('GET /api/books/:id should return 404 for non-existent book', async () => {
    await request(app)
      .get('/api/books/non-existent-id')
      .expect(404);
  });

  test('POST /api/books with missing fields should return 400', async () => {
    const invalidBook = { title: 'Missing Author', year: 2020 }; // Falta autor
    const response = await request(app)
      .post('/api/books')
      .send(invalidBook)
      .expect(400);

    expect(response.body.message).toBe('Missing required fields');
  });
});
```

### 2.3. End-to-End (E2E)

*   Simulan el flujo completo, desde el cliente hasta la base de datos real y el servidor en ejecución.
*   Son más lentos, pero garantizan que el sistema funciona como un todo. Requieren herramientas como Cypress o Playwright para simular interacciones de navegador o herramientas como Postman/Newman para automatizar llamadas a la API.

**Ejemplo conceptual de E2E**:

Un test E2E para la misma API de libros podría:
1.  Iniciar el servidor Express real.
2.  Hacer una petición `POST` a `/api/books` usando `axios` o `fetch` para crear un libro.
3.  Hacer una petición `GET` a `/api/books` para verificar que el libro aparece en la lista.
4.  Hacer una petición `GET` a `/api/books/:id` para obtener el libro específico.
5.  Limpiar la base de datos (si aplica) o restaurar el estado inicial.
6.  Apagar el servidor Express.

Estos tests son complejos de configurar y mantener, por lo que se usan con moderación.

**Pirámide de Testing**:
La pirámide de testing es una metáfora visual.
*   🟢 Muchos tests unitarios (base).
*   🟡 Menos tests de integración.
*   🔴 Pocos tests E2E.

## 3. Principios básicos

1.  **AAA (Arrange – Act – Assert)**
    *   **Arrange**: Preparar el escenario. Inicializar variables, configurar mocks, preparar datos de entrada.
    *   **Act**: Ejecutar la acción a probar. Llamar a la función, hacer la petición HTTP.
    *   **Assert**: Verificar el resultado esperado. Usar aserciones para comprobar el valor de retorno, el estado de un objeto, el código de respuesta, etc.

```typescript
test('should return a book if found', () => {
  // Arrange
  const mockBook = { id: '1', title: 'Test', author: 'Test', year: 2000 };
  const service = new BookService();
  service.create(mockBook.title, mockBook.author, mockBook.year);

  // Act
  const result = service.findById('1');

  // Assert
  expect(result).toEqual(mockBook);
});
```

2.  **Test Driven Development (TDD)**
    *   Escribir primero el test (que falla). Esto ayuda a definir la API de la función o módulo antes de implementarlo.
    *   Implementar el código mínimo para hacerlo pasar. Enfocarse solo en hacer que el test pase.
    *   Refactorizar manteniendo los tests verdes. Mejorar la calidad del código sin cambiar su comportamiento.

3.  **Determinismo**
    *   Los tests deben dar siempre el mismo resultado dadas las mismas entradas.
    *   Evitar dependencias externas no controladas (hora, fecha, orden de ejecución, llamadas de red a servicios externos, base de datos no reseteada). Usa mocks para esto.

4.  **Aislamiento**
    *   Cada test debe poder correr solo, sin depender de la secuencia o el estado dejado por otros tests.
    *   Usa `beforeEach` para reiniciar el estado si es necesario.

## 4. Herramientas en el ecosistema Node/TS

*   **Jest**: framework de testing popular para JavaScript/TypeScript.

    *   Permite escribir tests legibles.
    *   Integra mocks, aserciones y cobertura.
    *   Instalación: `npm install --save-dev jest @types/jest ts-jest`
    *   Configuración en `jest.config.js` (o en `package.json`):

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.ts'], // Buscar tests en la carpeta tests
};
```

*   **ts-jest**: adapta Jest para compilar TypeScript. Es el `preset` que se usa en la configuración de Jest.

*   **Supertest**: librería para enviar requests HTTP contra una app de Express en memoria. Simplifica enormemente los tests de integración de APIs.
    *   Instalación: `npm install --save-dev supertest @types/supertest`

*   **ts-node-dev**: para correr el servidor en desarrollo (no para tests). Permite auto-recarga y compilación de TypeScript en tiempo real.
    *   Instalación: `npm install --save-dev ts-node-dev`
    *   Uso en `package.json`: `"dev": "ts-node-dev src/server.ts"`

*   **zod** (u otras libs como `joi`, `yup`): validación de datos, útil para probar casos inválidos en las APIs.
    *   Instalación: `npm install zod`
    *   Ejemplo de uso para validar el body de un POST:

```typescript
// src/schemas/bookSchema.ts
import { z } from 'zod';

export const createBookSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  author: z.string().min(1, 'Author is required'),
  year: z.number().int().positive('Year must be a positive integer'),
});
```

```typescript
// Modificación en src/routes/bookRoutes.ts
import { Router } from 'express';
import { bookService } from '../services/bookService';
import { createBookSchema } from '../schemas/bookSchema';

const router = Router();

router.post('/books', (req, res) => {
  const validationResult = createBookSchema.safeParse(req.body);

  if (!validationResult.success) {
    return res.status(400).json({ errors: validationResult.error.errors });
  }

  const { title, author, year } = validationResult.data;
  const newBook = bookService.create(title, author, year);
  res.status(201).json(newBook);
});
// ... el resto de las rutas
```

## 5. Cómo estructurar un proyecto testeable

Una buena estructura facilita la organización y ejecución de tests.

*   Separar el **app** (Express con rutas, middlewares) del **server** (que hace `listen`). `app.ts` debe ser exportable para Supertest.
*   Inyectar dependencias (p.ej. un `BookService` nuevo en cada test o un mock de base de datos) en lugar de usar singletons globales cuando sea posible.
*   Mantener los tests en carpetas claras: `tests/unit/`, `tests/integration/`, `tests/e2e/`.

Ejemplo de estructura de proyecto:

```
├── src/
│   ├── app.ts            # Express app sin listen, exportable
│   ├── server.ts         # arranca el servidor (usa app.ts)
│   ├── config/           # Configuraciones (DB, env variables)
│   ├── controllers/      # Lógica de manejo de rutas (opcional, si las rutas son complejas)
│   ├── middlewares/      # Middlewares personalizados
│   ├── models/           # Definiciones de modelos de datos (interfaces, esquemas ORM)
│   ├── routes/           # Rutas de Express (importan services/controllers)
│   │   └── bookRoutes.ts
│   ├── schemas/          # Esquemas de validación (Zod, Joi)
│   │   └── bookSchema.ts
│   └── services/         # Lógica de negocio pura, sin Express (BookService)
│       └── bookService.ts
├── tests/
│   ├── integration/
│   │   └── bookApi.test.ts # Tests que usan Supertest y app.ts
│   ├── unit/
│   │   └── bookService.test.ts # Tests de funciones/clases aisladas
│   └── e2e/              # Opcional: tests end-to-end con herramientas como Playwright
├── .env                  # Variables de entorno
├── jest.config.js        # Configuración de Jest
├── package.json
├── tsconfig.json
└── README.md
```

## 6. Buenas prácticas de testing

*   Nombrar los tests de forma descriptiva: *"POST /books crea un libro válido"*, *"GET /books/:id retorna 404 si el libro no existe"*.
*   Un test debe probar **una sola cosa**; dividir en varios si hay muchos asserts o diferentes escenarios.
*   Usar `beforeEach` para preparar un estado inicial limpio antes de cada test.
*   Testear casos **felices** (cuando todo va bien) y casos **erróneos** (errores de validación, recursos no encontrados, errores internos del servidor).
*   Automatizar los tests en CI para que corran en cada `push` o `merge request`.

## 7. Ejemplos de casos de prueba típicos

*   **Servicio (unitario):**
    *   Crear un libro y verificar que aparece en la lista.
    *   Actualizar título de un libro y comprobar el cambio.
    *   Eliminar y verificar que ya no existe.
    *   Validar la lógica de negocio, por ejemplo, que no se pueda crear un libro con un año futuro.

*   **Ruta (integración):**
    *   `POST /books` con datos válidos devuelve 201 y el libro creado.
    *   `POST /books` con datos inválidos devuelve 400 y un mensaje de error claro.
    *   `GET /books` devuelve 200 y una lista (posiblemente vacía) de libros.
    *   `GET /books/:id` devuelve 200 si existe, 404 si no.
    *   `PUT /books/:id` con datos válidos devuelve 200 y el libro actualizado.
    *   `DELETE /books/:id` devuelve 204 si existe (No Content), 404 si no.
    *   Verificar middlewares de autenticación/autorización.

## 8. Cobertura de tests

La cobertura de tests indica qué porcentaje del código fue ejecutado por los tests. Jest puede generar informes de cobertura.

*   **Line coverage**: líneas de código ejecutadas.
*   **Branch coverage**: ramas de condiciones (`if/else`, `switch`, ternarios) ejecutadas.
*   **Function coverage**: funciones o métodos llamados.
*   **Statement coverage**: sentencias ejecutadas.

Comando para generar el reporte de cobertura:

```bash
npm test -- --coverage
```
O si lo tienes configurado en `package.json`:
```json
// package.json
{
  // ...
  "scripts": {
    "test": "jest",
    "coverage": "jest --coverage"
  }
}
```
Entonces, puedes correrlo con:
```bash
npm run coverage
```
Este comando generará una carpeta `coverage` con un reporte HTML (`coverage/lcov-report/index.html`) que puedes abrir en el navegador para una visualización detallada.

Interpretar el reporte para identificar código sin testear (generalmente resaltado en rojo) y priorizar la escritura de tests para esas partes. Un 100% de cobertura no garantiza un sistema libre de bugs, pero una cobertura baja sí es una alerta.

## 9. Ejercicios sugeridos

1.  **Validación de año (Unitario y Integración):**
    *   Agregar la validación en `bookService.create()`: *el año de un libro no puede ser mayor al actual*.
    *   **Escribir primero el test unitario** para `bookService` (que falle).
    *   **Implementar la regla** en el servicio para que el test pase.
    *   **Escribir un test de integración** para `POST /api/books` con un año futuro, esperando un 400 Bad Request.

```typescript
// tests/unit/bookService.test.ts (ejercicio)
test('should not create a book with a future year', () => {
  const currentYear = new Date().getFullYear();
  expect(() => service.create('Future Book', 'Author', currentYear + 1))
    .toThrow('Year cannot be in the future');
});

// src/services/bookService.ts (ejercicio, modificación en create)
create(title: string, author: string, year: number): Book {
  const currentYear = new Date().getFullYear();
  if (year > currentYear) {
    throw new Error('Year cannot be in the future');
  }
  // ... el resto de la lógica de creación
}
```

2.  **Filtrado por autor (Integración):**
    *   Implementar filtrado por autor en `GET /books?author=`.
    *   **Escribir un test de integración** que cree varios libros con distintos autores y luego haga una petición `GET /api/books?author=AutorX` esperando solo los libros de `AutorX`.
    *   Modificar la ruta `GET /books` en `src/routes/bookRoutes.ts` para aplicar el filtro.

```typescript
// src/routes/bookRoutes.ts (ejercicio, modificación en GET /books)
router.get('/books', (req, res) => {
  const { author } = req.query;
  let books = bookService.list();
  if (author && typeof author === 'string') {
    books = books.filter(book => book.author.toLowerCase().includes(author.toLowerCase()));
  }
  res.status(200).json(books);
});

// tests/integration/bookApi.test.ts (ejercicio)
test('GET /api/books?author= should filter books by author', async () => {
  bookService.create('Book A', 'Author X', 2000);
  bookService.create('Book B', 'Author Y', 2001);
  bookService.create('Book C', 'Author X', 2002);

  const response = await request(app)
    .get('/api/books?author=Author X')
    .expect(200);

  expect(response.body).toHaveLength(2);
  expect(response.body[0].author).toBe('Author X');
  expect(response.body[1].author).toBe('Author X');
});
```

3.  **Paginación (Integración):**
    *   Agregar paginación con `?page=&pageSize=` a `GET /books`.
    *   **Escribir tests de integración** que verifiquen el comportamiento de la paginación (ej: `page=1&pageSize=2` devuelve los dos primeros libros).
    *   Modificar la ruta `GET /books` en `src/routes/bookRoutes.ts`.

4.  **Test de dos libros distintos (Integración):**
    *   Escribir un test de integración que cree dos libros distintos y luego verifique que ambos se listan correctamente en `GET /books`. (Este ya está cubierto parcialmente en el ejemplo de integración, pero puedes expandirlo).

## 10. Conclusión

Testing no es opcional: es parte del ciclo de desarrollo profesional. Un código sin tests es un código que no se puede refactorizar con confianza y que es propenso a errores silenciosos.
Al dominar unitarios e integración con Jest y Supertest, los estudiantes podrán crear APIs robustas, refactorizar sin miedo y avanzar hacia prácticas modernas como TDD y CI/CD.
