## Primer examen parcial de Bases de Datos II
### 10 de junio de 2025
#### Horario: 19:30 a 20:55
**Entrega:** Presenta tus respuestas en un archivo de texto (.txt) y súbelo en la misma tarea de Moodle donde está este enunciado.
Puedes realizar los ejercicios en [OneCompiler MongoDB](https://onecompiler.com/mongodb) o usar `mongosh` si lo tienes instalado.

**Atención:** La detección del uso de IA para la resolución parcial o total se penalizará desaprobando el examen.

**Colecciones necesarias**

```js
// Inserción libros
db.libros.insertMany([
  { _id: ObjectId("650000000000000000000001"), titulo: "El Principito", genero: "Infantil", precio: 1500, ejemplares_disponibles: 18 },
  { _id: ObjectId("650000000000000000000002"), titulo: "Cien años de soledad", genero: "Realismo Mágico", precio: 2800, ejemplares_disponibles: 7 },
  { _id: ObjectId("650000000000000000000003"), titulo: "1984", genero: "Distopía", precio: 2200, ejemplares_disponibles: 12 },
  { _id: ObjectId("650000000000000000000004"), titulo: "Don Quijote", genero: "Clásico", precio: 3500, ejemplares_disponibles: 4 },
  { _id: ObjectId("650000000000000000000005"), titulo: "Harry Potter y la Piedra Filosofal", genero: "Fantasía", precio: 2400, ejemplares_disponibles: 25 },
  { _id: ObjectId("650000000000000000000006"), titulo: "El código Da Vinci", genero: "Thriller", precio: 1900, ejemplares_disponibles: 9 }
]);

// Inserción prestamos
db.prestamos.insertMany([
  { _id: ObjectId("650000000000000000000011"), libro_id: ObjectId("650000000000000000000001"), cantidad_prestada: 3, valor_prestamo: 4500, fecha: ISODate("2025-05-08T10:30:00Z") },
  { _id: ObjectId("650000000000000000000012"), libro_id: ObjectId("650000000000000000000002"), cantidad_prestada: 1, valor_prestamo: 2800, fecha: ISODate("2025-05-12T14:15:00Z") },
  { _id: ObjectId("650000000000000000000013"), libro_id: ObjectId("650000000000000000000003"), cantidad_prestada: 2, valor_prestamo: 4400, fecha: ISODate("2025-05-15T09:20:00Z") },
  { _id: ObjectId("650000000000000000000014"), libro_id: ObjectId("650000000000000000000004"), cantidad_prestada: 1, valor_prestamo: 3500, fecha: ISODate("2025-05-18T16:45:00Z") },
  { _id: ObjectId("650000000000000000000015"), libro_id: ObjectId("650000000000000000000005"), cantidad_prestada: 4, valor_prestamo: 9600, fecha: ISODate("2025-05-20T11:00:00Z") },
  { _id: ObjectId("650000000000000000000016"), libro_id: ObjectId("650000000000000000000006"), cantidad_prestada: 2, valor_prestamo: 3800, fecha: ISODate("2025-05-22T13:30:00Z") },
  { _id: ObjectId("650000000000000000000017"), libro_id: ObjectId("650000000000000000000003"), cantidad_prestada: 1, valor_prestamo: 2200, fecha: ISODate("2025-05-25T18:10:00Z") },
  { _id: ObjectId("650000000000000000000018"), libro_id: ObjectId("650000000000000000000001"), cantidad_prestada: 2, valor_prestamo: 3000, fecha: ISODate("2025-05-28T20:00:00Z") },
  { _id: ObjectId("640000000000000000000019"), libro_id: ObjectId("650000000000000000000001"), cantidad_prestada: 5, valor_prestamo: 7500, fecha: ISODate("2025-03-15T10:30:00Z") },
  { _id: ObjectId("640000000000000000000020"), libro_id: ObjectId("650000000000000000000002"), cantidad_prestada: 2, valor_prestamo: 5600, fecha: ISODate("2025-03-20T14:15:00Z") },
  { _id: ObjectId("640000000000000000000021"), libro_id: ObjectId("650000000000000000000003"), cantidad_prestada: 3, valor_prestamo: 6600, fecha: ISODate("2025-04-05T09:20:00Z") },
  { _id: ObjectId("640000000000000000000022"), libro_id: ObjectId("650000000000000000000004"), cantidad_prestada: 2, valor_prestamo: 7000, fecha: ISODate("2025-04-12T16:45:00Z") },
  { _id: ObjectId("640000000000000000000023"), libro_id: ObjectId("650000000000000000000005"), cantidad_prestada: 6, valor_prestamo: 14400, fecha: ISODate("2025-04-15T11:00:00Z") },
  { _id: ObjectId("640000000000000000000024"), libro_id: ObjectId("650000000000000000000006"), cantidad_prestada: 1, valor_prestamo: 1900, fecha: ISODate("2025-04-18T13:30:00Z") },
  { _id: ObjectId("640000000000000000000025"), libro_id: ObjectId("650000000000000000000001"), cantidad_prestada: 4, valor_prestamo: 6000, fecha: ISODate("2025-02-10T10:30:00Z") },
  { _id: ObjectId("640000000000000000000026"), libro_id: ObjectId("650000000000000000000002"), cantidad_prestada: 3, valor_prestamo: 8400, fecha: ISODate("2025-02-14T14:15:00Z") },
  { _id: ObjectId("640000000000000000000027"), libro_id: ObjectId("650000000000000000000003"), cantidad_prestada: 1, valor_prestamo: 2200, fecha: ISODate("2025-02-20T09:20:00Z") },
  { _id: ObjectId("640000000000000000000028"), libro_id: ObjectId("650000000000000000000004"), cantidad_prestada: 1, valor_prestamo: 3500, fecha: ISODate("2025-02-25T16:45:00Z") },
  { _id: ObjectId("640000000000000000000029"), libro_id: ObjectId("650000000000000000000005"), cantidad_prestada: 2, valor_prestamo: 4800, fecha: ISODate("2025-02-28T11:00:00Z") },
  { _id: ObjectId("640000000000000000000030"), libro_id: ObjectId("650000000000000000000006"), cantidad_prestada: 3, valor_prestamo: 5700, fecha: ISODate("2025-01-15T13:30:00Z") }
]);
```

**Nota:** a veces la página OneCompiler arroja error con el código pegado desde acá. Se puede usar esta página de conversión [Dos to Unix](https://toolslick.com/conversion/text/dos-to-unix) para evitar esos problemas.

---

### Ejercicio 1:

1. Lista el **título** y los **ejemplares_disponibles** de todos los libros cuya cantidad en biblioteca sea **menor o igual a 10**.
2. Cuenta cuántos préstamos se realizaron **el 15 de mayo de 2025**.
3. ¿Cuál es el ingreso total acumulado de todos los préstamos? Devuélvelo como un único valor numérico.

---

### Ejercicio 2:
Obtén los **3 libros** que hayan tenido **mayor cantidad de ejemplares prestados** en el último trimestre (marzo-mayo 2025), mostrando:

   * título del libro
   * total de ejemplares prestados