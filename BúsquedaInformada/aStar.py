from heapq import heappush, heappop
from Nodo import Nodo
import time

def distancia_manhattan(pos1, pos2):
    # Manhattan para la distancia entre 2 posiciones
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def calcular_heuristica(pos, paquetes_por_recoger):
    # Misma Heuristica que en avara
    if not paquetes_por_recoger:
        return 0
    
    # Encontrar la distancia al paquete más cercano
    return min(distancia_manhattan(pos, paquete) for paquete in paquetes_por_recoger)

def aStar(mundo, filas, columnas, posPaquetes, posInicial):
    # Iniciar el contador de tiempo
    tiempo_inicio = time.time()
    
    # Convertir la lista de paquetes a un conjunto para operaciones más eficientes
    paquetes_objetivo = set(posPaquetes)
    total_paquetes = len(paquetes_objetivo)
    
    # Calcular la heurística inicial
    heuristica_inicial = calcular_heuristica(posInicial, paquetes_objetivo)
    
    # Crear el nodo inicial
    nodo_inicial = Nodo(posInicial, None, set(), 0, 0, heuristica_inicial)
    
    # Definir los movimientos posibles (arriba, abajo, izquierda, derecha)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Cola de prioridad para la búsqueda
    cola_prioridad = []
    
    # En A*, ordenamos por f(n) = g(n) + h(n)
    # g(n) = costo acumulado hasta el nodo, h(n) = heurística
    f_inicial = nodo_inicial.costo + nodo_inicial.heuristica
    heappush(cola_prioridad, (f_inicial, nodo_inicial))  # (f(n), nodo)
    
    # Conjunto para almacenar estados visitados (posición, paquetes recogidos)
    visitados = set()
    
    # Diccionario para mantener el mejor costo (g) para cada estado
    mejor_costo = {}
    
    # Contadores para estadísticas
    nodos_expandidos = 0
    profundidad_maxima = 0
    
    while cola_prioridad:
        _, nodo_actual = heappop(cola_prioridad)
        nodos_expandidos += 1
        
        # Actualizar la profundidad máxima alcanzada
        profundidad_maxima = max(profundidad_maxima, nodo_actual.profundidad)
        
        # Verificar si estamos en un paquete y actualizar la lista de paquetes recogidos
        # if nodo_actual.posición in paquetes_objetivo:
        #     nodo_actual.paquetes.add(nodo_actual.posición)
        
        # Si ya hemos recogido todos los paquetes, hemos terminado
        if len(nodo_actual.paquetes) == total_paquetes:
            tiempo_fin = time.time()
            tiempo_ejecucion = tiempo_fin - tiempo_inicio
            camino = nodo_actual.construirCamino()
            
            # Devolver resultados: camino, tiempo, nodos expandidos, profundidad, costo
            return (camino, tiempo_ejecucion, nodos_expandidos, nodo_actual.profundidad, nodo_actual.costo)
        
        # Crear un identificador único para el estado actual
        estado_actual = (nodo_actual.posición, frozenset(nodo_actual.paquetes))
        
        # Si ya visitamos este estado con un mejor costo, continuamos
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
            
                # Verificamos si es un campo electromagnético y aumentamos el costo de acuerdo a eso
                if mundo[nueva_fila][nueva_col] == 3:
                    nuevo_costo = nodo_actual.costo + 8
                else:
                    nuevo_costo = nodo_actual.costo + 1
                
                # Copiar los paquetes recogidos hasta ahora
                paquetes_recogidos = set(nodo_actual.paquetes)
                # Verificar si recogemos un nuevo paquete
                if nueva_pos in paquetes_objetivo:
                    paquetes_recogidos.add(nueva_pos)
                
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
                
                # Crear un identificador único para el nuevo estado
                nuevo_estado = (nueva_pos, frozenset(paquetes_recogidos))
                
                # Verificar si ya visitamos este estado con un mejor costo
                if nuevo_estado in mejor_costo and mejor_costo[nuevo_estado] <= nuevo_costo:
                    continue
                
                # Actualizar el mejor costo para este estado
                mejor_costo[nuevo_estado] = nuevo_costo
                
                # Calcular f(n) = g(n) + h(n) para el nuevo nodo
                f_valor = nuevo_costo + heuristica
                
                # Agregar a la cola de prioridad
                heappush(cola_prioridad, (f_valor, nuevo_nodo))
    
    # Si no encontramos solución
    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio
    
    # Devolver: lista vacía (no hay camino), tiempo, nodos expandidos, profundidad máxima
    return None, tiempo_ejecucion, nodos_expandidos, profundidad_maxima, None