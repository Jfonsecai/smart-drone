import time
from heapq import heappush, heappop
from Nodo import Nodo

def distancia_manhattan(pos1, pos2):
    # Calcula la distancia Manhattan entre dos posiciones
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def calcular_heuristica(pos, paquetes_por_recoger):
    ## Calcula la heurística como la distancia al paquete más cercano.
    ## Si no hay paquetes por recoger, la heurística es 0.
    if not paquetes_por_recoger:
        return 0
    
    # Encontrar la distancia al paquete más cercano
    return min(distancia_manhattan(pos, paquete) for paquete in paquetes_por_recoger)

def avara(mundo, filas, columnas, posPaquetes, posInicial):
    # Convertir la lista de paquetes a un conjunto para operaciones más eficientes
    paquetes_objetivo = set(posPaquetes)
    total_paquetes = len(paquetes_objetivo)
    
    # Crear el nodo inicial
    nodo_inicial = Nodo(posInicial, None, set(), 0, 0)
    
    # Definir los movimientos posibles (arriba, abajo, izquierda, derecha)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Cola de prioridad para la búsqueda
    cola_prioridad = []
    
    # Calcular la heurística inicial
    heuristica_inicial = calcular_heuristica(posInicial, paquetes_objetivo)
    heappush(cola_prioridad, (heuristica_inicial, nodo_inicial))  # (heurística, nodo)
    
    # Conjunto para almacenar estados visitados (posición, paquetes recogidos)
    visitados = set()

    # Variables para los nodos y la produndidad máxima
    inicio_tiempo = time.time()
    nodos_expandidos = 0
    profundidad_maxima = 0
    
    while cola_prioridad:
        _, nodo_actual = heappop(cola_prioridad)
        nodos_expandidos += 1
        profundidad_maxima = max(profundidad_maxima, nodo_actual.profundidad)
        
        # Verificar si estamos en un paquete y actualizar la lista de paquetes recogidos
        if nodo_actual.posición in paquetes_objetivo:
            nodo_actual.paquetes.add(nodo_actual.posición)
        
        # Si ya hemos recogido todos los paquetes, hemos terminado
        if len(nodo_actual.paquetes) == total_paquetes:
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo

            print("\n[SOLUCIÓN ENCONTRADA]")
            print(f"Profundidad de la solución: {nodo_actual.profundidad}")
            print(f"Nodos expandidos: {nodos_expandidos}")
            print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
            print(f"Profundidad máxima alcanzada: {profundidad_maxima}")

            camino = nodo_actual.construirCamino()
            print("\n[CAMINO SOLUCIÓN]")
            for i, paso in enumerate(camino):
                print(f"Paso {i+1}: {paso}")

            return camino, tiempo_ejecucion, nodos_expandidos, nodo_actual.profundidad,None
        
        # Crear un identificador único para el estado actual
        estado_actual = (nodo_actual.posición, frozenset(nodo_actual.paquetes))
        
        # Si ya visitamos este estado, continuamos
        if estado_actual in visitados:
            continue
        
        # Marcar como visitado
        visitados.add(estado_actual)
        
        # Explorar los vecinos
        for dx, dy in movimientos:
            nueva_fila, nueva_col = nodo_actual.posición[0] + dx, nodo_actual.posición[1] + dy
            
            # Verificar si la nueva posición es válida
            if (0 <= nueva_fila < filas and 0 <= nueva_col < columnas and 
                mundo[nueva_fila][nueva_col] != 1):  # No es un obstáculo
                
                nueva_pos = (nueva_fila, nueva_col)
                nuevo_costo = nodo_actual.costo + 1  # Costo uniforme por cada movimiento
                
                # Si es un campo electromagnético, aumentamos el costo
                if mundo[nueva_fila][nueva_col] == 3:
                    nuevo_costo += 2
                
                # Copiar los paquetes recogidos hasta ahora
                paquetes_recogidos = set(nodo_actual.paquetes)
                
                # Calcular la heurística: distancia al paquete más cercano que no hemos recogido
                paquetes_por_recoger = paquetes_objetivo - paquetes_recogidos
                heuristica = calcular_heuristica(nueva_pos, paquetes_por_recoger)
                
                # Crear el nuevo nodo
                nuevo_nodo = Nodo(
                    nueva_pos, 
                    nodo_actual, 
                    paquetes_recogidos, 
                    nuevo_costo, 
                    nodo_actual.profundidad + 1,
                    heuristica
                )
                
                # Agregar a la cola de prioridad
                heappush(cola_prioridad, (heuristica, nuevo_nodo))
    
    # Si no encontramos solución
    print("\n[NO SE ENCONTRÓ SOLUCIÓN]")
    print(f"Nodos expandidos: {nodos_expandidos}")
    print(f"Tiempo de ejecución: {fin_tiempo - inicio_tiempo:.4f} segundos")
    return None