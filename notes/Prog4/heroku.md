# Introducción a Heroku

* **Cuenta Heroku** (no hay plan gratis clásico; existe **Eco** con 1000 horas/mes por **US$5** compartidas entre tus Eco dynos). ([help.heroku.com][1])
* **Heroku CLI** para crear apps, configurar variables y desplegar. ([devcenter.heroku.com][2])
* **Stack** por defecto: **heroku-24** (Ubuntu 24.04). Puedes fijarlo explícitamente. ([devcenter.heroku.com][3])
* **Buildpack de Node.js** (detección automática por `package.json`). ([devcenter.heroku.com][4])
* Guía oficial para **desplegar Node.js** si quieres ampliar. ([devcenter.heroku.com][5])


## 1) Registro e instalación

1. Crea tu cuenta en heroku.com y activa un plan (Eco si quieres algo barato). ([Heroku][6])
2. Instala la **Heroku CLI** (Windows/macOS/Linux).

   ```bash
   # luego de instalar:
   heroku login
   ```

   Se abrirá el navegador para autenticar. ([devcenter.heroku.com][2])


## 2) Estructura mínima del proyecto (monorepo simple)

Supongamos este layout:

```
my-app/
├─ server/              # Express (API + sirve React)
│  ├─ server.js
│  └─ package.json
├─ client/              # React (Vite o CRA)
│  ├─ package.json
│  └─ src/ …
├─ Procfile
└─ package.json         # raíz (scripts de despliegue)
```

### `server/server.js` (ejemplo breve)

```js
const express = require("express");
const path = require("path");
const app = express();

// API de ejemplo
app.get("/api/hello", (_, res) => res.json({ msg: "Hola desde Express" }));

// servir estáticos de React (build)
app.use(express.static(path.join(__dirname, "..", "client", "dist")));
app.get("*", (_, res) =>
  res.sendFile(path.join(__dirname, "..", "client", "dist", "index.html"))
);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Escuchando en ${PORT}`));
```

### `client/package.json` (React con Vite)

```json
{
  "name": "client",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

### `server/package.json` (Express)

```json
{
  "name": "server",
  "private": true,
  "type": "commonjs",
  "engines": { "node": ">=18.x" },
  "main": "server.js",
  "scripts": { "start": "node server.js" },
  "dependencies": { "express": "^4.19.2" }
}
```

### `Procfile` (raíz)

```
web: npm run start --workspace=server
```

### `package.json` (raíz, scripts de build para Heroku)

```json
{
  "name": "my-app",
  "private": true,
  "workspaces": ["client", "server"],
  "scripts": {
    "heroku-prebuild": "npm --prefix client ci || npm --prefix client install",
    "heroku-postbuild": "npm --prefix client run build"
  }
}
```

**Por qué así?**
Heroku detecta Node por `package.json` y usa el buildpack para instalar dependencias y construir. Con `heroku-postbuild` generas el `client/dist` antes de arrancar el servidor, y Express lo sirve como estático. (Buildpacks → transforman tu código en un “slug” listo para correr en el **dyno**). ([devcenter.heroku.com][4])

> Nota: Si prefieres **dos apps** (una para React estático y otra para API), también es válido, pero el monorepo con Express sirviendo React suele ser más simple para empezar.

## 3) Preparar el repo y variables

```bash
git init
git add .
git commit -m "Inicial"
```

Si tu React usa variables (`VITE_API_URL`, etc.), configúralas en Heroku como **config vars** más adelante.

## 4) Crear la app en Heroku y fijar el stack

```bash
heroku create my-app-xyz        # genera un nombre si omites el tuyo
heroku stack:set heroku-24 -a my-app-xyz
```

`heroku-24` es el stack por defecto hoy; dejarlo explícito evita sorpresas. ([devcenter.heroku.com][3])

## 5) Despliegue

```bash
# si usas la rama main:
git push heroku main
# o especificando remoto/app:
git push https://git.heroku.com/my-app-xyz.git main
```

Heroku ejecutará automáticamente la detección de **Node**, instalará dependencias y correrá `heroku-postbuild`, luego arrancará tu `web` del `Procfile`. ([devcenter.heroku.com][5])

Abre la app:

```bash
heroku open -a my-app-xyz
```

Ver logs (útil si algo falla):

```bash
heroku logs --tail -a my-app-xyz
```

## 6) Configuración útil (add-ons, variables, scaling)

* **Variables de entorno**:

```bash
heroku config:set NODE_ENV=production -a my-app-xyz
heroku config:set ANY_API_KEY=xxxx -a my-app-xyz
```
* **Dynos** (plan Eco/Standard, etc.) y escalado:

```bash
heroku ps:scale web=1 -a my-app-xyz
```

  Con **Eco** tus dynos “duermen” sin tráfico y consumen del pool de 1000 horas/mes cuando están activos. ([devcenter.heroku.com][7])
* **Base de datos** (opcional):

```bash
heroku addons:create heroku-postgresql:mini -a my-app-xyz
```

  (el plan **Mini** de Postgres es de pago; revisa precios vigentes). ([help.heroku.com][1])

## 7) Consideraciones de React

* Para CRA o Vite la idea es la misma: construir en `heroku-postbuild` y servir con Express.
* Si recién creaste una app CRA y te falla por stack, hoy el stack actual es **heroku-24**; la solución típica es **servir el build con Express** (como arriba). ([Medium][8])

## 8) Troubleshooting rápido

* **Pantalla vacía / 404**: revisa que Express sirva `client/dist` y tenga el catch-all `*` devolviendo `index.html`.
* **Build no corre**: confirma que el script `heroku-postbuild` está en el `package.json` de **raíz**, y que el `Procfile` existe. ([devcenter.heroku.com][5])
* **Versión de Node**: especifica `"engines"` (ej. `>=18`) para evitar versiones no deseadas. ([devcenter.heroku.com][9])
* **Stack**: valida con `heroku stack -a my-app-xyz`. ([devcenter.heroku.com][10])

## 9) Pasos “copy-paste” (resumen)

```bash
# 1) Login
heroku login

# 2) Repo
git init && git add . && git commit -m "init"

# 3) App + stack
heroku create my-app-xyz
heroku stack:set heroku-24 -a my-app-xyz

# 4) Config opcional
heroku config:set NODE_ENV=production -a my-app-xyz

# 5) Deploy
git push heroku main

# 6) Ver
heroku open -a my-app-xyz
heroku logs --tail -a my-app-xyz
```

[1]: https://help.heroku.com/RSBRUH58/removal-of-heroku-free-product-plans-faq?utm_source=chatgpt.com "Removal of Heroku Free Product Plans FAQ"
[2]: https://devcenter.heroku.com/articles/heroku-cli?utm_source=chatgpt.com "The Heroku CLI"
[3]: https://devcenter.heroku.com/changelog-items/3009?utm_source=chatgpt.com "Heroku-24 is now the default stack for new apps"
[4]: https://devcenter.heroku.com/articles/buildpacks?utm_source=chatgpt.com "Buildpacks"
[5]: https://devcenter.heroku.com/articles/deploying-nodejs?utm_source=chatgpt.com "Deploying Node.js Apps on Heroku"
[6]: https://www.heroku.com/pricing/?utm_source=chatgpt.com "Pricing Built for Every Stage of Your App's Journey"
[7]: https://devcenter.heroku.com/articles/eco-dyno-hours?utm_source=chatgpt.com "Eco Dyno Hours"
[8]: https://medium.com/%40tola.adet/seamlessly-deploy-create-react-app-on-heroku-24-stack-a-complete-guide-849b5d10bac6?utm_source=chatgpt.com "Seamlessly Deploy Create React App on Heroku-24 Stack"
[9]: https://devcenter.heroku.com/articles/nodejs-support?utm_source=chatgpt.com "Heroku Node.js Support Reference"
[10]: https://devcenter.heroku.com/articles/stack?utm_source=chatgpt.com "Stacks"
