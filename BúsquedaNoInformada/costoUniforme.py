import heapq
import time 
from Nodo import Nodo

def costoUniforme(mundo, filas, columnas, posPaquetes, posInicial):
    inicio_tiempo = time.time()
    nodoInicial = Nodo(posInicial, None, set(), 0, 0)  # profundidad y costo en 0
    nodosExpandidosLista = []
    nodosExpandidos = [(0, nodoInicial)]  # Cola de prioridad con (costo, nodo)
    visitados = set()  # Estados visitados (posición, paquetes)
    profundidad_maxima = 0

    costo_minimo = {(posInicial, frozenset()): 0}

    while nodosExpandidos:
        costoMin, nodo = heapq.heappop(nodosExpandidos)
        estado_actual = (nodo.posición, frozenset(nodo.paquetes))

        if estado_actual in visitados:
            continue

        # Verificamos primero si es solución
        if len(nodo.paquetes) == len(posPaquetes):
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo
            camino = nodo.construirCamino()
            costo_total = nodo.costo
            nodos_expandidos_count = len(nodosExpandidosLista)
            profundidad_solucion = nodo.profundidad
            return camino, tiempo_ejecucion, nodos_expandidos_count, profundidad_solucion, costo_total

        # Si no es solución, lo marcamos como visitado y lo expandimos
        visitados.add(estado_actual)
        nodosExpandidosLista.append(nodo)
        profundidad_maxima = max(profundidad_maxima, nodo.profundidad)

        movimientosPosibles = [
            (nodo.posición[0] + 1, nodo.posición[1]),  # Abajo
            (nodo.posición[0] - 1, nodo.posición[1]),  # Arriba
            (nodo.posición[0], nodo.posición[1] + 1),  # Derecha
            (nodo.posición[0], nodo.posición[1] - 1)   # Izquierda
        ]

        for movimiento in movimientosPosibles:
            if 0 <= movimiento[0] < filas and 0 <= movimiento[1] < columnas:
                if mundo[movimiento[0]][movimiento[1]] != 1:
                    nuevo_costo = nodo.costo + (8 if mundo[movimiento[0]][movimiento[1]] == 3 else 1)
                    paquetes_nuevos = set(nodo.paquetes)
                    if movimiento in posPaquetes:
                        paquetes_nuevos.add(movimiento)

                    estado = (movimiento, frozenset(paquetes_nuevos))

                    if estado not in costo_minimo or nuevo_costo < costo_minimo[estado]:
                        costo_minimo[estado] = nuevo_costo
                        nuevoNodo = Nodo(movimiento, nodo, paquetes_nuevos, nuevo_costo, nodo.profundidad + 1)
                        heapq.heappush(nodosExpandidos, (nuevo_costo, nuevoNodo))

    fin_tiempo = time.time()
    tiempo_ejecucion = fin_tiempo - inicio_tiempo
    nodos_expandidos_count = len(nodosExpandidosLista)
    return None, tiempo_ejecucion, nodos_expandidos_count, profundidad_maxima, None
