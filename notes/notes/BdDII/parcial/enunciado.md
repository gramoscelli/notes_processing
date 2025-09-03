## Primer examen parcial de Bases de Datos II
### 27 de mayo de 2025
**Entrega:** Presenta tus respuestas en un archivo de texto (.txt) y súbelo en la misma tarea de Moodle donde está este enunciado.
Puedes realizar los ejercicios en [OneCompiler MongoDB](https://onecompiler.com/mongodb) o usar `mongosh` si lo tienes instalado.

**Atención:** La detección del uso de IA para la resolución parcial o total se penalizará desaprobando el examen.

**Colecciones necesarias**

```js
db.productos.insertMany([
  { _id: ObjectId("650000000000000000000001"), nombre: "Auriculares XYZ",  categoria: "Electrónica", precio: 120, stock: 15 },
  { _id: ObjectId("650000000000000000000002"), nombre: "Camiseta Logo",      categoria: "Ropa",        precio: 25,  stock: 50 },
  { _id: ObjectId("650000000000000000000003"), nombre: "Taza Cerámica",      categoria: "Hogar",       precio: 10,  stock: 30 },
  { _id: ObjectId("650000000000000000000004"), nombre: "Smartwatch Pro",   categoria: "Electrónica", precio: 200, stock: 8  },
  { _id: ObjectId("650000000000000000000005"), nombre: "Jeans Classic",      categoria: "Ropa",        precio: 40,  stock: 20 },
  { _id: ObjectId("650000000000000000000006"), nombre: "Lámpara Mesa",       categoria: "Hogar",       precio: 35,  stock: 12 }
]);
// Inserción ventas
db.ventas.insertMany([
  { _id: ObjectId("650000000000000000000011"), producto_id: ObjectId("650000000000000000000001"), cantidad: 2, monto_total: 240, fecha: ISODate("2025-05-05T10:30:00Z") },
  { _id: ObjectId("650000000000000000000012"), producto_id: ObjectId("650000000000000000000002"), cantidad: 1, monto_total: 25,  fecha: ISODate("2025-05-06T14:15:00Z") },
  { _id: ObjectId("650000000000000000000013"), producto_id: ObjectId("650000000000000000000003"), cantidad: 3, monto_total: 30,  fecha: ISODate("2025-05-10T09:00:00Z") },
  { _id: ObjectId("650000000000000000000014"), producto_id: ObjectId("650000000000000000000004"), cantidad: 1, monto_total: 200, fecha: ISODate("2025-05-12T16:45:00Z") },
  { _id: ObjectId("650000000000000000000015"), producto_id: ObjectId("650000000000000000000005"), cantidad: 4, monto_total: 160, fecha: ISODate("2025-05-15T11:20:00Z") },
  { _id: ObjectId("650000000000000000000016"), producto_id: ObjectId("650000000000000000000006"), cantidad: 2, monto_total: 70,  fecha: ISODate("2025-05-18T13:00:00Z") },
  { _id: ObjectId("650000000000000000000017"), producto_id: ObjectId("650000000000000000000003"), cantidad: 1, monto_total: 10,  fecha: ISODate("2025-05-20T18:10:00Z") },
  { _id: ObjectId("650000000000000000000018"), producto_id: ObjectId("650000000000000000000001"), cantidad: 5, monto_total: 600, fecha: ISODate("2025-05-22T20:30:00Z") }
]);
```

Nota: a veces la página OneCompler arroja error son el código pegado desde acá. Se puede usar esta página de conversion [Dos to Unix](https://toolslick.com/conversion/text/dos-to-unix) para evitar esos problemas.

---

### Ejercicio 1:

1. Lista el **nombre** y el **stock** de todos los productos cuya cantidad en inventario sea **menor o igual a 12**.
2. Cuenta cuántas ventas se realizaron **el 10 de mayo de 2025**.
4. ¿Cuál es el ingreso total acumulado de todas las ventas? Devuélvelo como un único valor numérico.

---

**Ejercicio 2:**

1. Incrementa en un **10%** el campo `precio` de todos los productos de la categoría **“Ropa”**.
2. Inserta una venta de prueba para el producto “Taza Cerámica” con la **fecha actual** y una `cantidad` de tu elección; calcula correctamente `monto_total`.
3. Lista los documentos de `productos` mostrando únicamente los campos `nombre` y `precio` para verificar los cambios.

---

**Ejercicio 3:**

Obtén los **3 productos** que hayan vendido **más unidades** en el último trimestre, mostrando:

   * nombre del producto
   * total de unidades vendidas
