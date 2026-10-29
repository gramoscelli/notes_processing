
#### 1.3 Genéricos: Creando Componentes Reutilizables y Seguros

Los genéricos son una de las herramientas más poderosas de *TypeScript*. Te permiten escribir código (como funciones, clases o tipos) que es flexible y reutilizable, ya que puede operar sobre una variedad de tipos sin sacrificar la seguridad que *TypeScript* ofrece.

*   **¿Qué es un Genérico? El "Variable de Tipo"**

    Piensa en un genérico como un **marcador de posición** o una **variable para un tipo**. En lugar de decidir de antemano qué tipo aceptará tu función, usas un genérico para que el tipo se determine en el momento en que la función es llamada. La sintaxis `<T>` introduce una de estas variables de tipo.

    **Función Genérica Básica:**

    La gran ventaja sobre usar `any` es que mantenemos la seguridad de tipos. `resultadoString` es de tipo `string`, no `any`.

```ts
// La función 'identidad' acepta un argumento 'x' de un tipo 'T'
// y promete devolver un valor del mismo tipo 'T'.
function identidad<T>(x: T): T {
    return x;
}

// Al llamarla, TypeScript infiere el tipo 'T' a partir del argumento:
const resultadoString = identidad("Hola Mundo"); // 'T' es 'string'
const resultadoNumero = identidad(123);        // 'T' es 'number'
``` 

*   **Restricciones Genéricas: Poniendo Límites con `extends`**

    A menudo, necesitas que tu función genérica sepa *algo* sobre el tipo con el que está trabajando. Por ejemplo, que tiene una propiedad `.length`. Las **restricciones** te permiten decirle a *TypeScript*: "El tipo `T` puede ser cualquiera, *siempre y cuando* cumpla con esta forma o contrato".

    **Ejemplo Avanzado: Acceder a una Propiedad de Forma Segura**
```typescript
/**
 * Esta función toma un objeto 'obj' (de tipo 'T') y una clave 'k' (de tipo 'K')
    * y devuelve la propiedad correspondiente.
    *
    * Las restricciones son clave aquí:
    * 1. 'T': Representa el objeto.
    * 2. 'K extends keyof T': Esta es la restricción. Dice que el tipo 'K' DEBE SER
    *    una de las claves ('keyof') del objeto 'T'.
    * 3. Retorno 'T[K]': El tipo de retorno es el "tipo de la propiedad 'K' en 'T'".
    */
function obtenerPropiedad<T, K extends keyof T>(obj: T, k: K): T[K] {
    return obj[k];
}

const usuario = { nombre: "Ana", edad: 30 };
const nombre = obtenerPropiedad(usuario, "nombre"); // Válido. 'nombre' es de tipo 'string'.
const edad = obtenerPropiedad(usuario, "edad");     // Válido. 'edad' es de tipo 'number'.
// const invalido = obtenerPropiedad(usuario, "email"); // ❌ Error: "email" no es una clave de 'usuario'.
```

*   **Parámetros Genéricos por Defecto**

    Al igual que los parámetros de una función, los parámetros genéricos pueden tener un **tipo por defecto**. Esto proporciona un tipo de respaldo si el usuario no especifica uno, haciendo tu código más conveniente.

```typescript
// 'Bolsa' es un tipo genérico que contiene un array de 'T'.
// Si no se especifica 'T', por defecto será 'string'.
type Bolsa<T = string> = {
    items: T[];
};

const bolsaDeCuerdas: Bolsa = { items: ["cuerda1", "cuerda2"] }; // 'T' es 'string' (por defecto)
const bolsaDeNumeros: Bolsa<number> = { items: [1, 2, 3] };   // 'T' es 'number' (especificado)
```


---

#### 1.4 Tipado de `this` en Funciones: Evitando Errores de Contexto

En JavaScript, el valor de `this` es dinámico y una fuente común de errores, especialmente cuando una función se pasa como callback y pierde su contexto original. *TypeScript* ofrece dos mecanismos principales para controlar `this` y asegurar que siempre se use correctamente.

*   **1. Tipado Explícito de `this` (Para Métodos Tradicionales)**

    Para funciones declaradas con la sintaxis tradicional (`function() { ... }` o `metodo() { ... }`), puedes forzar el tipo de `this` añadiéndolo como un "parámetro fantasma" al principio de la lista de argumentos. Este parámetro no existe en el JavaScript compilado, pero le sirve a *TypeScript* como una **restricción de contexto**.

    **¿Para qué sirve?** Garantiza que un método solo pueda ser llamado si su `this` corresponde al tipo que has especificado.

```typescript
type Contador = {
    valor: number;
    // Esta firma EXIGE que 'incrementar' sea llamado en un contexto ('this') de tipo 'Contador'.
    incrementar(this: Contador): void;
};

const miContador: Contador = {
    valor: 0,
    incrementar() {
    this.valor++; // TypeScript sabe que 'this' aquí es de tipo 'Contador'.
    },
};

miContador.incrementar(); // Válido: 'this' es 'miContador'.

// Aquí es donde TypeScript nos protege:
const fn = miContador.incrementar;
// fn(); // ❌ Error: El contexto 'this' de esta llamada es 'undefined' (en modo estricto) y no es de tipo 'Contador'.
```

*   **2. Funciones de Flecha y el `this` Léxico (La Solución Moderna)**

    Las funciones de flecha (`=>`) se comportan de manera diferente: **no tienen su propio `this`**. En su lugar, capturan o "heredan" el `this` del ámbito en el que fueron definidas. A esto se le llama `this` léxico.

    **¿Por qué es útil?** Elimina por completo la necesidad de preocuparse por la pérdida de contexto, haciendo el código más predecible y robusto, especialmente en clases, callbacks o manejadores de eventos (como en React).

    Debido a este comportamiento, **no se puede (ni se necesita) tipar `this` explícitamente en una función de flecha.**

```typescript
class Cronometro {
    segundos = 0;
    
    // Usamos una función de flecha para el método.
    iniciar = () => {
    setInterval(() => {
        // Gracias a la función de flecha, 'this' aquí siempre
        // se referirá a la instancia de la clase 'Cronometro'.
        // No hay riesgo de perder el contexto.
        this.segundos++;
        console.log(this.segundos);
    }, 1000);
    };
}

const miCronometro = new Cronometro();
miCronometro.iniciar();
```


---

### 1.5 Clases en TypeScript: Blueprints con Superpoderes

Las clases en *TypeScript* son la evolución natural de las clases de JavaScript, enriquecidas con un robusto sistema de tipos que permite crear "planos" para objetos de forma segura y escalable.

*   **Modificadores: Controlando la Visibilidad y el Comportamiento**

    Los modificadores son palabras clave que se anteponen a las propiedades y métodos para controlar cómo y desde dónde se pueden acceder.

    *   **`public`**: (Por defecto) Accesible desde cualquier lugar, dentro o fuera de la clase.
    *   **`private`**: Solo accesible **desde dentro** de la misma clase. Ideal para ocultar detalles de implementación.
    *   **`protected`**: Accesible desde dentro de la clase y **desde las clases que la heredan** (subclases), pero no desde fuera.
    *   **`readonly`**: La propiedad solo se puede asignar en el constructor. Una vez asignada, no se puede cambiar, promoviendo la inmutabilidad.

*   **Propiedades de Parámetro: Menos Código, Misma Claridad**

    *TypeScript* ofrece una sintaxis abreviada muy conveniente que te permite declarar e inicializar una propiedad de clase directamente en la firma del constructor.

```typescript
// La forma larga y repetitiva:
class PuntoLargo {
    x: number;
    y: number;
    constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
    }
}

// La forma moderna con propiedades de parámetro:
class Punto {
    // Declara y asigna 'x' e 'y' como propiedades públicas de solo lectura en un solo paso.
    constructor(public readonly x: number, public readonly y: number) {}
}
```

*   **`getters` / `setters` y `override`**

    *   **Getters y Setters**: Permiten ejecutar lógica personalizada al leer o escribir una propiedad. Son útiles para validaciones, cálculos derivados o para exponer una versión controlada de una propiedad privada.
```ts
class Usuario {
private _nombre: string;
private _apellido: string;

constructor(nombre: string, apellido: string) {
    this._nombre = nombre;
    this._apellido = apellido;
}

public get nombreCompleto(): string {
    console.log("-> Se está usando el GETTER para leer el nombre completo.");
    return '${this._nombre} ${this._apellido}';
}
public set nombreCompleto(nuevoNombreCompleto: string) {
    console.log("-> Se está usando el SETTER para cambiar el nombre completo.");
    
    // Lógica de validación: nos aseguramos de que el nombre tenga al menos un espacio.
    if (!nuevoNombreCompleto || nuevoNombreCompleto.indexOf(' ') < 0) {
    console.error("Error: El nombre completo debe contener nombre y apellido.");
    return; // No hacemos ningún cambio si el valor es inválido.
    }

    // Si es válido, separamos el nombre y el apellido y actualizamos las propiedades internas.
    const [nuevoNombre, nuevoApellido] = nuevoNombreCompleto.split(' ');
    this._nombre = nuevoNombre;
    this._apellido = nuevoApellido;
}
}

```

    *   **`override`**: Una palabra clave de seguridad. Al usarla en un método de una subclase, le dices a *TypeScript*: "Tengo la intención de sobrescribir el método de la clase padre". Si te equivocas en el nombre del método, *TypeScript* te dará un error, previniendo bugs difíciles de encontrar.
```ts
// --- 1. La Clase Base (Padre) ---
class Vehiculo {
    constructor(protected marca: string, protected anio: number) {}

    mostrarDetalles(): void {
    console.log('Vehículo base: ${this.marca}, Año: ${this.anio}');
    }
}

// --- 2. La Subclase Correcta (Hija) ---
class Coche extends Vehiculo {
    constructor(marca: string, anio: number, public numeroDePuertas: number) {
    // 'super()' llama al constructor de la clase padre (Vehiculo)
    super(marca, anio);
    }

    /**
    * Usamos 'override' para indicar que estamos sobrescribiendo intencionadamente
    * el método 'mostrarDetalles' de la clase 'Vehiculo'.
    * TypeScript verifica que este método realmente exista en la clase padre.
    */
    override mostrarDetalles(): void {
    // 'super.mostrarDetalles()' nos permite llamar a la implementación original del padre.
    super.mostrarDetalles(); 
    console.log('  -> Detalles del Coche: ${this.numeroDePuertas} puertas.');
    }
}

// --- 3. La Protección de 'override' en Acción ---
// Ahora, imaginemos que cometemos un error de tipeo al intentar sobrescribir.

class Motocicleta extends Vehiculo {
    constructor(marca: string, anio: number, public tieneSidecar: boolean) {
    super(marca, anio);
    }

    // ¡ERROR INTENCIONADO! Escribimos "mostrarDetalle" en singular.
    // Gracias a 'override', TypeScript nos avisa inmediatamente del error.
    // Si quitas 'override', el error desaparece, pero creas un bug silencioso:
    // un método nuevo en lugar de sobrescribir el existente.
    
    /* 
    // DESCOMENTA ESTA SECCIÓN PARA VER EL ERROR DE TYPESCRIPT:
    override mostrarDetalle(): void { 
        // Error: This member cannot have an 'override' modifier because it is not 
        // declared in the base class 'Vehiculo'. Did you mean to write 'mostrarDetalles'?
        console.log("Este método nunca se llamará como esperamos");
    }
    */
}

```

*   **Privacidad Real (`#`) vs. Privacidad de Tipos (`private`)**

    Existen dos formas de declarar propiedades privadas, y la diferencia es crucial:

    *   **`private` (TypeScript)**: Es una construcción de *TypeScript* que solo existe **en tiempo de compilación**. Desaparece en el JavaScript final. Un desarrollador podría, si quisiera, acceder a la propiedad en el JavaScript compilado. Es como un "pacto de caballeros".
    *   **`#` (Campos Privados de JS)**: Es una característica nativa de JavaScript (ECMAScript). La privacidad se mantiene **en tiempo de ejecución**. Si intentas acceder a un campo `#privado` desde fuera de la clase, obtendrás un error real. Es como una puerta con cerradura.

```typescript
class Secreto {
    private secretoSuave = "Esto es un secreto de TypeScript";
    #secretoReal = "Esto es un secreto real de JavaScript";
}

const miSecreto = new Secreto();
// console.log(miSecreto.#secretoReal); // Error en tiempo de ejecución
```
    **Regla general:** Usa `#` para una privacidad robusta y garantizada.

*   **`implements` vs. `abstract`: Definiendo Contratos y Plantillas**

    Ambos ayudan a estandarizar tus clases, pero de maneras diferentes:

    *   **`interface` + `implements` (El Contrato)**: Una `interface` define la "forma" pública que una clase debe tener (qué métodos y propiedades debe exponer). La clase **promete** cumplir con ese contrato usando la palabra clave `implements`. La `interface` no proporciona ninguna implementación.
    *   **`abstract class` (La Plantilla)**: Es una clase a medio construir que no puede ser instanciada directamente. Puede contener métodos y propiedades ya implementados (comportamiento compartido) y también métodos `abstract` (sin implementación) que las clases hijas **están obligadas** a implementar.

```typescript
// El Contrato: Cualquier "Vehículo" debe tener estos métodos.
interface Vehiculo {
    acelerar(velocidad: number): void;
}

class Coche implements Vehiculo {
    acelerar(velocidad: number) { /* ... */ }
}

// La Plantilla: Un "Animal" tiene un método 'mover' compartido,
// pero cada subclase debe definir cómo 'hacerSonido'.
abstract class Animal {
    mover() { console.log("Moviéndose..."); }
    abstract hacerSonido(): void;
}

class Perro extends Animal {
    hacerSonido() { console.log("Guau!"); } // Obligatorio
}
```

---
