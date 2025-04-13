from collections import deque
import time
from Nodo import Nodo


def amplitud(mundo, filas, columnas, posPaquetes, posInicial):
    inicio_tiempo = time.time()
    nodoInicial = Nodo(posInicial, None, set(), profundidad=0)
    queue = deque([nodoInicial])
    nodosExpandidosLista = [nodoInicial]
    profundidad_maxima = 0

    # Lista para almacenar los estados (posición + paquetes recogidos) visitados
    estadosVisitados = [(posInicial, frozenset())]

    while queue:
        nodo = queue.popleft() # Extrae el primer nodo de la cola
        profundidad_maxima = max(profundidad_maxima, nodo.profundidad)

        if (len(nodo.paquetes) == len(posPaquetes)):
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo
            nodos_expandidos_count = len(nodosExpandidosLista)
            profundidad_solucion = nodo.profundidad
            camino = nodo.construirCamino()
            return camino, tiempo_ejecucion, nodos_expandidos_count, profundidad_solucion

        movimientosPosibles = [(nodo.posición[0] + 1, nodo.posición[1]), # Abajo
                                (nodo.posición[0] - 1, nodo.posición[1]),  # Arriba
                                (nodo.posición[0], nodo.posición[1] + 1),  # Derecha
                                (nodo.posición[0], nodo.posición[1] - 1)]  # Izquierda

        for movimiento in movimientosPosibles:
            # Verifica si el movimiento está dentro del mundo
            if 0 <= movimiento[0] < filas and 0 <= movimiento[1] < columnas:
                if (mundo[movimiento[0]][movimiento[1]] != 1): # Verifica que no es un obstáculo
                    # Si cumple ambas condiciones, es un movimiento válido
                    paquetes = set(nodo.paquetes) # Crea un nuevo set con los paquetes recogidos del nodo padre
                    if (movimiento in posPaquetes):
                        paquetes.add(movimiento) # Si la nueva posición es un paquete, se añade la coordenada del paquete recogido

                    estado = (movimiento, frozenset(paquetes))  # Estado actual, con posición y paquetes recogidos

                    # Verificar si este estado ha sido visitado antes
                    if estado not in estadosVisitados:
                        estadosVisitados.append(estado)  # Si no ha sido visitado, se añade a los estados visitados
                        nuevo_nodo = Nodo(movimiento, nodo, paquetes, profundidad=nodo.profundidad + 1)
                        queue.append(nuevo_nodo) # Se agrega el nodo a la cola
                        nodosExpandidosLista.append(nuevo_nodo)

    fin_tiempo = time.time()
    tiempo_ejecucion = fin_tiempo - inicio_tiempo
    nodos_expandidos_count = len(nodosExpandidosLista)
    return None, tiempo_ejecucion, nodos_expandidos_count, profundidad_maxima