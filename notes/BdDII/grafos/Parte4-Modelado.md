# Tema 4: Modelado de Datos con Grafos

## Objetivos de Aprendizaje
Al finalizar este tema, los estudiantes serán capaces de:
- Identificar qué elementos deben ser nodos vs relaciones
- Diseñar esquemas de grafos para diferentes dominios
- Implementar patrones comunes de modelado
- Optimizar modelos para consultas específicas

---

## 4.1 Principios Fundamentales del Modelado

### ¿Qué debe ser un Nodo?

```python
# REGLA GENERAL: Los nodos representan ENTIDADES con identidad propia

# ❌ INCORRECTO: Atributos como nodos
modelo_incorrecto = {
    'nodos': {
        'juan_perez': {'tipo': 'persona'},
        '25_años': {'tipo': 'edad'},          # ❌ Edad no es una entidad
        'madrid': {'tipo': 'ciudad'},
        'ingeniero': {'tipo': 'profesion'}    # ❌ Profesión como nodo genérico
    },
    'relaciones': [
        ('juan_perez', '25_años', 'TIENE_EDAD'),
        ('juan_perez', 'madrid', 'VIVE_EN'),
        ('juan_perez', 'ingeniero', 'TRABAJA_COMO')
    ]
}

# ✅ CORRECTO: Solo entidades con identidad como nodos
modelo_correcto = {
    'nodos': {
        'juan_perez': {
            'tipo': 'persona',
            'edad': 25,                       # ✅ Edad como propiedad
            'profesion': 'ingeniero'          # ✅ Profesión como propiedad
        },
        'madrid': {
            'tipo': 'ciudad',
            'poblacion': 3200000,
            'pais': 'España'
        }
    },
    'relaciones': [
        ('juan_perez', 'madrid', 'VIVE_EN', {'desde': '2020-01-01'})
    ]
}

def validar_modelo(modelo):
    """Valida si el modelo sigue buenas prácticas"""
    problemas = []
    
    for nodo_id, propiedades in modelo['nodos'].items():
        # Verificar que los nodos tengan identidad propia
        if 'tipo' not in propiedades:
            problemas.append(f"Nodo {nodo_id} sin tipo definido")
        
        # Verificar nombres de nodos descriptivos
        if nodo_id.isdigit():
            problemas.append(f"Nodo {nodo_id} tiene ID numérico poco descriptivo")
    
    # Verificar relaciones significativas
    for relacion in modelo['relaciones']:
        if len(relacion) < 3:
            problemas.append(f"Relación incompleta: {relacion}")
    
    return problemas

print("Problemas en modelo incorrecto:")
for problema in validar_modelo(modelo_incorrecto):
    print(f"  - {problema}")

print("\nProblemas en modelo correcto:")
problemas_correcto = validar_modelo(modelo_correcto)
if not problemas_correcto:
    print("  - ¡Ningún problema detectado!")
else:
    for problema in problemas_correcto:
        print(f"  - {problema}")
```

### ¿Qué debe ser una Relación?

```python
# REGLA GENERAL: Las relaciones representan INTERACCIONES o ASOCIACIONES

def ejemplos_relaciones():
    """Ejemplos de cómo modelar diferentes tipos de relaciones"""
    
    # 1. RELACIONES SIMPLES: Solo conectan entidades
    relaciones_simples = [
        ('ana', 'carlos', 'AMIGO_DE'),
        ('carlos', 'empresa_abc', 'TRABAJA_EN'),
        ('madrid', 'españa', 'UBICADO_EN')
    ]
    
    # 2. RELACIONES CON PROPIEDADES: Información adicional sobre la relación
    relaciones_con_propiedades = [
        ('ana', 'carlos', 'AMIGO_DE', {
            'desde': '2020-03-15',
            'intensidad': 'alta',
            'como_se_conocieron': 'universidad'
        }),
        ('carlos', 'empresa_abc', 'TRABAJA_EN', {
            'posicion': 'desarrollador senior',
            'desde': '2022-01-01',
            'salario': 45000,
            'modalidad': 'remoto'
        })
    ]
    
    # 3. RELACIONES TEMPORALES: Que cambian en el tiempo
    relaciones_temporales = [
        ('pedro', 'universidad_madrid', 'ESTUDIO_EN', {
            'desde': '2018-09-01',
            'hasta': '2022-06-30',
            'titulo': 'Ingeniería Informática',
            'nota_media': 8.5
        }),
        ('lucia', 'empresa_xyz', 'TRABAJO_EN', {
            'desde': '2020-01-15',
            'hasta': '2023-12-31',
            'motivo_salida': 'mejor_oportunidad'
        })
    ]
    
    return {
        'simples': relaciones_simples,
        'con_propiedades': relaciones_con_propiedades,
        'temporales': relaciones_temporales
    }

# Ejemplo práctico: Sistema de gestión académica
sistema_academico = {
    'nodos': {
        # Estudiantes
        'ana_garcia': {
            'tipo': 'estudiante',
            'edad': 20,
            'email': 'ana.garcia@universidad.edu'
        },
        'carlos_lopez': {
            'tipo': 'estudiante',
            'edad': 22,
            'email': 'carlos.lopez@universidad.edu'
        },
        
        # Profesores
        'prof_martinez': {
            'tipo': 'profesor',
            'departamento': 'Informática',
            'años_experiencia': 15
        },
        
        # Cursos
        'algoritmos_2024': {
            'tipo': 'curso',
            'nombre': 'Algoritmos y Estructuras de Datos',
            'creditos': 6,
            'semestre': '2024-1'
        },
        'bases_datos_2024': {
            'tipo': 'curso',
            'nombre': 'Bases de Datos',
            'creditos': 4,
            'semestre': '2024-1'
        }
    },
    'relaciones': [
        # Inscripciones de estudiantes
        ('ana_garcia', 'algoritmos_2024', 'INSCRITO_EN', {
            'fecha_inscripcion': '2024-01-15',
            'nota_final': None,  # Aún no terminado
            'asistencia': 0.95
        }),
        ('carlos_lopez', 'algoritmos_2024', 'INSCRITO_EN', {
            'fecha_inscripcion': '2024-01-10',
            'nota_final': 8.5,
            'asistencia': 0.88
        }),
        
        # Profesores que dictan cursos
        ('prof_martinez', 'algoritmos_2024', 'DICTA', {
            'horario': ['lunes 10:00-12:00', 'miércoles 14:00-16:00'],
            'aula': 'Lab-203'
        }),
        ('prof_martinez', 'bases_datos_2024', 'DICTA', {
            'horario': ['martes 08:00-10:00'],
            'aula': 'Aula-305'
        })
    ]
}

def consultas_academicas(sistema):
    """Ejemplos de consultas típicas en el sistema académico"""
    
    def estudiantes_de_curso(curso_id):
        """Encuentra todos los estudiantes inscritos en un curso"""
        estudiantes = []
        for rel in sistema['relaciones']:
            if rel[1] == curso_id and rel[2] == 'INSCRITO_EN':
                estudiante_info = sistema['nodos'][rel[0]].copy()
                estudiante_info['id'] = rel[0]
                if len(rel) > 3:  # Tiene propiedades
                    estudiante_info.update(rel[3])
                estudiantes.append(estudiante_info)
        return estudiantes
    
    def cursos_de_profesor(profesor_id):
        """Encuentra todos los cursos que dicta un profesor"""
        cursos = []
        for rel in sistema['relaciones']:
            if rel[0] == profesor_id and rel[2] == 'DICTA':
                curso_info = sistema['nodos'][rel[1]].copy()
                curso_info['id'] = rel[1]
                if len(rel) > 3:
                    curso_info.update(rel[3])
                cursos.append(curso_info)
        return cursos
    
    def promedio_curso(curso_id):
        """Calcula el promedio de notas de un curso"""
        notas = []
        for rel in sistema['relaciones']:
            if rel[1] == curso_id and rel[2] == 'INSCRITO_EN' and len(rel) > 3:
                if rel[3].get('nota_final') is not None:
                    notas.append(rel[3]['nota_final'])
        
        return sum(notas) / len(notas) if notas else None
    
    # Ejecutar consultas de ejemplo
    print("Estudiantes en Algoritmos 2024:")
    for estudiante in estudiantes_de_curso('algoritmos_2024'):
        nota = estudiante.get('nota_final', 'En progreso')
        print(f"  - {estudiante['id']}: {nota}")
    
    print(f"\nCursos del Prof. Martínez:")
    for curso in cursos_de_profesor('prof_martinez'):
        print(f"  - {curso['nombre']} ({curso['id']})")
    
    promedio = promedio_curso('algoritmos_2024')
    print(f"\nPromedio en Algoritmos 2024: {promedio if promedio else 'Sin notas finales'}")

consultas_academicas(sistema_academico)
```

---

## 4.2 Patrones Comunes de Modelado

### Patrón 1: Relaciones Jerárquicas (Árboles)

```python
def modelar_jerarquia_empresarial():
    """Modela la estructura organizacional de una empresa"""
    
    empresa = {
        'empleados': {
            'ceo_ana': {
                'tipo': 'empleado',
                'nombre': 'Ana Rodríguez',
                'posicion': 'CEO',
                'nivel': 1
            },
            'cto_carlos': {
                'tipo': 'empleado',
                'nombre': 'Carlos Mendoza',
                'posicion': 'CTO',
                'nivel': 2
            },
            'cfo_lucia': {
                'tipo': 'empleado',
                'nombre': 'Lucía Santos',
                'posicion': 'CFO',
                'nivel': 2
            },
            'dev_senior_pedro': {
                'tipo': 'empleado',
                'nombre': 'Pedro García',
                'posicion': 'Senior Developer',
                'nivel': 3
            },
            'dev_junior_sofia': {
                'tipo': 'empleado',
                'nombre': 'Sofía Martín',
                'posicion': 'Junior Developer',
                'nivel': 4
            },
            'contador_miguel': {
                'tipo': 'empleado',
                'nombre': 'Miguel López',
                'posicion': 'Contador',
                'nivel': 3
            }
        },
        'relaciones': [
            # Estructura jerárquica
            ('ceo_ana', 'cto_carlos', 'SUPERVISA'),
            ('ceo_ana', 'cfo_lucia', 'SUPERVISA'),
            ('cto_carlos', 'dev_senior_pedro', 'SUPERVISA'),
            ('dev_senior_pedro', 'dev_junior_sofia', 'SUPERVISA'),
            ('cfo_lucia', 'contador_miguel', 'SUPERVISA'),
            
            # Relaciones de colaboración
            ('dev_senior_pedro', 'contador_miguel', 'COLABORA_CON'),
            ('cto_carlos', 'cfo_lucia', 'COORDINA_CON')
        ]
    }
    
    def encontrar_subordinados(jefe_id, empresa):
        """Encuentra todos los subordinados de un jefe (directos e indirectos)"""
        subordinados_directos = []
        for rel in empresa['relaciones']:
            if rel[0] == jefe_id and rel[2] == 'SUPERVISA':
                subordinados_directos.append(rel[1])
        
        todos_subordinados = subordinados_directos.copy()
        for subordinado in subordinados_directos:
            todos_subordinados.extend(encontrar_subordinados(subordinado, empresa))
        
        return todos_subordinados
    
    def encontrar_jefe(empleado_id, empresa):
        """Encuentra el jefe directo de un empleado"""
        for rel in empresa['relaciones']:
            if rel[1] == empleado_id and rel[2] == 'SUPERVISA':
                return rel[0]
        return None
    
    def calcular_profundidad_jerarquica(empresa):
        """Calcula la profundidad de la jerarquía organizacional"""
        niveles = [emp['nivel'] for emp in empresa['empleados'].values()]
        return max(niveles) - min(niveles) + 1
    
    # Análisis de la estructura
    print("Análisis de Jerarquía Empresarial:")
    print("==================================")
    
    print(f"Subordinados del CTO:")
    subordinados_cto = encontrar_subordinados('cto_carlos', empresa)
    for sub_id in subordinados_cto:
        nombre = empresa['empleados'][sub_id]['nombre']
        posicion = empresa['empleados'][sub_id]['posicion']
        print(f"  - {nombre} ({posicion})")
    
    print(f"\nJefe de Pedro García:")
    jefe_pedro = encontrar_jefe('dev_senior_pedro', empresa)
    if jefe_pedro:
        jefe_info = empresa['empleados'][jefe_pedro]
        print(f"  - {jefe_info['nombre']} ({jefe_info['posicion']})")
    
    print(f"\nProfundidad jerárquica: {calcular_profundidad_jerarquica(empresa)} niveles")
    
    return empresa

empresa_modelo = modelar_jerarquia_empresarial()
```

### Patrón 2: Relaciones Muchos a Muchos

```python
def modelar_red_social_compleja():
    """Modela una red social con múltiples tipos de relaciones"""
    
    red_social = {
        'usuarios': {
            'ana_25': {
                'tipo': 'usuario',
                'nombre': 'Ana García',
                'edad': 25,
                'intereses': ['tecnología', 'viajes', 'fotografía']
            },
            'carlos_30': {
                'tipo': 'usuario', 
                'nombre': 'Carlos López',
                'edad': 30,
                'intereses': ['deportes', 'música', 'tecnología']
            },
            'lucia_28': {
                'tipo': 'usuario',
                'nombre': 'Lucía Martín',
                'edad': 28,
                'intereses': ['arte', 'literatura', 'viajes']
            },
            'pedro_32': {
                'tipo': 'usuario',
                'nombre': 'Pedro Santos',
                'edad': 32,
                'intereses': ['deportes', 'negocios', 'tecnología']
            }
        },
        'grupos': {
            'grupo_tech': {
                'tipo': 'grupo',
                'nombre': 'Entusiastas de la Tecnología',
                'categoria': 'tecnología',
                'miembros_count': 4
            },
            'grupo_viajes': {
                'tipo': 'grupo',
                'nombre': 'Viajeros del Mundo',
                'categoria': 'viajes',
                'miembros_count': 2
            }
        },
        'eventos': {
            'evento_tech_2024': {
                'tipo': 'evento',
                'nombre': 'TechConf 2024',
                'fecha': '2024-03-15',
                'ubicacion': 'Madrid'
            }
        },
        'relaciones': [
            # Amistades (simétricas)
            ('ana_25', 'carlos_30', 'AMIGO_DE', {'desde': '2022-01-15', 'fuerza': 'alta'}),
            ('ana_25', 'lucia_28', 'AMIGO_DE', {'desde': '2023-06-10', 'fuerza': 'media'}),
            ('carlos_30', 'pedro_32', 'AMIGO_DE', {'desde': '2021-09-20', 'fuerza': 'alta'}),
            
            # Pertenencia a grupos
            ('ana_25', 'grupo_tech', 'MIEMBRO_DE', {'rol': 'admin', 'desde': '2023-01-01'}),
            ('carlos_30', 'grupo_tech', 'MIEMBRO_DE', {'rol': 'miembro', 'desde': '2023-02-15'}),
            ('ana_25', 'grupo_viajes', 'MIEMBRO_DE', {'rol': 'miembro', 'desde': '2023-05-01'}),
            ('lucia_28', 'grupo_viajes', 'MIEMBRO_DE', {'rol': 'miembro', 'desde': '2023-05-10'}),
            
            # Asistencia a eventos
            ('ana_25', 'evento_tech_2024', 'ASISTIRA_A', {'confirmado': True}),
            ('carlos_30', 'evento_tech_2024', 'ASISTIRA_A', {'confirmado': False}),
            ('pedro_32', 'evento_tech_2024', 'ASISTIRA_A', {'confirmado': True}),
            
            # Interacciones
            ('ana_25', 'carlos_30', 'MENCIONO', {'fecha': '2024-01-20', 'contexto': 'post_tech'}),
            ('lucia_28', 'ana_25', 'COMENTO_POST', {'fecha': '2024-01-22', 'tipo': 'like'})
        ]
    }
    
    def encontrar_amigos_comunes(usuario1, usuario2, red):
        """Encuentra amigos en común entre dos usuarios"""
        amigos_u1 = set()
        amigos_u2 = set()
        
        for rel in red['relaciones']:
            if rel[2] == 'AMIGO_DE':
                if rel[0] == usuario1:
                    amigos_u1.add(rel[1])
                elif rel[1] == usuario1:
                    amigos_u1.add(rel[0])
                
                if rel[0] == usuario2:
                    amigos_u2.add(rel[1])
                elif rel[1] == usuario2:
                    amigos_u2.add(rel[0])
        
        return amigos_u1.intersection(amigos_u2)
    
    def sugerir_amigos(usuario_id, red):
        """Sugiere nuevos amigos basado en amigos comunes y grupos"""
        amigos_actuales = set()
        grupos_usuario = set()
        
        # Obtener amigos actuales y grupos del usuario
        for rel in red['relaciones']:
            if rel[2] == 'AMIGO_DE':
                if rel[0] == usuario_id:
                    amigos_actuales.add(rel[1])
                elif rel[1] == usuario_id:
                    amigos_actuales.add(rel[0])
            elif rel[2] == 'MIEMBRO_DE' and rel[0] == usuario_id:
                grupos_usuario.add(rel[1])
        
        candidatos = {}
        
        # Buscar miembros de los mismos grupos
        for rel in red['relaciones']:
            if rel[2] == 'MIEMBRO_DE' and rel[1] in grupos_usuario:
                candidato = rel[0]
                if candidato != usuario_id and candidato not in amigos_actuales:
                    if candidato not in candidatos:
                        candidatos[candidato] = {'puntos': 0, 'razones': []}
                    candidatos[candidato]['puntos'] += 2
                    candidatos[candidato]['razones'].append(f"Mismo grupo: {rel[1]}")
        
        # Buscar amigos de amigos
        for amigo in amigos_actuales:
            amigos_del_amigo = set()
            for rel in red['relaciones']:
                if rel[2] == 'AMIGO_DE':
                    if rel[0] == amigo:
                        amigos_del_amigo.add(rel[1])
                    elif rel[1] == amigo:
                        amigos_del_amigo.add(rel[0])
            
            for candidato in amigos_del_amigo:
                if candidato != usuario_id and candidato not in amigos_actuales:
                    if candidato not in candidatos:
                        candidatos[candidato] = {'puntos': 0, 'razones': []}
                    candidatos[candidato]['puntos'] += 1
                    candidatos[candidato]['razones'].append(f"Amigo de {amigo}")
        
        # Ordenar por puntuación
        sugerencias = sorted(candidatos.items(), key=lambda x: x[1]['puntos'], reverse=True)
        return sugerencias[:3]  # Top 3 sugerencias
    
    def analizar_actividad_grupos(red):
        """Analiza la actividad en grupos"""
        actividad_grupos = {}
        
        for grupo_id in red['grupos']:
            actividad_grupos[grupo_id] = {
                'miembros': 0,
                'admins': 0,
                'miembros_activos': 0
            }
        
        for rel in red['relaciones']:
            if rel[2] == 'MIEMBRO_DE':
                grupo_id = rel[1]
                actividad_grupos[grupo_id]['miembros'] += 1
                
                if len(rel) > 3 and rel[3].get('rol') == 'admin':
                    actividad_grupos[grupo_id]['admins'] += 1
        
        return actividad_grupos
    
    # Análisis de la red social
    print("Análisis de Red Social:")
    print("======================")
    
    print("Amigos comunes entre Ana y Carlos:")
    comunes = encontrar_amigos_comunes('ana_25', 'carlos_30', red_social)
    for amigo_id in comunes:
        nombre = red_social['usuarios'][amigo_id]['nombre']
        print(f"  - {nombre}")
    
    print(f"\nSugerencias de amistad para Lucía:")
    sugerencias = sugerir_amigos('lucia_28', red_social)
    for candidato_id, info in sugerencias:
        nombre = red_social['usuarios'][candidato_id]['nombre']
        print(f"  - {nombre} ({info['puntos']} puntos)")
        for razon in info['razones']:
            print(f"    • {razon}")
    
    print(f"\nActividad en grupos:")
    actividad = analizar_actividad_grupos(red_social)
    for grupo_id, stats in actividad.items():
        nombre_grupo = red_social['grupos'][grupo_id]['nombre']
        print(f"  - {nombre_grupo}: {stats['miembros']} miembros, {stats['admins']} admins")
    
    return red_social

red_social_modelo = modelar_red_social_compleja()
```

### Patrón 3: Relaciones Temporales

```python
def modelar_historial_laboral():
    """Modela el historial laboral con relaciones temporales"""
    
    historial = {
        'personas': {
            'ana_dev': {
                'tipo': 'persona',
                'nombre': 'Ana García',
                'profesion': 'Desarrolladora',
                'skills': ['Python', 'JavaScript', 'React']
            },
            'carlos_pm': {
                'tipo': 'persona',
                'nombre': 'Carlos López', 
                'profesion': 'Project Manager',
                'skills': ['Scrum', 'Agile', 'Leadership']
            }
        },
        'empresas': {
            'startup_tech': {
                'tipo': 'empresa',
                'nombre': 'TechStartup SL',
                'sector': 'Tecnología',
                'tamaño': 'pequeña'
            },
            'corporacion_big': {
                'tipo': 'empresa',
                'nombre': 'BigCorp SA',
                'sector': 'Consultoría',
                'tamaño': 'grande'
            },
            'empresa_media': {
                'tipo': 'empresa',
                'nombre': 'MediumTech SL',
                'sector': 'Software',
                'tamaño': 'mediana'
            }
        },
        'proyectos': {
            'proyecto_web': {
                'tipo': 'proyecto',
                'nombre': 'Plataforma E-commerce',
                'estado': 'completado',
                'tecnologias': ['React', 'Node.js', 'MongoDB']
            },
            'proyecto_mobile': {
                'tipo': 'proyecto',
                'nombre': 'App Móvil Bancaria',
                'estado': 'en_desarrollo',
                'tecnologias': ['React Native', 'Firebase']
            }
        },
        'relaciones': [
            # Historial laboral de Ana
            ('ana_dev', 'startup_tech', 'TRABAJO_EN', {
                'desde': '2020-01-15',
                'hasta': '2022-06-30',
                'posicion': 'Junior Developer',
                'salario_inicial': 28000,
                'salario_final': 32000,
                'motivo_salida': 'crecimiento_profesional'
            }),
            ('ana_dev', 'empresa_media', 'TRABAJO_EN', {
                'desde': '2022-07-01',
                'hasta': '2024-01-31',
                'posicion': 'Senior Developer',
                'salario_inicial': 45000,
                'salario_final': 50000,
                'motivo_salida': 'mejor_oportunidad'
            }),
            ('ana_dev', 'corporacion_big', 'TRABAJA_EN', {
                'desde': '2024-02-01',
                'hasta': None,  # Empleo actual
                'posicion': 'Tech Lead',
                'salario_inicial': 65000,
                'modalidad': 'hibrido'
            }),
            
            # Participación en proyectos
            ('ana_dev', 'proyecto_web', 'PARTICIPO_EN', {
                'desde': '2021-03-01',
                'hasta': '2021-12-15',
                'rol': 'Frontend Developer',
                'contribucion': 'alta'
            }),
            ('carlos_pm', 'proyecto_web', 'LIDERO', {
                'desde': '2021-02-15',
                'hasta': '2021-12-31',
                'metodologia': 'Scrum',
                'equipo_tamaño': 5
            }),
            ('ana_dev', 'proyecto_mobile', 'PARTICIPA_EN', {
                'desde': '2024-03-01',
                'hasta': None,  # Proyecto actual
                'rol': 'Tech Lead',
                'responsabilidades': ['arquitectura', 'mentoring']
            })
        ]
    }
    
    def calcular_experiencia_total(persona_id, historial):
        """Calcula la experiencia total en años"""
        from datetime import datetime, timedelta
        
        experiencia_total = timedelta()
        
        for rel in historial['relaciones']:
            if rel[0] == persona_id and 'TRABAJO' in rel[2]:
                props = rel[3]
                fecha_inicio = datetime.strptime(props['desde'], '%Y-%m-%d')
                
                if props.get('hasta'):
                    fecha_fin = datetime.strptime(props['hasta'], '%Y-%m-%d')
                else:
                    fecha_fin = datetime.now()  # Trabajo actual
                
                experiencia_total += fecha_fin - fecha_inicio
        
        años_experiencia = experiencia_total.days / 365.25
        return round(años_experiencia, 1)
    
    def analizar_progresion_salarial(persona_id, historial):
        """Analiza la progresión salarial de una persona"""
        empleos = []
        
        for rel in historial['relaciones']:
            if rel[0] == persona_id and 'TRABAJO' in rel[2]:
                empleo_info = {
                    'empresa': rel[1],
                    'desde': rel[3]['desde'],
                    'hasta': rel[3].get('hasta', 'Actual'),
                    'posicion': rel[3]['posicion'],
                    'salario_inicial': rel[3]['salario_inicial']
                }
                if 'salario_final' in rel[3]:
                    empleo_info['salario_final'] = rel[3]['salario_final']
                empleos.append(empleo_info)
        
        # Ordenar por fecha
        empleos.sort(key=lambda x: x['desde'])
        
        # Calcular crecimiento
        if len(empleos) > 1:
            salario_inicial = empleos[0]['salario_inicial']
            salario_actual = empleos[-1].get('salario_final', empleos[-1]['salario_inicial'])
            crecimiento = ((salario_actual - salario_inicial) / salario_inicial) * 100
        else:
            crecimiento = 0
        
        return empleos, crecimiento
    
    def encontrar_colaboradores_comunes(persona1, persona2, historial):
        """Encuentra proyectos donde colaboraron dos personas"""
        proyectos_p1 = set()
        proyectos_p2 = set()
        
        for rel in historial['relaciones']:
            if 'PROYECTO' in rel[2] or 'PARTICIP' in rel[2] or 'LIDERO' in rel[2]:
                if rel[0] == persona1:
                    proyectos_p1.add(rel[1])
                elif rel[0] == persona2:
                    proyectos_p2.add(rel[1])
        
        proyectos_comunes = proyectos_p1.intersection(proyectos_p2)
        
        colaboraciones = []
        for proyecto_id in proyectos_comunes:
            info_p1 = None
            info_p2 = None
            
            for rel in historial['relaciones']:
                if rel[1] == proyecto_id:
                    if rel[0] == persona1:
                        info_p1 = rel[3]
                    elif rel[0] == persona2:
                        info_p2 = rel[3]
            
            if info_p1 and info_p2:
                colaboraciones.append({
                    'proyecto': proyecto_id,
                    'rol_p1': info_p1.get('rol', 'N/A'),
                    'rol_p2': info_p2.get('rol', 'N/A'),
                    'periodo': f"{info_p1.get('desde', 'N/A')} - {info_p1.get('hasta', 'N/A')}"
                })
        
        return colaboraciones
    
    # Análisis del historial laboral
    print("Análisis de Historial Laboral:")
    print("==============================")
    
    exp_ana = calcular_experiencia_total('ana_dev', historial)
    print(f"Experiencia total de Ana: {exp_ana} años")
    
    empleos_ana, crecimiento_ana = analizar_progresion_salarial('ana_dev', historial)
    print(f"\nProgresión salarial de Ana:")
    for empleo in empleos_ana:
        salario_info = f"€{empleo['salario_inicial']:,}"
        if 'salario_final' in empleo:
            salario_info += f" → €{empleo['salario_final']:,}"
        print(f"  • {empleo['posicion']} en {empleo['empresa']}: {salario_info}")
    print(f"Crecimiento salarial total: {crecimiento_ana:.1f}%")
    
    colaboraciones = encontrar_colaboradores_comunes('ana_dev', 'carlos_pm', historial)
    print(f"\nColaboraciones entre Ana y Carlos:")
    for colab in colaboraciones:
        proyecto_nombre = historial['proyectos'][colab['proyecto']]['nombre']
        print(f"  • {proyecto_nombre}: Ana como {colab['rol_p1']}, Carlos como {colab['rol_p2']}")
    
    return historial

historial_modelo = modelar_historial_laboral()
```

---

## 4.3 Optimización para Consultas Específicas

### Modelado Orientado a Consultas

```python
def optimizar_para_consultas():
    """Demuestra cómo optimizar el modelo según las consultas más frecuentes"""
    
    # CASO: Sistema de e-commerce
    # Consultas más frecuentes:
    # 1. "Productos que compró el usuario X"
    # 2. "Usuarios que compraron el producto Y" 
    # 3. "Productos relacionados/recomendados"
    # 4. "Historial de pedidos del usuario"
    
    # ❌ MODELO SUBÓPTIMO: Todo como propiedades
    modelo_suboptimo = {
        'nodos': {
            'pedido_001': {
                'tipo': 'pedido',
                'usuario': 'ana_garcia',
                'productos': ['laptop', 'mouse', 'teclado'],
                'fecha': '2024-01-15',
                'total': 1250.00
            }
        },
        'relaciones': []  # Sin relaciones útiles para consultas
    }
    
    # ✅ MODELO OPTIMIZADO: Entidades separadas con relaciones explícitas
    modelo_optimizado = {
        'nodos': {
            # Usuarios
            'ana_garcia': {
                'tipo': 'usuario',
                'nombre': 'Ana García',
                'email': 'ana@email.com',
                'fecha_registro': '2023-01-15'
            },
            'carlos_lopez': {
                'tipo': 'usuario',
                'nombre': 'Carlos López', 
                'email': 'carlos@email.com',
                'fecha_registro': '2023-02-20'
            },
            
            # Productos
            'laptop_gaming': {
                'tipo': 'producto',
                'nombre': 'Laptop Gaming Pro',
                'precio': 1200.00,
                'categoria': 'electronica',
                'marca': 'TechBrand'
            },
            'mouse_wireless': {
                'tipo': 'producto',
                'nombre': 'Mouse Inalámbrico',
                'precio': 25.00,
                'categoria': 'accesorios',
                'marca': 'TechBrand'
            },
            'teclado_mecanico': {
                'tipo': 'producto',
                'nombre': 'Teclado Mecánico RGB',
                'precio': 85.00,
                'categoria': 'accesorios',
                'marca': 'GamerTech'
            },
            
            # Pedidos
            'pedido_001': {
                'tipo': 'pedido',
                'fecha': '2024-01-15',
                'estado': 'entregado',
                'total': 1310.00
            },
            'pedido_002': {
                'tipo': 'pedido',
                'fecha': '2024-01-20',
                'estado': 'enviado',
                'total': 110.00
            },
            
            # Categorías (para recomendaciones)
            'categoria_electronica': {
                'tipo': 'categoria',
                'nombre': 'Electrónicos',
                'descripcion': 'Dispositivos electrónicos'
            },
            'categoria_accesorios': {
                'tipo': 'categoria', 
                'nombre': 'Accesorios',
                'descripcion': 'Accesorios para computadora'
            }
        },
        'relaciones': [
            # Relación usuario-pedido (para historial)
            ('ana_garcia', 'pedido_001', 'REALIZO_PEDIDO'),
            ('carlos_lopez', 'pedido_002', 'REALIZO_PEDIDO'),
            
            # Relación pedido-producto (para detalles)
            ('pedido_001', 'laptop_gaming', 'INCLUYE', {'cantidad': 1, 'precio_unitario': 1200.00}),
            ('pedido_001', 'mouse_wireless', 'INCLUYE', {'cantidad': 2, 'precio_unitario': 25.00}),
            ('pedido_001', 'teclado_mecanico', 'INCLUYE', {'cantidad': 1, 'precio_unitario': 85.00}),
            ('pedido_002', 'mouse_wireless', 'INCLUYE', {'cantidad': 1, 'precio_unitario': 25.00}),
            ('pedido_002', 'teclado_mecanico', 'INCLUYE', {'cantidad': 1, 'precio_unitario': 85.00}),
            
            # Relación producto-categoría (para recomendaciones)
            ('laptop_gaming', 'categoria_electronica', 'PERTENECE_A'),
            ('mouse_wireless', 'categoria_accesorios', 'PERTENECE_A'),
            ('teclado_mecanico', 'categoria_accesorios', 'PERTENECE_A'),
            
            # Relaciones de compatibilidad (para recomendaciones)
            ('laptop_gaming', 'mouse_wireless', 'COMPATIBLE_CON'),
            ('laptop_gaming', 'teclado_mecanico', 'COMPATIBLE_CON'),
            ('mouse_wireless', 'teclado_mecanico', 'COMBINA_CON')
        ]
    }
    
    def consultas_optimizadas(modelo):
        """Implementa consultas eficientes sobre el modelo optimizado"""
        
        def productos_comprados_por_usuario(usuario_id):
            """CONSULTA 1: Productos que compró el usuario X"""
            productos = []
            
            # Paso 1: Encontrar pedidos del usuario
            pedidos_usuario = []
            for rel in modelo['relaciones']:
                if rel[0] == usuario_id and rel[2] == 'REALIZO_PEDIDO':
                    pedidos_usuario.append(rel[1])
            
            # Paso 2: Encontrar productos en esos pedidos
            for pedido_id in pedidos_usuario:
                for rel in modelo['relaciones']:
                    if rel[0] == pedido_id and rel[2] == 'INCLUYE':
                        producto_info = modelo['nodos'][rel[1]].copy()
                        producto_info['id'] = rel[1]
                        if len(rel) > 3:
                            producto_info.update(rel[3])  # Cantidad, precio
                        productos.append(producto_info)
            
            return productos
        
        def usuarios_que_compraron_producto(producto_id):
            """CONSULTA 2: Usuarios que compraron el producto Y"""
            usuarios = set()
            
            # Encontrar pedidos que incluyen el producto
            pedidos_con_producto = []
            for rel in modelo['relaciones']:
                if rel[1] == producto_id and rel[2] == 'INCLUYE':
                    pedidos_con_producto.append(rel[0])
            
            # Encontrar usuarios de esos pedidos
            for pedido_id in pedidos_con_producto:
                for rel in modelo['relaciones']:
                    if rel[1] == pedido_id and rel[2] == 'REALIZO_PEDIDO':
                        usuarios.add(rel[0])
            
            return list(usuarios)
        
        def productos_relacionados(producto_id):
            """CONSULTA 3: Productos relacionados/recomendados"""
            relacionados = []
            
            # Método 1: Productos compatibles directos
            for rel in modelo['relaciones']:
                if rel[0] == producto_id and rel[2] in ['COMPATIBLE_CON', 'COMBINA_CON']:
                    relacionados.append(('directo', rel[1]))
                elif rel[1] == producto_id and rel[2] in ['COMPATIBLE_CON', 'COMBINA_CON']:
                    relacionados.append(('directo', rel[0]))
            
            # Método 2: Productos de la misma categoría
            categoria_producto = None
            for rel in modelo['relaciones']:
                if rel[0] == producto_id and rel[2] == 'PERTENECE_A':
                    categoria_producto = rel[1]
                    break
            
            if categoria_producto:
                for rel in modelo['relaciones']:
                    if rel[1] == categoria_producto and rel[2] == 'PERTENECE_A':
                        if rel[0] != producto_id:
                            relacionados.append(('categoria', rel[0]))
            
            # Método 3: Productos frecuentemente comprados juntos
            usuarios_compradores = usuarios_que_compraron_producto(producto_id)
            productos_frecuentes = {}
            
            for usuario in usuarios_compradores:
                productos_usuario = productos_comprados_por_usuario(usuario)
                for prod in productos_usuario:
                    if prod['id'] != producto_id:
                        productos_frecuentes[prod['id']] = productos_frecuentes.get(prod['id'], 0) + 1
            
            # Ordenar por frecuencia
            for prod_id, frecuencia in sorted(productos_frecuentes.items(), 
                                            key=lambda x: x[1], reverse=True)[:3]:
                relacionados.append(('frecuente', prod_id))
            
            return relacionados
        
        def historial_usuario(usuario_id):
            """CONSULTA 4: Historial completo del usuario"""
            historial = {
                'pedidos': [],
                'productos_unicos': set(),
                'gasto_total': 0,
                'categorias_preferidas': {}
            }
            
            # Obtener todos los pedidos
            for rel in modelo['relaciones']:
                if rel[0] == usuario_id and rel[2] == 'REALIZO_PEDIDO':
                    pedido_info = modelo['nodos'][rel[1]].copy()
                    pedido_info['id'] = rel[1]
                    
                    # Obtener productos del pedido
                    productos_pedido = []
                    for rel2 in modelo['relaciones']:
                        if rel2[0] == rel[1] and rel2[2] == 'INCLUYE':
                            producto_info = modelo['nodos'][rel2[1]].copy()
                            producto_info['id'] = rel2[1]
                            if len(rel2) > 3:
                                producto_info.update(rel2[3])
                            productos_pedido.append(producto_info)
                            
                            historial['productos_unicos'].add(rel2[1])
                            
                            # Contar categorías preferidas
                            categoria = producto_info.get('categoria', 'sin_categoria')
                            historial['categorias_preferidas'][categoria] = \
                                historial['categorias_preferidas'].get(categoria, 0) + 1
                    
                    pedido_info['productos'] = productos_pedido
                    historial['pedidos'].append(pedido_info)
                    historial['gasto_total'] += pedido_info.get('total', 0)
            
            # Ordenar pedidos por fecha
            historial['pedidos'].sort(key=lambda x: x['fecha'], reverse=True)
            historial['productos_unicos'] = len(historial['productos_unicos'])
            
            return historial
        
        return {
            'productos_comprados_por_usuario': productos_comprados_por_usuario,
            'usuarios_que_compraron_producto': usuarios_que_compraron_producto,
            'productos_relacionados': productos_relacionados,
            'historial_usuario': historial_usuario
        }
    
    # Demostrar eficiencia de consultas
    consultas = consultas_optimizadas(modelo_optimizado)
    
    print("Consultas Optimizadas - E-commerce:")
    print("==================================")
    
    print("1. Productos comprados por Ana:")
    productos_ana = consultas['productos_comprados_por_usuario']('ana_garcia')
    for producto in productos_ana:
        print(f"   • {producto['nombre']} - €{producto['precio']} (Cantidad: {producto.get('cantidad', 1)})")
    
    print("\n2. Usuarios que compraron Mouse Inalámbrico:")
    usuarios_mouse = consultas['usuarios_que_compraron_producto']('mouse_wireless')
    for usuario_id in usuarios_mouse:
        nombre = modelo_optimizado['nodos'][usuario_id]['nombre']
        print(f"   • {nombre}")
    
    print("\n3. Productos relacionados con Laptop Gaming:")
    relacionados = consultas['productos_relacionados']('laptop_gaming')
    for tipo, producto_id in relacionados:
        nombre = modelo_optimizado['nodos'][producto_id]['nombre']
        print(f"   • {nombre} (relación: {tipo})")
    
    print("\n4. Historial completo de Ana:")
    historial = consultas['historial_usuario']('ana_garcia')
    print(f"   • Total de pedidos: {len(historial['pedidos'])}")
    print(f"   • Productos únicos: {historial['productos_unicos']}")
    print(f"   • Gasto total: €{historial['gasto_total']}")
    print(f"   • Categorías preferidas: {dict(historial['categorias_preferidas'])}")
    
    return modelo_optimizado

modelo_ecommerce = optimizar_para_consultas()
```

---

## 4.4 Ejercicios Prácticos de Modelado

### Ejercicio 1: Sistema de Gestión Hospitalaria

```python
def ejercicio_hospital():
    """Diseña un modelo de grafos para un sistema hospitalario"""
    
    # REQUISITOS:
    # - Pacientes con historial médico
    # - Médicos con especialidades
    # - Citas médicas programadas
    # - Tratamientos y medicamentos
    # - Departamentos del hospital
    # - Historial de hospitalizaciones
    
    hospital_modelo = {
        'nodos': {
            # TODO: Define los nodos necesarios
            # Considera: pacientes, médicos, departamentos, medicamentos, etc.
        },
        'relaciones': [
            # TODO: Define las relaciones
            # Considera: citas, tratamientos, prescripciones, etc.
        ]
    }
    
    def consultas_hospital():
        """Implementa consultas típicas del sistema hospitalario"""
        
        def historial_paciente(paciente_id):
            """Historial médico completo de un paciente"""
            pass
        
        def agenda_medico(medico_id, fecha):
            """Citas programadas para un médico en una fecha"""
            pass
        
        def pacientes_por_especialidad(especialidad):
            """Pacientes atendidos por una especialidad"""
            pass
        
        def medicamentos_prescritos(paciente_id):
            """Medicamentos actuales de un paciente"""
            pass
        
        def ocupacion_departamento(departamento_id):
            """Nivel de ocupación de un departamento"""
            pass
    
    # TODO: Implementa el modelo y las consultas
    return hospital_modelo

# Pistas para la implementación:
# - ¿Qué entidades tienen identidad propia?
# - ¿Cómo modelar citas (como nodos o relaciones)?
# - ¿Cómo manejar el historial temporal?
# - ¿Qué relaciones son más importantes para las consultas?
```

### Ejercicio 2: Plataforma de Cursos Online

```python
def ejercicio_plataforma_educativa():
    """Diseña un modelo para una plataforma de educación online"""
    
    # REQUISITOS:
    # - Estudiantes inscritos en cursos
    # - Instructores que crean cursos
    # - Cursos organizados en módulos y lecciones
    # - Progreso de estudiantes por lección
    # - Evaluaciones y calificaciones
    # - Certificaciones obtenidas
    # - Reseñas de cursos
    # - Rutas de aprendizaje (pre-requisitos)
    
    plataforma_modelo = {
        'nodos': {
            # TODO: Define nodos para todas las entidades
        },
        'relaciones': [
            # TODO: Define relaciones complejas
        ]
    }
    
    def consultas_educativas():
        """Consultas típicas de la plataforma"""
        
        def progreso_estudiante(estudiante_id, curso_id):
            """Progreso detallado en un curso específico"""
            pass
        
        def cursos_recomendados(estudiante_id):
            """Recomienda cursos basado en historial"""
            pass
        
        def estadisticas_instructor(instructor_id):
            """Estadísticas de todos los cursos de un instructor"""
            pass
        
        def estudiantes_en_riesgo(curso_id):
            """Estudiantes con bajo progreso"""
            pass
        
        def ruta_aprendizaje(objetivo_curso_id):
            """Secuencia óptima de cursos para llegar al objetivo"""
            pass
    
    # TODO: Implementa considerando:
    # - ¿Cómo modelar progreso incremental?
    # - ¿Rutas de aprendizaje como relaciones o nodos?
    # - ¿Cómo optimizar para recomendaciones?
    
    return plataforma_modelo
```

### Ejercicio 3: Red de Suministro Global

```python
def ejercicio_cadena_suministro():
    """Modela una cadena de suministro global compleja"""
    
    # REQUISITOS:
    # - Proveedores en diferentes países
    # - Fábricas con capacidades de producción
    # - Centros de distribución
    # - Productos con componentes
    # - Rutas de transporte con costos
    # - Inventarios en tiempo real
    # - Demanda por región
    # - Riesgos geopolíticos
    
    cadena_suministro = {
        'nodos': {
            # TODO: Considera la complejidad geográfica
        },
        'relaciones': [
            # TODO: Modela flujos de materiales y productos
        ]
    }
    
    def analisis_suministro():
        """Análisis crítico de la cadena de suministro"""
        
        def puntos_criticos():
            """Identifica cuellos de botella en la cadena"""
            pass
        
        def rutas_alternativas(origen, destino):
            """Encuentra rutas alternativas ante disrupciones"""
            pass
        
        def impacto_disrupcion(nodo_afectado):
            """Simula impacto de interrupción en un nodo"""
            pass
        
        def optimizar_inventarios():
            """Sugiere niveles óptimos de inventario"""
            pass
        
        def riesgo_concentracion():
            """Analiza riesgos de concentración geográfica"""
            pass
    
    # TODO: Considera:
    # - ¿Cómo modelar capacidades y limitaciones?
    # - ¿Inventarios como propiedades o nodos?
    # - ¿Cómo representar riesgos y alternativas?
    
    return cadena_suministro
```

---

## 4.5 Validación y Mejores Prácticas

### Checklist de Validación del Modelo

```python
def validar_modelo_completo(modelo):
    """Validación exhaustiva de un modelo de grafos"""
    
    problemas = []
    advertencias = []
    
    # 1. Validación de Nodos
    def validar_nodos():
        nodos_sin_tipo = []
        nodos_sin_propiedades = []
        
        for nodo_id, propiedades in modelo['nodos'].items():
            if 'tipo' not in propiedades:
                nodos_sin_tipo.append(nodo_id)
            
            if len(propiedades) <= 1:  # Solo tipo
                nodos_sin_propiedades.append(nodo_id)
        
        if nodos_sin_tipo:
            problemas.append(f"Nodos sin tipo: {nodos_sin_tipo}")
        
        if nodos_sin_propiedades:
            advertencias.append(f"Nodos con pocas propiedades: {nodos_sin_propiedades}")
    
    # 2. Validación de Relaciones
    def validar_relaciones():
        relaciones_invalidas = []
        nodos_aislados = set(modelo['nodos'].keys())
        tipos_relacion = set()
        
        for rel in modelo['relaciones']:
            # Verificar formato mínimo
            if len(rel) < 3:
                relaciones_invalidas.append(rel)
                continue
            
            origen, destino, tipo_rel = rel[0], rel[1], rel[2]
            tipos_relacion.add(tipo_rel)
            
            # Verificar que los nodos existen
            if origen not in modelo['nodos']:
                problemas.append(f"Nodo origen inexistente: {origen} en {rel}")
            else:
                nodos_aislados.discard(origen)
            
            if destino not in modelo['nodos']:
                problemas.append(f"Nodo destino inexistente: {destino} en {rel}")
            else:
                nodos_aislados.discard(destino)
        
        if relaciones_invalidas:
            problemas.append(f"Relaciones con formato inválido: {relaciones_invalidas}")
        
        if nodos_aislados:
            advertencias.append(f"Nodos sin relaciones: {list(nodos_aislados)}")
        
        return tipos_relacion
    
    # 3. Validación de Consistencia
    def validar_consistencia():
        # Verificar que las relaciones tienen sentido semántico
        tipos_nodos = {}
        for nodo_id, props in modelo['nodos'].items():
            tipo = props.get('tipo', 'sin_tipo')
            if tipo not in tipos_nodos:
                tipos_nodos[tipo] = []
            tipos_nodos[tipo].append(nodo_id)
        
        relaciones_inconsistentes = []
        for rel in modelo['relaciones']:
            if len(rel) >= 3:
                origen, destino, tipo_rel = rel[0], rel[1], rel[2]
                tipo_origen = modelo['nodos'][origen].get('tipo', 'sin_tipo')
                tipo_destino = modelo['nodos'][destino].get('tipo', 'sin_tipo')
                
                # Detectar relaciones potencialmente problemáticas
                if tipo_origen == tipo_destino and tipo_rel in ['ES_UN', 'TIPO_DE']:
                    relaciones_inconsistentes.append(f"{rel} - relación jerárquica entre mismo tipo")
        
        if relaciones_inconsistentes:
            advertencias.extend(relaciones_inconsistentes)
    
    # 4. Análisis de Densidad y Conectividad
    def analizar_conectividad():
        total_nodos = len(modelo['nodos'])
        total_relaciones = len(modelo['relaciones'])
        
        if total_nodos > 0:
            max_relaciones = total_nodos * (total_nodos - 1) / 2
            densidad = total_relaciones / max_relaciones if max_relaciones > 0 else 0
            
            if densidad > 0.8:
                advertencias.append(f"Modelo muy denso ({densidad:.2f}) - considerar simplificar")
            elif densidad < 0.1 and total_nodos > 5:
                advertencias.append(f"Modelo muy disperso ({densidad:.2f}) - verificar conexiones")
    
    # Ejecutar validaciones
    validar_nodos()
    tipos_rel = validar_relaciones()
    validar_consistencia()
    analizar_conectividad()
    
    # Generar reporte
    reporte = {
        'problemas_criticos': problemas,
        'advertencias': advertencias,
        'estadisticas': {
            'total_nodos': len(modelo['nodos']),
            'total_relaciones': len(modelo['relaciones']),
            'tipos_nodos': len(set(props.get('tipo', 'sin_tipo') 
                                 for props in modelo['nodos'].values())),
            'tipos_relaciones': len(tipos_rel)
        }
    }
    
    return reporte

def mejores_practicas():
    """Guía de mejores prácticas para modelado de grafos"""
    
    practicas = {
        'nomenclatura': [
            "Usar nombres descriptivos para nodos (ana_garcia, no user_1)",
            "Tipos de relación en MAYÚSCULAS (TRABAJA_EN, AMIGO_DE)",
            "Consistencia en nombres (siempre en español o inglés)",
            "Evitar espacios en IDs (usar _ o camelCase)"
        ],
        
        'estructura': [
            "Entidades con identidad propia → Nodos",
            "Interacciones y asociaciones → Relaciones", 
            "Atributos descriptivos → Propiedades",
            "Evitar nodos que son realmente propiedades"
        ],
        
        'performance': [
            "Modelar según consultas más frecuentes",
            "Crear índices implícitos con relaciones directas",
            "Evitar relaciones muy profundas (>5 saltos)",
            "Balancear entre normalización y desnormalización"
        ],
        
        'mantenibilidad': [
            "Documentar el esquema y sus decisiones",
            "Usar tipos consistentes para validación",
            "Planificar evolución del esquema",
            "Mantener ejemplos de consultas típicas"
        ]
    }
    
    return practicas

# Ejemplo de uso con validación
ejemplo_validacion = {
    'nodos': {
        'user_1': {'nombre': 'Ana'},  # ❌ Sin tipo
        'producto_laptop': {'tipo': 'producto', 'precio': 1200},  # ✅ Bien
        'nodo_aislado': {'tipo': 'test'}  # ⚠️ Sin relaciones
    },
    'relaciones': [
        ('user_1', 'producto_laptop', 'COMPRO'),  # ✅ Bien
        ('inexistente', 'producto_laptop')  # ❌ Formato incorrecto
    ]
}

reporte = validar_modelo_completo(ejemplo_validacion)
print("Reporte de Validación:")
print("=====================")
if reporte['problemas_criticos']:
    print("❌ PROBLEMAS CRÍTICOS:")
    for problema in reporte['problemas_criticos']:
        print(f"   • {problema}")

if reporte['advertencias']:
    print("\n⚠️  ADVERTENCIAS:")
    for advertencia in reporte['advertencias']:
        print(f"   • {advertencia}")

print(f"\n📊 ESTADÍSTICAS:")
for clave, valor in reporte['estadisticas'].items():
    print(f"   • {clave}: {valor}")
```

---

## 4.6 Resumen y Preparación

### Conceptos Clave del Modelado

- [ ] **Identificación de entidades**
  - Nodos para elementos con identidad propia
  - Propiedades para atributos descriptivos

- [ ] **Diseño de relaciones**
  - Relaciones para interacciones significativas
  - Propiedades en relaciones para metadatos

- [ ] **Patrones comunes**
  - Jerárquicos (árboles organizacionales)
  - Muchos a muchos (redes sociales)
  - Temporales (historiales)

- [ ] **Optimización**
  - Modelar según consultas frecuentes
  - Balance entre normalización y performance

---

## 4.7 Preparación para el Siguiente Tema

En el próximo tema exploraremos **algoritmos básicos de grafos**, incluyendo:
- Algoritmos de recorrido avanzados
- Camino más corto con pesos
- Detección de comunidades
- Métricas de centralidad avanzadas
