# Parte A: Fundamentos de Neo4j

## 1.1 ¿Qué son las bases de datos de grafos?

### Definición
Una base de datos de grafos es un sistema de gestión de bases de datos que utiliza estructuras de grafos para representar y almacenar datos. Los datos se organizan como nodos (entidades) conectados por aristas (relaciones).

### Componentes básicos
- **Nodos**: Representan entidades (personas, productos, lugares)
- **Relaciones**: Conexiones direccionales entre nodos
- **Propiedades**: Atributos tanto de nodos como de relaciones

### Diferencias con bases de datos relacionales

| Aspecto | Base de Datos Relacional | Base de Datos de Grafos |
|---------|-------------------------|------------------------|
| Estructura | Tablas con filas y columnas | Nodos y relaciones |
| Relaciones | Foreign keys, JOINs | Relaciones directas |
| Consultas complejas | Múltiples JOINs costosos | Traversal natural |
| Esquema | Rígido | Flexible |
| Escalabilidad | Vertical principalmente | Horizontal para relaciones |

### Ejemplo práctico: Red Social

**Modelo Relacional:**
```sql
-- Tabla usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR(100)
);

-- Tabla amistades
CREATE TABLE amistades (
    usuario1_id INT,
    usuario2_id INT,
    fecha_amistad DATE,
    FOREIGN KEY (usuario1_id) REFERENCES usuarios(id),
    FOREIGN KEY (usuario2_id) REFERENCES usuarios(id)
);

-- Consulta: Amigos de amigos
SELECT DISTINCT u3.nombre
FROM usuarios u1
JOIN amistades a1 ON u1.id = a1.usuario1_id
JOIN usuarios u2 ON a1.usuario2_id = u2.id
JOIN amistades a2 ON u2.id = a2.usuario1_id
JOIN usuarios u3 ON a2.usuario2_id = u3.id
WHERE u1.nombre = 'Juan' AND u3.id != u1.id;
```

**Modelo de Grafos (Neo4j):**
Ejemplo:
```cypher
// Crear nodos
CREATE (juan:Persona {nombre: 'Juan', email: 'juan@email.com'});
CREATE (maria:Persona {nombre: 'María', email: 'maria@email.com'});
CREATE (carlos:Persona {nombre: 'Carlos', email: 'carlos@email.com'});

// Crear relaciones
MATCH (juan:Persona {nombre: 'Juan'})
MATCH (maria:Persona {nombre: 'María'})
MATCH (carlos:Persona {nombre: 'Carlos'})
CREATE (juan)-[:AMIGO_DE {desde: '2023-01-15'}]->(maria),
       (maria)-[:AMIGO_DE {desde: '2023-02-10'}]->(carlos);

// Consulta: Amigos de amigos
MATCH (juan:Persona {nombre: 'Juan'})-[:AMIGO_DE]->()-[:AMIGO_DE]->(amigo_de_amigo)
RETURN amigo_de_amigo.nombre;
```
Mismo ejemplo de arriba, pero con una creación de nodos y relaciones más compacta:
```cypher
// Crear nodos y relaciones
CREATE 
  (juan:Persona {nombre: 'Juan', email: 'juan@email.com'}),
  (maria:Persona {nombre: 'María', email: 'maria@email.com'}),
  (carlos:Persona {nombre: 'Carlos', email: 'carlos@email.com'}),
  (juan)-[:AMIGO_DE {desde: '2023-01-15'}]->(maria),
  (maria)-[:AMIGO_DE {desde: '2023-02-10'}]->(carlos);

// Consulta: Amigos de amigos
MATCH (juan:Persona {nombre: 'Juan'})-[:AMIGO_DE]->()-[:AMIGO_DE]->(amigo_de_amigo)
RETURN amigo_de_amigo.nombre;
```

## 1.2 Casos de uso ideales

### 1. Redes Sociales
- **Problema**: Encontrar conexiones, sugerir amigos, analizar influencia
- **Ventaja**: Navegación natural por relaciones sociales
- **Ejemplo**: "Personas que podrías conocer" en Facebook

### 2. Sistemas de Recomendación
- **Problema**: Recomendar productos basados en comportamiento similar
- **Ventaja**: Análisis de patrones complejos de comportamiento
- **Ejemplo**: Amazon, Netflix, Spotify

```cypher
// Ejemplo: Recomendación de productos
MATCH (usuario:Usuario {nombre: 'Ana'})-[:COMPRO]->(producto)<-[:COMPRO]-(otros:Usuario)
MATCH (otros)-[:COMPRO]->(recomendacion)
WHERE NOT (usuario)-[:COMPRO]->(recomendacion)
RETURN recomendacion.nombre, COUNT(*) as popularidad
ORDER BY popularidad DESC
LIMIT 5
```

### 3. Detección de Fraude
- **Problema**: Identificar patrones sospechosos en transacciones
- **Ventaja**: Análisis de redes complejas de transacciones
- **Ejemplo**: Detección de lavado de dinero

### 4. Gestión de Conocimiento
- **Problema**: Mapear relaciones entre conceptos y documentos
- **Ventaja**: Navegación semántica del conocimiento
- **Ejemplo**: Grafos de conocimiento empresarial

### 5. Análisis de Dependencias
- **Problema**: Mapear dependencias en software o infraestructura
- **Ventaja**: Análisis de impacto y dependencias circulares
- **Ejemplo**: Microservicios, análisis de impacto

## 1.3 Introducción a Neo4j

### ¿Qué es Neo4j?
Neo4j es la base de datos de grafos más popular del mundo, desarrollada en Java y disponible tanto en versión Community (gratuita) como Enterprise (comercial).

### Características principales
- **ACID compliant**: Garantiza la integridad de las transacciones
- **Cypher**: Lenguaje de consulta declarativo específico para grafos
- **Escalabilidad**: Soporta billones de nodos y relaciones
- **Alto rendimiento**: Consultas en tiempo real sobre grafos complejos
- **Herramientas visuales**: Neo4j Browser y Neo4j Bloom

### Arquitectura de Neo4j

```
┌─────────────────┐
│   Aplicación    │
└─────────┬───────┘
          │
┌─────────▼───────┐
│   Driver API    │ (Bolt Protocol)
└─────────┬───────┘
          │
┌─────────▼───────┐
│   Neo4j Core    │
├─────────────────┤
│ Cypher Engine   │
├─────────────────┤
│ Transaction Log │
├─────────────────┤
│  Storage Engine │
└─────────────────┘
```

## 1.4 Instalación y configuración inicial

### Opción 1: Neo4j Desktop (Recomendada para desarrollo)

1. **Descargar Neo4j Desktop**

   - Ir a https://neo4j.com/download/
   - Registrarse y descargar Neo4j Desktop
   - Instalar siguiendo el asistente

2. **Crear primer proyecto**
   ```
   1. Abrir Neo4j Desktop
   2. Crear nuevo proyecto: "Curso Neo4j"
   3. Agregar base de datos local
   4. Configurar nombre: "mi-primera-bd"
   5. Establecer contraseña para usuario 'neo4j'
   6. Iniciar la base de datos
   ```

3. **Acceder a Neo4j Browser**
   - Hacer clic en "Open" junto a la base de datos
   - Se abrirá Neo4j Browser en el navegador

### Opción 2: Neo4j Aura (Cloud)

1. **Crear cuenta gratuita**
   - Ir a https://neo4j.com/cloud/aura/
   - Registrarse con email
   - Crear instancia gratuita

2. **Configurar conexión**
   ```
   URI: neo4j+s://xxxxxxx.databases.neo4j.io
   Usuario: neo4j
   Contraseña: [tu contraseña generada]
   ```

### Opción 3: Docker (Para usuarios avanzados)

```bash
# Ejecutar Neo4j en Docker
docker run \
    --name neo4j-curso \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/password123 \
    neo4j:latest
```

## 1.5 Neo4j Desktop vs Neo4j Browser

### Neo4j Desktop
- **Función**: Administrador local de instancias Neo4j
- **Ventajas**: 
  - Gestión múltiples bases de datos
  - Instalación de plugins
  - Gestión de versiones
  - Monitoreo de rendimiento
- **Uso**: Desarrollo local, experimentación

### Neo4j Browser
- **Función**: Interfaz web para consultas e visualización
- **Ventajas**:
  - Interfaz intuitiva
  - Visualización de grafos
  - Historial de consultas
  - Guías interactivas
- **Uso**: Consultas, exploración, presentaciones

## 1.6 Primeros pasos en Neo4j Browser

### Conectarse a la base de datos
```cypher
// Verificar conexión
CALL db.ping()
```

### Comandos básicos del Browser
```cypher
// Limpiar el área de trabajo
:clear

// Ayuda general
:help

// Listar comandos disponibles
:help commands

// Ver configuración actual
:sysinfo

// Cambiar tema visual
:style reset
```

### Tu primera consulta
```cypher
// Crear tu primer nodo
CREATE (yo:Persona {nombre: 'Tu Nombre', profesion: 'Estudiante Neo4j'})

// Ver lo que creaste
MATCH (n:Persona) RETURN n

// Limpiar cuando termines
MATCH (n) DELETE n
```

## Ejercicios Prácticos

### Ejercicio 1: Exploración del Browser
1. Conectarse a Neo4j Browser
2. Ejecutar `:play intro` para ver la guía interactiva
3. Completar al menos los primeros 3 slides
4. Experimentar con los diferentes paneles del Browser

### Ejercicio 2: Comparación de modelos
1. Diseñar un modelo relacional simple para una biblioteca (libros, autores, préstamos)
2. Diseñar el mismo modelo como grafo
3. Escribir la consulta SQL y Cypher para "encontrar todos los libros prestados por usuarios de una ciudad específica"
4. Comparar la complejidad de ambas consultas

### Ejercicio 3: Casos de uso
1. Identificar 3 problemas en tu trabajo/estudios que podrían beneficiarse de una base de datos de grafos
2. Para cada problema, describir:
   - ¿Qué entidades principales existen?
   - ¿Qué relaciones hay entre ellas?
   - ¿Por qué un grafo sería mejor que una base relacional?

## Recursos adicionales

- **Documentación oficial**: https://neo4j.com/docs/
- **Neo4j GraphAcademy**: https://graphacademy.neo4j.com/
- **Comunidad**: https://community.neo4j.com/
- **Datasets de práctica**: https://neo4j.com/developer/example-data/

## Resumen

En esta parte hemos cubierto:

- ✅ Conceptos fundamentales de bases de datos de grafos
- ✅ Diferencias con bases de datos relacionales
- ✅ Casos de uso ideales para Neo4j
- ✅ Instalación y configuración de Neo4j
- ✅ Familiarización con Neo4j Browser

