# Guion de clase — OpenAPI: el contrato escrito y Swagger UI

> Notas para dictar la clase. Siguen el orden real de exposición, con lo que se dice,
> lo que va en pantalla y las preguntas que se lanzan.
> Apunte del alumno: [Documentar la API con OpenAPI 3.1 y Swagger UI](u02_openapi.md).

---

## 1. Apertura: la pregunta que quedó abierta

La clase pasada cerramos con una pregunta sin contestar. La vuelvo a poner:

> Diseñamos un contrato completo: `{ data, meta, links }`, `400` contra `422`,
> `problem+json`, el tope de `pageSize`, la whitelist de `sort`.
> ¿Dónde está escrito ese contrato?

La respuesta honesta es: en nuestra cabeza y en los tests. Y los tests sólo los lee
quien tiene el repo.

*Pregunta: si el grupo que hace el front necesita saber que `meta.totalPages` existe,
¿cómo se entera hoy?*

Las tres respuestas que van a dar son las tres que queremos eliminar: pregunta por
WhatsApp, abre Postman y prueba, o lee el código del back. Las tres son trabajo
humano repetido, y las tres caducan sin avisar.

**Demo del problema, con un README de verdad:**

```markdown
## GET /books
Devuelve un array de libros.
```

Eso fue verdad hace tres semanas. Hoy devuelve `{ data, meta, links }`. Nadie
actualizó el README porque **nada lo obliga**.

**La frase del pizarrón:**

> La documentación en prosa no tiene cómo ser verdad. Un documento OpenAPI sí,
> porque lo lee una máquina y porque se puede testear contra la API.

---

## 2. Qué compra un documento legible por máquinas

Lo primero que hay que sacarles de la cabeza: OpenAPI **no es documentación**. Es un
archivo del que se derivan cosas.

**En pantalla**, el abanico:

```text
openapi.yaml ──→ Swagger UI (documentación navegable y ejecutable)
             ──→ Clientes tipados (TypeScript, Java, Python)
             ──→ Servidor mock
             ──→ Tests de contrato
             ──→ Detección de breaking changes en CI
             ──→ Configuración del API Gateway
```

Traducido a la cursada, que es lo que les importa:

* El grupo del front **arranca antes** que el back, contra un mock generado del documento.
* Nadie pregunta qué devuelve un endpoint: lo abre en `/docs` y lo ejecuta.
* Si el back cambia una respuesta sin avisar, **falla un test**.

**Aclaración de nombres, que siempre se confunde:** "Swagger" era el nombre de la
especificación hasta la 2.0. Desde la 3.0 la especificación se llama **OpenAPI** y
*Swagger* quedó como marca de las herramientas. Nosotros usamos **OpenAPI 3.1**, que
es la primera versión 100 % compatible con JSON Schema — y eso va a importar mucho en
la segunda mitad de la clase.

---

## 3. Anatomía: cinco secciones y dos versiones

**En pantalla**, el esqueleto completo, sin detalle:

```yaml
openapi: 3.1.0          # versión de la ESPECIFICACIÓN
info:                   # metadatos: title, version, description
servers:                # dónde vive: dev, producción
paths:                  # los endpoints
components:             # piezas reutilizables
```

Cinco claves. Todo documento OpenAPI del mundo tiene esta forma.

*Pregunta: hay dos campos que se llaman "version" acá. ¿Son lo mismo?*

No, y confundirlos es un clásico:

| | Qué es |
|---|---|
| `openapi: 3.1.0` | la versión del **formato del documento** |
| `info.version: 1.0.0` | la versión de **tu API**, en semver |

Son independientes. Puedo describir mi API `3.4.1` en un documento OpenAPI `3.1.0`.

### 3.1 La unidad mínima: una operación

Cada combinación de **path + método** es una *operación*. Esta es la que vamos a leer
línea por línea:

```yaml
paths:
  /v1/books/{id}:
    get:
      operationId: getBookById
      summary: Obtiene un libro por id
      tags: [Books]
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: El libro solicitado
          content:
            application/json:
              schema: { $ref: '#/components/schemas/BookEnvelope' }
        '404':
          $ref: '#/components/responses/NotFound'
```

Tres cosas que marcar mientras se lee:

* **`operationId`** es único en todo el documento, y no es decorativo: los generadores
  de clientes lo usan como nombre de método. Este `operationId` es el que hace que el
  front escriba `api.getBookById('7')`. Si lo llamás `get1`, el front va a escribir
  `api.get1('7')` para siempre.
* **`tags`** es la única navegación que tiene Swagger UI. Un tag por recurso.
* **`parameters`** con `in: path` es **siempre** `required: true`. No existe un path
  param opcional: si no está, es otra URL.

**Y el detalle que les va a pasar:** si `/v1/books/{id}` tiene `get`, `patch` y
`delete`, el `id` se declara **una vez** a nivel del path, no tres veces dentro de cada
método.

---

## 4. Components: la regla de las dos veces

```yaml
components:
  schemas:
    Book: { ... }
    NewBook: { ... }
    BookPatch:
      type: object
      minProperties: 1          # un PATCH vacío no tiene sentido
      properties: { ... }
    BookEnvelope:
      type: object
      required: [data]
      properties:
        data: { $ref: '#/components/schemas/Book' }
```

**La regla, y es toda la sección:**

> Si algo aparece dos veces en el documento, va a `components`.

Si escribieron dos veces la misma respuesta `404`, está mal. Y marcar `minProperties: 1`
en `BookPatch`: es la misma decisión que tomamos la clase pasada en Zod con
`.partial().refine(...)`, expresada en el documento.

### 4.1 La tentación de `readOnly`

```yaml
id:       { type: string, readOnly: true }   # aparece en respuestas, no se envía
password: { type: string, writeOnly: true }  # se envía, nunca vuelve
```

Con esto se podría describir `Book` **una sola vez** en lugar de mantener `Book` y
`NewBook`. Es válido y es más corto. Nosotros igual mantenemos los dos tipos separados,
porque es más explícito y porque dentro de un rato los vamos a derivar uno del otro con
una línea de código, y ahí la separación sale gratis.

### 4.2 Si encuentran ejemplos de 3.0 en internet

Les va a pasar: la mitad de los tutoriales son 3.0 y no compilan igual.

| 3.0 | 3.1 |
|---|---|
| `nullable: true` | `type: [string, 'null']` |
| `example: 'Rayuela'` | `examples: ['Rayuela']` |
| JSON Schema "parecido" | JSON Schema Draft 2020-12, de verdad |

---

## 5. Swagger UI, en vivo

Acá se cambia de modo: se deja de leer YAML y se pasa al navegador.

```bash
npm i swagger-ui-express yaml
npm i -D @types/swagger-ui-express
```

```ts
// src/app.ts
if (process.env.NODE_ENV !== 'production') {
  const doc = loadOpenApiDocument();
  app.get('/openapi.json', (_req, res) => res.json(doc));
  app.use('/docs', swaggerUi.serve, swaggerUi.setup(doc, {
    customSiteTitle: 'API de Libros'
  }));
}
```

**Demo:** `npm run dev`, abrir `http://localhost:3000/docs`, desplegar `POST /v1/books`,
apretar **Try it out** y crear un libro de verdad desde el navegador. Después
`GET /v1/books` y que vean aparecer el libro que acaban de crear.

Ese momento es el que vende la clase: la documentación no describe la API, **la ejecuta**.

*Pregunta: ¿esto lo dejarían encendido en producción?*

Es una decisión, no un dogma, y vale discutirla treinta segundos. Publicar el documento
le entrega a cualquiera el mapa completo: todos los endpoints, todos los campos, todos
los formatos. **No es una vulnerabilidad en sí misma** — una API bien hecha no depende
de que sus URLs sean secretas — pero sí le ahorra el trabajo de reconocimiento a un
atacante. Criterio: si la API es pública, publicalo; si es interna, dejalo detrás de la
misma autenticación que el resto.

---

## 6. El problema de fondo: dos descripciones del mismo contrato

Y acá viene el giro de la clase. Lo que tenemos ahora no está bien.

**En pantalla, los dos archivos juntos:**

```ts
// src/routes/books.query.ts  → valida en runtime
export const newBookSchema = z.object({
  title: z.string().min(1),
  author: z.string().min(1),
  year: z.number().int().max(new Date().getFullYear())
});
```

```yaml
# openapi.yaml → documenta
NewBook:
  required: [title, author, year]
  properties: { ... }
```

*Pregunta: ¿qué pasa el día que alguien agrega `isbn` al schema de Zod?*

El endpoint lo acepta. El documento sigue diciendo que no existe. El front no lo manda
nunca. Y nadie se enteró de nada.

**La frase del pizarrón:**

> Dos descripciones del mismo hecho se desincronizan. No es una posibilidad: es
> cuestión de tiempo.

Esto es exactamente el problema del README del principio de la clase, una vuelta más
arriba. La solución no es "acordarse de actualizar las dos": es que haya **una sola**
y que la otra se **derive**.

---

## 7. Generar el documento desde Zod

El schema de Zod ya existe y ya valida en runtime. Que sea él la fuente de verdad.

```bash
npm i @asteasolutions/zod-to-openapi
```

```ts
import { extendZodWithOpenApi } from '@asteasolutions/zod-to-openapi';

extendZodWithOpenApi(z);   // agrega el método .openapi() a Zod

export const BookSchema = z.object({
  id:     z.string().uuid().openapi({ example: '3f1a...' }),
  title:  z.string().min(1).openapi({ example: 'Rayuela' }),
  author: z.string().min(1).openapi({ example: 'Julio Cortázar' }),
  year:   z.number().int().openapi({ example: 1963 })
}).openapi('Book');          // ← el nombre en components/schemas

export const NewBookSchema   = BookSchema.omit({ id: true }).openapi('NewBook');
export const BookPatchSchema = NewBookSchema.partial().openapi('BookPatch');
```

**Lo que hay que señalar con el dedo son esas dos últimas líneas.** `NewBook` y
`BookPatch` no son copias de `Book`: son **transformaciones** de `Book`. `.omit()` y
`.partial()`. Es imposible que queden desalineados, porque no hay dos definiciones —
hay una y dos derivaciones.

Comparen con la sección 4, donde manteníamos los tres schemas a mano en el YAML.

Después se registran los paths y se genera:

```ts
registry.registerPath({
  method: 'get',
  path: '/v1/books',
  operationId: 'listBooks',
  tags: ['Books'],
  request: { query: listBooksQuery },   // ← el MISMO schema que valida la request
  responses: { 200: { /* ... */ } }
});
```

**Esa línea `request: { query: listBooksQuery }` es el corazón de la clase.** El schema
que documenta la query es el mismo objeto que la valida en el middleware. El tope de
`pageSize` y la whitelist de `sort` que diseñamos la clase pasada quedan documentados
sin que nadie los escriba dos veces.

---

## 8. `openapi:check`: convertir una buena intención en una garantía

```json
{
  "scripts": {
    "openapi": "tsx scripts/generate-openapi.ts",
    "openapi:check": "tsx scripts/generate-openapi.ts && git diff --exit-code openapi.yaml"
  }
}
```

Ese `git diff --exit-code` merece treinta segundos de explicación, porque es un truco
que les va a servir para muchas otras cosas: regenera el artefacto y **falla si el
resultado difiere de lo que está commiteado**.

*Pregunta: ¿qué pasa si alguien cambia un schema de Zod y no corre `npm run openapi`?*

El pipeline se pone en rojo. No puede mergear.

**La frase del pizarrón:**

> "Deberíamos mantener la documentación actualizada" es una intención.
> `openapi:check` en CI es una garantía. La diferencia entre las dos es toda la
> ingeniería de software.

### 8.1 El otro sentido: el front deja de escribir `fetch` a mano

```bash
npx openapi-typescript openapi.yaml -o src/api/types.ts
```

```ts
const api = createClient<paths>({ baseUrl: 'http://localhost:3000' });

const { data, error } = await api.GET('/v1/books', {
  params: { query: { page: 1, sort: '-year' } }
});
// data está tipado como BookPage; 'sort: "pasword"' NO COMPILA.
```

Mostrar ese comentario final y dejarlo un segundo en silencio. El typo en el nombre de
un parámetro de query, que antes se descubría en runtime y con suerte, ahora es un error
de compilación. Eso lo retomamos cuando el front consuma esta API.

---

## 9. Tests de contrato

Nos falta la última pata. El documento se genera del código, bien. Pero nada verifica
todavía que la **respuesta real** cumpla el documento.

> Un test de contrato no verifica *qué* devuelve el endpoint, sino que lo que devuelve
> **cumple el documento**.

```ts
import Ajv from 'ajv/dist/2020.js';       // ← Draft 2020-12, el de OpenAPI 3.1
```

Ese import con `/dist/2020.js` es el que les va a hacer perder veinte minutos si lo
ponen mal: OpenAPI 3.1 usa JSON Schema Draft 2020-12, y el Ajv por defecto valida
Draft-07.

```ts
it('la respuesta de GET /v1/books cumple el contrato', async () => {
  const res = await request(makeApp()).get('/v1/books');
  expectMatchesSchema(res.body, 'BookPage');
});
```

### 9.1 El test que realmente encuentra bugs

Los tests de arriba verifican que la respuesta **tenga** lo que promete. Falta el
inverso, y es el importante:

```ts
it('no filtra campos no declarados en el contrato', async () => {
  const res = await request(makeApp()).post('/v1/books')
    .send({ title: 'X', author: 'Y', year: 2020 });

  const declarados = ['id', 'title', 'author', 'year'];
  expect(Object.keys(res.body.data).sort()).toEqual(declarados.sort());
});
```

*Pregunta: ¿qué bug atrapa este test que los otros no?*

El día que alguien agregue `internalNotes`, `passwordHash` o `_rawRow` al objeto que se
serializa, este test falla. Los otros tres no, porque el campo de más no viola ningún
`required`.

**Y la parte que los va a convencer:** cuando `Book` venga de una base de datos y se
devuelva la fila tal como vino, este va a ser el test más valioso del archivo. Hoy
parece paranoia; en dos unidades es lo único que separa la API de filtrar una columna
que nunca debió salir.

---

## 10. Evolución del documento

Cerramos con el ciclo de vida, que es corto pero hay que decirlo.

| Cambio | `info.version` | Prefijo de URL |
|---|---|---|
| Agregar un endpoint | `1.0.0` → `1.1.0` | `/v1` |
| Agregar un campo opcional | `1.0.0` → `1.1.0` | `/v1` |
| Corregir una descripción | `1.0.0` → `1.0.1` | `/v1` |
| Quitar o renombrar un campo | `1.x` → `2.0.0` | `/v2` |

Y como el documento está en el repo, un cambio incompatible se puede detectar **antes**
de mergear:

```bash
docker run --rm -v "$PWD:/w" tufin/oasdiff breaking /w/base.yaml /w/openapi.yaml
```

En CI, ese paso falla si aparece un cambio *breaking* sin bump de major. Es el hermano
de `openapi:check`: uno verifica que el documento esté al día, el otro que el cambio no
rompa a nadie.

---

## 11. Cierre

Lo que se llevan de hoy, en una línea:

> El contrato dejó de vivir en nuestra cabeza. Vive en un archivo, se genera del código
> que ya teníamos, se navega en el browser, y hay dos pasos de CI que impiden que mienta.

Y la pregunta para la clase que viene, también sin contestar:

> Resolvimos **describir** nuestra API. Pero el front de la pantalla de detalle sigue
> haciendo trece requests en cascada para pintar una página, y la de inicio se baja dos
> kilobytes de sinopsis para mostrar dos líneas de texto.
> Documentar eso mejor no lo arregla. ¿Y si el cliente pudiera pedir exactamente los
> campos que necesita, en una sola request?

Eso es [GraphQL](u02_graphql.md).

---

## 12. Comandos de la demo

```bash
# 1. Generar el documento desde los schemas de Zod
npm run openapi

# 2. Levantar y abrir la documentación ejecutable
npm run dev
#    → http://localhost:3000/docs
#    → http://localhost:3000/openapi.json

# 3. El documento crudo, para que vean que es un archivo y nada más
curl -s localhost:3000/openapi.json | jq '.paths | keys'
curl -s localhost:3000/openapi.json | jq '.components.schemas | keys'

# 4. La demo de openapi:check — agregar un campo al schema de Zod y NO regenerar
npm run openapi:check        # ← falla, y eso es el punto

# 5. Tests de contrato
npx vitest run tests/contract

# 6. Generar el cliente tipado del front
npx openapi-typescript openapi.yaml -o src/api/types.ts

# 7. Breaking changes contra la base
docker run --rm -v "$PWD:/w" tufin/oasdiff breaking /w/base.yaml /w/openapi.yaml
```
