from Nodo import Nodo
import time

def profundidad(mundo, filas, columnas, posPaquetes, posInicial):
    inicio_tiempo = time.time()
    nodoInicial = Nodo(posInicial, None, set(), profundidad=0)
    stack = [(nodoInicial, set())]
    nodos_expandidos = 0
    profundidad_maxima = 0

    while stack:
        nodo, visitadosRama = stack.pop()

        # Verificar si el nodo actual es la solución ANTES de expandirlo
        if len(nodo.paquetes) == len(posPaquetes):
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo
            camino = nodo.construirCamino()
            return camino, tiempo_ejecucion, nodos_expandidos, nodo.profundidad

        # Si no es la solución, lo contamos como expandido
        nodos_expandidos += 1
        profundidad_maxima = max(profundidad_maxima, nodo.profundidad)

        estado = (nodo.posición, frozenset(nodo.paquetes))
        visitadosRama.add(estado)

        movimientosPosibles = [
            (nodo.posición[0] - 1, nodo.posición[1]),   # Arriba
            (nodo.posición[0], nodo.posición[1] - 1),   # Izquierda
            (nodo.posición[0] + 1, nodo.posición[1]),   # Abajo
            (nodo.posición[0], nodo.posición[1] + 1)    # Derecha
        ]

        for movimiento in movimientosPosibles:
            if 0 <= movimiento[0] < filas and 0 <= movimiento[1] < columnas:
                if mundo[movimiento[0]][movimiento[1]] != 1:
                    paquetes = set(nodo.paquetes)
                    if movimiento in posPaquetes and movimiento not in paquetes:
                        paquetes.add(movimiento)

                    nuevoEstado = (movimiento, frozenset(paquetes))

                    if nuevoEstado not in visitadosRama:
                        nuevo_nodo = Nodo(movimiento, nodo, paquetes, profundidad=nodo.profundidad + 1)
                        stack.append((nuevo_nodo, visitadosRama.copy()))

    fin_tiempo = time.time()
    tiempo_ejecucion = fin_tiempo - inicio_tiempo
    return None, tiempo_ejecucion, nodos_expandidos, profundidad_maxima