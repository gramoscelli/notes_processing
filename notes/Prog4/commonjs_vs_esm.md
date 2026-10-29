# 🚀 Importación de Módulos en TypeScript con Vite

En esta guía, desglosaremos cómo importar módulos de manera efectiva en tus proyectos TypeScript, especialmente cuando trabajas con la increíble velocidad de Vite. Prepárate para escribir código más limpio, organizado y eficiente.



## 1. 🛠️ Configuración Esencial de TypeScript (`tsconfig.json`)

Para que TypeScript y Vite trabajen en armonía, necesitamos decirle a TypeScript cómo manejar los módulos. Abre tu archivo `tsconfig.json` y asegúrate de que tenga estas configuraciones clave:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] },
    "resolveJsonModule": true,
    "noEmit": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

### ✨ Desglose de los puntos más importantes

*   **`"module": "ESNext"`**: Esto es crucial. Le dice a TypeScript que use la sintaxis moderna de módulos de ECMAScript (ESM), que es la forma preferida y más eficiente de trabajar en el ecosistema actual de JavaScript y TypeScript. Piensa en ello como el "lenguaje universal" de los módulos hoy en día.
    
*   **`"moduleResolution": "bundler"`**: Esta opción le indica a TypeScript que la resolución de módulos será manejada por un *bundler* (como Vite, que usa Rollup internamente). Es la forma más eficiente para que TypeScript entienda cómo el *bundler* encontrará tus archivos.
    
*   **`"esModuleInterop": true`** y **`"allowSyntheticDefaultImports": true`**: Estas dos opciones trabajan juntas para que puedas importar bibliotecas escritas en CommonJS (un sistema de módulos más antiguo, común en Node.js) como si fueran módulos ES. ¡Esto te da mucha flexibilidad!
*   **`"paths": { "@/*": ["src/*"] }`**: ¡Aquí está la magia de los alias! En lugar de escribir rutas relativas largas y complicadas como `./../../utils/myUtils`, puedes usar `@/utils/myUtils`. ¡Tu código se verá mucho más limpio y fácil de mantener!



## 2. ⚡ Configuración de Alias en Vite (`vite.config.ts`)

Para que Vite entienda nuestros alias de `paths` definidos en `tsconfig.json`, también necesitamos configurarlos en su archivo de configuración:

```ts
// vite.config.ts
import { defineConfig } from "vite";
import path from "node:path"; // Módulo nativo de Node.js para trabajar con rutas de archivos

export default defineConfig({
  resolve: {
    alias: {
      // Configuramos el alias "@" para que apunte a la carpeta "src"
      "@": path.resolve(__dirname, "src")
    }
  }
});
```

**¿Cómo se ve esto en acción?**

Imagina que tienes un archivo `util.ts` dentro de `src/utils`. Antes, quizás lo importabas así:

```ts
// src/components/MyComponent.ts
import { util } from "../../utils/util"; // ¡Uff, cuántos puntos y barras!
```

¡Ahora, con el alias, es mucho más elegante!

```ts
// src/components/MyComponent.ts
import { util } from "@/utils/util"; // ¡Mucho más limpio y fácil de leer!
```



## 3. 📚 Las Diferentes Caras de `import`

La palabra clave `import` puede usarse de varias maneras, cada una con su propósito. 

### 3.1. Importación por omisión: La más común para un solo elemento principal

Cuando un módulo tiene una **exportación por defecto**, significa que hay un "elemento principal" que se espera que uses de ese archivo. Solo puede haber uno por módulo.

```ts
// 📁 math.ts
// Esta es la exportación por defecto de este módulo
export default function sumar(a: number, b: number): number {
  return a + b;
}

// 📁 main.ts
// Importamos la función por defecto y le podemos dar el nombre que queramos (aquí 'sumar')
import sumar from "./math"; // La ruta es relativa al archivo actual
console.log(sumar(2, 3)); // Salida: 5
```

### 3.2. Importación con Nombre: Para elementos específicos

Si un módulo exporta varias cosas, puedes elegir importar solo las que necesitas usando sus nombres exactos.

```ts
// 📁 strings.ts
// Exportamos funciones con nombres específicos
export function upper(s: string): string { return s.toUpperCase(); }
export function lower(s: string): string { return s.toLowerCase(); }
export const PI = 3.14159; // También podemos exportar constantes

// 📁 main.ts
// Importamos solo las funciones 'upper' y 'lower'
import { upper, lower } from "./strings";
console.log(upper("hola")); // Salida: HOLA

// Podemos renombrar un import con 'as' si hay conflicto de nombres o queremos un nombre más corto
import { PI as MyPiValue } from "./strings";
console.log(MyPiValue); // Salida: 3.14159
```

### 3.3. Importar todo como un objeto: Cuando quieres agrupar utilidades
Si un módulo exporta muchas cosas con nombre y quieres acceder a ellas bajo un solo "paraguas", puedes importarlas todas como un objeto.

```ts
// 📁 utils.ts
export const PI = 3.14;
export function area(r: number): number { return PI * r * r; }
export function circumference(r: number): number { return 2 * PI * r; }

// 📁 main.ts
// Importamos todo lo exportado por 'utils.ts' y lo ponemos bajo el objeto 'utils'
import * as utils from "./utils";
console.log(utils.area(5));          // Salida: 78.5
console.log(utils.circumference(5)); // Salida: 31.400000000000002
```

### 3.4. Import combinado: Lo mejor de ambos mundos

Puedes importar la exportación por defecto *y* exportaciones con nombre del mismo módulo en una sola línea.

```ts
// 📁 logger.ts
// Exportación por defecto
export default function log(msg: string): void { console.log(msg); }
// Exportación con nombre
export const LEVEL = "INFO";
export const DEBUG_MODE = true;

// 📁 main.ts
import log, { LEVEL, DEBUG_MODE } from "./logger";
log(`Nivel: ${LEVEL}, Modo Debug: ${DEBUG_MODE}`); // Salida: Nivel: INFO, Modo Debug: true
```

### 3.5. `import` solo por efectos: Cuando la carga del módulo ya hace algo

A veces, un módulo no exporta nada, pero su simple carga ejecuta algún código (por ejemplo, configura variables globales, registra un *polyfill* o inicia una conexión).

```ts
// 📁 setup.ts
// Este módulo no exporta nada, pero su ejecución tiene un "efecto secundario"
console.log("🚀 Aplicación: Inicializando configuración global...");

// 📁 main.ts
import "./setup"; // Simplemente carga y ejecuta el código de setup.ts
console.log("¡Todo listo!");

// Salida esperada:
// 🚀 Aplicación: Inicializando configuración global...
// ¡Todo listo!
```

### 3.6. Importación Dinámica: Carga módulos solo cuando los necesitas

Esta es una característica poderosa que te permite cargar módulos de forma asíncrona, solo cuando son necesarios. Es ideal para optimizar el rendimiento de tu aplicación (ej. cargar componentes de una SPA solo cuando el usuario navega a ellos).

```ts
// 📁 math.ts (mismo de antes)
export default function sumar(a: number, b: number): number {
  return a + b;
}

// 📁 main.ts
async function cargarYUsarModulo() {
  console.log("Intentando cargar el módulo 'math'...");
  // El 'import()' devuelve una Promise que se resuelve con el módulo
  const mod = await import("./math");
  console.log("Módulo 'math' cargado.");
  console.log(`La suma de 4 y 5 es: ${mod.default(4, 5)}`); // Accedemos a la exportación por defecto
}

// Llamamos a la función para cargar el módulo dinámicamente
cargarYUsarModulo();

// Salida esperada:
// Intentando cargar el módulo 'math'...
// Módulo 'math' cargado.
// La suma de 4 y 5 es: 9
```

### 3.7. `import` solo de tipos: Exclusivo de TypeScript para optimización

Cuando solo necesitas usar una interfaz o un tipo de otro archivo, pero no su implementación en tiempo de ejecución. Usar `import type` le dice a TypeScript que este import debe ser eliminado completamente cuando el código se compile a JavaScript, ¡lo que ayuda a mantener tu código JS más pequeño!

```ts
// 📁 types.ts
export interface Usuario { id: number; nombre: string; }
export type Rol = "admin" | "editor" | "viewer";

// 📁 main.ts
// Usamos 'import type' porque solo necesitamos las definiciones de tipo, no código JS ejecutable.
import type { Usuario, Rol } from "./types";

const u: Usuario = { id: 1, nombre: "Ana" };
const rolActual: Rol = "admin";

console.log(`Usuario: ${u.nombre}, Rol: ${rolActual}`); // Salida: Usuario: Ana, Rol: admin

// ¡Importante! 'import type' no se transpila a JS.
// Si revisas el JS compilado de main.ts, verás que esta línea ha desaparecido.
```

### 3.8. Importación estilo CommonJS (`import = require`): Para librerías _legacy_ 

Esta sintaxis es una forma de interoperabilidad específica de TypeScript para importar módulos CommonJS (el sistema de módulos que Node.js usaba tradicionalmente) que no se exportan bien con las opciones `esModuleInterop` o `allowSyntheticDefaultImports`. **Úsala solo como último recurso para librerías muy antiguas.**

```ts
// 📁 main.ts
// Usamos 'import = require' para importar el módulo nativo 'fs' (File System) de Node.js,
// que históricamente usa CommonJS.
// Nota: En un proyecto frontend con Vite, 'fs' no estaría disponible directamente en el navegador.
// Este es un ejemplo para ilustrar la sintaxis.
import fs = require("fs");

// Podemos usar las funciones de fs como si fueran un objeto normal
// fs.readFileSync(...);
console.log("Módulo 'fs' importado usando CommonJS style.");
```

## 4. 💡 Recomendaciones Clave para un Código Impecable

Para mantener tu código limpio, eficiente y fácil de entender, sigue estas buenas prácticas:

1.  **Prioriza ESM (`ESNext`)**: Siempre que sea posible, usa la sintaxis moderna de `import` y `export` de ES Modules. Es el estándar actual y el que mejor se integra con herramientas modernas como Vite.
2.  **¡Alias al Rescate (`paths`)!**: Aprovecha los alias en `tsconfig.json` y `vite.config.ts`. Transforman rutas largas y propensas a errores en atajos limpios y descriptivos. Tu carpeta `src` te lo agradecerá.
3.  **`import type` para Tipos Puros**: Cuando solo necesites la definición de una interfaz o un tipo, usa `import type`. TypeScript lo eliminará al compilar, reduciendo el tamaño de tu JavaScript final y mejorando el rendimiento.
4.  **`import = require` solo para la Retaguardia**: Reserva la sintaxis `import = require` para esas raras ocasiones en que una biblioteca antigua de CommonJS no se importa correctamente con las opciones de interoperabilidad estándar. Es una herramienta de compatibilidad, no una práctica diaria.



## 5. 🎯 ¡Manos a la Obra! Ejercicios Prácticos

Crea un nuevo proyecto Vite con TypeScript y resuelve estos ejercicios.

### Ejercicio 1: Módulo de Utilidades Matemáticas

1.  Crea un archivo `src/mathUtils.ts`.
2.  Dentro de `mathUtils.ts`, exporta con nombre una función `sumar(a: number, b: number)` y otra `restar(a: number, b: number)`.
3.  En `src/main.ts` (o cualquier otro archivo), importa **solo la función `sumar`** usando la sintaxis de **importación con nombre**.
4.  Llama a `sumar` con dos números y muestra el resultado en consola.

### Ejercicio 2: Módulo de Configuración por Defecto

1.  Crea un archivo `src/config.ts`.
2.  Dentro de `config.ts`, exporta por defecto un objeto con las propiedades `{ appName: "MiApp", version: "1.0", debug: true }`.
3.  En `src/main.ts`, importa este objeto usando la **importación por defecto**. Dale el nombre `appConfig`.
4.  Muestra `appConfig.appName` y `appConfig.version` en consola.

### Ejercicio 3: Módulo de Constantes con Importación de Espacio de Nombres

1.  Crea un archivo `src/constants.ts`.
2.  Dentro de `constants.ts`, exporta con nombre varias constantes: `PI = 3.14159`, `E = 2.71828`, `GRAVEDAD = 9.81`.
3.  En `src/main.ts`, importa **todas** estas constantes bajo un único objeto llamado `mathConstants` usando la sintaxis `import * as`.
4.  Muestra `mathConstants.PI` y `mathConstants.GRAVEDAD` en consola.

### Ejercicio 4: Módulo con Efectos Secundarios

1.  Crea un archivo `src/initializer.ts`.
2.  Dentro de `initializer.ts`, haz que muestre un mensaje en consola: `"🌐 Conectando a la base de datos..."` y `"✅ Base de datos conectada."`. No exportes nada.
3.  En `src/main.ts`, importa `initializer.ts` usando la **importación solo por efectos**.
4.  Asegúrate de que los mensajes de `initializer.ts` aparezcan en la consola cuando se ejecuta `main.ts`.

### Ejercicio 5: Importación de Tipos Puros

1.  Crea un archivo `src/dataTypes.ts`.
2.  Dentro de `dataTypes.ts`, define y exporta una interfaz `Product { id: number; name: string; price: number; }`.
3.  En `src/main.ts`, importa **solo el tipo `Product`** usando `import type`.
4.  Declara una variable `myProduct` de tipo `Product` y asígnale un objeto con datos de un producto. Muestra el nombre del producto en consola.

### Ejercicio 6: Importación Dinámica Asíncrona

1.  Utiliza el módulo `src/mathUtils.ts` que creaste en el Ejercicio 1.
2.  En `src/main.ts`, crea una función asíncrona llamada `performCalculations()`.
3.  Dentro de `performCalculations()`, usa una **importación dinámica** para cargar el módulo `src/mathUtils.ts`.
4.  Una vez cargado, usa la función `restar` de ese módulo con dos números y muestra el resultado en consola.
5.  Llama a `performCalculations()` para ejecutarla.



## 6. 🧠 Resumen

Ahora tienes una comprensión sólida de cómo funcionan los módulos en TypeScript con Vite.

*   **Vite y TypeScript** se llevan de maravilla con los **ES Modules (`module: ESNext`)**.
*   Las **alias (`paths`)** son tus mejores amigos para un código organizado.
*   Conociste las diferentes **sintaxis de `import`**: por defecto, con nombre, como objeto, combinado, por efectos, dinámica y solo de tipos.
*   Y aprendiste a usar **`import type`** para optimizar tus aplicaciones.
*   Los **ejercicios** te permitieron poner todo en práctica.
