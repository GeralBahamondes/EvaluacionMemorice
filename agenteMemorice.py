import time
class AgenteMemorice:
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
                # Estrategia mejorada: explorar 2 cartas por turno
                cartas_exploradas = 0
                for pos in range(36):
                    if pos not in self.memoria and pos not in self.emparejadas and cartas_exploradas < 2:
                        self.memoria[pos] = self.tablero[pos]
                        print(f"Explorando posición {pos}, encontré valor {self.tablero[pos]}")
                        cartas_exploradas += 1
                self.movimientos += 1
        
        tiempo_total = time.time() - inicio_tiempo
        self.mostrar_estadisticas(tiempo_total)

    def mostrar_estadisticas(self, tiempo):
        print("\n=== JUEGO COMPLETADO ===")
        print(f"Movimientos totales: {self.movimientos}")
        print(f"Tiempo de resolución: {tiempo:.4f} segundos")
        print(f"Cartas en memoria: {len(self.memoria)}")
        


if __name__ == "__main__":

    tablero_ejemplo = [1, 5, 2, 8, 1, 3, 7, 2, 9, 4, 6, 5, 
                      10, 3, 11, 7, 12, 4, 13, 8, 14, 6, 15, 9,
                      16, 10, 17, 11, 18, 12, 13, 14, 15, 16, 17, 18]
    
    agente = AgenteMemorice(tablero_ejemplo)
    agente.resolver()