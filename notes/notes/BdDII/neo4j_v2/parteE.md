# Parte E: Performance y Herramientas
*Duración: 2 horas*

## 5.1 Optimización de consultas

### EXPLAIN y PROFILE - Herramientas de análisis
```cypher
// EXPLAIN muestra el plan de ejecución sin ejecutar
EXPLAIN 
MATCH (p:Persona)-[:CONOCE]->(amigo:Persona)
WHERE p.nombre = 'Juan'
RETURN amigo.nombre

// PROFILE ejecuta y muestra estadísticas de rendimiento
PROFILE 
MATCH (p:Persona)-[:CONOCE]->(amigo:Persona)
WHERE p.nombre = 'Juan'
RETURN amigo.nombre
```

### Interpretando los resultados

**Operadores comunes:**
- **NodeByLabelScan**: Escanea todos los nodos con una etiqueta
- **NodeByIndexSeek**: Usa un índice para encontrar nodos (¡BUENO!)
- **Expand**: Navega por relaciones
- **Filter**: Aplica condiciones WHERE
- **Sort**: Ordena resultados
- **Limit**: Limita resultados

**Métricas importantes:**
- **db hits**: Accesos a la base de datos (menor es mejor)
- **rows**: Filas procesadas en cada paso
- **estimated rows**: Estimación del optimizador
- **time**: Tiempo de ejecución en milisegundos

### Ejemplo de análisis de rendimiento
```cypher
// Consulta ineficiente
PROFILE 
MATCH (p:Persona), (producto:Producto)
WHERE p.nombre = 'Ana' AND producto.precio > 100
RETURN p, producto

// Mejora 1: Usar patrones en lugar de producto cartesiano
PROFILE 
MATCH (p:Persona {nombre: 'Ana'})-[:COMPRO]->(producto:Producto)
WHERE producto.precio > 100
RETURN p, producto

// Mejora 2: Filtrar temprano
PROFILE 
MATCH (p:Persona {nombre: 'Ana'})-[:COMPRO]->(producto:Producto {precio: 100})
WHERE producto.precio > 100
RETURN p, producto
```

## 5.2 Índices y constraints

### Tipos de índices en Neo4j

#### 1. Índices de rango (Range indexes)
```cypher
// Crear índice en propiedad simple
CREATE INDEX persona_nombre FOR (p:Persona) ON (p.nombre)

// Crear índice compuesto
CREATE INDEX persona_nombre_edad FOR (p:Persona) ON (p.nombre, p.edad)

// Verificar índices existentes
SHOW INDEXES

// Eliminar índice
DROP INDEX persona_nombre
```

#### 2. Índices de texto completo (Full-text indexes)
```cypher
// Índice de texto completo en múltiples propiedades
CREATE FULLTEXT INDEX busqueda_productos 
FOR (p:Producto) ON EACH [p.nombre, p.descripcion]

// Usar índice de texto completo
CALL db.index.fulltext.queryNodes('busqueda_productos', 'laptop gaming')
YIELD node, score
RETURN node.nombre, node.descripcion, score
ORDER BY score DESC
```

### Constraints - Integridad de datos

#### 1. Uniqueness constraints
```cypher
// Constraint de unicidad
CREATE CONSTRAINT usuario_email_unique 
FOR (u:Usuario) REQUIRE u.email IS UNIQUE

// Constraint compuesto
CREATE CONSTRAINT persona_nombre_documento_unique 
FOR (p:Persona) REQUIRE (p.nombre, p.documento) IS UNIQUE

// Ver constraints existentes
SHOW CONSTRAINTS

// Eliminar constraint
DROP CONSTRAINT usuario_email_unique
```

#### 2. Node property existence constraints (Enterprise)
```cypher
// Requiere que la propiedad exista (Solo Neo4j Enterprise)
CREATE CONSTRAINT persona_nombre_existe 
FOR (p:Persona) REQUIRE p.nombre IS NOT NULL

// Para múltiples propiedades
CREATE CONSTRAINT usuario_datos_completos 
FOR (u:Usuario) REQUIRE (u.nombre, u.email) IS NOT NULL
```

#### 3. Node key constraints (Enterprise)
```cypher
// Combinación de unicidad y existencia
CREATE CONSTRAINT persona_key 
FOR (p:Persona) REQUIRE (p.nombre, p.documento) IS NODE KEY
```

### Mejores prácticas para índices

#### 1. Cuándo crear índices
```cypher
// ✅ Crear índices para propiedades frecuentemente buscadas
CREATE INDEX empleado_id FOR (e:Empleado) ON (e.id)
CREATE INDEX producto_codigo FOR (p:Producto) ON (p.codigo)

// ✅ Índices para propiedades en WHERE, ORDER BY
CREATE INDEX pedido_fecha FOR (p:Pedido) ON (p.fecha)

// ❌ Evitar índices en propiedades que cambian frecuentemente
// ❌ No crear demasiados índices (ralentizan las escrituras)
```

#### 2. Estrategias de indexación
```cypher
// Para consultas por rango
CREATE INDEX producto_precio FOR (p:Producto) ON (p.precio)

// Para búsquedas de texto
CREATE FULLTEXT INDEX articulos_contenido 
FOR (a:Articulo) ON EACH [a.titulo, a.contenido]

// Para consultas geográficas (Neo4j 4.0+)
CREATE INDEX ubicacion_punto FOR (u:Ubicacion) ON (u.coordenadas)
```

## 5.3 Mejores prácticas de rendimiento

### 1. Optimización de patrones de consulta

#### Filtrar temprano y específicamente
```cypher
// ❌ Ineficiente: filtro tardío
MATCH (p:Persona)-[:TRABAJA_EN]->(e:Empresa)-[:UBICADA_EN]->(c:Ciudad)
WHERE p.edad > 30 AND c.nombre = 'Madrid'
RETURN p.nombre

// ✅ Eficiente: filtro temprano
MATCH (c:Ciudad {nombre: 'Madrid'})<-[:UBICADA_EN]-(e:Empresa)<-[:TRABAJA_EN]-(p:Persona)
WHERE p.edad > 30
RETURN p.nombre
```

#### Usar patrones específicos
```cypher
// ❌ Producto cartesiano accidental
MATCH (a:Actor), (p:Pelicula)
WHERE a.nombre = 'Tom Hanks' AND p.año = 2020
RETURN a, p

// ✅ Patrón específico con relación
MATCH (a:Actor {nombre: 'Tom Hanks'})-[:ACTUA_EN]->(p:Pelicula {año: 2020})
RETURN a, p
```

### 2. Optimización de agregaciones

#### Usar WITH para agregaciones intermedias
```cypher
// ✅ Agregar y filtrar eficientemente
MATCH (e:Empleado)-[:TRABAJA_EN]->(d:Departamento)
WITH d, avg(e.salario) as salario_promedio
WHERE salario_promedio > 50000
MATCH (d)<-[:TRABAJA_EN]-(empleado:Empleado)
RETURN d.nombre, salario_promedio, collect(empleado.nombre) as empleados
```

#### Limitar resultados temprano
```cypher
// ✅ LIMIT temprano para consultas exploratorias
MATCH (p:Producto)
WHERE p.precio > 100
RETURN p.nombre, p.precio
ORDER BY p.precio DESC
LIMIT 10
```

### 3. Gestión de memoria

#### Usar PERIODIC COMMIT para grandes cargas de datos
```cypher
// Para importaciones masivas (Legacy syntax)
:auto USING PERIODIC COMMIT 1000
LOAD CSV FROM 'file:///large_dataset.csv' AS row
CREATE (n:Node {property: row.value})

// Sintaxis moderna con transacciones explícitas
:auto
LOAD CSV FROM 'file:///large_dataset.csv' AS row
CALL {
  WITH row
  CREATE (n:Node {property: row.value})
} IN TRANSACTIONS OF 1000 ROWS
```

### 4. Optimización de escrituras

#### Usar MERGE eficientemente
```cypher
// ❌ Ineficiente: múltiples MERGE
MERGE (p:Persona {email: 'ana@email.com'})
MERGE (e:Empresa {nombre: 'TechCorp'})
MERGE (p)-[:TRABAJA_EN]->(e)

// ✅ Eficiente: MERGE con ON CREATE/MATCH
MERGE (p:Persona {email: 'ana@email.com'})
ON CREATE SET p.nombre = 'Ana', p.fecha_creacion = datetime()
WITH p
MERGE (e:Empresa {nombre: 'TechCorp'})
MERGE (p)-[:TRABAJA_EN]->(e)
```

#### Batch operations con UNWIND
```cypher
// Procesar múltiples elementos eficientemente
UNWIND [
  {email: 'ana@email.com', nombre: 'Ana'},
  {email: 'bob@email.com', nombre: 'Bob'},
  {email: 'carla@email.com', nombre: 'Carla'}
] as usuario_data
MERGE (u:Usuario {email: usuario_data.email})
ON CREATE SET u.nombre = usuario_data.nombre
```

## 5.4 Monitoreo y métricas

### Métricas del sistema
```cypher
// Información general del sistema
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Transactions') 
YIELD attributes
RETURN attributes.NumberOfOpenTransactions as transacciones_abiertas

// Estadísticas de la base de datos
CALL db.stats.retrieve('GRAPH COUNTS') YIELD data
RETURN data

// Información sobre índices
CALL db.indexes() YIELD name, state, populationPercent
RETURN name, state, populationPercent
WHERE state <> 'ONLINE'
```

### Consultas lentas y problemáticas
```cypher
// Consultas actualmente ejecutándose (Enterprise)
CALL dbms.listQueries() 
YIELD queryId, query, elapsedTimeMillis, allocatedBytes
WHERE elapsedTimeMillis > 1000
RETURN queryId, query, elapsedTimeMillis
ORDER BY elapsedTimeMillis DESC

// Terminar consulta específica (si es necesario)
CALL dbms.killQuery('query-id-here')
```

### Análisis de tamaño de datos
```cypher
// Contar nodos por etiqueta
MATCH (n) 
RETURN labels(n) as etiquetas, count(n) as cantidad
ORDER BY cantidad DESC

// Contar relaciones por tipo
MATCH ()-[r]->() 
RETURN type(r) as tipo_relacion, count(r) as cantidad
ORDER BY cantidad DESC

// Análisis de propiedades más comunes
MATCH (n:Persona) 
RETURN keys(n) as propiedades, count(*) as frecuencia
ORDER BY frecuencia DESC
```

## 5.5 Ecosistema Neo4j

### Neo4j Desktop - Administración local
**Características principales:**
- Gestión de múltiples proyectos y bases de datos
- Instalación automática de plugins
- Monitoreo de rendimiento
- Gestión de versiones de Neo4j

**Plugins útiles:**
- **APOC**: Procedimientos y funciones extendidas
- **Graph Data Science**: Algoritmos de análisis de grafos
- **Neosemantics**: Importación de datos RDF/OWL

### Neo4j Browser - Interfaz de consultas
```cypher
// Comandos útiles del Browser
:help          // Ayuda general
:clear         // Limpiar pantalla
:history       // Historial de consultas
:param nombre => 'Juan'  // Definir parámetros
:params clear  // Limpiar parámetros

// Guías interactivas
:play intro           // Introducción a Neo4j
:play cypher          // Tutorial de Cypher
:play movie-graph     // Dataset de ejemplo
```

### Neo4j Bloom - Visualización avanzada
**Características:**
- Visualización interactiva sin código
- Exploración natural del grafo
- Búsqueda en lenguaje natural
- Perspectivas personalizables para diferentes usuarios

**Casos de uso:**
- Presentaciones ejecutivas
- Exploración de datos por analistas de negocio
- Investigación de fraude
- Análisis de redes sociales

### APOC - Awesome Procedures on Cypher

#### Instalación y funciones básicas
```cypher
// Verificar instalación de APOC
CALL apoc.help('text')

// Funciones de texto
RETURN apoc.text.capitalize('neo4j') as capitalizado
RETURN apoc.text.slug('Texto con Espacios') as slug

// Funciones de fecha
RETURN apoc.date.format(timestamp(), 'yyyy-MM-dd') as fecha_actual

// Funciones de colección
RETURN apoc.coll.flatten([[1,2], [3,4]]) as lista_plana
```

#### Procedimientos avanzados con APOC
```cypher
// Cargar datos desde API REST
CALL apoc.load.json('https://api.ejemplo.com/datos') 
YIELD value
RETURN value

// Exportar datos
CALL apoc.export.csv.all('todos_los_datos.csv', {})

// Ejecutar Cypher dinámico
CALL apoc.cypher.run('MATCH (n:' + $etiqueta + ') RETURN count(n)', {etiqueta: 'Persona'}) 
YIELD value
RETURN value
```

### Drivers y conexión desde aplicaciones

#### Python con neo4j-driver
```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

# Uso
conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
result = conn.query("MATCH (p:Persona) RETURN p.nombre LIMIT 5")
print(result)
conn.close()
```

#### JavaScript con neo4j-driver
```javascript
const neo4j = require('neo4j-driver');

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'password')
);

async function runQuery() {
  const session = driver.session();
  try {
    const result = await session.run(
      'MATCH (p:Persona) RETURN p.nombre LIMIT 5'
    );
    
    result.records.forEach(record => {
      console.log(record.get('p.nombre'));
    });
  } finally {
    await session.close();
  }
}

runQuery().then(() => driver.close());
```

### Neo4j Aura - Cloud

#### Ventajas de Neo4j Aura
- Configuración automática y mantenimiento
- Escalabilidad automática
- Copias de seguridad automáticas
- Seguridad empresarial
- Disponibilidad global

#### Conectarse a Aura
```cypher
// Configuración típica para Aura
URI: neo4j+s://xxxxx.databases.neo4j.io
Usuario: neo4j
Contraseña: [contraseña generada]

// Verificar conexión
CALL db.ping() YIELD bolt
RETURN bolt
```

## 5.6 Laboratorio práctico: Optimización completa

### Escenario: E-commerce con problemas de rendimiento

```cypher
// 1. Crear dataset de prueba con muchos datos
UNWIND range(1, 10000) as userId
CREATE (u:Usuario {
  id: userId, 
  nombre: 'Usuario' + userId, 
  email: 'user' + userId + '@email.com',
  fecha_registro: date('2020-01-01') + duration({days: userId % 365})
})

UNWIND range(1, 5000) as prodId  
CREATE (p:Producto {
  id: prodId,
  nombre: 'Producto' + prodId,
  precio: toFloat(10 + (prodId % 1000)),
  categoria: ['Electrónica', 'Ropa', 'Hogar', 'Libros'][prodId % 4],
  stock: prodId % 100
})

// Crear relaciones de compra (esto será lento sin índices)
MATCH (u:Usuario), (p:Producto)
WHERE u.id <= 1000 AND p.id <= 1000 AND rand() < 0.01
CREATE (u)-[:COMPRO {
  fecha: date('2023-01-01') + duration({days: toInteger(rand() * 300)}),
  cantidad: toInteger(1 + rand() * 5),
  precio_pagado: p.precio * (0.8 + rand() * 0.4)
}]->(p)
```

### Análisis de rendimiento inicial
```cypher
// Consulta problemática sin índices
PROFILE 
MATCH (u:Usuario)-[c:COMPRO]->(p:Producto)
WHERE u.email = 'user500@email.com' 
  AND p.categoria = 'Electrónica'
  AND c.fecha > date('2023-06-01')
RETURN u.nombre, p.nombre, c.fecha, c.precio_pagado
ORDER BY c.fecha DESC
```

### Optimización paso a paso

#### Paso 1: Crear índices necesarios
```cypher
// Índices para propiedades frecuentemente consultadas
CREATE INDEX usuario_email FOR (u:Usuario) ON (u.email)
CREATE INDEX producto_categoria FOR (p:Producto) ON (p.categoria)
CREATE INDEX compra_fecha FOR ()-[c:COMPRO]-() ON (c.fecha)

// Verificar mejora
PROFILE 
MATCH (u:Usuario {email: 'user500@email.com'})-[c:COMPRO]->(p:Producto {categoria: 'Electrónica'})
WHERE c.fecha > date('2023-06-01')
RETURN u.nombre, p.nombre, c.fecha, c.precio_pagado
ORDER BY c.fecha DESC
```

#### Paso 2: Optimizar consultas de agregación
```cypher
// Consulta: Top productos por ventas
PROFILE 
MATCH (p:Producto)<-[c:COMPRO]-(u:Usuario)
WHERE c.fecha > date('2023-01-01')
WITH p, sum(c.cantidad * c.precio_pagado) as ingresos_totales, count(c) as total_compras
RETURN p.nombre, p.categoria, ingresos_totales, total_compras
ORDER BY ingresos_totales DESC
LIMIT 10
```

#### Paso 3: Crear vistas materializadas (usando nodos de agregación)
```cypher
// Crear nodos de métricas para consultas frecuentes
MATCH (p:Producto)<-[c:COMPRO]-()
WHERE c.fecha >= date('2023-01-01') AND c.fecha < date('2024-01-01')
WITH p, 
     sum(c.cantidad * c.precio_pagado) as ingresos_anuales,
     count(c) as compras_anuales,
     sum(c.cantidad) as unidades_vendidas
MERGE (m:MetricaProducto {producto_id: p.id, año: 2023})
SET m.ingresos = ingresos_anuales,
    m.compras = compras_anuales,
    m.unidades = unidades_vendidas,
    m.fecha_actualizacion = datetime()
MERGE (p)-[:TIENE_METRICAS]->(m)

// Consulta optimizada usando métricas precalculadas
MATCH (p:Producto)-[:TIENE_METRICAS]->(m:MetricaProducto {año: 2023})
RETURN p.nombre, p.categoria, m.ingresos, m.compras, m.unidades
ORDER BY m.ingresos DESC
LIMIT 10
```

### Monitoreo continuo
```cypher
// Script de monitoreo para ejecutar periódicamente
MATCH (n) 
WITH labels(n) as etiquetas, count(n) as cantidad
RETURN etiquetas, cantidad, 
       datetime() as timestamp_reporte
ORDER BY cantidad DESC

// Verificar salud de índices
CALL db.indexes() 
YIELD name, state, populationPercent, type
WHERE state <> 'ONLINE' OR populationPercent < 100
RETURN name, state, populationPercent, type
```

## 5.7 Ejercicios de optimización

### Ejercicio 1: Análisis de consultas lentas
Dada esta consulta problemática:
```cypher
MATCH (u:Usuario)-[:AMIGO_DE*2..4]-(amigo_remoto:Usuario)
WHERE u.ciudad = 'Madrid' 
  AND amigo_remoto.profesion = 'Ingeniero'
  AND NOT (u)-[:AMIGO_DE]-(amigo_remoto)
RETURN DISTINCT u.nombre, amigo_remoto.nombre, 
       length(path) as grados_separacion
ORDER BY grados_separacion
LIMIT 20
```

**Tareas:**
1. Usar PROFILE para analizar el rendimiento
2. Identificar cuáles índices mejorarían la consulta
3. Reescribir la consulta para mejor rendimiento
4. Comparar los resultados antes y después

### Ejercicio 2: Optimización de sistema de recomendaciones
```cypher
// Sistema de recomendación colaborativa
MATCH (usuario:Usuario {id: 123})-[:VALORO]->(producto:Producto)<-[:VALORO {puntuacion: 4..5}]-(otro_usuario:Usuario)
MATCH (otro_usuario)-[:VALORO {puntuacion: 4..5}]->(recomendacion:Producto)
WHERE NOT (usuario)-[:VALORO]->(recomendacion)
WITH recomendacion, count(*) as recomendadores, avg(v.puntuacion) as valoracion_promedio
ORDER BY recomendadores DESC, valoracion_promedio DESC
RETURN recomendacion.nombre, recomendadores, valoracion_promedio
LIMIT 10
```

**Tareas:**
1. Optimizar esta consulta de recomendaciones
2. Crear índices apropiados
3. Considerar crear nodos de métricas precalculadas
4. Implementar versión para actualización incremental

## 5.8 Despliegue en producción

### Configuración básica de Neo4j
```bash
# neo4j.conf - Configuraciones importantes
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=2G
dbms.memory.pagecache.size=4G

# Configuración de seguridad
dbms.default_listen_address=0.0.0.0
dbms.connector.bolt.listen_address=:7687
dbms.connector.http.listen_address=:7474

# Configuración de logs
dbms.logs.query.enabled=true
dbms.logs.query.threshold=1000ms
```

### Copias de seguridad
```bash
# Backup completo (Neo4j Enterprise)
neo4j-admin dump --database=neo4j --to=/backups/neo4j-backup.dump

# Restaurar desde backup
neo4j-admin load --from=/backups/neo4j-backup.dump --database=neo4j --force
```

### Estrategias de escalabilidad

#### 1. Escalamiento vertical
- Incrementar memoria RAM
- Usar SSDs rápidos
- CPUs con más cores

#### 2. Escalamiento horizontal (Enterprise)
- **Causal Clustering**: Réplicas de lectura
- **Fabric**: Federación de múltiples bases de datos
- **Sharding**: Distribución de datos por dominios

### Monitoreo en producción
```cypher
// Métricas clave para monitorear
CALL dbms.queryJmx('*:*') YIELD name, attributes
WHERE name CONTAINS 'memory' OR name CONTAINS 'transaction'
RETURN name, attributes.HeapMemoryUsage, attributes.NumberOfOpenTransactions
```

### Próximos pasos recomendados:

1. **Práctica continua**: Implementar proyectos personales
2. **Neo4j GraphAcademy**: Cursos especializados gratuitos
3. **Certificación**: Neo4j Certified Professional
4. **Comunidad**: Unirse a foros y meetups de Neo4j
5. **Especialización**: Graph Data Science, ML en grafos

### Recursos para seguir aprendiendo:
- **Documentación oficial**: https://neo4j.com/docs/
- **GraphAcademy**: https://graphacademy.neo4j.com/
- **Blog de Neo4j**: https://neo4j.com/developer-blog/
- **Comunidad**: https://community.neo4j.com/
- **GitHub**: Ejemplos y proyectos opensource

