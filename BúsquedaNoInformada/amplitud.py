from collections import deque
import time
from Nodo import Nodo

def amplitud(mundo, filas, columnas, posPaquetes, posInicial):
    inicio_tiempo = time.time()
    nodoInicial = Nodo(posInicial, None, set(), profundidad=0)
    queue = deque([nodoInicial])
    nodosCreadosLista = [nodoInicial]
    nodosExpandidosCount = 0
    profundidad_maxima = 0

    # Lista para almacenar los estados (posición + paquetes recogidos) visitados
    estadosVisitados = [(posInicial, frozenset())]

    while queue:
        nodo = queue.popleft()

        # Primero verificamos si el nodo ya es una solución
        if len(nodo.paquetes) == len(posPaquetes):
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo
            profundidad_solucion = nodo.profundidad
            camino = nodo.construirCamino()
            return camino, tiempo_ejecucion, nodosExpandidosCount, profundidad_solucion

        # Solo si no era solución, lo contamos como expandido
        nodosExpandidosCount += 1
        profundidad_maxima = max(profundidad_maxima, nodo.profundidad)

        movimientosPosibles = [
            (nodo.posición[0] - 1, nodo.posición[1]),  # Arriba
            (nodo.posición[0], nodo.posición[1] - 1),   # Izquierda
            (nodo.posición[0] + 1, nodo.posición[1]),  # Abajo
            (nodo.posición[0], nodo.posición[1] + 1)  # Derecha
            
        ]

        for movimiento in movimientosPosibles:
            if 0 <= movimiento[0] < filas and 0 <= movimiento[1] < columnas:
                if mundo[movimiento[0]][movimiento[1]] != 1:  # No es un obstáculo
                    paquetes = set(nodo.paquetes)
                    if movimiento in posPaquetes:
                        paquetes.add(movimiento)

                    estado = (movimiento, frozenset(paquetes))

                    if estado not in estadosVisitados:
                        estadosVisitados.append(estado)
                        nuevo_nodo = Nodo(movimiento, nodo, paquetes, profundidad=nodo.profundidad + 1)
                       
                        queue.append(nuevo_nodo)
                        nodosCreadosLista.append(nuevo_nodo)

    fin_tiempo = time.time()
    tiempo_ejecucion = fin_tiempo - inicio_tiempo
    return None, tiempo_ejecucion, nodosExpandidosCount, profundidad_maxima
