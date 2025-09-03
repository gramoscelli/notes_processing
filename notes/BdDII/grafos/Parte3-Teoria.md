# Tema 3: Teoría Básica de Grafos

## Objetivos de Aprendizaje
Al finalizar este tema, los estudiantes serán capaces de:
- Clasificar diferentes tipos de grafos
- Identificar caminos, ciclos y componentes conectados
- Calcular propiedades básicas de grafos
- Implementar algoritmos fundamentales en Python

---

## 3.1 Tipos de Grafos

### Grafos Dirigidos vs No Dirigidos

```python
# Grafo NO DIRIGIDO: Las relaciones son bidireccionales
amistad_facebook = {
    'nodos': ['ana', 'carlos', 'lucia', 'pedro'],
    'aristas': [
        ('ana', 'carlos'),      # Ana y Carlos son amigos mutuamente
        ('ana', 'lucia'),       # Ana y Lucia son amigas mutuamente
        ('carlos', 'pedro'),    # Carlos y Pedro son amigos mutuamente
        ('lucia', 'pedro')      # Lucia y Pedro son amigos mutuamente
    ]
}

# Grafo DIRIGIDO: Las relaciones tienen dirección específica
seguimiento_twitter = {
    'nodos': ['ana', 'carlos', 'lucia', 'pedro'],
    'aristas': [
        ('ana', 'carlos'),      # Ana sigue a Carlos (no necesariamente viceversa)
        ('carlos', 'ana'),      # Carlos sigue a Ana
        ('ana', 'lucia'),       # Ana sigue a Lucia
        ('pedro', 'lucia'),     # Pedro sigue a Lucia
        ('lucia', 'pedro')      # Lucia sigue a Pedro
    ]
}

def es_mutuo(usuario1, usuario2, grafo_dirigido):
    """Verifica si dos usuarios se siguen mutuamente"""
    sigue_12 = (usuario1, usuario2) in grafo_dirigido['aristas']
    sigue_21 = (usuario2, usuario1) in grafo_dirigido['aristas']
    return sigue_12 and sigue_21

print("Relaciones mutuas en Twitter:")
for u1 in seguimiento_twitter['nodos']:
    for u2 in seguimiento_twitter['nodos']:
        if u1 < u2 and es_mutuo(u1, u2, seguimiento_twitter):
            print(f"  {u1} ↔ {u2}")
```

### Grafos Ponderados

```python
# Grafo ponderado: Las aristas tienen peso o costo
red_transporte = {
    'estaciones': ['centro', 'norte', 'sur', 'este', 'oeste'],
    'rutas': [
        ('centro', 'norte', {'tiempo': 15, 'costo': 2.5}),
        ('centro', 'sur', {'tiempo': 20, 'costo': 3.0}),
        ('centro', 'este', {'tiempo': 12, 'costo': 2.0}),
        ('norte', 'oeste', {'tiempo': 25, 'costo': 3.5}),
        ('sur', 'oeste', {'tiempo': 18, 'costo': 2.8}),
        ('este', 'norte', {'tiempo': 22, 'costo': 3.2})
    ]
}

def encontrar_ruta_mas_rapida(origen, destino, grafo):
    """Encuentra la ruta más rápida entre dos estaciones"""
    # Implementación simple de Dijkstra
    import heapq
    
    # Inicializar distancias
    distancias = {estacion: float('inf') for estacion in grafo['estaciones']}
    distancias[origen] = 0
    predecesores = {}
    
    # Cola de prioridad: (distancia, nodo)
    cola = [(0, origen)]
    visitados = set()
    
    while cola:
        dist_actual, nodo_actual = heapq.heappop(cola)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        if nodo_actual == destino:
            break
        
        # Examinar vecinos
        for ruta in grafo['rutas']:
            if ruta[0] == nodo_actual:
                vecino = ruta[1]
                peso = ruta[2]['tiempo']
            elif ruta[1] == nodo_actual:
                vecino = ruta[0]
                peso = ruta[2]['tiempo']
            else:
                continue
            
            if vecino in visitados:
                continue
            
            nueva_distancia = dist_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_distancia, vecino))
    
    # Reconstruir camino
    if destino not in predecesores and destino != origen:
        return None, float('inf')
    
    camino = []
    actual = destino
    while actual != origen:
        camino.append(actual)
        actual = predecesores[actual]
    camino.append(origen)
    camino.reverse()
    
    return camino, distancias[destino]

# Ejemplo de uso
ruta, tiempo = encontrar_ruta_mas_rapida('centro', 'oeste', red_transporte)
print(f"Ruta más rápida de centro a oeste: {' → '.join(ruta)} ({tiempo} minutos)")
```

### Multigrafos

```python
# Multigrafo: Múltiples aristas entre los mismos nodos
comunicacion_empresarial = {
    'empleados': ['ana', 'carlos', 'lucia'],
    'comunicaciones': [
        ('ana', 'carlos', 'email', {'frecuencia': 'diaria'}),
        ('ana', 'carlos', 'slack', {'frecuencia': 'constante'}),
        ('ana', 'carlos', 'reunion', {'frecuencia': 'semanal'}),
        ('carlos', 'lucia', 'email', {'frecuencia': 'ocasional'}),
        ('carlos', 'lucia', 'telefono', {'frecuencia': 'rara'})
    ]
}

def analizar_intensidad_comunicacion(empleado1, empleado2, grafo):
    """Analiza la intensidad de comunicación entre dos empleados"""
    canales = []
    for comm in grafo['comunicaciones']:
        if (comm[0] == empleado1 and comm[1] == empleado2) or \
           (comm[0] == empleado2 and comm[1] == empleado1):
            canales.append({
                'canal': comm[2],
                'frecuencia': comm[3]['frecuencia']
            })
    
    # Asignar puntuación por frecuencia
    puntuacion_freq = {
        'constante': 5,
        'diaria': 4,
        'semanal': 3,
        'ocasional': 2,
        'rara': 1
    }
    
    puntuacion_total = sum(puntuacion_freq[canal['frecuencia']] for canal in canales)
    
    return {
        'canales': canales,
        'puntuacion_comunicacion': puntuacion_total
    }

print("Análisis de comunicación Ana-Carlos:")
resultado = analizar_intensidad_comunicacion('ana', 'carlos', comunicacion_empresarial)
print(f"Canales: {[c['canal'] for c in resultado['canales']]}")
print(f"Puntuación de intensidad: {resultado['puntuacion_comunicacion']}")
```

---

## 3.2 Conceptos Fundamentales

### Caminos y Ciclos

```python
def encontrar_todos_los_caminos(grafo, inicio, fin, camino_actual=[]):
    """Encuentra todos los caminos posibles entre dos nodos"""
    camino_actual = camino_actual + [inicio]
    
    if inicio == fin:
        return [camino_actual]
    
    caminos = []
    for arista in grafo['aristas']:
        siguiente = None
        if arista[0] == inicio and arista[1] not in camino_actual:
            siguiente = arista[1]
        elif arista[1] == inicio and arista[0] not in camino_actual:
            siguiente = arista[0]
        
        if siguiente:
            nuevos_caminos = encontrar_todos_los_caminos(grafo, siguiente, fin, camino_actual)
            caminos.extend(nuevos_caminos)
    
    return caminos

def detectar_ciclos(grafo):
    """Detecta todos los ciclos en un grafo no dirigido"""
    def dfs_ciclos(nodo, visitados, padre, camino_actual):
        visitados.add(nodo)
        
        for arista in grafo['aristas']:
            vecino = None
            if arista[0] == nodo:
                vecino = arista[1]
            elif arista[1] == nodo:
                vecino = arista[0]
            
            if vecino:
                if vecino not in visitados:
                    resultado = dfs_ciclos(vecino, visitados, nodo, camino_actual + [vecino])
                    if resultado:
                        return resultado
                elif vecino != padre and len(camino_actual) >= 3:
                    # Encontramos un ciclo
                    idx_inicio = camino_actual.index(vecino)
                    return camino_actual[idx_inicio:] + [vecino]
        
        return None
    
    visitados_global = set()
    ciclos = []
    
    for nodo in grafo['nodos']:
        if nodo not in visitados_global:
            visitados_locales = set()
            ciclo = dfs_ciclos(nodo, visitados_locales, None, [nodo])
            if ciclo:
                ciclos.append(ciclo)
            visitados_global.update(visitados_locales)
    
    return ciclos

# Ejemplo con red social
red_con_ciclos = {
    'nodos': ['ana', 'carlos', 'lucia', 'pedro'],
    'aristas': [
        ('ana', 'carlos'),
        ('carlos', 'lucia'),
        ('lucia', 'ana'),      # Ciclo: ana → carlos → lucia → ana
        ('carlos', 'pedro'),
        ('pedro', 'lucia')     # Otro ciclo posible
    ]
}

print("Todos los caminos de Ana a Pedro:")
caminos = encontrar_todos_los_caminos(red_con_ciclos, 'ana', 'pedro')
for i, camino in enumerate(caminos, 1):
    print(f"  Camino {i}: {' → '.join(camino)}")

print(f"\nCiclos detectados:")
ciclos = detectar_ciclos(red_con_ciclos)
for i, ciclo in enumerate(ciclos, 1):
    print(f"  Ciclo {i}: {' → '.join(ciclo)}")
```

### Conectividad y Componentes

```python
def encontrar_componentes_conectados(grafo):
    """Encuentra todos los componentes conectados en un grafo"""
    visitados = set()
    componentes = []
    
    def dfs(nodo, componente_actual):
        visitados.add(nodo)
        componente_actual.append(nodo)
        
        # Buscar todos los vecinos
        for arista in grafo['aristas']:
            vecino = None
            if arista[0] == nodo and arista[1] not in visitados:
                vecino = arista[1]
            elif arista[1] == nodo and arista[0] not in visitados:
                vecino = arista[0]
            
            if vecino:
                dfs(vecino, componente_actual)
    
    for nodo in grafo['nodos']:
        if nodo not in visitados:
            componente = []
            dfs(nodo, componente)
            componentes.append(componente)
    
    return componentes

def calcular_grado_nodos(grafo):
    """Calcula el grado (número de conexiones) de cada nodo"""
    grados = {nodo: 0 for nodo in grafo['nodos']}
    
    for arista in grafo['aristas']:
        grados[arista[0]] += 1
        grados[arista[1]] += 1
    
    return grados

def es_grafo_conectado(grafo):
    """Verifica si el grafo está completamente conectado"""
    componentes = encontrar_componentes_conectados(grafo)
    return len(componentes) == 1

# Ejemplo: Red social fragmentada
red_fragmentada = {
    'nodos': ['ana', 'carlos', 'lucia', 'pedro', 'sofia', 'miguel'],
    'aristas': [
        # Grupo 1: Ana, Carlos, Lucia
        ('ana', 'carlos'),
        ('carlos', 'lucia'),
        
        # Grupo 2: Pedro, Sofia (aislados del grupo 1)
        ('pedro', 'sofia'),
        
        # Miguel está completamente aislado
    ]
}

print("Análisis de conectividad:")
componentes = encontrar_componentes_conectados(red_fragmentada)
print(f"Número de componentes: {len(componentes)}")
for i, comp in enumerate(componentes, 1):
    print(f"  Componente {i}: {comp}")

print(f"\nGrado de cada nodo:")
grados = calcular_grado_nodos(red_fragmentada)
for nodo, grado in grados.items():
    print(f"  {nodo}: {grado} conexiones")

print(f"\n¿Está conectado? {es_grafo_conectado(red_fragmentada)}")
```

---

## 3.3 Propiedades Importantes

### Densidad del Grafo

```python
def calcular_densidad(grafo):
    """Calcula la densidad del grafo (0 = sin aristas, 1 = completo)"""
    n = len(grafo['nodos'])
    m = len(grafo['aristas'])
    
    # Máximo número de aristas posibles en grafo no dirigido
    max_aristas = n * (n - 1) // 2
    
    if max_aristas == 0:
        return 0
    
    densidad = m / max_aristas
    return densidad

def comparar_redes_sociales():
    """Compara la densidad de diferentes redes sociales"""
    
    # Red muy densa (todos conocen a todos)
    red_densa = {
        'nodos': ['ana', 'carlos', 'lucia', 'pedro'],
        'aristas': [
            ('ana', 'carlos'), ('ana', 'lucia'), ('ana', 'pedro'),
            ('carlos', 'lucia'), ('carlos', 'pedro'),
            ('lucia', 'pedro')
        ]
    }
    
    # Red dispersa (pocas conexiones)
    red_dispersa = {
        'nodos': ['ana', 'carlos', 'lucia', 'pedro', 'sofia', 'miguel', 'elena'],
        'aristas': [
            ('ana', 'carlos'),
            ('lucia', 'pedro'),
            ('sofia', 'miguel')
        ]
    }
    
    print("Comparación de densidades:")
    print(f"Red densa: {calcular_densidad(red_densa):.2f}")
    print(f"Red dispersa: {calcular_densidad(red_dispersa):.2f}")

comparar_redes_sociales()
```

### Diámetro del Grafo

```python
def calcular_distancia_minima(grafo, origen, destino):
    """Calcula la distancia mínima entre dos nodos usando BFS"""
    if origen == destino:
        return 0
    
    from collections import deque
    
    cola = deque([(origen, 0)])
    visitados = {origen}
    
    while cola:
        nodo_actual, distancia = cola.popleft()
        
        # Buscar vecinos
        for arista in grafo['aristas']:
            vecino = None
            if arista[0] == nodo_actual:
                vecino = arista[1]
            elif arista[1] == nodo_actual:
                vecino = arista[0]
            
            if vecino and vecino not in visitados:
                if vecino == destino:
                    return distancia + 1
                
                visitados.add(vecino)
                cola.append((vecino, distancia + 1))
    
    return float('inf')  # No hay camino

def calcular_diametro(grafo):
    """Calcula el diámetro del grafo (máxima distancia entre cualquier par de nodos)"""
    max_distancia = 0
    
    for i, nodo1 in enumerate(grafo['nodos']):
        for nodo2 in grafo['nodos'][i+1:]:
            distancia = calcular_distancia_minima(grafo, nodo1, nodo2)
            if distancia != float('inf'):
                max_distancia = max(max_distancia, distancia)
    
    return max_distancia

def analizar_distancias_red(grafo):
    """Analiza todas las distancias en una red"""
    print("Matriz de distancias:")
    print("    ", end="")
    for nodo in grafo['nodos']:
        print(f"{nodo:>6}", end="")
    print()
    
    for nodo1 in grafo['nodos']:
        print(f"{nodo1:>3} ", end="")
        for nodo2 in grafo['nodos']:
            if nodo1 == nodo2:
                print(f"{'0':>6}", end="")
            else:
                dist = calcular_distancia_minima(grafo, nodo1, nodo2)
                dist_str = str(dist) if dist != float('inf') else "∞"
                print(f"{dist_str:>6}", end="")
        print()
    
    diametro = calcular_diametro(grafo)
    print(f"\nDiámetro del grafo: {diametro}")

# Ejemplo de análisis
red_ejemplo = {
    'nodos': ['A', 'B', 'C', 'D', 'E'],
    'aristas': [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'E')
    ]
}

analizar_distancias_red(red_ejemplo)
```

### Centralidad de Nodos

```python
def calcular_centralidad_grado(grafo):
    """Calcula la centralidad de grado (normalizada)"""
    grados = calcular_grado_nodos(grafo)
    n = len(grafo['nodos'])
    max_grado = n - 1  # Máximo grado posible
    
    centralidad = {}
    for nodo, grado in grados.items():
        centralidad[nodo] = grado / max_grado if max_grado > 0 else 0
    
    return centralidad

def calcular_centralidad_intermediacion(grafo):
    """Calcula centralidad de intermediación (betweenness)"""
    centralidad = {nodo: 0 for nodo in grafo['nodos']}
    
    # Para cada par de nodos, encontrar todos los caminos más cortos
    for s in grafo['nodos']:
        for t in grafo['nodos']:
            if s != t:
                caminos_cortos = encontrar_caminos_mas_cortos(grafo, s, t)
                if caminos_cortos:
                    # Contar cuántos caminos pasan por cada nodo intermedio
                    for camino in caminos_cortos:
                        for nodo_intermedio in camino[1:-1]:  # Excluir origen y destino
                            centralidad[nodo_intermedio] += 1 / len(caminos_cortos)
    
    # Normalizar
    n = len(grafo['nodos'])
    normalizacion = (n - 1) * (n - 2) / 2 if n > 2 else 1
    
    for nodo in centralidad:
        centralidad[nodo] /= normalizacion
    
    return centralidad

def encontrar_caminos_mas_cortos(grafo, inicio, fin):
    """Encuentra todos los caminos más cortos entre dos nodos"""
    if inicio == fin:
        return [[inicio]]
    
    from collections import deque
    
    # BFS para encontrar la distancia mínima
    cola = deque([(inicio, [inicio])])
    visitados = {inicio: 0}
    caminos_cortos = []
    distancia_minima = None
    
    while cola:
        nodo_actual, camino_actual = cola.popleft()
        
        if distancia_minima is not None and len(camino_actual) > distancia_minima:
            break
        
        for arista in grafo['aristas']:
            vecino = None
            if arista[0] == nodo_actual:
                vecino = arista[1]
            elif arista[1] == nodo_actual:
                vecino = arista[0]
            
            if vecino:
                nuevo_camino = camino_actual + [vecino]
                
                if vecino == fin:
                    if distancia_minima is None:
                        distancia_minima = len(nuevo_camino)
                        caminos_cortos.append(nuevo_camino)
                    elif len(nuevo_camino) == distancia_minima:
                        caminos_cortos.append(nuevo_camino)
                
                elif vecino not in visitados or visitados[vecino] >= len(nuevo_camino):
                    visitados[vecino] = len(nuevo_camino)
                    cola.append((vecino, nuevo_camino))
    
    return caminos_cortos

def analizar_centralidades(grafo):
    """Analiza diferentes medidas de centralidad"""
    print("Análisis de Centralidades:")
    
    cent_grado = calcular_centralidad_grado(grafo)
    cent_intermediacion = calcular_centralidad_intermediacion(grafo)
    
    print(f"{'Nodo':<10} {'Grado':<10} {'Intermediación':<15}")
    print("-" * 35)
    
    for nodo in grafo['nodos']:
        print(f"{nodo:<10} {cent_grado[nodo]:<10.3f} {cent_intermediacion[nodo]:<15.3f}")

# Ejemplo: Red con nodo central importante
red_centralidad = {
    'nodos': ['centro', 'A', 'B', 'C', 'D', 'E'],
    'aristas': [
        ('centro', 'A'), ('centro', 'B'), ('centro', 'C'),
        ('centro', 'D'), ('centro', 'E'),
        ('A', 'B'), ('C', 'D')
    ]
}

analizar_centralidades(red_centralidad)
```

---

## 3.4 Ejercicios Prácticos

### Ejercicio 1: Análisis de Red Universitaria

```python
# Red de colaboración entre departamentos universitarios
universidad = {
    'departamentos': [
        'informatica', 'matematicas', 'fisica', 'quimica', 
        'biologia', 'psicologia', 'economia', 'literatura'
    ],
    'colaboraciones': [
        ('informatica', 'matematicas'),
        ('informatica', 'fisica'),
        ('matematicas', 'fisica'),
        ('matematicas', 'economia'),
        ('fisica', 'quimica'),
        ('quimica', 'biologia'),
        ('biologia', 'psicologia'),
        ('psicologia', 'literatura'),
        ('economia', 'psicologia')
    ]
}

def analizar_universidad():
    """Realiza un análisis completo de la red universitaria"""
    
    # TODO: Implementa las siguientes funciones:
    
    def departamentos_mas_conectados():
        """Encuentra los departamentos con más colaboraciones"""
        pass
    
    def departamentos_puente():
        """Identifica departamentos que conectan diferentes áreas"""
        pass
    
    def areas_aisladas():
        """Encuentra grupos de departamentos que colaboran solo entre sí"""
        pass
    
    def proponer_nuevas_colaboraciones():
        """Sugiere nuevas colaboraciones para mejorar la conectividad"""
        pass

# Implementa el análisis completo
```

### Ejercicio 2: Red de Distribución Logística

```python
# Red de centros de distribución y rutas
logistica = {
    'centros': ['madrid', 'barcelona', 'valencia', 'sevilla', 'bilbao', 'zaragoza'],
    'rutas': [
        ('madrid', 'barcelona', {'tiempo': 6, 'costo': 400}),
        ('madrid', 'valencia', {'tiempo': 4, 'costo': 250}),
        ('madrid', 'sevilla', {'tiempo': 5, 'costo': 350}),
        ('madrid', 'zaragoza', {'tiempo': 3, 'costo': 200}),
        ('barcelona', 'zaragoza', {'tiempo': 3, 'costo': 180}),
        ('valencia', 'barcelona', {'tiempo': 3, 'costo': 220}),
        ('sevilla', 'valencia', {'tiempo': 7, 'costo': 450}),
        ('bilbao', 'zaragoza', {'tiempo': 4, 'costo': 280}),
        ('bilbao', 'madrid', {'tiempo': 5, 'costo': 320})
    ]
}

def optimizar_logistica():
    """Optimiza la red de distribución"""
    
    # TODO: Implementa:
    
    def ruta_mas_economica(origen, destino):
        """Encuentra la ruta de menor costo"""
        pass
    
    def ruta_mas_rapida(origen, destino):
        """Encuentra la ruta más rápida"""
        pass
    
    def centros_criticos():
        """Identifica centros cuya falla afectaría más la red"""
        pass
    
    def redundancia_rutas():
        """Analiza rutas alternativas disponibles"""
        pass

# Implementa las optimizaciones
```

### Ejercicio 3: Red Social con Influencia

```python
# Red social con diferentes tipos de influencia
red_influencia = {
    'usuarios': {
        'ana': {'seguidores': 1000, 'categoria': 'tech'},
        'carlos': {'seguidores': 5000, 'categoria': 'deportes'},
        'lucia': {'seguidores': 800, 'categoria': 'arte'},
        'pedro': {'seguidores': 2000, 'categoria': 'tech'},
        'sofia': {'seguidores': 3000, 'categoria': 'lifestyle'},
        'miguel': {'seguidores': 500, 'categoria': 'tech'}
    },
    'conexiones': [
        ('ana', 'carlos', {'tipo': 'menciona', 'frecuencia': 3}),
        ('ana', 'pedro', {'tipo': 'colabora', 'frecuencia': 8}),
        ('carlos', 'sofia', {'tipo': 'comparte', 'frecuencia': 5}),
        ('lucia', 'ana', {'tipo': 'menciona', 'frecuencia': 2}),
        ('pedro', 'miguel', {'tipo': 'colabora', 'frecuencia': 6}),
        ('sofia', 'lucia', {'tipo': 'comparte', 'frecuencia': 4})
    ]
}

def analizar_influencia():
    """Analiza patrones de influencia en la red social"""
    
    # TODO: Implementa:
    
    def calcular_influencia_total(usuario):
        """Calcula influencia basada en seguidores y conexiones"""
        pass
    
    def detectar_influencers_por_categoria():
        """Encuentra influencers en cada categoría"""
        pass
    
    def medir_propagacion_contenido(usuario_origen):
        """Simula cómo se propaga contenido desde un usuario"""
        pass
    
    def sugerir_colaboraciones():
        """Sugiere colaboraciones entre usuarios de diferentes categorías"""
        pass

# Implementa el análisis de influencia
```

---

## 3.5 Algoritmos Fundamentales de Recorrido

### Búsqueda en Profundidad (DFS)

```python
def dfs_recursivo(grafo, nodo_inicio, visitados=None, orden_visita=None):
    """Implementación recursiva de DFS"""
    if visitados is None:
        visitados = set()
    if orden_visita is None:
        orden_visita = []
    
    visitados.add(nodo_inicio)
    orden_visita.append(nodo_inicio)
    
    # Visitar todos los vecinos no visitados
    for arista in grafo['aristas']:
        vecino = None
        if arista[0] == nodo_inicio and arista[1] not in visitados:
            vecino = arista[1]
        elif arista[1] == nodo_inicio and arista[0] not in visitados:
            vecino = arista[0]
        
        if vecino:
            dfs_recursivo(grafo, vecino, visitados, orden_visita)
    
    return orden_visita

def dfs_iterativo(grafo, nodo_inicio):
    """Implementación iterativa de DFS usando pila"""
    visitados = set()
    pila = [nodo_inicio]
    orden_visita = []
    
    while pila:
        nodo_actual = pila.pop()
        
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            orden_visita.append(nodo_actual)
            
            # Agregar vecinos a la pila
            vecinos = []
            for arista in grafo['aristas']:
                if arista[0] == nodo_actual:
                    vecinos.append(arista[1])
                elif arista[1] == nodo_actual:
                    vecinos.append(arista[0])
            
            # Agregar en orden inverso para mantener orden alfabético
            for vecino in sorted(vecinos, reverse=True):
                if vecino not in visitados:
                    pila.append(vecino)
    
    return orden_visita

# Ejemplo de uso
grafo_ejemplo = {
    'nodos': ['A', 'B', 'C', 'D', 'E', 'F'],
    'aristas': [
        ('A', 'B'), ('A', 'C'), ('B', 'D'), 
        ('C', 'E'), ('D', 'F'), ('E', 'F')
    ]
}

print("DFS Recursivo desde A:", dfs_recursivo(grafo_ejemplo, 'A'))
print("DFS Iterativo desde A:", dfs_iterativo(grafo_ejemplo, 'A'))
```

### Búsqueda en Amplitud (BFS)

```python
def bfs(grafo, nodo_inicio):
    """Implementación de BFS usando cola"""
    from collections import deque
    
    visitados = set()
    cola = deque([nodo_inicio])
    orden_visita = []
    
    visitados.add(nodo_inicio)
    
    while cola:
        nodo_actual = cola.popleft()
        orden_visita.append(nodo_actual)
        
        # Buscar vecinos y agregarlos a la cola
        vecinos = []
        for arista in grafo['aristas']:
            if arista[0] == nodo_actual:
                vecinos.append(arista[1])
            elif arista[1] == nodo_actual:
                vecinos.append(arista[0])
        
        # Agregar vecinos no visitados en orden alfabético
        for vecino in sorted(vecinos):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    
    return orden_visita

def bfs_con_niveles(grafo, nodo_inicio):
    """BFS que también retorna el nivel de cada nodo"""
    from collections import deque
    
    visitados = {nodo_inicio: 0}
    cola = deque([(nodo_inicio, 0)])
    orden_visita = []
    
    while cola:
        nodo_actual, nivel_actual = cola.popleft()
        orden_visita.append((nodo_actual, nivel_actual))
        
        # Buscar vecinos
        for arista in grafo['aristas']:
            vecino = None
            if arista[0] == nodo_actual:
                vecino = arista[1]
            elif arista[1] == nodo_actual:
                vecino = arista[0]
            
            if vecino and vecino not in visitados:
                visitados[vecino] = nivel_actual + 1
                cola.append((vecino, nivel_actual + 1))
    
    return orden_visita

print("BFS desde A:", bfs(grafo_ejemplo, 'A'))
print("BFS con niveles desde A:")
for nodo, nivel in bfs_con_niveles(grafo_ejemplo, 'A'):
    print(f"  {nodo}: nivel {nivel}")
```

---

## 3.6 Comparación y Aplicaciones

### Cuándo Usar Cada Algoritmo

```python
def comparar_algoritmos_recorrido():
    """Compara DFS vs BFS en diferentes escenarios"""
    
    # Crear un grafo más complejo
    grafo_complejo = {
        'nodos': list('ABCDEFGHIJ'),
        'aristas': [
            ('A', 'B'), ('A', 'C'), ('A', 'D'),
            ('B', 'E'), ('B', 'F'),
            ('C', 'G'), ('C', 'H'),
            ('D', 'I'), ('D', 'J'),
            ('E', 'F'), ('G', 'H'), ('I', 'J')
        ]
    }
    
    print("Comparación de algoritmos de recorrido:")
    print("==========================================")
    
    print("DFS - Exploración en profundidad:")
    dfs_resultado = dfs_recursivo(grafo_complejo, 'A')
    print(f"  Orden: {' → '.join(dfs_resultado)}")
    
    print("\nBFS - Exploración por niveles:")
    bfs_resultado = bfs_con_niveles(grafo_complejo, 'A')
    for nivel in range(max(nivel for _, nivel in bfs_resultado) + 1):
        nodos_nivel = [nodo for nodo, n in bfs_resultado if n == nivel]
        print(f"  Nivel {nivel}: {', '.join(nodos_nivel)}")
    
    print("\nAplicaciones típicas:")
    print("DFS:")
    print("  - Detectar ciclos")
    print("  - Encontrar componentes conectados")
    print("  - Resolver laberintos")
    print("  - Análisis de dependencias")
    
    print("\nBFS:")
    print("  - Camino más corto (sin pesos)")
    print("  - Análisis de grados de separación")
    print("  - Propagación en redes sociales")
    print("  - Algoritmos de búsqueda web")

comparar_algoritmos_recorrido()
```

---

## 3.7 Resumen de Conceptos Clave

### Checklist de Conceptos Importantes

- [ ] **Tipos de grafos**
  - Dirigidos vs no dirigidos
  - Ponderados vs no ponderados
  - Multigrafos

- [ ] **Propiedades fundamentales**
  - Caminos y ciclos
  - Conectividad
  - Componentes conectados
  - Grado de nodos

- [ ] **Métricas importantes**
  - Densidad del grafo
  - Diámetro del grafo
  - Centralidad (grado, intermediación)

- [ ] **Algoritmos básicos**
  - DFS (Búsqueda en profundidad)
  - BFS (Búsqueda en amplitud)
  - Detección de ciclos
  - Componentes conectados

---

## 3.8 Preparación para el Siguiente Tema

En el próximo tema exploraremos el **modelado de datos con grafos**, incluyendo:
- Cómo identificar entidades y relaciones
- Patrones comunes de modelado
- Ejercicios prácticos de diseño
