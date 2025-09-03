# Tema 2: Bases de Datos de Grafos vs Relacionales

## Objetivos de Aprendizaje
Al finalizar este tema, los estudiantes serán capaces de:
- Identificar cuándo usar grafos vs bases de datos relacionales
- Reconocer las ventajas y limitaciones de cada enfoque
- Convertir modelos relacionales a modelos de grafos
- Implementar comparaciones prácticas en Python

---

## 2.1 Limitaciones de las Bases de Datos Relacionales con Relaciones Complejas

### Problema: Consultas con Múltiples JOINs

Cuando tenemos muchas relaciones interconectadas, las consultas SQL se vuelven complejas y lentas.

**Ejemplo: Red Social en Modelo Relacional**

```python
# Simulación de tablas relacionales en Python
usuarios_tabla = [
    {'id': 1, 'nombre': 'Ana', 'ciudad': 'Madrid'},
    {'id': 2, 'nombre': 'Carlos', 'ciudad': 'Barcelona'},
    {'id': 3, 'nombre': 'Lucia', 'ciudad': 'Madrid'},
    {'id': 4, 'nombre': 'Pedro', 'ciudad': 'Valencia'},
    {'id': 5, 'nombre': 'Sofia', 'ciudad': 'Sevilla'}
]

amistades_tabla = [
    {'usuario1_id': 1, 'usuario2_id': 2, 'fecha': '2023-01-15'},
    {'usuario1_id': 1, 'usuario2_id': 3, 'fecha': '2023-02-10'},
    {'usuario1_id': 2, 'usuario2_id': 4, 'fecha': '2023-01-20'},
    {'usuario1_id': 3, 'usuario2_id': 5, 'fecha': '2023-03-05'},
    {'usuario1_id': 4, 'usuario2_id': 5, 'fecha': '2023-02-28'}
]

# Consulta compleja: "Amigos de amigos de Ana que viven en Madrid"
def amigos_de_amigos_madrid_relacional():
    # Paso 1: Encontrar amigos de Ana (ID = 1)
    amigos_ana = []
    for amistad in amistades_tabla:
        if amistad['usuario1_id'] == 1:
            amigos_ana.append(amistad['usuario2_id'])
        elif amistad['usuario2_id'] == 1:
            amigos_ana.append(amistad['usuario1_id'])
    
    # Paso 2: Encontrar amigos de los amigos de Ana
    amigos_de_amigos = []
    for amigo_id in amigos_ana:
        for amistad in amistades_tabla:
            if amistad['usuario1_id'] == amigo_id:
                amigos_de_amigos.append(amistad['usuario2_id'])
            elif amistad['usuario2_id'] == amigo_id:
                amigos_de_amigos.append(amistad['usuario1_id'])
    
    # Paso 3: Filtrar por Madrid y excluir a Ana y sus amigos directos
    resultado = []
    excluir = [1] + amigos_ana
    for usuario_id in amigos_de_amigos:
        if usuario_id not in excluir:
            # Buscar datos del usuario
            for usuario in usuarios_tabla:
                if usuario['id'] == usuario_id and usuario['ciudad'] == 'Madrid':
                    resultado.append(usuario['nombre'])
    
    return list(set(resultado))  # Eliminar duplicados

print("Modelo Relacional - Amigos de amigos en Madrid:")
print(amigos_de_amigos_madrid_relacional())
```

### El Mismo Problema con Grafos

```python
# Representación como grafo
red_social_grafo = {
    'usuarios': {
        'ana': {'ciudad': 'Madrid'},
        'carlos': {'ciudad': 'Barcelona'},
        'lucia': {'ciudad': 'Madrid'},
        'pedro': {'ciudad': 'Valencia'},
        'sofia': {'ciudad': 'Sevilla'}
    },
    'amistades': [
        ('ana', 'carlos'),
        ('ana', 'lucia'),
        ('carlos', 'pedro'),
        ('lucia', 'sofia'),
        ('pedro', 'sofia')
    ]
}

def amigos_de_amigos_madrid_grafo():
    # Paso 1: Amigos directos de Ana
    amigos_directos = []
    for amistad in red_social_grafo['amistades']:
        if amistad[0] == 'ana':
            amigos_directos.append(amistad[1])
        elif amistad[1] == 'ana':
            amigos_directos.append(amistad[0])
    
    # Paso 2: Amigos de los amigos
    amigos_de_amigos = []
    for amigo in amigos_directos:
        for amistad in red_social_grafo['amistades']:
            if amistad[0] == amigo and amistad[1] not in ['ana'] + amigos_directos:
                if red_social_grafo['usuarios'][amistad[1]]['ciudad'] == 'Madrid':
                    amigos_de_amigos.append(amistad[1])
            elif amistad[1] == amigo and amistad[0] not in ['ana'] + amigos_directos:
                if red_social_grafo['usuarios'][amistad[0]]['ciudad'] == 'Madrid':
                    amigos_de_amigos.append(amistad[0])
    
    return list(set(amigos_de_amigos))

print("Modelo de Grafos - Amigos de amigos en Madrid:")
print(amigos_de_amigos_madrid_grafo())
```

---

## 2.2 Ventajas de las Bases de Datos de Grafos

### 1. Representación Natural de Relaciones

```python
# Ejemplo: Sistema de Recomendaciones de Productos

# Modelo Relacional (complejo)
productos_tabla = [
    {'id': 1, 'nombre': 'Laptop Gaming', 'categoria': 'Electrónicos'},
    {'id': 2, 'nombre': 'Mouse Gamer', 'categoria': 'Accesorios'},
    {'id': 3, 'nombre': 'Teclado Mecánico', 'categoria': 'Accesorios'},
    {'id': 4, 'nombre': 'Monitor 4K', 'categoria': 'Electrónicos'}
]

compras_tabla = [
    {'usuario_id': 1, 'producto_id': 1},
    {'usuario_id': 1, 'producto_id': 2},
    {'usuario_id': 2, 'producto_id': 1},
    {'usuario_id': 2, 'producto_id': 3},
    {'usuario_id': 3, 'producto_id': 2},
    {'usuario_id': 3, 'producto_id': 3}
]

# Modelo de Grafos (intuitivo)
tienda_grafo = {
    'nodos': {
        'usuario_1': {'tipo': 'usuario', 'nombre': 'Ana'},
        'usuario_2': {'tipo': 'usuario', 'nombre': 'Carlos'},
        'usuario_3': {'tipo': 'usuario', 'nombre': 'Lucia'},
        'laptop_gaming': {'tipo': 'producto', 'categoria': 'Electrónicos'},
        'mouse_gamer': {'tipo': 'producto', 'categoria': 'Accesorios'},
        'teclado_mecanico': {'tipo': 'producto', 'categoria': 'Accesorios'},
        'monitor_4k': {'tipo': 'producto', 'categoria': 'Electrónicos'}
    },
    'relaciones': [
        ('usuario_1', 'laptop_gaming', 'COMPRO'),
        ('usuario_1', 'mouse_gamer', 'COMPRO'),
        ('usuario_2', 'laptop_gaming', 'COMPRO'),
        ('usuario_2', 'teclado_mecanico', 'COMPRO'),
        ('usuario_3', 'mouse_gamer', 'COMPRO'),
        ('usuario_3', 'teclado_mecanico', 'COMPRO'),
        ('laptop_gaming', 'mouse_gamer', 'COMPATIBLE_CON'),
        ('laptop_gaming', 'teclado_mecanico', 'COMPATIBLE_CON'),
        ('laptop_gaming', 'monitor_4k', 'COMPATIBLE_CON')
    ]
}

def recomendar_productos(usuario, grafo):
    """Recomienda productos basado en compras de usuarios similares"""
    # Productos que compró el usuario
    productos_usuario = []
    for rel in grafo['relaciones']:
        if rel[0] == usuario and rel[2] == 'COMPRO':
            productos_usuario.append(rel[1])
    
    # Usuarios que compraron productos similares
    usuarios_similares = []
    for producto in productos_usuario:
        for rel in grafo['relaciones']:
            if rel[1] == producto and rel[2] == 'COMPRO' and rel[0] != usuario:
                usuarios_similares.append(rel[0])
    
    # Productos que compraron usuarios similares
    recomendaciones = []
    for usuario_similar in set(usuarios_similares):
        for rel in grafo['relaciones']:
            if rel[0] == usuario_similar and rel[2] == 'COMPRO':
                if rel[1] not in productos_usuario:
                    recomendaciones.append(rel[1])
    
    return list(set(recomendaciones))

print("Recomendaciones para usuario_1:")
print(recomendar_productos('usuario_1', tienda_grafo))
```

### 2. Consultas Más Intuitivas

```python
# Ejemplo: Análisis de Influencia en Redes Sociales

def encontrar_influencers(grafo, min_conexiones=3):
    """Encuentra usuarios con muchas conexiones"""
    conteo_conexiones = {}
    
    for relacion in grafo['amistades']:
        # Contar conexiones para cada usuario
        for usuario in [relacion[0], relacion[1]]:
            conteo_conexiones[usuario] = conteo_conexiones.get(usuario, 0) + 1
    
    # Filtrar influencers
    influencers = {usuario: conexiones 
                  for usuario, conexiones in conteo_conexiones.items() 
                  if conexiones >= min_conexiones}
    
    return influencers

def analizar_comunidades(grafo):
    """Encuentra grupos de usuarios conectados"""
    visitados = set()
    comunidades = []
    
    def explorar_comunidad(usuario, comunidad_actual):
        if usuario in visitados:
            return
        
        visitados.add(usuario)
        comunidad_actual.append(usuario)
        
        # Buscar amigos del usuario
        for relacion in grafo['amistades']:
            if relacion[0] == usuario:
                explorar_comunidad(relacion[1], comunidad_actual)
            elif relacion[1] == usuario:
                explorar_comunidad(relacion[0], comunidad_actual)
    
    # Explorar cada usuario no visitado
    for usuario in grafo['usuarios']:
        if usuario not in visitados:
            comunidad = []
            explorar_comunidad(usuario, comunidad)
            if len(comunidad) > 1:
                comunidades.append(comunidad)
    
    return comunidades

# Análisis de la red social
print("Influencers en la red:")
print(encontrar_influencers(red_social_grafo))

print("\nComunidades detectadas:")
print(analizar_comunidades(red_social_grafo))
```

### 3. Performance en Consultas Complejas

```python
import time

def medir_performance_busqueda():
    """Compara performance entre modelos relacionales y grafos"""
    
    # Crear datos más grandes para la prueba
    usuarios_grandes = []
    amistades_grandes = []
    
    # Generar 1000 usuarios
    for i in range(1000):
        usuarios_grandes.append({
            'id': i,
            'nombre': f'Usuario_{i}',
            'ciudad': ['Madrid', 'Barcelona', 'Valencia'][i % 3]
        })
    
    # Generar 5000 amistades aleatorias
    import random
    for _ in range(5000):
        u1, u2 = random.sample(range(1000), 2)
        amistades_grandes.append({'usuario1_id': u1, 'usuario2_id': u2})
    
    # Modelo relacional: buscar amigos de amigos
    start_time = time.time()
    
    def busqueda_relacional(user_id):
        # Buscar amigos directos
        amigos = []
        for amistad in amistades_grandes:
            if amistad['usuario1_id'] == user_id:
                amigos.append(amistad['usuario2_id'])
            elif amistad['usuario2_id'] == user_id:
                amigos.append(amistad['usuario1_id'])
        
        # Buscar amigos de amigos
        amigos_de_amigos = []
        for amigo in amigos:
            for amistad in amistades_grandes:
                if amistad['usuario1_id'] == amigo:
                    amigos_de_amigos.append(amistad['usuario2_id'])
                elif amistad['usuario2_id'] == amigo:
                    amigos_de_amigos.append(amistad['usuario1_id'])
        
        return len(set(amigos_de_amigos))
    
    resultado_rel = busqueda_relacional(0)
    tiempo_relacional = time.time() - start_time
    
    print(f"Modelo Relacional: {resultado_rel} amigos de amigos en {tiempo_relacional:.4f} segundos")
    
    # Modelo de grafos usando diccionario de adyacencia (más eficiente)
    start_time = time.time()
    
    # Pre-procesar para crear índice de adyacencia
    grafo_adyacencia = {}
    for amistad in amistades_grandes:
        u1, u2 = amistad['usuario1_id'], amistad['usuario2_id']
        if u1 not in grafo_adyacencia:
            grafo_adyacencia[u1] = []
        if u2 not in grafo_adyacencia:
            grafo_adyacencia[u2] = []
        grafo_adyacencia[u1].append(u2)
        grafo_adyacencia[u2].append(u1)
    
    def busqueda_grafo(user_id):
        if user_id not in grafo_adyacencia:
            return 0
        
        amigos = grafo_adyacencia[user_id]
        amigos_de_amigos = set()
        
        for amigo in amigos:
            if amigo in grafo_adyacencia:
                amigos_de_amigos.update(grafo_adyacencia[amigo])
        
        # Excluir al usuario y sus amigos directos
        amigos_de_amigos.discard(user_id)
        amigos_de_amigos.difference_update(amigos)
        
        return len(amigos_de_amigos)
    
    resultado_grafo = busqueda_grafo(0)
    tiempo_grafo = time.time() - start_time
    
    print(f"Modelo de Grafos: {resultado_grafo} amigos de amigos en {tiempo_grafo:.4f} segundos")
    print(f"Mejora de performance: {tiempo_relacional/tiempo_grafo:.2f}x más rápido")

# Ejecutar comparación de performance
medir_performance_busqueda()
```

---

## 2.3 Casos de Uso Comparativos

### Cuándo Usar Grafos

```python
# 1. DETECCIÓN DE FRAUDE
transacciones_sospechosas = {
    'cuentas': {
        'cuenta_1': {'titular': 'Juan Pérez', 'tipo': 'personal'},
        'cuenta_2': {'titular': 'María García', 'tipo': 'personal'},
        'cuenta_3': {'titular': 'Empresa XYZ', 'tipo': 'empresarial'},
        'cuenta_4': {'titular': 'Carlos López', 'tipo': 'personal'}
    },
    'transacciones': [
        ('cuenta_1', 'cuenta_2', {'monto': 1000, 'fecha': '2024-01-15'}),
        ('cuenta_2', 'cuenta_3', {'monto': 950, 'fecha': '2024-01-15'}),
        ('cuenta_3', 'cuenta_4', {'monto': 900, 'fecha': '2024-01-16'}),
        ('cuenta_4', 'cuenta_1', {'monto': 850, 'fecha': '2024-01-16'})
    ]
}

def detectar_ciclos_sospechosos(grafo_transacciones):
    """Detecta ciclos de transacciones que podrían indicar lavado de dinero"""
    def encontrar_ciclo(cuenta_inicio, camino_actual, visitados):
        for transaccion in grafo_transacciones['transacciones']:
            if transaccion[0] == camino_actual[-1]:  # Desde la última cuenta
                destino = transaccion[1]
                if destino == cuenta_inicio and len(camino_actual) > 2:
                    # Encontramos un ciclo
                    return camino_actual + [destino]
                elif destino not in visitados and len(camino_actual) < 5:
                    # Continuar explorando
                    nuevo_camino = encontrar_ciclo(
                        cuenta_inicio, 
                        camino_actual + [destino], 
                        visitados | {destino}
                    )
                    if nuevo_camino:
                        return nuevo_camino
        return None
    
    ciclos_detectados = []
    for cuenta in grafo_transacciones['cuentas']:
        ciclo = encontrar_ciclo(cuenta, [cuenta], {cuenta})
        if ciclo:
            ciclos_detectados.append(ciclo)
    
    return ciclos_detectados

print("Ciclos sospechosos detectados:")
for ciclo in detectar_ciclos_sospechosos(transacciones_sospechosas):
    print(f"  {' -> '.join(ciclo)}")
```

### Cuándo Usar Bases de Datos Relacionales

```python
# Para datos tabulares con estructura fija y consultas OLAP
inventario_tienda = {
    'productos': [
        {'id': 1, 'nombre': 'Laptop', 'precio': 1200, 'categoria': 'Electrónicos', 'stock': 15},
        {'id': 2, 'nombre': 'Mouse', 'precio': 25, 'categoria': 'Accesorios', 'stock': 100},
        {'id': 3, 'nombre': 'Teclado', 'precio': 80, 'categoria': 'Accesorios', 'stock': 50}
    ],
    'ventas': [
        {'fecha': '2024-01-15', 'producto_id': 1, 'cantidad': 2, 'total': 2400},
        {'fecha': '2024-01-15', 'producto_id': 2, 'cantidad': 5, 'total': 125},
        {'fecha': '2024-01-16', 'producto_id': 3, 'cantidad': 3, 'total': 240}
    ]
}

def reporte_ventas_relacional():
    """Ejemplo de consulta típica relacional: agregaciones y reportes"""
    # Ventas por categoría
    ventas_por_categoria = {}
    for venta in inventario_tienda['ventas']:
        # Buscar producto
        producto = next(p for p in inventario_tienda['productos'] 
                       if p['id'] == venta['producto_id'])
        categoria = producto['categoria']
        
        if categoria not in ventas_por_categoria:
            ventas_por_categoria[categoria] = {'cantidad': 0, 'total': 0}
        
        ventas_por_categoria[categoria]['cantidad'] += venta['cantidad']
        ventas_por_categoria[categoria]['total'] += venta['total']
    
    return ventas_por_categoria

print("Reporte de ventas por categoría:")
for categoria, datos in reporte_ventas_relacional().items():
    print(f"  {categoria}: {datos['cantidad']} unidades, ${datos['total']}")
```

---

## 2.4 Flexibilidad del Esquema

### Problema con Esquemas Rígidos

```python
# En bases relacionales, cambiar el esquema es complejo
# Ejemplo: Agregar nuevo tipo de relación requiere modificar tablas

# Esquema original: solo amistades
red_original = {
    'usuarios': [
        {'id': 1, 'nombre': 'Ana'},
        {'id': 2, 'nombre': 'Carlos'}
    ],
    'amistades': [
        {'usuario1_id': 1, 'usuario2_id': 2}
    ]
}

# ¿Cómo agregar relaciones de trabajo sin romper el esquema?
# En SQL necesitaríamos nueva tabla o modificar la existente

# En grafos, es natural
red_flexible = {
    'nodos': {
        'ana': {'tipo': 'persona', 'nombre': 'Ana', 'edad': 25},
        'carlos': {'tipo': 'persona', 'nombre': 'Carlos', 'edad': 30},
        'empresa_abc': {'tipo': 'empresa', 'nombre': 'ABC Corp', 'sector': 'Tecnología'}
    },
    'relaciones': [
        ('ana', 'carlos', 'AMIGO_DE'),
        ('ana', 'empresa_abc', 'TRABAJA_EN'),
        ('carlos', 'empresa_abc', 'TRABAJA_EN')
    ]
}

def agregar_nueva_relacion(grafo, nodo1, nodo2, tipo_relacion, propiedades=None):
    """Agregar cualquier tipo de relación dinámicamente"""
    relacion = (nodo1, nodo2, tipo_relacion)
    if propiedades:
        relacion = relacion + (propiedades,)
    grafo['relaciones'].append(relacion)

# Fácil agregar nuevos tipos de relaciones
agregar_nueva_relacion(red_flexible, 'ana', 'carlos', 'COLABORA_CON', 
                      {'proyecto': 'Sistema XYZ', 'desde': '2024-01-01'})

print("Red flexible con múltiples tipos de relaciones:")
for relacion in red_flexible['relaciones']:
    print(f"  {relacion}")
```

---

## 2.5 Ejercicios Prácticos

### Ejercicio 1: Convertir Modelo Relacional a Grafo

```python
# Dado este modelo relacional de una biblioteca:
biblioteca_relacional = {
    'autores': [
        {'id': 1, 'nombre': 'Gabriel García Márquez', 'nacionalidad': 'Colombiana'},
        {'id': 2, 'nombre': 'Isabel Allende', 'nacionalidad': 'Chilena'},
        {'id': 3, 'nombre': 'Mario Vargas Llosa', 'nacionalidad': 'Peruana'}
    ],
    'libros': [
        {'id': 1, 'titulo': 'Cien años de soledad', 'autor_id': 1, 'año': 1967},
        {'id': 2, 'titulo': 'La casa de los espíritus', 'autor_id': 2, 'año': 1982},
        {'id': 3, 'titulo': 'Conversación en La Catedral', 'autor_id': 3, 'año': 1969}
    ],
    'usuarios': [
        {'id': 1, 'nombre': 'Ana Pérez', 'email': 'ana@email.com'},
        {'id': 2, 'nombre': 'Carlos López', 'email': 'carlos@email.com'}
    ],
    'prestamos': [
        {'usuario_id': 1, 'libro_id': 1, 'fecha_prestamo': '2024-01-15', 'fecha_devolucion': None},
        {'usuario_id': 2, 'libro_id': 2, 'fecha_prestamo': '2024-01-10', 'fecha_devolucion': '2024-01-25'}
    ]
}

# TODO: Convierte este modelo a un grafo
biblioteca_grafo = {
    'nodos': {
        # Completa aquí
    },
    'relaciones': [
        # Completa aquí
    ]
}

def encontrar_libros_disponibles(grafo):
    """Encuentra libros que no están prestados actualmente"""
    # Implementa esta función
    pass

def recomendar_por_autor(grafo, usuario):
    """Recomienda libros basado en autores que el usuario ha leído"""
    # Implementa esta función
    pass
```

### Ejercicio 2: Sistema de Transporte Multimodal

```python
# Modela un sistema que incluye metro, autobús y bicicleta compartida
transporte_multimodal = {
    'nodos': {
        # Estaciones de metro
        'metro_sol': {'tipo': 'estacion_metro', 'lineas': ['1', '2', '3']},
        'metro_atocha': {'tipo': 'estacion_metro', 'lineas': ['1']},
        
        # Paradas de autobús
        'bus_plaza_mayor': {'tipo': 'parada_bus', 'lineas': ['25', '39']},
        'bus_retiro': {'tipo': 'parada_bus', 'lineas': ['19']},
        
        # Estaciones de bicis
        'bici_centro': {'tipo': 'estacion_bici', 'bicis_disponibles': 12},
        'bici_parque': {'tipo': 'estacion_bici', 'bicis_disponibles': 8}
    },
    'relaciones': [
        # Conexiones directas de transporte
        ('metro_sol', 'metro_atocha', 'METRO_LINEA_1'),
        ('bus_plaza_mayor', 'bus_retiro', 'BUS_LINEA_25'),
        
        # Conexiones de cambio modal (a pie)
        ('metro_sol', 'bus_plaza_mayor', 'CAMINANDO'),
        ('metro_atocha', 'bici_centro', 'CAMINANDO'),
        ('bus_retiro', 'bici_parque', 'CAMINANDO')
    ]
}

def planificar_ruta_multimodal(origen, destino, grafo):
    """Planifica una ruta usando diferentes medios de transporte"""
    # TODO: Implementa algoritmo de búsqueda de rutas
    # Considera diferentes tipos de transporte y transbordos
    pass

def calcular_tiempo_ruta(ruta, grafo):
    """Calcula el tiempo total de una ruta multimodal"""
    # TODO: Asigna tiempos diferentes según el tipo de transporte
    # Metro: 2 min entre estaciones + 1 min transbordo
    # Bus: 3 min entre paradas + 2 min transbordo  
    # Bici: 5 min entre estaciones + 3 min recoger/dejar
    # Caminando: 8 min
    pass
```

---

## 2.6 Comparación de Performance

### Benchmark: Análisis de Redes Sociales

```python
def benchmark_consultas_complejas():
    """Compara performance en consultas de múltiples grados de separación"""
    
    # Generar red social grande
    import random
    
    # Crear 500 usuarios
    usuarios_grandes = {f'usuario_{i}': {'ciudad': random.choice(['Madrid', 'Barcelona', 'Valencia'])} 
                       for i in range(500)}
    
    # Crear 2000 conexiones aleatorias
    conexiones_grandes = []
    for _ in range(2000):
        u1, u2 = random.sample(list(usuarios_grandes.keys()), 2)
        conexiones_grandes.append((u1, u2))
    
    red_grande = {'usuarios': usuarios_grandes, 'amistades': conexiones_grandes}
    
    # Consulta: "Encontrar todos los usuarios a exactamente 3 grados de separación"
    def grados_separacion_ingenuo(usuario_inicio, grados, red):
        """Método ingenuo sin optimización"""
        nivel_actual = {usuario_inicio}
        visitados = {usuario_inicio}
        
        for grado in range(grados):
            siguiente_nivel = set()
            for usuario in nivel_actual:
                for amistad in red['amistades']:
                    vecino = None
                    if amistad[0] == usuario:
                        vecino = amistad[1]
                    elif amistad[1] == usuario:
                        vecino = amistad[0]
                    
                    if vecino and vecino not in visitados:
                        siguiente_nivel.add(vecino)
                        visitados.add(vecino)
            
            nivel_actual = siguiente_nivel
            if not nivel_actual:
                break
        
        return nivel_actual
    
    def grados_separacion_optimizado(usuario_inicio, grados, red):
        """Método optimizado con índice de adyacencia"""
        # Pre-computar índice de adyacencia
        adyacencia = {}
        for usuario in red['usuarios']:
            adyacencia[usuario] = []
        
        for amistad in red['amistades']:
            adyacencia[amistad[0]].append(amistad[1])
            adyacencia[amistad[1]].append(amistad[0])
        
        # BFS optimizado
        nivel_actual = {usuario_inicio}
        visitados = {usuario_inicio}
        
        for grado in range(grados):
            siguiente_nivel = set()
            for usuario in nivel_actual:
                for vecino in adyacencia[usuario]:
                    if vecino not in visitados:
                        siguiente_nivel.add(vecino)
                        visitados.add(vecino)
            
            nivel_actual = siguiente_nivel
            if not nivel_actual:
                break
        
        return nivel_actual
    
    # Medir performance
    import time
    usuario_test = list(usuarios_grandes.keys())[0]
    
    start = time.time()
    resultado_ingenuo = grados_separacion_ingenuo(usuario_test, 3, red_grande)
    tiempo_ingenuo = time.time() - start
    
    start = time.time()
    resultado_optimizado = grados_separacion_optimizado(usuario_test, 3, red_grande)
    tiempo_optimizado = time.time() - start
    
    print(f"Método ingenuo: {len(resultado_ingenuo)} usuarios en {tiempo_ingenuo:.4f}s")
    print(f"Método optimizado: {len(resultado_optimizado)} usuarios en {tiempo_optimizado:.4f}s")
    print(f"Mejora: {tiempo_ingenuo/tiempo_optimizado:.2f}x más rápido")

benchmark_consultas_complejas()
```

---

## 2.7 Resumen y Decisión

### Cuándo Usar Grafos

✅ **Relaciones complejas y dinámicas**
- Redes sociales, sistemas de recomendación
- Detección de fraude, análisis de influencia
- Rutas y navegación

✅ **Consultas de conexión y caminos**
- "Amigos de amigos que..."
- "¿Cómo está conectado X con Y?"
- "¿Qué influencia tiene X en Y?"

✅ **Esquemas flexibles y evolutivos**
- Nuevos tipos de relaciones frecuentes
- Propiedades variables por entidad

### Cuándo Usar Bases de Datos Relacionales

✅ **Datos tabulares estructurados**
- Inventarios, facturación, contabilidad
- Reportes y agregaciones (OLAP)
- Transacciones ACID críticas

✅ **Consultas de agregación**
- SUM, COUNT, GROUP BY, etc.
- Reportes financieros y estadísticas
- Análisis temporal de métricas

---

## 2.8 Preparación para el Siguiente Tema

En el próximo tema exploraremos la **teoría básica de grafos**, incluyendo:
- Tipos de grafos (dirigidos, no dirigidos, ponderados)
- Conceptos fundamentales (caminos, ciclos, conectividad)
- Propiedades importantes para el análisis
