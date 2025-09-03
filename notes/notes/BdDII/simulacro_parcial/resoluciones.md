```js
// Ejercicio 1: Operaciones CRUD y consultas

// 1. Listar estudiantes con edad entre 20 y 25
db.estudiantes.find({ edad: { $gte: 20, $lte: 25 } });

// 2. Incrementar promedio en 0.2 para Ingeniería
db.estudiantes.updateMany(
  { carrera: "Ingeniería" },
  { $inc: { promedio: 0.2 } }
);

// 3. Eliminar estudiantes con promedio < 7
db.estudiantes.deleteMany({ promedio: { $lt: 7 } });

// 4. Buscar estudiantes cuyo nombre comience con 'M' o promedio ≥ 9
db.estudiantes.find({
  $or: [
    { nombre: { $regex: '^M' } },
    { promedio: { $gte: 9 } }
  ]
});

// Ejercicio 2: Modelado de datos y lookup

db.pedidos.aggregate([
  {
    $lookup: {
      from: "clientes",
      localField: "cliente_id",
      foreignField: "_id",
      as: "cliente"
    }
  },
  { $unwind: "$cliente" }
]);

// Ejercicio 3: Pipeline de agregación

db.ventas.aggregate([
  { $match: {
      fecha: { $gte: ISODate("2025-01-01"), $lte: ISODate("2025-03-31") }
    }
  },
  { $group: {
      _id: "$categoria",
      totalVentas: { $sum: "$monto" },
      transacciones: { $sum: 1 }
    }
  },
  { $sort: { totalVentas: -1 } },
  { $limit: 3 }
]);
```
