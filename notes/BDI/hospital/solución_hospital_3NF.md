# Identificación de los problemas

| Problema                                  | Explicación                                                                                        |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------- |
| ❌ Teléfonos múltiples en una celda        | Se deben volver filas atómicas (un teléfono por fila).                                             |
| ❌ Especialidades del médico en lista      | Deben separarse en filas (una especialidad por fila).                                              |
| ❌ Síntomas listados en una sola celda     | Un síntoma por fila para cumplir 1FN.                                                              |
| ❌ Prácticas solicitadas separadas por “;” | Una práctica por fila (tabla detalle).                                                             |
| ⚠️ Paciente y Médico como texto libre     | Para 1FN **no es obligatorio** separar entidades, pero conviene dejar preparado el paso a 2FN/3FN. |

> La consigna y el fragmento de tabla “no normalizada” mantienen el **estilo del enunciado** que compartiste para comercio electrónico (presentación + actividades + muestra de tabla). 

# Transformación esperada a **1FN**

Se propone mantener una tabla de **cabecera** y crear **tablas de detalle** para cada campo multivaluado. Con esto se logra que **cada celda** de cada tabla tenga **un solo valor**:

**1) Turnos** (cabecera)
`turnos(id_turno PK, paciente, telefonos_paciente* , obra_social, medico, especialidades_medico* , fecha_turno, hora_turno, consultorio, sintomas_reportados* , practicas_solicitadas* )`

> *Campos marcados con * desaparecen al mover los valores a tablas de detalle.*

**2) Tablas detalle (1 a N respecto de `turnos`)**

* `turno_telefono(id_turno FK, telefono)` → **(id_turno, telefono) PK**
* `turno_especialidad(id_turno FK, especialidad)` → **(id_turno, especialidad) PK**
* `turno_sintoma(id_turno FK, sintoma)` → **(id_turno, sintoma) PK**
* `turno_practica(id_turno FK, practica)` → **(id_turno, practica) PK**

> Con esto, todos los atributos que eran **listas** pasan a ser **filas**, cumpliendo 1FN.

### DDL sugerido para MySQL – 1FN directo

```sql
-- Cabecera
CREATE TABLE turnos (
  id_turno INT PRIMARY KEY,
  paciente VARCHAR(100) NOT NULL,
  obra_social VARCHAR(100) NOT NULL,
  medico VARCHAR(100) NOT NULL,
  fecha_turno DATE NOT NULL,
  hora_turno TIME NOT NULL,
  consultorio VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Detalles multivaluados
CREATE TABLE turno_telefono (
  id_turno INT NOT NULL,
  telefono VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_turno, telefono),
  CONSTRAINT fk_tel_turno FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE turno_especialidad (
  id_turno INT NOT NULL,
  especialidad VARCHAR(80) NOT NULL,
  PRIMARY KEY (id_turno, especialidad),
  CONSTRAINT fk_esp_turno FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE turno_sintoma (
  id_turno INT NOT NULL,
  sintoma VARCHAR(120) NOT NULL,
  PRIMARY KEY (id_turno, sintoma),
  CONSTRAINT fk_sin_turno FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE turno_practica (
  id_turno INT NOT NULL,
  practica VARCHAR(120) NOT NULL,
  PRIMARY KEY (id_turno, practica),
  CONSTRAINT fk_pra_turno FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### Guía de transformación de datos

Suponiendo que partís del dataset **no normalizado** (`turnos_no_normalizada.sql`) que ya generamos:

**1. Cargar cabecera `turnos` (sin los campos multivaluados):**

```sql
INSERT INTO turnos (id_turno, paciente, obra_social, medico, fecha_turno, hora_turno, consultorio)
SELECT
  id_turno, paciente, obra_social, medico, fecha_turno, hora_turno, consultorio
FROM turnos_origen; -- la tabla original importada (no 1FN)
```

**2. Explosión de teléfonos a `turno_telefono`**
(Separados por `" / "` en la fuente)

```sql
-- Ejemplo genérico usando una tabla auxiliar de números o función split definida por el docente.
-- Alternativa manual en prácticas: exportar, dividir y reimportar.
```

**3. Explosión de especialidades a `turno_especialidad`**
(Separadas por coma en la fuente)

**4. Explosión de síntomas a `turno_sintoma`**
(Separados por coma en la fuente)

**5. Explosión de prácticas a `turno_practica`**
(Separadas por `;` en la fuente)

> Nota didáctica: MySQL no trae un `SPLIT()` nativo que devuelva filas; se puede:
>
> * Usar **CTEs + números** (0–N) y `SUBSTRING_INDEX` para particionar,
> * Apoyarse en **procedimientos almacenados**,
> * O resolver con **ETL rápido** (CSV → planilla → reimportar).

---
# 🚦 2FN
## Recordatorio rápido, ¿qué exige 2FN?

Una tabla está en **Segunda Forma Normal (2FN)** si:

1. Está en **1FN**, y
2. **No hay dependencias parciales**: ningún atributo no clave depende de **una parte** de una **clave candidata compuesta**.

> Importante didáctico: si usás un **ID artificial** (surrogate key) como clave primaria de una tabla (p. ej. `id_turno`), **2FN se cumple “vacíamente”** en esa tabla porque la clave no es compuesta. Aun así, pueden quedar **anomalías** por atributos que dependen de otras entidades (paciente, médico, obra social…). Por eso conviene **revisar las dependencias lógicas** y separar entidades.


## ❓ Por qué, conceptualmente, “no es 2FN” (visión de dependencias)

Tomemos la tabla **`turnos`** (cabecera) que tenés en 1FN:

```
turnos(id_turno PK, paciente, obra_social, medico, fecha_turno, hora_turno, consultorio)
```

* **Dependencias lógicas esperables**:

  * `paciente → obra_social` (la obra social está asociada a la persona, no al turno puntual).
  * `medico → {especialidades}` (las especialidades son propiedad del médico, no del turno).
  * `consultorio` suele depender de la **asignación** del médico/agenda (no estrictamente del turno).
* Si considerás una **clave candidata natural compuesta** para `turnos`, por ejemplo
  **K = (paciente, fecha_turno, hora_turno)** (o con consultorio), entonces:

  * `obra_social` depende **solo de `paciente`**, **no de toda la clave** → **dependencia parcial** → **viola 2FN**.
* Aunque en tu DDL 1FN la PK sea `id_turno` (clave simple), la **estructura sigue cargando atributos que pertenecen a otras entidades**; si cambiás a una clave compuesta natural (recurso didáctico típico para enseñar 2FN), se ve claro dónde están las dependencias parciales.


## 🧭 Pasos para llegar a 2FN (esquema propuesto)

> Objetivo: separar los atributos que dependen de **subconjuntos** de una clave candidata compuesta (o, más simple, **de otras entidades**), y dejar en `turnos` solo lo que **depende del turno**.

### Paso 1 — Identificar claves candidatas y dependencias

* Clave candidata natural (ejemplo): **(paciente, fecha_turno, hora_turno)**.
* Dependencias parciales típicas:

  * `paciente → obra_social`
  * `medico → especialidades`
  * (Opcional) `consultorio` puede modelarse como entidad si lo asigna agenda.

### Paso 2 — Extraer **Pacientes** y su **Obra Social**

Crear entidad **`pacientes`** y relacionarla con **`obras_sociales`** (con vigencia si aplica).

```sql
CREATE TABLE pacientes (
  id_paciente INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE obras_sociales (
  id_obra INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Si cada paciente tiene una sola obra social actual:
ALTER TABLE pacientes ADD id_obra INT, 
  ADD CONSTRAINT fk_paciente_obra FOREIGN KEY (id_obra) REFERENCES obras_sociales(id_obra);

-- Si querés historial/vigencia:
CREATE TABLE paciente_obra_social (
  id_paciente INT NOT NULL,
  id_obra INT NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NULL,
  PRIMARY KEY (id_paciente, id_obra, fecha_inicio),
  FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
  FOREIGN KEY (id_obra) REFERENCES obras_sociales(id_obra)
);
```

> Resultado: `obra_social` **sale de `turnos`**. Ya no depende (parcialmente) de una clave compuesta del turno, sino de **paciente**.

### Paso 3 — Extraer **Médicos** y sus **Especialidades**

```sql
CREATE TABLE medicos (
  id_medico INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

CREATE TABLE especialidades (
  id_especialidad INT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE medico_especialidad (
  id_medico INT NOT NULL,
  id_especialidad INT NOT NULL,
  PRIMARY KEY (id_medico, id_especialidad),
  FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
  FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
);
```

> Resultado: las **especialidades** dejan de “pegarse” al turno. **Dependen del médico**, no de la clave del turno.

### Paso 4 — (Opcional recomendable) **Consultorios** como entidad

```sql
CREATE TABLE consultorios (
  id_consultorio INT PRIMARY KEY,
  codigo VARCHAR(20) NOT NULL UNIQUE
);
```

> Si el consultorio es un catálogo (C1, C2, …), conviene FK. Si depende de la agenda del médico, la relación se modela en el **slot** de agenda (ver paso 6, opcional).

### Paso 5 — Redefinir **Turnos** apuntando a las entidades

```sql
CREATE TABLE turnos (
  id_turno INT PRIMARY KEY,
  id_paciente INT NOT NULL,
  id_medico INT NOT NULL,
  fecha_turno DATE NOT NULL,
  hora_turno TIME NOT NULL,
  id_consultorio INT NULL,
  FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
  FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
  FOREIGN KEY (id_consultorio) REFERENCES consultorios(id_consultorio)
);
```

* Ahora, en `turnos` **solo queda lo que depende del evento turno**.
* Si quisieras demostrar 2FN con clave compuesta natural, podrías definir una **UNIQUE** sobre `(id_medico, fecha_turno, hora_turno)` para forzar unicidad de agenda, pero manteniendo `id_turno` como PK:

  ```sql
  ALTER TABLE turnos
  ADD CONSTRAINT uq_agenda UNIQUE (id_medico, fecha_turno, hora_turno);
  ```

### Paso 6 — Mantener los detalles 1 a N del turno (ya en 2FN)

Tus tablas detalle (todas con **PK compuesta** y **sin atributos no clave**) ya cumplen 2FN:

```sql
-- Teléfonos del paciente ya deberían migrar a pacientes/paciente_telefono (mejor aún para 3FN)
CREATE TABLE paciente_telefono (
  id_paciente INT NOT NULL,
  telefono VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_paciente, telefono),
  FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
);

-- Síntomas y Prácticas del turno
CREATE TABLE turno_sintoma (
  id_turno INT NOT NULL,
  sintoma VARCHAR(120) NOT NULL,
  PRIMARY KEY (id_turno, sintoma),
  FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
);

CREATE TABLE practicas (
  id_practica INT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE turno_practica (
  id_turno INT NOT NULL,
  id_practica INT NOT NULL,
  PRIMARY KEY (id_turno, id_practica),
  FOREIGN KEY (id_turno) REFERENCES turnos(id_turno),
  FOREIGN KEY (id_practica) REFERENCES practicas(id_practica)
);
```

> Observá que en tablas de detalle como `turno_practica(id_turno, id_practica)` **no hay otros atributos no clave** → **no existen dependencias parciales** → 2FN ok.

## ✅ Resumen

* **Antes (1FN)**: `turnos` guardaba `obra_social` y (lógicamente) las `especialidades` del médico estaban mezcladas con el turno.
  Si mirás la **clave natural compuesta** (p. ej. `(paciente, fecha_turno, hora_turno)`), `obra_social` depende **solo de paciente** → **dependencia parcial** → **viola 2FN**.

* **Después (2FN)**: separaste **pacientes**, **médicos**, **obras_sociales**, **especialidades**, **consultorios**.
  `turnos` referencia esas entidades por **FK** y conserva solo atributos que **dependen del turno**.
  Las tablas detalle del turno no tienen columnas adicionales que dependan “parcialmente” de su PK compuesta → **2FN cumplida**.

---
¡Vamos con 3FN! Acá tenés **qué exige 3FN**, **por qué el esquema en 2FN todavía no está en 3FN** (en sentido práctico), y **los pasos concretos para llevarlo a 3FN** en el caso del hospital.

---

# 🚦 Recordatorio rápido: ¿Qué exige 3FN?

Una tabla está en **Tercera Forma Normal (3FN)** si:

1. Está en **2FN**, y
2. **No hay dependencias transitivas** de atributos no clave hacia la clave: es decir, **ningún atributo no clave depende de otro atributo no clave**.

> Eslogan didáctico: *“Cada atributo no clave debe depender **solo** de la clave, de toda la clave y de **nada más que la clave**.”*

## ❓ Por qué, conceptualmente, ni estructura 2FN “no es 3FN” (visión de transitividades)

Aun habiendo llevado el modelo a 2FN (separando entidades y quitando dependencias parciales), suelen quedar **atributos no clave** que **determinan** a otros dentro de la misma tabla o que **deberían vivir en catálogos**. Ejemplos típicos en el dominio:

* **Pacientes**

  * `paciente → obra_social` (ya separada en 2FN) pero además:
  * `obra_social → nombre_obra` → si guardás `nombre_obra` en `pacientes`, habría **transitiva**.
  * Si manejás **planes**: `obra_social, plan → copago, cobertura` → no deben estar duplicados en `turnos`.

* **Médicos**

  * `medico → matricula` (identificador único del médico). Si repetís `matricula` en otras tablas, generás transitivas/duplicación.

* **Consultorios**

  * `consultorio → piso, sector` → si `turnos` tuviera `piso`/`sector`, serían **transitivas** vía `consultorio`.

* **Prácticas**

  * `practica → nombre_practica, precio_base, tipo` → si en `turno_practica` guardás `precio_base`/`tipo`, generás **transitivas** con el ID de práctica.

* **Especialidades**

  * `especialidad → nombre_especialidad` → debe normalizarse como catálogo, no repetirse como texto libre una y otra vez.

**Conclusión**: Para 3FN, debés **migrar atributos derivados/categóricos** a sus **tablas de referencia** y mantener en las relaciones **solo claves** (FK) y **atributos propios** del hecho (ej: del turno).

## 🧭 3FN: Esquema propuesto

> Partimos del diseño en 2FN que ya tenés: `turnos`, `pacientes`, `medicos`, `consultorios`, `obras_sociales`, `especialidades`, `medico_especialidad`, `practicas`, `turno_practica`, `turno_sintoma`, `paciente_telefono`, etc.

### Paso 1 — Asegurar **catálogos** y **claves sustitutas** únicas

Crear/confirmar catálogos con **claves técnicas** y **restricciones UNIQUE** para sus nombres:

```sql
-- Obras sociales y planes
CREATE TABLE obras_sociales (
  id_obra INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE planes_os (
  id_plan INT PRIMARY KEY,
  id_obra INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  UNIQUE (id_obra, nombre),
  FOREIGN KEY (id_obra) REFERENCES obras_sociales(id_obra)
);

-- Prácticas y especialidades
CREATE TABLE practicas (
  id_practica INT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL UNIQUE,
  tipo VARCHAR(50) NULL
);

CREATE TABLE especialidades (
  id_especialidad INT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL UNIQUE
);
```

> **Por qué**: Evitás transitivas tipo `id_practica → nombre_practica` repetido en varias tablas. El **nombre** vive en el catálogo.

### Paso 2 — Ubicar **atributos dependientes** del catálogo en su tabla (no en las relaciones)

Ejemplos:

* Si hay **precio base** o **código NBU** de una práctica, colócalos en `practicas` o en una tabla de **tarifario** (ver paso 3).
* Si hay **piso/sector** del consultorio, guárdalos en `consultorios`, no en `turnos`.

```sql
CREATE TABLE consultorios (
  id_consultorio INT PRIMARY KEY,
  codigo VARCHAR(20) NOT NULL UNIQUE,
  piso INT NULL,
  sector VARCHAR(50) NULL
);
```

### Paso 3 — Atributos que varían por **obra social/plan** (evitar transitivas)

Si el **precio** de una práctica depende del **plan** de obra social, no lo pongas en `turno_practica`. Creá un **tarifario**:

```sql
CREATE TABLE aranceles_plan (
  id_plan INT NOT NULL,
  id_practica INT NOT NULL,
  precio DECIMAL(12,2) NOT NULL,
  PRIMARY KEY (id_plan, id_practica),
  FOREIGN KEY (id_plan) REFERENCES planes_os(id_plan),
  FOREIGN KEY (id_practica) REFERENCES practicas(id_practica)
);
```

> **Por qué**: Si almacenás `precio` en `turno_practica`, tendrías `id_practica → precio` (o `id_plan, id_practica → precio`) replicado por turno → **transitiva** respecto del turno. En 3FN, `turno_practica` solo referencia IDs; el precio se consulta con JOIN (o, si querés “congelarlo” como histórico, ver *nota histórica* al final).

### Paso 4 — Consolidar **médicos** y **matrículas**

Asegurate de no repetir la matrícula por fuera de `medicos`. Si querés validar unicidad:

```sql
ALTER TABLE medicos ADD matricula VARCHAR(30) NOT NULL UNIQUE;
```

> **Por qué**: Evita transitivas del estilo `id_medico → matricula` repetida en otras tablas.

### Paso 5 — Ligar **pacientes** con **planes** (si aplica)

Si cada paciente tiene un plan (o varios con vigencia), modelalo como relación:

```sql
CREATE TABLE paciente_plan (
  id_paciente INT NOT NULL,
  id_plan INT NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NULL,
  PRIMARY KEY (id_paciente, id_plan, fecha_inicio),
  FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
  FOREIGN KEY (id_plan) REFERENCES planes_os(id_plan)
);
```

> Así, en `turnos` **no** guardás `obra_social`/`plan` ni `copago` directo. Consultás vía joins (o registrás solo el **id_plan vigente** al momento del turno para facturación, ver nota histórica).

### Paso 6 — Revisar **turnos** y **tablas puente** para que no tengan transitivas

* `turnos(id_turno, id_paciente, id_medico, fecha, hora, id_consultorio, …)` → **solo** datos propios del turno.
* `turno_practica(id_turno, id_practica)` → **sin** nombre_practica, **sin** precio.
* `turno_sintoma(id_turno, id_sintoma)` si catalogás síntomas; si dejás texto libre, sigue siendo 3FN mientras **no dependa** de otro no-clave.

Ejemplo final (núcleo en 3FN):

```sql
-- Cabecera del turno (sin transitivas)
CREATE TABLE turnos (
  id_turno INT PRIMARY KEY,
  id_paciente INT NOT NULL,
  id_medico INT NOT NULL,
  fecha_turno DATE NOT NULL,
  hora_turno TIME NOT NULL,
  id_consultorio INT NULL,
  FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
  FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
  FOREIGN KEY (id_consultorio) REFERENCES consultorios(id_consultorio),
  UNIQUE (id_medico, fecha_turno, hora_turno) -- opcional de agenda
);

-- Síntomas (catalogados) y puente
CREATE TABLE sintomas (
  id_sintoma INT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE turno_sintoma (
  id_turno INT NOT NULL,
  id_sintoma INT NOT NULL,
  PRIMARY KEY (id_turno, id_sintoma),
  FOREIGN KEY (id_turno) REFERENCES turnos(id_turno),
  FOREIGN KEY (id_sintoma) REFERENCES sintomas(id_sintoma)
);

-- Prácticas (catálogo + puente) + arancel por plan
-- (ver Paso 3: aranceles_plan)
CREATE TABLE turno_practica (
  id_turno INT NOT NULL,
  id_practica INT NOT NULL,
  PRIMARY KEY (id_turno, id_practica),
  FOREIGN KEY (id_turno) REFERENCES turnos(id_turno),
  FOREIGN KEY (id_practica) REFERENCES practicas(id_practica)
);
```

### ✅ Resumen: “por qué no era 3FN” y cómo queda

* **Antes (2FN)**: Ya no había **parciales**, pero podían existir **transitivas**:

  * Repetir `nombre_obra`, `nombre_practica`, `piso/sector` en tablas no catálogo.
  * Guardar `precio` de práctica en `turno_practica` (cuando depende de `plan + práctica`).
* **Después (3FN)**:

  * Los **atributos descriptivos** se mueven a sus **catálogos** (obras, planes, prácticas, especialidades, consultorios, síntomas).
  * Las **relaciones** guardan **FKs** y **atributos propios** del hecho (el turno, su fecha/hora/consultorio, el vínculo con práctica/síntoma).
  * Cero atributos no clave **determinando** otros dentro de la misma tabla → **sin transitivas**.


### 🛠️ Consejos de migración (desde tu 2FN)

1. Crear catálogos (`practicas`, `especialidades`, `sintomas`, `consultorios`, `planes_os`) con **UNIQUE** sobre `nombre`/`codigo`.
2. Llenarlos con `INSERT … SELECT DISTINCT`.
3. Reemplazar columnas de texto en relaciones por **FKs** (IDs).
4. Mover `precio`/`copago` a `aranceles_plan` (o tabla histórica).
5. Quitar de `turnos` cualquier campo “derivable” del consultorio, paciente, médico o práctica.

**Validaciones rápidas**:

```sql
-- ¿Alguna tabla (no catálogo) tiene atributos repetidos que dependan de otro no-clave?
-- Chequear dependencia práctica→nombre en turno_practica: NO debe existir nombre_practica allí.
-- Chequear dependencia consultorio→piso/sector en turnos: NO deben existir en turnos.

-- Joins de comprobación
SELECT t.id_turno, p.nombre AS paciente, m.nombre AS medico, c.codigo AS cons
FROM turnos t
JOIN pacientes p ON p.id_paciente = t.id_paciente
JOIN medicos m ON m.id_medico = t.id_medico
LEFT JOIN consultorios c ON c.id_consultorio = t.id_consultorio
LIMIT 5;
```

### 🧾 Nota sobre “histórico” de valores (práctico vs. 3FN)

* Si necesitás **congelar el precio** usado *en ese turno* (auditoría/facturación), podés agregar en `turno_practica` un campo `precio_facturado`.

  * **Esto no viola 3FN** si interpretás que `precio_facturado` **depende del hecho “turno-práctica”**, no de la práctica/plan “abstracta”.
  * Aun así, mantené el **precio de referencia vigente** en `aranceles_plan` para consultas normales.
