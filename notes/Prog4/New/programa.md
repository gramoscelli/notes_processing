# Programación IV — Programa y cobertura de apuntes

Índice de las 10 unidades del programa (`temas.txt`) cruzado con los apuntes
que ya existen en el repositorio. Para cada unidad: los temas del programa, los
apuntes disponibles, el estado de cobertura y qué falta escribir.

**Convenciones de estado:**

| Estado | Significado |
|---|---|
| ✅ Cubierto | Hay material propio y suficiente para dictar la unidad |
| 🟡 Parcial | Hay material, pero faltan temas centrales del programa |
| 🔴 Sin cubrir | No hay apuntes propios sobre la unidad |

**Criterio de cobertura (importante):** sólo cuentan como cobertura los apuntes
de **Programación IV**. El material de `notes/Prog3/` y de las materias de bases
de datos se lista como **prerrequisito o consulta**, no como cobertura: son temas
que se dictan en otras materias y que esta materia asume conocidos. Por eso las
unidades 3 y 5 bajaron de estado respecto de la primera versión de este índice.

## Resumen de cobertura

| Unidad | Tema | Estado | Apuntes |
|---|---|:---:|:---:|
| 1 | Arquitectura y protocolos web avanzados | 🟡 Parcial | 2 |
| 2 | Diseño y documentación de APIs | ✅ Cubierto | 3 |
| 3 | Autenticación y autorización | 🔴 Sin cubrir | 0 |
| 4 | Acceso a datos y persistencia | 🔴 Sin cubrir | 0 |
| 5 | Front End y consumo de APIs | 🟡 Parcial | 5 |
| 6 | Comunicación en tiempo real | 🔴 Sin cubrir | 0 |
| 7 | Integración Front–Back y seguridad | ✅ Cubierto | 10 |
| 8 | Calidad y pruebas | ✅ Cubierto | 14 |
| 9 | Despliegue y CI/CD | 🟡 Parcial | 3 |
| 10 | Observabilidad y operación | 🔴 Sin cubrir | 0 |

Cuatro unidades sin material propio (3, 4, 6 y 10) y tres parciales (1, 5 y 9).
El peso del repositorio está en testing y seguridad. La Unidad 2 pasó a estar
cubierta con los tres apuntes nuevos de `New/`.

### Correspondencia con el curso publicado en Moodle

El aula virtual de *Programación IV (Ramoscelli)* todavía está organizada según
el programa anterior: objetos y TypeScript → Testing (4 partes) → Estilos →
React con TypeScript → Redes y Seguridad → Despliegue → Clases grabadas. De ahí
se deduce qué unidades del programa nuevo no tienen **ninguna** sección en el
aula:

| Unidad | Sección en Moodle |
|---|---|
| 1 | parcial: "Redes y Seguridad" |
| 2 | **ninguna** → la cubren los apuntes nuevos de `New/` |
| 3 | **ninguna** (JWT se dictó en Programación III) |
| 4 | **ninguna** |
| 5 | "React con TypeScript" |
| 6 | **ninguna** |
| 7 | "Redes y Seguridad" |
| 8 | "Testing" (partes 1 a 4) |
| 9 | un solo recurso: "Introducción general al despliegue" |
| 10 | **ninguna** |

El aula no contiene material de Programación III, lo que confirma el criterio de
arriba: esos temas se asumen conocidos y no se vuelven a dictar.

---

## UNIDAD 1: Arquitectura y protocolos web avanzados

**Temas del programa:** Modelo cliente–servidor revisitado. Capas y
responsabilidades. HTTP/1.1 vs HTTP/2 vs HTTP/3 (h/2, QUIC). CORS, políticas de
caché, CDN y compresión.

**Apuntes existentes:**

- [redes.md](../redes.md) — modelo TCP/IP, capas de acceso/internet/transporte/aplicación, NAT y resolución de nombres, herramientas de diagnóstico, redes con Docker, sockets en Python (2026 líneas, 16 secciones)
- [deployment_apunte.md](../deployment_apunte.md) — NGINX como proxy reverso, SSL/TLS, certificados (cubre la parte de infraestructura del modelo cliente–servidor)

**Estado: 🟡 Parcial.** Las capas y el modelo cliente–servidor están bien
servidos por `redes.md`, pero desde la óptica de redes, no de HTTP aplicado.

**Falta escribir:**

- Comparativa HTTP/1.1 vs HTTP/2 vs HTTP/3: multiplexing, head-of-line blocking, server push, QUIC sobre UDP
- Políticas de caché HTTP (`Cache-Control`, `ETag`, revalidación)
- CDN: qué resuelve, cuándo conviene
- Compresión (gzip / brotli) y negociación de contenido
- CORS como protocolo (el preflight está parcialmente en la Unidad 7, ver más abajo)

## UNIDAD 2: Diseño y documentación de APIs

**Temas del programa:** REST (recursos, verbos, códigos), HATEOAS. GraphQL
(tipos, queries, mutations). Especificación y documentación con
OpenAPI/Swagger. Versionado, compatibilidad y deprecaciones. Paginación,
ordenamientos y filtros; convenciones.

**Apuntes de la unidad** (nuevos, en `notes/Prog4/New/`):

1. [u02_rest_diseno.md](u02_rest_diseno.md) — **Diseño de APIs REST**: recursos
   vs acciones, diseño de URIs, métodos seguros e idempotentes, PUT vs PATCH,
   códigos de estado, errores uniformes con `problem+json` (RFC 9457) y
   middleware centralizado, colecciones (paginación offset vs cursor, orden,
   filtros validados con Zod, sobre `{ data, meta, links }`), versionado y
   deprecación (`Deprecation` / `Sunset`), HATEOAS y modelo de madurez de
   Richardson, checklist del contrato.
2. [u02_openapi.md](u02_openapi.md) — **OpenAPI 3.1 y Swagger UI**: anatomía del
   documento, descripción completa de `/v1/books`, componentes reutilizables,
   servir Swagger UI desde Express, **una sola fuente de verdad** generando el
   documento desde los schemas de Zod, generación del cliente tipado, tests de
   contrato con Ajv y detección de cambios incompatibles en CI.
3. [u02_graphql.md](u02_graphql.md) — **GraphQL**: over/under-fetching, esquema
   SDL (tipos, inputs, queries, mutations), resolvers sobre el **mismo**
   `BookService`, montaje en el Express existente, conexiones Relay vs
   `page`/`pageSize`, errores en `extensions` (y el "siempre 200"), N+1 y
   DataLoader, límites de profundidad y costo, comparación honesta REST vs
   GraphQL y cuándo elegir cada uno.

**Hilo conductor:** los tres extienden la **API de libros** de
[guia_tdd_api.md](../guia_tdd_api.md) (en Moodle: *Testing Parte 4*), el mismo
`BookService` y el mismo `makeApp()`. No se introduce un dominio nuevo: se le
agregan capas. Ese mismo servicio es el que recibe autorización en la Unidad 3,
persistencia real en la Unidad 4 y eventos en la Unidad 6.

**Material previo que se apoya:**

- [guia_tdd_api.md](../guia_tdd_api.md) — la API de libros original, con Zod y Supertest
- [testing_api.md](../testing_api.md) — estructura de una API Express para probarla

**Estado: ✅ Cubierto.** Los tres apuntes cubren los cinco temas del programa de
la unidad. Queda pendiente generarlos como sección nueva en el aula virtual.

**Posibles ampliaciones (no bloqueantes):**

- Colecciones Postman/Newman derivadas del documento OpenAPI (se solapa con la Unidad 8)
- Federación de esquemas GraphQL (queda fuera del alcance de la materia)

## UNIDAD 3: Autenticación y autorización

**Temas del programa:** OAuth 2.1/OIDC: authorization code, PKCE, scopes y
claims. JWT: estructura, firmas, expiración y revocación. SSO y federación.
Gestión de sesiones. Roles, permisos y control de acceso. Buenas prácticas de
almacenamiento de credenciales.

**Apuntes existentes en Prog4:** ninguno.

**Prerrequisito que se asume conocido** (dictado en Programación III, *no* cuenta
como cobertura y *no* se vuelve a dictar):

- [Prog3/clases/JWT.md](../../Prog3/clases/JWT.md) — JWT en APIs con Express y TypeScript: estructura, firma, middlewares de autenticación, roles (1440 líneas, 34 secciones)
- [Prog3/proyecto/seguridad.md](../../Prog3/proyecto/seguridad.md) — JWT, CORS y CSRF integrados, implementación en React

**Estado: 🔴 Sin cubrir.** Es coherente con el aula virtual, que no tiene ninguna
sección de autenticación: el JWT se dictó en Programación III. Lo que falta es
exactamente lo que *no* se vio allá: el lado del protocolo delegado.

**Falta escribir** (asumiendo JWT conocido, sin repetirlo):

- OAuth 2.1: flujo authorization code + PKCE, roles del protocolo, scopes
- OpenID Connect: ID token, claims, diferencia con OAuth
- Revocación de tokens y estrategia de refresh tokens
- SSO y federación de identidad
- Autorización como capa sobre la API de la Unidad 2: scopes → permisos → middleware
- Almacenamiento de credenciales: hashing (argon2/bcrypt), secretos, dónde guardar tokens en el cliente

## UNIDAD 4: Acceso a datos y persistencia

**Temas del programa:** Patrón repositorio. ORM (mapeo, migraciones,
relaciones, transacciones). SQL vs NoSQL: selección y trade offs. Caché de
lectura/escritura, invalidación. Integración con motores de búsqueda y colas de
mensajes.

**Apuntes existentes:** ninguno en Prog4.

**Material de otras materias** (consulta o prerrequisito, no cobertura):

- [BdDII/sequalize/sequelize.md](../../BdDII/sequalize/sequelize.md) y [example.md](../../BdDII/sequalize/example.md) — ORM Sequelize: mapeo y relaciones
- [BDI/transacciones.md](../../BDI/transacciones.md) — transacciones
- [BdDII/neo4j_v2/](../../BdDII/neo4j_v2/) y [BdDII/crud/crud_operations.md](../../BdDII/crud/crud_operations.md) — NoSQL (grafos y documentos)
- [Prog3/orm/pymongo.md](../../Prog3/orm/pymongo.md) — MongoDB, aunque desde Python

⚠️ **Decisión pendiente:** qué ORM/estrategia usar para esta unidad. Sequelize ya
se dictó en Programación III (`JWT.md`), así que repetirlo contradice el criterio
de no re-dictar temas de Prog3. Alternativas: Prisma, Drizzle, o un repositorio
a mano sobre `pg` para que el patrón quede explícito antes de taparlo con un ORM.

**Estado: 🔴 Sin cubrir** desde la perspectiva de Programación IV. Hay mucho
material de bases de datos, pero nada sobre la *capa de acceso a datos* de una
aplicación.

**Falta escribir:**

- Patrón repositorio: motivación, interfaz, implementación en TypeScript, testeabilidad
- ORM aplicado: migraciones versionadas, relaciones, transacciones y unit of work
- SQL vs NoSQL: criterios de selección y trade-offs concretos
- Caché de lectura/escritura (write-through, write-behind) e invalidación
- Integración con motores de búsqueda y colas de mensajes

## UNIDAD 5: Front End y consumo de APIs

**Temas del programa:** Consumo seguro (tokens, refresh, renovación). Gestión de
estado (por ejemplo, context/store). Validación de formularios en cliente y
servidor. Enrutamiento, protección de rutas y manejo de errores.

**Apuntes existentes en Prog4** (sección "React con TypeScript" del aula):

- [react_ts.md](../react_ts.md) — migración de React JS a TypeScript
- [React_peliculas.md](../React_peliculas.md) — app completa con búsqueda, detalle y consumo de API (1292 líneas, 25 secciones)
- [React_TS_Gatos.md](../React_TS_Gatos.md) y [React_TS_cat_simple.md](../React_TS_cat_simple.md) — estados entrelazados, consumo de API
- [React_TS_Cat_bootstrap.md](../React_TS_Cat_bootstrap.md) — la misma app con Bootstrap

**Prerrequisito que se asume conocido** (React de Programación III: hooks,
`useContext`/`useReducer`, React Router, `fetch` vs `axios`, localStorage). No
cuenta como cobertura.

**Estado: 🟡 Parcial.** Los apuntes de Prog4 enseñan React **con TypeScript** y
consumo de API, pero los cuatro temas del programa de esta unidad (consumo
seguro, gestión de estado, validación cliente/servidor, rutas protegidas) se
apoyaban en el material de Prog3.

**Falta escribir:**

- Consumo seguro: ciclo de refresh y renovación de tokens, interceptores, cola de reintentos (depende de la Unidad 3)
- Gestión de estado a escala de aplicación, con TypeScript: store tipado, estado de servidor vs estado de UI
- Validación de formularios con **esquema compartido** cliente/servidor (el mismo Zod de la Unidad 2)
- Protección de rutas y manejo global de errores: error boundaries, mapeo de `problem+json` a mensajes de UI
- Cliente generado desde OpenAPI (`openapi-fetch`) como alternativa a escribir `fetch` a mano — ya introducido en [u02_openapi.md](u02_openapi.md)

## UNIDAD 6: Comunicación en tiempo real

**Temas del programa:** WebSockets, SSE y alternativas. Pub/Sub y mensajería.
Diseño de eventos, idempotencia y reintentos. Casos de uso: notificaciones,
tableros en vivo, chat, tracking geográfico.

**Apuntes existentes:** ninguno.

**Material tangencial:**

- [Prog3/clases/observable.md](../../Prog3/clases/observable.md) — Observables en JavaScript: el modelo mental de streams de eventos
- [redes.md](../redes.md) §14 — sockets TCP con Python (la capa de transporte por debajo de WebSockets)

**Estado: 🔴 Sin cubrir.**

**Falta escribir:**

- WebSockets: handshake de upgrade, ciclo de vida, reconexión, `socket.io`
- Server-Sent Events y polling/long-polling como alternativas; cuándo usar cada uno
- Pub/Sub y mensajería: broker, tópicos, colas
- Diseño de eventos: idempotencia, reintentos, entrega at-least-once
- Un caso práctico de los cuatro del programa (chat o tablero en vivo son los más didácticos)

## UNIDAD 7: Integración Front–Back y seguridad

**Temas del programa:** CORS en detalle, CSRF, sanitización de entradas,
validación centralizada, rate limiting, throttling y protección ante fuerza
bruta. Subida de archivos segura.

**Apuntes existentes:**

- [ciberseguridad_guia.md](../ciberseguridad_guia.md) y [ciberseguridad_checklist.md](../ciberseguridad_checklist.md) — guía y checklist
- [ciberseguridad_práctica.md](../ciberseguridad_práctica.md) — prácticas de seguridad en código web para juniors (561 líneas)
- [ciberseguridad_DVWA_practica_0.md](../ciberseguridad_DVWA_practica_0.md) a [practica_4.md](../ciberseguridad_DVWA_practica_4.md) — cinco prácticas sobre DVWA con Docker
- [integrador_juice_shop.md](../integrador_juice_shop.md) y [soluciones_profesor.md](../soluciones_profesor.md) — práctica integradora OWASP Juice Shop
**Prerrequisito que se asume conocido:**
[Prog3/proyecto/seguridad.md](../../Prog3/proyecto/seguridad.md) — CORS y CSRF
con integración en React.

**Estado: ✅ Cubierto** en la parte de vulnerabilidades y práctica ofensiva.

**Falta escribir:**

- Rate limiting, throttling y protección ante fuerza bruta (no aparecen en ningún apunte)
- Límite de profundidad y de costo en GraphQL — pendiente desde [u02_graphql.md](u02_graphql.md) §6.3
- Subida de archivos segura: validación de tipo, tamaño, almacenamiento fuera del webroot
- Validación centralizada como patrón de arquitectura (middleware + esquema único); el middleware de errores de [u02_rest_diseno.md](u02_rest_diseno.md) §3.3 es el punto de partida

⚠️ **`ciberseguridad.md` está vacío (0 líneas).** Decidir si se completa o se
borra; hoy solo agrega ruido al listado.

## UNIDAD 8: Calidad y pruebas

**Temas del programa:** TDD/BDD. Pruebas unitarias e integración en back end y
front end. Pruebas de contrato y de API (Postman/Newman). Pruebas end to end.
Métricas de cobertura. Linters y formateadores.

**Apuntes existentes:**

- [guia_tdd_api.md](../guia_tdd_api.md) y [guia_tdd_api_2.md](../guia_tdd_api_2.md) — TDD para APIs con TypeScript + Express + Jest + Supertest, receta por user story, Zod, Definition of Done
- [React_and_Vitest_TDD.md](../React_and_Vitest_TDD.md), [_v2](../React_and_Vitest_TDD_v2.md), [_v3](../React_and_Vitest_TDD_v3.md) — TDD con React + Vite + Vitest
- [React_TDD_Integration.md](../React_TDD_Integration.md) y [_v2](../React_TDD_Integration_v2.md) — tests de integración con Vitest y React Testing Library
- [testing_c.md](../testing_c.md) — fundamentos de testing en TypeScript + Express
- [testing_a.md](../testing_a.md) — Vitest: empezando y mockeando
- [testing_b.md](../testing_b.md) — generar y ejecutar tests en TypeScript
- [testing_E2E.md](../testing_E2E.md) — tests end-to-end en APIs con Node/TypeScript
- [testing_api.md](../testing_api.md) — testing de API por capas
- [testing.md](../testing.md) y [testing2.md](../testing2.md) — notas sueltas
- [TP_TDD.md](../TP_TDD.md) y [TP3.md](../TP3.md) — trabajos prácticos (TDD + RTL + MSW)

**Estado: ✅ Cubierto,** con amplitud. Es el tema más trabajado del
repositorio.

**Falta escribir:**

- BDD explícito: Gherkin, Given/When/Then, Cucumber (hoy solo hay TDD)
- Pruebas de contrato y colecciones Postman/Newman en CI
- Métricas de cobertura: configuración, umbrales, cómo leerlas sin fetichizarlas
- Linters y formateadores: ESLint + Prettier, integración con el editor y con CI

## UNIDAD 9: Despliegue y CI/CD

**Temas del programa:** Empaquetado con Docker. Variables de entorno y
secretos. Promoción de ambientes (dev, test, prod). Migraciones de base de
datos. Monitoreo básico de salud. Estrategias de despliegue.

**Apuntes existentes:**

- [deployment_apunte.md](../deployment_apunte.md) — Docker, NGINX, SSL, CI/CD, cloud, entornos de despliegue, observabilidad básica (650 líneas, 14 secciones)
- [heroku.md](../heroku.md) — despliegue en Heroku paso a paso, variables, add-ons, scaling
- [ciberseguridad_DVWA_practica_0.md](../ciberseguridad_DVWA_practica_0.md) — Docker aplicado a levantar un entorno

**Estado: 🟡 Parcial.** `deployment_apunte.md` toca casi todos los temas, pero
en algunos casos de forma superficial.

**Falta escribir:**

- Dockerfile en profundidad: multi-stage builds, capas, imágenes mínimas, `docker-compose` para dev
- Gestión de secretos (no solo variables de entorno): vaults, secretos en CI
- Promoción de ambientes dev → test → prod como flujo, con gates
- Migraciones de base de datos en el pipeline de despliegue
- Estrategias de despliegue: blue-green, canary, rolling, feature flags
- Health checks y readiness/liveness probes

## UNIDAD 10: Observabilidad y operación

**Temas del programa:** Logging estructurado, trazas distribuidas y métricas.
Alertas. Diagnóstico de performance (latencia, throughput, uso de CPU/RAM/I/O).
Buenas prácticas de mantenimiento.

**Apuntes existentes:**

- [deployment_apunte.md](../deployment_apunte.md) §11 "Observabilidad (Monitoreo)" — es lo único que existe, una sección dentro de otro apunte
- [redes.md](../redes.md) §12 "Diagnóstico y herramientas de red" — diagnóstico, pero a nivel red

**Estado: 🔴 Sin cubrir** como unidad propia.

**Falta escribir:**

- Logging estructurado: niveles, formato JSON, correlación por request id, qué no loguear
- Trazas distribuidas: spans, contexto, OpenTelemetry
- Métricas: los cuatro signos de oro (latencia, tráfico, errores, saturación), histogramas vs contadores
- Alertas: umbrales, ruido, alertar sobre síntomas y no sobre causas
- Diagnóstico de performance: medir latencia y throughput, perfilar CPU/RAM/I/O
- Buenas prácticas de mantenimiento

---

## Material fuera del programa nuevo

Estos apuntes no corresponden a ninguna de las 10 unidades. Son temas del
programa anterior o prerrequisitos que conviene conservar como material de
consulta o de nivelación:

| Apunte | Tema |
|---|---|
| [apuntes_typescript_parte_1.md](../apuntes_typescript_parte_1.md) … [parte_4](../apuntes_typescript_parte_4.md), [parte_n](../apuntes_typescript_parte_n.md) | TypeScript: 5 apuntes, ~4000 líneas |
| [typescript_cronograma.md](../typescript_cronograma.md) | Programa del curso de TypeScript |
| [objetos.md](../objetos.md), [objetos2.md](../objetos2.md), [objetos3.md](../objetos3.md) | Programación orientada a objetos (~3100 líneas) |
| [bootstrap.md](../bootstrap.md), [bootstrap2.md](../bootstrap2.md), [bootstrap2_v2.md](../bootstrap2_v2.md), [React_TS_Cat_bootstrap.md](../React_TS_Cat_bootstrap.md) | Bootstrap y clases utilitarias |
| [lenguajes_proprocesador.md](../lenguajes_proprocesador.md) | Preprocesadores CSS |
| [commonjs_vs_esm.md](../commonjs_vs_esm.md) | Módulos en TypeScript con Vite |
| [enunciado_ej1_t1.md](../enunciado_ej1_t1.md), [_t2](../enunciado_ej1_t2.md), [_t3](../enunciado_ej1_t3.md), [examen.md](../examen.md), [recu/](../recu/) | Parciales y recuperatorios |
| [React_button_solution.md](../React_button_solution.md), [ejemplo_clases_1.md](../ejemplo_clases_1.md) | Resoluciones puntuales de clase |

TypeScript y POO siguen siendo prerrequisitos implícitos de las unidades 2 a 5,
aunque el programa nuevo ya no los liste.

## Duplicados a consolidar

Varios apuntes existen en múltiples versiones sin que esté marcado cuál es la
vigente:

| Familia | Archivos | Comentario |
|---|---|---|
| TDD con Vitest | `React_and_Vitest_TDD.md`, `_v2`, `_v3` | `_v2` es el más extenso (717 líneas, 14 secciones); `_v3` el más corto (403) |
| Tests de integración | `React_TDD_Integration.md`, `_v2` | `_v2` casi duplica al original |
| TDD para APIs | `guia_tdd_api.md`, `guia_tdd_api_2.md` | 806 y 760 líneas, mismo título |
| Bootstrap parte 2 | `bootstrap2.md`, `bootstrap2_v2.md` | `_v2` es "deep dive" |
| Testing sueltos | `testing.md`, `testing2.md`, `testing_a/b/c.md` | Sin h1 ni títulos claros en los dos primeros |

Conviene elegir una versión canónica por familia antes de sumar los apuntes
nuevos de las unidades 3, 4, 6 y 10.

## Prioridad sugerida

1. ~~**Unidad 2 (APIs)**~~ — ✅ hecha: tres apuntes en `New/`
2. **Unidad 4 (persistencia)** — el siguiente eslabón del hilo conductor: sacarle el array en memoria al `BookService`. Requiere decidir el ORM (ver la advertencia de la Unidad 4)
3. **Unidad 3 (auth)** — se monta sobre la API de la Unidad 2 y habilita el "consumo seguro" de la Unidad 5
4. **Unidad 6 (tiempo real)** — autocontenido; el caso natural es notificar cambios de la API de libros
5. **Unidad 10 (observabilidad)** — autocontenido y corto
6. **Completar unidades 1, 5 y 9** con los temas faltantes listados en cada sección

El hilo conductor queda así: la **API de libros** nace en la Unidad 8 (TDD),
recibe contrato y documentación en la **2**, autorización en la **3**,
persistencia en la **4**, eventos en la **6**, consumo desde el front en la
**5**, despliegue en la **9** e instrumentación en la **10**.

> Los enlaces de este índice son rutas relativas entre archivos `.md`, pensadas
> para navegar el repositorio desde el editor. En el HTML generado por el
> pipeline no resuelven, porque la salida queda un nivel más abajo
> (`New/html_output/`).
