# Guía de Instalación de MongoDB y PyMongo en Ubuntu

## 1. Instalación de MongoDB

### Paso 1: Importar la clave pública de MongoDB
```bash
sudo apt-get install gnupg curl

curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
```

### Paso 2: Crear el archivo de lista para MongoDB
```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

### Paso 3: Actualizar la lista de paquetes local
```bash
sudo apt-get update
```

### Paso 4: Instalar MongoDB
```bash
sudo apt-get install -y mongodb-org
```

### Paso 5: Iniciar MongoDB
```bash
sudo systemctl start mongod
```

### Paso 6: Verificar que MongoDB se ha iniciado correctamente
```bash
sudo systemctl status mongod
```

### Paso 7: Habilitar MongoDB para que se inicie automáticamente al reiniciar el sistema
```bash
sudo systemctl enable mongod
```

## 2. Instalación de PyMongo

### Paso 1: Instalar pip (si aún no está instalado)
```bash
sudo apt-get install -y python3-pip
```

### Paso 2: Instalar PyMongo
```bash
pip3 install pymongo
```

### Paso 3: Verificar la instalación
```python
python3 -c "import pymongo; print(pymongo.__version__)"
```

## 3. Ejemplo básico de uso de PyMongo

```python
from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient('localhost', 27017)

# Crear o acceder a una base de datos
db = client['mi_base_de_datos']

# Crear o acceder a una colección
coleccion = db['mi_coleccion']

# Insertar un documento
documento = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"}
resultado = coleccion.insert_one(documento)
print(f"ID del documento insertado: {resultado.inserted_id}")

# Consultar documentos
for doc in coleccion.find():
    print(doc)

# Cerrar la conexión
client.close()
```

## 4. Solución de problemas comunes

### MongoDB no inicia
Si MongoDB no inicia correctamente, revisar los logs:
```bash
sudo cat /var/log/mongodb/mongod.log
```

### Problemas de permisos
Si hay problemas con los permisos del directorio de datos:
```bash
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chmod 0755 /var/lib/mongodb
```

### Reiniciar MongoDB
```bash
sudo systemctl restart mongod
```

## 5. Comandos útiles de MongoDB

### Acceder a la shell de MongoDB
```bash
mongosh
```

### Listar bases de datos
```
show dbs
```

### Usar una base de datos
```
use mi_base_de_datos
```

### Listar colecciones
```
show collections
```

### Salir de la shell
```
exit
```

## 6. Recursos adicionales

- [Documentación oficial de MongoDB](https://docs.mongodb.com/)
- [Documentación de PyMongo](https://pymongo.readthedocs.io/)
- [Tutorial de MongoDB University](https://university.mongodb.com/)