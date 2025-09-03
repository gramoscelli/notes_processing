# Tema 1: Introducción a los Grafos

## Objetivos de Aprendizaje
Al finalizar este tema, los estudiantes serán capaces de:
- Definir qué es un grafo y sus componentes básicos
- Identificar grafos en situaciones cotidianas
- Distinguir entre nodos y aristas
- Crear representaciones simples de grafos en Python

---

## 1.1 ¿Qué es un grafo?

Un **grafo** es una estructura matemática que modela relaciones entre objetos. Consiste en un conjunto de **nodos** (también llamados vértices) conectados por **aristas** (también llamadas enlaces o relaciones).

### Ejemplos cotidianos:

**Red Social (Facebook/Instagram)**
- Nodos: Usuarios
- Aristas: Amistad o seguimiento entre usuarios

**Mapa de Transporte**
- Nodos: Estaciones o paradas
- Aristas: Rutas o conexiones entre estaciones

**Árbol Genealógico**
- Nodos: Personas
- Aristas: Relaciones familiares (padre-hijo, hermanos)

**Organigrama Empresarial**
- Nodos: Empleados o departamentos
- Aristas: Relaciones jerárquicas o de colaboración

---

## 1.2 Componentes Básicos

### Nodos (Vértices)
Los **nodos** representan las entidades o elementos principales del sistema:
- En una red social: cada usuario
- En un mapa: cada ubicación
- En un sistema académico: estudiantes, profesores, cursos

### Aristas (Relaciones)
Las **aristas** representan las conexiones o relaciones entre nodos:
- Pueden tener dirección (dirigidas) o no (no dirigidas)
- Pueden tener peso o costo asociado
- Pueden tener diferentes tipos o categorías

### Propiedades
Tanto nodos como aristas pueden tener **propiedades** que almacenan información adicional:
- Nodo "Usuario": nombre, edad, ciudad
- Arista "Amistad": fecha_inicio, tipo_relacion

### Etiquetas
Las **etiquetas** categorizan nodos y relaciones:
- Nodos: "Persona", "Empresa", "Producto"
- Relaciones: "AMIGO_DE", "TRABAJA_EN", "COMPRO"

---

## 1.3 Representación en Python

### Ejemplo 1: Red Social Simple

```python
# Representación básica con diccionarios
red_social = {
    'usuarios': {
        'ana': {'edad': 25, 'ciudad': 'Madrid'},
        'carlos': {'edad': 30, 'ciudad': 'Barcelona'},
        'lucia': {'edad': 28, 'ciudad': 'Madrid'},
        'pedro': {'edad': 35, 'ciudad': 'Valencia'}
    },
    'amistades': [
        ('ana', 'carlos'),
        ('ana', 'lucia'),
        ('carlos', 'pedro'),
        ('lucia', 'pedro')
    ]
}

# Función para encontrar amigos de un usuario
def obtener_amigos(usuario, red):
    amigos = []
    for amistad in red['amistades']:
        if amistad[0] == usuario:
            amigos.append(amistad[1])
        elif amistad[1] == usuario:
            amigos.append(amistad[0])
    return amigos

# Ejemplo de uso
print(f"Amigos de Ana: {obtener_amigos('ana', red_social)}")
```

### Ejemplo 2: Sistema de Transporte

```python
# Grafo de estaciones de metro
metro = {
    'estaciones': {
        'sol': {'linea': ['1', '2', '3'], 'zona': 'centro'},
        'atocha': {'linea': ['1'], 'zona': 'centro'},
        'retiro': {'linea': ['2'], 'zona': 'centro'},
        'cuatro_caminos': {'linea': ['1', '6'], 'zona': 'norte'}
    },
    'conexiones': [
        ('sol', 'atocha', {'linea': '1', 'tiempo': 3}),
        ('sol', 'retiro', {'linea': '2', 'tiempo': 2}),
        ('sol', 'cuatro_caminos', {'linea': '1', 'tiempo': 8}),
        ('atocha', 'cuatro_caminos', {'linea': '1', 'tiempo': 12})
    ]
}

# Función para encontrar conexiones directas
def conexiones_directas(estacion, metro):
    conexiones = []
    for conexion in metro['conexiones']:
        if conexion[0] == estacion:
            conexiones.append((conexion[1], conexion[2]))
        elif conexion[1] == estacion:
            conexiones.append((conexion[0], conexion[2]))
    return conexiones

# Ejemplo de uso
print(f"Desde Sol puedes ir a: {conexiones_directas('sol', metro)}")
```

### Ejemplo 3: Árbol Genealógico

```python
# Representación de familia
familia = {
    'personas': {
        'abuelo_juan': {'edad': 75, 'genero': 'M'},
        'abuela_maria': {'edad': 73, 'genero': 'F'},
        'padre_luis': {'edad': 45, 'genero': 'M'},
        'madre_carmen': {'edad': 42, 'genero': 'F'},
        'hijo_pablo': {'edad': 18, 'genero': 'M'},
        'hija_sofia': {'edad': 15, 'genero': 'F'}
    },
    'relaciones': [
        ('abuelo_juan', 'padre_luis', 'padre_de'),
        ('abuela_maria', 'padre_luis', 'madre_de'),
        ('padre_luis', 'madre_carmen', 'casado_con'),
        ('padre_luis', 'hijo_pablo', 'padre_de'),
        ('padre_luis', 'hija_sofia', 'padre_de'),
        ('madre_carmen', 'hijo_pablo', 'madre_de'),
        ('madre_carmen', 'hija_sofia', 'madre_de'),
        ('hijo_pablo', 'hija_sofia', 'hermano_de')
    ]
}

# Función para encontrar hijos de una persona
def obtener_hijos(persona, familia):
    hijos = []
    for relacion in familia['relaciones']:
        if relacion[0] == persona and relacion[2] in ['padre_de', 'madre_de']:
            hijos.append(relacion[1])
    return list(set(hijos))  # Eliminar duplicados

# Ejemplo de uso
print(f"Hijos de Luis: {obtener_hijos('padre_luis', familia)}")
```

---

## 1.4 Ejercicios Prácticos

### Ejercicio 1: Modelar tu red de contactos
```python
# TODO: Completa este diccionario con tus contactos reales
mi_red = {
    'contactos': {
        # 'nombre': {'profesion': '...', 'ciudad': '...'},
    },
    'relaciones': [
        # ('persona1', 'persona2', 'tipo_relacion'),
    ]
}

# Implementa estas funciones:
def contar_contactos(red):
    # Devuelve el número total de contactos
    pass

def contactos_por_ciudad(ciudad, red):
    # Devuelve lista de contactos en una ciudad específica
    pass

def tipos_de_relacion(red):
    # Devuelve todos los tipos de relación únicos
    pass
```

### Ejercicio 2: Sistema académico simple
```python
# Modela un sistema con estudiantes, profesores y cursos
sistema_academico = {
    'estudiantes': {
        # 'nombre': {'carrera': '...', 'semestre': ...},
    },
    'profesores': {
        # 'nombre': {'departamento': '...', 'especialidad': '...'},
    },
    'cursos': {
        # 'codigo': {'nombre': '...', 'creditos': ...},
    },
    'relaciones': [
        # ('estudiante', 'curso', 'inscrito_en'),
        # ('profesor', 'curso', 'dicta'),
    ]
}

# Implementa:
def estudiantes_de_curso(curso, sistema):
    # Devuelve estudiantes inscritos en un curso
    pass

def cursos_de_estudiante(estudiante, sistema):
    # Devuelve cursos de un estudiante
    pass

def profesor_de_curso(curso, sistema):
    # Devuelve el profesor que dicta un curso
    pass
```

---

## 1.5 Visualización Básica

### Usando NetworkX (opcional)
```python
import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo simple
G = nx.Graph()

# Agregar nodos
G.add_node("Ana", edad=25)
G.add_node("Carlos", edad=30)
G.add_node("Lucia", edad=28)

# Agregar aristas
G.add_edge("Ana", "Carlos", relacion="amigos")
G.add_edge("Ana", "Lucia", relacion="amigos")

# Visualizar
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=1500, font_size=12, font_weight='bold')
plt.title("Red Social Simple")
plt.show()
```

---

## 1.6 Conceptos Clave para Recordar

- **Grafo**: Estructura de nodos conectados por aristas
- **Nodo**: Entidad o elemento del sistema
- **Arista**: Conexión o relación entre nodos
- **Propiedades**: Información adicional de nodos y aristas
- **Etiquetas**: Categorización de elementos

---

## 1.7 Preparación para el Siguiente Tema

En el próximo tema exploraremos:
- Cuándo usar grafos vs bases de datos relacionales
- Ventajas específicas de los grafos
- Casos de uso donde los grafos sobresalen
