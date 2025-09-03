# Problema frecuente al crear relaciones en Neo4j

Cuando se crean nodos y relaciones en Neo4j, es habitual pensar que las variables declaradas en un bloque `CREATE` permanecen disponibles para otras sentencias posteriores. Sin embargo, **las variables solo existen dentro de la misma sentencia Cypher**.

Por ejemplo:

```cypher
CREATE (juan:Persona {nombre: 'Juan'});
CREATE (maria:Persona {nombre: 'María'});
CREATE (juan)-[:AMIGO_DE]->(maria);
```

Este bloque **no funciona como se espera**, porque en la tercera línea las variables `juan` y `maria` **no tienen valor**. Neo4j interpreta esa instrucción como "crear dos nodos nuevos sin etiquetas ni propiedades, y crear la relación entre ellos".

Por eso, aparecen nodos adicionales sin información.

**Cómo se soluciona**

Para referenciar correctamente nodos que ya existen, hay dos opciones principales:

1. **Usar MATCH para seleccionar los nodos existentes antes de crear relaciones**

```cypher
CREATE (:Persona {nombre: 'Juan'});
CREATE (:Persona {nombre: 'María'});

MATCH (juan:Persona {nombre: 'Juan'}), (maria:Persona {nombre: 'María'})
CREATE (juan)-[:AMIGO_DE]->(maria);
```

2. **Crear todo en una sola instrucción CREATE**, donde las variables permanecen vivas dentro de la misma sentencia:

```cypher
CREATE 
  (juan:Persona {nombre: 'Juan'}),
  (maria:Persona {nombre: 'María'}),
  (juan)-[:AMIGO_DE]->(maria);
```

**Recomendación general**

* Si los nodos aún no existen, es preferible crear todo en una sola instrucción `CREATE`.
* Si los nodos ya existen o pueden existir previamente, usa `MATCH` (o `MERGE` si quieres crearlos solo si no existen).
* **Utiliza `;` al final de cada instrucción Cypher cuando escribes varios comandos en el mismo bloque**, para evitar que Neo4j interprete las líneas como una sola sentencia.

De este modo se evitan nodos duplicados y relaciones incorrectas entre nodos vacíos.
