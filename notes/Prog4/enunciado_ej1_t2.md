# Primer Examen Parcial - Programación IV
## Turno 2
### Fecha: 15 de octubre de 2025
## Ejercicio 1: TypeScript (Con datos + Tipos)

> **Regla general (ejercicios con ejecución):** Para **cada** ejercicio que pida un resultado, imprime:
> `console.log('ejercicioN:', resultado)`
> (reemplazar `N` por el número de ejercicio).
>


```ts
/***********************
 *  Datos base comunes *
 ***********************/
type ID = string;

const personas = [
  { id: 'p1', nombre: 'Ana',   edad: 28 },
  { id: 'p2', nombre: 'Luis',  edad: 41 },
  { id: 'p3', nombre: 'Sofía', edad: 33 },
] as const;

const productos = [
  { sku: 'A1', nombre: 'Cuaderno',  precio: 1200,  categoria: 'libreria', stock: 10 },
  { sku: 'B2', nombre: 'Lápiz',     precio: 200,   categoria: 'libreria', stock: 0  },
  { sku: 'C3', nombre: 'Botella',   precio: 3500,  categoria: 'hogar',    stock: 5  },
  { sku: 'D4', nombre: 'Taza',      precio: 2200,  categoria: 'hogar',    stock: 12 },
] as const;

const movimientos = [
  { cuenta: 'caja',   tipo: 'ingreso',  monto: 1500 },
  { cuenta: 'banco',  tipo: 'egreso',   monto:  700 },
  { cuenta: 'caja',   tipo: 'ingreso',  monto:  900 },
  { cuenta: 'banco',  tipo: 'ingreso',  monto: 3200 },
  { cuenta: 'caja',   tipo: 'egreso',   monto:  300 },
] as const;

const pedidos = [
  { id: 'o1', items: [{ sku: 'A1', qty: 2 }, { sku: 'B2', qty: 5 }] },
  { id: 'o2', items: [{ sku: 'D4', qty: 1 }] },
  { id: 'o3', items: [{ sku: 'C3', qty: 3 }, { sku: 'A1', qty: 1 }] },
] as const;

const clientes = [
  { id: 'c1', nombre: 'Club Norte' },
  { id: 'c2', nombre: 'Asoc. Sur'  },
] as const;

const ventas = [
  { id: 'v1', clienteId: 'c1', items: [{ sku: 'A1', qty: 3 }, { sku: 'D4', qty: 2 }] },
  { id: 'v2', clienteId: 'c2', items: [{ sku: 'C3', qty: 1 }] },
  { id: 'v3', clienteId: 'c1', items: [{ sku: 'A1', qty: 1 }, { sku: 'B2', qty: 10 }] },
] as const;
```

### 1) Intersección simple

Dados estos arreglos

```ts

const a = [
  5, 12, 18, 27, 34, 42,
  1, 3, 7, 9, 15, 20, 21, 25, 30, 36, 38, 44, 50, 53
];

const b = [
  5, 12, 18, 27, 34, 42,
  2, 4, 6, 8, 11, 14, 19, 22, 28, 31, 37, 40, 45, 55
];

const c = [
  5, 12, 18, 27, 34, 42,
  0, 10, 13, 16, 17, 23, 24, 26, 29, 33, 35, 39, 41, 47
];

const d = [
  5, 12, 18, 27, 34, 42,
  7, 10, 11, 13, 16, 20, 24, 29, 33, 35, 37, 40, 45, 50
];

```

Devolver un arreglo con los números que aparecen en todos los arreglos (intersección), sin duplicados y ordenados de mayor a menor.


### 2) Catálogo visible con IVA y banda de precio

De `productos`, construir un array **solo con los que tienen `stock > 0`**, transformando a:

```ts
{ sku, nombre, precioConIVA, banda }
```

donde `precioConIVA = precio * 1.21` (redondear a 2 decimales) y

* `banda = 'bajo'` si precio < 1000
* `banda = 'medio'` si 1000 ≤ precio ≤ 3000
* `banda = 'alto'` si precio > 3000
  Ordenar ascendente por `precioConIVA`.

---

### 3) Frecuencia de aparición de SKU en pedidos (con validación)

A partir de `pedidos`, calcular **en cuántos pedidos aparece cada `sku`** (no sumar cantidades, solo contar pedidos distintos donde figure).
Retornar:

```ts
{ sku, pedidosQueLoContienen }
```

Incluir **solo** `sku` que existan en `productos`.
Si hay `sku` desconocidos en algún pedido, **lanzar un Error** listando los desconocidos **sin repetir**.

## Ejercicio 2 - Turno 2: Sistema de Movilidad Compartida
### Explicación breve del código

Este sistema modela una plataforma de movilidad compartida urbana. El sistema permite **gestionar vehículos** (bicicletas y scooters), **alquilarlos** y **calcular tarifas** de forma **tipada, pura y testeable**. La flota se compone de diferentes tipos de **vehículos** con sus propias características de tarificación.

* **Clases/archivos (rol):**

  * `FlotaMovilidad`: administra la colección básica de vehículos y operaciones de alquiler.
  * `FlotaMovilidadExtendida`: extiende la funcionalidad añadiendo cálculos de ingresos potenciales.
  * `Vehiculo` (abstracta) y concretos como `Bicicleta`, `Scooter`: encapsulan la lógica de cada vehículo.
  * `ITarifa` (interfaz): define el contrato para vehículos con sistema de tarificación.

### a) Implementar la nueva funcionalidad

La clase `Scooter` actualmente NO implementa la interfaz `ITarifa`. Tu tarea es:

1. Hacer que `Scooter` implemente la interfaz `ITarifa`
2. Implementar los métodos requeridos: `calcularTarifa` y `aplicarPromocion` (ver el archvo `Bicicleta.ts`). En el método `calcularTarifa` usar \$ 3 base + \$ 0.25/min.

### b) **TDD** mínimo obligatorio

Escribir PRIMERO los tests en `Scooter.test.ts` que verifiquen:

1. **Test de tarifa básica**: 
   - Crear un scooter y verificar que `calcularTarifa(20)` retorne `8` ($3 base + 20 * $0.25)
   - Verificar al menos 2 casos más con diferentes minutos

2. **Test de promoción**:
   - Verificar que `aplicarPromocion(20)` aplique 20% de descuento sobre la tarifa de 30 minutos
   - La tarifa de 30 minutos es $10.5, con 20% descuento debería ser $8.4
   - Usar `toBeCloseTo` para comparar:

> `toBeCloseTo`
> Type: (value: number, numDigits?: number) => Awaitable<void>
>
> Usar toBeCloseTo para comparar números de punto flotante. El argumento opcional `numDigits` limita el número de dígitos que se verifican después del punto decimal.
