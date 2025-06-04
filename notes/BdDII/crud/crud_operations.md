# Ejemplos Completos de CRUD en MongoDB con PyMongo

Este documento complementa las notas sobre operaciones de actualización, proporcionando ejemplos completos para las operaciones CRUD (Create, Read, Update, Delete) en MongoDB utilizando PyMongo.

## Configuración Inicial de PyMongo

```python
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import pprint

# Conectar al servidor MongoDB
client = MongoClient('mongodb://localhost:27017/')
# Seleccionar la base de datos
db = client['mi_restaurante']
# Seleccionar la colección
restaurante = db.restaurante

# Para imprimir documentos de forma legible
pp = pprint.PrettyPrinter(indent=2)
```

## Ejemplo de CRUD para un Sistema de Gestión de Restaurante

Trabajaremos con una colección llamada `restaurante` que gestiona información sobre platos del menú.

### 1. Create (Crear)

PyMongo ofrece dos métodos principales para insertar documentos:

#### insert_one()
```python
# Insertar un plato al menú
resultado = restaurante.insert_one({
    'nombre': 'Paella Valenciana',
    'categoria': 'Platos principales',
    'precio': 15.50,
    'ingredientes': ['arroz', 'azafrán', 'pollo', 'conejo', 'judías verdes', 'garrofón'],
    'alergenos': ['gluten'],
    'disponible': True,
    'calorias': 450,
    'valoraciones': [],
    'fecha_creacion': datetime.now()
})

# Obtener el ID del documento insertado
id_paella = resultado.inserted_id
print(f"Plato insertado con ID: {id_paella}")
```

#### insert_many()
```python
# Insertar varios platos al menú
resultados = restaurante.insert_many([
    {
        'nombre': 'Gazpacho',
        'categoria': 'Entrantes',
        'precio': 6.75,
        'ingredientes': ['tomate', 'pimiento', 'pepino', 'ajo', 'aceite', 'vinagre'],
        'alergenos': [],
        'disponible': True,
        'calorias': 120,
        'valoraciones': [{'usuario': 'cliente1', 'puntuacion': 4.5, 'comentario': 'Muy refrescante'}],
        'fecha_creacion': datetime.now()
    },
    {
        'nombre': 'Flan de vainilla',
        'categoria': 'Postres',
        'precio': 4.25,
        'ingredientes': ['huevo', 'leche', 'azúcar', 'vainilla'],
        'alergenos': ['huevo', 'lactosa'],
        'disponible': True,
        'calorias': 280,
        'valoraciones': [],
        'fecha_creacion': datetime.now()
    }
])

# Obtener los IDs de los documentos insertados
ids_platos = resultados.inserted_ids
print(f"Se insertaron {len(ids_platos)} platos con IDs: {ids_platos}")
```

### 2. Read (Leer)

PyMongo proporciona varios métodos para consultar documentos:

#### find_one()
```python
# Buscar un plato específico
paella = restaurante.find_one({'nombre': 'Paella Valenciana'})
pp.pprint(paella)
```

#### find()
```python
# Obtener todos los entrantes
entrantes = list(restaurante.find({'categoria': 'Entrantes'}))
print(f"Se encontraron {len(entrantes)} entrantes:")
for entrante in entrantes:
    pp.pprint(entrante)

# Buscar platos sin gluten y con precio menor a 10€
opciones_economicas_sin_gluten = list(restaurante.find({
    'alergenos': {'$nin': ['gluten']},
    'precio': {'$lt': 10}
}))
print(f"Opciones económicas sin gluten: {len(opciones_economicas_sin_gluten)}")
for plato in opciones_economicas_sin_gluten:
    print(f"- {plato['nombre']}: {plato['precio']}€")

# Buscar platos con ciertos ingredientes, ordenados por calorías
platos_con_tomate = list(restaurante.find(
    {'ingredientes': 'tomate'}
).sort('calorias', 1))  # 1 para ascendente, -1 para descendente
print(f"Platos con tomate ordenados por calorías:")
for plato in platos_con_tomate:
    print(f"- {plato['nombre']}: {plato['calorias']} calorías")

# Proyección: obtener solo nombre y precio
menu_simplificado = list(restaurante.find(
    {'disponible': True},
    {'nombre': 1, 'precio': 1, '_id': 0}
))
print("Menú simplificado:")
pp.pprint(menu_simplificado)

# Paginación: obtener 5 platos, saltando los primeros 5
segunda_pagina = list(restaurante.find().skip(5).limit(5))
print("Segunda página del menú:")
for plato in segunda_pagina:
    print(f"- {plato['nombre']}")
```

### 3. Update (Actualizar)

Como ya has detallado en tus notas, aquí te muestro algunos ejemplos prácticos adicionales:

#### update_one()
```python
# Actualizar el precio de un plato
resultado = restaurante.update_one(
    {'nombre': 'Paella Valenciana'},
    {'$set': {'precio': 16.75}}
)
print(f"Documentos encontrados: {resultado.matched_count}")
print(f"Documentos modificados: {resultado.modified_count}")

# Añadir una valoración a un plato
resultado = restaurante.update_one(
    {'nombre': 'Paella Valenciana'},
    {'$push': {
        'valoraciones': {
            'usuario': 'cliente2',
            'puntuacion': 5,
            'comentario': 'Auténtica y deliciosa'
        }
    }}
)
print(f"Valoración añadida: {resultado.modified_count > 0}")

# Actualizar documentos anidados con notación de punto
resultado = restaurante.update_one(
    {'valoraciones.usuario': 'cliente1'},
    {'$set': {'valoraciones.$.puntuacion': 4.7}}
)
print(f"Valoración actualizada: {resultado.modified_count > 0}")
```

#### update_many()
```python
# Incrementar el precio de todos los postres en un 5%
resultado = restaurante.update_many(
    {'categoria': 'Postres'},
    {'$mul': {'precio': 1.05}}
)
print(f"Postres actualizados: {resultado.modified_count}")

# Marcar como no disponibles todos los platos con alérgenos específicos
resultado = restaurante.update_many(
    {'alergenos': {'$in': ['frutos secos', 'mariscos']}},
    {'$set': {'disponible': False}}
)
print(f"Platos marcados como no disponibles: {resultado.modified_count}")
```

#### replace_one()
```python
# Reemplazar completamente un plato
resultado = restaurante.replace_one(
    {'nombre': 'Flan de vainilla'},
    {
        'nombre': 'Flan casero',
        'categoria': 'Postres',
        'precio': 4.50,
        'ingredientes': ['huevo', 'leche', 'azúcar', 'canela'],
        'alergenos': ['huevo', 'lactosa'],
        'disponible': True,
        'calorias': 295,
        'valoraciones': [],
        'fecha_creacion': datetime.now(),
        'receta_actualizada': True
    }
)
print(f"Plato reemplazado: {resultado.modified_count > 0}")
```

#### find_one_and_update()
```python
# Actualizar y devolver el documento actualizado
plato_actualizado = restaurante.find_one_and_update(
    {'nombre': 'Gazpacho'},
    {'$inc': {'precio': 0.25}},
    return_document=True  # Devuelve el documento después de la actualización
)
print("Plato actualizado:")
pp.pprint(plato_actualizado)
```

### 4. Delete (Eliminar)

PyMongo ofrece métodos para eliminar documentos:

#### delete_one()
```python
# Eliminar un plato del menú
resultado = restaurante.delete_one({'nombre': 'Gazpacho'})
print(f"Documentos eliminados: {resultado.deleted_count}")
```

#### delete_many()
```python
# Eliminar todos los platos no disponibles
resultado_multiple = restaurante.delete_many({'disponible': False})
print(f"Documentos eliminados: {resultado_multiple.deleted_count}")

# Eliminar platos con 0 valoraciones y alta cantidad de calorías
resultado = restaurante.delete_many({
    'valoraciones': {'$size': 0},
    'calorias': {'$gt': 500}
})
print(f"Platos eliminados: {resultado.deleted_count}")
```

#### find_one_and_delete()
```python
# Eliminar y devolver el plato eliminado
plato_eliminado = restaurante.find_one_and_delete(
    {'nombre': 'Flan casero'}
)
print("Plato eliminado:")
pp.pprint(plato_eliminado)
```

## Operaciones CRUD Avanzadas

### Uso de transacciones para operaciones múltiples

```python
# Iniciar una sesión
with client.start_session() as session:
    # Iniciar una transacción
    with session.start_transaction():
        try:
            # Crear un nuevo plato
            db.restaurante.insert_one({
                'nombre': 'Arroz negro',
                'categoria': 'Platos principales',
                'precio': 14.50,
                'ingredientes': ['arroz', 'sepia', 'tinta de calamar', 'pimientos'],
                'disponible': True
            }, session=session)
            
            # Actualizar precios en la misma transacción
            db.restaurante.update_many(
                {'categoria': 'Platos principales'},
                {'$inc': {'precio': 1}},
                session=session
            )
            
            # Si todo va bien, la transacción se confirma automáticamente
            print("Transacción completada con éxito")
        except Exception as e:
            # Si hay algún error, la transacción se aborta automáticamente
            print(f"Error en la transacción: {e}")
            # La excepción se propagará y abortará la transacción
```

### Operaciones con bulk_write()

```python
from pymongo import InsertOne, UpdateOne, DeleteMany

# Preparar operaciones de bulk
operaciones = [
    # Insertar un nuevo plato
    InsertOne({
        'nombre': 'Tortilla española',
        'categoria': 'Entrantes',
        'precio': 5.50,
        'ingredientes': ['huevo', 'patata', 'cebolla', 'aceite'],
        'disponible': True
    }),
    # Actualizar un plato existente
    UpdateOne(
        {'nombre': 'Paella Valenciana'},
        {'$set': {'destacado': True}}
    ),
    # Eliminar platos
    DeleteMany({'categoria': 'Fuera de temporada'})
]

# Realizar múltiples operaciones en una sola llamada
resultado = restaurante.bulk_write(operaciones)

print("Resultado de operaciones bulk_write:")
print(f"Documentos insertados: {resultado.inserted_count}")
print(f"Documentos modificados: {resultado.modified_count}")
print(f"Documentos eliminados: {resultado.deleted_count}")
```

### Consultas con agregación

```python
# Obtener estadísticas de platos por categoría
pipeline = [
    {'$match': {'disponible': True}},
    {'$group': {
        '_id': '$categoria',
        'numeroPlatos': {'$sum': 1},
        'precioPromedio': {'$avg': '$precio'},
        'caloriasTotales': {'$sum': '$calorias'}
    }},
    {'$sort': {'numeroPlatos': -1}}
]

estadisticas = list(restaurante.aggregate(pipeline))
print("Estadísticas por categoría:")
pp.pprint(estadisticas)

# Obtener los platos mejor valorados
pipeline = [
    {'$match': {'valoraciones.0': {'$exists': True}}},  # Platos con al menos una valoración
    {'$addFields': {
        'valoracionPromedio': {'$avg': '$valoraciones.puntuacion'}
    }},
    {'$sort': {'valoracionPromedio': -1}},
    {'$limit': 5},
    {'$project': {
        'nombre': 1,
        'categoria': 1,
        'precio': 1,
        'valoracionPromedio': 1,
        'numeroValoraciones': {'$size': '$valoraciones'},
        '_id': 0
    }}
]

mejores_platos = list(restaurante.aggregate(pipeline))
print("Top 5 platos mejor valorados:")
pp.pprint(mejores_platos)
```

## Buenas Prácticas para Operaciones CRUD con PyMongo

1. **Atomicidad**: Utilizar operadores atómicos como `$set`, `$inc`, etc., en lugar de leer-modificar-escribir.
2. **Indexación**: Crear índices para campos frecuentemente consultados para mejorar el rendimiento.
   ```python
   restaurante.create_index([('nombre', 1)])
   restaurante.create_index([('categoria', 1), ('precio', 1)])
   ```
3. **Validación**: Usar esquemas de validación para asegurar la integridad de los datos.
   ```python
   db.create_collection('restaurante', validator={
       '$jsonSchema': {
           'bsonType': 'object',
           'required': ['nombre', 'categoria', 'precio'],
           'properties': {
               'nombre': {'bsonType': 'string'},
               'categoria': {'bsonType': 'string'},
               'precio': {'bsonType': 'double', 'minimum': 0}
           }
       }
   })
   ```
4. **Control de errores**: Siempre verificar resultados de operaciones y manejar posibles errores.
5. **Paginación**: Usar `skip()` y `limit()` para grandes conjuntos de datos.
6. **Consistencia**: Considerar transacciones para operaciones relacionadas.
7. **Proyección**: Solicitar solo los campos necesarios para reducir el uso de memoria y red.