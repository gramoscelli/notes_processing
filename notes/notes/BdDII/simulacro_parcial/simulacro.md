# Simulacro de parcial

**Entrega:** Presenta todas tus respuestas en un archivo de texto (.txt) y súbelo en la misma tarea de Moodle donde está este enunciado.

Puedes realizar los ejercicios en [OneCompiler MongoDB](https://onecompiler.com/mongodb) o usar `mongosh` si lo tienes instalado.

**1. Operaciones CRUD y consultas con operadores relacionales y lógicos**
Colección `estudiantes` con datos de ejemplo:

```js
// Inserta documentos de muestra
db.estudiantes.insertMany([
  { nombre: "María", edad: 22, carrera: "Ingeniería", promedio: 8.5 },
  { nombre: "Pedro", edad: 19, carrera: "Matemáticas", promedio: 6.8 },
  { nombre: "Miguel", edad: 25, carrera: "Ingeniería", promedio: 9.2 },
  { nombre: "Ana",   edad: 24, carrera: "Física",       promedio: 7.5 },
  { nombre: "Laura", edad: 21, carrera: "Ingeniería", promedio: 6.5 },
  { nombre: "Jorge", edad: 23, carrera: "Matemáticas",  promedio: 8.0 },
  { nombre: "Lucía", edad: 20, carrera: "Biología",     promedio: 7.8 },
  { nombre: "Diego", edad: 26, carrera: "Ingeniería",   promedio: 9.0 }
]);
```

Escribe en la consola de MongoDB (o utiliza recursos en línea) las sentencias para:

* Listar todos los estudiantes cuya edad esté entre 20 y 25 años (inclusive).
* Incrementar en 0.2 el campo `promedio` de todos los estudiantes de la carrera “Ingeniería”.
* Eliminar los estudiantes que tengan un `promedio` menor a 7.
* Buscar los estudiantes cuyo nombre comience con la letra “M” o cuyo `promedio` sea mayor o igual a 9.

---

**2. Modelado de datos: documentos embebidos y referencias**
Colecciones con datos de ejemplo para realizar el `$lookup`:

```js
// Clientes
db.clientes.insertMany([
  { _id: ObjectId("64abf1234a1b2c3d4e5f6789"), nombre: "Empresa A", email: "contacto@empresaA.com" },
  { _id: ObjectId("64abf1234a1b2c3d4e5f6790"), nombre: "Empresa B", email: "info@empresaB.com" },
  { _id: ObjectId("64abf1234a1b2c3d4e5f6791"), nombre: "Empresa C", email: "ventas@empresaC.com" }
]);

// Pedidos
db.pedidos.insertMany([
  {
    _id: ObjectId(),
    fecha: ISODate("2025-04-01T10:00:00Z"),
    cliente_id: ObjectId("64abf1234a1b2c3d4e5f6789"),
    productos: [
      { producto: "Teclado", precio: 50.0, cantidad: 2 },
      { producto: "Mouse",   precio: 20.0, cantidad: 1 }
    ]
  },
  {
    _id: ObjectId(),
    fecha: ISODate("2025-04-02T14:30:00Z"),
    cliente_id: ObjectId("64abf1234a1b2c3d4e5f6789"),
    productos: [
      { producto: "Monitor", precio: 150.0, cantidad: 1 }
    ]
  },
  {
    _id: ObjectId(),
    fecha: ISODate("2025-04-03T09:15:00Z"),
    cliente_id: ObjectId("64abf1234a1b2c3d4e5f6790"),
    productos: [
      { producto: "Impresora", precio: 200.0, cantidad: 1 },
      { producto: "Tóner",    precio: 40.0, cantidad: 3 }
    ]
  },
  {
    _id: ObjectId(),
    fecha: ISODate("2025-04-05T11:00:00Z"),
    cliente_id: ObjectId("64abf1234a1b2c3d4e5f6791"),
    productos: [
      { producto: "Cámara",  precio: 350.0, cantidad: 1 },
      { producto: "Trípode", precio: 80.0,  cantidad: 1 }
    ]
  },
  {
    _id: ObjectId(),
    fecha: ISODate("2025-04-06T16:45:00Z"),
    cliente_id: ObjectId("64abf1234a1b2c3d4e5f6790"),
    productos: [
      { producto: "USB Drive", precio: 15.0, cantidad: 5 }
    ]
  }
]);
```

Escribe en la consola de MongoDB (o utiliza recursos en línea) la consulta `aggregate` que utilice `$lookup` para devolver cada documento de `clientes` incluyendo un arreglo `pedidos` con sus pedidos asociados.

---

**3. Pipeline de agregación: análisis de ventas por categoría**
Colección `ventas` con datos de ejemplo:

```js
// Inserta documentos de muestra
db.ventas.insertMany([
  { categoria: "Electrónica", monto: 500, fecha: ISODate("2025-01-10T12:00:00Z") },
  { categoria: "Electrónica", monto: 300, fecha: ISODate("2025-02-05T15:30:00Z") },
  { categoria: "Electrónica", monto: 450, fecha: ISODate("2025-03-15T09:00:00Z") },
  { categoria: "Ropa",        monto: 150, fecha: ISODate("2025-01-20T11:45:00Z") },
  { categoria: "Ropa",        monto: 200, fecha: ISODate("2025-02-28T14:00:00Z") },
  { categoria: "Ropa",        monto: 120, fecha: ISODate("2025-03-10T10:15:00Z") },
  { categoria: "Alimentos",   monto:  80, fecha: ISODate("2025-01-25T09:00:00Z") },
  { categoria: "Alimentos",   monto:  90, fecha: ISODate("2025-02-14T13:30:00Z") },
  { categoria: "Alimentos",   monto: 100, fecha: ISODate("2025-03-22T17:20:00Z") },
  { categoria: "Deportes",    monto: 250, fecha: ISODate("2025-02-11T08:00:00Z") },
  { categoria: "Deportes",    monto: 300, fecha: ISODate("2025-03-05T16:10:00Z") }
]);
```

Escribe en la consola de MongoDB (o utiliza recursos en línea) el pipeline de agregación (`db.ventas.aggregate([...])`) que:

1. Filtre las ventas entre el 1 de enero y el 31 de marzo de 2025.
2. Agrupe por `categoria`, calculando el total de ventas y el número de transacciones.
3. Ordene los resultados de forma descendente por total de ventas.
4. Limite la salida a las tres categorías con mayor facturación.
