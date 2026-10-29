# Guía DVWA con Docker

## Prerrequisitos

* Docker y Docker Compose (v2) instalados.
* Clonar/descargar la carpeta con el `docker-compose.yml`.
* Puertos libres (el `phpMyAdmin` usa **8081**; DVWA suele estar en **80/8080/8082**, confirmalo con `docker compose ps`).

---

## 1) Levantar los servicios

En la carpeta del `docker-compose.yml`:

**Linux / macOS / WSL**

```bash
docker compose pull          # opcional: baja las imágenes
docker compose up -d         # levanta en segundo plano
docker compose ps            # ver puertos y estado
```

**Windows PowerShell**

```powershell
docker compose pull
docker compose up -d
docker compose ps
```

> **Confirmar puertos:**
>
> * Abrí `docker compose ps` y mirá la columna **Ports** del servicio `dvwa`.
> * Navegá a `http://localhost:<PUERTO_DVWA>` (ej.: `http://localhost:8080`).
> * **phpMyAdmin:** `http://localhost:8081` (usuario `root`, pass `rootpass`; o usuario `dvwa`, pass `dvwapass`).

---

## 2) Inicialización de DVWA (Setup web)

1. Entrá a DVWA en `http://localhost:<PUERTO_DVWA>`.
2. Usuario/clave por defecto: `admin` / `password` (si no cambió).
3. Ir a **DVWA Security → PHP Info** (opcional, diagnóstico) y **Setup**:

   * Clic en **Create / Reset Database**.
   * Si falla, revisá que `db` esté **healthy** y las credenciales del compose:

     * `MYSQL_DATABASE= dvwa`
     * `MYSQL_USER= dvwa`
     * `MYSQL_PASSWORD= dvwapass`
   * Podés ver logs con `docker compose logs -f dvwa` o `docker compose logs -f db`.
4. (Opcional) Ajustar **DVWA Security** a **Low** (para prácticas intro), y habilitar `allow_url_include` según ejercicios.

---

## 3) ¿Dónde está el código de DVWA dentro del contenedor?

En **Apache/PHP** suele estar en:

```
/var/www/html
```

Ahí vas a ver carpetas como:

* `vulnerabilities/` (cada módulo vulnerable),
* `config/` (incluye `config.inc.php`),
* `includes/`, `external/`, etc.

---

## 4) Tres maneras de **modificar el código fuente**

### Opción A (recomendada): **Bind mount** con `docker-compose.override.yml`

Así editan en su **host** con su IDE (VS Code, etc.) y el contenedor lo toma en caliente. No tocás el `compose` original: agregás un override.

**Pasos:**

1. **Copiar** el código actual desde el contenedor al host (para tener la base del código):

   ```bash
   # Obtener el nombre/ID del contenedor de dvwa
   docker compose ps

   # Ej: el contenedor se llama "dvwa_1" o similar
   docker cp <CONTENEDOR_DVWA>:/var/www/html ./dvwa-src
   ```

   Esto crea una carpeta `./dvwa-src` con el código.

2. Crear un archivo **`docker-compose.override.yml`** al lado del original con:

   ```yaml
   services:
     dvwa:
       volumes:
         - ./dvwa-src:/var/www/html
   ```

   > Si ya tenés otros mounts, asegurate de no duplicar la misma ruta.
   > El override se aplica automáticamente al hacer `docker compose up -d`.

3. Reiniciar para aplicar:

   ```bash
   docker compose up -d
   ```

4. **Editar en el host**: abrí `./dvwa-src` en tu editor y modificá, por ejemplo:

   * `./dvwa-src/vulnerabilities/sqli/index.php`
   * `./dvwa-src/config/config.inc.php`

5. **Ver cambios**: refrescá el navegador.
   Si no se ven, limpiá caché o reiniciá el servicio:

   ```bash
   docker compose restart dvwa
   ```

> Ventajas: edición fácil, control de versiones con Git, coherente para todos los alumnos.

---

### Opción B: **Editar dentro del contenedor** (rápido, pero menos cómodo)

1. Entrar al contenedor:

   ```bash
   docker compose exec dvwa bash
   cd /var/www/html
   apt-get update && apt-get install -y nano # si necesitás editor
   nano vulnerabilities/sqli/index.php
   ```
2. Guardás, salís, y refrescás la página.

> Contras: los cambios se pierden si eliminás el contenedor (a menos que sea un volumen). Mejor para “toques” puntuales.

---

### Opción C: **Copiar archivos desde/hacia el contenedor** (sin override)

* **Exportar a host**:

  ```bash
  docker cp dvwa:/var/www/html ./dvwa-copy
  ```
* Editás `./dvwa-copy/...` en tu host.
* **Reimportar**:

  ```bash
  docker cp ./dvwa-copy/. dvwa:/var/www/html
  docker compose restart dvwa
  ```

> Útil cuando no podés/querés usar bind mounts, pero menos práctico que el override.

---

## 5) Estructura típica que tus alumnos van a tocar

* `vulnerabilities/`
  Cada subcarpeta es un módulo (e.g., `sqli`, `xss`, `csrf`, `upload`, etc.).
  Dentro hay `index.php` u otros `.php` con la lógica vulnerable.
* `config/config.inc.php`
  Conexión a DB, llaves, etc. DVWA suele generar/actualizar este archivo en el **Setup**.
* `includes/`
  Funciones y plantillas comunes.

---

## 6) Comandos de verificación y diagnóstico

* Ver puertos y servicios:

  ```bash
  docker compose ps
  ```

* Ver logs “en vivo”:

  ```bash
  docker compose logs -f dvwa
  docker compose logs -f db
  ```

* Ver salud de MySQL (prueba rápida con `phpMyAdmin`):

  * `http://localhost:8081` → login `root` / `rootpass`
  * Confirmar que la DB `dvwa` existe.

* Probar conectividad desde `dvwa` hacia `db`:

  ```bash
  docker compose exec dvwa bash
  apt-get update && apt-get install -y netcat
  nc -zv db 3306
  ```

---

## 7) Permisos y gotchas frecuentes

* **Permisos de escritura** en `/var/www/html`:

  * Si usás bind mount desde host, podría hacer falta:

    ```bash
    docker compose exec dvwa bash
    chown -R www-data:www-data /var/www/html
    chmod -R 755 /var/www/html
    ```
* **Windows**: evitar rutas con espacios/caracteres raros para los mounts.
* **Caché del navegador**: forzar recarga (Ctrl+Shift+R).
* **Resetear DVWA** (DB y configuración) si algo queda inconsistente:

  * Desde la UI: **Setup → Create / Reset Database**.
  * O recrear contenedores:

    ```bash
    docker compose down -v   # -v borra volúmenes (resetea DB)
    docker compose up -d
    ```

---

## 8) (Opcional) Hacer un “sandbox” por alumno

Para que cada alumno tenga su copia editable y no pisen su trabajo:

1. Crear ramas/carpeta `alumno_<apellido>` con una copia de `docker-compose.yml`.
2. En cada copia, usar un **proyecto** Compose distinto (cambia el prefijo de contenedores):

   ```bash
   docker compose -p dvwa_<apellido> up -d
   ```
3. Asignar **puertos distintos** para DVWA si todos trabajan en la misma máquina (p.ej., 8082, 8083, …). Esto se define en el `docker-compose.yml` (sección `ports:` del servicio `dvwa`).

---

## 9) (Opcional docente) Forzar que **siempre** editen en host

Si querés garantizar que los alumnos modifiquen los archivos fuera del contenedor (y versionen con Git), podés **incluir** desde el principio un `docker-compose.override.yml` con el bind mount y proveer la carpeta `dvwa-src` vacía (o ya poblada con `docker cp` como mostré). Así no dependen de `docker cp` ni de editores en el contenedor.

---

## 10) Resumen operativo para la clase

1. `docker compose up -d`
2. `docker compose ps` → encontrar puerto de DVWA
3. `http://localhost:<puerto_dvwa>` → **Setup → Create/Reset DB**
4. Crear `docker-compose.override.yml` con:

   ```yaml
   services:
     dvwa:
       volumes:
         - ./dvwa-src:/var/www/html
   ```
5. `docker cp <dvwa>:/var/www/html ./dvwa-src` (solo la primera vez)
6. Editar en `./dvwa-src/vulnerabilities/...`
7. Refrescar navegador / `docker compose restart dvwa` si hace falta.

