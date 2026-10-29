# 🚀 Apunte: Deployment de Aplicaciones Web (Docker, Nginx, SSL, CI/CD, Cloud)
## 1) ¿Qué es Deployment?

Desplegar (*deploy*) es el proceso de mover una aplicación desde la
etapa de desarrollo hasta un entorno donde los usuarios puedan
utilizarla. Involucra: 

- Configurar servidores 
- Publicar servicios 
- Asegurar escalabilidad, seguridad y monitoreo


## 2) Tipos de Servicios

Aquí tienes un **apunte corto y claro**, separado específicamente sobre los **tipos de servicios en la nube**:



### ☁️ **Tipos de Servicios en la Nube (Cloud Service Models)**

Los servicios cloud se clasifican según **qué nivel de control y responsabilidad tiene el usuario vs el proveedor**.



### 1️⃣ **IaaS – Infrastructure as a Service**

**(Infraestructura como Servicio)**

El proveedor da **servidores, almacenamiento y redes**.
Vos administrás el sistema operativo, aplicaciones y configuración.

| Administra el proveedor                  | Administra el usuario                                        |
| ---------------------------------------- | ------------------------------------------------------------ |
| Servidores, red, storage, virtualización | SO, actualizaciones, apps, bases de datos, seguridad interna |

✅ Control total
✅ Ideal para instalar Docker, bases de datos, etc
❌ Requiere conocimientos de administración de servidores

**Ejemplos:**

* AWS EC2
* Google Compute Engine
* Azure Virtual Machines
* DigitalOcean Droplets
* Hetzner VPS


### 2️⃣ **PaaS – Platform as a Service**

**(Plataforma como Servicio)**

El proveedor da **todo el entorno listo para desplegar apps**.
No te ocupás del sistema operativo ni del servidor.

| Administra el proveedor               | Administra el usuario        |
| ------------------------------------- | ---------------------------- |
| SO, red, runtime, escalado, seguridad | Código, configuración, datos |

✅ Muy fácil desplegar apps
✅ CI/CD y escalado a veces automaticos
❌ Menos control técnico, puede ser caro

**Ejemplos:**

* Heroku
* Render
* Railway
* Google App Engine
* Azure App Service


### 3️⃣ **SaaS – Software as a Service**

**(Software como Servicio)**

Es software listo para usar desde el navegador.
No se programa ni se administra infraestructura.

| Todo lo administra el proveedor        |
| -------------------------------------- |
| Servidores, red, app, datos, seguridad |

✅ No requiere conocimientos técnicos
❌ No permite modificar la infraestructura

**Ejemplos:**

* Gmail
* Google Drive
* Notion
* Slack
* Microsoft 365

### 4️⃣ **CaaS – Containers as a Service**

**(Contenedores como Servicio)**

Plataformas específicas para desplegar **Docker/Kubernetes** sin administrar servidores directamente.

| Proveedor maneja              | Usuario maneja             |
| ----------------------------- | -------------------------- |
| Orquestación, nodos, escalado | Imágenes Docker, servicios |

✅ Ideal si trabajás con contenedores
✅ Escala fácil
❌ Puede ser complejo si usa Kubernetes

**Ejemplos:**

* AWS ECS / EKS
* Google GKE
* Azure AKS
* Docker Swarm (Cloud providers lo ofrecen como servicio)
* Railway / Render (bajo el capó usan contenedores)


### 5️⃣ **FaaS – Function as a Service (Serverless)**

**(Funciones como Servicio)**

No hay servidor, solo subís funciones que se ejecutan cuando se llaman.

| Proveedor maneja                | Usuario maneja      |
| ------------------------------- | ------------------- |
| Servidores, escalado, ejecución | Código de funciones |

✅ Se paga solo por uso
✅ Escala automáticamente
❌ No ideal para apps tradicionales largas o con estado

**Ejemplos:**

* AWS Lambda
* Google Cloud Functions
* Azure Functions
* Cloudflare Workers


### 6️⃣ **BaaS – Backend as a Service**

**(Backend listo para usar)**

Servicios ya listos como autenticación, base de datos, storage, notificaciones.

✅ No hay que programar backend desde cero
❌ Dependencia del proveedor

**Ejemplos:**

* Firebase
* Supabase
* Appwrite

### Resumen rápido

| Tipo     | Te da                             | Vos controlás            |
| -------- | --------------------------------- | ------------------------ |
| **IaaS** | Servidores virtuales              | SO, apps, deploy         |
| **PaaS** | Plataforma lista para apps        | Código y datos           |
| **SaaS** | Software listo                    | Uso del software         |
| **CaaS** | Contenedores listos para correr   | Contenedores y servicios |
| **FaaS** | Funciones serverless              | Lógica de funciones      |
| **BaaS** | Backend listo (auth, DB, storage) | Uso y lógica de negocio  |


## 3) Modalidades de Infraestructura

| Tipo | Descripción | Ventajas | Desventajas |
|---|---|---|---|
| **Máquina virtual (VM)** | Servidores virtuales (EC2, Azure VM, DigitalOcean Droplet) | Control total, usar Docker | Administrar el sistema, parches, etc |
| **Infraestructura como Servicio (IaaS)** | Servidores bajo demanda | Flexibilidad, escalabilidad | Costos variables, requiere experiencia |
| **Plataforma como Servicio (PaaS)** | No gestionas servidores (Heroku, Railway, Render) | Deploy rápido | Menos control, costos altos a escala |
| **Serverless** | Sin servidores, se paga por uso (Cloudflare Workers, AWS Lambda) | Muy escalable, barato | No ideal para apps tradicionales con Docker |
| **Contenedores administrados** | Kubernetes, AWS ECS, Azure ACS | Escalable y moderno | Complejo |


## 4) Proveedores Cloud más usados

| Servicio        | Tipo                        | Soporta Docker      | Observaciones |
|-----------------|----------------------------|-------------------|--------------|
| **AWS**         | IaaS + PaaS                | ✅                | Muy completo, costoso, complejo |
| **Azure**       | IaaS + PaaS                | ✅                | Ideal integración con Microsoft |
| **Google Cloud**| IaaS + PaaS                | ✅                | Muy bueno para IA + datos |
| **Heroku**      | PaaS                       | ⚠ (Buildpacks)    | Fácil, caro a escala |
| **DigitalOcean**| IaaS                       | ✅                | Simple, económico |
| **Railway**     | PaaS                       | ✅                | Ideal estudiantes, rápido |
| **Render**      | PaaS                       | ✅                | Más control que Heroku |
| **Cloudflare**  | Edge (CDN + Seguridad + Serverless) | ⚠ Workers | Muy usado por: CDN, anti-DDoS, caché, tunnels |

### ¿Por qué se usa tanto Cloudflare?

✅ CDN global (el sitio carga rápido desde cualquier país)

✅ Protección contra ataques (DDoS, bots, WAF)

✅ Certificados SSL gratis

✅ Cache y optimización automática

✅ *Cloudflare Tunnels*: exponer tu PC/servidor sin abrir puertos


## 4) Entornos de despliegue

| Entorno        | Para qué se usa |
|---------------|-----------------|
| **Development** | Programar y probar |
| **Staging**     | Igual a producción, para pruebas finales |
| **Production**  | Acceso de usuarios reales |



## 5) Usar dominio en desarrollo local

### Editar `hosts`

📍 **Windows**

    C:\Windows\System32\drivers\etc\hosts

📍 **Linux / macOS**

    /etc/hosts

Agregar:

```
    127.0.0.1    miapp.local
    127.0.0.1    api.miapp.local
```


## 6) Usar NGINX como proxy reverso en Docker

### `docker-compose.yml`

```yaml
services:
  backend:
    build: ./backend
    expose:
      - 3000
    networks: [web]

  frontend:
    build: ./frontend
    expose:
      - 80
    networks: [web]

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    networks: [web]

  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c"
    command: "sleep 12h"
    networks: [web]

networks:
  web:

```


## 7) Configurar NGINX para proxy + SSL

Archivo `nginx/nginx.conf`:

```nginx
events {}

http {
    server {
        listen 80;
        server_name miapp.com www.miapp.com;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name miapp.com;

        ssl_certificate /etc/letsencrypt/live/miapp.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/miapp.com/privkey.pem;

        location / {
            proxy_pass http://frontend:80;
        }

        location /api/ {
            proxy_pass http://backend:3000/;
        }
    }
}
```
.
## 8) Generar certificados con Let's Encrypt

```bash

docker compose up -d
docker compose run --rm certbot certonly   --webroot --webroot-path=/var/www/certbot   -d miapp.com -d www.miapp.com   --email mail@ejemplo.com --agree-tos --no-eff-email
docker compose restart nginx

```

## 9) HTTPS en local con `mkcert`

Instalar y generar:

```bash
mkcert -install
mkcert miapp.local api.miapp.local
```

Colocar los `.pem` en `./certs` y montar en docker-compose.


## 🔄 10) CI/CD — Automatización del despliegue

### 🧩 ¿Qué significa CI/CD?

| Sigla  | Significa                                                          | Objetivo                                                                                       |
| ------ | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **CI** | *Continuous Integration* (Integración Continua)                    | Evitar que el código nuevo rompa el proyecto. Se prueba y valida automáticamente.              |
| **CD** | *Continuous Delivery / Deployment* (Entrega o Despliegue Continuo) | Publicar automáticamente los cambios validados a un servidor o entorno (staging o producción). |

### 🧠 Idea clave en pocas palabras

> **Cada vez que subo cambios al repositorio, el sistema los prueba y los despliega automáticamente sin intervención manual.**

Esto evita:

❌ subir código roto
❌ olvidarse de ejecutar pasos del deploy
❌ errores humanos
❌ tiempo perdido haciendo deploys manuales

Y permite:

✅ deploys rápidos y frecuentes
✅ procesos repetibles y automáticos
✅ menos bugs en producción
✅ equipos trabajando sin pisarse

### 🏭 Flujo típico de CI/CD

```
(1) Programador sube código a GitHub / GitLab
        ↓
(2) CI ejecuta pruebas automáticas (test, lint, build)
        ↓
(3) Si pasa → CD despliega en servidor (con Docker)
        ↓
(4) Aplicación actualizada sin tocar el servidor manualmente
```


### 💡 ¿Qué se automatiza habitualmente?

| Tarea                                           | Se puede automatizar con CI/CD |
| ----------------------------------------------- | :----------------------------: |
| Ejecutar tests                                  |                ✅               |
| Verificar errores de sintaxis (lint)            |                ✅               |
| Construir imágenes Docker                       |                ✅               |
| Publicar a un servidor                          |                ✅               |
| Reiniciar servicios                             |                ✅               |
| Notificar éxito o error (Slack, Discord, email) |                ✅               |



### 🧠 ¿Qué es GitHub Actions?
**GitHub Actions es el sistema de automatización de GitHub**.
Permite ejecutar tareas automáticamente cuando ocurre algo en un repositorio.

#### 🧠 Definición simple

> **Es una herramienta que ejecuta procesos automáticos** (llamados *workflows*) cuando haces cosas como:
> `git push`, `git pull request`, crear un tag, etc.

#### 🏭 ¿Para qué sirve?

Automatiza tareas como:

✅ Probar el código (tests)
✅ Revisar errores (lint, formato)
✅ Compilar o construir una app
✅ Crear imágenes Docker
✅ Desplegar en un servidor (deploy)
✅ Enviar notificaciones (Slack, correo, etc)

#### ⏱ ¿Cuándo se ejecuta?

Puede activarse cuando ocurre un evento, por ejemplo:

| Evento              | Se ejecuta cuando...    |
| ------------------- | ----------------------- |
| `push`              | Subís código (git push) |
| `pull_request`      | Alguien abre un PR      |
| `schedule`          | A una hora programada   |
| `workflow_dispatch` | Lo ejecutás manualmente |

#### ⚙ ¿Cómo funciona?

Vos creás un archivo dentro del repositorio en:

```
.github/workflows/archivo.yml
```

Ese archivo describe **qué debe hacer** y **cuándo**.
#### 🔎 Ejemplo mínimo

```yaml
name: Mensaje de prueba
on: push

jobs:
  saludar:
    runs-on: ubuntu-latest
    steps:
      - run: echo "¡Hola! Esto se está ejecutando automáticamente 🚀"
```

Cuando haces `git push`, GitHub:

1. Crea una máquina con Ubuntu
2. Ejecuta el comando `echo`
3. Te muestra el resultado en la pestaña **Actions**

#### 🧩 Componentes clave

| Concepto     | Qué es                                                      |
| ------------ | ----------------------------------------------------------- |
| **Workflow** | Todo el proceso automatizado                                |
| **Job**      | Un conjunto de pasos que se ejecutan en una máquina         |
| **Step**     | Una instrucción individual (comando o acción)               |
| **Runner**   | La computadora que ejecuta el proceso (GitHub provee una)   |
| **Action**   | Una tarea ya hecha por alguien (como `appleboy/ssh-action`) |

#### ✅ Relación con CI/CD

GitHub Actions se usa mucho para **CI/CD**, es decir:

| CI/CD              | Qué hace GitHub Actions                              |
| ------------------ | ---------------------------------------------------- |
| **CI (probar)**    | Ejecuta tests, revisa errores, construye el proyecto |
| **CD (desplegar)** | Sube la app al servidor y la actualiza               |


#### 🧠 En palabras simples

> **GitHub Actions es un “robot” que trabaja para vos cada vez que subís código.**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
```

➡️ Crea un **trabajo llamado `deploy`** y lo ejecuta en una máquina de GitHub con **Linux Ubuntu**.

```yaml
steps:
  - name: Conectar al servidor y ejecutar deploy
    uses: appleboy/ssh-action@master
```

➡️ Utiliza una acción ya creada (`appleboy/ssh-action`) que sirve para **conectarse por SSH a un servidor remoto**.

```yaml
with:
  host: ${{ secrets.SERVER_IP }}
  username: ${{ secrets.SERVER_USER }}
  key: ${{ secrets.SSH_KEY }}
```

➡️ Usa credenciales guardadas en GitHub (`Secrets`) para conectarse:

| Secret        | Qué contiene                             |
| ------------- | ---------------------------------------- |
| `SERVER_IP`   | La IP o dominio del servidor             |
| `SERVER_USER` | El usuario SSH (ej: root, ubuntu, admin) |
| `SSH_KEY`     | La clave privada SSH para autenticarse   |

Estas credenciales **NO están en el código**, son seguras.

```yaml
script: |
  cd /var/www/miapp
  git pull
  docker compose down
  docker compose up -d --build
```

➡️ Una vez conectado al servidor, ejecuta estos comandos **como si los escribieras vos a mano por SSH**:

| Comando                        | Qué hace                                                   |
| ------------------------------ | ---------------------------------------------------------- |
| `cd /var/www/miapp`            | Entra a la carpeta donde está tu proyecto en el servidor   |
| `git pull`                     | Descarga los últimos cambios del repositorio               |
| `docker compose down`          | Apaga la versión de la app que está corriendo              |
| `docker compose up -d --build` | Re-construye y levanta la app actualizada en segundo plano |

### ✅ En resumen simple:

Cada vez que se ejecuta este job:

1. Se conecta a tu servidor remoto por SSH
2. Actualiza el código del proyecto (`git pull`)
3. Apaga los contenedores
4. Los vuelve a construir y levantar con la nueva versión


### 🔧 Ejemplo práctico: CI/CD con GitHub Actions + Docker

📌 Archivo: `.github/workflows/deploy.yml`

```yaml
name: Deploy automático

on:
  push:
    branches:
      - main   # se activa cuando hay push en main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Conectar al servidor y ejecutar deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/miapp
            git pull
            docker compose down
            docker compose up -d --build
```


### 🔐 ¿Qué son los `secrets`?

Son variables seguras (no visibles en el repositorio) donde guardamos secretos como:

* IP del servidor
* Usuario SSH
* Claves privadas
* Tokens
* Passwords

📍 En GitHub se cargan en:

```
Settings → Secrets → Actions
```

Y se usan así:

```yaml
${{ secrets.NOMBRE_DEL_SECRETO }}
```

Nunca deben ir en el código ni en commits ❗


### 🐳 ¿Por qué funciona bien con Docker?

Porque el deploy se vuelve **idéntico en cualquier servidor**, solo ejecuta:

```bash
docker compose up -d --build
```

Ventajas:

✅ No importa si el server es Ubuntu, Debian, etc
✅ No hay "en mi máquina funciona"
✅ Todo está versionado: app + entorno + dependencias


### 🧪 CI/CD vs Deploy manual

| Deploy manual                 | CI/CD automatizado               |
| ----------------------------- | -------------------------------- |
| Lento                         | Rápido                           |
| Puede fallar por error humano | Repetible y confiable            |
| Pasos que se olvidan          | Todo documentado y versionado    |
| No hay pruebas antes de subir | Tests automáticos evitan errores |
| Hay que conectarse al server  | Ocurre sin tocar el servidor     |


### 🏁 Conclusión simple

> **CI/CD convierte el deploy en un proceso automático, seguro, repetible y rápido.**
> Cuanto menos manual, mejor.



## 11) Observabilidad (Monitoreo)

| Herramienta  | Función |
|-------------|---------|
| Portainer   | UI para Docker |
| Grafana     | Métricas |
| Uptime Kuma | Status del servicio |
| Dozzle      | Logs |

## 12) Seguridad mínima recomendada

```
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## ✅ Resumen

| Tema                        | Concepto |
|----------------------------|----------|
| Proxy reverso              | Nginx |
| SSL                        | Let's Encrypt o mkcert |
| Director de tráfico global | Cloudflare |
| Automatización             | CI/CD |
| Infraestructura            | VM, IaaS, PaaS, Containers |
