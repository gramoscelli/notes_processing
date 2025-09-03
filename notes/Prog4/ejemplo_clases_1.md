## Estructura del proyecto

* Archivos dentro de `src/`:

  * `figure.ts`, `circle.ts`, `rectangle.ts`, `triangulo.ts`, `arreglo.ts`, `main.ts`
* Configuración mínima sugerida:

  ```bash
  npm init -y
  npm i -D typescript ts-node @types/node
  npx tsc --init --rootDir src --outDir dist --target ES2020 --module commonjs --strict true
  ```
* Ejecución:

  * Desarrollo: `npx ts-node src/arreglo.ts` y `npx ts-node src/main.ts`
  * Compilado: `npx tsc` y luego `node dist/arreglo.js`, `node dist/main.js`

---

## Parte A — Jerarquía de figuras (clases y polimorfismo)

1. Cree una **clase abstracta** `Figure` en `figure.ts` con:

   * Campos privados `x: number`, `y: number`.
   * Dos constructores: por defecto (0, 0) y otro que reciba `(x: number, y: number)`.
   * Accesores (`get x()`, `set x(v: number)`, `get y()`, `set y(v: number)`).
   * **Métodos abstractos** (sin implementación) que retornen `void`:

     * `dibujar()`, `borrar()`, `mover()`, `eliminar()`.

   *Sugerencia de firma mínima:*

   ```ts
   export abstract class Figure {
     constructor(private _x = 0, private _y = 0) {}
     get x() { return this._x; } set x(v: number) { this._x = v; }
     get y() { return this._y; } set y(v: number) { this._y = v; }
     abstract dibujar(): void;
     abstract borrar(): void;
     abstract mover(): void;
     abstract eliminar(): void;
   }
   ```

2. Cree las subclases en archivos separados:

   * `circle.ts` → clase `Circle extends Figure`
   * `rectangle.ts` → clase `Rectangle extends Figure`
   * `triangulo.ts` → clase `Triangulo extends Figure`

   Cada subclase debe **sobrescribir** (con `override`) los métodos abstractos para que **impriman exactamente**:

   * `Circle`:
     `Dibujar Circle`, `Borrar Circle`, `Mover Circle`, `Eliminar Circle`
   * `Rectangle` (al menos `dibujar` y `borrar`):
     `Dibujar Rectangle`, `Borrar Rectangle`
   * `Triangulo`:
     `Dibujar Triangulo`, `Borrar Triangulo`, `Mover Triangulo`, `Eliminar Triangulo`

   *Ejemplo de una implementación (sólo ilustrativo):*

   ```ts
   import { Figure } from "./figure";
   export class Circle extends Figure {
     override dibujar() { console.log("Dibujar Circle"); }
     override borrar() { console.log("Borrar Circle"); }
     override mover() { console.log("Mover Circle"); }
     override eliminar() { console.log("Eliminar Circle"); }
   }
   ```

3. En `arreglo.ts`:

   * Importe las clases y cree `const figuras: Figure[] = []`.
   * Agregue un `Circle`, un `Rectangle` y un `Triangulo`.
   * Recorra `figuras` e invoque `dibujar()` (debe verse el **polimorfismo**).

**Salida esperada mínima (orden no estricto):**

```
Dibujar Circle
Dibujar Rectangle
Dibujar Triangulo
```

---

## Parte B — Arreglos y operaciones con cadenas

En el **mismo `arreglo.ts`**, después de la Parte A:

1. **Arreglos numéricos y de cadenas**

   * Declare `const arreglo: number[] = new Array(5);` (no asigne valores).
   * Declare `const finDeSemana: string[] = ["Sabado", "Domingo"];`
   * Recorra e imprima ambos arreglos (use `.length`).

2. **Lista de nombres** (use un arreglo `string[]`)

   * `const nombres: string[] = [];`
   * Agregue en este orden: `"Juan"`, `"Pedro"`, `"María"`, `"Carla"`.
   * Inserte `"Juana"` en la **posición 1** con `splice(1, 0, "Juana")`.
   * Agregue nuevamente `"Juan"` al final.
   * Imprima todos los nombres (uno por línea).
   * Muestre la **posición del primer `"Juan"`** usando `indexOf("Juan")`.
   * Indique si **existe `"Carla"`** usando `includes("Carla")` y muestre:

     * `"Carla está en la lista"` o `"Carla no está en la lista"`.
   * Elimine **una ocurrencia** de `"Juan"`:

     ```ts
     const idx = nombres.indexOf("Juan");
     if (idx !== -1) nombres.splice(idx, 1);
     ```
   * Invierta el orden con `nombres.reverse()` e imprima nuevamente.

---

## Parte C — Referencias, tipos y aserciones

Cree `main.ts` para demostrar:

1. **Asignación por referencia**

   * Declare dos referencias de tipo `Figure` apuntando a objetos distintos:

     ```ts
     import { Figure } from "./figure";
     import { Circle } from "./circle";
     import { Rectangle } from "./rectangle";

     let f: Figure = new Rectangle(0, 0);
     let g: Figure = new Circle(1, 1);
     f = g; // ahora f y g referencian el mismo objeto Circle
     f.dibujar(); // Debe imprimir "Dibujar Circle"
     ```
   * Comente que en JS/TS las **variables contienen referencias** a objetos.

2. **Conversión de valores (runtime) vs. type assertions (compile-time)**

   * Muestre que para “convertir” un `number` a entero se usa una función, no un casteo de tipos:

     ```ts
     const v: number = 5.3;
     let h: number = 7;
     h = Math.trunc(v);   // conversión real en tiempo de ejecución
     ```
   * Ejemplo de **type assertion** (no convierte, sólo guía al checker):

     ```ts
     const algo: unknown = 123;
     const n = algo as number; // assertion: afirma que es number
     ```
   * Contraste breve `any` vs `unknown`:

     * `any`: desactiva chequeo de tipos (peligroso si se abusa).
     * `unknown`: obliga a **narrowing** (más seguro).

3. **`object`, `Object` y `toString()`**

   * Demuestre que puede asignar una instancia a `object`/`unknown`, y llamar métodos solo tras refinar el tipo:

     ```ts
     let o: object | unknown = f;
     if (o instanceof Object) {
       // Aquí se puede hacer más, o convertir con 'as'
       (o as Figure).dibujar();
     }
     ```

---

## Requisitos de entrega

* **Separación en módulos** (un archivo por clase) y uso de `export`/`import`.
* Archivos TypeScript:

  * `figure.ts`, `circle.ts`, `rectangle.ts`, `triangulo.ts`, `arreglo.ts`, `main.ts`
* Debe ejecutarse sin errores con:

  * `npx ts-node src/arreglo.ts` y `npx ts-node src/main.ts`
  * (o bien compilado a `dist` con `npx tsc` y luego `node`)

---

## Criterios de evaluación

* Clase base **abstracta** y subclases con métodos `override` correctos.
* **Polimorfismo** observable al iterar `Figure[]` e invocar `dibujar()`.
* Operaciones con arreglos (`push`, `splice`, `indexOf`, `includes`, `reverse`) y recorrido correctos.
* Demostración clara de **referencias**, **type assertions**, y diferencia entre **conversión de valores** (p. ej., `Math.trunc`) y **assertions** (no convierten).
* Mensajes por consola **exactos** para las operaciones de cada figura.

---

## Nota rápida (buenas prácticas TS)

* Use `strict: true` en `tsconfig.json`.
* Prefiera `unknown` sobre `any` cuando no conozca el tipo por adelantado.
* Use `override` en métodos sobrescritos para que el compilador verifique la firma.
