from collections import deque
from Nodo import Nodo


def amplitud(mundo, filas, columnas, posPaquetes, posInicial):

    nodoInicial = Nodo(posInicial, None, set())
    queue = deque([nodoInicial])

    # Lista para almacenar los estados (posición + paquetes recogidos) visitados
    estadosVisitados = [(posInicial, frozenset())]

    while queue:
        nodo = queue.popleft() # Extrae el primer nodo de la cola
        if (len(nodo.paquetes) == len(posPaquetes)): 
            return nodo.construirCamino() # Retorna el camino si ya se encontraron los 3 paquetes
        
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
                        queue.append(Nodo(movimiento, nodo, paquetes)) # Se agrega el nodo a la cola
        



                

