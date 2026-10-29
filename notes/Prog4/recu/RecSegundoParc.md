# Recuperatorio del  Segundo Parcial

## Programación IV – Proyecto Node + React con foco en Seguridad Web

En el archivo ZIP provisto se encuentra una aplicación web full-stack compuesta por un **backend en Node + Express** y un **frontend en React + TypeScript**.  (alternativamente se puede bajar de [este repositorio de GitHub](https://github.com/gramoscelli/Prog4-Rec2doParcial-2025.git)).

Las funcionalidades básicas están implementadas, pero algunos mecanismos deben completarse para que los tests incluidos se ejecuten correctamente.

Descomprimir el proyecto, instalar las dependencias, y **desarrollar el código necesario para que los tres tests (dos de backend y uno de frontend) pasen exitosamente**.

> **IMPORTANTE:**
>
> * No se deben modificar los tests.
> * No se deben renombrar carpetas ni archivos.
> * El código de producción debe adaptarse a lo que los tests exigen.
> * La corrección se realizará ejecutando los tests provistos.



##  Instalación de dependencias

### Backend

```bash
$ cd backend
$ npm install
```

### Frontend

```bash
$ cd ../frontend
$ npm install
```



## Ejercicio 1 – Protección CSRF en una operación crítica (Backend)

La empresa ficticia **“ReservaFácil Coworking”** permite que los usuarios realicen operaciones críticas sobre sus reservas (por ejemplo, cancelarlas o modificarlas).
Para evitar ataques del tipo **Cross-Site Request Forgery (CSRF)**, la API debe verificar un token de seguridad antes de ejecutar la acción solicitada.

#### Requerimiento

Implementar la validación CSRF en el endpoint indicado por los tests:

* La petición **solo debe ser aceptada si incluye un token CSRF válido**.
* El token se enviará en un encabezado HTTP (por ejemplo `X-CSRF-Token`) u otra ubicación especificada en los tests.
* Si el token **falta o no es válido**, el servidor debe responder:

  * **HTTP 403 (Forbidden)**
  * Cuerpo JSON con una propiedad `error`.
* Si el token es válido, el endpoint debe ejecutar su lógica normalmente y devolver la respuesta esperada por los tests.

> Se permite usar un valor fijo para el token, siempre que coincida con lo que los tests esperan.



## Ejercicio 2 – Endpoint de resumen diario de reservas (Backend)

La gerencia de **“ReservaFácil Coworking”** solicita un pequeño reporte diario con estadísticas del estado de las reservas.
Se debe implementar un endpoint de solo lectura que devuelva un resumen del día en formato JSON.

#### Requerimiento

Implementar un endpoint (por ejemplo `GET /api/reports/daily`) que:

* Responda con **HTTP 200** cuando la petición sea válida.
* Devuelva un JSON con la siguiente estructura:

```json
{
  "date": "YYYY-MM-DD",
  "total": 10,
  "active": 7,
  "cancelled": 2,
  "pending": 1
}
```

donde:

* `date` es un string con la fecha del día (el formato esperado lo definirán los tests).
* Todos los campos numéricos deben ser **enteros mayores o iguales a 0**.

Si la petición no cumple con las precondiciones que los tests exigen (por ejemplo, parámetros faltantes o formato incorrecto), el endpoint debe responder:

* **HTTP 400 (Bad Request)**
* Cuerpo JSON con una propiedad `error`.

> No es necesario usar una base de datos real: los tests simulan la fuente de datos.



## Ejercicio 3 – Componente de ayuda en el panel del cliente (Frontend)

El equipo de UX pidió agregar una pequeña ayuda contextual en el panel de usuario del frontend.

#### Requerimiento

En el componente principal indicado por los tests, implementar:

1. Un botón con el texto exacto:

```
Ver ayuda
```

2. Cuando el usuario hace clic en ese botón, debe aparecer en la interfaz el siguiente mensaje:

```
Esta es una aplicación de práctica de seguridad web.
```

3. El mensaje **no debe mostrarse inicialmente**; solo debe aparecer después del clic.

Los tests verificarán:

* La presencia del botón.
* La aparición del texto tras la interacción.
* Que inicialmente el texto no esté visible.



## Entrega del trabajo

**Antes de comprimir el proyecto**:

1. Ejecutar **todos** los tests del backend y del frontend y confirmar que **pasen correctamente**.
2. **Eliminar** las carpetas `node_modules` de:

   * `backend/node_modules`
   * `frontend/node_modules`
   
3. Crear un único archivo `.zip` que contenga **todo el proyecto**.

Ejemplo (desde la carpeta raíz del proyecto):

```bash
$ zip -r Prog4-Rec2doParc.zip .
```
