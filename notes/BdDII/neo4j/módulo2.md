# Módulo 2: Modelo de Datos en Neo4j

## 1. Nodos y Relaciones

### Conceptos Fundamentales de los Nodos

Un **nodo** es la unidad básica de representación de datos en Neo4j. Los nodos representan entidades en nuestro dominio de datos, como personas, productos, eventos o lugares.

#### Características de los Nodos:

- **Identidad única**: Cada nodo tiene un identificador único generado por Neo4j
- **Autodescriptivos**: Contienen las propiedades que los describen
- **Pueden tener múltiples etiquetas**: Para categorizar y agrupar nodos similares
- **Son contenedores independientes**: No necesitan referencias a otros nodos para existir

#### Representación gráfica:
```
(variable:Etiqueta {propiedad1: "valor", propiedad2: valor})
```

Ejemplo:
```
(john:Person {name: "John Smith", age: 42, city: "New York"})
```

### Conceptos Fundamentales de las Relaciones

Una **relación** representa una conexión entre dos nodos. Las relaciones son direccionales y siempre tienen un nodo de inicio y un nodo de fin.

#### Características de las Relaciones:

- **Siempre dirigidas**: Tienen un sentido definido (inicio → fin)
- **Siempre tienen un tipo**: Describe la naturaleza de la conexión
- **Pueden tener propiedades**: Atributos que describen la relación
- **No pueden existir sin nodos**: Una relación siempre debe conectar dos nodos existentes

#### Representación gráfica:
```
(nodoA)-[variable:TIPO_RELACION {propiedad1: valor}]->(nodoB)
```

Ejemplo:
```
(john:Person)-[r:WORKS_AT {since: 2018, role: "Developer"}]->(company:Company)
```

### Diferencia con Modelos Relacionales

En bases de datos relacionales, las relaciones se modelan implícitamente a través de claves foráneas y tablas de unión. En Neo4j, las relaciones son:

- **Entidades de primera clase**: Existen por sí mismas, con su propio identificador único
- **Navegables directamente**: No requieren joins para ser recorridas
- **Semánticamente significativas**: El tipo de relación es parte integral del modelo de datos
- **Almacenadas físicamente como conexiones**: No como referencias indirectas

### Ejemplos Prácticos

#### Red Social
```
(alice:Person {name: "Alice"})-[:FRIEND_OF {since: 2020}]->(bob:Person {name: "Bob"})
(bob)-[:FRIEND_OF {since: 2019}]->(charlie:Person {name: "Charlie"})
(alice)-[:LIVES_IN]->(nyc:City {name: "New York"})
(bob)-[:LIVES_IN]->(chicago:City {name: "Chicago"})
```

#### E-commerce
```
(customer:Customer)-[:PURCHASED {date: "2023-05-15"}]->(product:Product)
(product)-[:BELONGS_TO]->(category:Category)
(customer)-[:WROTE]->(review:Review)-[:ABOUT]->(product)
```

## 2. Propiedades y Etiquetas

### Propiedades de Nodos

Las propiedades son los atributos que almacenan información sobre nodos y relaciones. Funcionan como pares clave-valor.

#### Tipos de datos soportados:

- **Numéricos**: Integer, Float
- **Texto**: String
- **Booleanos**: true/false
- **Temporales**: Date, DateTime, LocalTime
- **Espaciales**: Point
- **Estructurados**: Listas de valores simples (no listas de objetos)

#### Limitaciones:

- No se permiten valores NULL (se deben omitir las propiedades en su lugar)
- No se permiten objetos anidados (aunque se pueden simular con listas)
- No hay tipo específico para Binary Large Objects (se recomienda almacenar solo las referencias)

#### Ejemplos:

```cypher
CREATE (p:Person {
    name: "John Smith",
    age: 42,
    height: 1.85,
    active: true,
    hobbies: ["running", "reading", "cooking"],
    birthdate: date("1980-04-15"),
    lastLogin: datetime("2023-05-17T14:25:36")
})
```

### Propiedades de Relaciones

Las relaciones también pueden tener propiedades, que describen aspectos de la conexión entre nodos.

#### Usos comunes:

- **Información temporal**: Cuándo se estableció la relación
- **Pesos o fuerza**: En redes ponderadas
- **Metadatos**: Información sobre cómo se creó o validó la relación
- **Atributos calificativos**: Información específica sobre la naturaleza de la relación

#### Ejemplo:

```cypher
CREATE (alice:Person {name: "Alice"})-[:RATED {
    score: 4.5,
    date: date("2023-01-10"),
    comment: "Excellent product",
    verified: true
}]->(product:Product {name: "Smartphone X"})
```

### Etiquetas

Las etiquetas son marcadores que se aplican a los nodos para categorizarlos. Una etiqueta representa un conjunto o grupo de nodos.

#### Funciones de las etiquetas:

- **Agrupación**: Agrupar nodos similares
- **Clasificación**: Implementar jerarquías o taxonomías
- **Indexación**: Optimizar consultas sobre grupos específicos
- **Restricciones**: Aplicar reglas de integridad a conjuntos de nodos

#### Características:

- Un nodo puede tener múltiples etiquetas (0 o más)
- Las etiquetas se usan comúnmente para representar "clases" o "tipos" de entidades
- Son importantes para el rendimiento de las consultas

#### Ejemplos:

```cypher
// Nodo con una etiqueta
CREATE (p:Person {name: "John"})

// Nodo con múltiples etiquetas
CREATE (p:Person:Employee:Manager {name: "Sarah"})

// Consulta utilizando etiqueta
MATCH (p:Person) RETURN p

// Agregar etiqueta a un nodo existente
MATCH (p:Person {name: "John"})
SET p:Customer
```

### Multi-etiquetado y Herencia

A diferencia de las bases de datos relacionales, Neo4j permite implementar conceptos de herencia a través del multi-etiquetado:

```cypher
// Crear diferentes tipos de vehículos
CREATE (c:Vehicle:Car {wheels: 4, brand: "Toyota"})
CREATE (b:Vehicle:Bicycle {wheels: 2, type: "Mountain"})
CREATE (t:Vehicle:Truck:Commercial {wheels: 18, maxLoad: 5000})

// Consulta que retorna todos los vehículos
MATCH (v:Vehicle) RETURN v

// Consulta que retorna solo camiones
MATCH (t:Truck) RETURN t
```

## 3. Diseño de Modelos de Grafos

### Principios de Modelado

El modelado de grafos se basa en cuatro principios fundamentales:

1. **Modelo dirigido por las preguntas**: Comenzar con las preguntas que queremos responder
2. **Modelado incremental**: Construir el modelo de forma iterativa, añadiendo complejidad según sea necesario
3. **Optimización por patrones de acceso**: Estructurar el grafo según cómo se accederá a los datos
4. **Garantizar la trazabilidad semántica**: Mantener la claridad sobre el significado de cada elemento

### Proceso de Diseño

#### 1. Identificar Entidades del Dominio

Comenzar identificando las entidades principales del dominio y mapearlas a nodos con etiquetas:

```
- Clientes (Customer)
- Productos (Product)
- Pedidos (Order)
- Categorías (Category)
- Proveedores (Supplier)
```

#### 2. Identificar Relaciones entre Entidades

Determinar cómo se relacionan estas entidades entre sí:

```
- Cliente REALIZA Pedido
- Pedido CONTIENE Producto
- Producto PERTENECE_A Categoría
- Proveedor SUMINISTRA Producto
```

#### 3. Identificar Propiedades

Determinar qué atributos caracterizan a cada entidad y relación:

```
- Cliente: id, nombre, email, dirección
- Producto: id, nombre, precio, stock
- Pedido: id, fecha, estado, total
- REALIZA: fecha, método de pago
- CONTIENE: cantidad, precio unitario
```

#### 4. Evaluar Patrones de Consulta

Adaptar el modelo para optimizar las consultas más frecuentes o críticas:

```
- ¿Qué productos ha comprado un cliente?
- ¿Qué clientes han comprado un producto específico?
- ¿Cuáles son los productos más vendidos por categoría?
```

### Transformación desde Modelos Relacionales

#### Tablas → Nodos

Cada tabla principal típicamente se convierte en un tipo de nodo (etiqueta):
- Tabla `customers` → Nodos con etiqueta `:Customer`
- Tabla `products` → Nodos con etiqueta `:Product`

#### Claves Foráneas → Relaciones

Las claves foráneas se transforman en relaciones directas:
- FK `order.customer_id` → Relación `(:Customer)-[:PLACED]->(:Order)`

#### Tablas de Unión → Relaciones con Propiedades

Las tablas de unión se convierten en relaciones con propiedades:
- Tabla `order_items` → Relación `(:Order)-[:CONTAINS {quantity: 5, price: 9.99}]->(:Product)`

### Ejemplo: Transformación de E-commerce

#### Modelo Relacional
```
customers (id, name, email)
products (id, name, price, category_id)
categories (id, name)
orders (id, customer_id, date, status)
order_items (order_id, product_id, quantity, price)
```

#### Modelo de Grafo
```cypher
// Crear clientes
CREATE (c:Customer {id: 1, name: "Alice", email: "alice@example.com"})

// Crear categorías
CREATE (cat:Category {id: 1, name: "Electronics"})

// Crear productos
CREATE (p:Product {id: 1, name: "Smartphone", price: 699.99})

// Crear pedidos
CREATE (o:Order {id: 1, date: "2023-05-15", status: "Delivered"})

// Establecer relaciones
MATCH (c:Customer {id: 1}), (o:Order {id: 1})
CREATE (c)-[:PLACED {paymentMethod: "Credit Card"}]->(o)

MATCH (p:Product {id: 1}), (cat:Category {id: 1})
CREATE (p)-[:BELONGS_TO]->(cat)

MATCH (o:Order {id: 1}), (p:Product {id: 1})
CREATE (o)-[:CONTAINS {quantity: 1, price: 699.99}]->(p)
```

## 4. Mejores Prácticas de Modelado

### Patrones de Diseño Comunes

#### 1. Etiquetado Semántico

Usar etiquetas que reflejen claramente los conceptos del dominio:

```cypher
CREATE (p:Product:Electronics:Featured {name: "Smartphone X"})
```

#### 2. Relaciones Bidireccionales

Para relaciones que necesitan navegarse en ambas direcciones, crear dos relaciones explícitas:

```cypher
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CREATE (a)-[:KNOWS]->(b)
CREATE (b)-[:KNOWS]->(a)
```

#### 3. Hipernodos

Para manejar relaciones con alta cardinalidad (nodos con miles de conexiones):

```cypher
// En lugar de conectar directamente miles de usuarios a un producto popular
MATCH (p:Product {id: "popular-item"})
CREATE (h:ProductGroup {productId: p.id})
CREATE (p)-[:HAS_GROUP]->(h)

// Luego conectar usuarios al hipernodo
MATCH (u:User), (h:ProductGroup {productId: "popular-item"})
CREATE (u)-[:LIKED]->(h)
```

#### 4. Relaciones Compuestas

Para representar relaciones entre más de dos entidades:

```cypher
// Estudiante tomó un curso con un profesor específico
MATCH (s:Student), (c:Course), (t:Teacher)
CREATE (s)-[:TOOK {grade: "A", teacher: t.id}]->(c)

// O usando un nodo intermedio para mayor complejidad
CREATE (e:Enrollment {grade: "A", semester: "Fall 2023"})
CREATE (s)-[:HAS_ENROLLMENT]->(e)
CREATE (e)-[:FOR_COURSE]->(c)
CREATE (e)-[:WITH_TEACHER]->(t)
```

### Anti-patrones a Evitar

#### 1. Sobre-normalización

**Anti-patrón**: Crear demasiados nodos pequeños y específicos.

**Problema**: Aumenta las traversías necesarias y reduce el rendimiento.

**Solución**: Equilibrar entre normalización y redundancia según patrones de acceso.

```cypher
// En lugar de crear nodos separados para cada dirección
CREATE (c:Customer {
    id: 1, 
    name: "Alice",
    // Dirección como propiedades del nodo Cliente
    street: "123 Main St",
    city: "New York",
    zipCode: "10001"
})
```

#### 2. Relaciones Genéricas

**Anti-patrón**: Usar tipos de relaciones no específicas como `:HAS` o `:RELATED_TO`.

**Problema**: Reduce la claridad semántica y requiere filtrado por propiedades.

**Solución**: Usar tipos de relaciones semánticamente precisas.

```cypher
// En lugar de esto
CREATE (p:Person)-[:HAS {type: "car"}]->(c:Car)

// Hacer esto
CREATE (p:Person)-[:OWNS]->(c:Car)
```

#### 3. Listas Complejas como Propiedades

**Anti-patrón**: Almacenar grandes listas de datos complejos como propiedades.

**Problema**: Dificulta la consulta, actualización y el mantenimiento.

**Solución**: Convertir elementos de lista en nodos relacionados.

```cypher
// En lugar de esto
CREATE (p:Product {
    name: "Smartphone",
    reviews: [
        {user: "Alice", rating: 5, text: "Great!"},
        {user: "Bob", rating: 4, text: "Good"}
    ]
})

// Hacer esto
CREATE (p:Product {name: "Smartphone"})
CREATE (r1:Review {rating: 5, text: "Great!"})
CREATE (r2:Review {rating: 4, text: "Good"})
CREATE (u1:User {name: "Alice"})
CREATE (u2:User {name: "Bob"})
CREATE (u1)-[:WROTE]->(r1)-[:ABOUT]->(p)
CREATE (u2)-[:WROTE]->(r2)-[:ABOUT]->(p)
```

#### 4. Ignorar Direccionalidad

**Anti-patrón**: No considerar la dirección de las relaciones en el diseño.

**Problema**: Consultas ineficientes que necesitan dirección bidireccional.

**Solución**: Diseñar direcciones según los patrones de consulta más frecuentes.

```cypher
// Si la consulta típica es encontrar qué productos ha comprado un cliente
CREATE (customer)-[:PURCHASED]->(product)

// Si también es frecuente saber qué clientes compraron un producto
// Considerar índices o relaciones bidireccionales
```

### Modelado para Rendimiento

#### 1. Índices y Restricciones

Crear índices para propiedades consultadas frecuentemente:

```cypher
// Crear índice para una propiedad de búsqueda común
CREATE INDEX product_name FOR (p:Product) ON (p.name)

// Crear índice compuesto
CREATE INDEX customer_location FOR (c:Customer) ON (c.city, c.country)

// Crear restricción de unicidad
CREATE CONSTRAINT customer_email_unique FOR (c:Customer) REQUIRE c.email IS UNIQUE
```

#### 2. Denormalización Estratégica

Duplicar datos para optimizar patrones de acceso comunes:

```cypher
// Almacenar cantidad de amigos como propiedad calculada
MATCH (p:Person)-[:FRIEND]->(friend)
WITH p, count(friend) as friendCount
SET p.friendCount = friendCount

// Esto permite consultas más eficientes
MATCH (p:Person)
WHERE p.friendCount > 10
RETURN p
```

#### 3. Distribución de Carga

Evitar nodos sobrecargados (con miles o millones de relaciones):

```cypher
// En lugar de etiquetar directamente millones de transacciones por año
CREATE (y2023:Year {year: 2023})

// Crear nodos por mes
MATCH (y:Year {year: 2023})
FOREACH (month IN range(1,12) |
    CREATE (m:Month {month: month, year: 2023})
    CREATE (m)-[:PART_OF]->(y)
)

// Conectar transacciones a su mes específico
MATCH (t:Transaction {date: "2023-05-17"})
MATCH (m:Month {month: 5, year: 2023})
CREATE (t)-[:OCCURRED_IN]->(m)
```

## Ejercicios Prácticos

### Ejercicio 1: Modelado Básico

1. Crea un modelo de grafo para un sistema de biblioteca con:
   - Libros (título, ISBN, año de publicación)
   - Autores (nombre, nacionalidad)
   - Usuarios (nombre, email)
   - Categorías (nombre)
   - Préstamos (fecha de préstamo, fecha de devolución)

2. Implementa este modelo en Neo4j con al menos:
   - 5 libros
   - 3 autores
   - 4 usuarios
   - 3 categorías
   - Relaciones apropiadas entre ellos

### Ejercicio 2: Transformación de Modelo Relacional

Dado el siguiente esquema relacional de un sistema de gestión escolar:

```
students (id, name, email, graduation_year)
courses (id, name, credits, department_id)
departments (id, name, building)
enrollments (student_id, course_id, semester, grade)
professors (id, name, email, department_id)
teaching (professor_id, course_id, semester)
```

1. Diseña un modelo de grafo equivalente
2. Implementa una versión simplificada con datos de ejemplo
3. Escribe consultas Cypher que respondan a:
   - ¿Qué estudiantes están matriculados en un curso específico?
   - ¿Qué profesor enseña más cursos?
   - ¿Qué cursos tiene un departamento específico?

### Ejercicio 3: Mejora de Modelo

Dado un modelo simple de red social:

```cypher
CREATE (alice:Person {name: "Alice"})
CREATE (bob:Person {name: "Bob"})
CREATE (charlie:Person {name: "Charlie"})
CREATE (dave:Person {name: "Dave"})

CREATE (alice)-[:FRIEND]->(bob)
CREATE (bob)-[:FRIEND]->(alice)
CREATE (bob)-[:FRIEND]->(charlie)
CREATE (charlie)-[:FRIEND]->(bob)
CREATE (alice)-[:FRIEND]->(charlie)
CREATE (charlie)-[:FRIEND]->(alice)
CREATE (dave)-[:FRIEND]->(alice)
CREATE (alice)-[:FRIEND]->(dave)
```

1. Mejora este modelo para incluir:
   - Propiedades adicionales en los nodos Person (edad, ciudad, intereses)
   - Propiedades en las relaciones FRIEND (desde cuándo, cómo se conocieron)
   - Una nueva relación LIVES_IN hacia nodos City
   - Una nueva relación INTERESTED_IN hacia nodos Hobby

2. Implementa los cambios en Neo4j

3. Escribe una consulta para encontrar:
   - Amigos de amigos que viven en la misma ciudad
   - Personas que comparten al menos dos intereses

## Recursos Adicionales

- [Neo4j Graph Database Design](https://neo4j.com/developer/guide-data-modeling/)
- [Graph Data Modeling Guidelines](https://neo4j.com/docs/getting-started/current/data-modeling/)
- [Graph Data Modeling Book](https://neo4j.com/graph-data-modeling-book/)
- [Refactoring and Migrating Relational Databases to Graphs](https://neo4j.com/blog/relational-to-graph-data-modeling/)

---

## Autoevaluación de conocimientos

### Preguntas Conceptuales

1. Explica las diferencias entre las propiedades de los nodos y las propiedades de las relaciones. ¿Cuándo deberías usar cada una?

2. ¿Cuál es la importancia de las etiquetas en Neo4j y cómo afectan al rendimiento de las consultas?

3. Describe dos anti-patrones comunes en el modelado de grafos y explica cómo evitarlos.

4. Compara las estrategias de modelado de una relación muchos-a-muchos en un modelo relacional vs. en Neo4j.

### Ejercicio Práctico

Diseña e implementa un modelo de grafo para un sistema de comercio electrónico que incluya:

1. Entidades:
   - Clientes con información de perfil
   - Productos con detalles
   - Pedidos con fechas e información de pago
   - Categorías para los productos
   - Reseñas de productos

2. Relaciones:
   - Cliente realiza pedidos
   - Pedidos contienen productos
   - Clientes escriben reseñas sobre productos
   - Productos pertenecen a categorías
   - Clientes pueden seguir a otros clientes

3. Requisitos adicionales:
   - Implementa al menos un índice relevante
   - Incluye al menos una restricción de unicidad
   - Usa múltiples etiquetas para al menos un tipo de nodo
   - Demuestra un caso de denormalización estratégica

Se espera que utilices código Cypher para crear el modelo e
implementes al menos 5 consultas que demuestren la utilidad del modelo.
Observa el grafo resultante y analiza si es correcto.