# TypeScript (Con datos + Tipos)

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
### 1) Arreglo plano único

Dada la matriz:

```ts
const matriz = [[1, 2], [2, 3], [4, 1]];
```

Generar un arreglo plano con todos los números sin repetir.

### 2) Estadísticas de personas

Con `personas`, devolver:

```ts
{ promedioEdad, medianaEdad, mayoresDe30 }
```

* `promedioEdad`: número con 2 decimales.
* `medianaEdad`: si hay cantidad par, promediar las dos centrales (2 decimales).
* `mayoresDe30`: **array de nombres** de quienes tengan `edad > 30`, ordenados alfabéticamente.

---

### 3) Resumen de inventario por categoría

De `productos`, agrupar por `categoria` y devolver:

```ts
{ categoria, cantidadProductos, stockTotal, precioPromedio }
```

* `precioPromedio` con 2 decimales.
  Ordenar por `categoria` ascendente.

