# Recursión, Pilas y Colas en Python

## 1. Recursión

### ¿Qué es la Recursión?

La recursión es una técnica de programación donde una función se llama a sí misma para resolver un problema. Cada llamada recursiva debe acercarse a un **caso base** que termine la recursión.

### Componentes de una Función Recursiva

1. **Caso base**: Condición que detiene la recursión
2. **Caso recursivo**: La función se llama a sí misma con parámetros modificados

### Ejemplos de Recursión

#### Factorial
```python
def factorial(n):
    # Caso base
    if n <= 1:
        return 1
    # Caso recursivo
    return n * factorial(n - 1)

# Ejemplo de uso
print(factorial(5))  # Output: 120
```

#### Fibonacci
```python
def fibonacci(n):
    # Casos base
    if n <= 1:
        return n
    # Caso recursivo
    return fibonacci(n - 1) + fibonacci(n - 2)

# Ejemplo de uso
print(fibonacci(6))  # Output: 8
```

#### Suma de una Lista
```python
def suma_recursiva(lista):
    # Caso base
    if not lista:
        return 0
    # Caso recursivo
    return lista[0] + suma_recursiva(lista[1:])

# Ejemplo de uso
numeros = [1, 2, 3, 4, 5]
print(suma_recursiva(numeros))  # Output: 15
```

#### Búsqueda Binaria Recursiva
```python
def busqueda_binaria(arr, objetivo, inicio=0, fin=None):
    if fin is None:
        fin = len(arr) - 1
    
    # Caso base: elemento no encontrado
    if inicio > fin:
        return -1
    
    medio = (inicio + fin) // 2
    
    # Caso base: elemento encontrado
    if arr[medio] == objetivo:
        return medio
    
    # Casos recursivos
    elif arr[medio] > objetivo:
        return busqueda_binaria(arr, objetivo, inicio, medio - 1)
    else:
        return busqueda_binaria(arr, objetivo, medio + 1, fin)

# Ejemplo de uso
lista_ordenada = [1, 3, 5, 7, 9, 11, 13, 15]
print(busqueda_binaria(lista_ordenada, 7))  # Output: 3
```
### La Pila de Activación (Call Stack)

Cuando una función se llama a sí misma recursivamente, Python utiliza una estructura interna llamada **pila de activación** o **call stack** para manejar las llamadas a funciones.

#### ¿Cómo Funciona la Pila de Activación?

Cada vez que se llama a una función, Python:

1. Crea un **marco de activación** (stack frame) que contiene:
   
   - Variables locales de la función
   - Parámetros de la función
   - Dirección de retorno (dónde continuar después de la función)
  
2. Coloca este marco en el **tope de la pila**
3. Cuando la función termina, **remueve el marco** de la pila

```python
def factorial_con_debug(n, nivel=0):
    # Mostrar el estado actual de la pila
    indentacion = "  " * nivel
    print(f"{indentacion}→ Llamando factorial({n}) - Nivel {nivel}")
    
    # Caso base
    if n <= 1:
        print(f"{indentacion}← Caso base alcanzado: factorial({n}) = 1")
        return 1
    
    # Caso recursivo
    print(f"{indentacion}  Calculando {n} * factorial({n-1})")
    resultado = n * factorial_con_debug(n - 1, nivel + 1)
    
    print(f"{indentacion}← Retornando: factorial({n}) = {resultado}")
    return resultado

# Ejemplo que muestra cómo crece y decrece la pila
print("=== Ejecución de factorial(4) ===")
factorial_con_debug(4)
```

**Salida esperada:**
```
=== Ejecución de factorial(4) ===
→ Llamando factorial(4) - Nivel 0
  Calculando 4 * factorial(3)
  → Llamando factorial(3) - Nivel 1
    Calculando 3 * factorial(2)
    → Llamando factorial(2) - Nivel 2
      Calculando 2 * factorial(1)
      → Llamando factorial(1) - Nivel 3
      ← Caso base alcanzado: factorial(1) = 1
    ← Retornando: factorial(2) = 2
  ← Retornando: factorial(3) = 6
← Retornando: factorial(4) = 24
```

#### Visualización de la Pila de Activación

```python
import sys

def mostrar_pila_recursiva(n):
    """Función que muestra el crecimiento de la pila de activación"""
    print(f"Profundidad actual: {n}")
    print(f"Límite de recursión: {sys.getrecursionlimit()}")
    print(f"Marcos en la pila: ~{n}")
    print("-" * 40)
    
    if n <= 0:
        print("¡Caso base alcanzado!")
        return "Resultado final"
    
    # Llamada recursiva que incrementa la profundidad
    resultado = mostrar_pila_recursiva(n - 1)
    print(f"Retornando desde nivel {n}")
    return resultado

# Ejemplo con pocos niveles para ver el comportamiento
print("=== Visualización de la Pila ===")
mostrar_pila_recursiva(3)
```

#### Stack Overflow - Cuando la Pila se Desborda

```python
import sys

def recursion_infinita(contador=0):
    """Ejemplo de lo que NO se debe hacer - recursión sin caso base adecuado"""
    print(f"Llamada #{contador}")
    return recursion_infinita(contador + 1)

def demostrar_stack_overflow():
    """Demuestra qué pasa cuando la pila se desborda"""
    print(f"Límite actual de recursión: {sys.getrecursionlimit()}")
    
    # Reducir el límite para la demostración
    sys.setrecursionlimit(100)
    print(f"Límite reducido a: {sys.getrecursionlimit()}")
    
    try:
        recursion_infinita()
    except RecursionError as e:
        print(f"\n¡Stack Overflow! Error: {e}")
    finally:
        # Restaurar el límite original
        sys.setrecursionlimit(1000)

# Descomenta la siguiente línea para ver el stack overflow
# demostrar_stack_overflow()
```

#### Comparación: Recursión vs Iteración en Memoria

```python
def factorial_recursivo(n):
    """Versión recursiva - usa la pila de activación"""
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)

def factorial_iterativo(n):
    """Versión iterativa - no usa pila adicional"""
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

# Análisis del uso de memoria
def analizar_memoria():
    import tracemalloc
    
    # Medir memoria para versión recursiva
    tracemalloc.start()
    resultado_rec = factorial_recursivo(100)
    memoria_rec = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    
    # Medir memoria para versión iterativa
    tracemalloc.start()
    resultado_iter = factorial_iterativo(100)
    memoria_iter = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    
    print(f"Factorial recursivo: {memoria_rec} bytes")
    print(f"Factorial iterativo: {memoria_iter} bytes")
    print(f"Diferencia: {memoria_rec - memoria_iter} bytes")

# analizar_memoria()  # Descomenta para ver la diferencia
```

#### Optimización: Recursión de Cola

```python
def factorial_cola(n, acumulador=1):
    """
    Recursión de cola - la llamada recursiva es lo último que se ejecuta
    Python no optimiza automáticamente esto, pero algunos lenguajes sí
    """
    if n <= 1:
        return acumulador
    return factorial_cola(n - 1, n * acumulador)

def fibonacci_cola(n, a=0, b=1):
    """Fibonacci con recursión de cola"""
    if n == 0:
        return a
    if n == 1:
        return b
    return fibonacci_cola(n - 1, b, a + b)

# Comparación de eficiencia
import time

def comparar_fibonacci(n):
    # Fibonacci recursivo tradicional (ineficiente)
    start = time.time()
    resultado_tradicional = fibonacci(min(n, 35))  # Limitamos por eficiencia
    tiempo_tradicional = time.time() - start
    
    # Fibonacci con recursión de cola
    start = time.time()
    resultado_cola = fibonacci_cola(n)
    tiempo_cola = time.time() - start
    
    print(f"Fibonacci tradicional (n={min(n, 35)}): {tiempo_tradicional:.6f}s")
    print(f"Fibonacci cola (n={n}): {tiempo_cola:.6f}s")

comparar_fibonacci(40)
```

### Ventajas y Desventajas de la Recursión

**Ventajas:**
- Código más limpio y legible para problemas naturalmente recursivos
- Útil para estructuras de datos jerárquicas (árboles, grafos)
- Refleja directamente la definición matemática del problema

**Desventajas:**
- **Overhead de memoria**: Cada llamada consume espacio en la pila de activación
- **Riesgo de stack overflow**: Recursiones muy profundas pueden agotar la pila
- **Puede ser menos eficiente**: El overhead de llamadas a funciones es costoso
- **Difícil de debuggear**: Múltiples marcos en la pila pueden confundir

**Cuándo usar recursión:**
- El problema tiene una estructura naturalmente recursiva
- La profundidad máxima es razonable (< 1000 llamadas)
- La claridad del código es más importante que la eficiencia máxima
- Trabajas con estructuras como árboles o grafos



## 2. Pilas (Stacks)

### ¿Qué es una Pila?

Una pila es una estructura de datos que sigue el principio **LIFO** (Last In, First Out). El último elemento en entrar es el primero en salir.

### Implementación con Lista de Python

```python
class Pila:
    def __init__(self):
        self.elementos = []
    
    def push(self, elemento):
        """Agregar elemento al tope de la pila"""
        self.elementos.append(elemento)
    
    def pop(self):
        """Remover y retornar el elemento del tope"""
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.elementos.pop()
    
    def peek(self):
        """Ver el elemento del tope sin removerlo"""
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.elementos[-1]
    
    def esta_vacia(self):
        """Verificar si la pila está vacía"""
        return len(self.elementos) == 0
    
    def tamaño(self):
        """Obtener el tamaño de la pila"""
        return len(self.elementos)
    
    def __str__(self):
        return f"Pila: {self.elementos}"

# Ejemplo de uso
pila = Pila()
pila.push(1)
pila.push(2)
pila.push(3)
print(pila)  # Output: Pila: [1, 2, 3]
print(pila.pop())  # Output: 3
print(pila.peek())  # Output: 2
```

### Aplicaciones de Pilas

Las pilas son fundamentales en la programación y tienen múltiples aplicaciones prácticas.

#### La Pila de Activación en Acción

```python
def simular_call_stack():
    """Simulación de cómo funciona internamente la pila de activación"""
    
    class MarcoActivacion:
        def __init__(self, nombre_funcion, parametros, variables_locales=None):
            self.nombre_funcion = nombre_funcion
            self.parametros = parametros
            self.variables_locales = variables_locales or {}
            self.direccion_retorno = None
        
        def __str__(self):
            return f"{self.nombre_funcion}({self.parametros}) - vars: {self.variables_locales}"
    
    # Simulamos la pila del sistema
    call_stack = Pila()
    
    def simular_factorial(n):
        # Crear marco de activación
        marco = MarcoActivacion("factorial", {"n": n})
        call_stack.push(marco)
        
        print(f"PUSH: {marco}")
        print(f"Pila actual: {[str(frame) for frame in call_stack.elementos]}")
        print("-" * 50)
        
        # Caso base
        if n <= 1:
            marco.variables_locales["resultado"] = 1
            print(f"Caso base: retornando 1")
            call_stack.pop()
            print(f"POP: {marco}")
            return 1
        
        # Caso recursivo
        marco.variables_locales["temp"] = n
        resultado = n * simular_factorial(n - 1)
        
        # Al retornar, actualizamos el marco
        marco.variables_locales["resultado"] = resultado
        print(f"Retornando: {resultado}")
        call_stack.pop()
        print(f"POP: {marco}")
        
        return resultado
    
    print("=== Simulación de Call Stack ===")
    resultado = simular_factorial(4)
    print(f"\nResultado final: {resultado}")
    print(f"Pila final (debe estar vacía): {call_stack.elementos}")

simular_call_stack()
```

#### Verificar Paréntesis Balanceados
```python
def parentesis_balanceados(expresion):
    pila = Pila()
    pares = {'(': ')', '[': ']', '{': '}'}
    
    for caracter in expresion:
        if caracter in pares:  # Es un paréntesis de apertura
            pila.push(caracter)
        elif caracter in pares.values():  # Es un paréntesis de cierre
            if pila.esta_vacia():
                return False
            if pares[pila.pop()] != caracter:
                return False
    
    return pila.esta_vacia()

# Ejemplos de uso
print(parentesis_balanceados("()[]{}"))  # True
print(parentesis_balanceados("([)]"))    # False
```

#### Conversión de Infijo a Postfijo
```python
def infijo_a_postfijo(expresion):
    pila = Pila()
    resultado = []
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    for token in expresion.split():
        if token.isalnum():  # Operando
            resultado.append(token)
        elif token == '(':
            pila.push(token)
        elif token == ')':
            while not pila.esta_vacia() and pila.peek() != '(':
                resultado.append(pila.pop())
            pila.pop()  # Remover '('
        else:  # Operador
            while (not pila.esta_vacia() and 
                   pila.peek() != '(' and
                   precedencia.get(pila.peek(), 0) >= precedencia.get(token, 0)):
                resultado.append(pila.pop())
            pila.push(token)
    
    while not pila.esta_vacia():
        resultado.append(pila.pop())
    
    return ' '.join(resultado)

# Ejemplo de uso
print(infijo_a_postfijo("A + B * C"))  # Output: A B C * +
```



## 3. Colas (Queues)

### ¿Qué es una Cola?

Una cola es una estructura de datos que sigue el principio **FIFO** (First In, First Out). El primer elemento en entrar es el primero en salir.

### Implementación con Lista de Python

```python
class Cola:
    def __init__(self):
        self.elementos = []
    
    def enqueue(self, elemento):
        """Agregar elemento al final de la cola"""
        self.elementos.append(elemento)
    
    def dequeue(self):
        """Remover y retornar el primer elemento"""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.elementos.pop(0)
    
    def front(self):
        """Ver el primer elemento sin removerlo"""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.elementos[0]
    
    def esta_vacia(self):
        """Verificar si la cola está vacía"""
        return len(self.elementos) == 0
    
    def tamaño(self):
        """Obtener el tamaño de la cola"""
        return len(self.elementos)
    
    def __str__(self):
        return f"Cola: {self.elementos}"

# Ejemplo de uso
cola = Cola()
cola.enqueue(1)
cola.enqueue(2)
cola.enqueue(3)
print(cola)  # Output: Cola: [1, 2, 3]
print(cola.dequeue())  # Output: 1
print(cola.front())  # Output: 2
```

### Implementación Eficiente con collections.deque

```python
from collections import deque

class ColaEficiente:
    def __init__(self):
        self.elementos = deque()
    
    def enqueue(self, elemento):
        self.elementos.append(elemento)
    
    def dequeue(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.elementos.popleft()
    
    def front(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.elementos[0]
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def tamaño(self):
        return len(self.elementos)
    
    def __str__(self):
        return f"Cola: {list(self.elementos)}"
```

### Cola Circular

```python
class ColaCircular:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.elementos = [None] * capacidad
        self.frente = 0
        self.tamaño_actual = 0
    
    def enqueue(self, elemento):
        if self.esta_llena():
            raise OverflowError("La cola está llena")
        
        posicion = (self.frente + self.tamaño_actual) % self.capacidad
        self.elementos[posicion] = elemento
        self.tamaño_actual += 1
    
    def dequeue(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        
        elemento = self.elementos[self.frente]
        self.elementos[self.frente] = None
        self.frente = (self.frente + 1) % self.capacidad
        self.tamaño_actual -= 1
        return elemento
    
    def front(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.elementos[self.frente]
    
    def esta_vacia(self):
        return self.tamaño_actual == 0
    
    def esta_llena(self):
        return self.tamaño_actual == self.capacidad
    
    def tamaño(self):
        return self.tamaño_actual
```

### Aplicaciones de Colas

#### Búsqueda en Anchura (BFS)
```python
def bfs(grafo, inicio):
    visitados = set()
    cola = Cola()
    resultado = []
    
    cola.enqueue(inicio)
    visitados.add(inicio)
    
    while not cola.esta_vacia():
        nodo = cola.dequeue()
        resultado.append(nodo)
        
        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.enqueue(vecino)
    
    return resultado

# Ejemplo de uso
grafo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
print(bfs(grafo, 'A'))  # Output: ['A', 'B', 'C', 'D', 'E', 'F']
```

#### Sistema de Tareas con Prioridad
```python
import heapq

class ColaPrioridad:
    def __init__(self):
        self.elementos = []
        self.contador = 0
    
    def enqueue(self, elemento, prioridad):
        # Menor número = mayor prioridad
        heapq.heappush(self.elementos, (prioridad, self.contador, elemento))
        self.contador += 1
    
    def dequeue(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return heapq.heappop(self.elementos)[2]
    
    def esta_vacia(self):
        return len(self.elementos) == 0

# Ejemplo de uso
cola_tareas = ColaPrioridad()
cola_tareas.enqueue("Tarea normal", 2)
cola_tareas.enqueue("Tarea urgente", 1)
cola_tareas.enqueue("Tarea baja prioridad", 3)

print(cola_tareas.dequeue())  # Output: Tarea urgente
```



## 4. Comparación y Casos de Uso

### Cuándo Usar Cada Estructura

**Recursión:**
- Problemas que se pueden dividir en subproblemas similares
- Navegación en árboles y grafos
- Algoritmos divide y vencerás
- Problemas matemáticos (factorial, fibonacci)

**Pilas:**
- Verificación de sintaxis (paréntesis, llaves)
- Evaluación de expresiones
- Historial de navegación (undo/redo)
- **Implementación de la pila de activación** (call stack en recursión)
- Algoritmos de backtracking

**Colas:**
- Sistemas de espera (impresión, procesos)
- Búsqueda en anchura (BFS)
- Manejo de tareas asíncronas
- Buffers de datos

### Complejidad Temporal

| Operación | Pila | Cola | Cola (deque) |
|--|||--|
| Push/Enqueue | O(1) | O(n) | O(1) |
| Pop/Dequeue | O(1) | O(n) | O(1) |
| Peek/Front | O(1) | O(1) | O(1) |



## 5. Ejercicios Prácticos

### Ejercicio 1: Torre de Hanoi (Recursión)
```python
def torre_hanoi(n, origen, destino, auxiliar):
    if n == 1:
        print(f"Mover disco de {origen} a {destino}")
    else:
        torre_hanoi(n-1, origen, auxiliar, destino)
        print(f"Mover disco de {origen} a {destino}")
        torre_hanoi(n-1, auxiliar, destino, origen)

# Ejemplo de uso
torre_hanoi(3, 'A', 'C', 'B')
```

### Ejercicio 2: Calculadora con Pila
```python
def evaluar_postfijo(expresion):
    pila = Pila()
    
    for token in expresion.split():
        if token.isdigit():
            pila.push(int(token))
        else:
            b = pila.pop()
            a = pila.pop()
            
            if token == '+':
                pila.push(a + b)
            elif token == '-':
                pila.push(a - b)
            elif token == '*':
                pila.push(a * b)
            elif token == '/':
                pila.push(a // b)
    
    return pila.pop()

# Ejemplo de uso
print(evaluar_postfijo("3 4 + 2 *"))  # Output: 14
```

### Ejercicio 3: Simulador de Banco (Cola)
```python
import random

def simular_banco(clientes, tiempo_atencion):
    cola_espera = Cola()
    tiempo_total = 0
    
    # Agregar clientes a la cola
    for i in range(clientes):
        cola_espera.enqueue(f"Cliente {i+1}")
    
    print(f"Banco abierto con {clientes} clientes en espera")
    
    while not cola_espera.esta_vacia():
        cliente = cola_espera.dequeue()
        tiempo_servicio = random.randint(1, tiempo_atencion)
        tiempo_total += tiempo_servicio
        
        print(f"Atendiendo a {cliente} - Tiempo: {tiempo_servicio} min")
        print(f"Clientes en espera: {cola_espera.tamaño()}")
    
    print(f"Tiempo total de atención: {tiempo_total} minutos")

# Ejemplo de uso
simular_banco(5, 10)
```
### Ejercicio 4: Resolver Sudoku con Backtracking

El Sudoku es un juego de lógica que consiste en completar una cuadrícula de 9×9 celdas dividida en subcuadrículas de 3×3, con las siguientes reglas:

**Reglas del Sudoku:**
1. Cada fila debe contener los números del 1 al 9 sin repetirse
2. Cada columna debe contener los números del 1 al 9 sin repetirse  
3. Cada subcuadrícula de 3×3 debe contener los números del 1 al 9 sin repetirse
4. Algunas celdas ya están llenas como pistas iniciales

**Algoritmo de Backtracking:**
El backtracking es una técnica recursiva que prueba soluciones parciales y "retrocede" cuando encuentra un callejón sin salida.

```python
def resolver_sudoku(tablero):
    """
    Resuelve un sudoku usando backtracking recursivo
    tablero: matriz 9x9 donde 0 representa celdas vacías
    """
    # Buscar la primera celda vacía
    celda_vacia = encontrar_celda_vacia(tablero)
    
    # Caso base: no hay celdas vacías, sudoku resuelto
    if not celda_vacia:
        return True
    
    fila, columna = celda_vacia
    
    # Probar números del 1 al 9
    for numero in range(1, 10):
        if es_valido(tablero, numero, fila, columna):
            # Colocar el número (decisión)
            tablero[fila][columna] = numero
            
            # Recursión: intentar resolver el resto
            if resolver_sudoku(tablero):
                return True
            
            # Backtrack: deshacer la decisión si no funciona
            tablero[fila][columna] = 0
    
    # Si ningún número funciona, retroceder
    return False

def encontrar_celda_vacia(tablero):
    """Encuentra la primera celda vacía (con valor 0)"""
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:
                return (fila, columna)
    return None

def es_valido(tablero, numero, fila, columna):
    """Verifica si es válido colocar un número en una posición"""
    # Verificar fila
    for col in range(9):
        if tablero[fila][col] == numero:
            return False
    
    # Verificar columna
    for fil in range(9):
        if tablero[fil][columna] == numero:
            return False
    
    # Verificar subcuadrícula 3x3
    inicio_fila = (fila // 3) * 3
    inicio_col = (columna // 3) * 3
    
    for fil in range(inicio_fila, inicio_fila + 3):
        for col in range(inicio_col, inicio_col + 3):
            if tablero[fil][col] == numero:
                return False
    
    return True

def imprimir_tablero(tablero):
    """Imprime el tablero de sudoku de forma legible"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            
            if j == 8:
                print(tablero[i][j])
            else:
                print(str(tablero[i][j]) + " ", end="")

# Ejemplo de uso
sudoku_ejemplo = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("Sudoku inicial:")
imprimir_tablero(sudoku_ejemplo)

if resolver_sudoku(sudoku_ejemplo):
    print("\nSudoku resuelto:")
    imprimir_tablero(sudoku_ejemplo)
else:
    print("No se pudo resolver el sudoku")
```

**Cómo funciona el algoritmo:**

1. **Encontrar celda vacía**: Busca la primera celda con valor 0
2. **Probar números**: Para cada número del 1 al 9:
   - Verifica si es válido colocarlo según las reglas
   - Si es válido, lo coloca y llama recursivamente
   - Si la recursión tiene éxito, el sudoku está resuelto
   - Si falla, quita el número (backtrack) y prueba el siguiente
3. **Caso base**: Cuando no hay más celdas vacías, el sudoku está completo

**Optimizaciones posibles:**
```python
def resolver_sudoku_optimizado(tablero):
    """Versión optimizada que busca la celda con menos opciones"""
    celda_vacia = encontrar_mejor_celda(tablero)
    
    if not celda_vacia:
        return True
    
    fila, columna, opciones = celda_vacia
    
    for numero in opciones:
        tablero[fila][columna] = numero
        
        if resolver_sudoku_optimizado(tablero):
            return True
        
        tablero[fila][columna] = 0
    
    return False

def encontrar_mejor_celda(tablero):
    """Encuentra la celda vacía con menos opciones válidas"""
    mejor_celda = None
    min_opciones = 10
    
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:
                opciones = obtener_opciones_validas(tablero, fila, columna)
                if len(opciones) < min_opciones:
                    min_opciones = len(opciones)
                    mejor_celda = (fila, columna, opciones)
                    
                    # Si solo hay una opción, la elegimos inmediatamente
                    if min_opciones == 1:
                        return mejor_celda
    
    return mejor_celda

def obtener_opciones_validas(tablero, fila, columna):
    """Obtiene todos los números válidos para una posición"""
    opciones = []
    for numero in range(1, 10):
        if es_valido(tablero, numero, fila, columna):
            opciones.append(numero)
    return opciones
```

Este enfoque de backtracking para resolver sudokus demuestra el poder de la recursión para problemas de búsqueda con restricciones, donde necesitamos explorar múltiples posibilidades y retroceder cuando llegamos a un callejón sin salida.