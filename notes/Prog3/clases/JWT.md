# JWT en APIs con Express, TypeScript y Sequelize

## 1. Objetivo del apunte

En este apunte vamos a estudiar cómo implementar autenticación basada en **JWT** en una API desarrollada con:

* **Node.js**
* **Express**
* **TypeScript**
* **Sequelize**
* **Base de datos SQL**: MySQL, MariaDB, PostgreSQL o SQLite

El objetivo principal es construir una API donde:

1. Un usuario pueda registrarse.
2. Un usuario pueda iniciar sesión.
3. El servidor genere un token JWT.
4. El cliente use ese token para acceder a rutas protegidas.
5. El backend valide el token antes de permitir el acceso.

Este apunte está pensado para alumnos que ya conocen los conceptos básicos de APIs REST con Express.

---

## 2. ¿Qué problema resuelve JWT?

Cuando un usuario inicia sesión en una aplicación, el servidor necesita alguna forma de recordar que ese usuario ya fue autenticado.

Por ejemplo:

```text
1. El usuario envía email y contraseña.
2. El servidor verifica si los datos son correctos.
3. Si son correctos, el usuario queda autenticado.
4. Luego el usuario quiere consultar sus datos privados.
```

El problema es que HTTP es un protocolo **sin estado**. Esto significa que cada petición es independiente de las demás.

Por ejemplo:

```http
GET /perfil
```

Por sí sola, esa petición no le dice al servidor quién es el usuario.

Para resolver esto, se suele usar alguno de estos mecanismos:

* Sesiones en el servidor.
* Cookies de sesión.
* Tokens.
* JWT.

En este apunte vamos a trabajar con **JWT**, que es una forma muy usada de autenticar usuarios en APIs.

---

## 3. ¿Qué es JWT?

JWT significa **JSON Web Token**.

Un JWT es un texto largo que representa información firmada digitalmente por el servidor.

Ejemplo de token JWT:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhbmFAZXhhbXBsZS5jb20iLCJpYXQiOjE3MTUwMDAwMDAsImV4cCI6MTcxNTAwMzYwMH0.qWz8RZKz2W5V8nD4Ue4mnz3zvX9nFks9GtLx7zYwabc
```

Un JWT tiene tres partes separadas por puntos:

```text
HEADER.PAYLOAD.SIGNATURE
```

Por ejemplo:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
.
eyJpZCI6MSwiZW1haWwiOiJhbmFAZXhhbXBsZS5jb20iLCJpYXQiOjE3MTUwMDAwMDAsImV4cCI6MTcxNTAwMzYwMH0
.
qWz8RZKz2W5V8nD4Ue4mnz3zvX9nFks9GtLx7zYwabc
```

---

## 4. Partes de un JWT

### 4.1. Header

El **header** indica el tipo de token y el algoritmo usado para firmarlo.

Ejemplo:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

* `alg`: algoritmo de firma.
* `typ`: tipo de token.

---

### 4.2. Payload

El **payload** contiene los datos que queremos guardar dentro del token.

Ejemplo:

```json
{
  "id": 1,
  "email": "ana@example.com",
  "iat": 1715000000,
  "exp": 1715003600
}
```

Algunos campos comunes son:

* `id`: identificador del usuario.
* `email`: correo del usuario.
* `iat`: fecha de creación del token.
* `exp`: fecha de expiración del token.

Importante: el payload **no está cifrado**. Está codificado en Base64, pero puede ser leído fácilmente.

Por eso, dentro de un JWT no se debe guardar información sensible como:

* Contraseñas.
* Datos bancarios.
* Tokens de otras plataformas.
* Información privada innecesaria.

---

### 4.3. Signature

La **firma** permite verificar que el token no fue modificado.

El servidor firma el token usando una clave secreta.

Ejemplo conceptual:

```text
firma = algoritmo(header + payload + clave_secreta)
```

Si alguien modifica el payload, la firma deja de ser válida.

Por eso, aunque el contenido del token pueda leerse, no se puede modificar sin conocer la clave secreta del servidor.

---

## 5. Flujo de autenticación con JWT

El flujo general es el siguiente:

```text
Cliente                         Servidor
   |                               |
   | POST /auth/login              |
   | email + password              |
   |------------------------------>|
   |                               |
   | Verifica usuario              |
   | Verifica contraseña           |
   | Genera JWT                    |
   |                               |
   | token                         |
   |<------------------------------|
   |                               |
   | GET /users/me                 |
   | Authorization: Bearer token   |
   |------------------------------>|
   |                               |
   | Verifica JWT                  |
   | Permite acceso                |
   |                               |
```

Resumen:

1. El usuario inicia sesión.
2. El servidor verifica las credenciales.
3. El servidor genera un JWT.
4. El cliente guarda el token.
5. En cada petición protegida, el cliente envía el token.
6. El servidor valida el token.
7. Si el token es válido, permite acceder al recurso.

---

## 6. ¿Dónde se envía el JWT?

Normalmente el cliente envía el JWT en el encabezado `Authorization`.

Ejemplo:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

La palabra `Bearer` significa que el cliente está presentando un token de acceso.

En Express, este header se puede leer así:

```ts
const authHeader = req.headers.authorization;
```

---

## 7. Estructura del proyecto

Vamos a usar una estructura simple:

```text
src/
├── app.ts
├── server.ts
├── config/
│   └── database.ts
├── models/
│   └── User.ts
├── routes/
│   ├── auth.routes.ts
│   └── user.routes.ts
├── controllers/
│   ├── auth.controller.ts
│   └── user.controller.ts
├── middlewares/
│   └── auth.middleware.ts
└── types/
    └── express.d.ts
```

---

## 8. Instalación del proyecto

Crear el proyecto:

```bash
mkdir jwt-typescript-api
cd jwt-typescript-api
npm init -y
```

Instalar dependencias principales:

```bash
npm install express sequelize mysql2 bcrypt jsonwebtoken dotenv
```

Instalar dependencias de desarrollo:

```bash
npm install -D typescript ts-node-dev @types/node @types/express @types/bcrypt @types/jsonwebtoken
```

Inicializar TypeScript:

```bash
npx tsc --init
```

---

## 9. Configuración de TypeScript

Archivo `tsconfig.json` sugerido:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "rootDir": "src",
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"]
}
```

Nota: para este ejemplo usamos `CommonJS` para simplificar la ejecución con Express y TypeScript. En un proyecto con módulos ES se puede configurar de otra manera, pero requiere ajustar las extensiones de importación.

---

## 10. Scripts de NPM

En `package.json` agregar:

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js"
  }
}
```

Ejecutar el proyecto en desarrollo:

```bash
npm run dev
```

---

## 11. Variables de entorno

Crear un archivo `.env`:

```env
PORT=3000
DB_NAME=jwt_demo
DB_USER=root
DB_PASSWORD=123456
DB_HOST=localhost
JWT_SECRET=clave_super_secreta_para_firmar_tokens
JWT_EXPIRES_IN=1h
```

La variable más importante para JWT es:

```env
JWT_SECRET=clave_super_secreta_para_firmar_tokens
```

Esta clave debe mantenerse privada. No debe subirse a GitHub.

---

## 12. Configuración de Sequelize

Archivo `src/config/database.ts`:

```ts
import { Sequelize } from "sequelize";
import dotenv from "dotenv";

dotenv.config();

export const sequelize = new Sequelize(
  process.env.DB_NAME as string,
  process.env.DB_USER as string,
  process.env.DB_PASSWORD as string,
  {
    host: process.env.DB_HOST,
    dialect: "mysql",
    logging: false,
  }
);
```

Si se usa PostgreSQL, el dialecto sería:

```ts
dialect: "postgres"
```

Si se usa SQLite, la configuración cambia bastante y se usa un archivo local.

---

## 13. Modelo User con Sequelize

Archivo `src/models/User.ts`:

```ts
import { DataTypes, Model, Optional } from "sequelize";
import { sequelize } from "../config/database";

interface UserAttributes {
  id: number;
  name: string;
  email: string;
  password: string;
}

type UserCreationAttributes = Optional<UserAttributes, "id">;

export class User
  extends Model<UserAttributes, UserCreationAttributes>
  implements UserAttributes
{
  public id!: number;
  public name!: string;
  public email!: string;
  public password!: string;
}

User.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    password: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  },
  {
    sequelize,
    tableName: "users",
    timestamps: true,
  }
);
```

La tabla `users` tendrá, como mínimo, estos campos:

| Campo    | Tipo   | Descripción         |
| -------- | ------ | ------------------- |
| id       | number | Identificador único |
| name     | string | Nombre del usuario  |
| email    | string | Correo electrónico  |
| password | string | Contraseña hasheada |

Importante: la contraseña no se debe guardar en texto plano. Se debe guardar usando un hash.

---

## 14. ¿Qué es bcrypt?

`bcrypt` es una librería que permite transformar una contraseña en un hash seguro.

Por ejemplo, si el usuario escribe:

```text
123456
```

En la base de datos no guardamos `123456`, sino algo parecido a esto:

```text
$2b$10$N9qo8uLOickgx2ZMRZo5i.e6KjZzN3q5vR1Vh6n0WjqLq7fVxLf8K
```

Ese hash no debería poder convertirse fácilmente de nuevo en la contraseña original.

Para generar un hash:

```ts
const hashedPassword = await bcrypt.hash(password, 10);
```

Para comparar una contraseña con un hash:

```ts
const isValid = await bcrypt.compare(password, user.password);
```

---

## 15. Controlador de autenticación

Archivo `src/controllers/auth.controller.ts`:

```ts
import { Request, Response } from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { User } from "../models/User";

interface JwtPayload {
  id: number;
  email: string;
}

export const register = async (req: Request, res: Response) => {
  try {
    const { name, email, password } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({
        message: "Nombre, email y contraseña son obligatorios",
      });
    }

    const existingUser = await User.findOne({ where: { email } });

    if (existingUser) {
      return res.status(409).json({
        message: "El email ya está registrado",
      });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await User.create({
      name,
      email,
      password: hashedPassword,
    });

    return res.status(201).json({
      message: "Usuario registrado correctamente",
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
      },
    });
  } catch (error) {
    return res.status(500).json({
      message: "Error interno del servidor",
    });
  }
};

export const login = async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        message: "Email y contraseña son obligatorios",
      });
    }

    const user = await User.findOne({ where: { email } });

    if (!user) {
      return res.status(401).json({
        message: "Credenciales inválidas",
      });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      return res.status(401).json({
        message: "Credenciales inválidas",
      });
    }

    const payload: JwtPayload = {
      id: user.id,
      email: user.email,
    };

    const token = jwt.sign(
      payload,
      process.env.JWT_SECRET as string,
      {
        expiresIn: process.env.JWT_EXPIRES_IN || "1h",
      }
    );

    return res.json({
      message: "Login correcto",
      token,
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
      },
    });
  } catch (error) {
    return res.status(500).json({
      message: "Error interno del servidor",
    });
  }
};
```

---

## 16. Rutas de autenticación

Archivo `src/routes/auth.routes.ts`:

```ts
import { Router } from "express";
import { login, register } from "../controllers/auth.controller";

const router = Router();

router.post("/register", register);
router.post("/login", login);

export default router;
```

Estas rutas serán:

```http
POST /auth/register
POST /auth/login
```

---

## 17. Middleware de autenticación

Un middleware es una función que se ejecuta antes del controlador final.

En este caso, el middleware va a:

1. Leer el header `Authorization`.
2. Verificar que exista un token.
3. Validar el token con `jwt.verify`.
4. Guardar los datos del usuario autenticado en `req.user`.
5. Permitir que la petición continúe.

Archivo `src/middlewares/auth.middleware.ts`:

```ts
import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

interface TokenPayload {
  id: number;
  email: string;
}

export const authenticateToken = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    return res.status(401).json({
      message: "Token no enviado",
    });
  }

  const [type, token] = authHeader.split(" ");

  if (type !== "Bearer" || !token) {
    return res.status(401).json({
      message: "Formato de token inválido",
    });
  }

  try {
    const decoded = jwt.verify(
      token,
      process.env.JWT_SECRET as string
    ) as TokenPayload;

    req.user = decoded;

    next();
  } catch (error) {
    return res.status(401).json({
      message: "Token inválido o expirado",
    });
  }
};
```

---

## 18. Extender el tipo Request de Express

El problema es que TypeScript no sabe que agregamos una propiedad `user` al objeto `req`.

Por eso debemos extender el tipo `Request` de Express.

Archivo `src/types/express.d.ts`:

```ts
declare namespace Express {
  export interface Request {
    user?: {
      id: number;
      email: string;
    };
  }
}
```

Esto permite usar:

```ts
req.user
```

sin que TypeScript marque error.

---

## 19. Controlador de usuario autenticado

Archivo `src/controllers/user.controller.ts`:

```ts
import { Request, Response } from "express";
import { User } from "../models/User";

export const getProfile = async (req: Request, res: Response) => {
  try {
    if (!req.user) {
      return res.status(401).json({
        message: "Usuario no autenticado",
      });
    }

    const user = await User.findByPk(req.user.id, {
      attributes: ["id", "name", "email", "createdAt", "updatedAt"],
    });

    if (!user) {
      return res.status(404).json({
        message: "Usuario no encontrado",
      });
    }

    return res.json({
      user,
    });
  } catch (error) {
    return res.status(500).json({
      message: "Error interno del servidor",
    });
  }
};
```

---

## 20. Ruta protegida

Archivo `src/routes/user.routes.ts`:

```ts
import { Router } from "express";
import { authenticateToken } from "../middlewares/auth.middleware";
import { getProfile } from "../controllers/user.controller";

const router = Router();

router.get("/me", authenticateToken, getProfile);

export default router;
```

Esta ruta será:

```http
GET /users/me
```

Pero solo funcionará si el cliente envía un JWT válido.

---

## 21. Configuración principal de Express

Archivo `src/app.ts`:

```ts
import express from "express";
import authRoutes from "./routes/auth.routes";
import userRoutes from "./routes/user.routes";

export const app = express();

app.use(express.json());

app.get("/", (_req, res) => {
  res.json({
    message: "API JWT con Express, TypeScript y Sequelize",
  });
});

app.use("/auth", authRoutes);
app.use("/users", userRoutes);
```

---

## 22. Arranque del servidor

Archivo `src/server.ts`:

```ts
import dotenv from "dotenv";
import { app } from "./app";
import { sequelize } from "./config/database";
import "./models/User";

dotenv.config();

const PORT = process.env.PORT || 3000;

const main = async () => {
  try {
    await sequelize.authenticate();
    console.log("Conexión a la base de datos correcta");

    await sequelize.sync({ alter: true });
    console.log("Modelos sincronizados");

    app.listen(PORT, () => {
      console.log(`Servidor escuchando en http://localhost:${PORT}`);
    });
  } catch (error) {
    console.error("Error al iniciar el servidor", error);
  }
};

main();
```

Nota: `sync({ alter: true })` es útil para ejemplos y desarrollo, pero no es lo más recomendable para producción. En producción se suelen usar migraciones.

---

## 23. Probar la API

### 23.1. Registrar usuario

Petición:

```http
POST http://localhost:3000/auth/register
Content-Type: application/json
```

Body:

```json
{
  "name": "Ana Pérez",
  "email": "ana@example.com",
  "password": "123456"
}
```

Respuesta esperada:

```json
{
  "message": "Usuario registrado correctamente",
  "user": {
    "id": 1,
    "name": "Ana Pérez",
    "email": "ana@example.com"
  }
}
```

---

### 23.2. Iniciar sesión

Petición:

```http
POST http://localhost:3000/auth/login
Content-Type: application/json
```

Body:

```json
{
  "email": "ana@example.com",
  "password": "123456"
}
```

Respuesta esperada:

```json
{
  "message": "Login correcto",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "Ana Pérez",
    "email": "ana@example.com"
  }
}
```

El cliente debe guardar el token recibido.

---

### 23.3. Acceder a una ruta protegida

Petición:

```http
GET http://localhost:3000/users/me
Authorization: Bearer TOKEN_RECIBIDO
```

Ejemplo usando `curl`:

```bash
curl -X GET http://localhost:3000/users/me \
  -H "Authorization: Bearer TOKEN_RECIBIDO"
```

Respuesta esperada:

```json
{
  "user": {
    "id": 1,
    "name": "Ana Pérez",
    "email": "ana@example.com",
    "createdAt": "2026-05-18T12:00:00.000Z",
    "updatedAt": "2026-05-18T12:00:00.000Z"
  }
}
```

---

## 24. ¿Qué pasa si no envío token?

Si se llama a la ruta protegida sin token:

```http
GET /users/me
```

El servidor responderá:

```json
{
  "message": "Token no enviado"
}
```

Código HTTP:

```http
401 Unauthorized
```

---

## 25. ¿Qué pasa si envío un token inválido?

Si el token está mal formado, vencido o fue firmado con otra clave secreta, el servidor responderá:

```json
{
  "message": "Token inválido o expirado"
}
```

Código HTTP:

```http
401 Unauthorized
```

---

## 26. Diferencia entre autenticación y autorización

Aunque a veces se confunden, no significan lo mismo.

### Autenticación

La autenticación responde a la pregunta:

```text
¿Quién es el usuario?
```

Ejemplo:

```text
Este usuario es ana@example.com.
```

### Autorización

La autorización responde a la pregunta:

```text
¿Qué puede hacer este usuario?
```

Ejemplo:

```text
Ana puede consultar su perfil, pero no puede eliminar usuarios.
```

JWT permite autenticar al usuario, pero la autorización se debe implementar con reglas adicionales.

Por ejemplo, se puede agregar un campo `role`:

```json
{
  "id": 1,
  "email": "admin@example.com",
  "role": "admin"
}
```

Luego se pueden proteger rutas según el rol.

---

## 27. Ejemplo de autorización con roles

Supongamos que queremos permitir una ruta solo a administradores.

Primero, el token podría incluir un rol:

```ts
const payload = {
  id: user.id,
  email: user.email,
  role: user.role,
};
```

Luego se puede crear un middleware:

```ts
import { Request, Response, NextFunction } from "express";

export const requireAdmin = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (!req.user) {
    return res.status(401).json({
      message: "Usuario no autenticado",
    });
  }

  if (req.user.role !== "admin") {
    return res.status(403).json({
      message: "No tiene permisos para acceder a este recurso",
    });
  }

  next();
};
```

Para que esto funcione, también habría que agregar `role` al tipo de `req.user`.

---

## 28. Buenas prácticas

### 28.1. No guardar contraseñas en texto plano

Incorrecto:

```ts
password: password
```

Correcto:

```ts
password: await bcrypt.hash(password, 10)
```

---

### 28.2. No guardar datos sensibles en el JWT

Incorrecto:

```json
{
  "id": 1,
  "email": "ana@example.com",
  "password": "123456"
}
```

Correcto:

```json
{
  "id": 1,
  "email": "ana@example.com"
}
```

---

### 28.3. Usar expiración del token

Correcto:

```ts
jwt.sign(payload, secret, { expiresIn: "1h" });
```

Esto evita que un token sea válido indefinidamente.

---

### 28.4. Guardar la clave secreta en variables de entorno

Incorrecto:

```ts
const secret = "mi_clave";
```

Correcto:

```ts
const secret = process.env.JWT_SECRET as string;
```

---

### 28.5. Usar HTTPS en producción

JWT no cifra la información. Si el token viaja por HTTP, puede ser interceptado.

En producción se debe usar HTTPS.

---

### 28.6. Validar los datos recibidos

En este ejemplo validamos manualmente algunos campos. En proyectos reales conviene usar librerías como:

* Zod
* Joi
* Yup
* express-validator

Por ejemplo, se debería validar:

* Que el email tenga formato válido.
* Que la contraseña tenga longitud mínima.
* Que el nombre no esté vacío.

---

## 29. Errores comunes

### Error 1: `req.user` no existe en TypeScript

Causa: no se extendió correctamente el tipo `Request`.

Solución: crear el archivo:

```text
src/types/express.d.ts
```

con el contenido:

```ts
declare namespace Express {
  export interface Request {
    user?: {
      id: number;
      email: string;
    };
  }
}
```

---

### Error 2: `JWT_SECRET` es undefined

Causa: no se cargó `dotenv` o falta la variable en `.env`.

Solución:

```ts
import dotenv from "dotenv";
dotenv.config();
```

Y revisar el archivo `.env`:

```env
JWT_SECRET=clave_super_secreta_para_firmar_tokens
```

---

### Error 3: `Token inválido o expirado`

Posibles causas:

* El token venció.
* El token fue copiado incompleto.
* Se cambió la clave secreta.
* Se envió sin la palabra `Bearer`.

Formato correcto:

```http
Authorization: Bearer TOKEN
```

---

### Error 4: La contraseña no coincide aunque parece correcta

Posibles causas:

* Se guardó la contraseña sin `bcrypt.hash`.
* Se está comparando mal el hash.
* Se modificó manualmente el campo `password` en la base de datos.

Comparación correcta:

```ts
const isPasswordValid = await bcrypt.compare(password, user.password);
```

---

## 30. Código completo resumido del flujo

Registro:

```text
POST /auth/register
```

El servidor:

```text
1. Recibe name, email, password.
2. Verifica que el email no exista.
3. Hashea la contraseña.
4. Crea el usuario.
5. Devuelve los datos públicos del usuario.
```

Login:

```text
POST /auth/login
```

El servidor:

```text
1. Recibe email y password.
2. Busca el usuario por email.
3. Compara la contraseña usando bcrypt.
4. Genera un JWT.
5. Devuelve el token.
```

Ruta protegida:

```text
GET /users/me
```

El servidor:

```text
1. Lee el header Authorization.
2. Extrae el token.
3. Verifica la firma y expiración.
4. Obtiene el id del usuario desde el token.
5. Busca el usuario en la base de datos.
6. Devuelve el perfil.
```

---

## 31. Actividad práctica propuesta

### Consigna

Crear una API con Express, TypeScript y Sequelize que permita:

1. Registrar usuarios.
2. Iniciar sesión.
3. Obtener el perfil del usuario autenticado.
4. Crear una ruta protegida `/private` que solo responda si el usuario tiene un JWT válido.

### Requisitos mínimos

El modelo `User` debe tener:

| Campo    | Tipo   | Restricción         |
| -------- | ------ | ------------------- |
| id       | number | primary key         |
| name     | string | obligatorio         |
| email    | string | único y obligatorio |
| password | string | obligatorio         |

La API debe tener las siguientes rutas:

| Método | Ruta             | Protegida | Descripción                 |
| ------ | ---------------- | --------- | --------------------------- |
| POST   | `/auth/register` | No        | Registra un usuario         |
| POST   | `/auth/login`    | No        | Inicia sesión               |
| GET    | `/users/me`      | Sí        | Devuelve el perfil          |
| GET    | `/private`       | Sí        | Devuelve un mensaje privado |

### Ejemplo de respuesta de `/private`

```json
{
  "message": "Accediste a una ruta protegida",
  "user": {
    "id": 1,
    "email": "ana@example.com"
  }
}
```

---

## 32. Preguntas para repasar

1. ¿Por qué HTTP se considera un protocolo sin estado?
2. ¿Qué información conviene guardar dentro de un JWT?
3. ¿Por qué no se debe guardar la contraseña dentro del token?
4. ¿Qué función cumple la firma del JWT?
5. ¿Qué diferencia hay entre `jwt.sign` y `jwt.verify`?
6. ¿Qué significa enviar el token como `Bearer`?
7. ¿Qué pasa si el token está vencido?
8. ¿Por qué se usa `bcrypt` para guardar contraseñas?
9. ¿Cuál es la diferencia entre autenticación y autorización?
10. ¿Por qué es importante usar variables de entorno para la clave secreta?

---

## 33. Desafíos adicionales

### Desafío 1: Agregar roles

Agregar un campo `role` al usuario con dos valores posibles:

```text
user
admin
```

Luego crear una ruta:

```http
GET /admin/dashboard
```

que solo pueda ser accedida por usuarios con rol `admin`.

---

### Desafío 2: Cambiar contraseña

Crear una ruta protegida:

```http
PUT /users/change-password
```

El usuario debe enviar:

```json
{
  "oldPassword": "123456",
  "newPassword": "abcdef"
}
```

El servidor debe:

1. Verificar que el usuario esté autenticado.
2. Buscar al usuario por `req.user.id`.
3. Comparar `oldPassword` con la contraseña actual.
4. Hashear `newPassword`.
5. Guardar la nueva contraseña.

---

### Desafío 3: Logout conceptual

Con JWT, el logout no siempre elimina el token del servidor, porque el servidor no guarda sesión.

Investigar y explicar distintas formas de manejar logout:

* Borrar el token del cliente.
* Usar tokens de corta duración.
* Usar una lista negra de tokens.
* Usar refresh tokens.

---

## 34. Conclusión

JWT es una herramienta muy útil para autenticar usuarios en APIs REST.

Sus ideas principales son:

* El servidor genera un token cuando el usuario inicia sesión.
* El cliente envía ese token en cada petición protegida.
* El servidor valida la firma del token.
* Si el token es válido, permite acceder al recurso.

En una API con Express, TypeScript y Sequelize, JWT suele implementarse usando:

* Un modelo `User`.
* Un controlador de autenticación.
* Rutas públicas para registro y login.
* Un middleware para proteger rutas.
* Una clave secreta guardada en variables de entorno.

El punto más importante es entender que JWT no reemplaza todas las medidas de seguridad. Debe combinarse con buenas prácticas como contraseñas hasheadas, expiración de tokens, validación de datos y HTTPS en producción.
