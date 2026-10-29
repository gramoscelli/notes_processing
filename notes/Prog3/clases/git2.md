# 📘 Git: Colisiones y resolución de conflictos

## Introducción

Cuando dos o más personas trabajan sobre el mismo repositorio, es inevitable que en algún momento ambas modifiquen la misma parte de un archivo. Git detecta esta situación y la señala como un **conflicto**.

Este documento presenta un escenario concreto de colisión y distintas formas de resolverlo.


## El escenario

Dos programadores trabajan sobre el mismo repositorio en GitHub. El archivo `index.html` en el repositorio remoto contiene:

```html
<h1>Bienvenidos</h1>
<p>Página en construcción</p>
```

### Programador 1

Hace pull, obtiene el archivo actualizado y lo modifica:

```bash
git pull origin main
```

Edita `index.html`:

```html
<h1>Bienvenidos al sitio</h1>
<p>Página en construcción</p>
```

Guarda sus cambios y los sube:

```bash
git add index.html
git commit -m "Mejora el título de bienvenida"
git push origin main
```

Hasta acá no hay ningún problema. El remoto ahora tiene la versión del Programador 1.

### Programador 2

Había hecho pull **antes** del push del Programador 1, así que tiene la versión original. Modifica la misma línea:

```html
<h1>Hola mundo</h1>
<p>Página en construcción</p>
```

Guarda sus cambios localmente:

```bash
git add index.html
git commit -m "Cambia el título principal"
```

### El problema

Cuando el Programador 2 intenta subir sus cambios:

```bash
git push origin main
```

Git **rechaza el push** con un mensaje similar a:

```text
! [rejected]        main -> main (fetch first)
error: failed to push some refs to '...'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

El remoto tiene commits que el Programador 2 no tiene. Necesita integrarlos primero.


## ¿Qué pasa al hacer pull?

El Programador 2 ejecuta:

```bash
git pull origin main
```

Git intenta fusionar automáticamente, pero como ambos modificaron **la misma línea** del mismo archivo, no puede decidir cuál versión es la correcta. Marca el archivo con indicadores de conflicto:

```text
<<<<<<< HEAD
<h1>Hola mundo</h1>
=======
<h1>Bienvenidos al sitio</h1>
>>>>>>> origin/main
<p>Página en construcción</p>
```

Donde:

* `<<<<<<< HEAD` → lo que tiene el Programador 2 (cambio local)
* `=======` → separador entre ambas versiones
* `>>>>>>> origin/main` → lo que viene del remoto (cambio del Programador 1)

Si ejecutamos `git status` veremos:

```text
Unmerged paths:
  both modified:   index.html
```


## Solución 1: Resolución manual directa

Esta es la forma más básica y común.

### Paso 1: Abrir el archivo con conflicto

Abrir `index.html` en cualquier editor de texto. Se verán los marcadores de conflicto.

### Paso 2: Elegir qué conservar

Se puede optar por **una de las versiones** o **combinar ambas**. Por ejemplo, si se quiere conservar solo la versión local:

```html
<h1>Hola mundo</h1>
<p>Página en construcción</p>
```

O solo la versión remota:

```html
<h1>Bienvenidos al sitio</h1>
<p>Página en construcción</p>
```

O combinar ambas ideas:

```html
<h1>Hola mundo - Bienvenidos al sitio</h1>
<p>Página en construcción</p>
```

Lo importante es **eliminar los marcadores** (`<<<<<<<`, `=======`, `>>>>>>>`) y dejar el archivo como debe quedar.

### Paso 3: Confirmar la resolución

```bash
git add index.html
git commit -m "Resuelve conflicto en el título de index.html"
git push origin main
```


## Solución 2: Aceptar una versión completa con checkout

Si durante un conflicto se decide que una de las dos versiones es completamente correcta, se puede resolver sin editar manualmente.

### Aceptar la versión propia (local)

```bash
git checkout --ours index.html
```

Esto descarta los cambios del remoto y conserva la versión del Programador 2.

### Aceptar la versión del remoto

```bash
git checkout --theirs index.html
```

Esto descarta los cambios locales y conserva la versión del Programador 1.

### Confirmar

En ambos casos, después hay que confirmar:

```bash
git add index.html
git commit -m "Resuelve conflicto aceptando versión local/remota"
git push origin main
```

### ¿Cuándo conviene?

* Cuando se sabe con certeza que una de las dos versiones es la correcta.
* Cuando el archivo fue modificado por error en una de las ramas.


## Solución 3: Usar git stash para evitar el conflicto

Esta estrategia es útil cuando el Programador 2 **todavía no hizo commit** de sus cambios. En lugar de commitear y luego resolver conflictos, se guardan temporalmente los cambios locales, se trae lo nuevo del remoto, y se reaplican encima.

### ¿Qué es git stash?

`git stash` guarda los cambios locales sin commitear en una pila temporal y deja el directorio de trabajo limpio.

```text
Cambios locales sin commit → stash (pila temporal) → directorio limpio
```

### Paso a paso

El Programador 2 tiene `index.html` modificado pero **sin commit**:

```bash
git status
```

```text
modified:   index.html
```

### Paso 1: Guardar los cambios en el stash

```bash
git stash
```

Git responde:

```text
Saved working directory and index state WIP on main: abc1234 último commit...
```

Ahora `index.html` vuelve al estado del último commit local.

### Paso 2: Traer los cambios del remoto

```bash
git pull origin main
```

Como el directorio está limpio, el pull se ejecuta **sin conflictos**. Ahora se tiene la versión del Programador 1.

### Paso 3: Reaplicar los cambios guardados

```bash
git stash pop
```

Esto saca los cambios del stash e intenta aplicarlos sobre el estado actual.

### ¿Qué puede pasar?

**Caso A: No hay conflicto.** Si los cambios del stash y los del remoto no se superponen, se aplican limpiamente. Solo queda hacer commit y push.

**Caso B: Hay conflicto.** Si se superponen (como en nuestro ejemplo, ambos tocan la misma línea), Git marca el conflicto igual que antes:

```text
<<<<<<< Updated upstream
<h1>Bienvenidos al sitio</h1>
=======
<h1>Hola mundo</h1>
>>>>>>> Stashed changes
<p>Página en construcción</p>
```

La diferencia es que los marcadores dicen `Updated upstream` (lo que vino del pull) y `Stashed changes` (lo que estaba guardado). Se resuelve manualmente igual que en la Solución 1.

### Paso 4: Confirmar

```bash
git add index.html
git commit -m "Incorpora cambios del remoto y aplica modificación local"
git push origin main
```

### Ventaja del stash

La ventaja principal es que permite **ver primero qué cambió en el remoto** antes de decidir cómo integrar los cambios propios. Es especialmente útil cuando se tiene trabajo en progreso y se quiere actualizar la rama sin hacer un commit incompleto.

### Otros comandos útiles de stash

```bash
git stash list        # Ver todos los stashes guardados
git stash show        # Ver qué archivos cambia el último stash
git stash show -p     # Ver el diff completo del último stash
git stash drop        # Eliminar el último stash sin aplicarlo
git stash clear       # Eliminar todos los stashes
```


## Solución 4: Hacer pull con rebase

En lugar de fusionar (merge), se puede reescribir la historia local para que los commits propios queden **después** de los commits del remoto.

### ¿Qué diferencia hay con merge?

Con **merge** (el comportamiento por defecto de pull):

```text
A---B---C (remoto)
     \
      D---E (local)
           \
            M (merge commit)
```

Con **rebase**:

```text
A---B---C (remoto)
         \
          D'---E' (local, reescrito)
```

El resultado final es el mismo, pero la historia queda más lineal.

### Paso a paso

El Programador 2 ya hizo commit de sus cambios. En lugar de `git pull`, ejecuta:

```bash
git pull --rebase origin main
```

Git toma los commits locales, los "despega" temporalmente, aplica los commits del remoto, y luego intenta reaplicar los locales uno por uno encima.

### Si hay conflicto

Git se detiene y muestra el conflicto en el archivo:

```text
<<<<<<< HEAD
<h1>Bienvenidos al sitio</h1>
=======
<h1>Hola mundo</h1>
>>>>>>> Cambia el título principal
```

Se resuelve editando el archivo manualmente (igual que antes) y luego:

```bash
git add index.html
git rebase --continue
```

Si en algún momento se quiere cancelar el rebase y volver al estado anterior:

```bash
git rebase --abort
```

### Después del rebase

```bash
git push origin main
```

### ¿Cuándo conviene?

* Cuando se quiere mantener una historia lineal y limpia.
* En equipos que prefieren evitar commits de merge innecesarios.


## Resumen comparativo

| Solución | ¿Cuándo usarla? | Requiere editar manualmente |
|---|---|---|
| Manual directa | Siempre funciona, es la más común | Sí |
| checkout --ours/--theirs | Cuando una versión es claramente la correcta | No |
| git stash | Cuando todavía no se hizo commit del cambio local | Puede que sí |
| pull --rebase | Cuando se prefiere historia lineal | Puede que sí |


💬 Preguntas y respuestas:

* ¿Siempre que dos personas trabajan hay conflicto?
  → No. Solo cuando modifican la misma parte del mismo archivo.
* ¿Git puede resolver conflictos solo?
  → Sí, en muchos casos. Si los cambios son en partes distintas del archivo, Git los fusiona automáticamente. Solo pide intervención cuando no puede decidir.
* ¿Qué pasa si hago push sin resolver el conflicto?
  → No se puede. Git no permite hacer push mientras haya archivos con conflictos sin resolver.
* ¿Puedo perder código al resolver un conflicto?
  → Sí, si se borran líneas por error durante la edición manual. Por eso es importante leer ambas versiones con atención antes de decidir.
* ¿Qué diferencia hay entre stash y commit?
  → El commit queda en la historia del proyecto. El stash es temporal y no forma parte del historial de commits.
