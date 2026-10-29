# Préstamos de herramientas (Ferretería)

## Objetivo didáctico

* Practicar **herencia**, **métodos abstractos**, **polimorfismo** y el patrón **Template Method**.
* Diseñar una jerarquía simple y **evitar condicionales por tipo** (`if/switch/instanceof`).

## Consigna (enunciado para estudiantes)

Una ferretería alquila herramientas y cobra en función del tipo y de los días de alquiler.

1. Diseñá la clase abstracta `Herramienta` con:

   * Propiedades mínimas: `nombre: string`.
   * **Template Method** `costoAlquiler(dias: number): number` (NO se sobrescribe en subclases).

     * Fórmula general: `costoBase() + recargoPorDia() * dias + depositoReembolsable()`
     * Si `dias <= 0`, lanzar `Error("dias debe ser mayor que 0")`.
   * **Hooks abstractos**:

     * `costoBase(): number`
     * `recargoPorDia(): number`
     * `depositoReembolsable(): number` (puede ser `0` en algunas herramientas).
   * Método concreto `descripcion(dias: number): string` que devuelva:

     * `"<nombre>: \$<costo> por <dias> día(s)"` usando `costoAlquiler(dias)`.

2. Implementá **tres subclases** con los siguientes valores:

   * `Taladro`: base **\$1.000**, recargo **\$300/día**, **depósito \$0**.
   * `Amoladora`: base **\$1.200**, recargo **\$250/día**, **depósito \$0**.
    * `Hidrolavadora`: base **\$1.500**, recargo **\$400/día**, **depósito \$2.000** (se cobra, pero luego se devuelve al regresar la máquina en buen estado; en este ejercicio **se factura completo** para simplificar el cálculo del costo **a pagar al retirar**).

3. Dado un arreglo `herramientas: Herramienta[]` y un número de días `dias`, implementá una función:

   * `reporteAlquiler(herramientas: Herramienta[], dias: number): string`
   * Debe devolver un **texto multilínea** con una línea por herramienta (usando `descripcion`) y al final una línea `TOTAL: \$<suma>`.

4. **Restricciones**:

   * No se permiten condicionales por tipo (`if/switch/instanceof`). El cálculo debe resolverse por **polimorfismo**.
   * `costoAlquiler` NO debe sobrescribirse en subclases (el **Template Method** vive en la clase base y llama a los hooks).

5. **Bono (opcional, +10%)**:

   * Agregá `Lijadora`: base **\$900**, recargo **\$220/día**, depósito **\$500**.
   * Incluila en el `reporteAlquiler` con el mismo formato.



## Criterios de aceptación

* **Herencia y polimorfismo** usados correctamente.
* `Herramienta` define **Template Method** `costoAlquiler` y **hooks abstractos**.
* Subclases implementan sus **valores** sin condicionales por tipo.
* `reporteAlquiler` genera líneas correctas y `TOTAL` correcto.
* Manejo de errores para `dias <= 0`.

## Qué evaluar (rápido)

* Diseño OO claro (nombres, responsabilidades).
* Que NO haya `if/switch/instanceof` para distinguir tipos.
* Código conciso y legible; tests en verde.


