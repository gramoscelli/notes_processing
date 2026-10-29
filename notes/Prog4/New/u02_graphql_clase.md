# Guion de clase — GraphQL: el cliente decide la forma de la respuesta

> Notas para dictar la clase. Siguen el orden real de exposición, con lo que se dice,
> lo que va en pantalla y las preguntas que se lanzan.
> Apunte del alumno: [GraphQL: otra forma de exponer la misma API](u02_graphql.md).

---

## 1. Apertura: contar las requests

No empezamos con la definición de GraphQL. Empezamos con el problema, y el problema se
mide.

**En pantalla**, la pantalla de inicio de la app: una lista de veinte libros, y de cada
uno se muestra **título y autor**. Dos líneas de texto.

Y lo que devuelve `GET /v1/books`:

```json
{ "id": "...", "title": "Rayuela", "author": "Cortázar", "year": 1963,
  "isbn": "...", "synopsis": "… 2 KB de texto …", "coverUrl": "...",
  "publisher": { "..." }, "stock": 12 }
```

*Pregunta: con veinte libros por página, ¿cuántos kilobytes bajamos para pintar
cuarenta líneas de texto?*

Decenas. Y la sinopsis, que es el 90 % del peso, no se muestra en ningún lugar de esa
pantalla. Eso se llama **over-fetching**.

Ahora la pantalla de detalle: el libro, su autor con biografía, y las reseñas con el
nombre de cada usuario.

**En el pizarrón, y se cuenta en voz alta:**

```text
GET /v1/books/7                 → 1 request
GET /v1/authors/3               → 1 request
GET /v1/books/7/reviews         → 1 request
GET /v1/users/{id} × 10         → 10 requests
                                 ─────────────
                                   13 requests
```

Y lo peor no es el trece. Lo peor es que son **en cascada**: hasta que no vuelve
`/books/7` no sé qué autor pedir. Las latencias no se solapan, se suman. En un 4G malo,
trece round-trips son segundos. Eso es **under-fetching**.

**La frase del pizarrón:**

> El servidor decide la forma de la respuesta. Si la forma que necesita la pantalla no
> es la que el servidor decidió, el cliente paga: en bytes o en round-trips.

---

## 2. REST ya tenía respuestas (y por qué no alcanzan)

Antes de vender nada, hay que ser honestos: REST tiene soluciones para esto.

```text
GET /v1/books?fields=title,author           ← sparse fieldsets
GET /v1/books/7?include=author,reviews.user ← inclusión de relaciones
```

Y funcionan. El problema es otro:

* Cada API inventa su propia sintaxis (`fields`, `select`, `only`, `$select`…).
* Hay que implementarla **a mano, endpoint por endpoint**.
* Documentar qué combinaciones de `include` son válidas se vuelve inmanejable.

> GraphQL no inventó la idea. Tomó esa idea y la convirtió en **el modelo central**, con
> un lenguaje de consulta definido y un esquema tipado que lo describe.

**En pantalla**, lo mismo que las trece requests, en una:

```graphql
query DetalleDeLibro {
  book(id: "7") {
    title
    year
    author { name bio }
    reviews(first: 10) { rating text user { name } }
  }
}
```

Una request. Una respuesta. Exactamente esos campos, ni uno más.

**Y conviene decirlo ya, antes de que se entusiasmen:** esas trece requests **no
desaparecieron**. Se mudaron al servidor. La sección 7 de hoy es sobre eso, y es la
mitad importante de la clase.

---

## 3. El esquema es la API

En GraphQL el esquema no es documentación opcional como el OpenAPI de la clase pasada:
**es** la API. Si no está en el esquema, no se puede pedir.

```graphql
type Book {
  id: ID!
  title: String!
  author: String!
  year: Int!
}

input NewBookInput {
  title: String!
  author: String!
  year: Int!
}

type Query {
  book(id: ID!): Book
  books(page: Int = 1, pageSize: Int = 20,
        sort: BookSort = TITLE, filter: BookFilter): BookPage!
}

type Mutation {
  createBook(input: NewBookInput!): Book!
  updateBook(id: ID!, input: UpdateBookInput!): Book!
  deleteBook(id: ID!): Boolean!
}
```

### 3.1 El `!` es la decisión de diseño de cada campo

*Pregunta: ¿qué significa el signo de exclamación?*

"No nulo". Hasta ahí es fácil. Lo que hay que leer despacio es la tabla de listas:

| Declaración | Significa |
|---|---|
| `title: String` | puede venir `null` |
| `title: String!` | nunca es `null` |
| `items: [Book]` | la lista puede ser `null`, y puede contener `null` |
| `items: [Book!]` | la lista puede ser `null`, pero sin elementos `null` |
| `items: [Book!]!` | ni la lista ni sus elementos son `null` |

**Y el peligro, que es contraintuitivo:** si un campo `author: Author!` falla al
resolverse, GraphQL no puede devolver `null` ahí. Así que **propaga el null hacia
arriba** y anula el objeto padre entero.

*Pregunta: ¿qué pasa entonces si el servicio de autores se cae y `Book.author` es
`Author!`?*

Desaparece el libro de la respuesta. Y si `items: [Book!]!`, desaparece la lista. Un
campo no-nulo que depende de un sistema externo puede borrar toda la respuesta.

**La regla práctica:** `!` en lo que es estructuralmente imposible que falte — ids,
campos propios. Opcional en todo lo que viene de otro sistema.

### 3.2 `type` y `input` son mundos separados

No se puede usar un `type` como argumento ni un `input` como retorno. Es verboso y
molesta al principio, pero es exactamente la distinción `Book` / `NewBook` que hicimos
en REST: `Book` tiene `id: ID!` porque lo genera el servidor; `NewBookInput` no lo
tiene.

### 3.3 Lo que el esquema NO tiene

Esto es lo que quiero que noten solos.

*Pregunta: ¿qué cosas de las dos clases anteriores no aparecen en ninguna parte de este
esquema?*

No hay URLs. No hay métodos HTTP. No hay status codes. Todo pasa por un solo endpoint,
`POST /graphql`, y la respuesta es **siempre** `200`.

Tiren eso al aire y déjenlo: tiene consecuencias serias para caché y para errores, y las
vemos en 6 y en 8.

---

## 4. Resolvers: la parte que ya está escrita

Un *resolver* es la función que sabe producir el valor de un campo. La firma es siempre
la misma:

```ts
(parent, args, context, info) => valor
```

| Parámetro | Qué es |
|---|---|
| `parent` | el resultado del resolver padre (en `Query` viene `undefined`) |
| `args` | los argumentos, **ya validados** contra el esquema |
| `context` | lo compartido por request: usuario, servicios, loaders |
| `info` | el AST de la query; útil para optimizar, rara vez necesario |

Marcar `args`: no hay Zod acá. El esquema ya garantizó que `id` es un `ID!` y que
`pageSize` es un `Int`. Esa validación es gratis.

**En pantalla**, el resolver de `book`:

```ts
book: (_p, { id }, { service }: Ctx) => {
  const book = service.findById(id);
  if (!book) {
    throw new GraphQLError('Libro no encontrado', {
      extensions: { code: 'NOT_FOUND', id }
    });
  }
  return book;
}
```

*Pregunta: ¿cuánta lógica de negocio hay en ese resolver?*

Ninguna. Llama a `service.findById`. **El mismo `BookService` que usan las rutas REST.**

**La frase del pizarrón, y es la arquitectura de toda la unidad:**

> REST y GraphQL son dos capas de **transporte** sobre un mismo núcleo de dominio.

```text
        BooksRouter (REST) ─┐
                            ├─→ BookService ─→ (Unidad 4: base de datos)
      GraphQLResolvers ─────┘
```

Si la regla "el año no puede ser futuro" viviera en el router de Express, habría que
duplicarla acá. Y cuando algo se duplica, una de las dos copias queda vieja. Cuando ese
núcleo hable con una base de datos real, las dos capas van a seguir funcionando sin
tocar una línea.

---

## 5. Montarlo en el Express que ya tenemos

```bash
npm i graphql graphql-yoga
```

```ts
export function makeApp() {
  const app = express();
  const service = new BookService();

  // GraphQL ANTES de express.json(): Yoga parsea su propio body.
  app.use('/graphql', makeYoga(service));

  app.use(express.json());
  app.use('/v1/books', makeBooksRouter(service));
  app.use(errorHandler);
  return app;
}
```

**Detenerse en ese comentario. Es el bug de los cinco minutos perdidos.**

Si `express.json()` corre primero, consume el stream del body. Yoga recibe una request
vacía y tira un error que no dice absolutamente nada útil. Montá GraphQL antes, o
restringí el parser con `app.use('/v1', express.json())`.

Y señalar lo que queda: las dos interfaces conviven en el mismo proceso, sobre el mismo
servicio.

```text
POST /v1/books   → REST
GET  /v1/books   → REST
POST /graphql    → GraphQL
GET  /graphql    → GraphiQL (sólo en dev)
```

**Demo:** abrir `http://localhost:3000/graphql`, escribir la query en GraphiQL con
autocompletado, ejecutarla. Después **borrar un campo** de la query y ejecutar de nuevo,
para que vean que la respuesta cambia de forma sin tocar el servidor. Ese es el momento
de la clase.

```bash
curl -s localhost:3000/graphql -H 'content-type: application/json' \
  -d '{"query":"{ books(pageSize: 3, sort: DESC_YEAR) { items { title year } pageInfo { total } } }"}'
```

**Nota al margen, porque van a googlear:** `@apollo/server` hace lo mismo y es el
estándar de facto en la industria. Yoga necesita menos configuración y se monta directo
como middleware. Los conceptos — esquema, resolvers, context, loaders — son idénticos en
los dos.

---

## 6. Errores: GraphQL siempre contesta 200

Acá GraphQL rompe con todo lo que diseñamos en las dos clases anteriores.

```json
{
  "data": { "book": null },
  "errors": [
    { "message": "Libro no encontrado",
      "path": ["book"],
      "extensions": { "code": "NOT_FOUND", "id": "999" } }
  ]
}
```

Status de esa respuesta: **200 OK**.

*Pregunta: ¿se acuerdan del primer error de diseño de la lista de la clase de REST?*

"`200 OK` con un `error` adentro". Lo pusimos como antipatrón. Y GraphQL lo hace por
diseño. No es una contradicción: es que GraphQL no usa HTTP como protocolo semántico,
lo usa como transporte. Pero hay que pagar el precio y saber cuál es:

* `res.ok` en el cliente **no sirve** para saber si la operación funcionó. Hay que mirar
  `errors`.
* El monitoreo por status code no ve nada: todo es `200`. Hay que instrumentar a nivel
  de resolver.
* Una respuesta puede ser **parcialmente exitosa**: `data` con lo que resolvió y
  `errors` con lo que no. Eso no tiene ningún equivalente en REST.

### 6.1 `extensions.code` es el nuevo status code

Como no hay status codes, el contrato de errores se define en `extensions.code`. Es el
equivalente exacto del `type` de `problem+json`.

```ts
export const notFound = (what: string, id: string) =>
  new GraphQLError(`${what} no encontrado`, {
    extensions: { code: 'NOT_FOUND', id }
  });

export const businessRule = (detail: string) =>
  new GraphQLError('Regla de negocio violada', {
    extensions: { code: 'BUSINESS_RULE', detail }
  });
```

Mismo criterio que con `problem+json`: la lista de códigos es **cerrada** y es parte del
contrato. El cliente programa contra `code`, nunca contra `message`.

### 6.2 Y no filtrar el stack trace

```ts
createYoga({
  schema,
  maskedErrors: {
    maskError(error, message) {
      if (error instanceof GraphQLError && error.extensions?.code) {
        return error;              // errores nuestros, intencionales
      }
      console.error(error);        // el resto se loguea y se enmascara
      return new GraphQLError(message);
    }
  }
});
```

Yoga ya enmascara en producción, pero ser explícito acá vale: el criterio es *mis
errores pasan, los inesperados se loguean y salen genéricos*.

---

## 7. El N+1, que es el problema de GraphQL

Esta es la sección más importante de la clase. Si se van con una sola cosa, que sea esta.

Agreguemos el autor como relación:

```graphql
type Book { id: ID! title: String! author: Author! }
```

```ts
const resolvers = {
  Book: {
    author: (book, _args, { authorService }) =>
      authorService.findById(book.authorId)   // ← una consulta POR LIBRO
  }
};
```

Y esta query, que parece inofensiva:

```graphql
{ books(pageSize: 50) { items { title author { name } } } }
```

*Pregunta: ¿cuántas consultas a la base de datos dispara?*

Una para los cincuenta libros, y **cincuenta** de autor. Una por libro, aunque cuarenta
compartan el mismo autor.

**El remate:**

> Es exactamente el N+1 de la apertura de la clase. GraphQL **no lo eliminó**: lo movió
> de la red del cliente al servidor, donde es más barato pero no gratis. Y ahora el
> cliente lo puede provocar sin saberlo, pidiendo un campo más.

### 7.1 DataLoader

Dos mecanismos: **batching** (juntar todas las cargas de un mismo tick del event loop
en una consulta) y **caching por request** (no pedir dos veces el mismo id).

```ts
export function createLoaders(authorService: AuthorService) {
  return {
    authorById: new DataLoader<string, Author>(async (ids) => {
      // UNA sola consulta para todos los ids del tick
      const authors = await authorService.findByIds([...ids]);
      const byId = new Map(authors.map(a => [a.id, a]));

      // CRÍTICO: devolver en el MISMO orden y largo que `ids`
      return ids.map(id => byId.get(id) ?? new Error(`Author ${id} no existe`));
    })
  };
}
```

```ts
// el resolver no cambia de forma, cambia de quién pide
author: (book, _args, { loaders }) => loaders.authorById.load(book.authorId)
```

**Resultado: 2 consultas en lugar de 51.** Y el resolver quedó igual de simple.

**Las dos reglas que no se pueden saltear.** Estas dos van al pizarrón porque son dos
bugs silenciosos:

1. **Los loaders se crean por request**, en el `context`. Un loader global cachearía
   datos entre usuarios distintos: es un bug de corrección **y** una filtración de
   datos.
2. **La función de batch devuelve el mismo largo y el mismo orden que los ids.**
   DataLoader hace la correspondencia **por posición**. Si filtran los no encontrados,
   los autores quedan asignados al libro equivocado, en silencio, sin ningún error.

La segunda es de las que cuesta medio día encontrar. Por eso se devuelve un `Error` en
la posición del que falta, nunca se acorta el array.

### 7.2 El cliente decide el costo de la query

Y queda un agujero. Un cliente puede escribir esto:

```graphql
{ books { items { author { books { items { author { books { ... } } } } } } } }
```

*Pregunta: ¿qué hace el servidor con eso?*

Una sola request que genera millones de consultas. En REST esto **no existe**: cada
endpoint tiene un costo acotado por quien lo escribió. En GraphQL el costo lo decide el
cliente, así que hay que ponerle techo:

```ts
createYoga({
  schema,
  plugins: [
    maxDepthPlugin({ n: 7 }),
    costLimitPlugin({ maxCost: 5000 })
  ]
});
```

Y en producción, **apagar la introspección**: si no, cualquiera se descarga el esquema
completo. (`graphiql: false` ya lo deshabilita en Yoga, pero verificalo explícitamente.)

**La frase del pizarrón:**

> Un endpoint GraphQL público sin límite de profundidad, límite de costo y rate limiting
> es un DoS esperando a que alguien lo descubra.

---

## 8. La comparación honesta

Recién ahora, con los dos modelos completos, se puede comparar. **En pantalla**, y se
lee de corrido:

| Dimensión | REST | GraphQL |
|---|---|---|
| Endpoints | muchos, uno por recurso | uno (`/graphql`) |
| Forma de la respuesta | la decide el servidor | la decide el cliente |
| Over/under-fetching | hay que mitigarlo a mano | resuelto por diseño |
| Caché HTTP (navegador, CDN, proxy) | ✅ gratis, por URL + `ETag` | ❌ `POST` no se cachea |
| Status codes | semánticos y útiles | siempre `200` |
| Tipado del contrato | con OpenAPI (opcional) | obligatorio, es el esquema |
| Costo de una request | acotado por el endpoint | **lo decide el cliente** |
| Subida de archivos | natural (`multipart`) | incómoda, requiere spec aparte |
| Observabilidad | por URL y status, directa | requiere instrumentar resolvers |
| Versionado | por URL (`/v1`, `/v2`) | evolución continua con `@deprecated` |

La fila de la caché es la que más subestiman. Perder la caché HTTP gratis —la del
navegador, la del CDN, la del proxy— no es un detalle: es reemplazarla por una caché de
aplicación que hay que construir y mantener.

### 8.1 Evolución sin versiones

```graphql
type Book {
  title: String!
  year: Int! @deprecated(reason: "Usar publishedAt. Se elimina en 2026-08.")
  publishedAt: String!
}
```

GraphQL propone no versionar: agregar campos nuevos no rompe a nadie, porque los
clientes piden explícitamente lo que quieren. Y con métricas de uso **por campo** se
sabe cuándo nadie pide más `year`.

*Pregunta: ¿por qué en REST no podemos hacer esto?*

Porque en REST el servidor no sabe qué campos usó cada cliente: manda el objeto entero
siempre. Es una versión más fina y más medible del `Deprecation` / `Sunset` que vimos, y
funciona por una propiedad que REST no tiene.

### 8.2 Cuándo elegir cada uno

**REST cuando:** la API es pública o la consume gente que no controlás; la caché HTTP
importa; hay archivos, streaming o descargas; el equipo es chico y el dominio simple
—un CRUD con GraphQL es más infraestructura para el mismo resultado.

**GraphQL cuando:** hay varios clientes con necesidades distintas sobre el mismo
dominio; el grafo de relaciones es profundo y el front arma vistas muy compuestas; el
front itera rápido y pedir un endpoint nuevo por cada pantalla es el cuello de botella;
mobile con conexiones malas.

**Y la opción que nadie menciona en los tutoriales:** se pueden usar los dos, como
hicimos hoy. Un GraphQL interno para tus propios front-ends y una API REST versionada
para integraciones de terceros es una arquitectura común y perfectamente sana.

> **El error a evitar:** adoptar GraphQL porque "es más moderno". No lo es, es
> *distinto*. Si el problema no es ninguno de esos cuatro, GraphQL agrega esquema,
> resolvers, loaders, límites de profundidad y una caché propia para resolver un
> problema que no tenías.

Esta es la parte que les va a servir en una entrevista de trabajo, y la que quiero que
recuerden: la respuesta correcta a "¿REST o GraphQL?" nunca es una de las dos sola, es
"¿cuántos clientes distintos tenés y cuánto te importa la caché?".

---

## 9. Testear GraphQL

El transporte sigue siendo HTTP, así que Supertest funciona igual que siempre:

```ts
const gql = (app, query: string, variables?: object) =>
  request(app).post('/graphql')
    .set('content-type', 'application/json')
    .send({ query, variables });
```

Y el test que importa:

```ts
it('devuelve NOT_FOUND con código, no un 404', async () => {
  const res = await gql(app(), `{ book(id: "no-existe") { title } }`);

  expect(res.status).toBe(200);                       // ← siempre 200
  expect(res.body.data.book).toBeNull();
  expect(res.body.errors[0].extensions.code).toBe('NOT_FOUND');
});
```

Señalar ese `expect(res.status).toBe(200)` **dentro de un test de error**. Parece un
error del test. Es la diferencia de modelo escrita de forma explícita, para que nadie la
"arregle" a `404` dentro de seis meses.

Y el que protege el esquema, que es el `openapi:check` de esta clase:

```bash
npx graphql-inspector diff schema-base.graphql src/graphql/schema.graphql
```

Falla en CI ante cualquier cambio *breaking* del esquema: quitar un campo, volver
nullable algo que no lo era. Mismo patrón que la clase pasada, otra herramienta.

---

## 10. Cierre de la unidad

Las tres clases, en una línea cada una:

> **Diseño REST** — la API tiene un contrato: recursos, métodos con semántica, errores
> uniformes, colecciones navegables.
> **OpenAPI** — ese contrato está escrito en un archivo que se genera del código y que
> CI no deja mentir.
> **GraphQL** — el mismo dominio, expuesto con otro modelo, donde la forma de la
> respuesta la decide el cliente y el costo también.

Y lo que quiero que quede del conjunto, más que cualquier herramienta:

> El `BookService` no cambió en ninguna de las tres clases. Cambiaron las capas de
> arriba. Eso es lo que hace que una API sobreviva a sus propias decisiones de
> transporte.

En la unidad que viene, ese servicio deja de guardar libros en un array y empieza a
hablar con una base de datos. Las dos interfaces van a seguir funcionando sin que
toquemos ni el router ni los resolvers. Si eso pasa, la arquitectura estaba bien.

---

## 11. Comandos de la demo

```bash
# Instalar
npm i graphql graphql-yoga dataloader
npm i @escape.tech/graphql-armor-max-depth @escape.tech/graphql-armor-cost-limit

# Levantar: GraphiQL en el browser
npm run dev
#   → http://localhost:3000/graphql

# La misma query, dos formas distintas (quitar campos y ver la respuesta cambiar)
curl -s localhost:3000/graphql -H 'content-type: application/json' \
  -d '{"query":"{ books(pageSize: 3) { items { title } } }"}'

curl -s localhost:3000/graphql -H 'content-type: application/json' \
  -d '{"query":"{ books(pageSize: 3, sort: DESC_YEAR) { items { title year } pageInfo { total } } }"}'

# Un error: 200 OK con errors[] adentro. Mirar el -i.
curl -si localhost:3000/graphql -H 'content-type: application/json' \
  -d '{"query":"{ book(id: \"no-existe\") { title } }"}' | head -20

# REST y GraphQL sobre el mismo servicio, en el mismo proceso
curl -s localhost:3000/v1/books | jq '.meta'

# El N+1: con los logs de consultas encendidos, contar las líneas
curl -s localhost:3000/graphql -H 'content-type: application/json' \
  -d '{"query":"{ books(pageSize: 50) { items { title author { name } } } }"}' > /dev/null
#   antes de DataLoader: 51 consultas | después: 2

# El límite de profundidad rechazando la query maliciosa
curl -s localhost:3000/graphql -H 'content-type: application/json' \
  -d '{"query":"{ books { items { author { books { items { author { books { items { title } } } } } } } } }"}' \
  | jq '.errors[0].message'

# Tests
npx vitest run tests/integration/graphql.books.test.ts

# El guardián del esquema
npx graphql-inspector diff schema-base.graphql src/graphql/schema.graphql
```
