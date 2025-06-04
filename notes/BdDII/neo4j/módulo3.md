# Módulo 3: Lenguaje Cypher

## 1. Sintaxis Básica de Cypher

### Introducción a Cypher

Cypher es el lenguaje de consulta declarativo de Neo4j, creado específicamente para trabajar con grafos. Inspirado en SQL, pero adaptado para grafos, Cypher permite expresar patrones visuales de nodos y relaciones de forma textual.

#### Características principales:

- **Declarativo**: Especificas qué quieres encontrar, no cómo encontrarlo
- **Patrones visuales**: La sintaxis imita la apariencia visual de los grafos
- **Expresivo**: Permite consultas complejas de forma concisa
- **Legible por humanos**: Diseñado para ser leído y comprendido fácilmente

### Estructura Básica de Comandos

La mayoría de las consultas Cypher siguen un patrón similar a SQL, con cláusulas que se ejecutan en un orden específico:

```cypher
MATCH (patrón-a-encontrar)
WHERE (condiciones-a-cumplir)
RETURN (lo-que-se-quiere-devolver)
```

#### Principales cláusulas:

1. `MATCH`: Especifica patrones a buscar en el grafo
2. `WHERE`: Filtra los resultados según condiciones
3. `RETURN`: Indica qué datos devolver
4. `CREATE`: Crea nuevos nodos y relaciones
5. `MERGE`: Crea entidades si no existen, o coincide con existentes
6. `SET`: Establece valores de propiedades
7. `DELETE`: Elimina nodos, relaciones y propiedades
8. `REMOVE`: Elimina etiquetas y propiedades
9. `ORDER BY`: Ordena los resultados
10. `LIMIT`: Limita el número de filas devueltas

### Patrones de Nodos y Relaciones

La sintaxis de patrones en Cypher refleja visualmente lo que estás buscando en el grafo.

#### Nodos:

```cypher
// Nodo sin especificar (cualquier nodo)
(n)

// Nodo con etiqueta específica
(p:Person)

// Nodo con múltiples etiquetas
(m:Movie:Classic)

// Nodo con propiedades
(p:Person {name: "John", age: 42})

// Nodo con variable y etiqueta
(actor:Person)
```

#### Relaciones:

```cypher
// Relación básica (cualquier tipo, cualquier dirección)
(a)--(b)

// Relación con dirección específica
(a)-->(b)  // a hacia b
(a)<--(b)  // b hacia a

// Relación con tipo específico
(a)-[:KNOWS]->(b)

// Relación con propiedades
(a)-[:RATED {stars: 5}]->(b)

// Relación con variable
(a)-[r:KNOWS]->(b)  // r se puede usar después

// Relación con múltiples tipos posibles
(a)-[:KNOWS|:WORKED_WITH]->(b)
```

#### Patrones combinados:

```cypher
// Persona que conoce a alguien que vive en España
(p1:Person)-[:KNOWS]->(p2:Person)-[:LIVES_IN]->(c:Country {name: "Spain"})

// Actor que actuó en película dirigida por cierto director
(actor:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(director:Person)
```

### Operadores y Expresiones Básicas

#### Operadores de comparación:

- `=`: Igual a
- `<>` o `!=`: Distinto de
- `<`: Menor que
- `>`: Mayor que
- `<=`: Menor o igual que
- `>=`: Mayor o igual que

#### Operadores booleanos:

- `AND`: Ambas condiciones deben ser verdaderas
- `OR`: Al menos una condición debe ser verdadera
- `NOT` o `!`: Negación de la condición
- `XOR`: Una condición es verdadera pero no ambas

#### Operadores de cadenas:

- `+`: Concatenación de cadenas
- `STARTS WITH`: Comienza con una subcadena
- `ENDS WITH`: Termina con una subcadena
- `CONTAINS`: Contiene una subcadena

#### Ejemplos de expresiones:

```cypher
// Operadores de comparación
MATCH (p:Person)
WHERE p.age > 30 AND p.age <= 40
RETURN p

// Operadores de cadena
MATCH (m:Movie)
WHERE m.title STARTS WITH "The" OR m.title CONTAINS "Star"
RETURN m

// Operador IN para listas
MATCH (p:Person)
WHERE p.name IN ["John", "Mary", "Sue"]
RETURN p
```

### Ejemplos de Consultas Básicas

#### Encontrar todos los nodos con una etiqueta:

```cypher
MATCH (p:Person)
RETURN p
```

#### Encontrar un nodo por propiedad:

```cypher
MATCH (p:Person {name: "Tom Hanks"})
RETURN p
```

#### Encontrar relaciones entre nodos:

```cypher
MATCH (p1:Person)-[:KNOWS]->(p2:Person)
RETURN p1.name, p2.name
```

#### Filtrar con WHERE:

```cypher
MATCH (m:Movie)
WHERE m.released > 2010 AND m.title CONTAINS "Matrix"
RETURN m.title, m.released
```

#### Devolver propiedades específicas:

```cypher
MATCH (p:Person)
WHERE p.born < 1970
RETURN p.name AS Nombre, 2023 - p.born AS Edad, p.born AS "Año de nacimiento"
```

## 2. Consultas MATCH y WHERE

### MATCH Avanzado

La cláusula `MATCH` es el corazón de las consultas Cypher, permitiendo especificar patrones complejos en el grafo.

#### Patrones variables de longitud:

```cypher
// Personas conectadas por hasta 3 relaciones KNOWS
MATCH (p1:Person {name: "Alice"})-[:KNOWS*1..3]->(p2:Person)
RETURN p2.name

// Cualquier número de relaciones (potencialmente peligroso)
MATCH (p1:Person {name: "Alice"})-[:KNOWS*]->(p2:Person)
RETURN p2.name

// Exactamente 2 relaciones
MATCH (p1:Person {name: "Alice"})-[:KNOWS*2]->(p2:Person)
RETURN p2.name
```

#### Captura de caminos:

```cypher
// Guarda el camino completo en una variable
MATCH path = (p1:Person {name: "Alice"})-[:KNOWS*1..3]->(p2:Person)
RETURN path, length(path)
```

#### Múltiples patrones:

```cypher
// Buscar actores que trabajaron juntos y además se conocen
MATCH (a1:Actor)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(a2:Actor),
      (a1)-[:KNOWS]-(a2)
RETURN a1.name, a2.name, m.title
```

#### Patrones opcionales con OPTIONAL MATCH:

```cypher
// Encuentra todas las personas y sus mascotas (si tienen)
MATCH (p:Person)
OPTIONAL MATCH (p)-[:OWNS]->(pet:Pet)
RETURN p.name, pet.name
```

### WHERE Avanzado

La cláusula `WHERE` permite filtrar los resultados de `MATCH` con condiciones complejas.

#### Operadores de existencia:

```cypher
// Personas que tienen la propiedad 'email'
MATCH (p:Person)
WHERE p.email IS NOT NULL
RETURN p

// Películas sin la propiedad 'rating'
MATCH (m:Movie)
WHERE NOT exists(m.rating)
RETURN m.title
```

#### Expresiones regulares:

```cypher
// Nombres que empiezan con 'J' seguido de cualquier vocal
MATCH (p:Person)
WHERE p.name =~ "J[aeiou].*"
RETURN p.name

// Títulos con formato 'The X'
MATCH (m:Movie)
WHERE m.title =~ "The .*"
RETURN m.title
```

#### Filtrado por propiedades de relaciones:

```cypher
// Ratings con más de 4 estrellas
MATCH (u:User)-[r:RATED]->(m:Movie)
WHERE r.stars > 4
RETURN u.name, m.title, r.stars
```

#### Funciones en WHERE:

```cypher
// Películas con títulos largos
MATCH (m:Movie)
WHERE size(m.title) > 20
RETURN m.title

// Personas nacidas en la primera mitad del año
MATCH (p:Person)
WHERE date(p.born).month <= 6
RETURN p.name, p.born
```

### Funciones de Agregación

Las funciones de agregación permiten realizar cálculos sobre grupos de resultados.

#### Funciones comunes:

- `count()`: Cuenta el número de filas
- `sum()`: Suma valores
- `avg()`: Calcula el promedio
- `min()` y `max()`: Encuentra valores mínimos y máximos
- `collect()`: Agrupa valores en una lista

#### Ejemplos:

```cypher
// Contar el número de películas
MATCH (m:Movie)
RETURN count(m) AS TotalMovies

// Promedio de rating por película
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN m.title, avg(r.stars) AS AverageRating

// Película con mayor rating promedio
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN m.title, avg(r.stars) AS AverageRating
ORDER BY AverageRating DESC
LIMIT 1

// Agrupar amigos por persona
MATCH (p:Person)-[:KNOWS]->(friend:Person)
RETURN p.name, collect(friend.name) AS Friends
```

### Cláusula WITH para Consultas Encadenadas

La cláusula `WITH` funciona como un "punto y coma" en Cypher, permitiendo usar los resultados de una parte de la consulta en la siguiente.

#### Usos principales:

- Cálculos intermedios
- Filtrado de resultados intermedios
- Agregar resultados antes de continuar
- Ordenar antes de limitar

#### Ejemplos:

```cypher
// Encontrar películas con más de 3 actores
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
WITH m, count(a) AS actorCount
WHERE actorCount > 3
RETURN m.title, actorCount

// Personas con amigos que viven en el mismo país
MATCH (p1:Person)-[:LIVES_IN]->(c:Country)
WITH p1, c
MATCH (p1)-[:KNOWS]->(p2:Person)-[:LIVES_IN]->(c)
RETURN p1.name, p2.name, c.name

// Agrupar películas por década
MATCH (m:Movie)
WITH m.released/10 AS decade, collect(m.title) AS movies
RETURN decade*10 AS Decade, movies, size(movies) AS Count
ORDER BY decade
```

## 3. Creación y Modificación de Datos

### CREATE: Creación de Nodos y Relaciones

La cláusula `CREATE` se usa para añadir nuevos nodos y relaciones al grafo.

#### Crear nodos:

```cypher
// Crear un único nodo
CREATE (p:Person {name: "John Doe", born: 1980})

// Crear múltiples nodos
CREATE (a:Actor {name: "Tom Hanks"}),
       (m:Movie {title: "Forrest Gump", released: 1994})

// Crear nodo con múltiples etiquetas
CREATE (p:Person:Actor:Director {name: "Clint Eastwood"})
```

#### Crear relaciones:

```cypher
// Crear relación entre nodos existentes
MATCH (a:Actor {name: "Tom Hanks"}), (m:Movie {title: "Forrest Gump"})
CREATE (a)-[:ACTED_IN {role: "Forrest"}]->(m)

// Crear nodos y relaciones en una sola consulta
CREATE (a:Actor {name: "Leonardo DiCaprio"})-[:ACTED_IN {role: "Jack"}]->
       (m:Movie {title: "Titanic", released: 1997})
```

#### Crear estructuras complejas:

```cypher
// Crear una pequeña red social
CREATE (john:Person {name: "John"})-[:KNOWS]->(mary:Person {name: "Mary"}),
       (john)-[:WORKS_AT]->(company:Company {name: "Acme Inc"}),
       (mary)-[:WORKS_AT]->(company)
```

### MERGE: Creación Condicional

La cláusula `MERGE` busca un patrón y lo crea si no existe, evitando duplicados.

#### Uso básico:

```cypher
// Crear un nodo solo si no existe
MERGE (p:Person {name: "Alice"})
RETURN p

// Combinar con ON CREATE y ON MATCH para acciones condicionales
MERGE (p:Person {name: "Bob"})
ON CREATE SET p.created = date()
ON MATCH SET p.lastSeen = date()
RETURN p
```

#### MERGE con relaciones:

```cypher
// Asegurarse que existe la relación entre nodos
MATCH (a:Actor {name: "Tom Hanks"}), (m:Movie {title: "Forrest Gump"})
MERGE (a)-[:ACTED_IN]->(m)

// MERGE completo (busca o crea todo el patrón)
MERGE (a:Actor {name: "Tom Hanks"})-[:ACTED_IN]->(m:Movie {title: "Forrest Gump"})
```

#### Cuándo usar MERGE vs CREATE:

- `CREATE`: Cuando sabes que los datos no existen o permites duplicados
- `MERGE`: Cuando quieres prevenir duplicados o implementar lógica upsert

### SET: Modificar Propiedades y Etiquetas

La cláusula `SET` permite añadir o actualizar propiedades y etiquetas.

#### Modificar propiedades:

```cypher
// Actualizar una propiedad
MATCH (p:Person {name: "Alice"})
SET p.age = 35
RETURN p

// Actualizar múltiples propiedades
MATCH (m:Movie {title: "The Matrix"})
SET m.released = 1999, m.tagline = "Welcome to the Real World"
RETURN m

// Actualizar usando un mapa de propiedades
MATCH (p:Person {name: "Bob"})
SET p += {age: 42, occupation: "Developer"}
RETURN p
```

#### Modificar etiquetas:

```cypher
// Añadir una etiqueta a un nodo
MATCH (p:Person {name: "Clint Eastwood"})
SET p:Director
RETURN p

// Añadir múltiples etiquetas
MATCH (p:Person {name: "Tom Hanks"})
SET p:Actor:Producer
RETURN p
```

### DELETE y REMOVE: Eliminar Datos

Las cláusulas `DELETE` y `REMOVE` se usan para eliminar elementos del grafo.

#### DELETE para nodos y relaciones:

```cypher
// Eliminar un nodo (debe estar sin relaciones)
MATCH (p:Person {name: "ToDelete"})
DELETE p

// Eliminar un nodo y sus relaciones
MATCH (p:Person {name: "ToDelete"})
DETACH DELETE p

// Eliminar solo una relación
MATCH (a:Actor)-[r:ACTED_IN]->(m:Movie)
WHERE a.name = "Actor" AND m.title = "BadMovie"
DELETE r
```

#### REMOVE para propiedades y etiquetas:

```cypher
// Eliminar una propiedad
MATCH (p:Person {name: "Alice"})
REMOVE p.temporary_property
RETURN p

// Eliminar una etiqueta
MATCH (p:Person:Temporary)
REMOVE p:Temporary
RETURN p
```

### FOREACH: Operaciones Sobre Listas

La cláusula `FOREACH` permite realizar operaciones sobre elementos de una lista.

```cypher
// Actualizar todos los nodos en un camino
MATCH p = (:Person {name: "Alice"})-[:KNOWS*]->(:Person {name: "Charlie"})
FOREACH (n IN nodes(p) | SET n.visited = true)

// Crear relaciones a todos los elementos de una lista
MATCH (p:Person {name: "Alice"})
FOREACH (name IN ["Bob", "Charlie", "David"] |
  MERGE (friend:Person {name: name})
  MERGE (p)-[:KNOWS]->(friend)
)
```

## 4. Funciones y Operaciones Avanzadas

### Funciones para Manipulación de Cadenas

```cypher
// Concatenación
RETURN "Hello" + " " + "World" AS greeting

// Mayúsculas/minúsculas
MATCH (p:Person)
RETURN p.name, toUpper(p.name), toLower(p.name)

// Subcadenas
RETURN substring("Hello World", 6, 5) AS result // Returns "World"

// Reemplazo
RETURN replace("Hello World", "World", "Neo4j") AS result // Returns "Hello Neo4j"
```

### Funciones para Manipulación de Números

```cypher
// Redondeo
RETURN round(3.141592) AS result // Returns 3

// Funciones matemáticas
RETURN abs(-42) AS absolute,
       sqrt(16) AS squareRoot,
       sign(-5) AS signum

// Aleatorios
RETURN rand() AS random, // Número aleatorio entre 0 y 1
       round(rand() * 100) AS randomInt // Entero aleatorio entre 0 y 100
```

### Funciones para Listas

```cypher
// Crear listas
RETURN [1, 2, 3, 4] AS numbers

// Acceso por índice
RETURN [1, 2, 3, 4][2] AS thirdElement // Returns 3 (índice base 0)

// Slicing
RETURN [1, 2, 3, 4, 5][1..4] AS slice // Returns [2, 3, 4]

// Longitud de lista
RETURN size([1, 2, 3, 4]) AS count // Returns 4

// Funciones de lista
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
WHERE m.title = "The Matrix"
RETURN collect(a.name) AS actors,
       size(collect(a)) AS actorCount
```

### APOC: Librería de Procedimientos y Funciones

APOC (Awesome Procedures On Cypher) es una biblioteca de extensión para Neo4j con cientos de procedimientos y funciones adicionales.

#### Instalación de APOC:

- En Neo4j Desktop: Instalar desde el Marketplace de Plugins
- En Neo4j Server: Descargar el JAR y colocarlo en la carpeta plugins

#### Ejemplos de funciones APOC:

```cypher
// Generar UUID
RETURN apoc.create.uuid() AS uuid

// Manipular mapas
RETURN apoc.map.merge({name: "Alice"}, {age: 30}) AS result

// Convertir entre formatos
RETURN apoc.convert.toJson({name: "Alice", age: 30}) AS json

// Operaciones avanzadas con listas
RETURN apoc.coll.shuffle([1, 2, 3, 4, 5]) AS shuffled,
       apoc.coll.sort([3, 1, 4, 2]) AS sorted
```

#### Ejemplos de procedimientos APOC:

```cypher
// Exportar a CSV
CALL apoc.export.csv.query(
  "MATCH (p:Person) RETURN p.name, p.age",
  "people.csv",
  {}
)

// Importar datos desde JSON
CALL apoc.load.json("https://api.example.com/data") YIELD value
MERGE (p:Person {id: value.id})
SET p += value

// Encontrar camino más corto con restricciones
MATCH (start:Person {name: "Alice"}), (end:Person {name: "Bob"})
CALL apoc.path.expandConfig(start, {
  relationshipFilter: "KNOWS|WORKS_WITH",
  minLevel: 1,
  maxLevel: 5,
  terminatorNodes: [end]
})
YIELD path
RETURN path
```

### Algoritmos de Grafos

La biblioteca de Algoritmos de Grafos de Neo4j proporciona implementaciones eficientes de algoritmos comunes.

#### Categorías principales:

- **Centralidad**: Identificar nodos importantes (PageRank, Betweenness, etc.)
- **Comunidad**: Detectar grupos (Louvain, Label Propagation, etc.)
- **Caminos**: Encontrar rutas óptimas (Shortest Path, A*, etc.)
- **Similitud**: Comparar nodos (Jaccard, Cosine, etc.)

#### Ejemplos:

```cypher
// PageRank para encontrar actores influyentes
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
MATCH (n) WHERE id(n) = nodeId
RETURN n.name AS name, score
ORDER BY score DESC

// Detección de comunidades con Louvain
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
MATCH (n) WHERE id(n) = nodeId
RETURN communityId, collect(n.name) AS members
ORDER BY size(members) DESC

// Camino más corto ponderado
MATCH (source:Location {name: 'A'}), (target:Location {name: 'Z'})
CALL gds.shortestPath.dijkstra.stream('myGraph', {
    sourceNode: source,
    targetNode: target,
    relationshipWeightProperty: 'distance'
})
YIELD nodeIds, costs
RETURN nodeIds, costs
```

## Ejercicios Prácticos

### Ejercicio 1: Consultas Básicas

Utilizando la base de datos de ejemplo "Movies":

1. Encuentra todas las personas que dirigieron películas
2. Lista todas las películas lanzadas en la década de 1990
3. Encuentra los actores que actuaron en "The Matrix"
4. Encuentra directores que también actuaron en sus propias películas
5. Lista las 5 películas más antiguas y sus directores

### Ejercicio 2: Creación y Modificación

1. Crea un nuevo género de película llamado "Documentary"
2. Añade una nueva película documental con un director y al menos dos personas que aparezcan en ella
3. Actualiza la película para añadir un año de lanzamiento y un tagline
4. Conecta la película a otros nodos existentes de forma significativa
5. Finalmente, marca la película como "Nominated" añadiendo una etiqueta

### Ejercicio 3: Consultas Avanzadas

1. Encuentra la "distancia" entre Kevin Bacon y Tom Hanks (número de relaciones ACTED_IN->Movie<-ACTED_IN necesarias para conectarlos)
2. Lista los actores que han trabajado con al menos 3 directores diferentes
3. Encuentra directores que han hecho películas en al menos 3 géneros diferentes
4. Para cada actor, muestra en cuántas películas ha actuado por década
5. Encuentra los "equipos de actuación": parejas de actores que han aparecido juntos en al menos 2 películas

## Recursos Adicionales

- [Documentación oficial de Cypher](https://neo4j.com/docs/cypher-manual/current/)
- [Cypher Refcard](https://neo4j.com/docs/cypher-refcard/current/)
- [APOC Documentation](https://neo4j.com/labs/apoc/4.4/)
- [Graph Data Science Library Documentation](https://neo4j.com/docs/graph-data-science/current/)
- [Neo4j Cypher CheatSheet](https://neo4j.com/docs/cypher-cheat-sheet/current/)

---

## Autoevaluación

### Preguntas Conceptuales

1. Explica la diferencia entre `MATCH` y `OPTIONAL MATCH`. ¿En qué situaciones usarías cada uno?

2. ¿Cuál es la diferencia entre `MERGE` y `CREATE`? Proporciona un ejemplo de caso de uso para cada uno.

3. Describe el propósito de la cláusula `WITH` en Cypher y por qué es importante para consultas complejas.

4. Explica cómo se manejan los recorridos variables de longitud en Cypher y qué precauciones deberías tomar al usarlos.

### Ejercicios Prácticos

Utilizando la base de datos de ejemplo "Movies" (o la base de datos que hayas creado en los módulos anteriores), completa las siguientes tareas:

1. Escribe una consulta para encontrar el "actor más conectado" (aquel que ha trabajado con la mayor cantidad de otros actores).

2. Crea una consulta que muestre para cada director:
   - Su nombre
   - Número total de películas dirigidas
   - Año de su primera y última película
   - Géneros en los que ha trabajado
   - Actores con los que ha trabajado más frecuentemente

3. Implementa una recomendación simple de películas:
   - Dada una película que le gusta a un usuario
   - Encuentra otras películas con actores en común o del mismo género
   - Ordena por relevancia (más factores en común = mayor relevancia)

4. Escribe un procedimiento de importación que:
   - Cree varios nodos nuevos a partir de datos proporcionados
   - Establezca relaciones entre ellos basadas en ciertos criterios
   - Asegure que no se crean duplicados
   - Actualice nodos existentes si es necesario
