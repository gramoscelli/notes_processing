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
