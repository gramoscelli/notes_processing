## Genéricos avanzados, *utility types* y *conditional/mapped types*

**Objetivos**

* Aplicar `keyof`, *indexed access*, *template literal types*, `infer`.

### 1) Teoría mínima
#### 1.1 `keyof`, Indexed Access y Lookup Types: Inspeccionando Tipos

*TypeScript* proporciona un conjunto de operadores que nos permiten "inspeccionar" la estructura de otros tipos. Esto es fundamental para crear utilidades genéricas y seguras que puedan operar sobre objetos sin conocer sus propiedades de antemano.

*   **`keyof`: Obteniendo las Llaves del Tipo**

    El operador `keyof` toma un tipo de objeto `T` y produce un nuevo tipo que es una **unión de strings literales** de todas sus claves (propiedades) públicas. Piensa en él como si pidieras el "menú de propiedades" disponibles en un tipo.

```typescript
type User = {
  id: string;
  age: number;
  created: Date;
};

// `keyof User` inspecciona el tipo `User` y devuelve una unión de sus claves.
type UserKeys = keyof User; // El tipo resultante es: "id" | "age" | "created"
```

*   **`T[K]`: Consultando el Tipo de una Propiedad (Indexed Access Types)**

    Una vez que tienes la "llave" de una propiedad, puedes usar la sintaxis de corchetes `T[K]` para "buscar" y obtener el **tipo** de esa propiedad específica. A esto se le conoce como *Indexed Access Type* o *Lookup Type*.

```typescript
// Usamos una de las claves de `User` (un string literal) para consultar su tipo.
type AgeType = User["age"];     // El tipo resultante es `number`
type IdType = User["id"];       // El tipo resultante es `string`
```

*   **Poniéndolo Todo Junto: El Patrón en Acción**

    La verdadera magia ocurre cuando combinas `keyof` y `T[K]` para crear funciones genéricas seguras. El uso más común es para una función que accede a una propiedad de un objeto de forma segura.

```typescript
/**
 * Esta función genérica toma un objeto `obj` (de tipo `T`) y una clave `key` (de tipo `K`).
  *
  * La restricción `K extends keyof T` es crucial:
  * Asegura que el argumento `key` SÓLO pueda ser una de las claves válidas del objeto `obj`.
  *
  * El tipo de retorno `T[K]` garantiza que el tipo de salida coincida
  * perfectamente con el tipo de la propiedad que se está accediendo.
  */
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// --- Viéndolo funcionar ---
const user: User = {
  id: "user-123",
  age: 30,
  created: new Date(),
};

// `age` es de tipo `number` porque TypeScript infiere que T[K] es User["age"], que es `number`.
const age = getProperty(user, "age");

// `created` es de tipo `Date`.
const creationDate = getProperty(user, "created");

// const invalid = getProperty(user, "email"); // ❌ Error: Argument of type '"email"' is not 
                                              // assignable to parameter of type 'keyof User'.
```


#### 1.2 Mapped Types: Creando Nuevos Tipos a Partir de Otros

Piensa en los *Mapped Types* como un bucle `for...in` que opera sobre los **tipos** en lugar de sobre los valores. Te permiten tomar un tipo existente y, de forma programática, crear un nuevo tipo aplicando transformaciones a cada una de sus propiedades. Son como una "fábrica" para generar nuevos tipos.

**La Anatomía de un Mapped Type**

La sintaxis básica es una plantilla que itera sobre las claves de otro tipo.

```typescript
// La sintaxis `[K in keyof T]` se puede leer como:
// "Para cada clave `K` en el tipo `T`..."
type Mapped<T> = {
  [K in keyof T]: T[K] // "...la nueva propiedad `K` tendrá el tipo del valor original `T[K]`"
};
```

Los famosos tipos de utilidad `Readonly<T>` y `Partial<T>` son implementaciones perfectas de este patrón:

```typescript
// `Readonly<T>`: Añade el modificador `readonly` a cada propiedad.
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

// `Partial<T>`: Hace que cada propiedad sea opcional con `?`.
type Partial<T> = {
  [K in keyof T]?: T[K];
};

type User = { name: string; age: number };
type ReadonlyUser = Readonly<User>; // { readonly name: string; readonly age: number; }
type PartialUser = Partial<User>;   // { name?: string; age?: number; }
```

**Modificadores de Mapeo: Añadiendo o Quitando `readonly` y `?`**

Puedes controlar explícitamente si una propiedad debe ser opcional o de solo lectura usando los prefijos `+` (añadir) y `-` (quitar). Si no se usa prefijo, `+` es el valor por defecto.

```typescript
// `Required<T>` es lo opuesto a `Partial<T>`. Quita el `?` de cada propiedad.
type Required<T> = {
  // El modificador `-?` elimina la opcionalidad.
  [K in keyof T]-?: T[K];
};

type PartialUser = { name?: string; age?: number };
type RequiredUser = Required<PartialUser>; // { name: string; age: number; }
```

**Re-mapeo de Claves con `as`: Filtrando y Renombrando Propiedades**

Esta es la parte más poderosa. Usando la cláusula `as` dentro de un *Mapped Type*, puedes cambiar el **nombre de las claves** o incluso **filtrarlas** por completo.

La técnica de filtrado se basa en un tipo condicional: si la condición se cumple, mantienes la clave; si no, la "descartas" devolviendo `never`.

**Ejemplo: Crear un tipo que solo contenga las propiedades de tipo `string`**

```typescript
type UserWithMixedTypes = {
  name: string;
  age: number;
  email: string;
  isActive: boolean;
};

// Este Mapped Type filtra las claves.
type StringPropertiesOnly<T> = {
  // `as T[K] extends string ? K : never` es la clave del filtrado.
  // Se lee como:
  // "Para cada clave `K` en `T`..."
  // "...si el tipo del valor `T[K]` es un `string`..."
  // "...entonces (`?`) usa `K` como el nombre de la nueva clave..."
  // "...de lo contrario (`:`), descarta esta clave (`never`)."
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

// `FilteredUser` solo contendrá las propiedades `name` y `email`.
type FilteredUser = StringPropertiesOnly<UserWithMixedTypes>;
// El tipo resultante es: { name: string; email: string; }
```

#### 1.3 Conditional Types: El Operador Ternario para Tipos

Piensa en los tipos condicionales como el operador ternario de JavaScript (`condicion ? valorSiVerdadero : valorSiFalso`), pero para el sistema de tipos. Te permiten crear un tipo que cambia basándose en si otro tipo cumple una cierta condición.

**La Forma General: `T extends U ? X : Y`**

La sintaxis se lee de la siguiente manera:
*"Si el tipo `T` es asignable al tipo `U`, entonces el tipo resultante es `X`; de lo contrario, el tipo resultante es `Y`."*

```typescript
// Un ejemplo simple para ilustrar la lógica.
type EsUnString<T> = T extends string ? "Sí, es un string" : "No, no es un string";

type Caso1 = EsUnString<string>; // El tipo resultante es "Sí, es un string"
type Caso2 = EsUnString<number>; // El tipo resultante es "No, no es un string"
```

**La Magia de la Distribución sobre Uniones**

Aquí es donde los tipos condicionales realmente brillan. Si el tipo a la izquierda de `extends` (en nuestro caso, `T`) es una **variable de tipo genérica "desnuda"** (es decir, no está envuelta en otro tipo como `T[]` o `{ prop: T }`) y le pasas una **unión**, el tipo condicional se **distribuye** sobre cada miembro de esa unión.

En otras palabras, la operación se aplica a cada miembro de la unión por separado, y los resultados se vuelven a unir en una nueva unión.

```typescript
// `T` es un genérico "desnudo".
type AArray<T> = T extends any ? T[] : never;

// Cuando pasamos `string | number` a `AArray`, TypeScript lo descompone:
// 1. Aplica `AArray` a `string` -> `string[]`
// 2. Aplica `AArray` a `number` -> `number[]`
// 3. Recombina los resultados en una nueva unión.
type Resultado = AArray<string | number>; // El tipo resultante es: string[] | number[]
```

Para evitar este comportamiento de distribución, puedes "envolver" el genérico en ambos lados de `extends`:
```typescript
type AArraySinDistribuir<T> = [T] extends [any] ? T[] : never;
type ResultadoSinDistribuir = AArraySinDistribuir<string | number>; // El tipo es: (string | number)[]
```

**Extrayendo Tipos con `infer`**

La palabra clave `infer` se puede usar dentro de los tipos condicionales para "declarar" una nueva variable de tipo que captura una parte del tipo que se está comprobando. Es una herramienta increíblemente poderosa para "extraer" tipos anidados.

```typescript
// `ReturnType<T>` es una utilidad nativa que extrae el tipo de retorno de una función.
// Así es como funciona por dentro:
type MiReturnType<T> = T extends (...args: any[]) => infer R ? R : any;
// Se lee como: "Si `T` tiene la forma de una función,
// INFIERE su tipo de retorno en una nueva variable `R`, y usa `R` como resultado".

type MiFuncion = () => string;
type TipoDeRetorno = MiReturnType<MiFuncion>; // El tipo resultante es `string`
```

**La Base de las Utilidades Nativas**

Muchos de los tipos de utilidad más útiles de *TypeScript* están construidos con tipos condicionales.

*   **`Exclude<T, U>`**: De la unión `T`, excluye los miembros que son asignables a `U`.
```typescript
// Definición interna:
// type Exclude<T, U> = T extends U ? never : T;
type Letras = "a" | "b" | "c";
type LetrasSinA = Exclude<Letras, "a">; // El tipo es "b" | "c"
```
*   **`Extract<T, U>`**: De la unión `T`, extrae solo los miembros que son asignables a `U`.
*   **`NonNullable<T>`**: Excluye `null` y `undefined` de `T`.
¡Por supuesto! La palabra clave `infer` es como una herramienta de "deconstrucción" para los tipos. Desbloquea patrones de programación de tipos muy avanzados.



#### 1.4 `infer`: Capturando Tipos Dentro de Otros Tipos

La palabra clave `infer` es una herramienta avanzada que se usa exclusivamente dentro de los tipos condicionales (`T extends U ? X : Y`). Su propósito es **"inferir" o "capturar"** una parte del tipo que estás comprobando y almacenarla en una nueva variable de tipo temporal.

Piensa en ello como una expresión regular que, además de verificar si un string coincide con un patrón, también te permite **capturar y extraer partes de ese string**.

**La Sintaxis: `... infer R ...`**

Cuando usas `infer R`, le estás diciendo a *TypeScript*: "Si el tipo que estoy comprobando coincide con esta estructura, por favor, toma la parte del tipo que está en la posición de `R` y ponla en una nueva variable de tipo llamada `R` que pueda usar en la rama 'verdadera' de mi condicional".

**Ejemplo 1: Extrayendo el Tipo de Retorno de una Función**

Este es el caso de uso canónico. Queremos crear una utilidad `ReturnType<T>` que pueda tomar un tipo de función y devolvernos solo su tipo de retorno.

```typescript
// `T extends (...args: any) => infer R` es el patrón que queremos hacer coincidir.
// Se lee como: "Si `T` es una función..."
// `... infer R`: "...infiere su tipo de retorno y ponlo en una variable `R`."
// `? R`: "Si coincide, el resultado de este tipo condicional es `R`."
// `: never`: "Si no coincide, el resultado es `never`."
type Return<T> = T extends (...args: any) => infer R ? R : never;

// --- Viéndolo en acción ---
type MiFuncion = (nombre: string, edad: number) => boolean;

// TypeScript hace coincidir `MiFuncion` con el patrón:
// (...args: any) => infer R  =>  (nombre: string, edad: number) => boolean
// Y captura `boolean` en la variable `R`.
type ElTipoDeRetorno = Return<MiFuncion>; // El tipo resultante es `boolean`
```

**Ejemplo 2: Desenvolviendo el Tipo de una Promesa**

Otro patrón muy común es querer obtener el tipo del valor que una `Promise` resolverá.

```typescript
// `T extends Promise<infer U>` es el patrón.
// Se lee como: "Si `T` es una `Promise`..."
// `... infer U`: "...infiere el tipo genérico con el que fue creada y ponlo en `U`."
// `? U`: "Si coincide, el resultado es `U`."
// `: T`: "Si no coincide (no es una promesa), simplemente devuelve el tipo original `T`."
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

// --- Viéndolo en acción ---
type PromesaDeString = Promise<string>;
type PromesaDeNumero = Promise<number>;
type UnNumeroSimple = number;

// `U` se infiere como `string`.
type ValorResuelto1 = UnwrapPromise<PromesaDeString>; // El tipo es `string`

// `U` se infiere como `number`.
type ValorResuelto2 = UnwrapPromise<PromesaDeNumero>; // El tipo es `number`

// No coincide con el patrón `Promise<...>`.
type ValorResuelto3 = UnwrapPromise<UnNumeroSimple>; // El tipo es `number` (la rama "falsa")
```

#### 1.5 Template Literal Types: Manipulando Strings en el Sistema de Tipos

Los *Template Literal Types* llevan el poder de las plantillas de string de JavaScript (las que usan backticks ` `` `) directamente al sistema de tipos. Esto te permite crear tipos de string dinámicos, complejos y extremadamente específicos, lo que abre la puerta a patrones de validación muy avanzados.

**1. Componiendo Tipos de String**

En su forma más básica, puedes usarlos para construir nuevos tipos de string literal combinando otros tipos.

```typescript
// Este tipo genérico toma un string `P` y lo concatena dentro de un patrón.
type Route<P extends string> = `/api/v1/${P}`;

// Al usarlo, creamos un tipo de string literal específico y seguro.
type UserRoute = Route<"users">; // El tipo es exactamente "/api/v1/users"
type ProductRoute = Route<"products">; // El tipo es exactamente "/api/v1/products"

// const invalidRoute: UserRoute = "/api/v1/products"; // ❌ Error: Los tipos no coinciden.
```

**2. Manipulando Strings con Utilidades Nativas**

*TypeScript* incluye un conjunto de tipos de utilidad para realizar transformaciones comunes en los strings, como cambiar a mayúsculas o minúsculas.

*   `Capitalize<S>`: Pone en mayúscula el primer carácter.
*   `Uppercase<S>`: Pone todo el string en mayúsculas.
*   `Lowercase<S>`: Pone todo el string en minúsculas.
*   `Uncapitalize<S>`: Pone en minúscula el primer carácter.

```typescript
type Saludo = "hello world";

type SaludoCapitalizado = Capitalize<Saludo>; // El tipo es "Hello world"
type SaludoEnMayusculas = Uppercase<Saludo>; // El tipo es "HELLO WORLD"
```

**3. Extrayendo Patrones con `infer`**

Aquí es donde reside el verdadero poder. Puedes combinar los *Template Literal Types* con los tipos condicionales (`extends`) y la palabra clave `infer` para **deconstruir y capturar partes de un tipo de string**.

Piensa en ello como una expresión regular para el sistema de tipos.

**Ejemplo: Dividir un tipo de string por un guion**

```typescript
/**
 * Este tipo intenta dividir un string `S` en dos partes usando un guion como separador.
 *
 * La lógica `S extends `${infer A}-${infer B}`` se lee como:
 * "Si el tipo `S` coincide con el patrón de 'un_texto-otro_texto'..."
 *
 * `infer A`: "...captura la parte antes del guion en una nueva variable de tipo `A`."
 * `infer B`: "...y captura la parte después del guion en una nueva variable de tipo `B`."
 *
 * `? [A, B]`: "Si coincide, el resultado es una tupla con las dos partes capturadas."
 * `: [S]`: "Si no coincide, el resultado es una tupla con el string original."
 */
type SplitByDash<S extends string> = S extends `${infer A}-${infer B}` ? [A, B] : [S];

// --- Viéndolo en acción ---
type Result1 = SplitByDash<"user-profile">; // El tipo es ["user", "profile"]
type Result2 = SplitByDash<"dashboard">;    // El tipo es ["dashboard"] (no coincide el patrón)
type Result3 = SplitByDash<"id-name-role">; // El tipo es ["id", "name-role"] (solo divide en el primer guion)
```

¡Excelente! El re-mapeo de claves con `as` es la culminación de varias características avanzadas de *TypeScript* (Mapped Types, Conditional Types, Template Literals). Es una herramienta increíblemente poderosa para transformar la "forma" de los tipos de objeto.

#### 1.6 Key Remapping Avanzado con `as`

El re-mapeo de claves, habilitado por la cláusula `as` dentro de un *Mapped Type*, te da control total sobre las claves del nuevo tipo que estás creando. Te permite realizar dos operaciones principales: **renombrar** claves existentes o **filtrarlas** para eliminarlas por completo.

##### 1.6.1 Renombrar Claves

Puedes usar `as` junto con *Template Literal Types* para generar nuevos nombres de clave de forma programática.

**Ejemplo: Crear un tipo que añade un prefijo a todas las claves**

Imagina que quieres tomar un tipo `User` y crear un nuevo tipo donde cada propiedad esté prefijada con `user_` (por ejemplo, `name` se convierte en `user_name`).

```typescript
/**
 * Este tipo genérico toma un tipo `T` y un prefijo `P` (un string).
 * Luego, crea un nuevo tipo donde cada clave `K` de `T` es renombrada.
 */
type PrefixKeys<T, P extends string> = {
  // `as `${P}${Extract<K, string>}`` es la cláusula de renombrado.
  // Se lee como: "Para cada clave `K` en `T`, el nuevo nombre de la clave será..."
  // "...el prefijo `P` seguido del nombre de la clave `K`."
  //
  // (Nota: `Extract<K, string>` es una medida de seguridad para asegurar que solo
  // trabajamos con claves de tipo string, ya que `keyof` puede incluir numbers o symbols).
  [K in keyof T as `${P}${Extract<K, string>}`]: T[K];
};

// --- Viéndolo en acción ---
type User = {
  name: string;
  id: number;
};

// Creamos un nuevo tipo usando `PrefixKeys`.
type PrefixedUser = PrefixKeys<User, "user_">;

// El tipo resultante de `PrefixedUser` es:
// {
//   user_name: string;
//   user_id: number;
// }
```

##### 1.6.2 Filtrar Claves

El verdadero poder del re-mapeo se revela cuando lo combinas con tipos condicionales. Al mapear una clave a `never`, le dices a *TypeScript* que **descarte esa clave por completo** del tipo resultante.

**Ejemplo: Crear un tipo que elimina todas las propiedades que comienzan con un guion bajo**

Este es un caso de uso común para crear un tipo "público" a partir de un tipo que contiene propiedades "privadas" (convencionalmente prefijadas con `_`).

```typescript
/**
 * Este tipo genérico toma un tipo `T` y elimina cualquier clave que
 * comience con un guion bajo.
 */
type RemoveUnderscoreProperties<T> = {
  // La cláusula `as` ahora contiene un tipo condicional para filtrar.
  // Se lee como: "Para cada clave `K` en `T`..."
  // "...si `K` coincide con el patrón de un string que empieza por `_` (`_${string}`)..."
  // "...entonces (`?`) descarta esta clave (`never`)..."
  // "...de lo contrario (`:`), mantén el nombre original de la clave (`K`)."
  [K in keyof T as K extends `_${string}` ? never : K]: T[K];
};

// --- Viéndolo en acción ---
type UserWithInternalProperties = {
  id: string;
  name: string;
  _passwordHash: string; // Propiedad "privada" que queremos eliminar.
  _sessionToken: string; // Otra propiedad "privada".
};

// Aplicamos el filtro para obtener solo la vista pública del usuario.
type PublicUser = RemoveUnderscoreProperties<UserWithInternalProperties>;

// El tipo resultante de `PublicUser` es:
// {
//   id: string;
//   name: string;
// }
// Las propiedades `_passwordHash` y `_sessionToken` han sido eliminadas.
```

#### 1.7 Utility Types: La Caja de Herramientas de TypeScript

*TypeScript* viene con una "caja de herramientas" de tipos genéricos predefinidos, llamados *Utility Types*, diseñados para realizar transformaciones de tipos comunes. En lugar de reescribir la misma lógica de *Mapped* o *Conditional Types* una y otra vez, puedes usar estas utilidades para que tu código sea más conciso y expresivo.

A continuación, se presenta un panorama de los más importantes, agrupados por su función:

##### 1. Modificadores de Propiedades de Objetos

Estos tipos cambian la naturaleza de las propiedades de un tipo de objeto.

*   **`Partial<T>`**: Hace que todas las propiedades de `T` sean opcionales (`?`).
*   **`Required<T>`**: Hace que todas las propiedades de `T` sean requeridas (elimina `?`).
*   **`Readonly<T>`**: Hace que todas las propiedades de `T` sean de solo lectura (`readonly`).
*   **`Record<K, T>`**: Crea un tipo de objeto con un conjunto de claves `K` (generalmente una unión de strings) donde cada clave tiene el tipo `T`.

```typescript
type User = { name: string; age?: number };

type PartialUser = Partial<User>; // { name?: string; age?: number; }
type RequiredUser = Required<User>; // { name: string; age: number; }
```

##### 2. Subconjuntos de Propiedades de Objetos

Estos tipos te permiten crear nuevos tipos seleccionando u omitiendo propiedades de otro.

*   **`Pick<T, K>`**: Crea un tipo seleccionando solo un subconjunto de claves `K` del tipo `T`.
*   **`Omit<T, K>`**: Crea un tipo omitiendo un subconjunto de claves `K` del tipo `T`.

```typescript
type User = { id: string; name: string; email: string };

type UserWithIdAndName = Pick<User, "id" | "name">; // { id: string; name: string; }
type UserWithoutEmail = Omit<User, "email">;      // { id: string; name: string; }
```

##### 3. Manipulación de Uniones

Estos tipos operan sobre tipos de unión, permitiéndote filtrarlos.

*   **`Exclude<T, U>`**: De la unión `T`, excluye todos los miembros que son asignables a `U`.
*   **`Extract<T, U>`**: De la unión `T`, extrae solo los miembros que son asignables a `U`.
*   **`NonNullable<T>`**: Excluye `null` y `undefined` del tipo `T`.

```typescript
type Status = "success" | "loading" | "error" | null;

type NetworkStatus = Exclude<Status, "error" | null>;      // "success" | "loading"
type NullableStatus = Extract<Status, "error" | null>;     // "error" | null
type DefiniteStatus = NonNullable<Status>;                 // "success" | "loading" | "error"
```

##### 4. Introspección de Funciones y Clases

Estos tipos te permiten extraer "meta-información" de los tipos de funciones y constructores.

*   **`Parameters<T>`**: Extrae los tipos de los parámetros de una función `T` como una tupla.
*   **`ReturnType<T>`**: Extrae el tipo de retorno de una función `T`.
*   **`InstanceType<T>`**: Extrae el tipo de la instancia de una clase constructora `T`.

```typescript
type MiFuncion = (id: number, name: string) => boolean;

type MisParametros = Parameters<MiFuncion>; // [number, string]
type MiTipoDeRetorno = ReturnType<MiFuncion>; // boolean
```

---

**El Camino hacia la Maestría**

La idea fundamental es que **puedes recrear la mayoría de estas utilidades** usando las herramientas que hemos visto (*Mapped Types*, *Conditional Types*, `keyof`, `infer`, etc.). Hacerlo es el mejor ejercicio para comprender profundamente su semántica y cómo funciona el sistema de tipos de *TypeScript*.

> En la práctica, combinaremos todas estas piezas para crear nuestras propias **utilidades de tipos reutilizables** y específicas para nuestro dominio. Esto nos permite construir APIs de tipos robustas, seguras y auto-documentadas, validando su comportamiento con técnicas de "tests de tipos" para garantizar que nuestras transformaciones complejas siempre funcionen como se espera.



### 2) Práctica

> Usaremos archivos `src/04-*.ts`. Ejecutá `npm run typecheck` con frecuencia.

#### 2.1 Utilidades básicas de mapeo (`src/types/04-utilities.ts`)

```ts
// Quitar readonly y opcionales
type Mutable<T> = { -readonly [K in keyof T]-?: T[K] }

// Hacer opcionales solo algunas claves
export type OptionalBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

// Hacer requeridas solo algunas claves
export type RequiredBy<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>

// Profundidad recursiva: DeepPartial y DeepReadonly
export type DeepPartial<T> = T extends object ? { [K in keyof T]?: DeepPartial<T[K]> } : T
export type DeepReadonly<T> = T extends object ? { readonly [K in keyof T]: DeepReadonly<T[K]> } : T

// Marcas nominales (branded types)
export type Brand<T, B extends string> = T & { readonly __brand: B }

// Filtrar por tipo de valor
export type PickByValue<T, V> = { [K in keyof T as T[K] extends V ? K : never]: T[K] }
export type OmitByValue<T, V> = { [K in keyof T as T[K] extends V ? never : K]: T[K] }

// Expandir para mejorar DX en tooltips
export type Expand<T> = T extends infer O ? { [K in keyof O]: O[K] } : never
```

#### 2.2 Condicionales e `infer` (`src/04-conditional-infer.ts`)

```ts
// Unwrappers comunes
export type UnwrapPromise<T> = T extends Promise<infer U> ? U : T
export type ElementType<T> = T extends readonly (infer U)[] ? U : never

// Retorno de funciones síncronas y asíncronas	export type AsyncReturn<T> = T extends (...args: any) => Promise<infer R> ? R : T extends (...args: any) => infer R ? R : never

// Obtener claves cuyo valor coincide con V
export type KeysByValue<T, V> = { [K in keyof T]-?: T[K] extends V ? K : never }[keyof T]

// Acceso por ruta string: Get<T, "a.b.c">
export type Get<T, P extends string> = P extends `${infer K}.${infer R}`
  ? K extends keyof T
    ? Get<T[K], R>
    : never
  : P extends keyof T
    ? T[P]
    : never

// Tests básicos
interface User { id: string; meta: { tags: string[]; flags?: number } }
export type T1 = ElementType<User["meta"]["tags"]> // string
export type T2 = Get<User, "meta.flags">            // number | undefined
```

#### 2.3 Template literals y remapeo (`src/04-template-remap.ts`)

```ts
// Camelizar strings tipo "user_name" -> "userName"
export type ToCamel<S extends string> = S extends `${infer H}_${infer T}`
  ? `${Lowercase<H>}${Capitalize<ToCamel<T>>}`
  : Lowercase<S>

// Camelizar claves de un objeto
export type Camelize<T> = { [K in keyof T as K extends string ? ToCamel<K> : K]: T[K] }

// Prefijar claves
export type PrefixKeys<T, P extends string> = { [K in keyof T as `${P}${Extract<K, string>}`]: T[K] }

// Filtrar nullish vía remapeo
export type NonNullishProps<T> = { [K in keyof T as null extends T[K] | undefined ? never : K]: T[K] }

// Demo
type Raw = { user_name: string; created_at: string; count: number | null }
export type Clean = Camelize<Raw> // { userName: string; createdAt: string; count: number | null }
export type CleanNN = NonNullishProps<Clean> // quita 'count' si es nullish
```

#### 2.4 *Utility types* en acción (`src/04-utility-demo.ts`)

```ts
// Estándar de TS
type User = { id: string; name: string; email?: string }

export type U1 = Partial<User>
export type U2 = Required<User>
export type U3 = Readonly<User>
export type U4 = Pick<User, "id" | "name">
export type U5 = Omit<User, "email">
export type U6 = Record<"admin" | "viewer", User>
export type U7 = Exclude<"a" | "b" | "c", "b">      // "a" | "c"
export type U8 = Extract<"a" | "b" | "c", "b" | "x"> // "b"
export type U9 = NonNullable<string | null | undefined>   // string

function makeUser(id: string, name: string) { return { id, name } }
export type Ret = ReturnType<typeof makeUser>
export type Params = Parameters<typeof makeUser>
```

#### 2.5 “Tests de tipos” (`src/04-type-tests.ts`)

```ts
// Pequeño framework de assertions de tipos
export type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false
export type Expect<T extends true> = T

// Casos de prueba
import type { DeepPartial, DeepReadonly, OptionalBy, RequiredBy, Brand } from "./types/04-utilities"
import type { ToCamel, Camelize } from "./04-template-remap"
import type { UnwrapPromise, ElementType, Get } from "./04-conditional-infer"

type E1 = Expect<Equal<UnwrapPromise<Promise<number>>, number>>
type E2 = Expect<Equal<ElementType<readonly [1,2,3]>, 1 | 2 | 3>>
type E3 = Expect<Equal<Get<{ a: { b: 1 } }, "a.b">, 1>>

type P = { a: { b: string[] } }
type DP = DeepPartial<P>
// @ts-expect-error: debería permitir undefined en niveles profundos
const x: P = {} as DP

// Brands
type UserId = Brand<string, "UserId">
const id = "u1" as UserId
// @ts-expect-error: string sin brand no es UserId
const id2: UserId = "u2"
```

---

### 3) Ejercicios opcionales

1. **`PickByValue`/`OmitByValue`**: aplicalos a un tipo `Config` y justificá cuándo conviene remapear claves a `never`.
2. **`Get<T, P>`**: extendelo para aceptar hasta 4 niveles (`a.b.c.d`).
3. **`ToCamel` + `Camelize`**: agregá soporte para claves con múltiples guiones bajos consecutivos.
4. **`DeepReadonly`**: agregá una variante que no afecte arrays a nivel profundo.
5. **`KeysByValue<T, V>`**: usalo para construir un `Subtipo<T, V>` que **solo** conserve las propiedades con valor `V`.

---

### 4) Comandos útiles

```bash
npm run typecheck
npm run dev -- src/04-utility-demo.ts
npm run dev -- src/04-conditional-infer.ts
npm run dev -- src/04-template-remap.ts
```
