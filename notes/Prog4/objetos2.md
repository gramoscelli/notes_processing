# Programación Orientada por Objetos - Continuación

## Override y Polimorfismo

### ¿Qué es Override (Sobrescritura)?

Cuando una clase hija hereda de una clase padre, puede **redefinir** o **sobrescribir** los métodos de la clase padre para proporcionar su propia implementación específica. Esto se llama **Override**.

La sobrescritura permite que cada clase hija tenga un comportamiento específico para un método, aunque todas compartan la misma "interfaz" o "firma" del método.

### ¿Qué es el Polimorfismo?

El polimorfismo en la programación orientada a objetos se refiere a la capacidad de objetos de diferentes clases para responder a la misma operación o mensaje de manera diferente.

**Esto permite que el código sea más flexible y se reutilice de manera más efectiva**. Un objeto de clase base puede ser tratado como si fuera de varias clases diferentes, lo que significa que diferentes implementaciones de la misma operación pueden ser invocadas según el tipo de objeto que se esté manipulando. 

De esta manera podemos escribir código más generalizado y abstracto, que puede manejar diferentes tipos de objetos sin conocer los detalles específicos de cada uno.

### La clase Object en TypeScript

En TypeScript, al igual que en JavaScript, **todos los objetos heredan implícitamente de la clase `Object`**. Esto significa que sin saberlo, cuando creamos cualquier clase, automáticamente estamos usando herencia.

La clase `Object` en TypeScript provee varios métodos básicos que todas las clases heredan automáticamente:
- `toString()`: Convierte el objeto a una representación en string
- `valueOf()`: Devuelve el valor primitivo del objeto
- `hasOwnProperty()`: Verifica si el objeto tiene una propiedad específica

El más importante y utilizado es `toString()`. Por defecto, cuando llamamos a `toString()` en cualquier objeto, obtenemos algo como `[object Object]`, que no es muy útil. Pero podemos **sobrescribir** este método para que devuelva información más útil sobre nuestro objeto.

#### Ejemplo de toString() por defecto vs sobrescrito:

```ts
// archivo: vehiculo-basico.ts
export class VehiculoBasico {
  private marca: string;
  private modelo: string;

  constructor(marca: string, modelo: string) {
    this.marca = marca;
    this.modelo = modelo;
  }

  public getMarca(): string { return this.marca; }
  public getModelo(): string { return this.modelo; }

  // NO sobrescribimos toString() - usará el de Object
}
```

```ts
// archivo: vehiculo-mejorado.ts
export class VehiculoMejorado {
  private marca: string;
  private modelo: string;

  constructor(marca: string, modelo: string) {
    this.marca = marca;
    this.modelo = modelo;
  }

  // SÍ sobrescribimos toString() - nuestra propia implementación
  public toString(): string {
    return `${this.marca} ${this.modelo}`;
  }

  public getMarca(): string { return this.marca; }
  public getModelo(): string { return this.modelo; }
}
```

```ts
// archivo: main.ts - Comparando ambos enfoques
import { VehiculoBasico } from "./vehiculo-basico";
import { VehiculoMejorado } from "./vehiculo-mejorado";

const vehiculoBasico = new VehiculoBasico("Toyota", "Corolla");
const vehiculoMejorado = new VehiculoMejorado("Honda", "Civic");

console.log("=== SIN SOBRESCRIBIR toString() ===");
console.log(vehiculoBasico.toString());  // [object Object]
console.log(`Vehículo: ${vehiculoBasico}`);  // Vehículo: [object Object]

console.log("\n=== SOBRESCRIBIENDO toString() ===");
console.log(vehiculoMejorado.toString());  // Honda Civic
console.log(`Vehículo: ${vehiculoMejorado}`);  // Vehículo: Honda Civic
```

**Salida esperada:**
```
=== SIN SOBRESCRIBIR toString() ===
[object Object]
Vehículo: [object Object]

=== SOBRESCRIBIENDO toString() ===
Honda Civic
Vehículo: Honda Civic
```

#### ¿Por qué es importante sobrescribir toString()?

Cuando queremos imprimir un objeto o convertirlo a string, TypeScript automáticamente llama al método `toString()`. Si no lo sobrescribimos, obtenemos la implementación por defecto de `Object` que no es informativa.

Al sobrescribirlo, podemos:
- Mostrar información relevante del objeto
- Facilitar la depuración (debugging)
- Hacer que nuestro código sea más legible
- Permitir que nuestros objetos se comporten bien en logs y mensajes

#### Ejemplo más complejo con diferentes implementaciones de toString():

```ts
// archivo: persona-toString.ts
export class Persona {
  private nombre: string;
  private edad: number;
  private email: string;

  constructor(nombre: string, edad: number, email: string) {
    this.nombre = nombre;
    this.edad = edad;
    this.email = email;
  }

  // Sobrescribimos toString() para mostrar información útil
  public toString(): string {
    return `${this.nombre} (${this.edad} años) - ${this.email}`;
  }

  // Método adicional para diferentes formatos
  public toStringCorto(): string {
    return `${this.nombre}, ${this.edad} años`;
  }

  public toStringFormal(): string {
    return `Sr./Sra. ${this.nombre}`;
  }

  public getNombre(): string { return this.nombre; }
  public getEdad(): number { return this.edad; }
  public getEmail(): string { return this.email; }
}
```

```ts
// archivo: estudiante-toString.ts
import { Persona } from "./persona-toString";

export class Estudiante extends Persona {
  private carrera: string;
  private universidad: string;

  constructor(nombre: string, edad: number, email: string, carrera: string, universidad: string) {
    super(nombre, edad, email);
    this.carrera = carrera;
    this.universidad = universidad;
  }

  // Sobrescribimos toString() con información específica de estudiante
  public toString(): string {
    return `${super.toString()} - Estudiante de ${this.carrera} en ${this.universidad}`;
  }

  public getCarrera(): string { return this.carrera; }
  public getUniversidad(): string { return this.universidad; }
}
```

```ts
// archivo: main.ts - Polimorfismo con toString()
import { Persona } from "./persona-toString";
import { Estudiante } from "./estudiante-toString";

const personas: Persona[] = [
  new Persona("Juan Pérez", 35, "juan@email.com"),
  new Estudiante("María López", 20, "maria@estudiante.com", "Ingeniería", "UTN"),
  new Persona("Carlos García", 28, "carlos@email.com"),
  new Estudiante("Ana Martínez", 19, "ana@estudiante.com", "Medicina", "UBA")
];

console.log("=== POLIMORFISMO CON toString() ===");
personas.forEach((persona, index) => {
  console.log(`${index + 1}. ${persona.toString()}`);
  // Cada objeto usa su propia implementación de toString()
});

// También funciona automáticamente cuando concatenamos strings
console.log("\n=== CONCATENACIÓN AUTOMÁTICA ===");
console.log("La primera persona es: " + personas[0]);
console.log("El primer estudiante es: " + personas[1]);
```

**Salida esperada:**
```
=== POLIMORFISMO CON toString() ===
1. Juan Pérez (35 años) - juan@email.com
2. María López (20 años) - maria@estudiante.com - Estudiante de Ingeniería en UTN
3. Carlos García (28 años) - carlos@email.com
4. Ana Martínez (19 años) - ana@estudiante.com - Estudiante de Medicina en UBA

=== CONCATENACIÓN AUTOMÁTICA ===
La primera persona es: Juan Pérez (35 años) - juan@email.com
El primer estudiante es: María López (20 años) - maria@estudiante.com - Estudiante de Ingeniería en UTN
```

Esta es la base del polimorfismo: el mismo código (`persona.toString()`) se comporta de manera diferente dependiendo del tipo real del objeto, pero nosotros como programadores no necesitamos saber qué tipo específico es.

### Ejemplo práctico de Polimorfismo

Supongamos que tenemos una clase `Impresora` que tiene un método llamado `imprimirEnPantalla(objeto: any)`. Este método puede recibir cualquier objeto y lo que hace internamente es llamar al método `toString()` del objeto que recibe.

Luego crearemos diferentes clases como `Bicicleta`, `Auto`, `Persona`, etc. Cada una implementará su propio método `toString()` de manera diferente.

Cuando llamemos a `imprimirEnPantalla()`, el mismo método se comportará de manera diferente dependiendo del tipo de objeto que le pasemos. **¡Eso es polimorfismo!**

```ts
// archivo: impresora.ts
export class Impresora {
  public imprimirEnPantalla(objeto: any): void {
    console.log(objeto.toString());
  }
  // Nota: objeto.toString() es equivalente a objeto.toString()
  // TypeScript automáticamente llamará al método toString() del objeto
}
```

```ts
// archivo: bicicleta.ts
export class Bicicleta {
  private marca: string;
  private modelo: string;

  constructor(marca: string = "", modelo: string = "") {
    this.marca = marca;
    this.modelo = modelo;
  }

  // Sobrescribimos el método toString() para nuestra clase
  public toString(): string {
    return `Soy una bicicleta ${this.marca} modelo ${this.modelo}`;
  }

  public getMarca(): string { return this.marca; }
  public setMarca(marca: string): void { this.marca = marca; }
  public getModelo(): string { return this.modelo; }
  public setModelo(modelo: string): void { this.modelo = modelo; }
}
```

```ts
// archivo: auto.ts
export class Auto {
  private marca: string;
  private año: number;

  constructor(marca: string = "", año: number = 0) {
    this.marca = marca;
    this.año = año;
  }

  // Cada clase tiene su propia implementación de toString()
  public toString(): string {
    return `Auto ${this.marca} del año ${this.año}`;
  }

  public getMarca(): string { return this.marca; }
  public setMarca(marca: string): void { this.marca = marca; }
  public getAño(): number { return this.año; }
  public setAño(año: number): void { this.año = año; }
}
```

### ¿Qué imprime esto en pantalla?

```ts
// archivo: main.ts
import { Impresora } from "./impresora";
import { Bicicleta } from "./bicicleta";
import { Auto } from "./auto";

const impresora = new Impresora();
const bicicleta = new Bicicleta("Trek", "Mountain");
const auto = new Auto("Toyota", 2020);

impresora.imprimirEnPantalla(bicicleta);
impresora.imprimirEnPantalla(auto);

// ¿Qué pasaría si creo un objeto genérico?
const objetoGenerico = { nombre: "Juan", edad: 25 };
impresora.imprimirEnPantalla(objetoGenerico);
```

**Respuesta:**
```
Soy una bicicleta Trek modelo Mountain
Auto Toyota del año 2020
[object Object]
```

El polimorfismo aquí es que `impresora.imprimirEnPantalla()` acepta como entrada un objeto, que no sabe específicamente qué tipo es, puede ser una Bicicleta, Auto, Persona, etc., pero está seguro que sea cual sea tiene un método `toString()`. Tampoco sabe lo que tiene `toString()` adentro, y no le importa, solo sabe que es algo representable como string y lo imprime. **Eso es polimorfismo**.

### Ejemplo más complejo: Sistema de Vehículos con Polimorfismo

```ts
// archivo: vehiculo.ts
export class Vehiculo {
  protected marca: string;
  protected año: number;

  constructor(marca: string, año: number) {
    this.marca = marca;
    this.año = año;
  }

  public acelerar(): string {
    return "El vehículo está acelerando";
  }

  public frenar(): string {
    return "El vehículo está frenando";
  }

  public toString(): string {
    return `Vehículo ${this.marca} del año ${this.año}`;
  }

  public getMarca(): string { return this.marca; }
  public setMarca(marca: string): void { this.marca = marca; }
  public getAño(): number { return this.año; }
  public setAño(año: number): void { this.año = año; }
}
```

```ts
// archivo: auto.ts
import { Vehiculo } from "./vehiculo";

export class Auto extends Vehiculo {
  private puertas: number;

  constructor(marca: string, año: number, puertas: number) {
    super(marca, año);
    this.puertas = puertas;
  }

  // Sobrescribimos el método acelerar para que sea específico de Auto
  public acelerar(): string {
    return `El auto ${this.marca} acelera suavemente con ${this.puertas} puertas`;
  }

  public frenar(): string {
    return `El auto ${this.marca} frena usando frenos ABS`;
  }

  public toString(): string {
    return `Auto ${this.marca} del año ${this.año} con ${this.puertas} puertas`;
  }

  public getPuertas(): number { return this.puertas; }
  public setPuertas(puertas: number): void { this.puertas = puertas; }
}
```

```ts
// archivo: motocicleta.ts
import { Vehiculo } from "./vehiculo";

export class Motocicleta extends Vehiculo {
  private cilindrada: number;

  constructor(marca: string, año: number, cilindrada: number) {
    super(marca, año);
    this.cilindrada = cilindrada;
  }

  // La motocicleta acelera de manera diferente al auto
  public acelerar(): string {
    return `La motocicleta ${this.marca} acelera rápidamente con ${this.cilindrada}cc`;
  }

  public frenar(): string {
    return `La motocicleta ${this.marca} frena usando frenos de disco`;
  }

  public toString(): string {
    return `Motocicleta ${this.marca} del año ${this.año} de ${this.cilindrada}cc`;
  }

  public getCilindrada(): number { return this.cilindrada; }
  public setCilindrada(cilindrada: number): void { this.cilindrada = cilindrada; }
}
```

```ts
// archivo: main.ts - Ejemplo de polimorfismo en acción
import { Vehiculo } from "./vehiculo";
import { Auto } from "./auto";
import { Motocicleta } from "./motocicleta";

// Creamos un array que puede contener diferentes tipos de vehículos
const vehiculos: Vehiculo[] = [
  new Auto("Toyota", 2020, 4),
  new Motocicleta("Honda", 2021, 600),
  new Auto("Ford", 2019, 2),
  new Motocicleta("Yamaha", 2022, 300)
];

console.log("=== POLIMORFISMO EN ACCIÓN ===");

// Polimorfismo: el mismo código funciona para diferentes tipos de objetos
vehiculos.forEach((vehiculo, index) => {
  console.log(`Vehículo ${index + 1}:`);
  console.log(vehiculo.toString());     // Cada uno muestra diferente información
  console.log(vehiculo.acelerar());     // Cada uno acelera de manera diferente
  console.log(vehiculo.frenar());       // Cada uno frena de manera diferente
  console.log("---");
});
```

**Salida esperada:**
```
=== POLIMORFISMO EN ACCIÓN ===
Vehículo 1:
Auto Toyota del año 2020 con 4 puertas
El auto Toyota acelera suavemente con 4 puertas
El auto Toyota frena usando frenos ABS
---
Vehículo 2:
Motocicleta Honda del año 2021 de 600cc
La motocicleta Honda acelera rápidamente con 600cc
La motocicleta Honda frena usando frenos de disco
---
...
```

## Arrays y Collections en TypeScript

### ¿Qué son los Arrays?

TypeScript provee **arrays**, que es una estructura muy útil y básica, que seguramente conocerán de otros lenguajes. Los arrays nos permiten almacenar múltiples elementos del mismo tipo en una sola variable.

A diferencia de algunos lenguajes más estrictos, **en TypeScript los arrays son dinámicos**, lo que significa que pueden cambiar de tamaño durante la ejecución del programa.

### ¿Cómo se declara un Array?

En TypeScript, se puede definir un array utilizando la siguiente sintaxis:

```ts
tipoDeDato[] nombreDelArray = [elemento1, elemento2, ...];
```

Donde:
- `tipoDeDato` es el tipo de dato que almacenará el array, por ejemplo `number`, `string`, `boolean`, o cualquier clase que hayamos creado.
- `nombreDelArray` es el nombre que le daremos al array.
- Los elementos van entre corchetes `[]` separados por comas.

#### Ejemplos básicos:

```ts
// Array de números
let numeros: number[] = [10, 20, 30, 40, 50];

// Array de strings
let finDeSemana: string[] = ["sábado", "domingo"];

// Array de booleanos
let respuestas: boolean[] = [true, false, true, false];

// También se puede usar la sintaxis genérica (menos común)
let valores: Array<number> = [1, 2, 3, 4];
```

### ¿Cómo se accede a los elementos?

Para acceder a un elemento del Array se debe poner el índice del elemento entre corchetes. **Recordar que el índice del primer elemento de un Array es cero**.

Por ejemplo, si queremos acceder al segundo elemento del array "numeros":

```ts
let numeros: number[] = [10, 20, 30, 40, 50];
let valor: number = numeros[1];  // valor será 20
console.log(valor);  // Imprime: 20

// Otros ejemplos
console.log(numeros[0]);  // Imprime: 10 (primer elemento)
console.log(numeros[4]);  // Imprime: 50 (último elemento)
```

### Arrays dinámicos

Los arrays en TypeScript son dinámicos, lo que significa que podemos:
- Agregar elementos
- Remover elementos
- Cambiar su tamaño durante la ejecución

```ts
// Crear un array vacío
let frutas: string[] = [];

// Agregar elementos al final
frutas.push("manzana");
frutas.push("banana"); 
frutas.push("naranja");

console.log(frutas);  // ["manzana", "banana", "naranja"]
console.log(frutas.length);  // 3

// Remover el último elemento
let ultimaFruta = frutas.pop();
console.log(ultimaFruta);  // "naranja"
console.log(frutas);  // ["manzana", "banana"]

// Agregar elemento al principio
frutas.unshift("uva");
console.log(frutas);  // ["uva", "manzana", "banana"]

// Remover el primer elemento
let primeraFruta = frutas.shift();
console.log(primeraFruta);  // "uva"
console.log(frutas);  // ["manzana", "banana"]
```

### Arrays de Objetos

Lo más interesante es que podemos crear arrays de objetos de nuestras propias clases:

```ts
// archivo: main.ts
import { Persona } from "./persona";

// Crear un array de personas
let personas: Persona[] = [];

// Agregar personas al array
personas.push(new Persona("Juan", new Date(1990, 5, 15)));
personas.push(new Persona("María", new Date(1985, 10, 22)));
personas.push(new Persona("Pedro", new Date(1992, 2, 8)));

console.log(`Tenemos ${personas.length} personas`);

// Recorrer el array e imprimir cada persona
for (let i = 0; i < personas.length; i++) {
  console.log(`${i + 1}. ${personas[i].toString()} - Edad: ${personas[i].getEdad()}`);
}
```

### Métodos útiles de Arrays

TypeScript/JavaScript provee muchos métodos útiles para trabajar con arrays:

```ts
let numeros: number[] = [1, 5, 3, 8, 2, 7, 4];

// length: obtener la cantidad de elementos
console.log(numeros.length);  // 7

// includes: verificar si un elemento existe
console.log(numeros.includes(5));  // true
console.log(numeros.includes(10)); // false

// indexOf: encontrar la posición de un elemento
console.log(numeros.indexOf(8));   // 3
console.log(numeros.indexOf(10));  // -1 (no encontrado)

// slice: obtener una porción del array (sin modificar el original)
let porcion = numeros.slice(2, 5);  // del índice 2 al 4
console.log(porcion);  // [3, 8, 2]
console.log(numeros);  // [1, 5, 3, 8, 2, 7, 4] (original sin cambios)

// splice: remover elementos del array (modifica el original)
let removidos = numeros.splice(2, 2);  // desde índice 2, remover 2 elementos
console.log(removidos);  // [3, 8]
console.log(numeros);    // [1, 5, 2, 7, 4] (original modificado)
```

### Métodos avanzados de Arrays

```ts
let numeros: number[] = [1, 5, 3, 8, 2, 7];

// map: transforma cada elemento y devuelve un nuevo array
let numerosDobles = numeros.map(n => n * 2);
console.log(numerosDobles);  // [2, 10, 6, 16, 4, 14]
console.log(numeros);        // [1, 5, 3, 8, 2, 7] (original sin cambios)

// filter: filtra elementos que cumplan una condición
let numerosPares = numeros.filter(n => n % 2 === 0);
console.log(numerosPares);  // [8, 2]

// find: encuentra el primer elemento que cumple una condición
let numeroMayor5 = numeros.find(n => n > 5);
console.log(numeroMayor5);  // 8

// some: verifica si al menos un elemento cumple la condición
let hayMayorA10 = numeros.some(n => n > 10);
console.log(hayMayorA10);  // false

// every: verifica si todos los elementos cumplen la condición
let todosPositivos = numeros.every(n => n > 0);
console.log(todosPositivos);  // true

// reduce: reduce el array a un solo valor
let suma = numeros.reduce((acumulador, actual) => acumulador + actual, 0);
console.log(suma);  // 26

// sort: ordena el array (modifica el original)
let numerosOrdenados = [...numeros].sort((a, b) => a - b);  // copia y ordena
console.log(numerosOrdenados);  // [1, 2, 3, 5, 7, 8]
console.log(numeros);           // [1, 5, 3, 8, 2, 7] (original sin cambios)
```

### Ejemplo práctico: Sistema de Gestión de Estudiantes

```ts
// archivo: lista-estudiantes.ts
import { Estudiante } from "./estudiante";

export class ListaEstudiantes {
  private estudiantes: Estudiante[];

  constructor() {
    this.estudiantes = [];
  }

  public agregarEstudiante(estudiante: Estudiante): void {
    this.estudiantes.push(estudiante);
    console.log(`Estudiante ${estudiante.getNombre()} agregado correctamente`);
  }

  public removerEstudiante(nombre: string): boolean {
    const indice = this.estudiantes.findIndex(est => est.getNombre() === nombre);
    if (indice !== -1) {
      const estudianteRemovido = this.estudiantes.splice(indice, 1)[0];
      console.log(`Estudiante ${estudianteRemovido.getNombre()} removido correctamente`);
      return true;
    }
    console.log(`No se encontró el estudiante ${nombre}`);
    return false;
  }

  public buscarPorNombre(nombre: string): Estudiante | undefined {
    return this.estudiantes.find(est => est.getNombre() === nombre);
  }

  public filtrarPorColegio(colegio: string): Estudiante[] {
    return this.estudiantes.filter(est => est.getColegio() === colegio);
  }

  public obtenerTodos(): Estudiante[] {
    return [...this.estudiantes];  // Retorna una copia para evitar modificaciones externas
  }

  public getCantidad(): number {
    return this.estudiantes.length;
  }

  public imprimirListaCompleta(): void {
    console.log("=== LISTA COMPLETA DE ESTUDIANTES ===");
    if (this.estudiantes.length === 0) {
      console.log("No hay estudiantes registrados");
      return;
    }

    this.estudiantes.forEach((estudiante, index) => {
      console.log(`${index + 1}. ${estudiante.toString()} - Edad: ${estudiante.getEdad()}`);
    });
  }

  public obtenerEstadisticas(): void {
    console.log("=== ESTADÍSTICAS ===");
    console.log(`Total de estudiantes: ${this.estudiantes.length}`);
    
    if (this.estudiantes.length === 0) return;

    // Agrupar por colegio
    const porColegio: {[colegio: string]: number} = {};
    this.estudiantes.forEach(est => {
      const colegio = est.getColegio();
      porColegio[colegio] = (porColegio[colegio] || 0) + 1;
    });

    console.log("Estudiantes por colegio:");
    Object.keys(porColegio).forEach(colegio => {
      console.log(`  ${colegio}: ${porColegio[colegio]} estudiantes`);
    });

    // Promedio de edad
    const edades = this.estudiantes.map(est => est.getEdad());
    const promedioEdad = edades.reduce((sum, edad) => sum + edad, 0) / edades.length;
    console.log(`Promedio de edad: ${promedioEdad.toFixed(1)} años`);
  }
}
```

```ts
// archivo: main.ts - Ejemplo de uso
import { Estudiante } from "./estudiante";
import { ListaEstudiantes } from "./lista-estudiantes";

const lista = new ListaEstudiantes();

// Agregar estudiantes
lista.agregarEstudiante(new Estudiante("Juan Pérez", new Date(2005, 3, 15), "Colegio San José"));
lista.agregarEstudiante(new Estudiante("María González", new Date(2004, 8, 22), "Colegio Nacional"));
lista.agregarEstudiante(new Estudiante("Pedro Rodríguez", new Date(2005, 11, 8), "Colegio San José"));
lista.agregarEstudiante(new Estudiante("Ana Martínez", new Date(2003, 6, 12), "Colegio Nacional"));

// Mostrar lista completa
lista.imprimirListaCompleta();

// Buscar un estudiante específico
const estudianteBuscado = lista.buscarPorNombre("María González");
if (estudianteBuscado) {
  console.log(`Encontrado: ${estudianteBuscado.toString()}`);
}

// Filtrar por colegio
const estudiantesSanJose = lista.filtrarPorColegio("Colegio San José");
console.log("Estudiantes del Colegio San José:");
estudiantesSanJose.forEach(est => console.log(`  - ${est.getNombre()}`));

// Mostrar estadísticas
lista.obtenerEstadisticas();

// Remover un estudiante
lista.removerEstudiante("Pedro Rodríguez");
lista.imprimirListaCompleta();
```

## Clases Abstractas

### ¿Qué es una Clase Abstracta?

Una **clase abstracta** es una clase especial que **no puede ser instanciada directamente**. Su propósito es servir como plantilla o molde para otras clases que la hereden.

Las clases abstractas pueden contener:
- **Métodos concretos** (ya implementados) que las clases hijas pueden usar directamente
- **Métodos abstractos** (solo la firma, sin implementación) que las clases hijas **deben** implementar obligatoriamente
- **Atributos** que todas las clases hijas compartirán

### ¿Por qué usar Clases Abstractas?

Imaginen que queremos crear un sistema para diferentes tipos de figuras geométricas: círculos, rectángulos, triángulos, etc. Todas las figuras tienen características en común:
- Todas tienen un color
- Todas pueden calcular su área
- Todas pueden calcular su perímetro
- Todas pueden mostrarse como texto

Pero cada figura calcula su área y perímetro de manera diferente. Aquí es donde las clases abstractas son útiles: nos permiten definir la estructura común pero obligar a cada figura específica a implementar sus propios cálculos.

### Sintaxis de Clases Abstractas en TypeScript

```ts
// archivo: figura.ts
export abstract class Figura {
  protected color: string;  // Atributo común a todas las figuras

  constructor(color: string) {
    this.color = color;
  }

  // Método concreto (ya implementado) que todas las figuras pueden usar
  public getColor(): string {
    return this.color;
  }

  public setColor(color: string): void {
    this.color = color;
  }

  // Método concreto que usa los métodos abstractos
  public mostrarInformacion(): void {
    console.log(this.toString());
    console.log(`Color: ${this.color}`);
    console.log(`Área: ${this.calcularArea()}`);
    console.log(`Perímetro: ${this.calcularPerimetro()}`);
  }

  // Métodos abstractos (solo la firma) que DEBEN ser implementados por las clases hijas
  public abstract calcularArea(): number;
  public abstract calcularPerimetro(): number;
  public abstract toString(): string;
}
```

**Observen que:**
- La clase se declara con `abstract class`
- Los métodos abstractos se declaran con `abstract` y **no tienen implementación**
- Los métodos concretos sí tienen implementación y pueden usar métodos abstractos

### Implementando Clases Hijas

Ahora creamos clases específicas que hereden de `Figura`:

```ts
// archivo: circulo.ts
import { Figura } from "./figura";

export class Circulo extends Figura {
  private radio: number;

  constructor(color: string, radio: number) {
    super(color);  // Llamamos al constructor de la clase padre
    this.radio = radio;
  }

  // OBLIGATORIO: implementar todos los métodos abstractos
  public calcularArea(): number {
    return Math.PI * this.radio * this.radio;
  }

  public calcularPerimetro(): number {
    return 2 * Math.PI * this.radio;
  }

  public toString(): string {
    return `Círculo de radio ${this.radio}`;
  }

  // Métodos específicos del círculo
  public getRadio(): number { return this.radio; }
  public setRadio(radio: number): void { this.radio = radio; }

  public getDiametro(): number {
    return this.radio * 2;
  }
}
```

```ts
// archivo: rectangulo.ts
import { Figura } from "./figura";

export class Rectangulo extends Figura {
  private ancho: number;
  private alto: number;

  constructor(color: string, ancho: number, alto: number) {
    super(color);
    this.ancho = ancho;
    this.alto = alto;
  }

  // OBLIGATORIO: implementar todos los métodos abstractos
  public calcularArea(): number {
    return this.ancho * this.alto;
  }

  public calcularPerimetro(): number {
    return 2 * (this.ancho + this.alto);
  }

  public toString(): string {
    return `Rectángulo de ${this.ancho} x ${this.alto}`;
  }

  // Métodos específicos del rectángulo
  public getAncho(): number { return this.ancho; }
  public setAncho(ancho: number): void { this.ancho = ancho; }
  public getAlto(): number { return this.alto; }
  public setAlto(alto: number): void { this.alto = alto; }

  public esCuadrado(): boolean {
    return this.ancho === this.alto;
  }
}
```

```ts
// archivo: triangulo.ts
import { Figura } from "./figura";

export class Triangulo extends Figura {
  private lado1: number;
  private lado2: number;
  private lado3: number;

  constructor(color: string, lado1: number, lado2: number, lado3: number) {
    super(color);
    this.lado1 = lado1;
    this.lado2 = lado2;
    this.lado3 = lado3;
  }

  public calcularArea(): number {
    // Fórmula de Herón
    const s = this.calcularPerimetro() / 2;
    return Math.sqrt(s * (s - this.lado1) * (s - this.lado2) * (s - this.lado3));
  }

  public calcularPerimetro(): number {
    return this.lado1 + this.lado2 + this.lado3;
  }

  public toString(): string {
    return `Triángulo de lados ${this.lado1}, ${this.lado2}, ${this.lado3}`;
  }

  public getLado1(): number { return this.lado1; }
  public getLado2(): number { return this.lado2; }
  public getLado3(): number { return this.lado3; }

  public esEquilatero(): boolean {
    return this.lado1 === this.lado2 && this.lado2 === this.lado3;
  }
}
```

### Uso de Clases Abstractas y Polimorfismo

```ts
// archivo: main.ts
import { Figura } from "./figura";
import { Circulo } from "./circulo";
import { Rectangulo } from "./rectangulo";
import { Triangulo } from "./triangulo";

// ❌ Esto NO se puede hacer - no se puede instanciar una clase abstracta
// const figura = new Figura("rojo");  // Error de compilación

// ✅ Esto SÍ se puede hacer - instanciar las clases hijas
const circulo = new Circulo("azul", 5);
const rectangulo = new Rectangulo("verde", 4, 6);
const triangulo = new Triangulo("rojo", 3, 4, 5);

// ✅ Polimorfismo con clases abstractas
const figuras: Figura[] = [circulo, rectangulo, triangulo];

console.log("=== MOSTRANDO TODAS LAS FIGURAS ===");
figuras.forEach((figura, index) => {
  console.log(`\nFigura ${index + 1}:`);
  figura.mostrarInformacion();  // Cada figura se comporta diferente
});

// ✅ Podemos usar métodos específicos si hacemos casting
console.log("\n=== MÉTODOS ESPECÍFICOS ===");
if (circulo instanceof Circulo) {
  console.log(`El círculo tiene un diámetro de ${circulo.getDiametro()}`);
}

if (rectangulo instanceof Rectangulo) {
  console.log(`¿Es cuadrado? ${rectangulo.esCuadrado()}`);
}

if (triangulo instanceof Triangulo) {
  console.log(`¿Es equilátero? ${triangulo.esEquilatero()}`);
}
```

### Ejemplo más complejo: Sistema de Empleados

```ts
// archivo: empleado-abstracto.ts
export abstract class EmpleadoAbstracto {
  protected nombre: string;
  protected fechaNacimiento: Date;
  protected salarioBase: number;

  constructor(nombre: string, fechaNacimiento: Date, salarioBase: number) {
    this.nombre = nombre;
    this.fechaNacimiento = fechaNacimiento;
    this.salarioBase = salarioBase;
  }

  // Método concreto compartido por todos los empleados
  public getEdad(): number {
    const hoy = new Date();
    let edad = hoy.getFullYear() - this.fechaNacimiento.getFullYear();
    const m = hoy.getMonth() - this.fechaNacimiento.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < this.fechaNacimiento.getDate())) {
      edad--;
    }
    return edad;
  }

  public mostrarInformacionBasica(): void {
    console.log(`Nombre: ${this.nombre}`);
    console.log(`Edad: ${this.getEdad()} años`);
    console.log(`Tipo: ${this.getTipo()}`);
    console.log(`Salario: ${this.calcularSalario()}`);
  }

  // Métodos abstractos que deben implementar las clases hijas
  public abstract calcularSalario(): number;
  public abstract getTipo(): string;
  public abstract obtenerBeneficios(): string[];

  // Getters y setters
  public getNombre(): string { return this.nombre; }
  public setNombre(nombre: string): void { this.nombre = nombre; }
  public getFechaNacimiento(): Date { return this.fechaNacimiento; }
  public getSalarioBase(): number { return this.salarioBase; }
  public setSalarioBase(salario: number): void { this.salarioBase = salario; }
}
```

```ts
// archivo: empleado-fijo.ts
import { EmpleadoAbstracto } from "./empleado-abstracto";

export class EmpleadoFijo extends EmpleadoAbstracto {
  private bonificacion: number;
  private añosAntiguedad: number;

  constructor(nombre: string, fechaNacimiento: Date, salarioBase: number, 
              bonificacion: number, añosAntiguedad: number) {
    super(nombre, fechaNacimiento, salarioBase);
    this.bonificacion = bonificacion;
    this.añosAntiguedad = añosAntiguedad;
  }

  public calcularSalario(): number {
    const bonusAntiguedad = this.añosAntiguedad * 100; // $100 por año
    return this.salarioBase + this.bonificacion + bonusAntiguedad;
  }

  public getTipo(): string {
    return "Empleado Fijo";
  }

  public obtenerBeneficios(): string[] {
    return [
      "Seguro médico completo",
      "Vacaciones pagadas (30 días)",
      "Bonificación por antigüedad",
      "Fondo de jubilación"
    ];
  }

  public getBonificacion(): number { return this.bonificacion; }
  public setBonificacion(bonificacion: number): void { this.bonificacion = bonificacion; }
  public getAñosAntiguedad(): number { return this.añosAntiguedad; }
  public setAñosAntiguedad(años: number): void { this.añosAntiguedad = años; }
}
```

```ts
// archivo: empleado-por-horas.ts
import { EmpleadoAbstracto } from "./empleado-abstracto";

export class EmpleadoPorHoras extends EmpleadoAbstracto {
  private horasTrabajadas: number;
  private valorHora: number;

  constructor(nombre: string, fechaNacimiento: Date, salarioBase: number, valorHora: number) {
    super(nombre, fechaNacimiento, salarioBase);
    this.horasTrabajadas = 0;
    this.valorHora = valorHora;
  }

  public calcularSalario(): number {
    const salarioHoras = this.horasTrabajadas * this.valorHora;
    // Si trabaja más de 160 horas, obtiene horas extra (1.5x)
    let horasExtra = 0;
    if (this.horasTrabajadas > 160) {
      horasExtra = (this.horasTrabajadas - 160) * this.valorHora * 0.5;
    }
    return this.salarioBase + salarioHoras + horasExtra;
  }

  public getTipo(): string {
    return "Empleado por Horas";
  }

  public obtenerBeneficios(): string[] {
    const beneficios = ["Seguro médico básico"];
    if (this.horasTrabajadas >= 120) {
      beneficios.push("Vacaciones proporcionales");
    }
    if (this.horasTrabajadas >= 160) {
      beneficios.push("Pago de horas extra (1.5x)");
    }
    return beneficios;
  }

  public registrarHoras(horas: number): void {
    this.horasTrabajadas += horas;
    console.log(`Registradas ${horas} horas. Total: ${this.horasTrabajadas}`);
  }

  public resetearHoras(): void {
    this.horasTrabajadas = 0;
  }

  public getHorasTrabajadas(): number { return this.horasTrabajadas; }
  public getValorHora(): number { return this.valorHora; }
  public setValorHora(valor: number): void { this.valorHora = valor; }
}
```

```ts
// archivo: empleado-comisionista.ts
import { EmpleadoAbstracto } from "./empleado-abstracto";

export class EmpleadoComisionista extends EmpleadoAbstracto {
  private ventasRealizadas: number;
  private porcentajeComision: number;

  constructor(nombre: string, fechaNacimiento: Date, salarioBase: number, 
              porcentajeComision: number) {
    super(nombre, fechaNacimiento, salarioBase);
    this.ventasRealizadas = 0;
    this.porcentajeComision = porcentajeComision;
  }

  public calcularSalario(): number {
    const comision = this.ventasRealizadas * (this.porcentajeComision / 100);
    return this.salarioBase + comision;
  }

  public getTipo(): string {
    return "Empleado Comisionista";
  }

  public obtenerBeneficios(): string[] {
    const beneficios = ["Seguro médico básico", "Comisión por ventas"];
    if (this.ventasRealizadas >= 50000) {
      beneficios.push("Bonificación por metas alcanzadas");
      beneficios.push("Viaje de incentivo");
    }
    return beneficios;
  }

  public registrarVenta(montoVenta: number): void {
    this.ventasRealizadas += montoVenta;
    const comision = montoVenta * (this.porcentajeComision / 100);
    console.log(`Venta registrada: ${montoVenta}. Comisión: ${comision}`);
  }

  public resetearVentas(): void {
    this.ventasRealizadas = 0;
  }

  public getVentasRealizadas(): number { return this.ventasRealizadas; }
  public getPorcentajeComision(): number { return this.porcentajeComision; }
  public setPorcentajeComision(porcentaje: number): void { this.porcentajeComision = porcentaje; }
}
```

```ts
// archivo: empresa.ts
import { EmpleadoAbstracto } from "./empleado-abstracto";

export class Empresa {
  private nombre: string;
  private empleados: EmpleadoAbstracto[];

  constructor(nombre: string) {
    this.nombre = nombre;
    this.empleados = [];
  }

  public contratarEmpleado(empleado: EmpleadoAbstracto): void {
    this.empleados.push(empleado);
    console.log(`${empleado.getNombre()} ha sido contratado como ${empleado.getTipo()}`);
  }

  public despedirEmpleado(nombre: string): boolean {
    const indice = this.empleados.findIndex(emp => emp.getNombre() === nombre);
    if (indice !== -1) {
      const empleadoDespedido = this.empleados.splice(indice, 1)[0];
      console.log(`${empleadoDespedido.getNombre()} ha sido despedido`);
      return true;
    }
    console.log(`No se encontró el empleado ${nombre}`);
    return false;
  }

  public calcularTotalSalarios(): number {
    return this.empleados.reduce((total, empleado) => total + empleado.calcularSalario(), 0);
  }

  public generarReporteNomina(): void {
    console.log(`\n=== REPORTE DE NÓMINA - ${this.nombre} ===`);
    console.log(`Total de empleados: ${this.empleados.length}`);
    
    if (this.empleados.length === 0) {
      console.log("No hay empleados registrados");
      return;
    }

    console.log("\nDetalle por empleado:");
    this.empleados.forEach((empleado, index) => {
      console.log(`\n${index + 1}. ${empleado.getNombre()}`);
      console.log(`   Tipo: ${empleado.getTipo()}`);
      console.log(`   Edad: ${empleado.getEdad()} años`);
      console.log(`   Salario: ${empleado.calcularSalario()}`);
      
      const beneficios = empleado.obtenerBeneficios();
      console.log(`   Beneficios: ${beneficios.join(', ')}`);
    });

    console.log(`\nTOTAL A PAGAR: ${this.calcularTotalSalarios()}`);
  }

  public obtenerEmpleadosPorTipo(tipo: string): EmpleadoAbstracto[] {
    return this.empleados.filter(emp => emp.getTipo() === tipo);
  }

  public obtenerPromedioEdad(): number {
    if (this.empleados.length === 0) return 0;
    const sumaEdades = this.empleados.reduce((suma, emp) => suma + emp.getEdad(), 0);
    return sumaEdades / this.empleados.length;
  }

  public getNombre(): string { return this.nombre; }
  public getCantidadEmpleados(): number { return this.empleados.length; }
}
```

```ts
// archivo: main.ts - Sistema completo de empleados
import { Empresa } from "./empresa";
import { EmpleadoFijo } from "./empleado-fijo";
import { EmpleadoPorHoras } from "./empleado-por-horas";
import { EmpleadoComisionista } from "./empleado-comisionista";

// Crear la empresa
const empresa = new Empresa("TechCorp S.A.");

// Crear diferentes tipos de empleados
const empleadoFijo = new EmpleadoFijo(
  "Juan Pérez", 
  new Date(1985, 5, 15), 
  30000, // salario base
  5000,  // bonificación
  3      // años de antigüedad
);

const empleadoPorHoras = new EmpleadoPorHoras(
  "María González",
  new Date(1992, 10, 22),
  15000, // salario base mínimo
  25     // valor por hora
);

const empleadoComisionista = new EmpleadoComisionista(
  "Carlos Rodríguez",
  new Date(1988, 2, 8),
  20000, // salario base
  8      // 8% de comisión
);

// Contratar empleados
empresa.contratarEmpleado(empleadoFijo);
empresa.contratarEmpleado(empleadoPorHoras);
empresa.contratarEmpleado(empleadoComisionista);

// Simular actividad laboral
console.log("\n=== SIMULANDO ACTIVIDAD LABORAL ===");

// El empleado por horas trabaja
empleadoPorHoras.registrarHoras(40); // semana 1
empleadoPorHoras.registrarHoras(45); // semana 2
empleadoPorHoras.registrarHoras(38); // semana 3
empleadoPorHoras.registrarHoras(42); // semana 4

// El empleado comisionista hace ventas
empleadoComisionista.registrarVenta(15000);
empleadoComisionista.registrarVenta(22000);
empleadoComisionista.registrarVenta(18000);

// Generar reporte
empresa.generarReporteNomina();

// Estadísticas adicionales
console.log("\n=== ESTADÍSTICAS ADICIONALES ===");
console.log(`Promedio de edad: ${empresa.obtenerPromedioEdad().toFixed(1)} años`);

const empleadosFijos = empresa.obtenerEmpleadosPorTipo("Empleado Fijo");
console.log(`Empleados fijos: ${empleadosFijos.length}`);

const empleadosHoras = empresa.obtenerEmpleadosPorTipo("Empleado por Horas");
console.log(`Empleados por horas: ${empleadosHoras.length}`);

const empleadosComision = empresa.obtenerEmpleadosPorTipo("Empleado Comisionista");
console.log(`Empleados comisionistas: ${empleadosComision.length}`);
```

## Clases readonly

### ¿Qué significa readonly?

En TypeScript, podemos usar el modificador `readonly` para crear propiedades que **solo pueden ser asignadas durante la inicialización o en el constructor**. Una vez asignadas, no pueden ser modificadas.

Esto es muy útil para crear propiedades que deben mantenerse constantes durante toda la vida del objeto, como identificadores únicos, fechas de creación, configuraciones inmutables, etc.

### ¿Cuándo usar readonly?

Usamos `readonly` cuando:
- Queremos asegurar que ciertos valores no cambien después de la creación del objeto
- Necesitamos identificadores únicos (IDs, códigos, etc.)
- Queremos fechas de creación/registro inmutables
- Tenemos configuraciones que no deben modificarse
- Queremos arrays o objetos que no deben ser reasignados (aunque su contenido puede cambiar)

### Sintaxis de readonly

```ts
// archivo: producto.ts
export class Producto {
  public readonly id: string;           // ID único, no cambia nunca
  public readonly fechaCreacion: Date;  // Fecha de creación, no cambia nunca
  public readonly categoria: string;    // Categoría, no cambia una vez asignada
  
  private nombre: string;               // Nombre sí puede cambiar
  private precio: number;               // Precio sí puede cambiar

  constructor(categoria: string, nombre: string, precio: number) {
    this.id = this.generarId();         // Solo se puede asignar aquí
    this.fechaCreacion = new Date();    // Solo se puede asignar aquí
    this.categoria = categoria;         // Solo se puede asignar aquí
    this.nombre = nombre;
    this.precio = precio;
  }

  private generarId(): string {
    return `PROD_${Math.random().toString(36).substring(2, 15).toUpperCase()}`;
  }

  // Métodos getter para readonly properties - NO necesitan setter
  public getId(): string { return this.id; }
  public getFechaCreacion(): Date { return this.fechaCreacion; }
  public getCategoria(): string { return this.categoria; }

  // Métodos getter y setter para propiedades modificables
  public getNombre(): string { return this.nombre; }
  public setNombre(nombre: string): void { this.nombre = nombre; }
  
  public getPrecio(): number { return this.precio; }
  public setPrecio(precio: number): void { 
    if (precio > 0) {
      this.precio = precio;
    }
  }

  public toString(): string {
    return `${this.nombre} (ID: ${this.id}) - ${this.precio} - Categoría: ${this.categoria}`;
  }
}
```

### Arrays readonly

```ts
// archivo: configuracion.ts
export class Configuracion {
  // Array readonly - no se puede reasignar, pero su contenido puede leerse
  private readonly configuracionesValidas: readonly string[] = [
    "desarrollo",
    "produccion", 
    "testing",
    "staging"
  ];
  
  // Configuración actual sí puede cambiar
  private configuracionActual: string;

  constructor() {
    this.configuracionActual = "desarrollo"; // configuración por defecto
  }

  public esConfiguracionValida(config: string): boolean {
    return this.configuracionesValidas.includes(config);
  }

  public setConfiguracion(config: string): boolean {
    if (this.esConfiguracionValida(config)) {
      this.configuracionActual = config;
      console.log(`Configuración cambiada a: ${config}`);
      return true;
    }
    console.log(`Error: '${config}' no es una configuración válida`);
    return false;
  }

  public getConfiguracion(): string {
    return this.configuracionActual;
  }

  // Devolver copia readonly del array para evitar modificaciones externas
  public getConfiguracionesValidas(): readonly string[] {
    return this.configuracionesValidas;
  }

  public mostrarConfiguracionesDisponibles(): void {
    console.log("Configuraciones disponibles:");
    this.configuracionesValidas.forEach((config, index) => {
      const marca = config === this.configuracionActual ? " ← ACTUAL" : "";
      console.log(`  ${index + 1}. ${config}${marca}`);
    });
  }
}
```

### Ejemplo práctico: Sistema de Usuarios con readonly

```ts
// archivo: usuario.ts
export class Usuario {
  public readonly id: string;
  public readonly fechaRegistro: Date;
  public readonly tipoUsuario: string;
  private readonly rolesPermitidos: readonly string[] = [
    "invitado", 
    "usuario", 
    "moderador", 
    "admin"
  ];
  
  private nombre: string;
  private email: string;
  private rolActual: string;
  private activo: boolean;

  constructor(nombre: string, email: string, tipoUsuario: string = "usuario") {
    this.id = this.generarId();
    this.fechaRegistro = new Date();
    this.tipoUsuario = tipoUsuario;
    this.nombre = nombre;
    this.email = email;
    this.rolActual = "invitado"; // rol inicial
    this.activo = true;
  }

  private generarId(): string {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 8);
    return `USER_${timestamp}_${random}`.toUpperCase();
  }

  public cambiarRol(nuevoRol: string): boolean {
    if (!this.rolesPermitidos.includes(nuevoRol)) {
      console.log(`Error: '${nuevoRol}' no es un rol válido`);
      return false;
    }

    if (!this.activo) {
      console.log("Error: No se puede cambiar el rol de un usuario inactivo");
      return false;
    }

    const rolAnterior = this.rolActual;
    this.rolActual = nuevoRol;
    console.log(`Rol de ${this.nombre} cambiado de '${rolAnterior}' a '${nuevoRol}'`);
    return true;
  }

  public desactivar(): void {
    this.activo = false;
    this.rolActual = "invitado"; // Al desactivar, vuelve a invitado
    console.log(`Usuario ${this.nombre} desactivado`);
  }

  public reactivar(): void {
    this.activo = true;
    console.log(`Usuario ${this.nombre} reactivado`);
  }

  public puedeAccederA(recurso: string): boolean {
    if (!this.activo) return false;

    switch (this.rolActual) {
      case "invitado":
        return recurso === "pagina_publica";
      case "usuario":
        return ["pagina_publica", "perfil", "configuracion"].includes(recurso);
      case "moderador":
        return !["panel_admin", "configuracion_sistema"].includes(recurso);
      case "admin":
        return true;
      default:
        return false;
    }
  }

  // Getters para propiedades readonly
  public getId(): string { return this.id; }
  public getFechaRegistro(): Date { return this.fechaRegistro; }
  public getTipoUsuario(): string { return this.tipoUsuario; }
  
  // Getters y setters para propiedades modificables
  public getNombre(): string { return this.nombre; }
  public setNombre(nombre: string): void { this.nombre = nombre; }
  
  public getEmail(): string { return this.email; }
  public setEmail(email: string): void { this.email = email; }
  
  public getRolActual(): string { return this.rolActual; }
  public isActivo(): boolean { return this.activo; }

  public toString(): string {
    const estado = this.activo ? "Activo" : "Inactivo";
    return `${this.nombre} (${this.rolActual}) - ${estado} - Registrado: ${this.fechaRegistro.toLocaleDateString()}`;
  }
}
```

```ts
// archivo: main.ts - Ejemplo de uso de readonly
import { Usuario } from "./usuario";
import { Producto } from "./producto";
import { Configuracion } from "./configuracion";

console.log("=== EJEMPLO DE PROPIEDADES READONLY ===");

// Crear productos
const producto1 = new Producto("Electrónicos", "Laptop Gaming", 1200);
const producto2 = new Producto("Libros", "TypeScript Avanzado", 45);

console.log("\nProductos creados:");
console.log(producto1.toString());
console.log(producto2.toString());

// Las propiedades readonly no se pueden modificar
console.log(`\nID del producto 1: ${producto1.getId()}`);
// producto1.id = "NUEVO_ID"; // ❌ Error: Cannot assign to 'id' because it is a read-only property

// Pero las propiedades normales sí
producto1.setNombre("Super Laptop Gaming");
producto1.setPrecio(1100);
console.log(`Producto modificado: ${producto1.toString()}`);

// Configuración con arrays readonly
console.log("\n=== CONFIGURACIÓN DEL SISTEMA ===");
const config = new Configuracion();
config.mostrarConfiguracionesDisponibles();

config.setConfiguracion("produccion");
config.setConfiguracion("invalida"); // Esto fallará
config.mostrarConfiguracionesDisponibles();

// Usuarios con propiedades readonly
console.log("\n=== SISTEMA DE USUARIOS ===");
const usuario1 = new Usuario("Juan Pérez", "juan@email.com", "usuario");
const usuario2 = new Usuario("Ana Admin", "ana@email.com", "admin");

console.log(usuario1.toString());
console.log(usuario2.toString());

// IDs únicos generados automáticamente
console.log(`\nID único de Juan: ${usuario1.getId()}`);
console.log(`ID único de Ana: ${usuario2.getId()}`);

// Cambiar roles (permitido)
usuario1.cambiarRol("moderador");
usuario1.cambiarRol("admin");

// Intentar cambiar propiedades readonly (no permitido)
// usuario1.id = "NUEVO_ID";           // ❌ Error de compilación
// usuario1.fechaRegistro = new Date(); // ❌ Error de compilación

console.log("\nEstado final:");
console.log(usuario1.toString());
console.log(usuario2.toString());
```

## Ejercicios Prácticos

### Ejercicio 1: Sistema de Formas Geométricas Avanzado
Crear un sistema completo usando clases abstractas donde:

1. **Clase abstracta `Forma`** con:
   - Color (readonly)
   - Métodos abstractos: `calcularArea()`, `calcularPerimetro()`, `dibujar()`
   - Método concreto: `mostrarInformacion()`

2. **Clases concretas**: `Triangulo`, `Cuadrado`, `Circulo`, `Hexagono`

3. **Clase `Lienzo`** que:
   - Contenga un array de formas
   - Calcule el área total de todas las formas
   - Genere un reporte por tipo de forma
   - Encuentre la forma con mayor/menor área

### Ejercicio 2: Sistema de Vehículos con Readonly
Implementar un sistema de concesionario donde:

1. **Clase abstracta `Vehiculo`** con:
   - Propiedades readonly: `numeroChasis`, `fechaFabricacion`, `marca`
   - Métodos abstractos: `acelerar()`, `frenar()`, `obtenerTipoLicencia()`

2. **Clases hijas**: `Auto`, `Motocicleta`, `Camion`, `Bicicleta`

3. **Clase `Concesionario`** con:
   - Array de vehículos disponibles
   - Métodos para buscar por marca, año, tipo
   - Sistema de ventas con registro de fecha (readonly)

### Ejercicio 3: Sistema de Gestión Académica
Desarrollar un sistema universitario completo:

1. **Clase abstracta `Persona`** con datos básicos y método abstracto `obtenerRol()`

2. **Clases hijas**: `Estudiante`, `Profesor`, `Personal`

3. **Clase `Universidad`** que:
   - Maneje arrays de diferentes tipos de personas
   - Genere reportes estadísticos
   - Implemente sistema de calificaciones
   - Use propiedades readonly para IDs y fechas de ingreso

Estos ejercicios te permitirán practicar todos los conceptos vistos: herencia, polimorfismo, clases abstractas, propiedades readonly, y manejo avanzado de arrays en TypeScript.