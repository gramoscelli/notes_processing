# Planificación control de caja
## 1) Alcance por fases (con cuotas integradas)

**Fase 1 – Paridad con Excel (MVP)**

* Movimientos de caja **manuales**: ingresos/egresos (donaciones, eventos, librería, compras).
* Cierres diarios/mensuales, arqueos, reportes equivalentes a los Excel.
* Importar histórico desde planillas (mapeo automático).
* Usuarios/roles + bitácora.
* **Sincronización de cuotas**: traer *cobrados* de `cobrocuotas` como **ingresos** con referencia (`CC_ID`), reversas automáticas si aparecen en `cuotas_anuladas`.

**Fase 2 – Recaudación y conciliaciones**

* Conciliación MP/Banco y rendiciones por cobrador (`Re_ID`).
* Exportes a PDF/Excel estilados (igual que tus reportes actuales).
* Portal de lectura para auditoría.

**Fase 3 – Avanzado**

* Centros de costo, presupuestos y ejecución.
* API pública y dashboards.

## 2) Modelo de datos (Caja) — unificado

> Mantiene **todo lo que ya te propuse** + encastre “Cuotas”.

**Catálogos**

* `categorias` (tipo ingreso/egreso, jerarquía opcional)
* `medios_pago` (efectivo, transferencia, MP, cheque, etc.)
* `proveedores` (para egresos)
* `usuarios`

**Operativo caja**

* `caja_aperturas`(…)
* `caja_movimientos`(id, fecha, **tipo** ingreso/egreso, categoria_id, medio_pago_id, monto, descripcion, **origen**: 'manual' | 'cuota', **origen_id**: `CC_ID` si viene de socios, socio_id?, cobrador_id?, re_id?, adjunto_url?, created_by…)
* `caja_cierres`(…)
* `recibos`(movimiento_id, numero, pdf_url)
* `conciliaciones`(banco/mp; diferencias)

**Integración socios (solo lo necesario para mostrar/filtrar)**

* `socios_cache`(So_ID, nombre, doc, …) *(opcional si no hay API en línea)*
* índices por (`origen`, `origen_id`) para idempotencia.

## 3) Flujos clave

### 3.1 Movimientos **manuales** (todo lo no-cuotas)

1. **Apertura de caja**
2. Registrar **Ingresos** (donaciones, ventas de feria, eventos) y **Egresos** (compras, servicios, caja chica) con **medio de pago** y **categoría**.
3. Adjuntar foto de ticket/factura si aplica.
4. **Cierre/Arqueo** con diferencias, firma y PDF.

### 3.2 Cuotas de socios (sin duplicar lógica)

1. **Sincronizador R/O** a la DB de socios:

   * Lee `cobrocuotas` (solo filas con `CC_Cobrado='Y'` y `CC_FechaCobrado` ≠ NULL).
   * Crea/actualiza **movimientos de ingreso** en Caja (`origen='cuota'`, `origen_id=CC_ID`, `monto=CC_Valor`, `fecha=CC_FechaCobrado`, `cobrador_id=Co_ID`, `re_id=Re_ID`, `socio_id=So_ID`).
   * Si un `CC_ID` figura en `cuotas_anuladas` → genera **movimiento de reversa** (egreso correctivo, linkeado al original).
   * Idempotencia: **no** duplica el mismo `CC_ID`.
2. **Rendiciones por cobrador**

   * Vista por `Re_ID`: total, cantidad de cobros, estado de conciliación, PDF.
3. **Reportes** combinados

   * Libro diario/mensual que **integra** manuales + cuotas.
   * Recaudación por cobrador, por medio de pago, por categoría, por centro de costo.
   * Historial por socio (solo lectura desde Caja; los cambios viven en “Socios”).

## 4) UI / Experiencia

* **Caja de hoy**: tabla única con *todas* las entradas; chips “Manual” / “Cuota” con link a detalles. Totales por medio de pago y categoría. Botón “Cerrar caja”.
* **Alta rápida** de movimientos manuales (atajos por categoría frecuente).
* **Rendiciones**: agrupadas por `Re_ID`/cobrador para control operativo.
* **Conciliación**: importar extractos MP/Banco y macheo guiado.
* **Buscador** por texto, socio, cobrador, `CC_ID`, período, categoría, medio.

## 5) Integración técnica con “Socios”

* **Modo recomendado** inicial: conexión **read-only** a la base actual.
* Filtros incrementales por **último `CC_ID`** o por **`CC_FechaCobrado`**.
* **Reversas**: consultar `cuotas_anuladas` / `cobrocuotas_bajas` y generar egreso espejo.
* **Rendiciones**: usar `Re_ID` de `cobrocuotas`/`rendiciones` para agrupar.
* **Encoding**: si la DB de socios no está en UTF-8, convertir en la consulta o al almacenar en `socios_cache`.

## 6) Reportes (reemplazan Excel 1:1, pero mejor)

* **Libro de caja** (diario/mensual), con subtotales por medio y categoría.
* **Cuotas**: cobradas vs. anuladas (neto), por cobrador y por `Re_ID`.
* **Egresos** por proveedor y rubro.
* **Comparativo anual** y por centro de costo.
* **Auditoría**: quién modificó qué y cuándo, hash de cierres.

## 7) Stack (igual al propuesto, con sincronizador)

* **Frontend**: React + Vite + TS (shadcn/ui), React Query.
* **Backend**: Node (Nest/Express) + **Prisma**.
* **DB**: PostgreSQL.
* **Jobs**: cron/worker para sincronizar `cobrocuotas` → `caja_movimientos`.
* **Storage**: S3/MinIO para adjuntos.
* **Infra**: Docker Compose; backups automáticos.

## 8) Migración y validación

1. Importar histórico de **movimientos manuales** desde Excel.
2. Correr sincronizador de **cuotas** para un mes piloto.
3. Comparar reportes (Caja vs. Excel/Socios) y ajustar mapeos.
4. Operación paralela breve y luego switch-off de Excel.

## 9) Entregables inmediatos (puedo prepararlos ya)

* **DDL** de `caja_*` (PostgreSQL) con claves e índices, incluyendo (`origen`,`origen_id`).
* **Script de sincronización** (Node/TS):

  * lee `cobrocuotas`/`cuotas_anuladas` R/O,
  * upsertea en `caja_movimientos`,
  * registra bitácora e idempotencia.
* **Plantillas de reporte** (Libro de caja y Rendición por cobrador) en PDF/Excel.
* **Mapa de campos** Excel→Caja y Socios→Caja (cuotas).

