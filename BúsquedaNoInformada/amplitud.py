from collections import deque
from Nodo import Nodo


def amplitud(mundo, filas, columnas, posPaquetes, posInicial):

    nodoInicial = Nodo(posInicial, None, set())
    queue = deque([nodoInicial])

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
                if (mundo[movimiento[0]][movimiento[1]] != 1): # Verifica que no hay pared
                    paquetes = nodo.paquetes.copy()
                    if (movimiento in posPaquetes): # Si la nueva posición es un paquete, se añade la coordenada del paquete recogido
                        paquetes.add(movimiento)
                    queue.append(Nodo(movimiento, nodo, paquetes)) # Se agrega el nodo a la cola
                    #print("Nodo expandido: ", nodo)
        



                

