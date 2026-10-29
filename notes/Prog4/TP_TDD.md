# Trabajo Práctico de TDD
**Teoría + Mini‑proyectos (TypeScript/Express/Zod + Jest o Vitest)**

> **Objetivo general.** 
Practicar TDD (Rojo → Verde → Refactor) construyendo una API pequeña con TypeScript + Express, validaciones con Zod y tests **unitarios** + **integración** (Jest **o** Vitest + Supertest). Las **preguntas teóricas** son comunes a todos; cada grupo desarrolla **un mini‑proyecto distinto** de la lista.



## 1) Requisitos técnicos

* Node 18+ y npm.
* TypeScript, Express, Zod.
* Testing: **Jest** (ts‑jest) **o** **Vitest** + **Supertest**.
* ESM recomendado: `"module": "ESNext"`, `"moduleResolution": "NodeNext"` (usar extensión `.js` en imports relativos TS→TS).
* Separar **app** de **server**: `makeApp()` sin `listen` en tests.
* Validación en bordes con Zod (body/query/params). Reglas de negocio en servicios (probadas con unit tests).



## 2) Modalidad y organización

* **Equipos:** 2–3 integrantes. Cada equipo elige **un proyecto distinto** (sin repetidos si es posible).
* **Evidencia de TDD:** commits pequeños que muestren `test rojo → implementación mínima → refactor`.
* **Repositorio público o privado compartido con docentes**.



## 3) Entregables

1. **Código** de la API con tests unitarios + integración en verde.
2. **Historial de commits** mostrando el ciclo TDD por historia (user story).
3. **Cobertura**: ≥ **80%** en archivos modificados.
4. **Matriz de casos** (tabla CA ↔ tests) en README o en el PR.
5. **Guía de ejecución**: scripts npm, requisitos, comandos para correr tests.



## 4) Rúbrica de evaluación (100 pts)

* **TDD aplicado (30 pts):** commits atómicos, tests antes del código, refactors sin romper tests.
* **Calidad de tests (25 pts):** casos felices y de error; claridad; ausencia de mocks innecesarios; nombres descriptivos.
* **Diseño/validación (20 pts):** Zod en bordes; reglas de dominio en servicios; inyección de dependencias; manejo de errores consistente.
* **Cobertura (10 pts):** umbrales cumplidos y cobertura significativa.
* **Documentación/entrega (10 pts):** README con matriz de casos, ejemplos `curl`, scripts.
* **Buenas prácticas (5 pts):** linter/formatter, estructura limpia.



## 5) Preguntas de teoría (comunes para todos)

Responda en un archivo `TEORIA.md` (máx. 1–2 párrafos por ítem, salvo que se pida código):

1. Explique el ciclo **Rojo → Verde → Refactor** y por qué es importante el tamaño de los pasos.
2. Diferencie **tests unitarios**, **de integración** y **E2E** en APIs.
3. ¿Qué es un **doble de prueba**? Defina **mock**, **stub** y **spy** y cuándo conviene cada uno.
4. ¿Por qué es útil separar `app` de `server`? Muestre (en 8–10 líneas) un ejemplo mínimo con `makeApp()` y un test de integración con Supertest.
5. Zod: diferencia entre `parse` y `safeParse`. ¿Dónde usaría cada uno en una ruta Express y por qué?
6. Dé **dos ejemplos** de **reglas de dominio** que deben probarse con tests unitarios (no sólo validación de entrada).
7. ¿Qué **malos olores** suele haber en suites de tests? Dé 3 ejemplos (naming, duplicación, asserts débiles, mocks frágiles, etc.).
8. ¿Cómo trazará **criterios de aceptación ↔ tests**? Incluya un mini ejemplo de tabla con 2 filas.
9. ¿Por qué no perseguir 100% de cobertura a toda costa? Mencione riesgos/limitaciones.
10. Defina y dé un ejemplo de **helper**/builder para tests.



## 6) Mini‑proyectos (elegir 1 de la lista, todos distintos)

> Para cada proyecto implementar **al menos**: 3–5 endpoints, validaciones con Zod, **tests unitarios** de reglas de negocio y **tests de integración** del contrato HTTP (status/body/errores). Incluya ejemplos `curl` en README.

### P0. Gestor de Tareas

* **Endpoints mínimos:**

  * `POST /tasks` (crear), `GET /tasks?status`, `PATCH /tasks/:id/complete`, `DELETE /tasks/:id`.
* **Reglas de negocio:**

  * `dueDate` no puede ser pasada; un **título no puede repetirse** si la tarea está **pendiente**; cambiar `completedAt` sólo vía `complete`.
* **Validaciones (Zod):** `status ∈ {"todo","doing","done"}`, `title` min 3, `dueDate` ISO.
* **Errores:** 400 por datos inválidos; 404 si `:id` no existe; 409 si título duplicado (pendiente).
* **Extra:** paginación y orden por dueDate.

### P1. Agenda de Contactos

* **Endpoints:** `POST/GET/PUT/DELETE /contacts`, `GET /contacts?query=…`.
* **Reglas:** `email` **único**; `phone` en formato E.164; búsqueda por `query` en nombre/email.
* **Validaciones:** `name` min 2, `email` válido, `phone` regex.
* **Errores:** 409 por email duplicado; 400 por query vacía si se usa.
* **Extra:** favoritos y `GET /contacts/favorites`.

### P2. Pedidos de Pizzería

* **Endpoints:** `POST /orders`, `GET /orders/:id`, `POST /orders/:id/cancel`, `GET /orders?status`.
* **Reglas:** `size ∈ {S,M,L}`, máx. 5 toppings; **precio calculado** (size + toppings); no se puede cancelar si `status = delivered`.
* **Validaciones:** body con `items[]` no vacío; `address` min 10.
* **Errores:** 422 si `items` vacío; 409 si intenta cancelar entregado.
* **Extra:** estimación de entrega en minutos.

### P3. Inventario de Ferretería

* **Endpoints:** `POST /items`, `PATCH /items/:id/adjust` (±stock), `GET /items?lowStock`, `GET /items/:id`.
* **Reglas:** `SKU` único; el stock **no puede quedar < 0**; marcar `lowStock` si `stock ≤ threshold`.
* **Validaciones:** `name` min 2; `threshold ≥ 0`; `delta` entero.
* **Errores:** 409 si `SKU` duplicado; 422 si ajuste deja stock negativo.
* **Extra:** histórico de ajustes.

### P4. Turnos Médicos

* **Endpoints:** `POST /appointments`, `GET /appointments?doctorId&date`, `DELETE /appointments/:id`.
* **Reglas:** turnos de 30′; **no solapar** turnos del mismo médico; no reservar en pasado.
* **Validaciones:** `doctorId`/`patientId` UUID; `dni` formato `\d{7,8}`.
* **Errores:** 409 por solapamiento; 422 por fecha pasada.
* **Extra:** `POST /appointments/:id/reschedule` con mismas reglas.

### P5. Reservas de Cine (simplificado)

* **Endpoints:** `POST /shows`, `GET /shows/:id/seats`, `POST /reservations`.
* **Reglas:** asiento debe estar **disponible**; máx. 8 asientos por reserva.
* **Validaciones:** sala con `rows` y `cols` (1–30); `seats[]` pares `{row,col}` válidos.
* **Errores:** 409 por seat ocupado; 422 por fuera de rango.
* **Extra:** cancelar reserva y liberar asientos.

### P6. Gastos Compartidos

* **Endpoints:** `POST /groups`, `POST /expenses`, `GET /groups/:id/balance`.
* **Reglas:** no repetir miembro; **balances** correctos por persona; `shares` suman 100% (o repartir equitativo si no se envían).
* **Validaciones:** `amount > 0`; `currency ∈ {ARS,USD,EUR}`.
* **Errores:** 400 si `shares` inconsistentes.
* **Extra:** exportar balance simplificado (quién paga a quién).

### P7. Microblogging

* **Endpoints:** `POST /posts`, `GET /posts?authorId`, `POST /posts/:id/like`, `GET /feed`.
* **Reglas:** `content` ≤ 280 chars; **no likear tu propio post**; cada usuario likea una vez.
* **Validaciones:** `authorId` UUID; `content` min 1.
* **Errores:** 409 por like repetido o propio.
* **Extra:** `GET /trending` por likes en ventana de tiempo.

### P8. Mascotas y Vacunas

* **Endpoints:** `POST /pets`, `GET /pets?owner`, `POST /pets/:id/vaccines`.
* **Reglas:** calendario por especie (`dog/cat`); **no booster antes** de la base; microchip `^[A-Z0-9]{10,15}$`.
* **Validaciones:** `species ∈ {dog,cat}`; fechas ISO.
* **Errores:** 409 si se viola orden de vacunas.
* **Extra:** `GET /pets/:id/card` con últimas vacunas.

### P9. Alquiler de Herramientas

* **Endpoints:** `POST /tools`, `POST /rentals`, `POST /rentals/:id/return`, `GET /rentals?status`.
* **Reglas:** **no solapar** alquiler del mismo ítem; depósito calculado; multa por atraso.
* **Validaciones:** rango de fechas válido (`start < end`).
* **Erroros:** 409 si solapa; 422 si rango inválido.
* **Extra:** reporte simple de ingresos por período.

### P10. Cursos e Inscripciones

* **Endpoints:** `POST /courses`, `POST /courses/:id/enroll`, `GET /courses/:id`.
* **Reglas:** **cupo** máximo; no inscribir dos veces al mismo alumno; **cierre** de inscripción por fecha límite.
* **Validaciones:** `capacity ≥ 1`; `studentId` UUID.
* **Erroros:** 409 por cupo completo o doble inscripción; 422 por fuera de fecha.
* **Extra:** `GET /courses/:id/waitlist` con reglas claras.

### P11. Tickets de Soporte

* **Endpoints:** `POST /tickets`, `PATCH /tickets/:id/status`, `GET /tickets?status&priority`.
* **Reglas:** transiciones válidas (p.ej., `open→in_progress→resolved→closed`); no cerrar sin `resolution`.
* **Validaciones:** `priority ∈ {low,medium,high}`; `title` min 5.
* **Erroros:** 409 por transición inválida; 422 por falta de `resolution` al cerrar.
* **Extra:** SLA simple por prioridad.

> **Nota:** todos los proyectos deben exponer al menos **un caso de negocio** que se pruebe con **tests unitarios** (servicio) y uno o más **contratos HTTP** que se prueben con **Supertest** (integración).



## 7) Reglas de TDD para este TP

1. Escribir primero el **test** del caso (unitario) → **rojo**.
2. Implementar **lo mínimo** en el servicio → **verde**.
3. Agregar test **de integración** del endpoint (status, body, errores) → **rojo → verde**.
4. **Refactor** (nombres, helpers, duplicación) manteniendo tests en verde.
5. Repetir por cada historia (user story).



## 8) Formato de entrega

* Link al **repositorio** y breve README con: scripts, instrucciones de ejecución, ejemplos `curl` y **Matriz de casos**.
* Indicar si usan **Jest** o **Vitest** y cómo correr `coverage`.
* Marcar en el README las **user stories** abordadas.



## 9) Plantillas útiles

### 9.1 Scripts npm (Jest)

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watchAll",
    "coverage": "jest --coverage"
  }
}
```

### 9.2 Scripts npm (Vitest)

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "coverage": "vitest run --coverage"
  }
}
```

### 9.3 Matriz de casos (copiar/pegar)

| ID   | Caso / Descripción | Precondición | Input | Acción | Resultado esperado | Test |
|-|-|-|-|-|-|-|
| CA1  |                    |              |       |        |                    |      |
| CA2  |                    |              |       |        |                    |      |
| ERR1 |                    |              |       |        |                    |      |



## 10) Reglas administrativas

* No subir secretos/credenciales.
* Si usan datos persistentes, usar **in‑memory** o un stub/adapter para la DB (no se requiere DB real).
* Cada integración con librerías externas debe aislarse para poder testear.



## 11) Sugerencias para avanzar

* Definir primero **criterios de aceptación** por user story.
* Empezar por la **regla de dominio** más simple → test unitario.
* Subir a la ruta con **validación Zod** y **Supertest**.
* Mantener **nombres** y **mensajes de error** consistentes.
* Usar **helpers** y **builders** de test para reducir duplicación.
