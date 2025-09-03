# Parte C: Cypher Intermedio

## 3.1 Agregaciones: COUNT, SUM, AVG

### COUNT - Contar elementos
```cypher
// Contar todos los nodos
MATCH (n) RETURN count(n);

// Contar nodos por etiqueta
MATCH (p:Persona) RETURN count(p) as total_personas;

// Contar relaciones
MATCH ()-[r:CONOCE]->() RETURN count(r) as total_conocimientos;

// COUNT con DISTINCT
MATCH (p:Persona)-[:TRABAJA_EN]->(d:Departamento)
RETURN count(DISTINCT d) as departamentos_con_empleados;

// COUNT con propiedades
MATCH (p:Persona)
RETURN count(p.email) as personas_con_email;  // No cuenta NULL
```

### SUM - Sumar valores
```cypher
// Sumar salarios por departamento
MATCH (e:Empleado)-[:TRABAJA_EN]->(d:Departamento)
RETURN d.nombre, sum(e.salario) as masa_salarial;

// Sumar horas de trabajo por proyecto
MATCH (p:Proyecto)<-[a:ASIGNADO_A]-(e:Empleado)
RETURN p.nombre, sum(a.horas_semana) as total_horas;

// Sumar con condiciones
MATCH (e:Empleado)
WHERE e.años_empresa > 2
RETURN sum(e.salario) as salarios_empleados_senior;
```

### AVG - Promedio
```cypher
// Salario promedio
MATCH (e:Empleado) RETURN avg(e.salario) as salario_promedio

// Promedio por departamento
MATCH (e:Empleado)-[:TRABAJA_EN]->(d:Departamento)
RETURN d.nombre, avg(e.salario) as salario_promedio_depto

// Valoración promedio de películas
MATCH (u:Usuario)-[v:VALORO]->(p:Pelicula)
RETURN p.titulo, avg(v.puntuacion) as valoracion_promedio
ORDER BY valoracion_promedio DESC
```

### MIN y MAX
```cypher
// Salario mínimo y máximo
MATCH (e:Empleado) 
RETURN min(e.salario) as salario_minimo, max(e.salario) as salario_maximo;

// Empleado más joven y más veterano
MATCH (e:Empleado)
RETURN min(e.años_empresa) as menos_antiguedad, max(e.años_empresa) as mas_antiguedad;

// Película más larga por género
MATCH (p:Pelicula)-[:PERTENECE_A]->(g:Genero)
RETURN g.nombre, max(p.duracion) as pelicula_mas_larga;
```

## 3.2 Agrupamiento con WITH

### Concepto de WITH
`WITH` es como un "punto y coma" en Cypher. Te permite:

- Pasar resultados a la siguiente parte de la consulta
- Hacer agregaciones intermedias
- Filtrar resultados agregados
- Renombrar variables

```cypher
// Sintaxis básica
MATCH (patron)
WITH variable1, variable2, agregacion
MATCH (otro_patron)
RETURN resultado;
```

### Ejemplos prácticos de WITH

**Encontrar empleados con salario mayor al promedio:**
```cypher
// Paso 1: Calcular promedio
MATCH (e:Empleado)
WITH avg(e.salario) as salario_promedio;

// Paso 2: Encontrar empleados sobre el promedio
MATCH (emp:Empleado)
WHERE emp.salario > salario_promedio
RETURN emp.nombre, emp.salario, salario_promedio;
```

**Top 3 departamentos por masa salarial:**
```cypher
MATCH (e:Empleado)-[:TRABAJA_EN]->(d:Departamento)
WITH d, sum(e.salario) as masa_salarial
ORDER BY masa_salarial DESC
LIMIT 3
RETURN d.nombre, masa_salarial;
```

**Empleados que trabajan en proyectos múltiples:**
```cypher
MATCH (e:Empleado)-[:ASIGNADO_A]->(p:Proyecto)
WITH e, count(p) as num_proyectos
WHERE num_proyectos > 1
MATCH (e)-[:ASIGNADO_A]->(proyecto)
RETURN e.nombre, num_proyectos, collect(proyecto.nombre) as proyectos;
```

## 3.3 Funciones de colección

### COLLECT - Recopilar en listas
```cypher
// Recopilar nombres
MATCH (p:Persona) RETURN collect(p.nombre) as todos_los_nombres;

// Agrupar empleados por departamento
MATCH (e:Empleado)-[:TRABAJA_EN]->(d:Departamento)
RETURN d.nombre, collect(e.nombre) as empleados;

// Recopilar con propiedades múltiples
MATCH (e:Empleado)
RETURN collect({nombre: e.nombre, salario: e.salario}) as empleados_info;
```

### SIZE - Tamaño de colecciones
```cypher
// Contar elementos en una lista
MATCH (d:Departamento)<-[:TRABAJA_EN]-(e:Empleado)
WITH d, collect(e) as empleados
RETURN d.nombre, size(empleados) as cantidad_empleados;

// Usar con propiedades de tipo lista
MATCH (p:Producto)
WHERE size(p.tags) > 2
RETURN p.nombre, p.tags;
```

### Funciones de manipulación de listas
```cypher
// HEAD - primer elemento
MATCH (p:Persona)
WITH collect(p.nombre) as nombres
RETURN head(nombres) as primer_nombre;

// TAIL - todos excepto el primero
MATCH (p:Persona)
WITH collect(p.nombre) as nombres
RETURN tail(nombres) as resto_nombres;

// REVERSE - invertir orden
MATCH (p:Persona)
WITH collect(p.nombre) as nombres
RETURN reverse(nombres) as nombres_inverso;

// RANGE - generar secuencias
RETURN range(1, 10) as numeros;
RETURN range(0, 100, 10) as multiplos_de_10;
```

## 3.4 ORDER BY y LIMIT

### ORDER BY - Ordenamiento
```cypher
// Orden ascendente (por defecto)
MATCH (e:Empleado)
RETURN e.nombre, e.salario
ORDER BY e.salario;

// Orden descendente
MATCH (e:Empleado)
RETURN e.nombre, e.salario
ORDER BY e.salario DESC;

// Múltiples criterios
MATCH (e:Empleado)
RETURN e.nombre, e.salario, e.años_empresa
ORDER BY e.salario DESC, e.años_empresa DESC;

// Ordenar por expresiones
MATCH (p:Persona)
RETURN p.nombre, p.edad * 12 as edad_meses
ORDER BY edad_meses  // Ordenar por edad en meses
```

### LIMIT y SKIP
```cypher
// Top 5 empleados mejor pagados
MATCH (e:Empleado)
RETURN e.nombre, e.salario
ORDER BY e.salario DESC
LIMIT 5;

// Paginación con SKIP
MATCH (e:Empleado)
RETURN e.nombre, e.salario
ORDER BY e.salario DESC
SKIP 5 LIMIT 5;  // Empleados del 6 al 10

```

## 3.5 Funciones de texto y fechas

### Funciones de texto
```cypher
CREATE (p:Persona {nombre: '  Juan  ', email: 'ejemplo@email.com'});

// UPPER y LOWER
MATCH (p:Persona)
RETURN upper(p.nombre) as nombre_mayusculas, lower(p.email) as email_minusculas;

// TRIM - eliminar espacios
MATCH (p:Persona {nombre: '  Juan  '})
SET p.nombre = trim(p.nombre)
RETURN p.nombre;

// SUBSTRING
MATCH (p:Persona)
RETURN p.nombre, substring(p.nombre, 0, 3) as iniciales;

// SPLIT - dividir texto
MATCH (p:Persona)
WHERE p.email IS NOT NULL
RETURN p.nombre, split(p.email, '@')[0] as usuario, split(p.email, '@')[1] as dominio;

// REPLACE
MATCH (p:Persona)
RETURN p.nombre, replace(p.nombre, 'á', 'a') as nombre_sin_acentos;

// SIZE - longitud de texto
MATCH (p:Persona)
WHERE size(p.nombre) > 10
RETURN p.nombre, size(p.nombre) as longitud;
```

### Funciones de fechas
```cypher
// Fecha actual
RETURN date() as hoy, datetime() as ahora;

// Crear fechas específicas
RETURN date('2023-12-25') as navidad;
RETURN datetime('2023-12-25T10:30:00') as navidad_con_hora;

// Componentes de fecha
MATCH (e:Empleado)-[r:CONTRATADO {fecha: date('2023-06-15')}]->()
RETURN e.nombre, 
       r.fecha.year as año,
       r.fecha.month as mes,
       r.fecha.day as dia;

// Operaciones con fechas
MATCH (e:Empleado)
WHERE e.fecha_contratacion IS NOT NULL
RETURN e.nombre, 
       e.fecha_contratacion,
       duration.between(e.fecha_contratacion, date()) as tiempo_empresa;

// Formato de fechas
MATCH (evento:Evento)
RETURN evento.nombre, 
       toString(evento.fecha) as fecha_texto,
       evento.fecha.year + '-' + evento.fecha.month as año_mes;
```

## 3.6 OPTIONAL MATCH y manejo de nulos

### OPTIONAL MATCH - Coincidencias opcionales 
```cypher
// Similar a LEFT JOIN en SQL
MATCH (e:Empleado)
OPTIONAL MATCH (e)-[:ASIGNADO_A]->(p:Proyecto)
RETURN e.nombre, p.nombre as proyecto;

// Múltiples OPTIONAL MATCH
MATCH (p:Persona)
OPTIONAL MATCH (p)-[:TRABAJA_EN]->(empresa:Empresa)
OPTIONAL MATCH (p)-[:VIVE_EN]->(ciudad:Ciudad)
RETURN p.nombre, empresa.nombre, ciudad.nombre;
```

### Manejo de valores NULL
```cypher
// COALESCE - primer valor no null
MATCH (p:Persona)
OPTIONAL MATCH (p)-[:TRABAJA_EN]->(empresa)
RETURN p.nombre, coalesce(empresa.nombre, 'Desempleado') as estado_laboral;

// CASE - condicionales
MATCH (e:Empleado)
RETURN e.nombre,
       CASE 
         WHEN e.salario > 70000 THEN 'Alto'
         WHEN e.salario > 50000 THEN 'Medio'
         ELSE 'Bajo'
       END as rango_salarial;

// IS NULL y IS NOT NULL
MATCH (p:Persona)
WHERE p.email IS NOT NULL
RETURN p.nombre, p.email;

// Contar valores no nulos
MATCH (p:Persona)
RETURN count(p.telefono) as personas_con_telefono,
       count(*) - count(p.telefono) as personas_sin_telefono;
```

## 3.7 Modificación de datos: UPDATE y DELETE

### SET - Actualizar propiedades
```cypher
// Actualizar una propiedad
MATCH (p:Persona {nombre: 'Juan'})
SET p.edad = 31
RETURN p;

// Actualizar múltiples propiedades
MATCH (e:Empleado {nombre: 'Ana García'})
SET e.salario = 70000, e.puesto = 'Lead Developer'
RETURN e;

// Agregar nueva propiedad
MATCH (p:Persona)
SET p.fecha_actualizacion = datetime()
RETURN count(p) as personas_actualizadas;

// Actualizar desde otra propiedad
MATCH (e:Empleado)
SET e.salario_anual = e.salario * 12;

// Copiar propiedades
MATCH (p1:Persona {nombre: 'Juan'}), (p2:Persona {nombre: 'María'})
SET p2 += {email: p1.email, telefono: p1.telefono};
```

### REMOVE - Eliminar propiedades y etiquetas
```cypher
// Eliminar propiedad
MATCH (p:Persona {nombre: 'Juan'})
REMOVE p.edad
RETURN p;

// Eliminar etiqueta
MATCH (p:Persona:Temporal)
REMOVE p:Temporal
RETURN p;

// Eliminar múltiples propiedades
MATCH (p:Persona)
REMOVE p.campo_temporal, p.otro_campo_temporal;
```

### DELETE - Eliminar nodos y relaciones
```cypher
// Eliminar relación específica
MATCH (a:Persona)-[r:CONOCE]->(b:Persona)
WHERE a.nombre = 'Juan' AND b.nombre = 'María';
DELETE r

// Eliminar nodo (primero eliminar relaciones)
MATCH (p:Persona {nombre: 'Juan'})
DETACH DELETE p;  // DETACH elimina automáticamente las relaciones

// Eliminar múltiples nodos
MATCH (p:Persona)
WHERE p.activo = false
DETACH DELETE p;

// Eliminar todo (¡CUIDADO!)
MATCH (n)
DETACH DELETE n;
```

## 3.8 MERGE - Evitar duplicados

### Concepto de MERGE
MERGE es una operación "upsert" que:

- Si encuentra el patrón, no hace nada (o usa ON MATCH)
- Si no lo encuentra, lo crea (o usa ON CREATE)

```cypher
// MERGE básico
MERGE (p:Persona {email: 'juan@email.com'})
RETURN p

// Con ON CREATE y ON MATCH
MERGE (p:Persona {email: 'juan@email.com'})
ON CREATE SET p.nombre = 'Juan', p.fecha_creacion = datetime()
ON MATCH SET p.fecha_ultima_actualizacion = datetime()
RETURN p
```

### Ejemplos prácticos de MERGE

**Sistema de tags:**
```cypher
// Crear o encontrar tags
MATCH (articulo:Articulo {id: 123})
FOREACH (tag_name IN ['neo4j', 'grafos', 'bases-datos'] |
  MERGE (tag:Tag {nombre: tag_name})
  MERGE (articulo)-[:TIENE_TAG]->(tag)
)
```

**Importación de datos sin duplicados:**
```cypher
// Asegurar que cada persona existe solo una vez
UNWIND [
  {nombre: 'Ana', email: 'ana@email.com'},
  {nombre: 'Bob', email: 'bob@email.com'},
  {nombre: 'Ana', email: 'ana@email.com'}  // Duplicado
] as persona_data

MERGE (p:Persona {email: persona_data.email})
ON CREATE SET p.nombre = persona_data.nombre
RETURN p
```

**Relaciones únicas:**
```cypher
// Evitar relaciones duplicadas
MATCH (a:Persona {nombre: 'Ana'}), (b:Persona {nombre: 'Bob'})
MERGE (a)-[:CONOCE]->(b)

// MERGE con propiedades en relaciones
MATCH (usuario:Usuario {id: 123}), (producto:Producto {id: 456})
MERGE (usuario)-[r:COMPRO {fecha: date('2023-10-01')}]->(producto)
ON CREATE SET r.cantidad = 1, r.precio = producto.precio
ON MATCH SET r.cantidad = r.cantidad + 1
```

## 3.9 Relaciones dinámicas y patrones avanzados

### Relaciones con longitud variable
```cypher
// Buscar en 1 a 3 saltos
MATCH (inicio:Persona {nombre: 'Ana'})-[:CONOCE*1..3]->(destino:Persona)
RETURN destino.nombre, length(path) as grados_separacion

// Cualquier longitud (¡CUIDADO con grafos grandes!)
MATCH (inicio)-[:CONOCE*]->(destino)
WHERE inicio.nombre = 'Ana' AND destino.nombre = 'Carlos'
RETURN path

// Longitud exacta
MATCH (inicio)-[:CONOCE*2]->(destino)
WHERE inicio.nombre = 'Ana'
RETURN destino.nombre as amigos_de_amigos

// Con filtros en nodos intermedios
MATCH (inicio)-[:CONOCE*2..4]->(destino)
WHERE ALL(persona IN nodes(path) WHERE persona.edad > 18)
RETURN destino.nombre
```

### Múltiples tipos de relaciones
```cypher
// OR en tipos de relaciones
MATCH (p:Persona)-[:TRABAJA_EN|:ESTUDIA_EN|:VIVE_EN]->(lugar)
RETURN p.nombre, type(r) as tipo_relacion, lugar.nombre

// Patrones complejos
MATCH (empleado:Empleado)-[:TRABAJA_EN]->(dept:Departamento),
      (empleado)-[:ASIGNADO_A]->(proyecto:Proyecto)
WHERE dept.nombre = 'Desarrollo'
RETURN empleado.nombre, proyecto.nombre
```

### Funciones de path (camino)
```cypher
// Información sobre paths
MATCH path = (inicio)-[:CONOCE*]->(fin)
WHERE inicio.nombre = 'Ana' AND fin.nombre = 'Carlos'
RETURN 
  length(path) as longitud,
  nodes(path) as nodos_en_camino,
  relationships(path) as relaciones_en_camino

// Camino más corto
MATCH path = shortestPath((inicio:Persona {nombre: 'Ana'})-[:CONOCE*]-(fin:Persona {nombre: 'Carlos'}))
RETURN path, length(path)

// Todos los caminos más cortos
MATCH path = allShortestPaths((inicio:Persona {nombre: 'Ana'})-[:CONOCE*]-(fin:Persona {nombre: 'Carlos'}))
RETURN path
```

## 3.10 Laboratorio práctico: Sistema de e-commerce

### Objetivo
Crear un sistema de e-commerce completo con usuarios, productos, categorías, pedidos y valoraciones.

### Paso 1: Crear el modelo de datos
```cypher
// Limpiar base de datos
MATCH (n) DETACH DELETE n;

// Crear usuarios
CREATE 
  (ana:Usuario:Cliente {
    id: 1, nombre: 'Ana García', email: 'ana@email.com', 
    fecha_registro: date('2023-01-15'), ciudad: 'Madrid'
  }),
  (bob:Usuario:Cliente {
    id: 2, nombre: 'Bob Johnson', email: 'bob@email.com', 
    fecha_registro: date('2023-02-20'), ciudad: 'Barcelona'
  }),
  (carla:Usuario:Cliente {
    id: 3, nombre: 'Carla López', email: 'carla@email.com', 
    fecha_registro: date('2023-03-10'), ciudad: 'Madrid'
  }),
  (david:Usuario:Cliente {
    id: 4, nombre: 'David Chen', email: 'david@email.com', 
    fecha_registro: date('2023-04-05'), ciudad: 'Valencia'
  }),

// Crear categorías
  (electronica:Categoria {nombre: 'Electrónica', descripcion: 'Dispositivos electrónicos'}),
  (ropa:Categoria {nombre: 'Ropa', descripcion: 'Vestimenta y accesorios'}),
  (hogar:Categoria {nombre: 'Hogar', descripcion: 'Artículos para el hogar'}),
  (libros:Categoria {nombre: 'Libros', descripcion: 'Literatura y educación'}),

// Crear productos
  (laptop:Producto {
    id: 101, nombre: 'Laptop Dell XPS', precio: 1299.99, stock: 15,
    descripcion: 'Laptop de alta gama', marca: 'Dell'
  }),
  (iphone:Producto {
    id: 102, nombre: 'iPhone 14', precio: 999.99, stock: 8,
    descripcion: 'Smartphone Apple', marca: 'Apple'
  }),
  (camisa:Producto {
    id: 201, nombre: 'Camisa Casual', precio: 49.99, stock: 25,
    descripcion: 'Camisa de algodón', marca: 'Zara'
  }),
  (jeans:Producto {
    id: 202, nombre: 'Jeans Clásicos', precio: 79.99, stock: 18,
    descripcion: 'Pantalón denim azul', marca: 'Levi\'s'
  }),
  (mesa:Producto {
    id: 301, nombre: 'Mesa de Comedor', precio: 299.99, stock: 5,
    descripcion: 'Mesa de madera roble', marca: 'IKEA'
  }),
  (libro_neo4j:Producto {
    id: 401, nombre: 'Learning Neo4j', precio: 39.99, stock: 12,
    descripcion: 'Guía completa de Neo4j', marca: 'O\'Reilly'
  }),

// Productos pertenecen a categorías
  (laptop)-[:PERTENECE_A]->(electronica),
  (iphone)-[:PERTENECE_A]->(electronica),
  (camisa)-[:PERTENECE_A]->(ropa),
  (jeans)-[:PERTENECE_A]->(ropa),
  (mesa)-[:PERTENECE_A]->(hogar),
  (libro_neo4j)-[:PERTENECE_A]->(libros),

// Crear pedidos
  (pedido1:Pedido {
    id: 1001, fecha: date('2023-09-01'), estado: 'Entregado', 
    total: 1349.98, direccion_envio: 'Madrid, España'
  }),
  (pedido2:Pedido {
    id: 1002, fecha: date('2023-09-15'), estado: 'En tránsito', 
    total: 129.98, direccion_envio: 'Barcelona, España'
  }),
  (pedido3:Pedido {
    id: 1003, fecha: date('2023-09-20'), estado: 'Procesando', 
    total: 299.99, direccion_envio: 'Madrid, España'
  }),

// Usuarios realizan pedidos
  (ana)-[:REALIZO_PEDIDO]->(pedido1),
  (bob)-[:REALIZO_PEDIDO]->(pedido2),
  (carla)-[:REALIZO_PEDIDO]->(pedido3),

// Pedidos contienen productos
  (pedido1)-[:CONTIENE {cantidad: 1, precio_unitario: 1299.99}]->(laptop),
  (pedido1)-[:CONTIENE {cantidad: 1, precio_unitario: 49.99}]->(camisa),
  (pedido2)-[:CONTIENE {cantidad: 1, precio_unitario: 79.99}]->(jeans),
  (pedido2)-[:CONTIENE {cantidad: 1, precio_unitario: 49.99}]->(camisa),
  (pedido3)-[:CONTIENE {cantidad: 1, precio_unitario: 299.99}]->(mesa),

// Usuarios valoran productos
  (ana)-[:VALORO {puntuacion: 5, comentario: 'Excelente laptop', fecha: date('2023-09-05')}]->(laptop),
  (ana)-[:VALORO {puntuacion: 4, comentario: 'Buena calidad', fecha: date('2023-09-06')}]->(camisa),
  (bob)-[:VALORO {puntuacion: 4, comentario: 'Cómodos y duraderos', fecha: date('2023-09-18')}]->(jeans),
  (carla)-[:VALORO {puntuacion: 3, comentario: 'Esperaba mejor calidad', fecha: date('2023-09-22')}]->(mesa),
  (david)-[:VALORO {puntuacion: 5, comentario: 'Muy útil para aprender', fecha: date('2023-09-25')}]->(libro_neo4j),

// Usuarios siguen a otros (para recomendaciones sociales)
  (ana)-[:SIGUE]->(bob),
  (bob)-[:SIGUE]->(ana),
  (ana)-[:SIGUE]->(carla),
  (carla)-[:SIGUE]->(david),
  (david)-[:SIGUE]->(ana);
```

### Paso 2: Consultas de análisis de negocio

**1. Productos más vendidos:**
```cypher
MATCH (producto:Producto)<-[c:CONTIENE]-(pedido:Pedido)
RETURN producto.nombre, 
       sum(c.cantidad) as total_vendido,
       sum(c.cantidad * c.precio_unitario) as ingresos_totales
ORDER BY total_vendido DESC;
```

**2. Clientes más valiosos:**
```cypher
MATCH (cliente:Cliente)-[:REALIZO_PEDIDO]->(pedido:Pedido)
WITH cliente, sum(pedido.total) as valor_total_cliente, count(pedido) as num_pedidos
RETURN cliente.nombre, valor_total_cliente, num_pedidos,
       valor_total_cliente / num_pedidos as valor_promedio_pedido
ORDER BY valor_total_cliente DESC;
```

**3. Análisis de valoraciones por categoría:**
```cypher
MATCH (usuario:Usuario)-[v:VALORO]->(producto:Producto)-[:PERTENECE_A]->(categoria:Categoria)
RETURN categoria.nombre, 
       avg(v.puntuacion) as valoracion_promedio,
       count(v) as total_valoraciones,
       collect(DISTINCT producto.nombre)[0..3] as productos_muestra
ORDER BY valoracion_promedio DESC;
```

**4. Tendencias temporales de ventas:**
```cypher
MATCH (pedido:Pedido)
WITH pedido.fecha.month as mes, sum(pedido.total) as ventas_mes
RETURN mes, ventas_mes
ORDER BY mes;
```

### Paso 3: Sistema de recomendaciones

**1. Recomendaciones basadas en productos similares:**
```cypher
// Usuarios que compraron X también compraron Y
MATCH (producto_base:Producto {nombre: 'Laptop Dell XPS'})<-[:CONTIENE]-(pedido1:Pedido)<-[:REALIZO_PEDIDO]-(usuario:Usuario)
MATCH (usuario)-[:REALIZO_PEDIDO]->(pedido2:Pedido)-[:CONTIENE]->(producto_recomendado:Producto)
WHERE producto_recomendado <> producto_base
RETURN producto_recomendado.nombre, count(*) as veces_comprado_junto
ORDER BY veces_comprado_junto DESC
LIMIT 5;
```

**2. Recomendaciones sociales:**
```cypher
// Productos que compraron personas que sigo
MATCH (yo:Usuario {nombre: 'Ana García'})-[:SIGUE]->(amigo:Usuario)
MATCH (amigo)-[:REALIZO_PEDIDO]->()-[:CONTIENE]->(producto:Producto)
WHERE NOT EXISTS((yo)-[:REALIZO_PEDIDO]->()-[:CONTIENE]->(producto))
OPTIONAL MATCH (amigo)-[v:VALORO]->(producto)
RETURN producto.nombre, 
       count(DISTINCT amigo) as amigos_que_compraron,
       avg(v.puntuacion) as valoracion_promedio
ORDER BY amigos_que_compraron DESC, valoracion_promedio DESC
LIMIT 5;
```

**3. Productos trending en mi ciudad:**
```cypher
MATCH (yo:Usuario {nombre: 'Ana García'})
MATCH (otros:Usuario)-[:REALIZO_PEDIDO]->(pedido:Pedido)-[:CONTIENE]->(producto:Producto)
WHERE otros.ciudad = yo.ciudad 
  AND pedido.fecha > date('2023-08-01')  // Últimas compras
  AND NOT EXISTS((yo)-[:REALIZO_PEDIDO]->()-[:CONTIENE]->(producto))
RETURN producto.nombre, 
       count(*) as popularidad_local,
       producto.precio
ORDER BY popularidad_local DESC
LIMIT 5;
```

### Paso 4: Análisis de inventario y alertas

**1. Productos con stock bajo:**
```cypher
MATCH (p:Producto)
WHERE p.stock < 10
RETURN p.nombre, p.stock, p.precio
ORDER BY p.stock ASC;
```

**2. Productos sin ventas recientes:**
```cypher
MATCH (p:Producto)
WHERE NOT EXISTS(
  (p)<-[:CONTIENE]-(pedido:Pedido)
  WHERE pedido.fecha > date('2023-08-01')
)
RETURN p.nombre, p.stock, p.precio;
```

**3. Análisis de rentabilidad por categoría:**
```cypher
MATCH (categoria:Categoria)<-[:PERTENECE_A]-(producto:Producto)<-[c:CONTIENE]-(pedido:Pedido)
WITH categoria, 
     sum(c.cantidad * c.precio_unitario) as ingresos,
     sum(c.cantidad) as unidades_vendidas,
     count(DISTINCT producto) as productos_diferentes
RETURN categoria.nombre, ingresos, unidades_vendidas, productos_diferentes,
       ingresos / productos_diferentes as ingreso_promedio_por_producto
ORDER BY ingresos DESC;
```

## 3.11 Ejercicios de práctica

### Ejercicio 1: Análisis de usuarios
Usando el dataset del e-commerce, responde:

1. ¿Cuál es el gasto promedio por pedido de cada usuario?
2. ¿Qué usuarios han valorado productos pero nunca han comprado nada?
3. ¿Cuál es la distribución de usuarios por ciudad?

```cypher
// Soluciones propuestas:

// 1. Gasto promedio por pedido
MATCH (u:Usuario)-[:REALIZO_PEDIDO]->(p:Pedido)
RETURN u.nombre, avg(p.total) as gasto_promedio
ORDER BY gasto_promedio DESC;

// 2. Usuarios que valoran pero no compran
MATCH (u:Usuario)-[:VALORO]->(:Producto)
WHERE NOT EXISTS((u)-[:REALIZO_PEDIDO]->())
RETURN u.nombre;

// 3. Distribución por ciudad
MATCH (u:Usuario)
RETURN u.ciudad, count(u) as usuarios_por_ciudad
ORDER BY usuarios_por_ciudad DESC;
```

### Ejercicio 2: Optimización de inventario

1. Identifica productos que deberían reabastecerse (stock bajo + alta demanda)
2. Encuentra productos que podrían descontinuarse (sin ventas + stock alto)
3. Calcula el valor total del inventario

### Ejercicio 3: Análisis de red social

1. Encuentra quién tiene más seguidores
2. Identifica usuarios que se siguen mutuamente
3. Calcula el grado de separación promedio entre usuarios

## 3.12 Funciones avanzadas

### Funciones matemáticas
```cypher
// Operaciones matemáticas básicas
MATCH (p:Producto)
RETURN p.nombre, 
       round(p.precio) as precio_redondeado,
       ceil(p.precio) as precio_techo,
       floor(p.precio) as precio_piso,
       abs(p.precio - 100) as diferencia_con_100;

// Funciones estadísticas
MATCH (p:Producto)
RETURN avg(p.precio) as precio_promedio,
       stDev(p.precio) as desviacion_estandar,
       percentileDisc(p.precio, 0.5) as mediana,
       percentileDisc(p.precio, 0.25) as primer_cuartil;
```

### Funciones de conversión
```cypher
// Conversiones de tipo
MATCH (p:Producto)
RETURN p.nombre,
       toString(p.precio) as precio_texto,
       toInteger(p.precio) as precio_entero,
       toFloat('123.45') as numero_desde_texto;

// Trabajar con listas
WITH [1, 2, 3, 4, 5] as numeros
RETURN reduce(total = 0, n IN numeros | total + n) as suma,
       [x IN numeros WHERE x > 3] as mayores_que_tres,
       [x IN numeros | x * 2] as duplicados;
```

## Resume

En esta parte hemos aprendido:

- ✅ Agregaciones: COUNT, SUM, AVG, MIN, MAX
- ✅ Uso de WITH para consultas complejas
- ✅ Funciones de colección: COLLECT, SIZE
- ✅ Ordenamiento y paginación: ORDER BY, LIMIT, SKIP
- ✅ Funciones de texto y fechas
- ✅ OPTIONAL MATCH y manejo de NULL
- ✅ Modificación de datos: UPDATE, DELETE, MERGE
- ✅ Patrones avanzados y relaciones dinámicas
- ✅ Sistema completo de e-commerce con análisis avanzado

