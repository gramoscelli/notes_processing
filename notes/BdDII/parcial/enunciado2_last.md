## Primer examen parcial de Bases de Datos II
### 27 de mayo de 2025
#### Horario: 19:30 a 20:55
**Entrega:** Presenta tus respuestas en un archivo de texto (.txt) y súbelo en la misma tarea de Moodle donde está este enunciado.
Puedes realizar los ejercicios en [OneCompiler MongoDB](https://onecompiler.com/mongodb) o usar `mongosh` si lo tienes instalado.

**Atención:** La detección del uso de IA para la resolución parcial o total se penalizará desaprobando el examen.

**Colecciones necesarias**

```js
// Inserción platos
db.platos.insertMany([
  { _id: ObjectId("650000000000000000000001"), nombre: "Milanesa Napolitana", categoria: "Carnes", precio: 2800, porciones_disponibles: 10 },
  { _id: ObjectId("650000000000000000000002"), nombre: "Ensalada César", categoria: "Ensaladas", precio: 1900, porciones_disponibles: 25 },
  { _id: ObjectId("650000000000000000000003"), nombre: "Pizza Margherita", categoria: "Pizzas", precio: 2200, porciones_disponibles: 8 },
  { _id: ObjectId("650000000000000000000004"), nombre: "Tiramisú", categoria: "Postres", precio: 1400, porciones_disponibles: 5 },
  { _id: ObjectId("650000000000000000000005"), nombre: "Pasta Carbonara", categoria: "Pastas", precio: 2100, porciones_disponibles: 15 },
  { _id: ObjectId("650000000000000000000006"), nombre: "Empanadas de Carne", categoria: "Entradas", precio: 1600, porciones_disponibles: 12 }
]);
// Inserción pedidos - DATOS ORIGINALES (desde 13/05/2025)
db.pedidos.insertMany([
  { _id: ObjectId("650000000000000000000011"), plato_id: ObjectId("650000000000000000000001"), cantidad: 3, total_pedido: 8400, fecha: ISODate("2025-05-04T19:30:00Z") },
  { _id: ObjectId("650000000000000000000012"), plato_id: ObjectId("650000000000000000000002"), cantidad: 2, total_pedido: 3800, fecha: ISODate("2025-05-07T20:15:00Z") },
  { _id: ObjectId("650000000000000000000013"), plato_id: ObjectId("650000000000000000000003"), cantidad: 1, total_pedido: 2200, fecha: ISODate("2025-05-10T21:00:00Z") },
  { _id: ObjectId("650000000000000000000014"), plato_id: ObjectId("650000000000000000000004"), cantidad: 4, total_pedido: 5600, fecha: ISODate("2025-05-11T18:45:00Z") },
  { _id: ObjectId("650000000000000000000015"), plato_id: ObjectId("650000000000000000000005"), cantidad: 2, total_pedido: 4200, fecha: ISODate("2025-05-13T19:20:00Z") },
  { _id: ObjectId("650000000000000000000016"), plato_id: ObjectId("650000000000000000000006"), cantidad: 6, total_pedido: 9600, fecha: ISODate("2025-05-16T20:10:00Z") },
  { _id: ObjectId("650000000000000000000017"), plato_id: ObjectId("650000000000000000000003"), cantidad: 2, total_pedido: 4400, fecha: ISODate("2025-05-18T19:55:00Z") },
  { _id: ObjectId("650000000000000000000018"), plato_id: ObjectId("650000000000000000000001"), cantidad: 1, total_pedido: 2800, fecha: ISODate("2025-05-20T21:30:00Z") },
  { _id: ObjectId("640000000000000000000019"), plato_id: ObjectId("650000000000000000000001"), cantidad: 5, total_pedido: 14000, fecha: ISODate("2025-04-15T19:30:00Z") },
  { _id: ObjectId("640000000000000000000020"), plato_id: ObjectId("650000000000000000000002"), cantidad: 3, total_pedido: 5700,  fecha: ISODate("2025-04-18T20:15:00Z") },
  { _id: ObjectId("640000000000000000000021"), plato_id: ObjectId("650000000000000000000003"), cantidad: 4, total_pedido: 8800,  fecha: ISODate("2025-04-20T21:00:00Z") },
  { _id: ObjectId("640000000000000000000022"), plato_id: ObjectId("650000000000000000000004"), cantidad: 2, total_pedido: 2800,  fecha: ISODate("2025-04-22T18:45:00Z") },
  { _id: ObjectId("640000000000000000000023"), plato_id: ObjectId("650000000000000000000005"), cantidad: 6, total_pedido: 12600, fecha: ISODate("2025-04-25T19:20:00Z") },
  { _id: ObjectId("640000000000000000000024"), plato_id: ObjectId("650000000000000000000006"), cantidad: 3, total_pedido: 4800,  fecha: ISODate("2025-04-28T20:10:00Z") },
  { _id: ObjectId("640000000000000000000025"), plato_id: ObjectId("650000000000000000000001"), cantidad: 2, total_pedido: 5600,  fecha: ISODate("2025-03-10T19:30:00Z") },
  { _id: ObjectId("640000000000000000000026"), plato_id: ObjectId("650000000000000000000002"), cantidad: 4, total_pedido: 7600,  fecha: ISODate("2025-03-15T20:15:00Z") },
  { _id: ObjectId("640000000000000000000027"), plato_id: ObjectId("650000000000000000000003"), cantidad: 1, total_pedido: 2200,  fecha: ISODate("2025-03-18T21:00:00Z") },
  { _id: ObjectId("640000000000000000000028"), plato_id: ObjectId("650000000000000000000004"), cantidad: 3, total_pedido: 4200,  fecha: ISODate("2025-03-22T18:45:00Z") },
  { _id: ObjectId("640000000000000000000029"), plato_id: ObjectId("650000000000000000000005"), cantidad: 1, total_pedido: 2100,  fecha: ISODate("2025-03-25T19:20:00Z") },
  { _id: ObjectId("640000000000000000000030"), plato_id: ObjectId("650000000000000000000006"), cantidad: 5, total_pedido: 8000,  fecha: ISODate("2025-03-28T20:10:00Z") },
  { _id: ObjectId("640000000000000000000031"), plato_id: ObjectId("650000000000000000000001"), cantidad: 4, total_pedido: 11200, fecha: ISODate("2025-05-01T19:30:00Z") },
  { _id: ObjectId("640000000000000000000032"), plato_id: ObjectId("650000000000000000000002"), cantidad: 1, total_pedido: 1900,  fecha: ISODate("2025-05-02T20:15:00Z") },
  { _id: ObjectId("640000000000000000000033"), plato_id: ObjectId("650000000000000000000003"), cantidad: 3, total_pedido: 6600,  fecha: ISODate("2025-05-05T21:00:00Z") },
  { _id: ObjectId("640000000000000000000034"), plato_id: ObjectId("650000000000000000000004"), cantidad: 2, total_pedido: 2800,  fecha: ISODate("2025-05-08T18:45:00Z") },
  { _id: ObjectId("640000000000000000000035"), plato_id: ObjectId("650000000000000000000005"), cantidad: 3, total_pedido: 6300,  fecha: ISODate("2025-05-09T19:20:00Z") },
  { _id: ObjectId("640000000000000000000036"), plato_id: ObjectId("650000000000000000000006"), cantidad: 2, total_pedido: 3200,  fecha: ISODate("2025-05-12T20:10:00Z") }
]);
```

**Nota:** a veces la página OneCompiler arroja error con el código pegado desde acá. Se puede usar esta página de conversión [Dos to Unix](https://toolslick.com/conversion/text/dos-to-unix) para evitar esos problemas.

---

### Ejercicio 1:

1. Lista el **nombre** y las **porciones_disponibles** de todos los platos cuya cantidad en cocina sea **menor o igual a 12**.
2. Cuenta cuántos pedidos se realizaron **el 10 de mayo de 2025**.
3. ¿Cuál es el ingreso total acumulado de todos los pedidos? Devuélvelo como un único valor numérico.

---

### Ejercicio 2:
Obtén los **3 platos** que hayan tenido **mayor cantidad de porciones pedidas** desde el 13/05/2025 y hasta hoy, mostrando:

   * nombre del plato
   * total de porciones pedidas
