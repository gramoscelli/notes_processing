# Ejemplo — Normalización: Primera Forma Normal
## **Sistema Hospitalario:** Turnos Médicos

## 📌 Presentación del problema

El hospital “San Benito” administra los turnos médicos en una base de datos única, donde se registran los pacientes, los médicos, y los detalles de cada turno otorgado.
Actualmente toda esta información se guarda en una sola tabla llamada `turnos`, incluyendo los teléfonos del paciente, las especialidades del médico, los síntomas informados y las prácticas solicitadas dentro de una misma columna.


## 🎯 Actividades

1. Analizar la tabla `turnos` provista.
2. Identificar:

   * La clave primaria actual.
   * Qué columnas contienen más de un valor.
3. Proponer una estructura de tablas que permita cumplir con la Primera Forma Normal (1FN).
4. Indicar claves primarias y foráneas que surgirían de la reorganización propuesta.
5. Insertar los datos de ejemplo nuevamente pero ya normalizados a 1FN.

## 🗂️ Ejemplo de la tabla actual (NO normalizada)

| id_turno | paciente     | telefonos_paciente        | obra_social | medico     | especialidades_medico | fecha_turno | hora_turno | consultorio | sintomas_reportados    | practicas_solicitadas |
| -------- | ------------ | ------------------------- | ----------- | ---------- | --------------------- | ----------- | ---------- | ----------- | ---------------------- | --------------------- |
| 1001     | Carla Suárez | 291-1234567 / 291-5559999 | IOMA        | Dr. López  | Cardiología, Clínica  | 2025-10-20  | 08:30      | C1          | dolor torácico, fatiga | ECG; Análisis sangre  |
| 1010     | Juan Rojas   | 291-3331111               | OSDE        | Dr. López  | Cardiología, Clínica  | 2025-10-26  | 08:15      | C2          | palpitaciones, disnea  | ECG; Holter 24h       |
| 1024     | Carla López  | 299-5554443               | IOMA        | Dra. Rivas | Ginecología           | 2025-10-30  | 08:15      | G3          | controles anuales      | PAP; Colposcopía      |

📌 Los campos **telefonos_paciente**, **especialidades_medico**, **sintomas_reportados** y **practicas_solicitadas** presentan más de un dato en la misma celda.
