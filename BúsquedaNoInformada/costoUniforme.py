import heapq
from Nodo import Nodo


def costoUniforme(mundo, filas, columnas, posPaquetes, posInicial):
    nodoInicial = Nodo(posInicial, None, set(), 0)
    nodosExpandidos = [] 
    heapq.heappush(nodosExpandidos, (0, nodoInicial)) # Los nodos se almacenan en una cola de prioridad, ordenada por su costo

    # Diccionario para almacenar el menor costo por estado (es decir, posición + paquetes recogidos)
    costo_minimo = {(posInicial, frozenset()): 0}

    while nodosExpandidos:
        costoMin, nodo = heapq.heappop(nodosExpandidos)  # Extrae el nodo con menor costo

        if len(nodo.paquetes) == len(posPaquetes):  # Si recogió todos los paquetes, termina
            print("Costo total de la solución: ", nodo.costo)
            return nodo.construirCamino()
        
        # Generar movimientos válidos
        movimientosPosibles = [
            (nodo.posición[0] + 1, nodo.posición[1]),  # Abajo
            (nodo.posición[0] - 1, nodo.posición[1]),  # Arriba
            (nodo.posición[0], nodo.posición[1] + 1),  # Derecha
            (nodo.posición[0], nodo.posición[1] - 1)   # Izquierda
        ]

        for movimiento in movimientosPosibles:
            if 0 <= movimiento[0] < filas and 0 <= movimiento[1] < columnas:  # Verifica si está dentro del mundo
                if mundo[movimiento[0]][movimiento[1]] != 1:  # Verifica que no es un obstáculo
                    # Si cumple ambas condiciones, es un movimiento válido, por lo que se calcula su costo
                    nuevo_costo = nodo.costo + (8 if mundo[movimiento[0]][movimiento[1]] == 3 else 1)

                    # Copia el conjunto de paquetes del nodo padre
                    paquetes_nuevos = set(nodo.paquetes)  

                    if movimiento in posPaquetes:
                        paquetes_nuevos.add(movimiento) # Si hay un paquete en la posición, se añade al conjunto

                    estado = (movimiento, frozenset(paquetes_nuevos))  # Estado actual, con posición y paquetes recogidos

                    # Verificar si este estado ha sido visitado antes con menor costo
                    if estado not in costo_minimo or nuevo_costo < costo_minimo[estado]:
                        costo_minimo[estado] = nuevo_costo  # Actualizar menor costo
                        # Si el estado no ha sido visitado antes o el costo actual es menor, se crea un nuevo nodo
                        nuevoNodo = Nodo(movimiento, nodo, paquetes_nuevos, nuevo_costo)
                        heapq.heappush(nodosExpandidos, (nuevo_costo, nuevoNodo))  # Agregar a la cola