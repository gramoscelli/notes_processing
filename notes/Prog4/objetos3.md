# Programación Orientada por Objetos - Tercera parte
## Teoría
### El Calificador `static`

Hasta ahora, todas las propiedades y métodos que hemos visto pertenecen a una **instancia** de una clase. Esto significa que para poder usarlos, primero debemos crear un objeto con `new`.

Sin embargo, a veces necesitamos propiedades o métodos que pertenezcan a la **clase en sí misma**, no a un objeto individual. Para esto, usamos el calificador `static`.

- **Propiedades Estáticas**: Son variables que son compartidas por **todas las instancias** de una clase. Piensa en ellas como una propiedad "global" para esa clase. Son ideales para contadores, constantes o configuraciones que deben ser las mismas para todos los objetos.

- **Métodos Estáticos**: Son funciones que se pueden llamar directamente desde la clase, sin necesidad de crear un objeto. Son perfectos para crear funciones de utilidad o "métodos de fábrica" (factory methods) que construyen objetos de una manera específica.

**Punto Clave**: Dentro de un método estático, **no se puede usar `this`** para referirse a una instancia, porque el método no opera sobre un objeto específico, sino sobre la clase.

#### Ejemplo Práctico: Contador de Objetos Creados

Este es el ejemplo clásico para `static`. Queremos llevar la cuenta de cuántos objetos de una clase específica han sido creados en total a lo largo de nuestro programa. Una propiedad de instancia no serviría, ya que cada objeto tendría su propio contador. Necesitamos un contador centralizado en la clase.

```ts
// archivo: Coche.ts
export class Coche {
  // 1. Propiedad Estática: El contador
  // `private` para que solo pueda ser modificado desde dentro de la clase.
  // Es compartido por TODOS los objetos `Coche`.
  private static contadorDeCoches: number = 0;

  // Propiedades de instancia
  public marca: string;
  public modelo: string;

  constructor(marca: string, modelo: string) {
    this.marca = marca;
    this.modelo = modelo;

    // Cada vez que el constructor es llamado, incrementamos
    // el contador ESTÁTICO de la clase.
    Coche.contadorDeCoches++;
    console.log(`Creando ${this.marca} ${this.modelo}...`);
  }

  // 2. Método Estático: Para acceder al contador
  // Un método `public static` nos permite consultar el valor
  // del contador desde fuera de la clase.
  public static obtenerCantidadDeCochesCreados(): number {
    return Coche.contadorDeCoches;
  }

  public toString(): string {
    return `${this.marca} ${this.modelo}`;
  }
}
```

```ts
// archivo: main.ts
import { Coche } from "./Coche";

console.log("=== CONTADOR DE INSTANCIAS CON STATIC ===");

// Podemos llamar al método estático ANTES de crear cualquier objeto.
let cantidadInicial = Coche.obtenerCantidadDeCochesCreados();
console.log(`Cantidad de coches creados al inicio: ${cantidadInicial}`); // 0

console.log("\nFabricando coches...");
const coche1 = new Coche("Toyota", "Corolla");
const coche2 = new Coche("Ford", "Mustang");
const coche3 = new Coche("Honda", "Civic");

// Después de crear las instancias, el contador estático ha sido actualizado.
let cantidadActual = Coche.obtenerCantidadDeCochesCreados();
console.log(`\nCantidad de coches creados ahora: ${cantidadActual}`); // 3

console.log("\nFabricando otro coche...");
const coche4 = new Coche("Tesla", "Model 3");

let cantidadFinal = Coche.obtenerCantidadDeCochesCreados();
console.log(`\nCantidad final de coches creados: ${cantidadFinal}`); // 4
```

### Igualdad entre Objetos

Una de las preguntas más importantes al trabajar con objetos es: ¿cuándo son dos objetos "iguales"? La respuesta depende de si hablamos de igualdad por **referencia** o por **valor**.

- **Igualdad por Referencia (Identidad)**: Es lo que JavaScript/TypeScript comprueba por defecto con el operador `===`. Dos variables de objeto son iguales por referencia solo si **apuntan exactamente al mismo objeto en la memoria**. Es como tener dos llaves que abren la misma y única puerta.

- **Igualdad por Valor (Equivalencia)**: Ocurre cuando dos objetos, aunque sean instancias diferentes en la memoria, tienen los **mismos valores en sus propiedades**. Es como tener dos llaves que abren dos puertas diferentes de dos casas que son idénticas por dentro. Por defecto, TypeScript no comprueba esto; debemos escribir nuestra propia lógica para hacerlo.

#### Ejemplo Práctico: Comparando Puntos

```ts
// archivo: Punto.ts
export class Punto {
  private x: number;
  private y: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }

  // Método para comprobar la igualdad por VALOR
  public esIgualA(otroPunto: Punto): boolean {
    return this.x === otroPunto.x && this.y === otroPunto.y;
  }

  public toString(): string {
    return `Punto(x: ${this.x}, y: ${this.y})`;
  }
}
```

```ts
// archivo: main.ts
import { Punto } from "./Punto";

console.log("\n=== IGUALDAD DE OBJETOS ===");

const p1 = new Punto(10, 20);
const p2 = new Punto(10, 20); // Mismos valores, pero objeto diferente
const p3 = p1;                 // Misma referencia, mismo objeto

console.log(`p1: ${p1}`);
console.log(`p2: ${p2}`);
console.log(`p3: ${p3}`);

console.log("\n--- Comprobando igualdad por Referencia (===) ---");
console.log(`¿p1 === p2? ${p1 === p2}`); // false -> Son dos objetos distintos en memoria.
console.log(`¿p1 === p3? ${p1 === p3}`); // true  -> Apuntan al mismo objeto en memoria.

console.log("\n--- Comprobando igualdad por Valor (lógica propia) ---");
console.log(`¿p1 es igual en valor a p2? ${p1.esIgualA(p2)}`); // true -> Sus propiedades internas son iguales.
```

### Copia Superficial vs. Copia Profunda

Relacionado con la igualdad, está el concepto de **copiar objetos**. Si simplemente asignamos un objeto a otra variable (`p3 = p1`), no estamos creando una copia, solo otra referencia al mismo objeto. Para crear un duplicado real, tenemos dos opciones:

- **Copia Superficial (Shallow Copy)**: Se crea un nuevo objeto, y las propiedades de nivel superior del objeto original se copian en él. **Problema**: Si alguna de esas propiedades es a su vez un objeto o un array, lo que se copia es la **referencia** a ese objeto/array anidado, no una copia del mismo.

- **Copia Profunda (Deep Copy)**: Se crea un nuevo objeto, y se recorren **recursivamente** todas sus propiedades. Si se encuentra un objeto o array anidado, se crea también una copia profunda de él. Esto garantiza que el objeto copiado sea completamente independiente del original.

#### Ejemplo Práctico: Copiando un Pedido

```ts
// archivo: Cliente.ts
export class Cliente {
  public nombre: string;
  constructor(nombre: string) { this.nombre = nombre; }
}

// archivo: Pedido.ts
import { Cliente } from "./Cliente";

export class Pedido {
  public id: number;
  public cliente: Cliente; // Propiedad anidada (un objeto)

  constructor(id: number, cliente: Cliente) {
    this.id = id;
    this.cliente = cliente;
  }

  public toString(): string {
    return `Pedido ID: ${this.id}, Cliente: ${this.cliente.nombre}`;
  }
}
```

```ts
// archivo: main.ts
import { Cliente } from "./Cliente";
import { Pedido } from "./Pedido";

console.log("\n=== COPIA SUPERFICIAL VS. PROFUNDA ===");

const clienteOriginal = new Cliente("Ana");
const pedidoOriginal = new Pedido(101, clienteOriginal);

console.log("Estado Original:");
console.log(pedidoOriginal.toString());

// --- 1. Copia Superficial (Shallow Copy) ---
// Usamos el operador de propagación (...) para una copia superficial.
const copiaSuperficial = { ...pedidoOriginal };

console.log("\nRealizando cambios en la Copia Superficial...");
// Cambiamos el nombre del cliente a través de la copia.
copiaSuperficial.cliente.nombre = "Beatriz";

console.log(`Copia Superficial: ${copiaSuperficial.id}, Cliente: ${copiaSuperficial.cliente.nombre}`);
console.log(`Pedido Original: ${pedidoOriginal.toString()}`); // ¡¡¡El original también cambió!!!
// Esto sucede porque ambos objetos (original y copia) comparten la MISMA referencia al objeto Cliente.

// --- 2. Copia Profunda (Deep Copy) ---
// Reseteamos el nombre para una demostración limpia.
clienteOriginal.nombre = "Ana";

// Usamos el "truco de JSON" para una copia profunda simple.
// NOTA: Este método tiene limitaciones (pierde funciones, fechas se convierten en strings, etc.).
// Para casos complejos, se recomienda usar una librería como Lodash.
const copiaProfunda = JSON.parse(JSON.stringify(pedidoOriginal));

console.log("\nRealizando cambios en la Copia Profunda...");
// Cambiamos el nombre del cliente a través de la copia profunda.
copiaProfunda.cliente.nombre = "Carla";

console.log(`Copia Profunda: Pedido ID: ${copiaProfunda.id}, Cliente: ${copiaProfunda.cliente.nombre}`);
console.log(`Pedido Original: ${pedidoOriginal.toString()}`); // ¡El original NO cambió!
// Esto funciona porque la copia profunda creó un objeto Pedido nuevo Y un objeto Cliente nuevo.
```

## Ejercicios Prácticos para la Clase

A continuación, se presentan una serie de ejercicios diseñados para aplicar los conceptos de miembros estáticos, igualdad de objetos y técnicas de copiado.

---

### Ejercicio 1: Miembros Estáticos - El Configurador Global

**Objetivo:** Practicar el uso de propiedades `static` para mantener un estado compartido y métodos `static` como funciones de utilidad.

**Consigna:**
Vamos a crear una clase `Configurador` que gestione la configuración global de una aplicación. Esta configuración (por ejemplo, el modo de ejecución) debe ser la misma en todo el programa, sin importar cuántas partes del código interactúen con ella.

1.  **Crea la clase `Configurador`** en un archivo `Configurador.ts`.
2.  Añade una propiedad `private static version: string = "1.0.5"`. Hazla de solo lectura (`readonly`).
3.  Añade una propiedad `private static modo: string = "desarrollo"`. Este será el estado compartido que podremos cambiar.
4.  Crea un método `public static establecerModo(nuevoModo: 'desarrollo' | 'produccion' | 'testing')` que permita cambiar el valor de la propiedad `modo`.
5.  Crea un método `public static obtenerConfiguracion()` que imprima en la consola la versión y el modo actual.
6.  En `main.ts`, demuestra el uso de la clase **sin crear ninguna instancia**.

**Código de Partida (`Configurador.ts`):**

```typescript
// archivo: Configurador.ts
export class Configurador {
  // TODO: Añadir propiedades estáticas (version y modo)

  // TODO: Añadir método estático para establecer el modo

  // TODO: Añadir método estático para obtener la configuración
}
```

**Pruebas Sugeridas (en `main.ts`):**

```typescript
// archivo: main.ts
import { Configurador } from "./Configurador";

console.log("--- Configuración Inicial ---");
// 1. Llama a obtenerConfiguracion() ANTES de hacer nada.
Configurador.obtenerConfiguracion();

console.log("\n--- Cambiando a modo Producción ---");
// 2. Cambia el modo a "produccion".
Configurador.establecerModo("produccion");
Configurador.obtenerConfiguracion();

// 3. Intenta cambiar la versión (no debería ser posible si es readonly).
// Configurador.version = "2.0.0"; // Esto debería dar un error.
```

**Desafío Adicional:**
Modifica el método `establecerModo()` para que imprima un mensaje de advertencia si se intenta cambiar al mismo modo que ya está configurado.

---

### Ejercicio 2: Igualdad de Objetos - Fichas de Dominó

**Objetivo:** Implementar un método personalizado para determinar si dos objetos son "iguales" por su valor, no por su referencia en memoria.

**Consigna:**
Una ficha de dominó tiene dos valores numéricos. Dos fichas se consideran equivalentes si tienen los mismos números, sin importar el orden. Por ejemplo, una ficha `[3, 6]` es equivalente a una ficha `[6, 3]`.

1.  **Crea la clase `FichaDomino`** en un archivo `FichaDomino.ts`.
2.  La clase debe tener dos propiedades privadas: `ladoA: number` y `ladoB: number`.
3.  Implementa el constructor para inicializar estas propiedades.
4.  Crea un método `public esEquivalenteA(otraFicha: FichaDomino): boolean`. Este método debe devolver `true` si la otra ficha tiene los mismos valores, incluso si están invertidos.
5.  Sobrescribe el método `toString()` para que muestre la ficha de forma legible, por ejemplo: `[3|6]`.

**Código de Partida (`FichaDomino.ts`):**

```typescript
// archivo: FichaDomino.ts
export class FichaDomino {
  private ladoA: number;
  private ladoB: number;

  constructor(ladoA: number, ladoB: number) {
    this.ladoA = ladoA;
    this.ladoB = ladoB;
  }

  public esEquivalenteA(otraFicha: FichaDomino): boolean {
    // TODO: Implementar la lógica de equivalencia.
    // Pista: Comprueba (A==A y B==B) O (A==B y B==A).
    return false; // Reemplazar
  }

  public toString(): string {
    // TODO: Implementar la representación en string.
    return `[${this.ladoA}|${this.ladoB}]`;
  }
}
```

**Pruebas Sugeridas (en `main.ts`):**

```typescript
// archivo: main.ts
import { FichaDomino } from "./FichaDomino";

const ficha1 = new FichaDomino(3, 6);
const ficha2 = new FichaDomino(3, 6); // Mismos valores, otra instancia
const ficha3 = new FichaDomino(6, 3); // Valores invertidos
const ficha4 = new FichaDomino(1, 5); // Valores diferentes
const ficha5 = ficha1; // Misma referencia

console.log("--- Igualdad por Referencia (===) ---");
console.log(`¿ficha1 === ficha2? ${ficha1 === ficha2}`); // Esperado: false
console.log(`¿ficha1 === ficha5? ${ficha1 === ficha5}`); // Esperado: true

console.log("\n--- Igualdad por Valor (esEquivalenteA) ---");
console.log(`¿${ficha1} es equivalente a ${ficha2}? ${ficha1.esEquivalenteA(ficha2)}`); // Esperado: true
console.log(`¿${ficha1} es equivalente a ${ficha3}? ${ficha1.esEquivalenteA(ficha3)}`); // Esperado: true
console.log(`¿${ficha1} es equivalente a ${ficha4}? ${ficha1.esEquivalenteA(ficha4)}`); // Esperado: false
```

---

### Ejercicio 3: Copia Superficial y Profunda - Clonando un Equipo

**Objetivo:** Entender y visualizar la diferencia fundamental entre una copia superficial y una profunda al modificar objetos anidados.

**Consigna:**
Vamos a modelar un equipo deportivo. El equipo tiene un nombre y una lista de jugadores. Queremos poder clonar el equipo, pero veremos qué pasa cuando modificamos la lista de jugadores en la copia.

1.  **Crea una clase simple `Jugador`** con una propiedad `nombre: string`.
2.  **Crea la clase `Equipo`** con `nombre: string` y `jugadores: Jugador[]`.
3.  En la clase `Equipo`, implementa dos métodos de clonación:
    *   `public clonarSuperficial(): Equipo`: Debe crear una nueva instancia de `Equipo` usando el operador de propagación (`...this`) o `Object.assign`.
    *   `public clonarProfundo(): Equipo`: Debe crear una nueva instancia de `Equipo` y, además, crear **nuevas instancias** para cada jugador en la lista.
4.  En `main.ts`, crea un equipo original, clónalo con ambos métodos, modifica un jugador en cada copia y observa el efecto en el equipo original.

**Código de Partida:**

```typescript
// archivo: Jugador.ts
export class Jugador {
  constructor(public nombre: string) {}
}

// archivo: Equipo.ts
import { Jugador } from "./Jugador";

export class Equipo {
  public nombre: string;
  public jugadores: Jugador[];

  constructor(nombre: string, jugadores: Jugador[]) {
    this.nombre = nombre;
    this.jugadores = jugadores;
  }

  public clonarSuperficial(): Equipo {
    console.log("Realizando copia superficial...");
    // TODO: Usar el operador de propagación para crear una copia.
    return new Equipo(this.nombre, this.jugadores); // Reemplazar
  }

  public clonarProfundo(): Equipo {
    console.log("Realizando copia profunda...");
    // TODO: Crear un nuevo array y nuevas instancias de Jugador.
    // Pista: usa el método `.map()` en el array de jugadores.
    const nuevosJugadores = this.jugadores.map(j => new Jugador(j.nombre));
    return new Equipo(this.nombre, nuevosJugadores);
  }

  public imprimir(): void {
    const nombres = this.jugadores.map(j => j.nombre).join(', ');
    console.log(`Equipo: ${this.nombre}, Jugadores: ${nombres}`);
  }
}
```

**Pruebas Sugeridas (en `main.ts`):**

```typescript
// archivo: main.ts
import { Jugador } from "./Jugador";
import { Equipo } from "./Equipo";

const jugadoresOriginales = [new Jugador("Messi"), new Jugador("Maradona")];
const equipoOriginal = new Equipo("Argentina", jugadoresOriginales);

console.log("--- Prueba con Copia Superficial ---");
const copiaSuperficial = equipoOriginal.clonarSuperficial();
// Modificamos un jugador a través de la copia
copiaSuperficial.jugadores[0].nombre = "Riquelme";

console.log("Original después de modificar copia superficial:");
equipoOriginal.imprimir(); // Esperado: El nombre del jugador cambió!

// Reseteamos para la siguiente prueba
equipoOriginal.jugadores[0].nombre = "Messi"; 

console.log("\n--- Prueba con Copia Profunda ---");
const copiaProfunda = equipoOriginal.clonarProfundo();
// Modificamos un jugador a través de la copia
copiaProfunda.jugadores[0].nombre = "Di María";

console.log("Original después de modificar copia profunda:");
equipoOriginal.imprimir(); // Esperado: El nombre del jugador NO cambió.
```