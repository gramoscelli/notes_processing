# 📘 Apunte de Git

## 1. Introducción: repositorios y control de versiones

### ¿Qué es un repositorio?

Un **repositorio** es un lugar donde se almacenan archivos y su historial de cambios.

💡 Ejemplo:

* Un proyecto con código
* Un documento que se va modificando

👉 Un repositorio no solo guarda el estado actual, sino también **todas las versiones anteriores**.



### ¿Qué es el control de versiones?

Es un sistema que permite:

* Guardar cambios
* Volver a versiones anteriores
* Comparar versiones

💡 Sin control de versiones:

* archivo_v1
* archivo_v2
* archivo_final

💡 Con control de versiones:

* Todo queda organizado automáticamente



### Historia breve

Antes de Git existían otros sistemas como:

* **CVS (Concurrent Versions System)**
* **Subversion (SVN)**

👉 Estos sistemas eran **centralizados**:

* Un servidor central
* Los usuarios dependen de ese servidor



### ¿Qué cambia con Git?

Git (creado en 2005 por Linus Torvalds) introduce:

* Sistema **distribuido**
* Cada usuario tiene una copia completa del repositorio
* Mayor velocidad y flexibilidad

👉 Esto permite trabajar sin conexión y facilita el trabajo en equipo.



💬 Preguntas y respuestas:

* ¿Qué es un repositorio?
  → Es una carpeta que guarda archivos y su historial.
* ¿Qué problema resuelve el control de versiones?
  → Evita perder cambios y permite volver atrás.
* ¿Qué diferencia hay entre Git y SVN?
  → Git es distribuido, SVN es centralizado.



## 2. Instalación de Git en Ubuntu

### Instalación

```
sudo apt update
sudo apt install git -y
```

Verificar:

```
git --version
```

### Configuración inicial

```
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```



### Instalación en WSL

```
wsl --install
```

Luego en Ubuntu:

```
sudo apt update
sudo apt install git -y
```



💬 Preguntas y respuestas:

* ¿Para qué sirve configurar el usuario?
  → Para identificar quién hace los cambios.



## 3. ¿Qué es Git?

Git es un **sistema de control de versiones distribuido**. Eso significa que permite registrar los cambios que se realizan sobre un conjunto de archivos y, además, que cada persona que trabaja con el proyecto puede tener una copia completa del repositorio en su propia computadora.

En otras palabras, Git no se limita a guardar archivos: guarda la **historia del proyecto**.

### ¿Para qué sirve Git?

Git sirve para:

* registrar cambios de forma ordenada;
* volver a versiones anteriores si algo sale mal;
* comparar distintas versiones de un mismo archivo;
* trabajar en equipo sin sobrescribir el trabajo de otros;
* desarrollar nuevas ideas en ramas separadas sin afectar la versión principal.

### ¿Qué guarda Git exactamente?

Git guarda:

* el contenido de los archivos en distintos momentos;
* quién realizó cada cambio;
* cuándo se realizó;
* un mensaje que describe qué se hizo.

A cada punto guardado en la historia se lo llama **commit**.

### Ejemplo conceptual

Supongamos que un alumno está desarrollando una página web:

* Día 1: crea `index.html`
* Día 2: agrega estilos en `style.css`
* Día 3: modifica el menú y rompe el diseño

Si está usando Git, puede revisar la historia del proyecto y volver a una versión anterior que funcionaba correctamente.



💬 Preguntas y respuestas:

* ¿Git guarda archivos o versiones?
  → Git guarda versiones de los archivos y el historial de cambios del proyecto.
* ¿Qué es un commit?
  → Es un registro guardado del proyecto en un momento determinado.
* ¿Git sirve solo para programar?
  → No. También puede usarse con documentos, apuntes, configuraciones y otros tipos de archivos.



## 4. Flujo de trabajo

Para entender Git, conviene pensar el trabajo en tres zonas diferentes:

1. **Working Directory**
2. **Staging Area**
3. **Repository**

### 4.1 Working Directory

Es la carpeta de trabajo normal, es decir, el lugar donde creás, editás y eliminás archivos.

Por ejemplo:

* escribís código en un archivo;
* corregís un texto;
* agregás una imagen al proyecto.

En esta etapa, los cambios todavía no forman parte de la historia guardada de Git.

### 4.2 Staging Area

La **staging area** es una zona intermedia. Allí se colocan los cambios que querés incluir en el próximo commit.

Esto es importante porque Git permite elegir con precisión qué cambios se van a guardar y cuáles no.

👉 Idea clave: **editar un archivo no significa guardarlo automáticamente en Git**.

Primero se prepara con `git add`.

### 4.3 Repository

Es el repositorio propiamente dicho, donde Git almacena el historial confirmado mediante commits.

Cuando hacés un commit, los cambios pasan a formar parte de la historia del proyecto.

### Resumen del flujo

```text
Working Directory → Staging Area → Repository
editar            → git add      → git commit
```

### Ejemplo

1. Editás `archivo.txt`
2. Ejecutás:

```bash
git add archivo.txt
```

3. Luego ejecutás:

```bash
git commit -m "Actualiza el contenido inicial"
```



💬 Preguntas y respuestas:

* ¿Qué es staging?
  → Es una zona intermedia donde se preparan los cambios antes de guardarlos definitivamente.
* ¿Qué pasa si modifico un archivo pero no hago commit?
  → El cambio existe en tu carpeta de trabajo, pero no queda registrado en la historia de Git.
* ¿Qué pasa si hago `git add` pero no `git commit`?
  → El cambio queda preparado, pero todavía no está guardado definitivamente en el repositorio.



## 5. Comandos básicos

A continuación se presentan los comandos más importantes para comenzar a trabajar con Git.

### 5.1 `git init`

```bash
git init
```

Este comando convierte la carpeta actual en un repositorio Git.

Cuando se ejecuta, Git crea internamente una carpeta oculta llamada `.git`, donde guarda toda la información del historial.

### 5.2 `git status`

```bash
git status
```

Muestra el estado actual del repositorio. Indica, por ejemplo:

* qué archivos fueron modificados;
* cuáles están preparados para commit;
* cuáles todavía no están siendo seguidos por Git.

Es uno de los comandos más útiles, especialmente para principiantes.

### 5.3 `git add`

```bash
git add archivo.txt
```

Agrega un archivo específico al área de preparación.

Para agregar todos los cambios de la carpeta actual:

```bash
git add .
```

⚠️ Aunque `git add .` es práctico, conviene usarlo con cuidado, porque puede incluir archivos que no querías guardar.

### 5.4 `git commit`

```bash
git commit -m "mensaje"
```

Guarda en la historia del repositorio todos los cambios que estaban en staging.

El mensaje debe explicar claramente qué se hizo.

#### Ejemplos de buenos mensajes

* `Agrega archivo README inicial`
* `Corrige error en el cálculo del total`
* `Incorpora estilos básicos a la página principal`

#### Ejemplos de malos mensajes

* `cambios`
* `arreglé algo`
* `123`

### 5.5 `git log`

```bash
git log
```

Muestra el historial de commits del repositorio.

Versión resumida:

```bash
git log --oneline
```



💬 Preguntas y respuestas:

* ¿Qué hace `git init`?
  → Crea un repositorio Git en la carpeta actual.
* ¿Para qué sirve `git status`?
  → Para ver qué archivos cambiaron y en qué estado están.
* ¿Qué pasa si hago commit sin add?
  → Git no incluirá los cambios nuevos que no hayan sido preparados previamente.
* ¿Por qué es importante el mensaje del commit?
  → Porque ayuda a entender la historia del proyecto.



## 6. Ejemplo completo

Veamos un ejemplo sencillo, paso a paso.

### 6.1 Crear una carpeta de trabajo

```bash
mkdir proyecto
cd proyecto
```

Esto crea una carpeta llamada `proyecto` y entra en ella.

### 6.2 Inicializar Git

```bash
git init
```

Ahora la carpeta ya es un repositorio.

### 6.3 Crear un archivo

```bash
echo "Hola" > archivo.txt
```

Se crea un archivo llamado `archivo.txt` con el texto `Hola`.

### 6.4 Ver el estado

```bash
git status
```

Git mostrará que existe un archivo nuevo sin seguimiento.

### 6.5 Preparar el archivo

```bash
git add archivo.txt
```

Ahora el archivo pasa al staging area.

### 6.6 Crear el primer commit

```bash
git commit -m "Primer commit"
```

Con esto queda registrada la primera versión del proyecto.

### 6.7 Consultar el historial

```bash
git log --oneline
```

Verás el commit recién creado.



💬 Preguntas y respuestas:

* ¿Cómo veo el historial?
  → Con `git log` o `git log --oneline`.
* ¿Qué significa “archivo sin seguimiento”?
  → Que Git detecta el archivo, pero todavía no fue agregado al repositorio.
* ¿Cuál suele ser el primer commit de un proyecto?
  → Generalmente uno que crea la estructura inicial o agrega el README.



## 7. Archivos ignorados: .gitignore

En muchos proyectos existen archivos que **no deben guardarse en el repositorio**, por ejemplo:

* archivos temporales;
* configuraciones locales;
* dependencias descargadas;
* archivos generados automáticamente.

Para evitar que Git los registre, se utiliza un archivo llamado **`.gitignore`**.

### ¿Qué es `.gitignore`?

Es un archivo de texto donde se especifican patrones de archivos o carpetas que Git debe ignorar.

👉 Es decir: Git ve esos archivos, pero decide no incluirlos en los commits.

### Ejemplo básico

Crear el archivo:

```bash
touch .gitignore
```

Editar su contenido:

```text
node_modules/
*.log
.env
```

Esto indica:

* ignorar la carpeta `node_modules`;
* ignorar todos los archivos `.log`;
* ignorar el archivo `.env`.

### Ejemplo aplicado

Supongamos un proyecto con esta estructura:

```text
proyecto/
├── app.js
├── node_modules/
├── error.log
└── .env
```

Con `.gitignore`, solo se versionará:

```text
app.js
```

### Importante

👉 `.gitignore` **no elimina archivos ya versionados**.

Si un archivo ya fue agregado, primero hay que quitarlo del repositorio:

```bash
git rm --cached archivo
```

Luego agregarlo al `.gitignore`.

### Buenas prácticas

* Crear `.gitignore` al inicio del proyecto.
* Usar plantillas (por ejemplo, para Node, Python, etc.).
* No subir archivos sensibles (como contraseñas).



💬 Preguntas y respuestas:

* ¿Para qué sirve `.gitignore`?
  → Para evitar que ciertos archivos se incluyan en el repositorio.
* ¿Git ignora archivos automáticamente?
  → No. Solo los que estén definidos en `.gitignore`.
* ¿Qué pasa si ya subí un archivo que quiero ignorar?
  → Hay que quitarlo del repositorio con `git rm --cached`.



## 8. GitHub

### ¿Qué es GitHub?

GitHub es una plataforma en línea que permite alojar repositorios Git en internet.

Git funciona en la computadora local. GitHub agrega una capa de trabajo remoto y colaboración.

### ¿Para qué sirve GitHub?

Sirve para:

* tener una copia remota del proyecto;
* compartir el repositorio con otras personas;
* trabajar en equipo;
* publicar proyectos;
* integrar revisiones y propuestas de cambio.

### Relación entre Git y GitHub

* **Git**: herramienta de control de versiones.
* **GitHub**: servicio web que aloja repositorios Git.

👉 No son lo mismo. Se puede usar Git sin GitHub.

### 7.1 Conectar un repositorio local con GitHub

```bash
git remote add origin URL
```

Ejemplo:

```bash
git remote add origin https://github.com/usuario/mi-proyecto.git
```

Aquí:

* `remote` indica un repositorio remoto;
* `origin` es el nombre habitual que se le da al remoto principal;
* `URL` es la dirección del repositorio en GitHub.

### 7.2 Subir cambios

```bash
git push -u origin main
```

Esto envía los commits locales al repositorio remoto.

* `push` = subir cambios;
* `origin` = remoto;
* `main` = rama principal.

### 7.3 Traer cambios

```bash
git pull origin main
```

Esto descarga y fusiona en tu repositorio local los cambios que existan en GitHub.

### 7.4 Clonar un repositorio

```bash
git clone https://github.com/usuario/mi-proyecto.git
```

Este comando copia un repositorio remoto completo a tu computadora.



💬 Preguntas y respuestas:

* ¿Qué es `origin`?
  → Es el nombre que normalmente se le da al repositorio remoto principal.
* ¿Qué hace `git push`?
  → Sube los commits locales al repositorio remoto.
* ¿Qué hace `git pull`?
  → Trae cambios del remoto y los integra al repositorio local.
* ¿Qué diferencia hay entre `git clone` y `git init`?
  → `git init` crea un repositorio nuevo; `git clone` copia uno existente.



## 9. Ramas

Las ramas permiten desarrollar cambios en paralelo sin afectar directamente la rama principal.

### ¿Por qué existen las ramas?

Porque en un proyecto real no conviene mezclar todo en una sola línea de trabajo. Por ejemplo, se puede:

* mantener una versión estable del proyecto;
* desarrollar una nueva funcionalidad en otra rama;
* corregir errores sin alterar la versión principal.

### Rama principal

Actualmente, la rama principal suele llamarse `main`.

Allí suele mantenerse la versión más estable del proyecto.

### 8.1 Crear una rama

```bash
git branch nueva-rama
```

### 8.2 Cambiar de rama

```bash
git checkout nueva-rama
```

Forma moderna:

```bash
git switch nueva-rama
```

### 8.3 Crear y cambiar en un solo paso

```bash
git checkout -b nueva-rama
```

O con sintaxis moderna:

```bash
git switch -c nueva-rama
```

### 8.4 Fusionar ramas

Primero se vuelve a la rama principal:

```bash
git switch main
```

Luego se fusiona:

```bash
git merge nueva-rama
```

Esto incorpora en `main` los cambios hechos en `nueva-rama`.

### Ejemplo práctico

```bash
git switch -c feature-login
```

Se trabaja en esa rama, se hacen commits y luego:

```bash
git switch main
git merge feature-login
```



💬 Preguntas y respuestas:

* ¿Por qué no conviene trabajar siempre en `main`?
  → Porque cualquier error impacta directamente en la versión principal.
* ¿Qué es una feature branch?
  → Es una rama creada para desarrollar una funcionalidad específica.
* ¿Qué hace `git merge`?
  → Une los cambios de una rama dentro de otra.



## 10. Conflictos

Un conflicto ocurre cuando Git no puede unir automáticamente dos cambios.

Esto suele pasar cuando dos ramas modificaron la misma parte de un archivo.

### Ejemplo de conflicto

Git puede marcar el archivo así:

```text
<<<<<<< HEAD
código A
=======
código B
>>>>>>> rama
```

Esto significa que hay dos versiones distintas de la misma zona del archivo.

### ¿Cómo se resuelve?

1. Leer ambas versiones.
2. Decidir cuál debe quedar, o combinar ambas.
3. Editar el archivo manualmente.
4. Guardar el archivo corregido.
5. Agregarlo nuevamente con `git add`.
6. Confirmar la resolución con un commit.

### Ejemplo de resolución

```bash
git add archivo.txt
git commit -m "Resuelve conflicto de merge"
```

### Idea importante

Los conflictos no son un error extraño: son una consecuencia normal del trabajo en equipo.



💬 Preguntas y respuestas:

* ¿Qué es un conflicto?
  → Es una situación en la que Git no puede decidir automáticamente cómo unir cambios.
* ¿Siempre que hay dos ramas hay conflicto?
  → No. Solo cuando los cambios interfieren entre sí.
* ¿Git resuelve todos los conflictos solo?
  → No. A veces necesita intervención manual.



