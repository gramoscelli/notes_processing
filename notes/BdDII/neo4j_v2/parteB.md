# Parte B: Modelo de Datos y Cypher Básico

## 2.1 Conceptos fundamentales del modelo de grafos

### Nodos (Nodes)
Los nodos representan entidades en tu dominio. Son los "sustantivos" de tu grafo.

**Características:**

- Pueden tener cero o más etiquetas (labels)
- Pueden tener cero o más propiedades
- Cada nodo tiene un ID único interno

**Ejemplo:**
```cypher
// Nodo simple
(persona)

// Nodo con etiqueta
(persona:Persona)

// Nodo con múltiples etiquetas
(juan:Persona:Empleado)

// Nodo con propiedades
(juan:Persona {nombre: 'Juan', edad: 30, email: 'juan@email.com'})
```

### Relaciones (Relationships)
Las relaciones conectan nodos y representan cómo las entidades se relacionan entre sí.

**Características:**
- Siempre tienen dirección (aunque puedes ignorarla en consultas)
- Tienen exactamente un tipo
- Pueden tener propiedades
- Conectan exactamente dos nodos (origen y destino)

**Ejemplo:**
```cypher
// Relación simple
(juan)-[:CONOCE]->(maria)

// Relación con propiedades
(juan)-[:CONOCE {desde: '2020-01-15', confianza: 8}]->(maria)

// Relación bidireccional (dos relaciones)
(juan)-[:AMIGO_DE]->(maria)
(maria)-[:AMIGO_DE]->(juan)
```

### Propiedades (Properties)
Almacenan información sobre nodos y relaciones.

**Tipos de datos soportados:**
- `String`: texto
- `Integer`: números enteros
- `Float`: números decimales
- `Boolean`: verdadero/falso
- `Date/DateTime/Time`: fechas y tiempos
- `Point`: coordenadas geográficas
- `Lists`: arrays de los tipos anteriores

**Ejemplos:**
```cypher
// Propiedades de diferentes tipos
CREATE (producto:Producto {
    nombre: 'Laptop Dell',           // String
    precio: 899.99,                  // Float
    stock: 15,                       // Integer
    disponible: true,                // Boolean
    lanzamiento: date('2023-06-15'), // Date
    tags: ['tecnología', 'computación'], // List
    ubicacion: point({latitude: 40.7128, longitude: -74.0060}) // Point
})
```

### Etiquetas (Labels)
Las etiquetas categorizan nodos y son fundamentales para la organización y consulta eficiente.

**Buenas prácticas:**
- Usar PascalCase: `Persona`, `ProductoTecnologico`
- Ser específico pero no excesivo
- Usar sustantivos, no verbos
- Considerar jerarquías: `Persona:Empleado:Gerente`

**Ejemplos:**
```cypher
// Etiquetas jerárquicas
CREATE (ana:Persona:Empleado:Desarrolladora {nombre: 'Ana'})
CREATE (libro:Producto:Libro {titulo: 'Neo4j en Acción'})
CREATE (madrid:Lugar:Ciudad:Capital {nombre: 'Madrid'})
```

## 2.2 Esquema flexible vs estructura

### Ventajas del esquema flexible
```cypher
// Diferentes personas pueden tener diferentes propiedades
CREATE 
  (juan:Persona {nombre: 'Juan', edad: 30, profesion: 'Ingeniero'}),
  (maria:Persona {nombre: 'María', telefono: '+34-666-123-456', direccion: 'Madrid'}),
  (empresa:Organizacion {nombre: 'TechCorp', empleados: 500, fundada: 1995}),
  (juan)-[:TRABAJA_EN {desde: 2020, cargo: 'Senior Developer'}]->(empresa),
  (maria)-[:CONSULTA_PARA {proyecto: 'Web Redesign'}]->(empresa);
```

### Cuándo usar constraints y validaciones
```cypher
// Crear constraints para integridad de datos
CREATE CONSTRAINT persona_email_unique FOR (p:Persona) REQUIRE p.email IS UNIQUE
CREATE CONSTRAINT producto_codigo_unique FOR (p:Producto) REQUIRE p.codigo IS UNIQUE

// Indexes para rendimiento
CREATE INDEX persona_nombre FOR (p:Persona) ON (p.nombre)
CREATE INDEX producto_categoria FOR (p:Producto) ON (p.categoria)
```

## 2.3 Cypher - Primeros pasos

### ¿Qué es Cypher?
Cypher es el lenguaje de consulta declarativo de Neo4j, inspirado en SQL pero diseñado específicamente para grafos.

### Sintaxis básica: Patrones ASCII Art
Cypher usa una sintaxis visual que imita cómo dibujarías un grafo:

```cypher
// Nodos se representan con paréntesis
(n)

// Relaciones se representan con corchetes y flechas
(a)-[r]->(b)

// Ejemplo completo
(juan:Persona)-[:CONOCE {desde: 2020}]->(maria:Persona)
```

### CREATE - Crear datos

**Crear nodos:**
```cypher
// Nodo simple
CREATE (n)

// Nodo con etiqueta
CREATE (p:Persona)

// Nodo con propiedades
CREATE (juan:Persona {nombre: 'Juan', edad: 30})

// Múltiples nodos
CREATE 
  (juan:Persona {nombre: 'Juan', edad: 30}),
  (maria:Persona {nombre: 'María', edad: 28}),
  (carlos:Persona {nombre: 'Carlos', edad: 35})
```

**Crear relaciones:**
```cypher
// Primero crear nodos
CREATE (juan:Persona {nombre: 'Juan'})
CREATE (maria:Persona {nombre: 'María'})

// Luego crear relación
MATCH (j:Persona {nombre: 'Juan'}), (m:Persona {nombre: 'María'})
CREATE (j)-[:CONOCE]->(m)

// O crear todo junto
CREATE (juan:Persona {nombre: 'Juan'})-[:CONOCE]->(maria:Persona {nombre: 'María'})
```

### MATCH - Encontrar patrones

**Encontrar nodos:**
```cypher
// Todos los nodos
MATCH (n) RETURN n

// Nodos con etiqueta específica
MATCH (p:Persona) RETURN p

// Nodos con propiedades específicas
MATCH (p:Persona {nombre: 'Juan'}) RETURN p

// Usando variables
MATCH (p:Persona) 
WHERE p.edad > 25 
RETURN p.nombre, p.edad
```

**Encontrar relaciones:**
```cypher
// Relaciones salientes
MATCH (p:Persona)-[:CONOCE]->(amigo) 
RETURN p.nombre, amigo.nombre

// Relaciones entrantes
MATCH (p:Persona)<-[:CONOCE]-(quien_lo_conoce) 
RETURN p.nombre, quien_lo_conoce.nombre

// Relaciones bidireccionales (ignorar dirección)
MATCH (p:Persona)-[:CONOCE]-(conectado) 
RETURN p.nombre, conectado.nombre

// Múltiples saltos
MATCH (p:Persona)-[:CONOCE]->()-[:CONOCE]->(amigo_de_amigo)
RETURN p.nombre, amigo_de_amigo.nombre
```

### RETURN - Devolver resultados

```cypher
// Devolver nodos completos
MATCH (p:Persona) RETURN p

// Devolver propiedades específicas
MATCH (p:Persona) RETURN p.nombre, p.edad

// Usar alias
MATCH (p:Persona) RETURN p.nombre AS nombre, p.edad AS edad

// Devolver expresiones
MATCH (p:Persona) RETURN p.nombre, p.edad, p.edad + 10 AS edad_en_10_años

// Devolver valores únicos
MATCH (p:Persona) RETURN DISTINCT p.ciudad
```

## 2.4 Patrones de grafos

### Patrones básicos
```cypher
// Patrón simple: nodo
(n)

// Patrón: nodo con relación
(a)-[r]->(b)

// Patrón: cadena
(a)-[r1]->(b)-[r2]->(c)

// Patrón: múltiples relaciones desde un nodo
(centro)-[:REL1]->(a), (centro)-[:REL2]->(b)
```

### Patrones complejos
```cypher
// Triángulo (tres nodos completamente conectados)
MATCH (a)-[:CONOCE]->(b)-[:CONOCE]->(c)-[:CONOCE]->(a)
RETURN a, b, c

// Camino variable (1 a 3 saltos)
MATCH (inicio)-[:CONOCE*1..3]->(fin)
WHERE inicio.nombre = 'Juan'
RETURN fin.nombre

// Múltiples tipos de relaciones
MATCH (p:Persona)-[:TRABAJA_EN|:ESTUDIA_EN]->(lugar)
RETURN p.nombre, lugar.nombre
```

### Ejemplo práctico: Red de colaboración
```cypher
// Crear datos de ejemplo
CREATE 
  (ana:Persona {nombre: 'Ana', profesion: 'Desarrolladora'}),
  (bob:Persona {nombre: 'Bob', profesion: 'Diseñador'}),
  (carlos:Persona {nombre: 'Carlos', profesion: 'Product Manager'}),
  (diana:Persona {nombre: 'Diana', profesion: 'QA Tester'}),
  
  (proyecto1:Proyecto {nombre: 'App Móvil', estado: 'En desarrollo'}),
  (proyecto2:Proyecto {nombre: 'Sitio Web', estado: 'Completado'}),
  
  (ana)-[:COLABORA_EN {rol: 'Lead Developer'}]->(proyecto1),
  (bob)-[:COLABORA_EN {rol: 'UI Designer'}]->(proyecto1),
  (carlos)-[:COLABORA_EN {rol: 'Product Owner'}]->(proyecto1),
  (diana)-[:COLABORA_EN {rol: 'QA Lead'}]->(proyecto1),
  
  (ana)-[:COLABORA_EN {rol: 'Backend Developer'}]->(proyecto2),
  (bob)-[:COLABORA_EN {rol: 'Frontend Designer'}]->(proyecto2),
  
  (ana)-[:CONOCE {desde: '2022-01-15'}]->(bob),
  (bob)-[:CONOCE {desde: '2022-01-15'}]->(ana),
  (ana)-[:CONOCE {desde: '2021-06-10'}]->(carlos),
  (carlos)-[:CONOCE {desde: '2021-06-10'}]->(ana);
```
Eliminar todos los nodos junto con las relaciones:
```cypher
MATCH (p) DETACH DELETE p;
```
## 2.5 Filtrado con WHERE

### Operadores de comparación
```cypher
// Igualdad
MATCH (p:Persona) WHERE p.edad = 30 RETURN p

// Desigualdad
MATCH (p:Persona) WHERE p.edad <> 30 RETURN p
MATCH (p:Persona) WHERE p.edad != 30 RETURN p

// Comparaciones numéricas
MATCH (p:Persona) WHERE p.edad > 25 RETURN p
MATCH (p:Persona) WHERE p.edad >= 30 RETURN p
MATCH (p:Persona) WHERE p.edad < 40 RETURN p
MATCH (p:Persona) WHERE p.edad <= 35 RETURN p
```

### Operadores lógicos
```cypher
// AND
MATCH (p:Persona) 
WHERE p.edad > 25 AND p.profesion = 'Desarrolladora' 
RETURN p

// OR
MATCH (p:Persona) 
WHERE p.edad > 40 OR p.profesion = 'Gerente' 
RETURN p

// NOT
MATCH (p:Persona) 
WHERE NOT p.profesion = 'Estudiante' 
RETURN p
```

### Operadores de cadenas
```cypher
// CONTAINS (contiene)
MATCH (p:Persona) 
WHERE p.nombre CONTAINS 'an' 
RETURN p.nombre

// STARTS WITH (empieza con)
MATCH (p:Persona) 
WHERE p.nombre STARTS WITH 'Ana' 
RETURN p.nombre

// ENDS WITH (termina con)
MATCH (p:Persona) 
WHERE p.email ENDS WITH '@gmail.com' 
RETURN p.nombre, p.email

// Expresiones regulares
MATCH (p:Persona) 
WHERE p.telefono =~ '\\+34.*' 
RETURN p.nombre, p.telefono
```

### Operadores de listas
```cypher
// IN (en lista)
MATCH (p:Persona) 
WHERE p.edad IN [25, 30, 35] 
RETURN p

// Verificar propiedades de listas
MATCH (p:Producto) 
WHERE 'tecnología' IN p.tags 
RETURN p.nombre

// Tamaño de listas
MATCH (p:Producto) 
WHERE size(p.tags) > 2 
RETURN p.nombre, p.tags
```

### Verificar existencia de propiedades
```cypher
// Verificar si existe una propiedad
MATCH (p:Persona) 
WHERE p.email IS NOT NULL 
RETURN p.nombre, p.email

// Verificar si no existe
MATCH (p:Persona) 
WHERE p.telefono IS NULL 
RETURN p.nombre

// Usando EXISTS (Neo4j 4.4+)
MATCH (p:Persona) 
WHERE p.email IS NOT NULL 
RETURN p.nombre
```

## 2.6 Ejercicios prácticos con datasets simples

### Dataset: Biblioteca Universitaria

```cypher
// Limpiar base de datos
MATCH (n) DETACH DELETE n;

// Crear estudiantes
CREATE 
  (ana:Estudiante:Persona {nombre: 'Ana García', carrera: 'Informática', año: 3}),
  (bob:Estudiante:Persona {nombre: 'Bob Smith', carrera: 'Matemáticas', año: 2}),
  (carla:Estudiante:Persona {nombre: 'Carla López', carrera: 'Informática', año: 4}),
  (david:Estudiante:Persona {nombre: 'David Chen', carrera: 'Física', año: 1}),

// Crear profesores
  (prof_martinez:Profesor:Persona {nombre: 'Dr. Martínez', departamento: 'Informática'}),
  (prof_johnson:Profesor:Persona {nombre: 'Dra. Johnson', departamento: 'Matemáticas'}),

// Crear libros
  (libro1:Libro {titulo: 'Introducción a Algoritmos', autor: 'Cormen', año: 2009, isbn: '978-0262033848'}),
  (libro2:Libro {titulo: 'Cálculo Avanzado', autor: 'Stewart', año: 2015, isbn: '978-1285741550'}),
  (libro3:Libro {titulo: 'Bases de Datos Modernas', autor: 'Elmasri', año: 2020, isbn: '978-0133970777'}),
  (libro4:Libro {titulo: 'Física Cuántica', autor: 'Griffiths', año: 2018, isbn: '978-1107179868'}),

// Crear préstamos
  (ana)-[:PIDIO_PRESTADO {fecha: date('2023-09-15'), devolucion: date('2023-10-15')}]->(libro1),
  (ana)-[:PIDIO_PRESTADO {fecha: date('2023-09-20'), devolucion: date('2023-10-20')}]->(libro3),
  (bob)-[:PIDIO_PRESTADO {fecha: date('2023-09-18'), devolucion: date('2023-10-18')}]->(libro2),
  (carla)-[:PIDIO_PRESTADO {fecha: date('2023-09-22'), devolucion: date('2023-10-22')}]->(libro1),
  (david)-[:PIDIO_PRESTADO {fecha: date('2023-09-25'), devolucion: date('2023-10-25')}]->(libro4),

// Profesores recomiendan libros
  (prof_martinez)-[:RECOMIENDA {para_carrera: 'Informática'}]->(libro1),
  (prof_martinez)-[:RECOMIENDA {para_carrera: 'Informática'}]->(libro3),
  (prof_johnson)-[:RECOMIENDA {para_carrera: 'Matemáticas'}]->(libro2);
```

### Ejercicios de consulta

**Ejercicio 1: Consultas básicas**
```cypher
// 1. Encontrar todos los estudiantes
MATCH (e:Estudiante) RETURN e.nombre, e.carrera;

// 2. Encontrar todos los libros prestados
MATCH (estudiante)-[:PIDIO_PRESTADO]->(libro) 
RETURN estudiante.nombre, libro.titulo;

// 3. Encontrar estudiantes de Informática
MATCH (e:Estudiante) 
WHERE e.carrera = 'Informática' 
RETURN e.nombre, e.año;
```

**Ejercicio 2: Filtros complejos**
```cypher
// 4. Estudiantes que pidieron libros después del 20 de septiembre
MATCH (e:Estudiante)-[p:PIDIO_PRESTADO]->(libro) 
WHERE p.fecha > date('2023-09-20') 
RETURN e.nombre, libro.titulo, p.fecha;

// 5. Libros recomendados para Informática
MATCH (profesor)-[r:RECOMIENDA]->(libro) 
WHERE r.para_carrera = 'Informática' 
RETURN profesor.nombre, libro.titulo;

// 6. Estudiantes de último año (año >= 4)
MATCH (e:Estudiante) 
WHERE e.año >= 4 
RETURN e.nombre, e.carrera, e.año;
```

**Ejercicio 3: Patrones complejos**
```cypher
// 7. Libros que han pedido prestado múltiples estudiantes
MATCH (libro)<-[:PIDIO_PRESTADO]-(estudiante)
WITH libro, count(estudiante) as veces_prestado
WHERE veces_prestado > 1
RETURN libro.titulo, veces_prestado;

// 8. Estudiantes que comparten intereses (mismo libro)
MATCH (e1:Estudiante)-[:PIDIO_PRESTADO]->(libro)<-[:PIDIO_PRESTADO]-(e2:Estudiante)
WHERE e1 <> e2
RETURN e1.nombre, e2.nombre, libro.titulo;

// 9. Profesores y los estudiantes que siguieron sus recomendaciones
MATCH (prof:Profesor)-[:RECOMIENDA]->(libro)<-[:PIDIO_PRESTADO]-(estudiante)
RETURN prof.nombre, libro.titulo, estudiante.nombre;
```

### Dataset: Empresa de Tecnología

```cypher
// Limpiar para nuevo dataset
MATCH (n) DETACH DELETE n;

// Crear empleados
CREATE 
  (ana:Empleado:Persona {nombre: 'Ana García', puesto: 'Senior Developer', salario: 65000, años_empresa: 3}),
  (bob:Empleado:Persona {nombre: 'Bob Johnson', puesto: 'Junior Developer', salario: 45000, años_empresa: 1}),
  (carla:Empleado:Persona {nombre: 'Carla Martínez', puesto: 'Tech Lead', salario: 85000, años_empresa: 5}),
  (diana:Empleado:Persona {nombre: 'Diana Chen', puesto: 'QA Engineer', salario: 55000, años_empresa: 2}),
  (eduardo:Empleado:Persona {nombre: 'Eduardo López', puesto: 'Product Manager', salario: 75000, años_empresa: 4}),
// Crear departamentos
  (desarrollo:Departamento {nombre: 'Desarrollo', presupuesto: 500000}),
  (calidad:Departamento {nombre: 'Quality Assurance', presupuesto: 200000}),
  (producto:Departamento {nombre: 'Producto', presupuesto: 300000}),
// Crear proyectos
  (app_mobile:Proyecto {nombre: 'App Móvil', estado: 'En desarrollo', presupuesto: 150000}),
  (web_platform:Proyecto {nombre: 'Plataforma Web', estado: 'Completado', presupuesto: 200000}),
  (api_service:Proyecto {nombre: 'API Service', estado: 'Planificación', presupuesto: 100000}),
// Relaciones empleado-departamento
  (ana)-[:TRABAJA_EN]->(desarrollo),
  (bob)-[:TRABAJA_EN]->(desarrollo),
  (carla)-[:TRABAJA_EN]->(desarrollo),
  (diana)-[:TRABAJA_EN]->(calidad),
  (eduardo)-[:TRABAJA_EN]->(producto),
// Relaciones empleado-proyecto
  (ana)-[:ASIGNADO_A {rol: 'Backend Developer', horas_semana: 40}]->(app_mobile),
  (bob)-[:ASIGNADO_A {rol: 'Frontend Developer', horas_semana: 35}]->(app_mobile),
  (carla)-[:ASIGNADO_A {rol: 'Tech Lead', horas_semana: 30}]->(app_mobile),
  (carla)-[:ASIGNADO_A {rol: 'Architect', horas_semana: 10}]->(api_service),
  (diana)-[:ASIGNADO_A {rol: 'QA Lead', horas_semana: 40}]->(app_mobile),
  (eduardo)-[:ASIGNADO_A {rol: 'Product Owner', horas_semana: 20}]->(app_mobile),
  (eduardo)-[:ASIGNADO_A {rol: 'Product Manager', horas_semana: 20}]->(api_service),
// Relaciones de supervisión
  (carla)-[:SUPERVISA]->(ana),
  (carla)-[:SUPERVISA]->(bob),
  (diana)-[:REPORTA_A]->(carla),
  (eduardo)-[:COLABORA_CON]->(carla);
```

### Ejercicios avanzados

**Ejercicio 4: Análisis organizacional**
```cypher
// 10. Empleados por departamento
MATCH (e:Empleado)-[:TRABAJA_EN]->(d:Departamento)
RETURN d.nombre, collect(e.nombre) as empleados;

// 11. Proyectos con más de 3 personas asignadas
MATCH (p:Proyecto)<-[:ASIGNADO_A]-(e:Empleado)
WITH p, count(e) as num_empleados
WHERE num_empleados > 3
RETURN p.nombre, num_empleados;

// 12. Empleados que trabajan en múltiples proyectos
MATCH (e:Empleado)-[:ASIGNADO_A]->(p:Proyecto)
WITH e, count(p) as num_proyectos
WHERE num_proyectos > 1
RETURN e.nombre, num_proyectos;

// 13. Cadena de supervisión
MATCH path = (supervisor)-[:SUPERVISA*]->(subordinado)
RETURN supervisor.nombre, subordinado.nombre, length(path) as niveles
ORDER BY niveles;
```

**Ejercicio 5: Análisis de recursos**
```cypher
// 14. Total de horas asignadas por proyecto
MATCH (p:Proyecto)<-[a:ASIGNADO_A]-(e:Empleado)
RETURN p.nombre, sum(a.horas_semana) as total_horas_semana;

// 15. Empleados con salario mayor al promedio
MATCH (e:Empleado)
WITH avg(e.salario) as salario_promedio
MATCH (emp:Empleado)
WHERE emp.salario > salario_promedio
RETURN emp.nombre, emp.salario, salario_promedio;

// 16. Departamentos ordenados por presupuesto
MATCH (d:Departamento)
RETURN d.nombre, d.presupuesto
ORDER BY d.presupuesto DESC;
```

## 2.7 Mejores prácticas para principiantes

### 1. Nomenclatura consistente
```cypher
// ✅ Buenas prácticas
CREATE (p:Persona {nombre: 'Juan'});  // Etiqueta en PascalCase
CREATE (p)-[:CONOCE_A]->(m);          // Relación en UPPER_SNAKE_CASE
MATCH (persona:Persona)  ...          // Variable en camelCase

// ❌ Evitar
CREATE (P:persona {Nombre: 'juan'});  // Inconsistente
CREATE (p)-[:conoce a]->(m);          // Espacios en relaciones
```

### 2. Usar variables descriptivas
```cypher
// ✅ Claro y legible
MATCH (empleado:Empleado)-[:TRABAJA_EN]->(departamento:Departamento)
WHERE departamento.nombre = 'Desarrollo'
RETURN empleado.nombre;

// ❌ Poco claro
MATCH (e)-[:TRABAJA_EN]->(d)
WHERE d.nombre = 'Desarrollo'
RETURN e.nombre;
```

### 3. Filtrar temprano
```cypher
// ✅ Eficiente - filtrar en MATCH
MATCH (p:Persona {edad: 30})-[:CONOCE]->(amigo)
RETURN p.nombre, amigo.nombre;

// ❌ Menos eficiente - filtrar después
MATCH (p:Persona)-[:CONOCE]->(amigo)
WHERE p.edad = 30
RETURN p.nombre, amigo.nombre;
```

### 4. Usar LIMIT para exploración
```cypher
// Al explorar datos grandes, usar LIMIT
MATCH (n) RETURN n LIMIT 10;
MATCH (p:Persona) RETURN p LIMIT 5;
```

## 2.8 Errores comunes y cómo evitarlos

### 1. Olvidar la dirección de las relaciones
```cypher
// ❌ Error: dirección incorrecta
MATCH (libro)-[:PIDIO_PRESTADO]->(estudiante);  // Libro pidió al estudiante??

// ✅ Correcto
MATCH (estudiante)-[:PIDIO_PRESTADO]->(libro) ; // Estudiante pidió el libro
```

### 2. No usar variables cuando es necesario
```cypher
// ❌ Error: no se puede referenciar la relación
MATCH (a)-[:CONOCE]->(b)
WHERE fecha > date('2023-01-01') ; // ¿Qué fecha?

// ✅ Correcto
MATCH (a)-[r:CONOCE]->(b)
WHERE r.fecha > date('2023-01-01');
```

### 3. Consultas cartesianas accidentales
```cypher
// ❌ Peligroso: producto cartesiano
MATCH (p:Persona), (l:Lugar)
RETURN p, l;  // Todas las combinaciones persona-lugar

// ✅ Correcto: con relación específica
MATCH (p:Persona)-[:VIVE_EN]->(l:Lugar)
RETURN p, l;
```

## Laboratorio práctico: Sistema de recomendación simple

### Objetivo
Crear un sistema básico de recomendación de películas basado en géneros y valoraciones.

### Paso 1: Crear el modelo
```cypher
// Limpiar base de datos
MATCH (n) DETACH DELETE n;

// Crear usuarios
CREATE 
  (ana:Usuario {nombre: 'Ana', edad: 28}),
  (bob:Usuario {nombre: 'Bob', edad: 34}),
  (carla:Usuario {nombre: 'Carla', edad: 25}),
  (david:Usuario {nombre: 'David', edad: 31}),
// Crear géneros
  (accion:Genero {nombre: 'Acción'}),
  (comedia:Genero {nombre: 'Comedia'}),
  (drama:Genero {nombre: 'Drama'}),
  (scifi:Genero {nombre: 'Ciencia Ficción'}),
// Crear películas
  (avatar:Pelicula {titulo: 'Avatar', año: 2009, duracion: 162}),
  (inception:Pelicula {titulo: 'Inception', año: 2010, duracion: 148}),
  (hangover:Pelicula {titulo: 'The Hangover', año: 2009, duracion: 100}),
  (forrest:Pelicula {titulo: 'Forrest Gump', año: 1994, duracion: 142}),
  (matrix:Pelicula {titulo: 'The Matrix', año: 1999, duracion: 136}),
// Películas pertenecen a géneros
  (avatar)-[:PERTENECE_A]->(accion),
  (avatar)-[:PERTENECE_A]->(scifi),
  (inception)-[:PERTENECE_A]->(scifi),
  (inception)-[:PERTENECE_A]->(accion),
  (hangover)-[:PERTENECE_A]->(comedia),
  (forrest)-[:PERTENECE_A]->(drama),
  (forrest)-[:PERTENECE_A]->(comedia),
  (matrix)-[:PERTENECE_A]->(scifi),
  (matrix)-[:PERTENECE_A]->(accion),
// Usuarios valoran películas
  (ana)-[:VALORO {puntuacion: 5, fecha: date('2023-09-01')}]->(avatar),
  (ana)-[:VALORO {puntuacion: 4, fecha: date('2023-09-05')}]->(inception),
  (bob)-[:VALORO {puntuacion: 3, fecha: date('2023-09-02')}]->(hangover),
  (bob)-[:VALORO {puntuacion: 5, fecha: date('2023-09-07')}]->(matrix),
  (carla)-[:VALORO {puntuacion: 4, fecha: date('2023-09-03')}]->(forrest),
  (carla)-[:VALORO {puntuacion: 5, fecha: date('2023-09-08')}]->(avatar),
  (david)-[:VALORO {puntuacion: 4, fecha: date('2023-09-04')}]->(inception),
  (david)-[:VALORO {puntuacion: 3, fecha: date('2023-09-09')}]->(hangover);
```

### Paso 2: Consultas de análisis
```cypher
// 1. Películas mejor valoradas
MATCH (u:Usuario)-[v:VALORO]->(p:Pelicula)
RETURN p.titulo, avg(v.puntuacion) as valoracion_promedio, count(v) as num_valoraciones
ORDER BY valoracion_promedio DESC;

// 2. Géneros favoritos de cada usuario
MATCH (u:Usuario)-[:VALORO]->(p:Pelicula)-[:PERTENECE_A]->(g:Genero)
RETURN u.nombre, g.nombre, count(*) as peliculas_del_genero
ORDER BY u.nombre, peliculas_del_genero DESC;

// 3. Usuarios con gustos similares
MATCH (u1:Usuario)-[:VALORO]->(p:Pelicula)<-[:VALORO]-(u2:Usuario)
WHERE u1 <> u2
RETURN u1.nombre, u2.nombre, collect(p.titulo) as peliculas_comunes;
```

### Desafío final
Escribe una consulta que recomiende películas a un usuario basándose en:

1. Películas que les gustaron a usuarios con gustos similares
2. Que el usuario objetivo no haya visto aún
3. Ordenadas por valoración promedio

```cypher
// Solución propuesta
MATCH (usuario:Usuario {nombre: 'Ana'})-[:VALORO]->(pelicula_vista)<-[:VALORO]-(usuario_similar)
MATCH (usuario_similar)-[v:VALORO]->(recomendacion:Pelicula)
WHERE NOT (usuario)-[:VALORO]->(recomendacion)
WITH recomendacion, avg(v.puntuacion) as valoracion_promedio
RETURN recomendacion.titulo, valoracion_promedio
ORDER BY valoracion_promedio DESC
LIMIT 3
```

## Resumen

En esta parte hemos aprendido:

- ✅ Modelo de datos de grafos: nodos, relaciones, propiedades
- ✅ Sintaxis básica de Cypher: CREATE, MATCH, RETURN
- ✅ Patrones de grafos y cómo expresarlos
- ✅ Filtrado con WHERE y operadores
- ✅ Ejercicios prácticos con datasets reales
- ✅ Mejores prácticas y errores comunes
