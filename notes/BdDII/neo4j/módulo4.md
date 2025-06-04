# Módulo 4: Funciones y Operaciones Avanzadas

## 1. Manipulación de Cadenas, Números y Listas

### Funciones para Manipulación de Cadenas

Neo4j proporciona un conjunto completo de funciones para trabajar con valores de tipo string. Estas funciones son útiles para formatear, extraer y modificar datos textuales.

#### Funciones básicas de cadenas:

```cypher
// Concatenación
RETURN "Hello" + " " + "World" AS greeting

// Longitud de una cadena
RETURN size("Neo4j") AS length  // Devuelve 5

// Conversión a mayúsculas/minúsculas
RETURN toUpper("neo4j") AS uppercase,  // Devuelve "NEO4J"
       toLower("NEO4J") AS lowercase   // Devuelve "neo4j"

// Extraer subcadenas
RETURN substring("Hello World", 6, 5) AS result  // Devuelve "World"

// Reemplazo de texto
RETURN replace("Hello World", "World", "Neo4j") AS result  // Devuelve "Hello Neo4j"
```

#### Funciones de búsqueda y coincidencia:

```cypher
// Comprobar si una cadena comienza o termina con cierto texto
RETURN 
  "Neo4j"  STARTS WITH "Neo" AS starts_with_neo,  // true
  "Neo4j" ENDS WITH "4j" AS ends_with_4j,         // true
  "Neo4j" CONTAINS "o4" AS contains_o4            // true

// Buscar la posición de una subcadena (índice base 0)
RETURN 
  indexOf("Neo4j", "4") AS index_of_4  // Devuelve 3
```

#### Expresiones regulares:

```cypher
// Comprobar si una cadena coincide con un patrón
MATCH (p:Person)
WHERE p.email =~ ".*@gmail\\.com"
RETURN p.name, p.email

// Extraer partes usando grupos de captura
MATCH (p:Person)
WHERE p.name =~ "(Mr|Mrs|Ms)\\.? (.+)"
RETURN p.name, split(p.name, " ")[0] AS title, split(p.name, " ")[1] AS name
```

#### Formateo de cadenas:

```cypher
// Formato de texto
RETURN 
  toString(42) AS string_value,                 // "42"
  toString(date()) AS today,                    // "2023-05-17"
  toString(datetime()) AS now,                  // "2023-05-17T10:15:30.000000000Z"
  toString(3.14159, "#.##") AS formatted_float  // "3.14"
```

### Funciones para Manipulación de Números

Neo4j ofrece una variedad de funciones matemáticas para manipular valores numéricos.

#### Funciones matemáticas básicas:

```cypher
// Operaciones aritméticas
RETURN 
  1 + 2 AS addition,      // 3
  5 - 2 AS subtraction,   // 3
  3 * 4 AS multiplication,// 12
  10 / 2 AS division,     // 5
  10 % 3 AS modulo        // 1 (resto de la división)

// Redondeo
RETURN 
  round(3.14159) AS rounded,      // 3
  floor(3.14159) AS floor_value,  // 3 (redondeo hacia abajo)
  ceil(3.14159) AS ceil_value     // 4 (redondeo hacia arriba)

// Funciones matemáticas avanzadas
RETURN 
  abs(-42) AS absolute_value,     // 42
  sign(-25) AS sign_value,        // -1 (devuelve -1, 0 o 1)
  sqrt(16) AS square_root,        // 4
  log10(100) AS log_base_10,      // 2
  exp(1) AS e_power_1,            // 2.718281828459045 (valor de e^1)
  pi() AS pi_value                // 3.141592653589793
```

#### Funciones trigonométricas:

```cypher
// Funciones trigonométricas (los ángulos se expresan en radianes)
RETURN 
  sin(radians(30)) AS sine,           // 0.5
  cos(radians(60)) AS cosine,         // 0.5
  tan(radians(45)) AS tangent,        // 1.0
  degrees(asin(0.5)) AS arc_sine_deg  // 30.0
```

#### Funciones aleatorias:

```cypher
// Generar números aleatorios
RETURN 
  rand() AS random0to1,              // Número aleatorio entre 0 y 1
  rand() * 100 AS random0to100,      // Número aleatorio entre 0 y 100
  round(rand() * 10) AS random0to10  // Entero aleatorio entre 0 y 10

// Ejemplo: crear nodos con valores aleatorios
UNWIND range(1, 5) AS id
CREATE (p:Product {
  id: id,
  name: "Product " + id,
  price: round(rand() * 100 * 100) / 100  // Precio aleatorio hasta 100 con 2 decimales
})
```

### Funciones para Manipulación de Listas

Las listas en Neo4j son colecciones ordenadas de valores que pueden ser manipuladas con diversas funciones.

#### Creación y acceso a listas:

```cypher
// Crear una lista literal
RETURN [1, 2, 3, 4, 5] AS list_of_integers

// Función range para crear secuencias
RETURN range(1, 5) AS simple_range,           // [1, 2, 3, 4, 5]
       range(0, 10, 2) AS range_with_step     // [0, 2, 4, 6, 8, 10]

// Acceso a elementos (índice base 0)
RETURN [1, 2, 3, 4, 5][0] AS first_element,   // 1
       [1, 2, 3, 4, 5][-1] AS last_element,   // 5
       [1, 2, 3, 4, 5][2] AS third_element    // 3

// Slicing de listas
RETURN [1, 2, 3, 4, 5][1..3] AS slice         // [2, 3]
```

#### Funciones de lista:

```cypher
// Tamaño de la lista
RETURN size([1, 2, 3]) AS list_size   // 3

// Verificar si un elemento está en la lista
RETURN 
  3 IN [1, 2, 3, 4] AS contains_3,    // true
  5 IN [1, 2, 3, 4] AS contains_5     // false

// Operaciones con listas
RETURN 
  [1, 2] + [3, 4] AS concatenated,     // [1, 2, 3, 4]
  [1, 2, 3] + 4 AS appended,           // [1, 2, 3, 4]
  reverse([1, 2, 3]) AS reversed       // [3, 2, 1]
```

#### Funciones de agregación con listas:

```cypher
// Lista de valores
WITH [3, 1, 4, 1, 5, 9, 2, 6] AS numbers
RETURN 
  min(numbers) AS min_value,           // 1
  max(numbers) AS max_value,           // 9
  avg(numbers) AS average,             // 3.875
  sum(numbers) AS total                // 31
```

#### Funciones de transformación de listas:

```cypher
// Crear lista a partir de resultados
MATCH (p:Person)
RETURN collect(p.name) AS all_names

// Transformación de lista mediante comprensión de lista
WITH [1, 2, 3, 4, 5] AS numbers
RETURN [x IN numbers WHERE x % 2 = 0 | x * 10] AS even_times_ten  // [20, 40]

// Unwind para desarmar una lista en filas
WITH [1, 2, 3] AS numbers
UNWIND numbers AS number
RETURN number  // Devuelve 3 filas con valores 1, 2 y 3
```

#### Ejemplo práctico con listas:

```cypher
// Crear usuarios con una lista de intereses
CREATE (alice:User {name: "Alice", interests: ["music", "sports", "cooking"]})
CREATE (bob:User {name: "Bob", interests: ["sports", "technology", "movies"]})
CREATE (charlie:User {name: "Charlie", interests: ["sports", "cooking", "travel"]})

// Encontrar usuarios con intereses comunes
MATCH (u1:User {name: "Alice"}), (u2:User)
WHERE u1 <> u2
WITH u1, u2, [x IN u1.interests WHERE x IN u2.interests] AS common_interests
WHERE size(common_interests) > 0
RETURN u1.name, u2.name, common_interests, size(common_interests) AS num_common
ORDER BY num_common DESC
```

## 2. APOC: Biblioteca de Procedimientos y Funciones Extendidas

### Introducción a APOC

APOC (Awesome Procedures On Cypher) es una biblioteca de extensión para Neo4j que proporciona cientos de procedimientos y funciones adicionales para ampliar las capacidades de Cypher. APOC facilita muchas operaciones comunes y complejas que no están disponibles en el núcleo de Neo4j.

#### Instalación de APOC:

- **En Neo4j Desktop**: 
  1. Abrir la base de datos deseada
  2. Clic en "Plugins"
  3. Instalar APOC desde el Marketplace

- **En Neo4j Server**:
  1. Descargar el JAR de APOC correspondiente a tu versión de Neo4j desde GitHub
  2. Colocar el archivo JAR en la carpeta plugins de Neo4j
  3. Configurar `apoc.export.file.enabled=true` en neo4j.conf (si se necesita exportación de archivos)
  4. Reiniciar Neo4j

#### Verificación de la instalación:

```cypher
// Listar todos los procedimientos de APOC disponibles
CALL apoc.help("apoc")
```

### Funciones Básicas de APOC

#### Manipulación de texto:

```cypher
// Funciones para texto
RETURN 
  apoc.text.capitalize("hello world") AS capitalized,     // "Hello world"
  apoc.text.camelCase("hello world") AS camel_case,       // "helloWorld"
  apoc.text.clean("Hello, World!") AS cleaned,            // "HelloWorld"
  apoc.text.distance("neo4j", "neo5j") AS edit_distance   // 1 (distancia de Levenshtein)
```

#### Manipulación de colecciones:

```cypher
// Operaciones sobre listas
WITH [1, 2, 3, 4, 5] AS list
RETURN 
  apoc.coll.sum(list) AS sum,                        // 15
  apoc.coll.avg(list) AS avg,                        // 3.0
  apoc.coll.contains(list, 3) AS contains_3,         // true
  apoc.coll.duplicates(list + [1, 3]) AS duplicates, // [1, 3]
  apoc.coll.shuffle(list) AS shuffled,               // Orden aleatorio
  apoc.coll.sortNodes([n IN list | {value: n}], 'value') AS sorted_nodes // Ordenar objetos por propiedad
```

#### Manipulación de mapas:

```cypher
// Funciones para mapas (objetos)
WITH {name: "Alice", age: 30, city: "New York"} AS person
RETURN 
  apoc.map.get(person, "name", "Unknown") AS name_with_default,  // "Alice"
  apoc.map.submap(person, ["name", "city"]) AS name_and_city,   // {name: "Alice", city: "New York"}
  apoc.map.fromPairs([["name", "Bob"], ["age", 25]]) AS map_from_pairs // {name: "Bob", age: 25}
```

#### Conversión de datos:

```cypher
// Conversión entre formatos
RETURN 
  apoc.convert.toJson({name: "Alice", age: 30}) AS json_string,           // '{"name":"Alice","age":30}'
  apoc.convert.fromJsonMap('{"name":"Bob","age":25}') AS map_from_json,   // {name: "Bob", age: 25}
  apoc.convert.toBoolean("true") AS bool_value,                           // true
  apoc.convert.toString(42) AS string_value                               // "42"
```

### Procedimientos Avanzados de APOC

#### Operaciones en grafos:

```cypher
// Clonar un subgrafo
MATCH (source:Person {name: "Alice"})
CALL apoc.refactor.cloneSubgraph([source], {
  relationshipSelectionStrategy: "outgoing"
})
YIELD input, output
RETURN input, output

// Fusionar nodos
MATCH (a:Person {name: "Alice Johnson"}), (b:Person {name: "Alice J."})
CALL apoc.refactor.mergeNodes([a, b], {properties: "combine"})
YIELD node
RETURN node
```

#### Operaciones con fecha y hora:

```cypher
// Manipulación de fechas
RETURN 
  apoc.date.format(timestamp(), "yyyy-MM-dd") AS formatted_date,        // Fecha actual formateada
  apoc.date.parse("2023-05-17", "ms", "yyyy-MM-dd") AS timestamp_ms,    // Convertir texto a timestamp
  apoc.date.add(timestamp(), "P1Y2M", "ms") AS date_plus_1year_2months  // Sumar periodo a fecha
```

#### Importación y exportación de datos:

```cypher
// Importar datos desde CSV
CALL apoc.load.csv("https://raw.githubusercontent.com/neo4j-examples/movies-python-bolt/master/data/movies.csv")
YIELD map
RETURN map.title, map.tagline LIMIT 5

// Importar datos desde JSON
CALL apoc.load.json("https://jsonplaceholder.typicode.com/users")
YIELD value
RETURN value.name, value.email, value.company.name LIMIT 5

// Exportar a CSV (requiere apoc.export.file.enabled=true)
MATCH (m:Movie)
CALL apoc.export.csv.query(
  "MATCH (m:Movie) RETURN m.title, m.released", 
  "movies.csv", 
  {}
)
```

#### Procedimientos para creación dinámica:

```cypher
// Crear nodo con propiedades dinámicas
CALL apoc.create.node(["Person"], {name: "Dynamic Node", created: timestamp()})
YIELD node
RETURN node

// Crear relación dinámica
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CALL apoc.create.relationship(a, "KNOWS", {since: date()}, b)
YIELD rel
RETURN a, rel, b
```

#### Ejecución de Cypher dinámico:

```cypher
// Ejecutar Cypher construido dinámicamente
WITH "MATCH (p:Person) WHERE p.age > $minAge RETURN p.name AS name, p.age AS age" AS query
CALL apoc.cypher.run(query, {minAge: 30}) YIELD value
RETURN value.name, value.age
```

### Casos de Uso Prácticos con APOC

#### Importación de datos complejos:

```cypher
// Supongamos que tenemos un JSON con una estructura jerárquica
CALL apoc.load.json("https://example.com/api/departments")
YIELD value
UNWIND value.departments AS department
MERGE (d:Department {id: department.id})
SET d.name = department.name
WITH d, department
UNWIND department.employees AS employee
MERGE (e:Employee {id: employee.id})
SET e.name = employee.name,
    e.position = employee.position
MERGE (e)-[:WORKS_IN]->(d)
```

#### Manipulación masiva de datos:

```cypher
// Actualizar propiedades masivamente
MATCH (p:Person)
WHERE p.age IS NULL
WITH collect(p) AS people
CALL apoc.do.when(
    size(people) > 0,
    "UNWIND people AS p SET p.age = round(18 + rand() * 50) RETURN count(p) AS updated",
    "RETURN 0 AS updated",
    {people: people}
)
YIELD value
RETURN value.updated
```

## 3. Algoritmos de Grafos

### Introducción a los Algoritmos de Grafos en Neo4j

Neo4j proporciona una biblioteca dedicada de algoritmos de grafos (Graph Data Science Library o GDS) que implementa algoritmos eficientes para análisis de grafos a gran escala. Estos algoritmos ayudan a descubrir patrones, identificar estructuras importantes y extraer insights de los datos conectados.

#### Instalación de la biblioteca GDS:

- **En Neo4j Desktop**:
  1. Abrir la base de datos deseada
  2. Clic en "Plugins"
  3. Instalar "Graph Data Science Library" desde el Marketplace

- **En Neo4j Server**:
  1. Descargar el JAR de GDS correspondiente a tu versión de Neo4j
  2. Colocar el archivo JAR en la carpeta plugins de Neo4j
  3. Reiniciar Neo4j

#### Verificación de la instalación:

```cypher
// Verificar la versión instalada
CALL gds.version()
```

### Flujo de Trabajo con Algoritmos de Grafos

El uso de algoritmos de grafos en Neo4j generalmente sigue estos pasos:

1. **Proyección del grafo**: Crear una vista en memoria del grafo para el análisis
2. **Ejecución del algoritmo**: Aplicar el algoritmo al grafo proyectado
3. **Procesamiento de resultados**: Escribir los resultados de vuelta a la base de datos o consultar los resultados

#### Proyección del grafo:

```cypher
// Proyección explícita
CALL gds.graph.create(
    'social-network',               // Nombre del grafo proyectado
    'Person',                       // Nodos a incluir
    {
        KNOWS: {                    // Relación a incluir
            orientation: 'UNDIRECTED'   // Tratar como no direccionada
        }
    }
)
```

#### Modos de ejecución:

- **stream**: Devuelve los resultados para procesamiento posterior
- **stats**: Devuelve estadísticas resumidas
- **mutate**: Escribe los resultados en el grafo proyectado
- **write**: Escribe los resultados de vuelta a la base de datos Neo4j

### Algoritmos de Centralidad

Los algoritmos de centralidad identifican los nodos más importantes en un grafo según diferentes métricas.

#### PageRank:

Mide la influencia de los nodos basándose en las conexiones que reciben.

```cypher
// Crear grafo proyectado
CALL gds.graph.create(
    'pr-graph',
    'Page',
    'LINKS'
)

// Ejecutar PageRank y transmitir resultados
CALL gds.pageRank.stream('pr-graph')
YIELD nodeId, score
MATCH (p:Page) WHERE id(p) = nodeId
RETURN p.url AS url, score
ORDER BY score DESC
LIMIT 10

// Ejecutar PageRank y escribir los resultados en la base de datos
CALL gds.pageRank.write('pr-graph', {
    writeProperty: 'pageRank'
})
YIELD nodePropertiesWritten
```

#### Betweenness Centrality:

Mide cuántas veces un nodo actúa como puente a lo largo de los caminos más cortos entre otros nodos.

```cypher
// Ejecutar Betweenness Centrality
CALL gds.betweenness.stream('social-network')
YIELD nodeId, score
MATCH (p:Person) WHERE id(p) = nodeId
RETURN p.name AS name, score
ORDER BY score DESC
LIMIT 10
```

### Algoritmos de Comunidad

Los algoritmos de detección de comunidades identifican grupos de nodos densamente conectados.

#### Louvain:

Detecta comunidades mediante la optimización de la modularidad.

```cypher
// Ejecutar Louvain
CALL gds.louvain.stream('social-network')
YIELD nodeId, communityId
MATCH (p:Person) WHERE id(p) = nodeId
RETURN communityId, collect(p.name) AS members, count(*) AS memberCount
ORDER BY memberCount DESC
```

#### Label Propagation:

Detecta comunidades propagando etiquetas entre nodos vecinos.

```cypher
// Ejecutar Label Propagation
CALL gds.labelPropagation.stream('social-network')
YIELD nodeId, communityId
MATCH (p:Person) WHERE id(p) = nodeId
RETURN communityId, collect(p.name) AS members, count(*) AS memberCount
ORDER BY memberCount DESC
```

### Algoritmos de Caminos

Los algoritmos de caminos encuentran rutas óptimas entre nodos.

#### Shortest Path (Dijkstra):

Encuentra los caminos más cortos entre nodos, considerando pesos en las relaciones.

```cypher
// Proyectar grafo con pesos
CALL gds.graph.create(
    'routes',
    'City',
    {
        ROAD: {
            orientation: 'UNDIRECTED',
            properties: {
                distance: {
                    property: 'distance'
                }
            }
        }
    }
)

// Encontrar el camino más corto entre dos ciudades
MATCH (source:City {name: 'New York'}), (target:City {name: 'Los Angeles'})
CALL gds.shortestPath.dijkstra.stream('routes', {
    sourceNode: source,
    targetNode: target,
    relationshipWeightProperty: 'distance'
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs
RETURN 
    index,
    gds.util.asNode(sourceNode).name AS sourceNodeName,
    gds.util.asNode(targetNode).name AS targetNodeName,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS path
```

### Algoritmos de Similitud

Los algoritmos de similitud miden cuán similares son los nodos basándose en sus propiedades o conexiones.

#### Jaccard Similarity:

Mide la similitud entre nodos basada en sus vecinos comunes.

```cypher
// Proyectar grafo
CALL gds.graph.create(
    'similarity-graph',
    'User',
    'LIKES'
)

// Calcular similitud de Jaccard
CALL gds.nodeSimilarity.stream('similarity-graph')
YIELD node1, node2, similarity
RETURN 
    gds.util.asNode(node1).name AS user1,
    gds.util.asNode(node2).name AS user2,
    similarity
ORDER BY similarity DESC
LIMIT 10
```

### Casos de Uso Prácticos con Algoritmos de Grafos

#### Análisis de Redes Sociales:

```cypher
// Crear grafo para análisis de red social
CALL gds.graph.create(
    'social-analysis',
    'Person',
    {
        FRIEND: {
            orientation: 'UNDIRECTED'
        },
        FOLLOWS: {
            orientation: 'NATURAL'
        }
    },
    {
        nodeProperties: ['age', 'gender']
    }
)

// Identificar influencers con PageRank
CALL gds.pageRank.write('social-analysis', {
    writeProperty: 'influence',
    maxIterations: 20,
    dampingFactor: 0.85
})
YIELD nodePropertiesWritten

// Detectar comunidades
CALL gds.louvain.write('social-analysis', {
    writeProperty: 'community'
})
YIELD communityCount, modularity

// Analizar resultados
MATCH (p:Person)
RETURN 
    p.community AS community,
    count(*) AS memberCount,
    round(avg(p.influence), 4) AS avgInfluence,
    collect(p.name)[..5] AS sampleMembers
ORDER BY memberCount DESC
```

#### Recomendación de Productos:

```cypher
// Crear grafo para recomendaciones
CALL gds.graph.create(
    'product-recommendations',
    ['User', 'Product'],
    {
        PURCHASED: {
            orientation: 'NATURAL',
            properties: ['rating']
        }
    }
)

// Calcular similitud entre usuarios
CALL gds.nodeSimilarity.write('product-recommendations', {
    writeProperty: 'similarity',
    nodeLabels: ['User'],
    similarityCutoff: 0.5
})

// Generar recomendaciones para un usuario específico
MATCH (u1:User {name: 'Alice'})
MATCH (u1)-[s:SIMILAR]->(u2:User)
MATCH (u2)-[:PURCHASED]->(p:Product)
WHERE NOT (u1)-[:PURCHASED]->(p)
RETURN p.name AS recommendation, 
       count(u2) AS frequencyAmongSimilarUsers,
       s.similarity AS userSimilarity
ORDER BY userSimilarity * frequencyAmongSimilarUsers DESC
LIMIT 10
```

## 4. Integración con Python

### El Driver de Neo4j para Python

El driver oficial de Neo4j para Python permite la integración con aplicaciones Python, proporcionando una forma eficiente de comunicarse con la base de datos.

#### Instalación:

```bash
pip install neo4j
```

#### Conexión básica:

```python
from neo4j import GraphDatabase

# Configuración de conexión
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

# Crear cliente driver
driver = GraphDatabase.driver(uri, auth=(user, password))

# Función para ejecutar consultas
def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record for record in result]

# Ejemplo de uso
query = "MATCH (n:Person) RETURN n.name AS name LIMIT 5"
results = run_query(query)
for record in results:
    print(record["name"])

# Cerrar conexión al finalizar
driver.close()
```

### Gestión de Sesiones y Transacciones

```python
from neo4j import GraphDatabase

class Neo4jRepository:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def create_product(self, name, price, category_id):
        with self.driver.session() as session:
            # Función de transacción
            result = session.write_transaction(self._create_product, name, price, category_id)
            return result
            
    @staticmethod
    def _create_product(tx, name, price, category_id):
        query = """
        CREATE (p:Product {id: randomUUID(), name: $name, price: $price})
        WITH p
        MATCH (c:Category {id: $category_id})
        CREATE (p)-[:BELONGS_TO]->(c)
        RETURN p.id AS id, p.name AS name
        """
        result = tx.run(query, name=name, price=price, category_id=category_id)
        record = result.single()
        return {"id": record["id"], "name": record["name"]}
        
    def get_products_by_category(self, category_name):
        with self.driver.session() as session:
            return session.read_transaction(self._get_products_by_category, category_name)
            
    @staticmethod
    def _get_products_by_category(tx, category_name):
        query = """
        MATCH (p:Product)-[:BELONGS_TO]->(c:Category {name: $category_name})
        RETURN p.id AS id, p.name AS name, p.price AS price
        ORDER BY p.price DESC
        """
        result = tx.run(query, category_name=category_name)
        return [{"id": record["id"], "name": record["name"], "price": record["price"]} 
                for record in result]
```

### Uso de APOC desde Python

```python
from neo4j import GraphDatabase

class ApocIntegration:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def import_json_data(self, url):
        with self.driver.session() as session:
            return session.write_transaction(self._import_json_data, url)
            
    @staticmethod
    def _import_json_data(tx, url):
        query = """
        CALL apoc.load.json($url)
        YIELD value
        RETURN value
        """
        result = tx.run(query, url=url)
        return [record["value"] for record in result]
        
    def export_graph_to_json(self, file_path):
        with self.driver.session() as session:
            query = """
            MATCH (n)
            CALL apoc.export.json.all($file, {useTypes: true})
            YIELD file, source, nodes, relationships
            RETURN file, nodes, relationships
            """
            result = session.run(query, file=file_path)
            return result.single()
```

### Integrando Algoritmos de Grafos con Python

```python
from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt

class GraphAlgorithmsService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def create_projection(self, graph_name, node_labels, relationships):
        with self.driver.session() as session:
            query = """
            CALL gds.graph.exists($graph_name)
            YIELD exists
            """
            result = session.run(query, graph_name=graph_name)
            exists = result.single()["exists"]
            
            if exists:
                # Eliminar proyección existente
                delete_query = """
                CALL gds.graph.drop($graph_name)
                YIELD graphName
                """
                session.run(delete_query, graph_name=graph_name)
            
            # Crear nueva proyección
            create_query = """
            CALL gds.graph.create($graph_name, $node_labels, $relationships)
            YIELD graphName, nodeCount, relationshipCount
            RETURN graphName, nodeCount, relationshipCount
            """
            result = session.run(create_query, 
                              graph_name=graph_name, 
                              node_labels=node_labels, 
                              relationships=relationships)
            return result.single()
            
    def run_pagerank(self, graph_name, write_property=None):
        with self.driver.session() as session:
            if write_property:
                # Modo write: escribe resultados en la base de datos
                query = """
                CALL gds.pageRank.write($graph_name, {
                    writeProperty: $write_property,
                    maxIterations: 20,
                    dampingFactor: 0.85
                })
                YIELD nodePropertiesWritten, ranIterations, didConverge
                RETURN nodePropertiesWritten, ranIterations, didConverge
                """
                result = session.run(query, graph_name=graph_name, write_property=write_property)
                return result.single()
            else:
                # Modo stream: devuelve resultados para procesamiento
                query = """
                CALL gds.pageRank.stream($graph_name)
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
                ORDER BY score DESC
                """
                result = session.run(query, graph_name=graph_name)
                return [(record["name"], record["score"]) for record in result]
    
    def run_community_detection(self, graph_name, algorithm="louvain", write_property=None):
        with self.driver.session() as session:
            if algorithm.lower() not in ["louvain", "label_propagation"]:
                raise ValueError("Algoritmo no soportado. Use 'louvain' o 'label_propagation'")
                
            algo_name = "louvain" if algorithm.lower() == "louvain" else "labelPropagation"
            
            if write_property:
                # Modo write
                query = f"""
                CALL gds.{algo_name}.write($graph_name, {{
                    writeProperty: $write_property
                }})
                YIELD communityCount, modularity
                RETURN communityCount, modularity
                """
                result = session.run(query, graph_name=graph_name, write_property=write_property)
                return result.single()
            else:
                # Modo stream
                query = f"""
                CALL gds.{algo_name}.stream($graph_name)
                YIELD nodeId, communityId
                RETURN communityId, collect(gds.util.asNode(nodeId).name) AS members, 
                       count(*) AS memberCount
                ORDER BY memberCount DESC
                """
                result = session.run(query, graph_name=graph_name)
                return [(record["communityId"], record["members"], record["memberCount"]) 
                        for record in result]
    
    def analyze_communities(self, graph_name, community_property="community"):
        """Analiza las comunidades detectadas y genera visualizaciones"""
        with self.driver.session() as session:
            # Obtener datos de comunidades
            query = f"""
            MATCH (n)
            WHERE n.{community_property} IS NOT NULL
            RETURN n.{community_property} AS community, 
                   count(*) AS memberCount,
                   collect(n.name) AS members
            ORDER BY memberCount DESC
            """
            result = session.run(query)
            communities = [(record["community"], record["memberCount"], record["members"]) 
                          for record in result]
            
            # Crear DataFrame para visualización
            df = pd.DataFrame([
                {"community": comm, "memberCount": count} 
                for comm, count, _ in communities
            ])
            
            # Visualizar distribución de comunidades
            plt.figure(figsize=(10, 6))
            plt.bar(df['community'].astype(str), df['memberCount'])
            plt.title('Distribución de Tamaños de Comunidades')
            plt.xlabel('Comunidad')
            plt.ylabel('Número de Miembros')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            return communities, plt
```

### Ejemplo Completo: Análisis de Red Social con Python y Neo4j

```python
from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from IPython.display import display

class SocialNetworkAnalysis:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def create_sample_data(self):
        """Crea datos de muestra para una red social"""
        with self.driver.session() as session:
            # Verificar si ya existen datos
            count_query = "MATCH (n:Person) RETURN count(n) AS count"
            count = session.run(count_query).single()["count"]
            
            if count > 0:
                print(f"Ya existen {count} nodos Person en la base de datos.")
                return count
            
            # Crear datos de muestra
            create_query = """
            // Crear personas
            CREATE (alice:Person {name: 'Alice', age: 30})
            CREATE (bob:Person {name: 'Bob', age: 32})
            CREATE (charlie:Person {name: 'Charlie', age: 25})
            CREATE (david:Person {name: 'David', age: 29})
            CREATE (eve:Person {name: 'Eve', age: 27})
            CREATE (frank:Person {name: 'Frank', age: 35})
            CREATE (grace:Person {name: 'Grace', age: 31})
            CREATE (heidi:Person {name: 'Heidi', age: 24})
            CREATE (ivan:Person {name: 'Ivan', age: 33})
            CREATE (judy:Person {name: 'Judy', age: 28})
            
            // Crear relaciones de amistad
            CREATE (alice)-[:FRIEND]->(bob)
            CREATE (bob)-[:FRIEND]->(alice)
            CREATE (alice)-[:FRIEND]->(charlie)
            CREATE (charlie)-[:FRIEND]->(alice)
            CREATE (alice)-[:FRIEND]->(david)
            CREATE (david)-[:FRIEND]->(alice)
            CREATE (bob)-[:FRIEND]->(charlie)
            CREATE (charlie)-[:FRIEND]->(bob)
            CREATE (bob)-[:FRIEND]->(eve)
            CREATE (eve)-[:FRIEND]->(bob)
            CREATE (charlie)-[:FRIEND]->(frank)
            CREATE (frank)-[:FRIEND]->(charlie)
            CREATE (david)-[:FRIEND]->(grace)
            CREATE (grace)-[:FRIEND]->(david)
            CREATE (eve)-[:FRIEND]->(heidi)
            CREATE (heidi)-[:FRIEND]->(eve)
            CREATE (frank)-[:FRIEND]->(ivan)
            CREATE (ivan)-[:FRIEND]->(frank)
            CREATE (grace)-[:FRIEND]->(judy)
            CREATE (judy)-[:FRIEND]->(grace)
            CREATE (heidi)-[:FRIEND]->(ivan)
            CREATE (ivan)-[:FRIEND]->(heidi)
            
            // Crear relaciones de seguimiento
            CREATE (alice)-[:FOLLOWS]->(eve)
            CREATE (bob)-[:FOLLOWS]->(frank)
            CREATE (charlie)-[:FOLLOWS]->(grace)
            CREATE (david)-[:FOLLOWS]->(heidi)
            CREATE (eve)-[:FOLLOWS]->(ivan)
            CREATE (frank)-[:FOLLOWS]->(judy)
            CREATE (grace)-[:FOLLOWS]->(alice)
            CREATE (heidi)-[:FOLLOWS]->(bob)
            CREATE (ivan)-[:FOLLOWS]->(charlie)
            CREATE (judy)-[:FOLLOWS]->(david)
            
            // Retornar conteo
            MATCH (n:Person) RETURN count(n) AS count
            """
            count = session.run(create_query).single()["count"]
            print(f"Creados {count} nodos Person con relaciones FRIEND y FOLLOWS.")
            return count
    
    def run_centrality_analysis(self):
        """Ejecuta análisis de centralidad y visualiza resultados"""
        # Crear proyección del grafo
        with self.driver.session() as session:
            # Eliminar proyección anterior si existe
            session.run("CALL gds.graph.drop('social-network', false) YIELD graphName")
            
            # Crear nueva proyección
            projection_query = """
            CALL gds.graph.create(
                'social-network',
                'Person',
                {
                    FRIEND: {
                        orientation: 'UNDIRECTED'
                    },
                    FOLLOWS: {
                        orientation: 'NATURAL'
                    }
                }
            )
            YIELD graphName, nodeCount, relationshipCount
            RETURN graphName, nodeCount, relationshipCount
            """
            projection = session.run(projection_query).single()
            print(f"Proyección creada: {projection['graphName']} con {projection['nodeCount']} nodos y {projection['relationshipCount']} relaciones.")
            
            # Ejecutar PageRank
            pagerank_query = """
            CALL gds.pageRank.write('social-network', {
                writeProperty: 'pagerank',
                maxIterations: 20,
                dampingFactor: 0.85
            })
            YIELD nodePropertiesWritten
            RETURN nodePropertiesWritten
            """
            pagerank = session.run(pagerank_query).single()
            print(f"PageRank calculado para {pagerank['nodePropertiesWritten']} nodos.")
            
            # Ejecutar Betweenness Centrality
            betweenness_query = """
            CALL gds.betweenness.write('social-network', {
                writeProperty: 'betweenness'
            })
            YIELD nodePropertiesWritten
            RETURN nodePropertiesWritten
            """
            betweenness = session.run(betweenness_query).single()
            print(f"Betweenness calculado para {betweenness['nodePropertiesWritten']} nodos.")
            
            # Obtener resultados para análisis
            results_query = """
            MATCH (p:Person)
            RETURN p.name AS name, 
                   p.pagerank AS pagerank, 
                   p.betweenness AS betweenness,
                   size((p)-[:FRIEND]-()) AS friendCount,
                   size((p)-[:FOLLOWS]->()) AS followsCount,
                   size((p)<-[:FOLLOWS]-()) AS followersCount
            ORDER BY p.pagerank DESC
            """
            results = session.run(results_query)
            df = pd.DataFrame([{
                "name": record["name"],
                "pagerank": record["pagerank"],
                "betweenness": record["betweenness"],
                "friendCount": record["friendCount"],
                "followsCount": record["followsCount"],
                "followersCount": record["followersCount"]
            } for record in results])
            
            # Visualizar resultados
            plt.figure(figsize=(10, 6))
            plt.scatter(df['pagerank'], df['betweenness'], s=100)
            
            # Añadir etiquetas
            for _, row in df.iterrows():
                plt.annotate(row['name'], 
                            (row['pagerank'], row['betweenness']),
                            xytext=(5, 5), 
                            textcoords='offset points')
                
            plt.title('PageRank vs Betweenness Centrality')
            plt.xlabel('PageRank')
            plt.ylabel('Betweenness Centrality')
            plt.grid(True, linestyle='--', alpha=0.7)
            
            return df, plt
    
    def run_community_detection(self):
        """Ejecuta algoritmos de detección de comunidades"""
        with self.driver.session() as session:
            # Ejecutar algoritmo Louvain
            louvain_query = """
            CALL gds.louvain.write('social-network', {
                writeProperty: 'louvain_community'
            })
            YIELD communityCount, modularity
            RETURN communityCount, modularity
            """
            louvain = session.run(louvain_query).single()
            print(f"Louvain detectó {louvain['communityCount']} comunidades con modularidad {louvain['modularity']:.4f}")
            
            # Ejecutar Label Propagation
            lpa_query = """
            CALL gds.labelPropagation.write('social-network', {
                writeProperty: 'lpa_community'
            })
            YIELD communityCount, ranIterations
            RETURN communityCount, ranIterations
            """
            lpa = session.run(lpa_query).single()
            print(f"Label Propagation detectó {lpa['communityCount']} comunidades en {lpa['ranIterations']} iteraciones")
            
            # Obtener resultados para comparación
            results_query = """
            MATCH (p:Person)
            RETURN p.name AS name, 
                   p.louvain_community AS louvain,
                   p.lpa_community AS lpa
            ORDER BY p.name
            """
            results = session.run(results_query)
            df = pd.DataFrame([{
                "name": record["name"],
                "louvain_community": record["louvain"],
                "lpa_community": record["lpa"]
            } for record in results])
            
            # Visualizar comunidades Louvain
            louvain_communities = df.groupby('louvain_community')['name'].apply(list).reset_index()
            louvain_communities['count'] = louvain_communities['name'].apply(len)
            
            plt.figure(figsize=(10, 6))
            plt.bar(louvain_communities['louvain_community'].astype(str), 
                   louvain_communities['count'])
            plt.title('Comunidades detectadas por Louvain')
            plt.xlabel('Comunidad')
            plt.ylabel('Número de miembros')
            
            return df, plt
    
    def visualize_network(self):
        """Visualiza la red social utilizando networkx"""
        with self.driver.session() as session:
            # Obtener nodos y relaciones
            query = """
            MATCH (p:Person)
            RETURN p.name AS name, p.louvain_community AS community
            """
            nodes_result = session.run(query)
            nodes = {record["name"]: record["community"] for record in nodes_result}
            
            query = """
            MATCH (p1:Person)-[r:FRIEND]->(p2:Person)
            RETURN p1.name AS source, p2.name AS target, 'FRIEND' AS type
            UNION
            MATCH (p1:Person)-[r:FOLLOWS]->(p2:Person)
            RETURN p1.name AS source, p2.name AS target, 'FOLLOWS' AS type
            """
            edges_result = session.run(query)
            edges = [(record["source"], record["target"], record["type"]) for record in edges_result]
            
            # Crear grafo con networkx
            G = nx.Graph()
            
            # Añadir nodos con atributos
            for name, community in nodes.items():
                G.add_node(name, community=community)
            
            # Añadir aristas
            for source, target, rel_type in edges:
                G.add_edge(source, target, type=rel_type)
            
            # Configurar visualización
            plt.figure(figsize=(12, 10))
            
            # Posiciones de nodos
            pos = nx.spring_layout(G, seed=42)
            
            # Colores por comunidad
            communities = set(nx.get_node_attributes(G, 'community').values())
            colors = plt.cm.rainbow(np.linspace(0, 1, len(communities)))
            community_colors = dict(zip(communities, colors))
            
            node_colors = [community_colors[G.nodes[node]['community']] for node in G.nodes()]
            
            # Dibujar nodos
            nx.draw_networkx_nodes(G, pos, 
                                  node_color=node_colors, 
                                  node_size=300, 
                                  alpha=0.8)
            
            # Dibujar aristas
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
            
            # Etiquetas
            nx.draw_networkx_labels(G, pos, font_size=10)
            
            plt.title('Visualización de Red Social con Comunidades')
            plt.axis('off')
            
            # Leyenda para comunidades
            import matplotlib.patches as mpatches
            patches = [mpatches.Patch(color=community_colors[c], label=f"Comunidad {c}") 
                      for c in communities]
            plt.legend(handles=patches, title="Comunidades")
            
            return G, plt
```

## Ejercicios Prácticos

### Ejercicio 1: Manipulación Avanzada de Datos

Utilizando las funciones para manipulación de cadenas, números y listas, realiza las siguientes tareas en la base de datos de ejemplo "Movies":

1. Crea una consulta que devuelva los títulos de películas en mayúsculas, junto con el año de lanzamiento y la longitud del título

2. Para cada director, crea una lista de sus películas ordenadas por año, mostrando el nombre del director y la lista de películas

3. Calcula la década de lanzamiento para cada película y agrupa las películas por década

4. Extrae el primer nombre y apellido de los actores/actrices, y crea un nuevo nodo `Person` para cada actor/actriz si no existe ya

5. Genera una puntuación aleatoria entre 1 y 5 para cada relación `ACTED_IN` que no tenga ya una propiedad `rating`

### Ejercicio 2: Trabajando con APOC

Implementa las siguientes operaciones utilizando la biblioteca APOC:

1. Importa datos desde un JSON público (por ejemplo, desde una API pública como JSONPlaceholder) y crea nodos y relaciones basados en los datos

2. Utiliza funciones de APOC para:
   - Transformar propiedades de texto (capitalizar, camelCase, etc.)
   - Calcular distancias de texto entre nombres similares
   - Realizar operaciones complejas sobre colecciones

3. Genera un UUID para cada nodo que no tenga un identificador único

4. Exporta un subgrafo a formato GraphML o JSON

5. Utiliza `apoc.periodic.iterate` para actualizar un gran número de nodos de manera eficiente

### Ejercicio 3: Aplicación de Algoritmos de Grafos

Utilizando la biblioteca de algoritmos de grafos (Graph Data Science), realiza el siguiente análisis en la base de datos "Movies":

1. Proyecta un grafo que incluya actores y películas, donde las relaciones representen "actuó en"

2. Ejecuta PageRank para identificar los actores más influyentes de la red

3. Utiliza un algoritmo de detección de comunidades para identificar grupos de actores que tienden a trabajar juntos

4. Encuentra el camino más corto entre dos actores famosos (por ejemplo, Kevin Bacon y otro actor)

5. Calcula la similitud entre actores basada en las películas en las que han actuado

## Recursos Adicionales

- [Documentación oficial de Cypher - Funciones](https://neo4j.com/docs/cypher-manual/current/functions/)
- [APOC Documentation](https://neo4j.com/labs/apoc/4.4/)
- [Graph Data Science Library Documentation](https://neo4j.com/docs/graph-data-science/current/)
- [Neo4j Developer Blog - APOC Tips](https://neo4j.com/developer-blog/helpful-neo4j-apoc-procedures/)
- [GitHub de APOC](https://github.com/neo4j-contrib/neo4j-apoc-procedures)
- [Tutoriales de Algoritmos de Grafos](https://neo4j.com/docs/graph-data-science/current/algorithms/)
- [Neo4j Python Driver Documentation](https://neo4j.com/docs/api/python-driver/current/)
- [Ejemplos de Python con Neo4j](https://github.com/neo4j-examples/movies-python-bolt)

---

## Autoevaluación

### Preguntas Conceptuales

1. Explica las diferencias entre las funciones `collect()`, `reduce()` y `apoc.coll.sum()`. Proporciona un ejemplo de uso para cada una.

2. ¿Cuáles son las ventajas de utilizar APOC para importar datos en comparación con LOAD CSV nativo de Cypher? Enumera al menos tres diferencias clave.

3. Describe los pasos necesarios para aplicar un algoritmo de centralidad a un grafo y explicar cómo interpretar sus resultados.

4. Compara y contrasta los algoritmos PageRank, Betweenness Centrality y Closeness Centrality. ¿Qué tipo de nodos identifica cada uno como importantes?

### Ejercicio Práctico

Desarrolla una solución que integre los conceptos aprendidos en este módulo:

1. Crear un conjunto de datos que incluya:
   - Al menos 20 nodos de al menos 2 tipos diferentes
   - Al menos 30 relaciones de al menos 2 tipos diferentes
   - Propiedades relevantes en nodos y relaciones

2. Implementar funciones avanzadas de Cypher para:
   - Transformar y analizar propiedades de texto
   - Realizar cálculos numéricos
   - Manipular listas de valores

3. Utilizar APOC para:
   - Importar datos adicionales de una fuente externa
   - Ejecutar operaciones masivas sobre el grafo
   - Exportar un subgrafo a un formato específico

4. Aplicar al menos 2 algoritmos de grafos para:
   - Identificar nodos importantes
   - Detectar comunidades
   - Calcular similitudes entre nodos

5. Documentar todo el proceso, incluyendo:
   - El modelo de datos y su justificación
   - Las consultas Cypher utilizadas y sus resultados
   - Visualizaciones o resúmenes de los resultados de los algoritmos
   - Conclusiones e insights obtenidos
