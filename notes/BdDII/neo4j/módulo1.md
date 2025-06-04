# Módulo 1: Fundamentos de Bases de Datos de Grafos

## 1. Introducción a Bases de Datos de Grafos

### ¿Qué es una Base de Datos de Grafos?

Una base de datos de grafos es un tipo de base de datos NoSQL diseñada para almacenar, consultar y manipular datos altamente interconectados. A diferencia de las bases de datos relacionales tradicionales que organizan la información en tablas, las bases de datos de grafos representan los datos como una colección de:

- **Nodos**: Entidades o "cosas" (equivalentes a registros en una base relacional)
- **Relaciones**: Conexiones entre nodos (equivalentes a las relaciones entre tablas)
- **Propiedades**: Atributos asociados tanto a nodos como a relaciones

Esta estructura refleja naturalmente cómo pensamos sobre la información en el mundo real - como entidades conectadas entre sí mediante diferentes tipos de relaciones.

### Historia y Evolución

- **Origen teórico**: Las bases de datos de grafos tienen sus raíces en la teoría de grafos, una rama de las matemáticas que se remonta al siglo XVIII con el problema de los puentes de Königsberg resuelto por Leonhard Euler.

- **Primeras implementaciones (1960s-1970s)**: Los primeros sistemas de gestión de redes jerárquicas y bases de datos de red como IDS y CODASYL pueden considerarse precursores.

- **Bases de datos semánticas (1980s-1990s)**: Desarrollo de bases de datos orientadas a objetos y sistemas basados en RDF.

- **Era moderna (2000s-presente)**: Surgimiento de Neo4j (2007) como la primera base de datos de grafos de propósito general y comercial, seguida por otras soluciones como ArangoDB, Amazon Neptune, JanusGraph, etc.

## 2. Ventajas sobre Bases de Datos Relacionales

### Rendimiento con Datos Conectados

- **Consultas de relaciones**: Las bases de datos de grafos superan significativamente a las relacionales en consultas que implican múltiples joins. Mientras que el rendimiento de las bases relacionales se degrada exponencialmente con cada join adicional, las bases de grafos mantienen tiempos de respuesta constantes independientemente de la profundidad de las conexiones.

- **Ejemplo práctico**: Encontrar "amigos de amigos" hasta 3 niveles de profundidad:
  - En SQL: Múltiples joins autocorreferenciados que se vuelven extremadamente costosos
  - En Cypher (Neo4j): Simple consulta `MATCH (person)-[:FRIEND*1..3]->(friend) RETURN friend`

### Modelo de Datos Flexible

- **Esquema flexible**: No se requiere definir un esquema rígido por adelantado. Los nodos pueden tener diferentes propiedades incluso dentro de la misma categoría.

- **Evolución natural**: Se pueden añadir nuevos tipos de relaciones y propiedades sin afectar a los datos existentes ni requerir migraciones complejas.

### Representación Intuitiva

- **Modelado cercano al dominio**: La estructura de grafo refleja directamente los modelos mentales que usamos para entender dominios complejos.

- **Comprensión visual**: Los datos pueden visualizarse y comprenderse de forma natural como diagramas de entidades conectadas.

### Casos Comparativos

| Escenario | Base de Datos Relacional | Base de Datos de Grafos |
|-----------|--------------------------|-------------------------|
| Añadir nueva propiedad | Requiere ALTER TABLE, potencialmente afecta a todos los registros | Simplemente se añade a los nodos necesarios |
| Consulta de relaciones profundas | Complejidad O(n^depth) con múltiples joins | Complejidad O(n) independiente de la profundidad |
| Modelado de relaciones muchos-a-muchos | Requiere tablas de unión adicionales | Las relaciones son ciudadanos de primera clase |
| Travesías de datos | Complejas de expresar en SQL | Naturales y concisas en lenguajes como Cypher |

## 3. Casos de Uso de Neo4j

### Redes Sociales y Análisis de Comunidades

- **Recomendación de amigos/conexiones**: Encontrar amigos de amigos, conexiones comunes
- **Análisis de influencia**: Identificar líderes de opinión y difusores de información
- **Detección de comunidades**: Encontrar grupos de usuarios con intereses similares
- **Ejemplo real**: LinkedIn utiliza grafos para sus recomendaciones "Personas que quizás conozcas"

### Motores de Recomendación

- **Recomendaciones basadas en comportamiento**: "Las personas que compraron X también compraron Y"
- **Recomendaciones contextuales**: Combinación de preferencias de usuario, comportamiento y características de productos
- **Ejemplo real**: Empresas como Walmart y eBay utilizan Neo4j para motores de recomendación personalizados

### Detección de Fraude y Análisis de Riesgos

- **Identificación de patrones sospechosos**: Relaciones ocultas entre cuentas, transacciones y entidades
- **Análisis de rutas**: Seguimiento del flujo de dinero a través de múltiples cuentas
- **Ejemplo real**: Instituciones financieras como Standard Chartered Bank utilizan Neo4j para detectar fraudes

### Gestión de Identidad y Accesos

- **Control de acceso basado en grafos**: Modelado de jerarquías organizacionales complejas
- **Análisis de permisos**: Identificación de accesos excesivos o inapropiados
- **Ejemplo real**: Cisco utiliza Neo4j para gestionar su estructura de control de acceso

### Gestión de Redes y Data Centers

- **Mapeo de infraestructura IT**: Visualización de dependencias entre servidores, aplicaciones y servicios
- **Análisis de impacto**: Predicción de efectos cascada de fallos de componentes
- **Ejemplo real**: Administradores de sistemas en empresas como Cisco utilizan Neo4j para modelar infraestructuras complejas

### Bioinformática y Ciencias de la Vida

- **Redes de proteínas**: Modelado de interacciones entre proteínas
- **Investigación farmacéutica**: Descubrimiento de compuestos para el desarrollo de medicamentos
- **Ejemplo real**: Proyectos como el consorcio de la Universidad de Cambridge utilizan Neo4j para investigación genómica

## 4. Instalación y Configuración de Neo4j

### Opciones de Instalación

#### Neo4j Desktop (Recomendado para desarrollo)

1. **Descarga**:
   - Visita [neo4j.com/download](https://neo4j.com/download/)
   - Selecciona Neo4j Desktop para tu sistema operativo (Windows, macOS, Linux)

2. **Instalación**:
   - Windows: Ejecuta el instalador y sigue las instrucciones
   - macOS: Arrastra Neo4j Desktop a la carpeta Aplicaciones
   - Linux: Sigue las instrucciones específicas de la distribución

3. **Primer uso**:
   - Crea una cuenta gratuita de Neo4j o inicia sesión
   - Crea un nuevo proyecto en Neo4j Desktop

#### Neo4j Sandbox (Sin instalación)

- Accede a [neo4j.com/sandbox](https://neo4j.com/sandbox/)
- Crea una cuenta y selecciona una plantilla de proyecto (vacía o prepoblada)
- Ideal para pruebas rápidas sin instalación local

#### Neo4j Aura (Servicio en la nube)

- Versión gestionada en la nube de Neo4j
- Ofrece un nivel gratuito para proyectos pequeños
- Configuración sencilla a través de [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura/)

### Creación de una Base de Datos en Neo4j Desktop

1. **Crear un nuevo proyecto**:
   - Clic en "Nuevo Proyecto"
   - Asigna un nombre descriptivo

2. **Añadir una base de datos**:
   - Dentro del proyecto, clic en "Añadir → Local DBMS"
   - Establece un nombre para la base de datos
   - Selecciona la versión de Neo4j (recomendada la última versión estable)
   - Establece una contraseña (recuérdala, la necesitarás para conectarte)

3. **Iniciar la base de datos**:
   - Clic en "Start" para iniciar el servidor
   - El indicador cambiará a verde cuando esté en funcionamiento

### Explorar Neo4j Browser

Neo4j Browser es la interfaz web principal para interactuar con Neo4j:

1. **Acceso**:
   - En Neo4j Desktop, clic en "Open" junto a Neo4j Browser
   - O accede vía http://localhost:7474 en tu navegador

2. **Autenticación**:
   - Usuario por defecto: neo4j
   - Contraseña: la que estableciste al crear la base de datos

3. **Elementos principales de la interfaz**:
   - Editor de comandos (arriba): Para escribir consultas Cypher
   - Panel de resultados (centro): Visualización de resultados como grafos o tablas
   - Barra de información (izquierda): Acceso a documentación, ejemplos y metadatos

4. **Comandos útiles para empezar**:
   - `:help` - Muestra ayuda general
   - `:play intro` - Tutorial interactivo de introducción
   - `:play movies` - Carga y explora la base de datos de ejemplo Movies
   - `:schema` - Muestra el esquema actual de la base de datos

### Configuración Básica

#### Ajustes de Memoria

Para proyectos de desarrollo, los valores por defecto suelen ser suficientes. Para producción:

```
// En neo4j.conf:
dbms.memory.heap.initial_size=1G
dbms.memory.heap.max_size=4G
```

#### Puertos

Neo4j utiliza varios puertos por defecto:
- 7474: HTTP para Neo4j Browser
- 7473: HTTPS
- 7687: Bolt (protocolo binario para drivers)

Para cambiarlos:

```
// En neo4j.conf:
dbms.connector.http.listen_address=:7474
dbms.connector.https.listen_address=:7473
dbms.connector.bolt.listen_address=:7687
```

## Ejercicios Prácticos

### Ejercicio 1: Instalación y Verificación

1. Instala Neo4j Desktop siguiendo las instrucciones anteriores
2. Crea un nuevo proyecto llamado "CursoNeo4j"
3. Crea una base de datos local con la última versión estable
4. Inicia la base de datos y abre Neo4j Browser
5. Ejecuta el comando `:play intro` y completa el primer apartado del tutorial

### Ejercicio 2: Exploración del Modelo de Películas

1. Carga la base de datos de ejemplo Movies con el comando `:play movies`
2. Sigue las instrucciones para cargar el conjunto de datos
3. Ejecuta la consulta: `MATCH (n) RETURN n LIMIT 25`
4. Explora el grafo resultante: identifica tipos de nodos y relaciones
5. Intenta responder: ¿Cuántos tipos de nodos diferentes hay? ¿Qué relaciones existen entre ellos?

## Recursos Adicionales

- [Documentación oficial de Neo4j](https://neo4j.com/docs/)
- [Neo4j Sandbox](https://neo4j.com/sandbox/) para experimentar con conjuntos de datos preconfigurados
- [Neo4j Developer Portal](https://neo4j.com/developer/) con tutoriales y recursos de aprendizaje
- [Neo4j Community Site](https://community.neo4j.com/) para preguntas y soporte

---

## Ejercicios para afianzar conocimientos

### Preguntas Conceptuales

1. Explica las diferencias fundamentales entre una base de datos relacional y una base de datos de grafos.
2. ¿Qué problemas específicos resuelve Neo4j mejor que las bases de datos relacionales tradicionales?
3. Describe tres casos de uso reales donde Neo4j sería la opción óptima. Justifica tu respuesta.
4. Explica cómo afecta el rendimiento la profundidad de las relaciones en consultas de bases de datos de grafos vs. relacionales.

### Ejercicios Prácticos

1. Instala Neo4j y realiza esto:
   - Crear una nueva base de datos
   - Conectarte a través de Neo4j Browser
   - Ejecutar comandos básicos de ayuda

2. En la base de datos de ejemplo Movies:
   - Encuentra todas las personas que dirigieron películas
   - Encuentra todas las películas lanzadas en un año específico
   - Documenta los pasos que seguiste y los resultados obtenidos

.