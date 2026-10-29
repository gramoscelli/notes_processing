
# Recuperatorio del Primer Parcial


## **Ejercicio 1 – TypeScript (Con datos + Tipos)**

Regla general: Para cada ejercicio que requiera imprimir un resultado, usar:

```ts
console.log('ejercicioN:', resultado);
```



### **Datos base comunes**

```ts
type ID = string;

const empleados = [
  { id: 'e1', nombre: 'Mara',   sector: 'produccion' },
  { id: 'e2', nombre: 'Diego',  sector: 'logistica' },
  { id: 'e3', nombre: 'Paula',  sector: 'ventas' },
] as const;

const insumos = [
  { codigo: 'X1', nombre: 'Metal',   costo: 500,   categoria: 'materia prima', stock: 3 },
  { codigo: 'Y2', nombre: 'Pintura', costo: 800,   categoria: 'quimicos',       stock: 0 },
  { codigo: 'Z3', nombre: 'Plástico',costo: 1200,  categoria: 'materia prima', stock: 10 },
  { codigo: 'W4', nombre: 'Tornillos', costo: 150, categoria: 'accesorios',    stock: 50 },
] as const;

const consumos = [
  { empleadoId: 'e1', items: [{ codigo: 'X1', qty: 1 }, { codigo: 'W4', qty: 10 }] },
  { empleadoId: 'e2', items: [{ codigo: 'Z3', qty: 2 }] },
  { empleadoId: 'e1', items: [{ codigo: 'W4', qty: 5 }] },
  { empleadoId: 'e3', items: [{ codigo: 'X1', qty: 1 }, { codigo: 'Z3', qty: 1 }] },
] as const;

const movimientosCaja = [
  { tipo: 'ingreso', monto: 10000 },
  { tipo: 'egreso',  monto: 2000  },
  { tipo: 'egreso',  monto: 1500  },
  { tipo: 'ingreso', monto:  800  },
  { tipo: 'egreso',  monto: 1200  },
] as const;
```



### **1) Unificar y ordenar números (sin repetir)**

Dados:

```ts
const a = [12, 4, 9, 12, 1];
const b = [3, 9, 2, 10, 4];
const c = [6, 1, 8, 3, 12];
```

Generar un arreglo único con todos los valores combinados **sin duplicados** y ordenado **de menor a mayor**.



### **2) Diccionario de insumos con validación**

A partir de `insumos`, generar un diccionario:

```ts
{ [codigo]: insumo }
```

Reglas:

* No mutar el array original.
* Si aparece un **código duplicado**, lanzar un `Error`.
* Tipar correctamente el resultado.



### **3) Consumo total por insumo (join con validación)**

Generar un array:

```ts
{ codigo, nombreInsumo, totalConsumido }
```

donde `totalConsumido` es la suma total de unidades consumidas en todos los `consumos`.

Reglas:

* Incluir solo códigos que existan en `insumos`.
* Si algún consumo incluye códigos desconocidos, lanzar un `Error` con la lista **sin repetir**.
* No modificar los arrays originales.


## **Ejercicio 2 – Sistema de Gestión de Robots Industriales**

Explicación breve:

Un sistema controla **robots industriales** dentro de una línea de producción.
Cada robot realiza tareas y tiene un consumo energético. El sistema permite calcular métricas agregadas y extender comportamientos.

#### **Clases (roles):**

* **LineaProduccion**: administra un conjunto de robots.
* **LineaProduccionExtendida**: agrega cálculos avanzados.
* **Robot** (abstracta): base para todos los robots.
* Robots concretos: **RobotSoldador**, **RobotPintor**, etc.
* **IConsumoEnergetico** (interfaz):

  * `calcularConsumo(minutos: number): number`
  * `aplicarAhorro(consumo: number): number`



### **a) Nueva funcionalidad obligatoria**

La clase **RobotPintor** **NO** implementa actualmente `IConsumoEnergetico`.
Debe:

1. Implementar la interfaz.
2. Usar la siguiente fórmula:

```
consumo = 5 (base) + 0.4 * minutos
```

3. Para `aplicarAhorro(consumo)` aplicar un **10% de reducción**.



### **b) TDD mínimo obligatorio**

Crear tests *antes* de implementar.
#### **Cuidado**: Los test pasan porque *no están implementados*.

#### **Test de consumo básico**

* Crear un `RobotPintor`.
* Verificar:

```
calcularConsumo(10) → 5 + 0.4*10 = 9
calcularConsumo(25) → 5 + 0.4*25 = 15
calcularConsumo(0)  → 5
```

Usar `toBeCloseTo`.

#### **Test de ahorro energético**

* Para un consumo equivalente a 30 minutos:

```
consumo = 5 + 0.4*30 = 17
ahorro = 17 * 0.9 = 15.3
```

Comparar con `toBeCloseTo`.

## Recursos

* Usar el .zip adjunto con los fuentes en Typescript
* Alternativamente, se puede descargar los fuentes desde [este repositorio de GitHub](https://github.com/gramoscelli/Prog4-Rec1erParcial-2025.git)

