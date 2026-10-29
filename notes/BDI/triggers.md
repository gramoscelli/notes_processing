
# Triggers (Disparadores)

## ¿Qué es un Trigger?

Un *trigger* o *disparador* es un bloque de código SQL que se ejecuta automáticamente cuando ocurre un evento en una tabla, como una **inserción**, **actualización** o **eliminación**.

**Características:**

* Se asocia a una tabla específica.
* Se activa antes o después del evento (`BEFORE` / `AFTER`).
* Puede servir para validar datos, mantener auditorías o actualizar otras tablas.

```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="350" viewBox="0 0 900 350">
  <defs>
    <style>
      .title { font: bold 28px sans-serif; fill: #333; }
      .label { font: 16px sans-serif; fill: #ffffff; }
      .small-label { font: 16px sans-serif; fill: #333333; }
      .combo-text { font: 18px sans-serif; fill: #4a4a4a; }
      .chip { fill: #ffffff; stroke: none; rx: 12; ry: 12; }
      .band-time { fill: #b22222; rx: 14; ry: 14; }
      .band-event { fill: #0d5e95; rx: 14; ry: 14; }
      .panel { fill: #f2f4f7; stroke: #999; stroke-width: 2; rx: 16; ry: 16; }
      .arrow { stroke: #333; stroke-width: 3; fill: none; marker-end: url(#arrowhead); }
      .vline { stroke: #333; stroke-width: 3; }
      .chip-outline { fill: #ffffff; stroke: #dddddd; stroke-width: 2; rx: 10; ry: 10; }
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="40" text-anchor="middle" class="title">MySQL Triggers</text>

  <!-- TIME band -->
  <rect x="40" y="80" width="500" height="80" class="band-time"/>
  <text x="70" y="102" class="label" dy="-6" font-weight="bold"> </text>
  <text x="65" y="130" class="label" fill="#ffffff" font-weight="bold">Time</text>

  <!-- BEFORE / AFTER chips in TIME band -->
  <rect x="140" y="95" width="140" height="50" class="chip-outline"/>
  <text x="210" y="125" text-anchor="middle" class="small-label" fill="#333333" font-weight="bold">BEFORE</text>

  <rect x="320" y="95" width="140" height="50" class="chip-outline"/>
  <text x="390" y="125" text-anchor="middle" class="small-label" fill="#333333" font-weight="bold">AFTER</text>

  <!-- EVENT band -->
  <rect x="40" y="190" width="650" height="90" class="band-event"/>
  <text x="65" y="215" class="label" font-weight="bold">Event</text>

  <!-- INSERT / UPDATE / DELETE chips -->
  <rect x="140" y="205" width="140" height="55" class="chip-outline"/>
  <text x="210" y="238" text-anchor="middle" class="small-label" font-weight="bold">INSERT</text>

  <rect x="320" y="205" width="140" height="55" class="chip-outline"/>
  <text x="390" y="238" text-anchor="middle" class="small-label" font-weight="bold">UPDATE</text>

  <rect x="500" y="205" width="140" height="55" class="chip-outline"/>
  <text x="570" y="238" text-anchor="middle" class="small-label" font-weight="bold">DELETE</text>

  <!-- Connector arrow to combinations panel -->
  <path d="M 480 120 L 710 120" class="arrow"/>
  <line x1="620" y1="120" x2="620" y2="190" class="vline"/>

  <!-- Combinations panel -->
  <rect x="710" y="70" width="180" height="220" class="panel"/>
  <text x="725" y="110" class="combo-text">BEFORE INSERT</text>
  <text x="725" y="140" class="combo-text">AFTER INSERT</text>
  <text x="725" y="170" class="combo-text">BEFORE UPDATE</text>
  <text x="725" y="200" class="combo-text">AFTER UPDATE</text>
  <text x="725" y="230" class="combo-text">BEFORE DELETE</text>
  <text x="725" y="260" class="combo-text">AFTER DELETE</text>

</svg>
```

## ⚙️ Tipos de Triggers

1. **BEFORE INSERT / UPDATE / DELETE**
   Se ejecutan **antes** de que la operación ocurra.
   Útiles para **validar datos o modificar valores**.

2. **AFTER INSERT / UPDATE / DELETE**
   Se ejecutan **después** de la operación.
   Útiles para **registrar cambios** o **actualizar tablas relacionadas**.



## 🧱 Sintaxis Básica de un Trigger en MySQL

```sql
DELIMITER $$
CREATE TRIGGER nombre_trigger
{BEFORE | AFTER} {INSERT | UPDATE | DELETE}
ON nombre_tabla
FOR EACH ROW
BEGIN
   -- Código a ejecutar
END$$
DELIMITER ;
```



## 🧩 Ejemplo 1 – Auditoría de Inserciones

```sql
DELIMITER $$
CREATE TRIGGER log_insert_empleado
AFTER INSERT ON empleados
FOR EACH ROW
BEGIN
   INSERT INTO auditoria_empleados (empleado_id, accion, fecha)
   VALUES (NEW.id, 'INSERT', NOW());
END$$
DELIMITER ;
```

**Explicación:**

* `NEW.id` hace referencia al nuevo registro insertado.
* Guarda un registro en la tabla `auditoria_empleados` cada vez que se agrega un empleado.



## 🧩 Ejemplo 2 – Validación Antes de Insertar

```sql
DELIMITER $$
CREATE TRIGGER validar_salario
BEFORE INSERT ON empleados
FOR EACH ROW
BEGIN
   IF NEW.salario < 0 THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'El salario no puede ser negativo';
   END IF;
END$$
DELIMITER ;
```

**Explicación:**
Evita que se inserten empleados con salarios negativos usando `SIGNAL` para lanzar un error.



## 🧩 Eliminar un Trigger

```sql
DROP TRIGGER IF EXISTS nombre_trigger;
```

## Más ejemplos prácticos


### 🧩 Ejemplo 3 – Registrar Inserciones (AFTER INSERT)

**Objetivo:** Crear una auditoría automática cuando se inserta un nuevo empleado.

```sql
DELIMITER $$
CREATE TRIGGER auditoria_empleado_insert
AFTER INSERT ON empleados
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_empleados (empleado_id, accion, fecha)
    VALUES (NEW.id, 'INSERCIÓN', NOW());
END$$
DELIMITER ;
```

**Explicación:**
Cada vez que se inserta un empleado, se guarda un registro en la tabla `auditoria_empleados` indicando la acción y la fecha.



### 🧩 Ejemplo 4 – Validar Datos (BEFORE INSERT)

**Objetivo:** Evitar que se inserten salarios negativos.

```sql
DELIMITER $$
CREATE TRIGGER validar_salario
BEFORE INSERT ON empleados
FOR EACH ROW
BEGIN
    IF NEW.salario < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El salario no puede ser negativo';
    END IF;
END$$
DELIMITER ;
```

**Explicación:**
Antes de insertar un empleado, el trigger verifica el valor de `salario`. Si es negativo, lanza un error y cancela la operación.



### 🧩 Ejemplo 5 – Actualizar Stock (AFTER INSERT)

**Objetivo:** Cada vez que se inserta una venta, reducir el stock del producto.

```sql
DELIMITER $$
CREATE TRIGGER actualizar_stock
AFTER INSERT ON ventas
FOR EACH ROW
BEGIN
    UPDATE productos
    SET stock = stock - NEW.cantidad
    WHERE id = NEW.producto_id;
END$$
DELIMITER ;
```

**Explicación:**
Después de registrar una venta, se actualiza automáticamente el stock del producto correspondiente.



### 🧩 Ejemplo 6 – Controlar Modificaciones (BEFORE UPDATE)

**Objetivo:** Evitar que se baje el salario de un empleado sin autorización.

```sql
DELIMITER $$
CREATE TRIGGER evitar_baja_salario
BEFORE UPDATE ON empleados
FOR EACH ROW
BEGIN
    IF NEW.salario < OLD.salario THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede disminuir el salario sin autorización';
    END IF;
END$$
DELIMITER ;
```

**Explicación:**
Compara el salario nuevo con el anterior (`OLD.salario`). Si es menor, bloquea la actualización.



### 🧩 Ejemplo 7 – Registrar Eliminaciones (BEFORE DELETE)

**Objetivo:** Mantener un historial de registros eliminados.

```sql
DELIMITER $$
CREATE TRIGGER backup_empleado
BEFORE DELETE ON empleados
FOR EACH ROW
BEGIN
    INSERT INTO empleados_eliminados (id, nombre, apellido, fecha_eliminacion)
    VALUES (OLD.id, OLD.nombre, OLD.apellido, NOW());
END$$
DELIMITER ;
```

**Explicación:**
Antes de eliminar un registro de `empleados`, se guarda una copia en `empleados_eliminados`.



### 🧩 Ejemplo 8 – Evitar Borrado de Clientes con Ventas (BEFORE DELETE)

**Objetivo:** Impedir la eliminación de clientes con ventas asociadas.

```sql
DELIMITER $$
CREATE TRIGGER evitar_borrado_cliente
BEFORE DELETE ON clientes
FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*) FROM ventas WHERE cliente_id = OLD.id) > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede eliminar un cliente con ventas registradas';
    END IF;
END$$
DELIMITER ;
```

**Explicación:**
Antes de borrar un cliente, el trigger revisa si tiene ventas. Si las hay, lanza un error.



### 🧩 Ejemplo 9 – Sumar Ventas al Total del Día (AFTER INSERT)

**Objetivo:** Actualizar el total de ventas diarias automáticamente.

```sql
DELIMITER $$
CREATE TRIGGER sumar_total_ventas
AFTER INSERT ON ventas
FOR EACH ROW
BEGIN
    UPDATE resumen_diario
    SET total = total + NEW.monto
    WHERE fecha = CURDATE();
END$$
DELIMITER ;
```

**Explicación:**
Cada vez que se registra una venta, se suma su monto al total del día.
