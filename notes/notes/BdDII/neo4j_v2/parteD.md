# Parte D: Casos Prácticos y Modelado


## 4.1 Principios de modelado de grafos

### Diferencias clave con modelado relacional

| Aspecto | Modelo Relacional | Modelo de Grafos |
|---------|------------------|------------------|
| **Enfoque** | Normalización, evitar redundancia | Desnormalización, optimizar consultas |
| **Relaciones** | Foreign keys, JOINs | Relaciones directas, navigación |
| **Esquema** | Rígido, definido previamente | Flexible, evolutivo |
| **Consultas** | JOINs complejos para relaciones | Traversal natural |
| **Performance** | Degrada con JOINs complejos | Constante para navegación local |

### Principios fundamentales del modelado de grafos

#### 1. **Modelar para las consultas específicas**
```cypher
// ❌ Modelo genérico poco eficiente
CREATE 
  (persona:Entidad {tipo: 'persona', nombre: 'Juan'}),
  (empresa:Entidad {tipo: 'empresa', nombre: 'TechCorp'}),
  (persona)-[:RELACIONADO_CON {tipo: 'trabaja_en'}]->(empresa);

// ✅ Modelo específico y eficiente
CREATE
  (juan:Persona {nombre: 'Juan'}),
  (techcorp:Empresa {nombre: 'TechCorp'}),
  (juan)-[:TRABAJA_EN {desde: date('2020-01-15'), puesto: 'Developer'}]->(techcorp);
```

#### 2. **Desnormalizar para performance**
```cypher
// En lugar de normalizar completamente, duplicar datos estratégicamente
CREATE (pedido:Pedido {
  id: 1001,
  fecha: date('2023-10-01'),
  total: 299.99,
  // Datos duplicados del cliente para consultas rápidas
  cliente_nombre: 'Ana García',
  cliente_email: 'ana@email.com',
  cliente_ciudad: 'Madrid'
})
```

#### 3. **Usar etiquetas jerárquicas**
```cypher
// Jerarquía de etiquetas para flexibilidad
CREATE (ana:Persona:Empleado:Desarrolladora {nombre: 'Ana'})
CREATE (producto:Item:Producto:Electronico {nombre: 'Laptop'})

// Permite consultas a diferentes niveles
MATCH (p:Persona) RETURN count(p)        // Todas las personas
MATCH (e:Empleado) RETURN count(e)       // Solo empleados
MATCH (d:Desarrolladora) RETURN count(d) // Solo desarrolladoras
```

## 4.2 Patrones comunes de modelado

### 1. Patrón: Entidades conectadas
**Cuándo usar:** Modelar entidades del mundo real y sus relaciones naturales.

```cypher
// Ejemplo: Red social profesional
CREATE 
  (ana:Persona {nombre: 'Ana García', profesion: 'Desarrolladora'}),
  (bob:Persona {nombre: 'Bob Smith', profesion: 'Diseñador'}),
  (techcorp:Empresa {nombre: 'TechCorp', sector: 'Tecnología'}),
  (madrid:Ciudad {nombre: 'Madrid', pais: 'España'}),
  
  (ana)-[:TRABAJA_EN {desde: date('2020-01-15'), puesto: 'Senior Developer'}]->(techcorp),
  (bob)-[:TRABAJA_EN {desde: date('2021-03-01'), puesto: 'UI Designer'}]->(techcorp),
  (ana)-[:VIVE_EN]->(madrid),
  (techcorp)-[:UBICADA_EN]->(madrid),
  (ana)-[:CONOCE {desde: date('2020-02-01'), contexto: 'trabajo'}]->(bob);
```

### 2. Patrón: Timeline/Eventos
**Cuándo usar:** Modelar secuencias temporales, historiales, logs.

```cypher
// Ejemplo: Historial médico
CREATE 
  (paciente:Paciente {nombre: 'María López', fecha_nacimiento: date('1985-05-20')}),
  (doctor:Doctor {nombre: 'Dr. Martínez', especialidad: 'Cardiología'}),
  
  // Consultas como eventos
  (consulta1:Consulta:Evento {
    fecha: datetime('2023-09-15T10:00:00'),
    motivo: 'Chequeo rutinario',
    notas: 'Presión arterial normal'
  }),
  (consulta2:Consulta:Evento {
    fecha: datetime('2023-10-20T15:30:00'),
    motivo: 'Seguimiento',
    notas: 'Mejoría notable'
  }),
  
  // Relaciones temporales
  (paciente)-[:TUVO_CONSULTA]->(consulta1)-[:ATENDIDA_POR]->(doctor),
  (paciente)-[:TUVO_CONSULTA]->(consulta2)-[:ATENDIDA_POR]->(doctor),
  (consulta1)-[:SEGUIDA_POR]->(consulta2);

// Consultar timeline
MATCH (p:Paciente {nombre: 'María López'})-[:TUVO_CONSULTA]->(consulta:Consulta)
RETURN consulta.fecha, consulta.motivo, consulta.notas
ORDER BY consulta.fecha;
```

### 3. Patrón: Jerarquías y Taxonomías
**Cuándo usar:** Categorías, organigramas, estructuras de archivos.

```cypher
// Ejemplo: Estructura organizacional
CREATE 
  (ceo:Persona:Ejecutivo {nombre: 'Carlos Ruiz', puesto: 'CEO'}),
  (cto:Persona:Ejecutivo {nombre: 'Ana Torres', puesto: 'CTO'}),
  (lead_backend:Persona:TechLead {nombre: 'Juan Pérez', puesto: 'Backend Lead'}),
  (lead_frontend:Persona:TechLead {nombre: 'María Silva', puesto: 'Frontend Lead'}),
  (dev1:Persona:Desarrollador {nombre: 'Pedro García', puesto: 'Backend Developer'}),
  (dev2:Persona:Desarrollador {nombre: 'Laura Vega', puesto: 'Frontend Developer'}),
  
  // Jerarquía organizacional
  (ceo)-[:SUPERVISA]->(cto),
  (cto)-[:SUPERVISA]->(lead_backend),
  (cto)-[:SUPERVISA]->(lead_frontend),
  (lead_backend)-[:SUPERVISA]->(dev1),
  (lead_frontend)-[:SUPERVISA]->(dev2);

// Consultar jerarquía completa desde CEO
MATCH path = (ceo:Persona {puesto: 'CEO'})-[:SUPERVISA*]->(subordinado)
RETURN subordinado.nombre, subordinado.puesto, length(path) as nivel_jerarquico
ORDER BY nivel_jerarquico, subordinado.nombre;
```

### 4. Patrón: Agregación y Métricas
**Cuándo usar:** Dashboards, reportes, análisis de KPIs.

```cypher
// Ejemplo: Métricas de ventas
CREATE 
  // Nodos de tiempo para agregación
  (enero:Mes {nombre: 'Enero', año: 2023, numero: 1}),
  (febrero:Mes {nombre: 'Febrero', año: 2023, numero: 2}),
  (q1:Trimestre {nombre: 'Q1', año: 2023, numero: 1}),
  (año2023:Año {año: 2023}),
  
  // Métricas agregadas
  (metro_enero:Metrica {
    ventas_total: 150000,
    num_pedidos: 45,
    clientes_nuevos: 12
  }),
  (metro_febrero:Metrica {
    ventas_total: 180000,
    num_pedidos: 52,
    clientes_nuevos: 15
  }),
  
  // Relaciones de agregación
  (enero)-[:TIENE_METRICAS]->(metro_enero),
  (febrero)-[:TIENE_METRICAS]->(metro_febrero),
  (enero)-[:PERTENECE_A]->(q1),
  (febrero)-[:PERTENECE_A]->(q1),
  (q1)-[:PERTENECE_A]->(año2023);

// Consultar métricas agregadas por trimestre
MATCH (trimestre:Trimestre)-[:PERTENECE_A]->(año:Año {año: 2023})
MATCH (mes:Mes)-[:PERTENECE_A]->(trimestre)
MATCH (mes)-[:TIENE_METRICAS]->(metrica:Metrica)
RETURN trimestre.nombre,
       sum(metrica.ventas_total) as ventas_trimestre,
       sum(metrica.num_pedidos) as pedidos_trimestre,
       sum(metrica.clientes_nuevos) as nuevos_clientes_trimestre;
```

### 5. Patrón: Recomendación por Filtrado Colaborativo
**Cuándo usar:** Sistemas de recomendación, sugerencias personalizadas.

```cypher
// Ejemplo: Recomendación de libros
CREATE 
  (ana:Usuario {nombre: 'Ana', edad: 28}),
  (bob:Usuario {nombre: 'Bob', edad: 32}),
  (carla:Usuario {nombre: 'Carla', edad: 26}),
  
  (libro1:Libro {titulo: 'Clean Code', autor: 'Robert Martin', genero: 'Técnico'}),
  (libro2:Libro {titulo: 'Design Patterns', autor: 'Gang of Four', genero: 'Técnico'}),
  (libro3:Libro {titulo: 'The Pragmatic Programmer', autor: 'Hunt & Thomas', genero: 'Técnico'}),
  (libro4:Libro {titulo: 'Soft Skills', autor: 'John Sonmez', genero: 'Desarrollo Personal'}),
  
  // Valoraciones (filtrado colaborativo)
  (ana)-[:VALORO {puntuacion: 5}]->(libro1),
  (ana)-[:VALORO {puntuacion: 4}]->(libro2),
  (bob)-[:VALORO {puntuacion: 5}]->(libro1),
  (bob)-[:VALORO {puntuacion: 5}]->(libro3),
  (carla)-[:VALORO {puntuacion: 4}]->(libro2),
  (carla)-[:VALORO {puntuacion: 5}]->(libro4);

// Algoritmo: Usuarios con gustos similares → Recomendaciones
MATCH (usuario_objetivo:Usuario {nombre: 'Ana'})-[v1:VALORO]->(libro_comun:Libro)<-[v2:VALORO]-(usuario_similar:Usuario)
WHERE abs(v1.puntuacion - v2.puntuacion) <= 1  // Valoraciones similares
WITH usuario_objetivo, usuario_similar, count(libro_comun) as libros_en_comun
WHERE libros_en_comun >= 1
MATCH (usuario_similar)-[v:VALORO]->(libro_recomendado:Libro)
WHERE NOT (usuario_objetivo)-[:VALORO]->(libro_recomendado)
  AND v.puntuacion >= 4
RETURN libro_recomendado.titulo, 
       avg(v.puntuacion) as valoracion_promedio,
       count(*) as recomendado_por
ORDER BY valoracion_promedio DESC, recomendado_por DESC;
```

## 4.3 Proyecto práctico: Sistema de gestión académica

### Requisitos del sistema
- Gestionar estudiantes, profesores, cursos, materias, calificaciones
- Prerrequisitos entre materias
- Horarios y aulas
- Sistema de calificaciones y transcripciones
- Análisis de rendimiento académico

### Paso 1: Análisis y diseño del modelo

**Entidades identificadas:**
- Estudiante, Profesor, Materia, Curso, Aula, Semestre
- Calificación, Prerrequisito, Horario

**Relaciones principales:**
- Estudiante INSCRITO_EN Curso
- Profesor ENSEÑA Curso  
- Curso PERTENECE_A Materia
- Materia TIENE_PRERREQUISITO Materia
- Curso SE_DICTA_EN Aula
- Estudiante OBTUVO Calificación

### Paso 2: Implementación del modelo

```cypher
// Limpiar base de datos
MATCH (n) DETACH DELETE n;

// Crear semestres
CREATE 
  (sem_2023_1:Semestre {año: 2023, periodo: 1, nombre: '2023-1', fecha_inicio: date('2023-02-01'), fecha_fin: date('2023-06-30')}),
  (sem_2023_2:Semestre {año: 2023, periodo: 2, nombre: '2023-2', fecha_inicio: date('2023-08-01'), fecha_fin: date('2023-12-15')}),
  (sem_2024_1:Semestre {año: 2024, periodo: 1, nombre: '2024-1', fecha_inicio: date('2024-02-01'), fecha_fin: date('2024-06-30')}),

// Crear aulas
  (aula101:Aula {numero: '101', edificio: 'A', capacidad: 30, tipo: 'Laboratorio'}),
  (aula102:Aula {numero: '102', edificio: 'A', capacidad: 40, tipo: 'Aula Teórica'}),
  (aula201:Aula {numero: '201', edificio: 'B', capacidad: 25, tipo: 'Laboratorio'}),
  (aula_magna:Aula {numero: 'Magna', edificio: 'C', capacidad: 100, tipo: 'Auditorio'}),

// Crear materias con prerrequisitos
  (prog1:Materia {codigo: 'CS101', nombre: 'Programación I', creditos: 4, nivel: 1}),
  (prog2:Materia {codigo: 'CS102', nombre: 'Programación II', creditos: 4, nivel: 2}),
  (estructuras:Materia {codigo: 'CS201', nombre: 'Estructuras de Datos', creditos: 4, nivel: 3}),
  (algoritmos:Materia {codigo: 'CS301', nombre: 'Algoritmos', creditos: 4, nivel: 4}),
  (bd:Materia {codigo: 'CS202', nombre: 'Bases de Datos', creditos: 4, nivel: 3}),
  (matematicas:Materia {codigo: 'MAT101', nombre: 'Matemáticas I', creditos: 3, nivel: 1}),
  (estadistica:Materia {codigo: 'MAT201', nombre: 'Estadística', creditos: 3, nivel: 2}),

// Establecer prerrequisitos
  (prog2)-[:TIENE_PRERREQUISITO]->(prog1),
  (estructuras)-[:TIENE_PRERREQUISITO]->(prog2),
  (algoritmos)-[:TIENE_PRERREQUISITO]->(estructuras),
  (bd)-[:TIENE_PRERREQUISITO]->(prog2),
  (estadistica)-[:TIENE_PRERREQUISITO]->(matematicas),

// Crear profesores
  (prof_garcia:Profesor:Persona {
    id: 'P001', nombre: 'Dr. García', especialidad: 'Algoritmos', 
    años_experiencia: 15, email: 'garcia@universidad.edu'
  }),
  (prof_martinez:Profesor:Persona {
    id: 'P002', nombre: 'Dra. Martínez', especialidad: 'Bases de Datos', 
    años_experiencia: 12, email: 'martinez@universidad.edu'
  }),
  (prof_lopez:Profesor:Persona {
    id: 'P003', nombre: 'Prof. López', especialidad: 'Programación', 
    años_experiencia: 8, email: 'lopez@universidad.edu'
  }),
  (prof_chen:Profesor:Persona {
    id: 'P004', nombre: 'Dr. Chen', especialidad: 'Matemáticas', 
    años_experiencia: 20, email: 'chen@universidad.edu'
  }),

// Crear estudiantes
  (ana:Estudiante:Persona {
    id: 'E001', nombre: 'Ana García', carrera: 'Ingeniería en Sistemas', 
    semestre_actual: 3, fecha_ingreso: date('2022-02-01'), promedio_general: 8.5
  }),
  (bob:Estudiante:Persona {
    id: 'E002', nombre: 'Bob Johnson', carrera: 'Ingeniería en Sistemas', 
    semestre_actual: 4, fecha_ingreso: date('2021-08-01'), promedio_general: 9.2
  }),
  (carla:Estudiante:Persona {
    id: 'E003', nombre: 'Carla López', carrera: 'Ingeniería en Sistemas', 
    semestre_actual: 2, fecha_ingreso: date('2022-08-01'), promedio_general: 7.8
  }),
  (david:Estudiante:Persona {
    id: 'E004', nombre: 'David Chen', carrera: 'Ingeniería en Sistemas', 
    semestre_actual: 1, fecha_ingreso: date('2024-02-01'), promedio_general: 8.0
  }),

// Crear cursos (instancias de materias en semestres específicos)
  (curso_prog1_23_1:Curso {
    id: 'C001', seccion: 'A', cupo_maximo: 30, 
    horario: 'Lunes 8-10, Miércoles 8-10'
  }),
  (curso_prog2_23_1:Curso {
    id: 'C002', seccion: 'A', cupo_maximo: 25, 
    horario: 'Martes 10-12, Jueves 10-12'
  }),
  (curso_estructuras_23_2:Curso {
    id: 'C003', seccion: 'A', cupo_maximo: 20, 
    horario: 'Lunes 14-16, Miércoles 14-16'
  }),
  (curso_bd_23_2:Curso {
    id: 'C004', seccion: 'A', cupo_maximo: 25, 
    horario: 'Martes 8-10, Jueves 8-10'
  }),
  (curso_algoritmos_24_1:Curso {
    id: 'C005', seccion: 'A', cupo_maximo: 20, 
    horario: 'Lunes 10-12, Miércoles 10-12'
  }),
  (curso_matematicas_24_1:Curso {
    id: 'C006', seccion: 'A', cupo_maximo: 35, 
    horario: 'Martes 14-16, Jueves 14-16'
  }),

// Relacionar cursos con materias y semestres
  (curso_prog1_23_1)-[:INSTANCIA_DE]->(prog1),
  (curso_prog1_23_1)-[:DICTADO_EN]->(sem_2023_1),
  (curso_prog2_23_1)-[:INSTANCIA_DE]->(prog2),
  (curso_prog2_23_1)-[:DICTADO_EN]->(sem_2023_1),
  (curso_estructuras_23_2)-[:INSTANCIA_DE]->(estructuras),
  (curso_estructuras_23_2)-[:DICTADO_EN]->(sem_2023_2),
  (curso_bd_23_2)-[:INSTANCIA_DE]->(bd),
  (curso_bd_23_2)-[:DICTADO_EN]->(sem_2023_2),
  (curso_algoritmos_24_1)-[:INSTANCIA_DE]->(algoritmos),
  (curso_algoritmos_24_1)-[:DICTADO_EN]->(sem_2024_1),
  (curso_matematicas_24_1)-[:INSTANCIA_DE]->(matematicas),
  (curso_matematicas_24_1)-[:DICTADO_EN]->(sem_2024_1),

// Asignar profesores a cursos
  (prof_lopez)-[:ENSEÑA]->(curso_prog1_23_1),
  (prof_lopez)-[:ENSEÑA]->(curso_prog2_23_1),
  (prof_garcia)-[:ENSEÑA]->(curso_estructuras_23_2),
  (prof_martinez)-[:ENSEÑA]->(curso_bd_23_2),
  (prof_garcia)-[:ENSEÑA]->(curso_algoritmos_24_1),
  (prof_chen)-[:ENSEÑA]->(curso_matematicas_24_1),

// Asignar aulas a cursos
  (curso_prog1_23_1)-[:SE_DICTA_EN]->(aula101),
  (curso_prog2_23_1)-[:SE_DICTA_EN]->(aula101),
  (curso_estructuras_23_2)-[:SE_DICTA_EN]->(aula201),
  (curso_bd_23_2)-[:SE_DICTA_EN]->(aula102),
  (curso_algoritmos_24_1)-[:SE_DICTA_EN]->(aula201),
  (curso_matematicas_24_1)-[:SE_DICTA_EN]->(aula_magna),

// Inscribir estudiantes en cursos
  (ana)-[:INSCRITO_EN {fecha_inscripcion: date('2023-01-15')}]->(curso_prog1_23_1),
  (bob)-[:INSCRITO_EN {fecha_inscripcion: date('2023-01-15')}]->(curso_prog2_23_1),
  (carla)-[:INSCRITO_EN {fecha_inscripcion: date('2023-01-15')}]->(curso_prog1_23_1),
  (david)-[:INSCRITO_EN {fecha_inscripcion: date('2024-01-15')}]->(curso_matematicas_24_1),
  
  (ana)-[:INSCRITO_EN {fecha_inscripcion: date('2023-07-15')}]->(curso_estructuras_23_2),
  (bob)-[:INSCRITO_EN {fecha_inscripcion: date('2023-07-15')}]->(curso_bd_23_2),
  (carla)-[:INSCRITO_EN {fecha_inscripcion: date('2023-07-15')}]->(curso_estructuras_23_2),
  
  (bob)-[:INSCRITO_EN {fecha_inscripcion: date('2024-01-15')}]->(curso_algoritmos_24_1),

// Crear calificaciones
  (ana)-[:OBTUVO {
    nota_final: 8.5, parcial1: 8.0, parcial2: 9.0, trabajos: 8.5, 
    fecha_calificacion: date('2023-06-15'), estado: 'Aprobado'
  }]->(curso_prog1_23_1),
  
  (bob)-[:OBTUVO {
    nota_final: 9.2, parcial1: 9.0, parcial2: 9.5, trabajos: 9.0, 
    fecha_calificacion: date('2023-06-15'), estado: 'Aprobado'
  }]->(curso_prog2_23_1),
  
  (carla)-[:OBTUVO {
    nota_final: 7.8, parcial1: 7.5, parcial2: 8.0, trabajos: 8.0, 
    fecha_calificacion: date('2023-06-15'), estado: 'Aprobado'
  }]->(curso_prog1_23_1),
  
  (ana)-[:OBTUVO {
    nota_final: 8.8, parcial1: 8.5, parcial2: 9.0, trabajos: 9.0, 
    fecha_calificacion: date('2023-12-15'), estado: 'Aprobado'
  }]->(curso_estructuras_23_2),
  
  (bob)-[:OBTUVO {
    nota_final: 9.5, parcial1: 9.2, parcial2: 9.8, trabajos: 9.5, 
    fecha_calificacion: date('2023-12-15'), estado: 'Aprobado'
  }]->(curso_bd_23_2),
  
  (carla)-[:OBTUVO {
    nota_final: 6.8, parcial1: 6.5, parcial2: 7.0, trabajos: 7.0, 
    fecha_calificacion: date('2023-12-15'), estado: 'Aprobado'
  }]->(curso_estructuras_23_2);
```

### Paso 3: Consultas de análisis académico

**1. Transcripción académica de un estudiante:**
```cypher
MATCH (estudiante:Estudiante {nombre: 'Ana García'})-[calificacion:OBTUVO]->(curso:Curso)-[:INSTANCIA_DE]->(materia:Materia)
MATCH (curso)-[:DICTADO_EN]->(semestre:Semestre)
RETURN 
  semestre.año AS año,
  semestre.periodo AS periodo,
  semestre.nombre AS semestre,
  materia.codigo AS codigo,
  materia.nombre AS materia,
  materia.creditos AS creditos,
  calificacion.nota_final AS nota,
  calificacion.estado AS estado
ORDER BY semestre.año, semestre.periodo, materia.codigo;
```

**2. Análisis de rendimiento por profesor:**
```cypher
MATCH (profesor:Profesor)-[:ENSEÑA]->(curso:Curso)<-[calificacion:OBTUVO]-(estudiante:Estudiante)
MATCH (curso)-[:INSTANCIA_DE]->(materia:Materia)
RETURN profesor.nombre,
       materia.nombre,
       count(calificacion) as total_estudiantes,
       avg(calificacion.nota_final) as promedio_curso,
       count(CASE WHEN calificacion.estado = 'Aprobado' THEN 1 END) as aprobados,
       round(100.0 * count(CASE WHEN calificacion.estado = 'Aprobado' THEN 1 END) / count(calificacion), 2) as porcentaje_aprobacion
ORDER BY promedio_curso DESC
```

**3. Verificación de prerrequisitos:**
```cypher
// Verificar si un estudiante puede inscribirse en una materia
MATCH (estudiante:Estudiante {nombre: 'Ana García'})
MATCH (materia_objetivo:Materia {codigo: 'CS301'})  // Algoritmos
OPTIONAL MATCH (materia_objetivo)-[:TIENE_PRERREQUISITO*]->(prerrequisito:Materia)
OPTIONAL MATCH (estudiante)-[:OBTUVO {estado: 'Aprobado'}]->(curso_aprobado:Curso)-[:INSTANCIA_DE]->(materia_aprobada:Materia)

WITH estudiante, materia_objetivo, 
     collect(DISTINCT prerrequisito.codigo) as prerrequisitos_necesarios,
     collect(DISTINCT materia_aprobada.codigo) as materias_aprobadas

RETURN estudiante.nombre,
       materia_objetivo.codigo,
       prerrequisitos_necesarios,
       materias_aprobadas,
       ALL(prereq IN prerrequisitos_necesarios WHERE prereq IN materias_aprobadas) as puede_inscribirse;
```

**4. Planificación de horarios (detectar conflictos):**
```cypher
MATCH (estudiante:Estudiante {nombre: 'Bob Johnson'})-[:INSCRITO_EN]->(curso1:Curso)
MATCH (estudiante)-[:INSCRITO_EN]->(curso2:Curso)
MATCH (curso1)-[:DICTADO_EN]->(semestre:Semestre)<-[:DICTADO_EN]-(curso2)
WHERE curso1 <> curso2
  AND curso1.horario CONTAINS 'Lunes'
  AND curso2.horario CONTAINS 'Lunes'
RETURN estudiante.nombre,
       curso1.horario as horario1,
       curso2.horario as horario2,
       'Posible conflicto de horarios' as alerta;
```

**5. Ranking de estudiantes por promedio:**
```cypher
MATCH (estudiante:Estudiante)-[calificacion:OBTUVO]->(curso:Curso)-[:INSTANCIA_DE]->(materia:Materia)
WITH estudiante, 
     sum(calificacion.nota_final * materia.creditos) as puntos_totales,
     sum(materia.creditos) as creditos_totales
RETURN estudiante.nombre,
       estudiante.carrera,
       creditos_totales,
       round(puntos_totales / creditos_totales, 2) as promedio_ponderado
ORDER BY promedio_ponderado DESC;
```

**6. Análisis de utilización de aulas:**
```cypher
MATCH (aula:Aula)<-[:SE_DICTA_EN]-(curso:Curso)-[:DICTADO_EN]->(semestre:Semestre {nombre: '2023-2'})
MATCH (curso)<-[:INSCRITO_EN]-(estudiante:Estudiante)
RETURN aula.numero as aula,
       aula.edificio as edificio,
       aula.capacidad as capacidad,
       count(DISTINCT curso) as cursos_programados,
       count(estudiante) as total_estudiantes,
       round(100.0 * count(estudiante) / (aula.capacidad * count(DISTINCT curso)), 2) as porcentaje_ocupacion
ORDER BY porcentaje_ocupacion DESC;
```

### Paso 4: Funciones avanzadas para análisis académico

**1. Detección de estudiantes en riesgo académico:**
```cypher
MATCH (estudiante:Estudiante)-[calificacion:OBTUVO]->(curso:Curso)
WHERE calificacion.nota_final < 7.0
WITH estudiante, count(calificacion) as materias_reprobadas
WHERE materias_reprobadas >= 2
MATCH (estudiante)-[cal:OBTUVO]->(c:Curso)-[:INSTANCIA_DE]->(materia:Materia)
RETURN estudiante.nombre,
       estudiante.carrera,
       materias_reprobadas,
       avg(cal.nota_final) as promedio_actual,
       'Estudiante en riesgo' as alerta
ORDER BY materias_reprobadas DESC, promedio_actual ASC;
```

**2. Recomendaciones de materias para el próximo semestre:**
```cypher
MATCH (estudiante:Estudiante {nombre: 'Ana García'})-[:OBTUVO {estado: 'Aprobado'}]->(curso_aprobado:Curso)-[:INSTANCIA_DE]->(materia_aprobada:Materia)
WITH estudiante, collect(materia_aprobada.codigo) as materias_completadas

MATCH (materia_disponible:Materia)
WHERE NOT materia_disponible.codigo IN materias_completadas
OPTIONAL MATCH (materia_disponible)-[:TIENE_PRERREQUISITO*]->(prerrequisito:Materia)
WITH estudiante, materia_disponible, materias_completadas,
     collect(prerrequisito.codigo) as prerrequisitos_necesarios

WHERE ALL(prereq IN prerrequisitos_necesarios WHERE prereq IN materias_completadas)
RETURN materia_disponible.codigo,
       materia_disponible.nombre,
       materia_disponible.creditos,
       materia_disponible.nivel,
       prerrequisitos_necesarios
ORDER BY materia_disponible.nivel, materia_disponible.codigo;
```

**3. Análisis de progresión académica:**
```cypher
MATCH (estudiante:Estudiante)-[calificacion:OBTUVO]->(curso:Curso)-[:DICTADO_EN]->(semestre:Semestre)
MATCH (curso)-[:INSTANCIA_DE]->(materia:Materia)
WITH 
  estudiante, 
  semestre,
  count(materia) AS materias_cursadas,
  sum(materia.creditos) AS creditos_semestre,
  avg(calificacion.nota_final) AS promedio_semestre
ORDER BY semestre.año, semestre.periodo
WITH estudiante,
     collect({
       semestre: semestre,
       materias_cursadas: materias_cursadas,
       creditos_semestre: creditos_semestre,
       promedio: promedio_semestre
     }) AS datos_semestres
WITH estudiante, datos_semestres, range(0, size(datos_semestres)-1) AS idxs
UNWIND idxs AS i
WITH estudiante, datos_semestres, i,
     datos_semestres[i] AS actual,
     CASE 
       WHEN i=0 THEN null
       ELSE datos_semestres[i-1].promedio
     END AS promedio_anterior
RETURN 
   estudiante.nombre,
   actual.semestre.nombre AS semestre,
   actual.materias_cursadas AS materias_cursadas,
   actual.creditos_semestre AS creditos_semestre,
   actual.promedio AS promedio_semestre,
   promedio_anterior
ORDER BY estudiante.nombre, actual.semestre.año, actual.semestre.periodo;
```

## 4.4 Importación de datos desde CSV

### Preparación de datos
```cypher
// Ejemplo: Importar estudiantes desde CSV
LOAD CSV WITH HEADERS FROM 'file:///estudiantes.csv' AS row
MERGE (e:Estudiante {id: row.student_id})
SET e.nombre = row.nombre,
    e.email = row.email,
    e.carrera = row.carrera,
    e.fecha_ingreso = date(row.fecha_ingreso),
    e.semestre_actual = toInteger(row.semestre_actual);

// Importar calificaciones con relaciones
LOAD CSV WITH HEADERS FROM 'file:///calificaciones.csv' AS row
MATCH (estudiante:Estudiante {id: row.student_id})
MATCH (curso:Curso {id: row.course_id})
MERGE (estudiante)-[:OBTUVO {
  nota_final: toFloat(row.nota_final),
  parcial1: toFloat(row.parcial1),
  parcial2: toFloat(row.parcial2),
  trabajos: toFloat(row.trabajos),
  fecha_calificacion: date(row.fecha_calificacion),
  estado: row.estado
}]->(curso);
```

### Validación de datos importados
```cypher
// Verificar integridad de datos
MATCH (e:Estudiante)
WHERE e.email IS NULL OR e.nombre IS NULL
RETURN count(e) as estudiantes_sin_datos_completos;

// Verificar relaciones huérfanas
MATCH (calificacion:OBTUVO)
WHERE NOT EXISTS((:Estudiante)-[:OBTUVO]-(:Curso))
RETURN count(calificacion) as calificaciones_huerfanas;
```

## Resumen

En esta parte hemos aprendido:

- ✅ Principios fundamentales del modelado de grafos
- ✅ Patrones comunes: entidades conectadas, timeline, jerarquías, métricas
- ✅ Proyecto completo: Sistema de gestión académica
- ✅ Consultas avanzadas para análisis de datos
- ✅ Importación y validación de datos desde CSV
