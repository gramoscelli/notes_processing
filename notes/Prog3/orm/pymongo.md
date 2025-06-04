# Guía Completa de PyMongo

## Introducción a PyMongo

PyMongo es la biblioteca oficial de Python para trabajar con MongoDB, una base de datos NoSQL orientada a documentos. PyMongo permite interactuar con MongoDB desde aplicaciones Python de manera sencilla y eficiente.

MongoDB almacena datos en documentos tipo JSON (llamados BSON) organizados en colecciones, en lugar de tablas con filas y columnas como las bases de datos relacionales.

## Instalación

Para instalar PyMongo, utiliza pip:

```bash
$ pip install pymongo
```

Si necesitas soporte para características específicas como autenticación GSSAPI o conectividad TLS/SSL:

```bash
$ pip install pymongo[snappy,gssapi,srv,tls]
```

## Conexión a MongoDB

### Conexión básica a una instancia local

```python
from pymongo import MongoClient

# Conexión a instancia local por defecto
client = MongoClient()  # Se conecta a 'localhost', puerto 27017

# Alternativamente, especificar host y puerto
client = MongoClient('localhost', 27017)

# O usando formato URI
client = MongoClient('mongodb://localhost:27017/')
```

### Conexión a MongoDB Atlas (en la nube)

```python
from pymongo import MongoClient

# Conexión a MongoDB Atlas
client = MongoClient('mongodb+srv://usuario:contraseña@cluster0.ejemplo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
```

### Acceso a bases de datos y colecciones

```python
# Acceder a una base de datos
db = client.mi_base_datos  # Sintaxis de atributo
# O alternativamente:
db = client['mi_base_datos']  # Sintaxis de diccionario

# Acceder a una colección
coleccion = db.usuarios  # Sintaxis de atributo
# O alternativamente:
coleccion = db['usuarios']  # Sintaxis de diccionario
```

## Operaciones CRUD Básicas

### Create (Crear)

#### Insertar un solo documento

```python
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.mi_base_datos
usuarios = db.usuarios

usuario = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@ejemplo.com",
    "fecha_registro": datetime.datetime.now()
}

# Insertar un documento
resultado = usuarios.insert_one(usuario)
print(f"ID del documento insertado: {resultado.inserted_id}")
```

#### Insertar múltiples documentos

```python
nuevos_usuarios = [
    {
        "nombre": "María",
        "apellido": "González",
        "email": "maria.gonzalez@ejemplo.com",
        "fecha_registro": datetime.datetime.now()
    },
    {
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "email": "carlos.rodriguez@ejemplo.com",
        "fecha_registro": datetime.datetime.now()
    }
]

# Insertar múltiples documentos
resultado = usuarios.insert_many(nuevos_usuarios)
print(f"IDs de documentos insertados: {resultado.inserted_ids}")
```

### Read (Leer)

#### Encontrar un solo documento

```python
# Encontrar un documento
usuario = usuarios.find_one({"nombre": "Juan"})
print(usuario)

# Encontrar por ID
from bson.objectid import ObjectId
usuario_por_id = usuarios.find_one({"_id": ObjectId("5f50a15d0b3...")})
```

#### Encontrar múltiples documentos

```python
# Encontrar todos los documentos de la colección
todos_usuarios = usuarios.find()
for usuario in todos_usuarios:
    print(usuario)

# Encontrar con filtro
usuarios_filtrados = usuarios.find({"apellido": "González"})
for usuario in usuarios_filtrados:
    print(usuario)

# Limitar campos devueltos (1 incluye, 0 excluye)
usuarios_proyeccion = usuarios.find({}, {"nombre": 1, "email": 1, "_id": 0})
for usuario in usuarios_proyeccion:
    print(usuario)  # Solo muestra nombre y email
```

#### Ordenación, límites y saltos

```python
# Ordenar resultados
usuarios_ordenados = usuarios.find().sort("apellido", 1)  # 1 ascendente, -1 descendente

# Limitar resultados
usuarios_limitados = usuarios.find().limit(5)  # Solo 5 documentos

# Saltar resultados
usuarios_con_skip = usuarios.find().skip(10).limit(5)  # Saltar 10, mostrar 5 (para paginación)
```

### Update (Actualizar)

#### Actualizar un solo documento

```python
# Actualizar un documento
filtro = {"nombre": "Juan"}
nueva_info = {"$set": {"email": "juan.nuevo@ejemplo.com"}}

resultado = usuarios.update_one(filtro, nueva_info)
print(f"Documentos modificados: {resultado.modified_count}")
```

#### Actualizar múltiples documentos

```python
# Actualizar múltiples documentos
filtro = {"apellido": "González"}
nueva_info = {"$set": {"activo": True}}

resultado = usuarios.update_many(filtro, nueva_info)
print(f"Documentos modificados: {resultado.modified_count}")
```

#### Reemplazar un documento completo

```python
# Reemplazar un documento entero
filtro = {"nombre": "Carlos"}
nuevo_documento = {
    "nombre": "Carlos",
    "apellido": "Rodríguez Gómez",  # Apellido actualizado
    "email": "carlos.rodriguez@ejemplo.com",
    "activo": True,
    "ultima_actualizacion": datetime.datetime.now()
}

resultado = usuarios.replace_one(filtro, nuevo_documento)
print(f"Documentos modificados: {resultado.modified_count}")
```

### Delete (Eliminar)

#### Eliminar un solo documento

```python
# Eliminar un documento
filtro = {"nombre": "Juan"}
resultado = usuarios.delete_one(filtro)
print(f"Documentos eliminados: {resultado.deleted_count}")
```

#### Eliminar múltiples documentos

```python
# Eliminar múltiples documentos
filtro = {"activo": False}
resultado = usuarios.delete_many(filtro)
print(f"Documentos eliminados: {resultado.deleted_count}")
```

## Consultas Avanzadas

### Operadores de comparación

```python
# Usuarios mayores de cierta edad
mayores = usuarios.find({"edad": {"$gt": 30}})  # mayor que 30
# Usuarios en un rango de edad
rango_edad = usuarios.find({"edad": {"$gte": 18, "$lte": 65}})  # entre 18 y 65
# Usuarios con ciertos apellidos
apellidos = usuarios.find({"apellido": {"$in": ["González", "Rodríguez", "López"]}})
```

### Operadores lógicos

```python
# AND implícito (todos los criterios deben cumplirse)
usuarios.find({"edad": {"$gt": 30}, "activo": True})

# OR explícito
from pymongo import MongoClient
import pymongo

usuarios.find({
    "$or": [
        {"edad": {"$lt": 18}},
        {"edad": {"$gt": 65}}
    ]
})

# AND y OR combinados
usuarios.find({
    "genero": "F",
    "$or": [
        {"edad": {"$lt": 18}},
        {"edad": {"$gt": 65}}
    ]
})
```

### Expresiones regulares

```python
# Búsqueda por coincidencia parcial usando regex
regex_usuarios = usuarios.find({"nombre": {"$regex": "^Mar"}})  # Nombres que empiezan con "Mar"
```

## Operaciones con Índices

### Crear índices

```python
# Crear un índice simple
usuarios.create_index("email")

# Crear un índice único
usuarios.create_index("email", unique=True)

# Crear un índice compuesto
usuarios.create_index([("apellido", pymongo.ASCENDING), ("nombre", pymongo.ASCENDING)])

# Crear un índice TTL (Time-To-Live)
usuarios.create_index("fecha_ultimo_acceso", expireAfterSeconds=2592000)  # 30 días
```

### Listar y eliminar índices

```python
# Listar todos los índices
for indice in usuarios.list_indexes():
    print(indice)

# Eliminar un índice específico
usuarios.drop_index("email_1")

# Eliminar todos los índices excepto _id
usuarios.drop_indexes()
```

## Agregaciones

El framework de agregación de MongoDB permite realizar operaciones de transformación y análisis de datos complejas.

### Pipeline de agregación básico

```python
# Ejemplo: Contar usuarios por apellido
pipeline = [
    {"$group": {"_id": "$apellido", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]

resultados = usuarios.aggregate(pipeline)
for resultado in resultados:
    print(f"Apellido: {resultado['_id']}, Cantidad: {resultado['count']}")
```

### Ejemplo de pipeline más complejo

```python
# Estadísticas de usuarios por grupo de edad
pipeline = [
    # Etapa 1: Agregar un campo calculado
    {"$addFields": {
        "grupo_edad": {
            "$switch": {
                "branches": [
                    {"case": {"$lt": ["$edad", 18]}, "then": "Menor"},
                    {"case": {"$lt": ["$edad", 30]}, "then": "Joven"},
                    {"case": {"$lt": ["$edad", 60]}, "then": "Adulto"}
                ],
                "default": "Senior"
            }
        }
    }},
    # Etapa 2: Agrupar por el nuevo campo
    {"$group": {
        "_id": "$grupo_edad",
        "cantidad": {"$sum": 1},
        "edad_promedio": {"$avg": "$edad"},
        "usuarios": {"$push": {"nombre": "$nombre", "edad": "$edad"}}
    }},
    # Etapa 3: Ordenar resultados
    {"$sort": {"_id": 1}}
]

resultados = usuarios.aggregate(pipeline)
for resultado in resultados:
    print(f"Grupo: {resultado['_id']}")
    print(f"Cantidad: {resultado['cantidad']}")
    print(f"Edad promedio: {resultado['edad_promedio']:.1f}")
    print("----------------")
```

## Transacciones

MongoDB 4.0+ soporta transacciones multi-documento en implementaciones replicadas. PyMongo 3.7+ tiene soporte para estas transacciones.

```python
# Ejemplo de transacción
from pymongo import MongoClient

# Asegúrate de usar MongoDB 4.0+ y un replica set
client = MongoClient('mongodb://localhost:27017/?replicaSet=rs0')
db = client.mi_base_datos

# Iniciar una sesión
with client.start_session() as session:
    # Iniciar transacción
    with session.start_transaction():
        # Operaciones dentro de la transacción
        db.cuentas.update_one(
            {"_id": cuenta_origen_id},
            {"$inc": {"saldo": -monto}},
            session=session
        )
        
        db.cuentas.update_one(
            {"_id": cuenta_destino_id},
            {"$inc": {"saldo": monto}},
            session=session
        )
        
        db.transacciones.insert_one(
            {
                "origen": cuenta_origen_id,
                "destino": cuenta_destino_id,
                "monto": monto,
                "fecha": datetime.datetime.now()
            },
            session=session
        )
        # La transacción se confirma automáticamente al salir del bloque
        # Si ocurre una excepción, se revierte automáticamente
```

## Manejo de Errores

```python
from pymongo.errors import ConnectionFailure, OperationFailure, DuplicateKeyError

try:
    # Intentar conectar
    client = MongoClient('mongodb://localhost:27017/')
    # Verificar conexión
    client.admin.command('ismaster')
    print("Conexión exitosa a MongoDB")
    
    try:
        # Intentar operación con posible error de clave duplicada
        result = db.usuarios.insert_one({"email": "usuario@ejemplo.com"})
    except DuplicateKeyError:
        print("Error: El email ya existe en la base de datos")
    
except ConnectionFailure:
    print("Error: No se pudo conectar al servidor MongoDB")
except OperationFailure as e:
    print(f"Error de operación: {e}")
```

## Buenas Prácticas

1. **Manejo de conexiones**:
   - Reutiliza objetos `MongoClient` en tu aplicación.
   - MongoDB maneja internamente un pool de conexiones.
   - Cierra las conexiones explícitamente al terminar tu programa con `client.close()`.

2. **Seguridad**:
   - Nunca incluyas credenciales directamente en el código fuente.
   - Usa variables de entorno o archivos de configuración seguros.
   - Implementa autenticación y SSL/TLS para conexiones.

3. **Rendimiento**:
   - Crea índices para consultas frecuentes.
   - Usa proyecciones para devolver solo campos necesarios.
   - Evita documentos demasiado grandes (>16MB).
   - Utiliza el operador `$exists` con precaución, ya que no aprovecha índices.

4. **Diseño de esquemas**:
   - Prefiere la desnormalización cuando sea apropiado.
   - Almacena datos que se acceden juntos en el mismo documento.
   - Considera las limitaciones de tamaño de documento (16MB).
   - Implementa referencias cuando sea necesario para documentos grandes.

5. **Monitoreo**:
   - Usa `explain()` para analizar el rendimiento de consultas.
   - Configura el registro y monitoreo para operaciones lentas.

## Ejemplo Completo: Sistema de Blog Simple

A continuación, un ejemplo que integra varios conceptos para un sistema de blog simple:

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import pprint

# Configurar cliente de MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.blog_db

# Función para crear un nuevo post
def crear_post(titulo, contenido, autor_id, tags=None):
    post = {
        "titulo": titulo,
        "contenido": contenido,
        "autor_id": autor_id,
        "fecha_creacion": datetime.datetime.now(),
        "comentarios": [],
        "tags": tags or [],
        "visitas": 0
    }
    
    resultado = db.posts.insert_one(post)
    return resultado.inserted_id

# Función para añadir un comentario
def añadir_comentario(post_id, autor, texto):
    comentario = {
        "autor": autor,
        "texto": texto,
        "fecha": datetime.datetime.now()
    }
    
    db.posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comentarios": comentario}}
    )

# Función para buscar posts por tag
def buscar_por_tag(tag):
    return db.posts.find({"tags": tag}).sort("fecha_creacion", -1)

# Función para mostrar estadísticas
def estadisticas_tags():
    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    
    return list(db.posts.aggregate(pipeline))

# Ejecutar ejemplo
if __name__ == "__main__":
    # Crear un autor
    autor_id = db.autores.insert_one({
        "nombre": "Ana García",
        "email": "ana@ejemplo.com",
        "bio": "Escritora y programadora"
    }).inserted_id
    
    # Crear posts
    post_id1 = crear_post(
        "Introducción a MongoDB", 
        "MongoDB es una base de datos NoSQL...",
        autor_id,
        ["mongodb", "nosql", "bases de datos"]
    )
    
    post_id2 = crear_post(
        "Python y MongoDB con PyMongo", 
        "PyMongo es la biblioteca oficial...",
        autor_id,
        ["python", "mongodb", "pymongo"]
    )
    
    # Añadir comentarios
    añadir_comentario(post_id1, "Carlos López", "¡Gran artículo!")
    añadir_comentario(post_id1, "María Rodríguez", "Muy útil, gracias")
    
    # Incrementar visitas
    db.posts.update_one({"_id": ObjectId(post_id1)}, {"$inc": {"visitas": 5}})
    db.posts.update_one({"_id": ObjectId(post_id2)}, {"$inc": {"visitas": 3}})
    
    # Mostrar un post completo
    post = db.posts.find_one({"_id": ObjectId(post_id1)})
    print("\n----- POST -----")
    pprint.pprint(post)
    
    # Mostrar posts con el tag "mongodb"
    print("\n----- POSTS CON TAG 'mongodb' -----")
    for post in buscar_por_tag("mongodb"):
        print(f"{post['titulo']} - {post['fecha_creacion']}")
    
    # Mostrar estadísticas de tags
    print("\n----- ESTADÍSTICAS DE TAGS -----")
    for stat in estadisticas_tags():
        print(f"{stat['_id']}: {stat['count']} posts")

    # Cerrar conexión
    client.close()
```

Este apunte cubre las operaciones fundamentales y avanzadas que puedes realizar con PyMongo para interactuar con MongoDB desde Python, proporcionando ejemplos prácticos para cada sección.