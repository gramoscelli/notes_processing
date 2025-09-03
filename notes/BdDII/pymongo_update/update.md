# Operaciones de Actualización en MongoDB

## Operaciones de Actualización (Update Operations)

Las operaciones de actualización en MongoDB nos permiten modificar documentos existentes en una colección. Existen tres métodos principales para realizar actualizaciones:

### 1. updateOne()

Este método actualiza el primer documento que coincide con el filtro especificado.

**Sintaxis básica:**
```javascript
db.coleccion.updateOne(
    { filtro }, 
    { $operador: { campo: valor } },
    { opciones }
)
```

**Ejemplo:**
```javascript
db.empleados.updateOne(
    { nombre: "Carlos" },
    { $set: { departamento: "Ventas" } }
)
```

### 2. updateMany()

Actualiza todos los documentos que coinciden con el filtro especificado.

**Sintaxis básica:**
```javascript
db.coleccion.updateMany(
    { filtro }, 
    { $operador: { campo: valor } },
    { opciones }
)
```

**Ejemplo:**
```javascript
db.productos.updateMany(
    { categoria: "Electrónica" },
    { $inc: { precio: 100 } }
)
```

### 3. replaceOne()

Reemplaza completamente un documento con uno nuevo, manteniendo su _id.

**Sintaxis básica:**
```javascript
db.coleccion.replaceOne(
    { filtro },
    { documento_completo_nuevo },
    { opciones }
)
```

**Ejemplo:**
```javascript
db.clientes.replaceOne(
    { _id: ObjectId("5f8d0b3c7f74b42a1c8b4567") },
    {
        nombre: "Ana García",
        email: "ana@ejemplo.com",
        telefono: "555-123-456"
    }
)
```

### Operadores de Actualización Principales

#### $set
- Modifica el valor de un campo existente o crea el campo si no existe.
- **Ejemplo:** `{ $set: { nombre: "Nuevo Nombre" } }`

#### $inc
- Incrementa el valor de un campo numérico por la cantidad especificada.
- **Ejemplo:** `{ $inc: { stock: -1, visitas: 5 } }`

#### $push
- Añade un elemento a un array.
- **Ejemplo:** `{ $push: { comentarios: "Muy buen producto" } }`

#### $pull
- Elimina elementos de un array que coincidan con la condición.
- **Ejemplo:** `{ $pull: { tags: "oferta" } }`

#### $addToSet
- Añade elementos a un array solo si no existen.
- **Ejemplo:** `{ $addToSet: { categorias: "Premium" } }`

#### $unset
- Elimina campos de un documento.
- **Ejemplo:** `{ $unset: { temporal: "" } }`

#### $rename
- Cambia el nombre de un campo.
- **Ejemplo:** `{ $rename: { "nombre_antiguo": "nombre_nuevo" } }`

#### $mul
- Multiplica el valor de un campo por un número.
- **Ejemplo:** `{ $mul: { precio: 1.1 } }`

### Opciones de Actualización

- **upsert**: Si es true, crea un nuevo documento cuando no encuentra coincidencias con el filtro.
- **multi**: (Obsoleto en versiones nuevas, usar updateMany en su lugar) 
- **arrayFilters**: Condiciones para actualizar elementos específicos en arrays.

**Ejemplo con upsert:**
```javascript
db.pedidos.updateOne(
    { cliente_id: 12345 },
    { $set: { estado: "Procesando" } },
    { upsert: true }
)
```

### Actualizaciones en Documentos Anidados

Para actualizar campos en documentos anidados o subdocumentos, se utiliza la notación de punto.

**Ejemplo:**
```javascript
db.usuarios.updateOne(
    { _id: ObjectId("5f8d0b3c7f74b42a1c8b4568") },
    { $set: { "direccion.ciudad": "Madrid", "direccion.codigo_postal": "28001" } }
)
```

### Actualizaciones en Arrays

Las actualizaciones en arrays pueden ser complejas. Se pueden usar operadores específicos como $[] y $[identifier] junto con arrayFilters.

**Ejemplo de actualización de elemento específico en un array:**
```javascript
db.inventario.updateOne(
    { _id: ObjectId("5f8d0b3c7f74b42a1c8b4569") },
    { $set: { "productos.$[elem].disponible": false } },
    { arrayFilters: [ { "elem.stock": { $lt: 5 } } ] }
)
```

---

**Buenas prácticas:**
1. Usar operadores de actualización en lugar de reemplazar documentos completos cuando sea posible.
2. Considerar el uso de transacciones para actualizaciones complejas en múltiples documentos.
3. Verificar los resultados de la operación para asegurar que se realizaron correctamente.
4. Utilizar upsert con precaución para evitar crear documentos no deseados.
