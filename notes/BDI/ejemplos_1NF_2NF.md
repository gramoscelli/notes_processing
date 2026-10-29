
## 📘 Enunciado – Normalización de Bases de Datos (FN1 y FN2)

El objetivo de este trabajo es analizar y normalizar diferentes conjuntos de datos reales que inicialmente se encuentran en tablas **no normalizadas** (forma plana), con datos repetidos y valores multivaluados. Se deberán aplicar las reglas de **Primera Forma Normal (FN1)** y **Segunda Forma Normal (FN2)** para mejorar la estructura, eliminar redundancias y garantizar la integridad de los datos.

Se trabajará con tres dominios diferentes:

---

### ✅ Caso 1: Sistema de Ventas

Una empresa de tecnología almacena información de ventas incluyendo cliente, fecha y productos vendidos con sus cantidades. El diseño inicial contiene datos repetidos dentro de una misma fila (listados de productos y cantidades), generando **dependencias parciales y redundancias**.

**Objetivo:**
Aplicar normalización hasta FN2 para obtener:

* Una tabla de clientes.
* Una tabla de productos.
* Una tabla de ventas (cabecera).
* Una tabla de detalle de ventas (líneas de productos por venta).

Se debe garantizar integridad entre ventas y sus detalles mediante claves foráneas.

---

### ✅ Caso 2: Inscripción a Cursos

Un instituto educativo registra inscripciones de estudiantes a cursos. En el diseño original, cada alumno puede tener una lista de cursos en una sola fila, y cada curso tiene asignado un profesor. Esto genera **atributos multivaluados** y **dependencia de atributos no clave** (el profesor depende del curso, no del estudiante).

**Objetivo:**
Normalizar hasta FN2 obteniendo:

* Una tabla de estudiantes.
* Una tabla de cursos.
* Una tabla intermedia de inscripción (relación muchos a muchos).

Se deben eliminar dependencias parciales y evitar redundancia del dato "profesor".

---

### ✅ Caso 3: Préstamos de Biblioteca

Una biblioteca registra préstamos realizados por sus socios, donde en cada préstamo puede haber uno o varios libros. El diseño plano original contiene una lista de libros en una sola celda para cada préstamo, provocando **grupos repetitivos** y dificultades para consultas consistentes.

**Objetivo:**
Reestructurar el modelo hasta FN2 logrando:

* Una tabla de socios.
* Una tabla de libros.
* Una tabla de préstamos (cabecera).
* Una tabla detalle por cada libro prestado.

Debe garantizarse consistencia de préstamos a través de claves compuestas y relaciones.

---

## 🧩 Objetivos Didácticos

Con estos tres casos se busca:
✔ Comprender cómo detectar violaciones a FN1 y FN2.
✔ Transformar tablas con valores multivaluados en estructuras relacionales correctas.
✔ Identificar y resolver dependencias parciales.
✔ Construir claves primarias y foráneas correctamente.
✔ Diferenciar cabecera y detalle en relaciones uno a muchos.
✔ Modelar relaciones muchos a muchos correctamente.

