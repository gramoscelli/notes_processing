# Programa del Curso de TypeScript

## Requisitos previos
- Conocimientos de JavaScript/Node u otro lenguaje imperativo.
- NPM/Yarn instalado y uso básico de terminal.

---

## 1) Fundamentos del lenguaje
- ¿Qué es TypeScript? Ventajas y flujo de compilación (TS → JS)
- Instalación, `tsc`, `ts-node`, estructura de proyecto
- `tsconfig.json`: `target`, `module`, `strict`, `lib`, `paths`, `include/exclude`
- Tipos primitivos y especiales: `string`, `number`, `boolean`, `null`, `undefined`, `any`, `unknown`, `never`
- Inferencia de tipos, anotaciones y aserciones (`as`, `as const`, `!`)

## 2) Construcción de tipos
- Objetos, `type` vs `interface`, compatibilidad estructural
- Uniones e intersecciones (`|` y `&`), tipos literales
- Tuplas, `readonly`, `enum` (pros/contras)
- *Narrowing*: `typeof`, `in`, `instanceof`, *type predicates*

## 3) Funciones y clases
- Tipado de funciones: parámetros, retorno, opcionales, *overloads*
- Funciones genéricas y restricciones (`extends`)
- Clases: `public`, `private`, `protected`, `readonly`, `abstract`
- Getters/setters, `implements`, composición vs herencia

## 4) Genéricos y utilidades del tipo
- Genéricos avanzados: `keyof`, `typeof`, *Indexed Access*, *Lookup types*
- *Mapped types* y *Conditional types* (`infer`, distribución)
- *Template Literal Types* y *key remapping*
- Utility Types: `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable`, `ReturnType`, `Parameters`, etc.

## 5) Módulos y organización
- ES Modules vs CommonJS, *module resolution*
- Estructura por capas, *barrels*, alias de rutas (`paths`)
- *Declaration merging* y *module augmentation*
- Creación y consumo de declaraciones `.d.ts`

## 6) Interoperabilidad con JavaScript
- Uso seguro de librerías JS: `@types`, DefinitelyTyped
- Patrones para domar `any` y `unknown`
- Tipos del DOM (cuando aplica)

## 7) Asincronía y manejo de errores
- Promesas, `async/await` y tipado de flujos asíncronos
- Tipos para errores y resultados: `Result/Either`, *exhaustive checks*
- Cancelación y *timeouts* (patrones)

## 8) Calidad, pruebas y *tooling*
- `tsc --noEmit` como verificación de tipos en CI
- ESLint con parser de TS y reglas *type-aware*
- Prettier
- Pruebas con Jest/Vitest en TS (config mínima)
- *Source maps* y depuración

## 9) Build y distribución
- Bundlers/compiladores: esbuild, tsup, Vite (visión general)
- Targets múltiples (Node/Browser), *dual package* (ESM/CJS)
- Publicación de librerías: `types` en `package.json`, *semver*

## 10) Integraciones (elige una o ambas rutas)
### Ruta Frontend (React con TS)
- Tipado de Props/State, eventos y refs
- Componentes genéricos, *context*, *reducers* con *discriminated unions*
- Formularios y *schema validation* (p. ej., Zod) con tipos inferidos
- Patrones comunes: HOCs, *render props*, *hooks* personalizados

### Ruta Backend (Node con TS)
- Express/Fastify: tipado de `Request/Response`, *middlewares*
- Validación de entrada/salida con Zod/TypeBox (tipos como contrato)
- ORM/DB (Prisma/TypeORM) y tipos inferidos
- OpenAPI/Swagger y generación de tipos

## 11) Tipado avanzado y patrones
- *Nominal/Branded types*, *phantom types*
- *State machines* con *discriminated unions*
- *Exhaustiveness checking* y `assertNever`
- *Decorators* (experimental) y `reflect-metadata` (opcional)

## 12) Proyecto final (*capstone*)
- **Propuesta A (Frontend):** SPA en React+TS con validación tipada extremo a extremo
- **Propuesta B (Backend):** API REST en Node+TS con esquemas, pruebas y tipos generados
- **Entregables:** repo con CI (lint+typecheck+tests), documentación breve y *typedoc*

---

## Cronograma sugerido (8–10 semanas)
1. **Sem 1:** Fundamentos + `tsconfig` + tipos básicos  
2. **Sem 2:** Objetos/Interfaces/Uniones + funciones  
3. **Sem 3:** Clases + genéricos (intro)  
4. **Sem 4:** Genéricos avanzados + Utility/Conditional/Mapped  
5. **Sem 5:** Módulos, organización, `.d.ts`, JS interop  
6. **Sem 6:** Asincronía + manejo de errores tipado  
7. **Sem 7:** Tooling (ESLint/Prettier/Tests) + build  
8–10. **Sem 8–10:** Ruta elegida (Frontend o Backend) + Proyecto final

---

## Evaluación y práctica
- Micro-katas por módulo (5–15 min)
- 2 *checkpoints* prácticos (sem 4 y sem 7)
- Revisión por pares del proyecto final con checklist de tipos
