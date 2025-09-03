

## Funciones, clases y genéricos (intro)

**Objetivos**

* Tipar funciones (parámetros/retorno/overloads) y clases; genéricos con restricciones.

### 1) Teoría

#### 1.1 Tipado de Funciones en TypeScript

Tipar las funciones es una de las prácticas más importantes en *TypeScript*. Asegura que los datos que entran (parámetros) y los que salen (retorno) tengan la forma correcta, eliminando una gran cantidad de errores comunes.

*   **La Anatomía Básica: Parámetros y Retorno**

    La sintaxis fundamental te permite anotar el tipo de cada parámetro y el tipo del valor que la función devuelve.

    ```typescript
    // Esta función acepta un número (x: number)
    // y promete devolver un string (: string).
    function sumarUnoYFormatear(x: number): string {
      return 'El resultado es: ${x + 1}';
    }
    ```

*   **Flexibilidad en los Parámetros**

    *TypeScript* ofrece varias formas de hacer que los parámetros de una función sean más flexibles.

    *   **Parámetros Opcionales (`?`):** Puedes marcar un parámetro con un `?` para indicar que puede ser omitido al llamar a la función. Si no se proporciona, su valor será `undefined`.
    *   **Valores por Defecto:** Puedes asignar un valor por defecto a un parámetro. Si el argumento no se proporciona, se usará ese valor. *TypeScript* inferirá automáticamente el tipo del parámetro a partir del valor por defecto.
    *   **Parámetros Rest (`...`):** Permiten agrupar un número variable de argumentos en un único array. Debe ser el último parámetro de la función.

    ```typescript
    // name es opcional.
    // prefix tiene un valor por defecto, por lo que su tipo se infiere como string.
    function saludar(name?: string, prefix = "Hola"): string {
      // Usamos el operador ?? (Nullish Coalescing) para dar un valor de respaldo si name es null o undefined.
      return '${prefix}, ${name ?? "mundo"}';
    }
    saludar(); // "Hola, mundo"
    saludar("Ana"); // "Hola, Ana"
    saludar("Juan", "Adiós"); // "Adiós, Juan"
    // Esta función acepta cualquier cantidad de números y los suma.
    function sumarTodos(...numeros: number[]): number {
      return numeros.reduce((total, n) => total + n, 0);
    }
    sumarTodos(1, 2, 3, 4); // Devuelve 10
    ```

*   **Definiendo la Forma de una Función (Tipos de Función)**

    Puedes crear un "tipo" que describa la firma de una función. Esto es extremadamente útil para asegurar que los callbacks o las funciones pasadas como parámetros tengan la forma correcta.

    ```typescript
    // Creamos un tipo genérico que describe una función con un argumento 'A' y un retorno 'R'.
    type FuncionConUnArgumento<A, R> = (argumento: A) => R;
    // 'incrementar' debe cumplir con la forma 'FuncionConUnArgumento<number, number>'.
    const incrementar: FuncionConUnArgumento<number, number> = (n) => n + 1;
    ```

*   **Firmas de Llamada y Construcción (*Call/Construct Signatures*)**

    Este es un concepto avanzado, útil para describir objetos que tienen una doble naturaleza: pueden ser **llamados como una función** y también **instanciados con `new`**.

    ```typescript
    // Este tipo describe algo que es tanto una función como un constructor.
    type Logger = {
      // Firma de llamada (call signature): se puede invocar como 'miLogger("mensaje")'
      (mensaje: string): void;
      
      // Firma de construcción (construct signature): se puede instanciar como 'new miLogger("info")'
      new (nivel: "info" | "warn"): LoggerInstance;
    }
    interface LoggerInstance {
      log(msg: string): void;
    }
    // (El uso real de un tipo como 'Logger' es complejo y se ve más en APIs y librerías).
    ```

---

#### 1.2 Sobrecarga de Funciones (*Overloads*)

La sobrecarga de funciones es una técnica que te permite definir múltiples "firmas" o formas de llamar a una misma función, mientras mantienes una única implementación centralizada.

Piensa en ello como un **menú público** para los consumidores de tu función (las firmas), mientras que la implementación es la **receta única** que la cocina usa para preparar todos los platos.

**¿Por qué usar sobrecargas en lugar de una simple unión de tipos?**

*   **Experiencia de Desarrollo (DX) Mejorada:** *TypeScript* mostrará al desarrollador las diferentes formas de llamar a la función de manera explícita, con autocompletado y documentación específica para cada caso.
*   **Seguridad de Tipos Más Estricta:** Permite crear una relación más precisa entre los tipos de los argumentos de entrada y el tipo del valor de retorno.

**La Estructura: Firmas vs. Implementación**

El patrón siempre consta de dos partes:

1.  **Las Firmas de Sobrecarga (El "Menú" Público):** Una lista de declaraciones de función sin cuerpo. Esto es lo que *TypeScript* muestra al usuario de la función.
2.  **La Implementación (La "Receta" Privada):** Una única función con cuerpo, cuya firma debe ser lo suficientemente general para ser compatible con todas las firmas de sobrecarga. Esta implementación no es visible para el consumidor.

**Ejemplo en Acción:**

```typescript
// --- 1. Las Firmas de Sobrecarga (El "Menú" Público) ---
// El usuario verá que puede llamar a 'format' con un número o con una fecha.
function format(input: number): string;
function format(input: Date): string;

// --- 2. La Firma y Cuerpo de la Implementación (La "Receta" Privada) ---
// Esta firma no es visible externamente. Debe ser compatible con todas las de arriba.
function format(input: number | Date): string {
  // Dentro del cuerpo, usamos "narrowing" para diferenciar los tipos.
  if (typeof input === "number") {
    // TypeScript sabe que 'input' es un número aquí.
    return input.toFixed(2);
  } else {
    // Y aquí, TypeScript sabe que 'input' es un objeto Date.
    return input.toISOString();
  }
}

// El resultado: llamadas más claras y seguras.
const numeroFormateado = format(123.45); // Devuelve "123.45"
const fechaFormateada = format(new Date()); // Devuelve una fecha en formato ISO
```

**La Regla de Oro: Claridad ante Todo**

*   **Usa la sobrecarga** cuando quieras ofrecer una API pública muy clara y cuando el comportamiento de la función cambie significativamente dependiendo de los tipos de entrada.
*   **Evita la sobrecarga** si una simple unión de tipos en los parámetros es suficiente y la lógica interna no es compleja. A veces, una unión es más simple y legible.

---

#### 1.3 Genéricos: Creando Componentes Reutilizables y Seguros

Los genéricos son una de las herramientas más poderosas de *TypeScript*. Te permiten escribir código (como funciones, clases o tipos) que es flexible y reutilizable, ya que puede operar sobre una variedad de tipos sin sacrificar la seguridad que *TypeScript* ofrece.

*   **¿Qué es un Genérico? El "Variable de Tipo"**

    Piensa en un genérico como un **marcador de posición** o una **variable para un tipo**. En lugar de decidir de antemano qué tipo aceptará tu función, usas un genérico para que el tipo se determine en el momento en que la función es llamada. La sintaxis `<T>` introduce una de estas variables de tipo.

    **Función Genérica Básica:**
    ```typescript
    // La función 'identidad' acepta un argumento 'x' de un tipo 'T'
    // y promete devolver un valor del mismo tipo 'T'.
    function identidad<T>(x: T): T {
      return x;
    }

    // Al llamarla, TypeScript infiere el tipo 'T' a partir del argumento:
    const resultadoString = identidad("Hola Mundo"); // 'T' es 'string'
    const resultadoNumero = identidad(123);        // 'T' es 'number'
    ```    
    La gran ventaja sobre usar `any` es que mantenemos la seguridad de tipos. `resultadoString` es de tipo `string`, no `any`.

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

#### 1.6 Composición sobre Herencia: Un Principio de Diseño Clave

En el diseño de software, tanto la herencia como la composición son mecanismos para reutilizar código, pero lo hacen de maneras fundamentalmente diferentes. Un principio de diseño ampliamente aceptado es **"preferir la composición sobre la herencia"** por su flexibilidad y robustez.

*   **Herencia (Relación "es un/a"):**
    La herencia crea una jerarquía rígida y fuertemente acoplada. Cuando una clase `Perro` hereda de `Animal`, se establece que un `Perro` **es un** `Animal`. Esto significa que `Perro` obtiene *todo* el comportamiento de `Animal`, lo quiera o no. Los cambios en la clase padre (`Animal`) pueden romper inesperadamente a las clases hijas (`Perro`), lo que hace que el código sea más frágil.

*   **Composición (Relación "tiene un/a"):**
    La composición es como construir con bloques de LEGO. En lugar de heredar un conjunto de características, construyes objetos complejos combinando piezas más pequeñas e independientes que encapsulan un comportamiento específico. Un `Coche` no *es un* motor, sino que **tiene un** motor. Esta aproximación es mucho más flexible, ya que puedes "conectar" y "desconectar" comportamientos según sea necesario sin afectar a otras partes del sistema.

**Ejemplo Práctico: Composición con Funciones (Patrón Mixin)**

El código que presentaste es un excelente ejemplo de composición funcional. En lugar de una clase `ObjetoConLogger` que hereda de `ObjetoBase`, creamos una función "mixin" que puede **añadir la capacidad de registrar logs a *cualquier* objeto**.

```typescript
// 1. Definimos la "capacidad" que queremos añadir.
// Cualquier objeto que tenga esta forma, "tiene un logger".
type HasLogger = {
  log: (message: string) => void;
};

/**
 * Esta es una función de orden superior que actúa como un "compositor".
 * Toma un objeto genérico 'T' y le añade la capacidad de logging.
 * @param obj El objeto base al que se le añadirá la funcionalidad.
 * @returns Un nuevo objeto que es una combinación del original Y la capacidad de logger.
 */
const withLogger = <T extends object>(obj: T): T & HasLogger => {
  // Usamos el operador de propagación (...) para copiar todas las propiedades del objeto original.
  // Luego, añadimos la nueva propiedad 'log'.
  return {
    ...obj,

    // Esta es la nueva capacidad que estamos "componiendo".
    log: (message: string) => {
      console.log('[LOG]: ${message}');
    },
  };
};

// --- Veamos cómo se usa ---

// Un objeto simple sin ninguna capacidad especial.
const usuario = {
  nombre: "Ana",
  iniciarSesion() {
    console.log('${this.nombre} ha iniciado sesión.');
  },
};

// Usamos nuestra función compositora para crear una versión mejorada del usuario.
const usuarioConLogger = withLogger(usuario);

// Ahora 'usuarioConLogger' tiene tanto sus métodos originales como el nuevo método 'log'.
usuarioConLogger.iniciarSesion();        // Salida: Ana ha iniciado sesión.
usuarioConLogger.log("Intento de inicio de sesión exitoso."); // Salida: [LOG]: Intento de inicio de sesión exitoso.
```

**Ventaja Clave:** Podríamos usar la misma función `withLogger` para añadir esta capacidad a cualquier otro objeto (`Producto`, `Pedido`, etc.), demostrando la increíble flexibilidad y reusabilidad de la composición.
#### 1.7 Operador `satisfies` (validación no-ensanchante)

* Verifica que un valor **cumple** un tipo **sin** cambiar sus literales:

  ```ts
  const routes = {
    home: "/",
    about: "/about"
  } as const satisfies Record<"home"|"about", string>
  ```

---

### 2) Práctica

> Si aún no instalaste **tsup**, hacelo para empaquetar utilidades con `.d.ts`.

```bash
npm i -D tsup
```

Agregá/ajustá scripts en `package.json`:

```json
{
  "scripts": {
    "dev": "ts-node",
    "typecheck": "tsc --noEmit",
    "build": "tsup src/index.ts --format cjs,esm --dts --sourcemap",
    "prepublishOnly": "npm run typecheck && npm run build"
  }
}
```

#### 2.1 Utilidad genérica: `Result<T, E>` (`src/lib/result.ts`)

```ts
export type Ok<T> = { ok: true; value: T }
export type Err<E> = { ok: false; error: E }
export type Result<T, E = Error> = Ok<T> | Err<E>

export const ok = <T>(value: T): Ok<T> => ({ ok: true, value })
export const err = <E>(error: E): Err<E> => ({ ok: false, error })

export const map = <A, B, E>(r: Result<A, E>, f: (a: A) => B): Result<B, E> =>
  r.ok ? ok(f(r.value)) : r

export const flatMap = <A, B, E>(r: Result<A, E>, f: (a: A) => Result<B, E>): Result<B, E> =>
  r.ok ? f(r.value) : r
```

#### 2.2 Funciones genéricas útiles (`src/03-functions.ts`)

```ts
// groupBy con restricciones de clave
export function groupBy<T, K extends PropertyKey>(xs: readonly T[], key: (t: T) => K): Record<K, T[]> {
  return xs.reduce((acc, x) => {
    const k = key(x)
    ;(acc[k] ??= []).push(x)
    return acc
  }, {} as Record<K, T[]>)
}

// pluck: extrae campo K de T
export function pluck<T, K extends keyof T>(xs: readonly T[], k: K): T[K][] {
  return xs.map(x => x[k])
}

// mapValues tipado
export function mapValues<T extends object, R>(obj: T, f: <K extends keyof T>(v: T[K], k: K) => R): { [K in keyof T]: R } {
  const out: any = {}
  for (const k in obj) out[k] = f(obj[k], k as any)
  return out
}

// overloads: format
export function format(x: number): string
export function format(x: Date): string
export function format(x: number | Date): string {
  return typeof x === "number" ? x.toFixed(2) : x.toISOString()
}

// getIn para rutas seguras
export function getIn<T, K1 extends keyof T>(o: T, k1: K1): T[K1]
export function getIn<T, K1 extends keyof T, K2 extends keyof T[K1]>(o: T, k1: K1, k2: K2): T[K1][K2]
export function getIn(o: any, ...ks: PropertyKey[]): any {
  return ks.reduce((acc, k) => (acc == null ? acc : acc[k]), o)
}

// demo
type User = { id: string; age: number; created: Date; name: string }
const users: User[] = [
  { id: "u1", age: 30, created: new Date(), name: "Ada" },
  { id: "u2", age: 25, created: new Date(), name: "Linus" }
]
console.log(groupBy(users, u => (u.age >= 30 ? "30+" : "<30")))
console.log(pluck(users, "name"))
console.log(format(3.14159), format(new Date()))
```

#### 2.3 Clases y repositorio genérico (`src/03-classes.ts`)

```ts
type Id = string | number

export interface Entity { id: Id }
export interface Repository<T extends Entity> {
  add(e: T): T
  get(id: Id): T | undefined
  update(e: T): T
  remove(id: Id): boolean
  all(): readonly T[]
}

export class InMemoryRepo<T extends Entity> implements Repository<T> {
  #data = new Map<Id, T>()
  add(e: T): T { this.#data.set(e.id, e); return e }
  get(id: Id): T | undefined { return this.#data.get(id) }
  update(e: T): T { if (!this.#data.has(e.id)) throw new Error("not found"); this.#data.set(e.id, e); return e }
  remove(id: Id): boolean { return this.#data.delete(id) }
  all(): readonly T[] { return Array.from(this.#data.values()) }
}

export interface Equatable<T> { equals(other: T): boolean }

export class Vec2 implements Equatable<Vec2> {
  constructor(public readonly x: number, public readonly y: number) {}
  static zero() { return new Vec2(0, 0) }
  add(v: Vec2) { return new Vec2(this.x + v.x, this.y + v.y) }
  scale(f: number) { return new Vec2(this.x * f, this.y * f) }
  equals(other: Vec2) { return this.x === other.x && this.y === other.y }
  get length() { return Math.hypot(this.x, this.y) }
}

// Demo
const repo = new InMemoryRepo<Vec2 & Entity>()
repo.add(Object.assign(new Vec2(1,2), { id: "a" }))
repo.add(Object.assign(Vec2.zero(), { id: "b" }))
console.log("repo size:", repo.all().length)
```


---

#### 2.4 Aserciones de Tipo con `asserts`

Las funciones de aserción son una forma de decirle al compilador de *TypeScript*: "**Te garantizo que esta condición es verdadera. Si no lo es, mi programa se detendrá.**"

El principal beneficio es que te permiten crear funciones de validación reutilizables que refinan (o "estrechan") el tipo de una variable para todo el código que sigue a la llamada de la función.

**El Problema Común (Sin Aserción)**

Imagina que tienes que comprobar si una variable es nula en varios lugares:

```typescript
function procesar(valor: string | null) {
  if (valor === null) {
    throw new Error("El valor no puede ser nulo");
  }
  // TypeScript sabe que aquí `valor` es un string
  console.log(valor.toUpperCase());
}
```
Esto funciona, pero si tienes que repetir esta validación en 10 funciones diferentes, se vuelve tedioso. Si lo extraes a una función normal, pierdes el refinamiento de tipo.

**La Solución Elegante con `asserts`**

Una función de aserción encapsula esta lógica y, lo más importante, **comunica el resultado de la validación al compilador**.

**Desglosando el Ejemplo:**

```typescript
// La firma de la función es la clave de todo.
// `asserts x is NonNullable<T>` le dice a TypeScript:
// 1. `asserts`: Esto no es una función normal; es una aserción.
// 2. `x is ...`: Si esta función NO lanza un error, te prometo que el parámetro `x`...
// 3. `... is NonNullable<T>`: ...cumple con el tipo `NonNullable<T>`.
//    (NonNullable<T> es un tipo de utilidad que elimina `null` y `undefined` de `T`).
export function assertPresent<T>(x: T, msg = "valor requerido"): asserts x is NonNullable<T> {
  // La lógica de la aserción: si la condición no se cumple, LANZA UN ERROR.
  // Esto es obligatorio. La función no debe retornar si la aserción falla.
  if (x == null) {
    throw new Error(msg);
  }
}

// --- Poniéndolo en práctica ---

// 1. `maybe` es de tipo `string | null`. TypeScript no puede estar seguro de su valor.
const maybe: string | null = Math.random() > 0.5 ? "ok" : null;

// console.log(maybe.toUpperCase()); // ❌ Error: 'maybe' could be 'null'.

// 2. Llamamos a nuestra función de aserción.
assertPresent(maybe);

// 3. El "milagro" de TypeScript:
// El compilador sabe que si el código ha llegado hasta esta línea, es porque
// `assertPresent` NO lanzó un error. Por lo tanto, la promesa (`asserts x is NonNullable<T>`)
// debe ser cierta. TypeScript ahora trata a `maybe` como si fuera de tipo `string`.
console.log(maybe.toUpperCase()); // ✅ ¡Ahora es válido!
```

**Regla Mental:**

Usa `asserts` para crear funciones de validación que actúan como "guardias". Si la variable pasa la guardia (la función no lanza un error), *TypeScript* confía en que es segura y le aplica un tipo más específico para todo el código que viene después.

#### 2.5 Índice del paquete (`src/index.ts`)

```ts
export * from "./lib/result"
export * from "./03-functions"
export * from "./03-classes"
export * from "./03-asserts"
```

#### 2.6 Comandos útiles

```bash
npm run typecheck
npm run dev src/03-functions.ts
npm run dev src/03-classes.ts
npm run dev src/03-asserts.ts
npm run build
```

---

### 3) Ejercicios para auto-evaluación

1. **Overloads**: Agrega una firma `format(x: string): string` que trate strings como números si es posible y, si no, devuelva el string.
2. **Genéricos**: implementá `uniqueBy<T, K>(xs: T[], key: (t: T) => K): T[]` sin perder tipos.
3. **Repositorio**: Agrega `find(predicate: (t: T) => boolean): T[]` al repo genérico.
4. **Clases**: Añade `normalize()` a `Vec2` que devuelva un nuevo vector de norma 1 (o `this` si es cero).
5. **`satisfies`**: definí un mapa de mensajes `as const` y validalo contra `Record<"ok"|"err", string>`.

