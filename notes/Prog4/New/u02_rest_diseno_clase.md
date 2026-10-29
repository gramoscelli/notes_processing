# Guion de clase — Diseño de APIs REST: recursos, contrato y colecciones

> Notas para dictar la clase. Siguen el orden real de exposición, con lo que se dice,
> lo que va en pantalla y las preguntas que se lanzan.
> Apunte del alumno: [Diseño de APIs REST](u02_rest_diseno.md).

---

## 1. Apertura: el middleware que miente

**En pantalla**, el código que ellos mismos escribieron en Testing Parte 4:

```ts
export function errorHandler(err: unknown, _req: Request, res: Response, _next: NextFunction) {
  const message = err instanceof Error ? err.message : 'UnexpectedError';
  const status = /not found/i.test(message) ? 404 : 400;
  res.status(status).json({ error: message });
}
```

Esto es lo que tenemos hoy y funciona: los tests pasan. Pero miren cómo decide el
status code. Lo decide leyendo el **texto** del mensaje de error y buscando ahí adentro
la frase "not found", en inglés, con una expresión regular.

*Pregunta: ¿qué pasa si mañana alguien carga un libro titulado "Not Found"?*

**Demo:**

```bash
curl -i -X POST localhost:3000/books -H 'content-type: application/json' \
  -d '{"title":"Not Found","author":"X","year":1990}'
```

Y hay algo peor. Si la base de datos se cae, el error dice "connection refused". No
contiene "not found", así que cae en el `else`: devuelve **400**. Le estamos diciendo
al cliente "lo que mandaste está mal" cuando el que se rompió fue el servidor. El
front va a mostrar un cartel de error de validación por una caída nuestra.

**La frase que queda en el pizarrón toda la clase:**

> El status code no se decide con una expresión regular sobre un mensaje.
> Se decide con el **tipo** del error. Y el formato de la respuesta es uno solo para
> toda la API.

Eso es un **contrato**, y es de lo que se trata esta clase.

---

## 2. De endpoints que funcionan a una API con contrato

Lo que tenemos hoy son funciones accesibles por HTTP:

```ts
router.post('/', (req, res) => { /* crea un libro */ });
router.get('/',  (req, res) => { /* lista libros  */ });
```

Eso no es todavía una API. La diferencia es la **promesa estable** que le hacemos a
quien consume. Comparen las dos columnas:

| Sin contrato | Con contrato |
|---|---|
| "Devuelve un array" | `200` con `{ data, meta }`, `data` es un array de `Book` |
| "Si falla tira 500" | `400` validación, `404` inexistente, `409` conflicto, `422` regla de negocio |
| "Agregamos un campo y listo" | Agregar es compatible; renombrar o quitar es breaking |
| El front descubre la forma probando | El front lee el contrato y programa contra él |

La columna izquierda es la que obliga al front a abrir el Postman para averiguar qué
devuelve cada endpoint. La derecha es la que le permite escribir el cliente antes de
que el back exista.

Un contrato se apoya en cuatro decisiones, y son las cuatro de hoy:

```text
Recursos y URLs → Métodos y semántica → Estados y errores → Colecciones y evolución
```

**Regla de oro:** el contrato es lo primero que se diseña y lo último que se cambia.

---

## 3. Recursos, no acciones

REST modela **sustantivos**, no **verbos**. El verbo ya lo pone HTTP. Cuando uno pone
el verbo también en la URL, lo está diciendo dos veces y mal.

**En el pizarrón, para que lo traduzcan ellos:**

```text
POST /crearLibro
POST /borrarLibro?id=7
GET  /obtenerLibrosDelAutor?autor=Borges
POST /actualizarAñoDelLibro
```

Son cuatro URLs distintas para un mismo recurso. El método HTTP no significa nada
—todo es `POST`—, nada de esto es cacheable y nada es predecible: para saber cómo
borrar hay que leer la documentación.

```text
POST   /books
DELETE /books/7
GET    /books?author=Borges
PATCH  /books/7
```

*Pregunta: ¿cuántas URLs distintas necesita un CRUD completo de libros?*

Dos. **`/books` y `/books/{id}`.** Toda API REST se arma repitiendo esos dos patrones:
la colección y el ítem. Cuatro operaciones, dos URLs.

### 3.1 Anidamiento

Se anida cuando hay pertenencia real:

```text
/books/{id}/reviews        → las reseñas de un libro
/books/{id}/reviews/{rid}  → una reseña concreta
```

Pero esto es un error de diseño:

```text
/authors/3/books/7/reviews/12/comments/4
```

*Pregunta: ¿dónde lo cortarían?*

El criterio: **anidá sólo si el hijo no tiene sentido fuera del padre**. Una reseña sin
libro no significa nada, se anida. Un comentario ya tiene id propio global, así que se
expone de primer nivel y se filtra:

```text
/comments/4
/comments?reviewId=12
```

Más de dos niveles de anidamiento es casi siempre señal de que estamos modelando la
navegación de la pantalla en lugar de los recursos.

### 3.2 Convenciones que se fijan de entrada

* **Plural** para colecciones: `/books`, no `/book`.
* **kebab-case** si hay más de una palabra: `/reading-lists`.
* **Sin extensión ni verbo**: nada de `/books.json` ni `/getBooks`.
* **Sin barra final**.
* **Ids opacos**: quien consume no debe asumir que son numéricos ni correlativos.

Son arbitrarias, cualquiera de las dos opciones sirve. Lo que no sirve es tener las dos
en la misma API.

### 3.3 La excepción honesta

A veces hay una operación que realmente no es un CRUD: publicar un borrador, reenviar
un mail, recalcular un índice. Forzarla a ser un recurso produce diseños peores que
admitir la excepción:

```text
POST /books/7/publish
POST /books/7/restore
```

Está aceptado por convención. Es legítimo **si es la excepción**. Si la mitad de la API
son acciones, el modelo de recursos está mal planteado y conviene rehacerlo.

---

## 4. Métodos: seguridad e idempotencia

Dos propiedades definen la semántica de cada método:

* **Seguro:** no modifica estado. Se puede ejecutar mil veces sin consecuencias.
* **Idempotente:** ejecutarlo N veces deja el mismo estado final que ejecutarlo una vez.

| Método | Seguro | Idempotente | Uso en `/books` |
|---|:--:|:--:|---|
| `GET` | ✅ | ✅ | leer colección o ítem |
| `POST` | ❌ | ❌ | crear (el servidor asigna el id) |
| `PUT` | ❌ | ✅ | reemplazo completo |
| `PATCH` | ❌ | ❌* | modificación parcial |
| `DELETE` | ❌ | ✅ | eliminar |

**El ejemplo que hace entender para qué sirve la palabra.** El usuario está en el
subte, manda el request, se corta la señal justo después. El cliente no sabe si llegó
y reintenta.

*Pregunta: ¿qué pasa si eso era un `POST /books`? ¿Y si era un `PUT /books/7`?*

Con `POST` quedan dos libros. Con `PUT` queda uno. Por eso importa: los proxies, las
CDN y los navegadores **reintentan solos** los métodos idempotentes ante un timeout.
No es teoría de examen, es el motivo por el que un `PUT` que crea sin id provisto por
el cliente duplica registros en producción.

Dos aclaraciones que siempre hacen falta:

* Idempotente **no** es "devuelve lo mismo". Es que el **estado final del servidor** es
  el mismo. `DELETE /books/7` dos veces es idempotente aunque la segunda dé `404`.
* `PATCH` es idempotente *si* el parche es absoluto (`{"year": 1994}`). No lo es si es
  relativo (`{"incrementStock": 1}`).

### 4.1 `PUT` vs `PATCH`

```ts
// PUT /books/7 → el body es el libro COMPLETO. Lo que falta, se borra.
{ "title": "Rayuela", "author": "Cortázar", "year": 1963 }

// PATCH /books/7 → el body son SÓLO los campos a cambiar.
{ "year": 1963 }
```

El error clásico es implementar `PUT` como si fuera `PATCH`: mergear en lugar de
reemplazar. Queda una API donde es **imposible borrar un campo opcional**, y eso se
descubre en producción, con un cliente que no puede limpiar un dato.

Recomendación práctica, discutible y vale discutirla: **expongan `PATCH` y no expongan
`PUT`**. Es menos frágil frente a clientes desactualizados y evita el merge accidental.

---

## 5. Estados y errores

### 5.1 Qué código devolver

No hace falta memorizar la tabla, hace falta razonar el caso. **Van dictando y ellos
contestan:**

| Caso | Respuesta |
|---|---|
| Se creó el libro | `201` + header `Location` |
| Se borró el libro | `204`, sin cuerpo |
| `{"year": "mil"}` | `400` |
| `{"year": 2097}` | `422` |
| ISBN repetido | `409` |
| `GET /books/999` | `404` |
| Se cayó la base | `500` |

El par que hay que dejar clavado:

> **`400` = no entiendo lo que me mandaste. `422` = te entiendo perfectamente, pero no
> puedo aceptarlo.**

`{"year": "mil"}` no es un número: no lo entiendo, `400`. `{"year": 2097}` es un número
perfectamente válido, lo entiendo, pero un libro no puede ser del futuro: `422`.

Y esto no es decorativo, le sirve concretamente al front: **ante un `400` hay un bug en
el cliente** —mandó algo mal formado, el usuario no puede arreglarlo—; **ante un `422`
hay un mensaje para mostrarle al usuario**.

Aclaración honesta: hay equipos serios que usan `400` para todo y no están violando la
especificación. Nosotros distinguimos porque el front necesita saber si muestra un
cartel o reporta un bug.

### 5.2 Un solo formato de error

Nada hace más difícil consumir una API que tener tres formatos de error distintos
según qué parte del código falló. Usamos **RFC 9457, `application/problem+json`** —un
estándar, no un invento de la cátedra:

```ts
// src/http/problem.ts
export type Problem = {
  type: string;      // URI que identifica el tipo de error
  title: string;     // resumen legible, estable
  status: number;    // el mismo status HTTP
  detail?: string;   // explicación de ESTA ocurrencia
  instance?: string; // la URL que falló
  errors?: Record<string, string[]>; // detalle por campo
};
```

Un error de validación se ve así. Fíjense en `errors`: es lo que le permite al front
pintar de rojo el campo exacto del formulario.

```json
{
  "type": "https://api.utn.edu.ar/errors/validation",
  "title": "La solicitud no pasó la validación",
  "status": 400,
  "detail": "Revisá los campos indicados en 'errors'.",
  "instance": "/v1/books",
  "errors": { "year": ["Expected number, received string"] }
}
```

### 5.3 El middleware centralizado

> **Las rutas lanzan, el middleware traduce. Ninguna ruta arma un error a mano.**

Es la misma separación que ya hicimos entre dominio y transporte: el service no sabe
de HTTP, tira un error de negocio, y hay un solo lugar que decide cómo se ve eso en la
respuesta.

Primero los errores tipados —acá está el reemplazo de la expresión regular del
principio:

```ts
// src/http/errors.ts
export class AppError extends Error {
  constructor(
    public status: number,
    public type: string,
    public title: string,
    public detail?: string,
    public errors?: Record<string, string[]>
  ) { super(title); }
}

export const notFound = (what: string, id: string) =>
  new AppError(404, 'https://api.utn.edu.ar/errors/not-found',
    `${what} no encontrado`, `No existe ${what} con id ${id}.`);

export const businessRule = (detail: string) =>
  new AppError(422, 'https://api.utn.edu.ar/errors/business-rule',
    'Regla de negocio violada', detail);

export const conflict = (detail: string) =>
  new AppError(409, 'https://api.utn.edu.ar/errors/conflict',
    'Conflicto con el estado actual', detail);
```

Y el traductor, con tres ramas y nada más:

```ts
// src/http/errorHandler.ts
export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  if (err instanceof ZodError) {
    return res.status(400).type('application/problem+json').json({
      type: 'https://api.utn.edu.ar/errors/validation',
      title: 'La solicitud no pasó la validación',
      status: 400,
      instance: req.originalUrl,
      errors: err.flatten().fieldErrors
    });
  }

  if (err instanceof AppError) {
    return res.status(err.status).type('application/problem+json').json({
      type: err.type, title: err.title, status: err.status,
      detail: err.detail, instance: req.originalUrl, errors: err.errors
    });
  }

  console.error(err);                       // adentro, completo
  return res.status(500).type('application/problem+json').json({
    type: 'about:blank', title: 'Error interno',
    status: 500, instance: req.originalUrl  // afuera, genérico
  });
};
```

Tres cosas mientras se escribe:

1. **La tercera rama nunca filtra el stack.** El log va adentro; la respuesta es
   genérica. Un stack trace le regala al atacante la estructura de carpetas, las
   versiones de las librerías y las rutas internas. Volvemos a esto en Unidad 7.
2. **Se registra último**, después de todas las rutas. Si va antes, no se ejecuta nunca:

```ts
app.use('/v1/books', makeBooksRouter(service));
app.use(errorHandler); // ← siempre último
```

3. **Cuidado con `async` en Express 4.** Un `throw` dentro de un handler `async` no
   llega acá: el request queda colgado hasta el timeout. Hay que capturar y llamar
   `next(err)`, o usar un wrapper. En Express 5 ya se propaga solo.

### 5.4 El contrato es un test

```ts
it('404 con problem+json cuando el libro no existe', async () => {
  const res = await request(makeApp()).get('/v1/books/no-existe');

  expect(res.status).toBe(404);
  expect(res.headers['content-type']).toMatch(/application\/problem\+json/);
  expect(res.body).toMatchObject({ status: 404, title: expect.any(String) });
});

it('422 cuando el year es futuro (regla de negocio, no sintaxis)', async () => {
  const res = await request(makeApp()).post('/v1/books')
    .send({ title: 'X', author: 'Y', year: new Date().getFullYear() + 5 });
  expect(res.status).toBe(422);
});
```

> El contrato no es documentación: es un test. Si nadie verifica el `content-type` del
> error, el contrato se rompe y no se entera nadie hasta que lo reporta el front.

---

## 6. Colecciones

```bash
curl -s localhost:3000/v1/books | wc -c
```

Con tres libros, unos cientos de bytes. *Pregunta: ¿cuánto da con cuarenta mil?*

Un `GET /books` que devuelve todo es una bomba de tiempo: anda perfecto en la demo y
tira el servidor en producción. **Toda colección se pagina desde el día uno**, aunque
hoy tenga tres registros, porque agregar paginación después es un cambio breaking.

### 6.1 Offset o cursor

| | Offset / página | Cursor / keyset |
|---|---|---|
| URL | `?page=3&pageSize=20` | `?cursor=abc&limit=20` |
| Saltar a la página N | ✅ directo | ❌ sólo siguiente/anterior |
| Costo en la base | crece con el offset | constante |
| Si los datos cambian mientras paginás | ❌ repite o saltea ítems | ✅ estable |
| Cuándo | back-office, tablas con paginador | feeds, scroll infinito |

Nosotros usamos **offset**, que es lo que espera una tabla con paginador. En Unidad 4,
contra una base real, vamos a ver por qué se degrada.

### 6.2 Validar la query con Zod

Los query params **siempre** llegan como string. Convertirlos a mano en cada ruta es la
fuente número uno de bugs de paginación.

```ts
export const listBooksQuery = z.object({
  page:     z.coerce.number().int().positive().default(1),
  pageSize: z.coerce.number().int().positive().max(100).default(20),
  sort:     z.enum(['title', 'year', 'author', '-title', '-year', '-author'])
              .default('title'),
  author:   z.string().min(1).optional(),
  yearFrom: z.coerce.number().int().optional(),
  yearTo:   z.coerce.number().int().optional(),
  q:        z.string().min(1).optional()
}).refine(
  v => v.yearFrom == null || v.yearTo == null || v.yearFrom <= v.yearTo,
  { message: 'yearFrom no puede ser mayor que yearTo', path: ['yearFrom'] }
);
```

Hay tres decisiones deliberadas ahí, y las tres importan:

**`z.coerce`** hace el casteo de string a número en un solo lugar. Nunca más un
`Number(req.query.page)` suelto en una ruta.

**`.max(100)` en `pageSize`.** *Pregunta: ¿qué pasa si alguien pide `?pageSize=999999`?*
Sin el tope, le estamos dando a cualquiera una forma trivial de tirarnos la API. Un
límite sin tope no es un límite.

**`z.enum` en `sort`, no `z.string()`.** Hoy, con datos en memoria, un `sort` libre
sólo es feo. En Unidad 4, contra una base de datos, un campo de orden que viene del
cliente es una vía de inyección y de full scan. La whitelist se define **ahora**,
cuando no cuesta nada.

La convención de orden: un solo parámetro, `-` para descendente, coma para multi-campo.

```text
?sort=title        → título ascendente
?sort=-year        → año descendente
?sort=-year,title  → año descendente y, a igual año, título ascendente
```

### 6.3 El sobre de respuesta

Si devolvemos un array pelado no hay dónde poner los metadatos de paginación. Por eso
el sobre:

```ts
export type Page<T> = {
  data: T[];
  meta:  { page: number; pageSize: number; total: number; totalPages: number };
  links: { self: string; first: string; prev: string | null;
           next: string | null; last: string };
};
```

Los `links` son el dato más útil para el front: no tiene que saber armar la URL de la
página siguiente, la sigue. Y cuando `next` es `null`, se terminó.

**Coherencia:** si la colección devuelve `{ data, meta }`, el ítem individual también
devuelve `{ data }`. Una API donde `GET /books` y `GET /books/7` tienen formas
distintas obliga al front a escribir dos deserializadores.

### 6.4 El test que vale por diez

```ts
const years = res.body.data.map((b: any) => b.year);
expect(years).toEqual([...years].sort((a, b) => b - a));
```

Pará acá. Este test **no hardcodea el resultado esperado**: verifica la *propiedad*
"está ordenado descendente". Sigue pasando cuando cambian los datos de prueba, y falla
exactamente cuando el orden se rompe. Es el patrón que quiero ver en el TP.

---

## 7. Versionado

Toda API que se usa, cambia. La pregunta no es *si* vas a romper el contrato, sino
*cómo* lo vas a administrar.

**Juego rápido: digo el cambio, ustedes dicen si rompe o no.**

| Cambio | ¿Breaking? |
|---|:--:|
| Agregar un campo opcional a la respuesta | No |
| Agregar un endpoint nuevo | No |
| Agregar un query param con default | No |
| Quitar o renombrar un campo | **Sí** |
| Cambiar el tipo de un campo | **Sí** |
| Agregar un campo requerido al request | **Sí** |
| Cambiar un status code | **Sí** |
| Endurecer una validación | **Sí** |

> **Agregar es seguro; quitar y cambiar, no.** Y los clientes viejos siguen existiendo
> aunque hayas avisado.

La versión va **en la URL y sólo major**: `/v1/books`. Es visible, cacheable, trivial
de rutear y de probar con `curl`. No existe `/v1.2`, porque los cambios menores son
compatibles por definición.

Y no se apaga una versión de un día para el otro. El procedimiento: publicar `/v2`,
marcar `/v1` como deprecada con los headers estándar `Deprecation` y `Sunset`, medir
cuánto tráfico sigue entrando por `/v1`, y recién ahí apagarla.

```ts
res.set('Deprecation', 'true');
res.set('Sunset', 'Sat, 01 Aug 2026 00:00:00 GMT');
res.set('Link', '</v2/books>; rel="successor-version"');
```

---

## 8. HATEOAS, en cinco minutos

La idea: la respuesta no trae sólo datos, trae **qué se puede hacer ahora** con esos
datos.

```json
{
  "data": { "id": "7", "title": "Rayuela", "status": "draft" },
  "links": {
    "self":    { "href": "/v1/books/7", "method": "GET" },
    "publish": { "href": "/v1/books/7/publish", "method": "POST" }
  }
}
```

Lo interesante es lo que **no** aparece: si el libro ya estuviera publicado, el link
`publish` no vendría. El servidor comunica su máquina de estados y el front **no tiene
que reimplementar** la regla "el botón Publicar se muestra sólo si está en borrador".

Dicho esto, HATEOAS completo casi nadie lo implementa: requiere un cliente que descubra
links en runtime, infla las respuestas y cada API inventa su propio formato.

**Posición del curso:** adoptamos la hipermedia útil —los links de paginación que ya
hicimos, y los links de acción condicionados por estado— y no la ortodoxia.

Si preguntan si entonces nuestra API no es REST: en el modelo de Richardson estamos en
**nivel 2** (recursos + verbos + status codes), que es lo que la industria llama REST.
El nivel 3 es la hipermedia. Nuestra API queda en nivel 2 con los links de paginación
del 3, y eso está bien.

---

## 9. Cierre

Los errores que vamos a ver una y otra vez, y que están todos en el apunte:

* `200 OK` con `{"error": "..."}` adentro — rompe `res.ok`, los reintentos y el monitoreo.
* Un `GET` que modifica estado — un prefetch del navegador ejecuta la acción.
* Listado sin paginación.
* `sort` como string libre.
* `float` para plata — `0.1 + 0.2 !== 0.3`. Enteros en centavos.
* Fechas con formato propio — ISO 8601 UTC siempre.
* `null` y campo ausente usados indistintamente: en `PATCH`, `null` es "ponelo en nada"
  y ausente es "no lo toques".

Y la pregunta con la que nos vamos, **sin contestarla**:

> Todo este contrato que acabamos de diseñar, ¿dónde está escrito? En nuestra cabeza y
> en los tests. ¿Cómo hace el front para saber que `meta.totalPages` existe, sin
> preguntarnos por WhatsApp?

Eso es la clase que viene: [OpenAPI](u02_openapi.md).

---

## 10. Comandos de la demo

```bash
# Apertura: el título que rompe el middleware viejo
curl -i -X POST localhost:3000/books -H 'content-type: application/json' \
  -d '{"title":"Not Found","author":"X","year":1990}'

# 404 con problem+json
curl -i localhost:3000/v1/books/no-existe

# 400: sintaxis mal
curl -i -X POST localhost:3000/v1/books -H 'content-type: application/json' \
  -d '{"title":"X","author":"Y","year":"mil novecientos"}'

# 422: sintaxis bien, regla de negocio violada
curl -i -X POST localhost:3000/v1/books -H 'content-type: application/json' \
  -d '{"title":"X","author":"Y","year":2097}'

# 201 + Location
curl -i -X POST localhost:3000/v1/books -H 'content-type: application/json' \
  -d '{"title":"Rayuela","author":"Cortázar","year":1963}'

# El sobre completo
curl -s localhost:3000/v1/books | jq '{meta, links}'

# El tope de pageSize y la whitelist de sort
curl -i 'localhost:3000/v1/books?pageSize=999999'
curl -i 'localhost:3000/v1/books?sort=password'

# Headers de deprecación
curl -sI localhost:3000/v1/books | grep -iE 'deprecation|sunset|link'
```
