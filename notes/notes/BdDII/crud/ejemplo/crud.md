```python
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

# Paso 1: Conectar a MongoDB
def get_database():
    # Crear una conexión utilizando MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    
    # Obtener/crear una base de datos llamada 'empresa'
    db = client['empresa']
    return db

# ------------------ CREATE ------------------
def crear_empleado(empleados_collection):
    # Definir un nuevo documento (registro)
    nuevo_empleado = {
        "nombre": "Ana García",
        "email": "ana.garcia@ejemplo.com",
        "edad": 28,
        "puesto": "Desarrollador Python",
        "fecha_contratacion": datetime.datetime.now(),
        "habilidades": ["Python", "MongoDB", "Flask"]
    }
    
    # Insertar el documento en la colección
    resultado = empleados_collection.insert_one(nuevo_empleado)
    
    # Devolver el ID del nuevo documento
    print(f"Empleado creado con ID: {resultado.inserted_id}")
    return resultado.inserted_id

# ------------------ READ ------------------
def leer_empleados(empleados_collection):
    # Obtener todos los empleados
    print("\nTodos los empleados:")
    for empleado in empleados_collection.find():
        print(f"ID: {empleado['_id']}, Nombre: {empleado['nombre']}, Puesto: {empleado['puesto']}")
    
    # Buscar un empleado específico por nombre
    print("\nBuscar por nombre:")
    empleado = empleados_collection.find_one({"nombre": "Ana García"})
    if empleado:
        print(f"Encontrado: {empleado['nombre']}, Email: {empleado['email']}")
    else:
        print("Empleado no encontrado")
    
    # Buscar empleados por criterio (ejemplo: mayores de 25 años)
    print("\nEmpleados mayores de 25 años:")
    query = {"edad": {"$gt": 25}}
    for empleado in empleados_collection.find(query):
        print(f"Nombre: {empleado['nombre']}, Edad: {empleado['edad']}")

# ------------------ UPDATE ------------------
def actualizar_empleado(empleado_id, empleados_collection):
    # Actualizar un solo campo
    filtro = {"_id": ObjectId(empleado_id, )}
    nueva_info = {"$set": {"edad": 29}}
    
    resultado = empleados_collection.update_one(filtro, nueva_info)
    print(f"\nEmpleado actualizado: {resultado.modified_count} documento(s) modificado(s)")
    
    # Actualizar múltiples campos
    nueva_info_multiple = {
        "$set": {
            "puesto": "Desarrollador Senior Python",
            "habilidades": ["Python", "MongoDB", "Flask", "FastAPI"]
        }
    }
    
    resultado = empleados_collection.update_one(filtro, nueva_info_multiple)
    print(f"Información actualizada: {resultado.modified_count} documento(s) modificado(s)")
    
    # Verificar la actualización
    empleado_actualizado = empleados_collection.find_one(filtro)
    print(f"Empleado actualizado: {empleado_actualizado['nombre']}, Puesto: {empleado_actualizado['puesto']}")

# ------------------ DELETE ------------------
def eliminar_empleado(empleado_id, empleados_collection):
    # Eliminar un solo documento
    filtro = {"_id": ObjectId(empleado_id)}
    resultado = empleados_collection.delete_one(filtro)
    
    print(f"\nEmpleado eliminado: {resultado.deleted_count} documento(s) eliminado(s)")
    
    # Podríamos también eliminar múltiples documentos
    # Por ejemplo, eliminar todos los empleados con edad > 60
    # resultado = empleados_collection.delete_many({"edad": {"$gt": 60}})

# ------------------ EJECUTAR OPERACIONES ------------------
def main():
    # Obtener la base de datos
    db = get_database()

    # Obtener una colección (equivalente a una tabla en BD relacionales)
    empleados_collection = db['empleados']
    # Crear un nuevo empleado y obtener su ID
    empleado_id = crear_empleado(empleados_collection)
    
    # Leer empleados
    leer_empleados(empleados_collection)
    
    # Actualizar el empleado recién creado
    actualizar_empleado(empleado_id, empleados_collection)
    
    # Eliminar el empleado
    eliminar_empleado(empleado_id, empleados_collection)
    
    # Verificar que se haya eliminado
    print("\nVerificar después de eliminar:")
    empleado = empleados_collection.find_one({"_id": ObjectId(empleado_id)})
    if empleado:
        print(f"El empleado aún existe: {empleado['nombre']}")
    else:
        print("El empleado ha sido eliminado correctamente")

if __name__ == "__main__":
    main()
```