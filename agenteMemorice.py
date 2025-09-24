import time
import heapq
from copy import deepcopy

# ===== ALGORITMO ORIGINAL (VORAZ) =====
class AgenteMemorice:
    """Algoritmo voraz original - toma decisiones inmediatas sin retroceder"""
    def __init__(self, tablero):
        self.tablero = tablero
        self.memoria = {}  # Para recordar cartas vistas {posicion: valor}
        self.emparejadas = set()  # Posiciones ya emparejadas
        self.movimientos = 0  # Contador de movimientos
    
    def buscar_pareja_conocida(self):
        # Crear un diccionario para agrupar posiciones por valor
        valores_posiciones = {}
        
        # Agrupar posiciones no emparejadas por su valor
        for pos, valor in self.memoria.items():
            if pos not in self.emparejadas:  # Solo considerar cartas no emparejadas
                if valor not in valores_posiciones:
                    valores_posiciones[valor] = []
                valores_posiciones[valor].append(pos)
        
        # Buscar valores que tengan al menos 2 posiciones
        for valor, posiciones in valores_posiciones.items():
            if len(posiciones) >= 2:  # Encontré una pareja
                return (posiciones[0], posiciones[1])
        
        return None  # No encontré ninguna pareja

    def resolver(self):
        print("=== ALGORITMO VORAZ (ORIGINAL) ===")
        inicio_tiempo = time.time()  # Iniciar cronómetro
        
        while len(self.emparejadas) < 36:
            # 1. Buscar si ya conocemos alguna pareja
            pareja = self.buscar_pareja_conocida()
            
            if pareja:
                # Si encontramos pareja conocida, emparejarla
                pos1, pos2 = pareja
                print(f"Emparejando posiciones {pos1} y {pos2} (valor: {self.tablero[pos1]})")
                self.emparejadas.add(pos1)
                self.emparejadas.add(pos2)
                self.movimientos += 1
            else:
                # Estrategia: explorar 2 cartas por turno
                cartas_exploradas = 0
                for pos in range(36):
                    if pos not in self.memoria and pos not in self.emparejadas and cartas_exploradas < 2:
                        self.memoria[pos] = self.tablero[pos]
                        print(f"Explorando posición {pos}, encontré valor {self.tablero[pos]}")
                        cartas_exploradas += 1
                self.movimientos += 1
        
        tiempo_total = time.time() - inicio_tiempo
        self.mostrar_estadisticas(tiempo_total, "Algoritmo Voraz")

    def mostrar_estadisticas(self, tiempo, metodo):
        print(f"\n=== JUEGO COMPLETADO CON {metodo} ===")
        print(f"Movimientos totales: {self.movimientos}")
        print(f"Tiempo de resolución: {tiempo:.4f} segundos")
        print(f"Cartas en memoria: {len(self.memoria)}")


# ===== ALGORITMO A* (BÚSQUEDA INFORMADA) =====
class EstadoJuego:
    """Representa un estado del juego de memoria para A*"""
    def __init__(self, memoria=None, emparejadas=None, movimientos=0):
        self.memoria = memoria if memoria else {}
        self.emparejadas = emparejadas if emparejadas else set()
        self.movimientos = movimientos
        self.g = movimientos  # Costo real desde el inicio
        self.h = 0  # Heurística (se calculará)
        self.f = 0  # Función de evaluación f = g + h
    
    def es_estado_final(self):
        """Verifica si el juego está completado"""
        return len(self.emparejadas) >= 36
    
    def copia(self):
        """Crea una copia profunda del estado"""
        nuevo_estado = EstadoJuego(
            memoria=deepcopy(self.memoria),
            emparejadas=deepcopy(self.emparejadas),
            movimientos=self.movimientos
        )
        return nuevo_estado
    
    def __lt__(self, other):
        """Comparador para la cola de prioridad"""
        return self.f < other.f
    
    def __eq__(self, other):
        """Igualdad basada en el estado del juego"""
        return (self.memoria == other.memoria and 
                self.emparejadas == other.emparejadas)
    
    def __hash__(self):
        """Hash para usar en conjuntos"""
        return hash((frozenset(self.memoria.items()), frozenset(self.emparejadas)))

class AgentememoriceAstar:
    """Algoritmo A* - búsqueda informada con heurística"""
    def __init__(self, tablero):
        self.tablero = tablero
        self.solucion_encontrada = None
        self.nodos_explorados = 0
        self.nodos_expandidos = 0
        
    def calcular_heuristica(self, estado):
        """
        Heurística para A*: estima el número mínimo de movimientos restantes
        
        h(n) = (parejas_restantes / 2) + penalizacion_por_cartas_desconocidas
        """
        parejas_restantes = (36 - len(estado.emparejadas)) // 2
        
        # Contar parejas que ya conocemos en memoria
        valores_conocidos = {}
        for pos, valor in estado.memoria.items():
            if pos not in estado.emparejadas:
                valores_conocidos[valor] = valores_conocidos.get(valor, 0) + 1
        
        parejas_conocidas = sum(1 for count in valores_conocidos.values() if count >= 2)
        
        # Heurística: movimientos para emparejar conocidas + estimación para desconocidas
        cartas_sin_descubrir = 36 - len(estado.memoria)
        estimacion_descubrimiento = cartas_sin_descubrir // 2  # Optimista: 2 cartas por movimiento
        
        # Parejas restantes que no conocemos
        parejas_desconocidas = parejas_restantes - parejas_conocidas
        
        return parejas_conocidas + max(0, parejas_desconocidas) + estimacion_descubrimiento
    
    def buscar_pareja_conocida(self, estado):
        """Busca si existe una pareja conocida en la memoria del estado"""
        valores_posiciones = {}
        
        for pos, valor in estado.memoria.items():
            if pos not in estado.emparejadas:
                if valor not in valores_posiciones:
                    valores_posiciones[valor] = []
                valores_posiciones[valor].append(pos)
        
        for valor, posiciones in valores_posiciones.items():
            if len(posiciones) >= 2:
                return (posiciones[0], posiciones[1])
        
        return None
    
    def generar_sucesores(self, estado):
        """Genera todos los posibles estados sucesores"""
        sucesores = []
        
        # Prioridad 1: Si hay parejas conocidas, emparejarlas
        pareja = self.buscar_pareja_conocida(estado)
        if pareja:
            nuevo_estado = estado.copia()
            pos1, pos2 = pareja
            nuevo_estado.emparejadas.add(pos1)
            nuevo_estado.emparejadas.add(pos2)
            nuevo_estado.movimientos += 1
            nuevo_estado.g = nuevo_estado.movimientos
            sucesores.append((nuevo_estado, f"Emparejar {pos1}-{pos2} (valor: {self.tablero[pos1]})"))
            return sucesores
        
        # Prioridad 2: Explorar nuevas cartas
        posiciones_disponibles = [pos for pos in range(36) 
                                if pos not in estado.memoria and pos not in estado.emparejadas]
        
        # Estrategia: explorar 2 cartas por movimiento (como el algoritmo original)
        for i, pos1 in enumerate(posiciones_disponibles[:5]):  # Limitar para eficiencia
            for pos2 in posiciones_disponibles[i+1:6]:
                nuevo_estado = estado.copia()
                nuevo_estado.memoria[pos1] = self.tablero[pos1]
                nuevo_estado.memoria[pos2] = self.tablero[pos2]
                nuevo_estado.movimientos += 1
                nuevo_estado.g = nuevo_estado.movimientos
                
                # Bonificación heurística si descubrimos una pareja inmediatamente
                if self.tablero[pos1] == self.tablero[pos2]:
                    nuevo_estado.emparejadas.add(pos1)
                    nuevo_estado.emparejadas.add(pos2)
                    accion = f"Descubrir y emparejar {pos1}-{pos2} (valor: {self.tablero[pos1]})"
                else:
                    accion = f"Explorar posiciones {pos1},{pos2}"
                
                sucesores.append((nuevo_estado, accion))
        
        # También permitir explorar solo 1 carta si es necesario
        if len(sucesores) == 0:
            for pos in posiciones_disponibles[:3]:
                nuevo_estado = estado.copia()
                nuevo_estado.memoria[pos] = self.tablero[pos]
                nuevo_estado.movimientos += 1
                nuevo_estado.g = nuevo_estado.movimientos
                sucesores.append((nuevo_estado, f"Explorar posición {pos}"))
        
        return sucesores
    
    def resolver_con_astar(self):
        """Implementa el algoritmo A* para resolver el juego"""
        print("=== ALGORITMO A* (BÚSQUEDA INFORMADA) ===")
        inicio_tiempo = time.time()
        
        # Inicialización
        estado_inicial = EstadoJuego()
        estado_inicial.h = self.calcular_heuristica(estado_inicial)
        estado_inicial.f = estado_inicial.g + estado_inicial.h
        
        # Cola de prioridad (heap) para A*
        frontera = [(estado_inicial.f, 0, estado_inicial, [])]  # (f, counter, estado, camino)
        counter = 1  # Para desempatar en el heap
        
        # Conjunto de estados explorados
        explorados = set()
        mejor_estado = None  # Para trackear el mejor estado encontrado
        
        while frontera:
            f_actual, _, estado_actual, camino = heapq.heappop(frontera)
            
            self.nodos_explorados += 1
            
            # Verificar si ya exploramos este estado
            if estado_actual in explorados:
                continue
                
            explorados.add(estado_actual)
            
            # Actualizar el mejor estado (para mostrar progreso)
            if mejor_estado is None or len(estado_actual.emparejadas) > len(mejor_estado.emparejadas):
                mejor_estado = estado_actual
            
            # Verificar si alcanzamos el estado final
            if estado_actual.es_estado_final():
                tiempo_total = time.time() - inicio_tiempo
                self.solucion_encontrada = {
                    'estado': estado_actual,
                    'camino': camino,
                    'nodos_explorados': self.nodos_explorados,
                    'nodos_expandidos': self.nodos_expandidos
                }
                self.mostrar_resultado(tiempo_total, "Algoritmo A*")
                return self.solucion_encontrada
            
            # Expandir sucesores
            self.nodos_expandidos += 1
            sucesores = self.generar_sucesores(estado_actual)
            
            # Ejecutar la mejor acción encontrada (similar al voraz)
            if sucesores:
                mejor_sucesor, mejor_accion = sucesores[0]  # A* ya ordena por calidad
                
                # Mostrar la acción elegida (similar al estilo voraz)
                if "Emparejar" in mejor_accion:
                    # Extraer posiciones del string de acción
                    partes = mejor_accion.split()
                    posiciones = partes[1].split('-')
                    pos1, pos2 = int(posiciones[0]), int(posiciones[1])
                    print(f"Emparejando posiciones {pos1} y {pos2} (valor: {self.tablero[pos1]})")
                elif "Descubrir y emparejar" in mejor_accion:
                    partes = mejor_accion.split()
                    posiciones = partes[3].split('-')
                    pos1, pos2 = int(posiciones[0]), int(posiciones[1])
                    print(f"¡Descubrí pareja inmediata! Posiciones {pos1} y {pos2} (valor: {self.tablero[pos1]})")
                elif "Explorar posiciones" in mejor_accion:
                    # Extraer posiciones del string
                    partes = mejor_accion.split()
                    posiciones = partes[2].split(',')
                    pos1, pos2 = int(posiciones[0]), int(posiciones[1])
                    print(f"Explorando posición {pos1}, encontré valor {self.tablero[pos1]}")
                    print(f"Explorando posición {pos2}, encontré valor {self.tablero[pos2]}")
                elif "Explorar posición" in mejor_accion:
                    partes = mejor_accion.split()
                    pos = int(partes[2])
                    print(f"Explorando posición {pos}, encontré valor {self.tablero[pos]}")
            
            # Añadir todos los sucesores a la frontera
            for estado_sucesor, accion in sucesores:
                if estado_sucesor not in explorados:
                    # Calcular heurística y función de evaluación
                    estado_sucesor.h = self.calcular_heuristica(estado_sucesor)
                    estado_sucesor.f = estado_sucesor.g + estado_sucesor.h
                    
                    nuevo_camino = camino + [accion]
                    heapq.heappush(frontera, (estado_sucesor.f, counter, estado_sucesor, nuevo_camino))
                    counter += 1
        
        # No se encontró solución
        tiempo_total = time.time() - inicio_tiempo
        print(f"\nNo se encontró solución")
        print(f"Nodos explorados: {self.nodos_explorados}")
        print(f"Tiempo transcurrido: {tiempo_total:.4f} segundos")
        return None
    
    def mostrar_resultado(self, tiempo, metodo):
        """Muestra las estadísticas del resultado"""
        if self.solucion_encontrada:
            print(f"\n=== SOLUCIÓN ENCONTRADA CON {metodo} ===")
            print(f"Movimientos totales: {self.solucion_encontrada['estado'].movimientos}")
            print(f"Tiempo de resolución: {tiempo:.4f} segundos")
            print(f"Nodos explorados: {self.solucion_encontrada['nodos_explorados']}")
            print(f"Nodos expandidos: {self.solucion_encontrada['nodos_expandidos']}")
            print(f"Cartas en memoria: {len(self.solucion_encontrada['estado'].memoria)}")
            print(f"Factor de ramificación efectivo: {self.solucion_encontrada['nodos_explorados'] / max(1, self.solucion_encontrada['nodos_expandidos']):.2f}")
            
            print(f"\nPrimeros pasos de la solución:")
            for i, accion in enumerate(self.solucion_encontrada['camino'][:8], 1):
                print(f"  {i}. {accion}")
            if len(self.solucion_encontrada['camino']) > 8:
                print(f"  ... y {len(self.solucion_encontrada['camino']) - 8} pasos más")


# ===== CLASE COMPARADORA =====
class ComparadorAlgoritmos:
    """Clase para comparar el rendimiento de ambos algoritmos"""
    def __init__(self, tablero):
        self.tablero = tablero
    
    def ejecutar_comparacion(self):
        print("="*70)
        print("COMPARACIÓN: ALGORITMO VORAZ vs A* - JUEGO DE MEMORIA")
        print("="*70)
        print(f"Tablero: {self.tablero}")
        print(f"Dimensión: 6x6 = 36 cartas, 18 pares únicos")
        print("="*70)
        
        # ========== EJECUTAR ALGORITMO VORAZ ==========
        print("\n" + "🚀 " + "="*25 + " ALGORITMO VORAZ " + "="*25 + " 🚀")
        print("Iniciando algoritmo voraz (estrategia greedy)...")
        print("-" * 70)
        
        agente_voraz = AgenteMemorice(self.tablero)
        inicio_voraz = time.time()
        agente_voraz.resolver()
        tiempo_voraz = time.time() - inicio_voraz
        
        print("=" * 70)
        print("VORAZ COMPLETADO ✓")
        print("=" * 70)
        
        # Separador visual
        print("\n" * 2)
        input("Presiona ENTER para continuar con A*...")
        print("\n")
        
        # ========== EJECUTAR ALGORITMO A* ==========
        print("🧠 " + "="*26 + " ALGORITMO A* " + "="*26 + " 🧠")
        print("Iniciando algoritmo A* (búsqueda informada con heurística)...")
        print("-" * 70)
        
        agente_astar = AgentememoriceAstar(self.tablero)
        inicio_astar = time.time()
        resultado_astar = agente_astar.resolver_con_astar()
        tiempo_astar = time.time() - inicio_astar
        
        print("=" * 70)
        print("A* COMPLETADO ✓")
        print("=" * 70)
        
        # ========== MOSTRAR COMPARACIÓN FINAL ==========
        print("\n" * 2)
        input("Presiona ENTER para ver la comparación final...")
        print("\n")
        
        print("📊 " + "="*23 + " COMPARACIÓN FINAL " + "="*23 + " 📊")
        print("RESUMEN COMPARATIVO DE RESULTADOS")
        print("="*70)
        
        print(f"{'Métrica':<30} | {'VORAZ':<15} | {'A*':<15}")
        print("-" * 70)
        print(f"{'Movimientos':<30} | {agente_voraz.movimientos:<15} | {resultado_astar['estado'].movimientos if resultado_astar else 'N/A':<15}")
        print(f"{'Tiempo (seg)':<30} | {tiempo_voraz:<15.4f} | {tiempo_astar:<15.4f}")
        print(f"{'Cartas en memoria':<30} | {len(agente_voraz.memoria):<15} | {len(resultado_astar['estado'].memoria) if resultado_astar else 'N/A':<15}")
        print(f"{'Nodos explorados':<30} | {'1 (directo)':<15} | {agente_astar.nodos_explorados:<15}")
        print(f"{'Nodos expandidos':<30} | {'1 (directo)':<15} | {agente_astar.nodos_expandidos:<15}")
        
        # Análisis de eficiencia
        print("\n" + "="*70)
        print("📋 ANÁLISIS DETALLADO DE ALGORITMOS")
        print("="*70)
        print("🚀 ALGORITMO VORAZ (GREEDY):")
        print("  ✅ Extremadamente rápido y eficiente en memoria")
        print("  ✅ Estrategia simple y directa")
        print("  ✅ Sin complejidad computacional")
        print("  ❌ Puede no encontrar la solución óptima")
        print("  ❌ No considera consecuencias futuras")
        
        print("\n🧠 ALGORITMO A* (BÚSQUEDA INFORMADA):")
        print("  ✅ Garantiza encontrar solución óptima (con heurística admisible)")
        print("  ✅ Usa información heurística para guiar la búsqueda")
        print("  ✅ Considera múltiples estrategias y consecuencias")
        print("  ✅ Sistemático y completo")
        print("  ❌ Más lento y consume más memoria")
        print("  ❌ Complejidad computacional mayor")
        
        # Determinar ganadores
        print("\n" + "="*70)
        print("🏆 RESULTADOS FINALES")
        print("="*70)
        
        if resultado_astar:
            if agente_voraz.movimientos <= resultado_astar['estado'].movimientos:
                print(f"🥇 GANADOR EN EFICIENCIA: VORAZ ({agente_voraz.movimientos} movimientos)")
                print(f"🥈 A*: {resultado_astar['estado'].movimientos} movimientos")
            else:
                print(f"🥇 GANADOR EN EFICIENCIA: A* ({resultado_astar['estado'].movimientos} movimientos)")  
                print(f"🥈 VORAZ: {agente_voraz.movimientos} movimientos")
            
            if tiempo_voraz <= tiempo_astar:
                print(f"⚡ GANADOR EN VELOCIDAD: VORAZ ({tiempo_voraz:.4f} segundos)")
                print(f"🐌 A*: {tiempo_astar:.4f} segundos")
            else:
                print(f"⚡ GANADOR EN VELOCIDAD: A* ({tiempo_astar:.4f} segundos)")
                print(f"🐌 VORAZ: {tiempo_voraz:.4f} segundos")
                
            # Análisis de trade-off
            print(f"\n💡 TRADE-OFF ANÁLISIS:")
            factor_tiempo = tiempo_astar / tiempo_voraz if tiempo_voraz > 0 else float('inf')
            diferencia_movimientos = abs(agente_voraz.movimientos - resultado_astar['estado'].movimientos)
            
            print(f"   • A* es {factor_tiempo:.1f}x más lento que Voraz")
            print(f"   • Diferencia en movimientos: {diferencia_movimientos}")
            
            if diferencia_movimientos <= 2 and factor_tiempo > 100:
                print(f"   🎯 RECOMENDACIÓN: Usar VORAZ (diferencia mínima, mucho más rápido)")
            elif diferencia_movimientos > 5:
                print(f"   🎯 RECOMENDACIÓN: Usar A* (mejora significativa en eficiencia)")
            else:
                print(f"   🎯 RECOMENDACIÓN: Depende del contexto (velocidad vs precisión)")
        
        return {
            'voraz': {
                'movimientos': agente_voraz.movimientos,
                'tiempo': tiempo_voraz,
                'memoria': len(agente_voraz.memoria)
            },
            'astar': {
                'movimientos': resultado_astar['estado'].movimientos if resultado_astar else None,
                'tiempo': tiempo_astar,
                'nodos_explorados': agente_astar.nodos_explorados,
                'memoria': len(resultado_astar['estado'].memoria) if resultado_astar else None
            } if resultado_astar else None
        }


if __name__ == "__main__":
    # Tablero de ejemplo
    tablero_ejemplo = [1, 5, 2, 8, 1, 3, 7, 2, 9, 4, 6, 5, 
                      10, 3, 11, 7, 12, 4, 13, 8, 14, 6, 15, 9,
                      16, 10, 17, 11, 18, 12, 13, 14, 15, 16, 17, 18]
    
    # Ejecutar comparación
    comparador = ComparadorAlgoritmos(tablero_ejemplo)
    resultados = comparador.ejecutar_comparacion()
    
    print("\n" + "="*70)
    print("EJECUCIÓN COMPLETADA - ANÁLISIS FINALIZADO")
    print("="*70)