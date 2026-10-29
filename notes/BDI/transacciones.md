# 🧩 Transacciones en MySQL

## ¿Qué es una transacción?**
Una transacción es un bloque de una o más sentencias SQL que se ejecutan como una unidad lógica única.
Todas las operaciones deben completarse correctamente para que los cambios se guarden en la base de datos.

**Propósito:** garantizar la **integridad de los datos** cuando ocurren errores o fallos durante una operación múltiple.



## ⚙️ Propiedades ACID

| Propiedad        | Descripción                                              |
| - | -- |
| **Atomicidad**   | Todas las operaciones se ejecutan o ninguna.             |
| **Consistencia** | La base de datos pasa de un estado válido a otro.        |
| **Aislamiento**  | Las transacciones concurrentes no interfieren entre sí.  |
| **Durabilidad**  | Los cambios confirmados persisten incluso tras un fallo. |



## 🧱 Sintaxis Básica

```sql
START TRANSACTION;

-- Sentencias SQL
INSERT INTO cuentas VALUES (1, 5000);
UPDATE cuentas SET saldo = saldo - 500 WHERE id = 1;

COMMIT;    -- Confirma los cambios
-- o
ROLLBACK;  -- Revierte todo si ocurre un error
```



## 🧩 Ejemplo Práctico – Transferencia Bancaria

```sql
START TRANSACTION;

UPDATE cuentas SET saldo = saldo - 1000 WHERE id = 1;
UPDATE cuentas SET saldo = saldo + 1000 WHERE id = 2;

COMMIT;
```

**Explicación:**
Ambas operaciones se ejecutan como una sola transacción.
Si alguna falla (por ejemplo, saldo insuficiente), se utiliza `ROLLBACK` para deshacer los cambios.



## 🔄 Control de Transacciones en MySQL

| Comando        | Función                                             |
|--|--|
| **START TRANSACTION** / **BEGIN** | Inicia una nueva transacción.                       |
| **COMMIT**                        | Confirma los cambios realizados.                    |
| **ROLLBACK**                      | Revierte los cambios no confirmados.                |
| **SAVEPOINT nombre**              | Crea un punto intermedio dentro de una transacción. |
| **ROLLBACK TO nombre**            | Revierte hasta el punto guardado.                   |
| **SET AUTOCOMMIT = 0**            | Desactiva el modo automático de confirmación.       |



## ✅ Buenas Prácticas

* Desactiva `AUTOCOMMIT` para tener control manual.
* Coloca las transacciones en bloques `TRY/CATCH` en lenguajes de programación.
* Usa transacciones para operaciones que modifiquen múltiples tablas o filas relacionadas.
* Evita transacciones muy largas para no bloquear otros usuarios.

