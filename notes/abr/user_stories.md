> **Convención de numeración**
>
> * Mantengo tus IDs y agrego nuevas HU en bloques temáticos para que sea fácil priorizar:
>
>   * 001–009: Caja (diaria) — *tú ya tienes 001–003*
>   * 010–019: Pedidos/OC — *tú ya tienes 010–012*
>   * 020–029: Catálogos & Configuración
>   * 030–039: Importación & Migración desde Excel
>   * 040–049: Reportes
>   * 050–059: Auditoría & Seguridad
>   * 060–069: Conciliaciones (Banco/MP)
>   * 070–079: Rendiciones por cobrador
>   * 080–089: Recibos & Comprobantes
>   * 090–099: Adjuntos & Evidencias
>   * 100–109: Integración con sistema de Socios (Cuotas)

---

# ÉPICA 01: Caja (continuación de tus HU-001..003)  

**HU-004 — Editar/Anular movimiento con control**

* **Como** cajero **quiero** poder editar o anular un movimiento **para** corregir errores sin perder trazabilidad.
* **Criterios de aceptación**

  * Dado un movimiento del día abierto, cuando edito campos permitidos, entonces se registra en bitácora el *antes/después*.
  * Dado un cierre ya realizado, cuando intento editar, entonces el sistema lo bloquea o exige rol con autorización y genera *nota de ajuste*.
  * Dada una anulación, cuando confirmo, entonces el saldo se revierte con *movimiento inverso* y se marca “anulado”.

**HU-005 — Transferencia entre cajas/medios (traspasos)**

* **Como** tesorero **quiero** registrar traspasos (p.ej., efectivo → banco) **para** mantener saldos consistentes.
* **Criterios**

  * Dado un traspaso, cuando registro, entonces crea dos movimientos vinculados (egreso origen, ingreso destino) y no altera el neto global.

**HU-006 — Caja chica**

* **Como** responsable **quiero** administrar un fondo fijo de caja chica **para** egresos menores y reposiciones.
* **Criterios**

  * Dado un fondo inicial, cuando cargo egresos, entonces descuenta del fondo y permite *rendición* con reposición a tope.

**HU-007 — Cierres parciales y reapertura controlada**

* **Como** cajero **quiero** cierres parciales por turno **para** cortes operativos.
* **Criterios**

  * Dado un cierre parcial, cuando otro usuario continúa, entonces puede registrar nuevos movimientos sin mezclar saldos.
  * Dada una reapertura, cuando se autoriza por un rol superior, entonces crea *evento de auditoría*.

**HU-008 — Búsqueda y filtros en caja**

* **Como** cajero **quiero** buscar por texto, fecha, categoría, medio, monto, socio y comprobante **para** encontrar movimientos rápido.
* **Criterios**

  * Dado un filtro, cuando aplico, entonces la lista responde en <2s (90% de casos) y muestra totales filtrados (ingreso/egreso/neto).

**HU-009 — Categorización y centros de costo**

* **Como** tesorero **quiero** asignar categoría y centro de costo **para** análisis por actividad (talleres, eventos, proyectos).
* **Criterios**

  * Dado un movimiento con centro de costo, cuando genero reportes, entonces suma en ese centro y en la categoría.

---

# ÉPICA 02: Pedidos de Compra (ya creada por ti) — *extensiones opcionales*  

**HU-013 — Recepción parcial y remitos**

* **Como** solicitante **quiero** recepcionar parcial y adjuntar remito **para** registrar entregas diferidas.
* **Criterios**: recepción parcial actualiza estado; bloqueo de facturación total si hay ítems pendientes.

**HU-014 — Vincular OC → Egreso de caja**

* **Como** tesorero **quiero** convertir una OC aprobada en egreso **para** evitar doble carga.
* **Criterios**: la creación de egreso arrastra proveedor, ítems (resumen), centro de costo y adjuntos.

---

# ÉPICA 03: Catálogos & Configuración

**HU-020 — Gestión de categorías y subcategorías**

* **Como** admin **quiero** ABM de categorías (ingreso/egreso) **para** normalizar conceptos.
* **Criterios**: no se pueden borrar categorías usadas; se pueden inactivar.

**HU-021 — Gestión de medios de pago**

* **Como** admin **quiero** ABM de medios (efectivo, transferencia, MP, cheque, …) **para** reportes consistentes.
* **Criterios**: parametrizar alias, cuentas bancarias asociadas, “requiere comprobante” sí/no.

**HU-022 — Parámetros de caja**

* **Como** admin **quiero** configurar umbrales (alertas de faltante/sobrante, montos que requieren doble aprobación) **para** control interno.

---

# ÉPICA 04: Importación & Migración desde Excel

**HU-030 — Importar históricos desde planillas**

* **Como** tesorero **quiero** importar movimientos históricos **para** iniciar la app sin re-cargar manualmente.
* **Criterios**: mapeo de columnas; validación de fechas/montos; previsualización y *dry-run*; informe de filas rechazadas.

**HU-031 — Pegado rápido desde Excel (bulk)**

* **Como** cajero **quiero** pegar rangos tabulares **para** alta rápida masiva.
* **Criterios**: plantillas; verificación de duplicados por número de comprobante/fecha/monto.

---

# ÉPICA 05: Reportes

**HU-040 — Libro de caja diario/mensual**

* **Como** tesorero **quiero** generar libro de caja **para** auditorías y archivos.
* **Criterios**: totales por medio y categoría; exportar PDF/Excel; sello de cierre.

**HU-041 — Informe de recaudación por medio**

* **Como** comité **quiero** ver recaudación por efectivo/MP/transferencia **para** decidir políticas.
* **Criterios**: rango de fechas; comparación vs. período anterior.

**HU-042 — Informe por centros de costo**

* **Como** dirección **quiero** ver ingresos/egresos por actividad **para** evaluar sostenibilidad.
* **Criterios**: top N centros; variación mensual.

---

# ÉPICA 06: Auditoría & Seguridad

**HU-050 — Bitácora de operaciones**

* **Como** auditor **quiero** ver quién creó/editó/anuló **para** trazabilidad.
* **Criterios**: registra usuario, timestamp, IP, valores antes/después, motivo.

**HU-051 — Control de permisos por rol**

* **Como** admin **quiero** roles (Cajero, Tesorero, Auditor, Admin, Bibliotecario) **para** limitar acciones.
* **Criterios**: matriz de permisos; bloqueo de funciones sensibles (reapertura, anulación, configuración).

**HU-052 — Cierre con hash y certificación**

* **Como** auditor **quiero** que el cierre genere un hash y PDF firmado **para** evitar alteraciones posteriores.
* **Criterios**: cambio posterior exige *nota de ajuste* y queda en bitácora.

*(Tus HNF sobre rendimiento, seguridad, backups y observabilidad siguen vigentes.)* 

---

# ÉPICA 07: Conciliaciones (Banco / Mercado Pago)

**HU-060 — Conciliar extracto bancario**

* **Como** tesorero **quiero** importar CSV del banco **para** machear con movimientos y traspasos.
* **Criterios**: reglas por monto/fecha/descripción; diferencias a revisar; marca “conciliado”.

**HU-061 — Conciliar liquidaciones de MP**

* **Como** tesorero **quiero** importar liquidaciones de MP **para** reconocer comisiones y acreditaciones.
* **Criterios**: cargos de comisión como egresos automáticos; vincular a cobros identificados.

---

# ÉPICA 08: Rendiciones por cobrador (cuotas y otros)

**HU-070 — Listar rendiciones por cobrador**

* **Como** tesorero **quiero** ver rendiciones (`Re_ID`) con totales **para** controlar entregas.
* **Criterios**: filtros por fecha/cobrador/estado; exporte PDF/Excel.

**HU-071 — Cierre de rendición**

* **Como** tesorero **quiero** cerrar una rendición **para** consolidar cobros de ese cobrador.
* **Criterios**: bloqueo de edición; acta firmada; diferencias detalladas.

---

# ÉPICA 09: Recibos & Comprobantes

**HU-080 — Emisión de recibo numerado**

* **Como** cajero **quiero** emitir recibo con numeración y logo **para** entregar constancia.
* **Criterios**: numeración secuencial por serie; reimpresión con marca “Duplicado”.

**HU-081 — Búsqueda por número de comprobante**

* **Como** auditor **quiero** buscar por número **para** ubicar rápidamente un recibo.
* **Criterios**: exacto y por prefijo; muestra PDF asociado.

---

# ÉPICA 10: Adjuntos & Evidencias

**HU-090 — Adjuntar comprobantes**

* **Como** cajero **quiero** subir foto/PDF de ticket/factura **para** sostener cada movimiento.
* **Criterios**: tamaños/formatos permitidos; vista previa; retención definida en política.

**HU-091 — Enlazar documentos externos**

* **Como** tesorero **quiero** linkear drive/URL **para** ahorrar subida duplicada.
* **Criterios**: valida accesibilidad; guarda URL con título.

---

# ÉPICA 11: Integración con Sistema de Socios (Cuotas)

> Esta épica **no reemplaza** el sistema de socios; solo refleja cobros en la caja con trazabilidad. (Se apoya en tu estructura de tablas de socios; integración R/O.)

**HU-100 — Ingresar cuotas cobradas (sincronización)**

* **Como** caja **quiero** incorporar cobros de cuotas marcados como *cobrados* en el sistema de socios **para** reflejar ingresos reales.
* **Criterios**

  * Dado `CC_Cobrado='Y'` y `CC_FechaCobrado` definido, cuando sincronizo, entonces se crea/actualiza un **ingreso** con `origen='cuota'`, `origen_id=CC_ID`, `monto=CC_Valor`, `fecha=CC_FechaCobrado`, `socio_id=So_ID`, `cobrador_id=Co_ID`, `re_id=Re_ID`.
  * Dado un `CC_ID` ya importado, cuando vuelve a llegar, entonces **no** se duplica (idempotente).
  * Dado un error de lectura, cuando termina la corrida, entonces registra evento y permite reintentar por rango de IDs/fechas.

**HU-101 — Reversa por anulación de cuota**

* **Como** caja **quiero** generar un movimiento inverso **cuando** una cuota previamente importada figura anulada **para** cuadrar saldos.
* **Criterios**

  * Dado un `CC_ID` en `cuotas_anuladas`/bajas, cuando sincronizo, entonces se crea un **egreso** espejo enlazado al ingreso original y ambos quedan claramente relacionados.
  * Dado que una anulación llegó tarde, cuando se refleje, entonces impacta en el día corriente con nota explicativa y mantiene la fecha de cobro original como referencia.

**HU-102 — Vista de cobros por rendición**

* **Como** tesorero **quiero** ver cobros agrupados por `Re_ID` y cobrador **para** cerrar rendiciones.
* **Criterios**: totales por rendición; cantidad de cuotas; exporte a PDF con detalle.

**HU-103 — Búsqueda por `CC_ID` / socio**

* **Como** auditor **quiero** localizar un cobro por `CC_ID` o socio **para** trazabilidad entre sistemas.
* **Criterios**: link a ficha del socio (solo lectura) o a la rendición asociada.

**HU-104 — Mapeo de medios de pago (reglas)**

* **Como** tesorero **quiero** definir reglas para inferir medio de pago de cuotas (p.ej., cobrador calle=efectivo; online=MP) **para** reportes consistentes.
* **Criterios**: tabla de reglas editable; prevalece el dato explícito si el sistema de socios lo provee en el futuro.

**HU-105 — Panel de sincronización**

* **Como** admin **quiero** un panel con último `CC_ID` importado, estado, errores y botón “reprocesar” **para** control operativo.
* **Criterios**: logs descargables; filtros por fecha/ID; modo *dry-run*.

---

## Historias No Funcionales (complemento a las tuyas)  

**HNF-005 — Integridad e idempotencia**

* Las sincronizaciones deben ser idempotentes por (`origen`,`origen_id`) y transaccionales (o con compensación).

**HNF-006 — Trazabilidad de cierres**

* Los cierres generan hash y PDF firmado; cualquier ajuste posterior queda como *nota de ajuste* + evento en bitácora.

**HNF-007 — Retención de adjuntos**

* Política configurable (p.ej., 10 años); expirados quedan inaccesibles salvo rol autorizado que levanta una *excepción auditada*.

