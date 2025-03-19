from Nodo import Nodo


def profundidad(mundo, filas, columnas, posPaquetes, posInicial):
    nodoInicial = Nodo(posInicial, None, set())
    stack = [(nodoInicial, set())]  # Usamos una lista que simulara una pila, que almacena tuplas: (nodo, estados visitados en la rama)

    while stack:
        nodo, visitadosRama = stack.pop()  # Extraemos el último nodo (LIFO)

        if len(nodo.paquetes) == len(posPaquetes):  
            return nodo.construirCamino()  # Retorna el camino si ya recogió todos los paquetes
        
        # Marcar este estado como visitado en esta rama
        estado = (nodo.posición, frozenset(nodo.paquetes))
        visitadosRama.add(estado)

        # Acá definimos el orden de los operadores, que por la estructura de pila es inverso a como se agregan.
        # Por tanto es: derecha, abajo, izquierda, arriba. Se priorizaron de esta manera porque es óptimo para el mundo 
        # definido en el proyecto, pero no necesariamente es el mejor orden para otros mundos.
        movimientosPosibles = [(nodo.posición[0] - 1, nodo.posición[1]),  # Arriba
                               (nodo.posición[0], nodo.posición[1] - 1),  # Izquierda
                               (nodo.posición[0] + 1, nodo.posición[1]),  # Abajo
                               (nodo.posición[0], nodo.posición[1] + 1)]  # Derecha           

        for movimiento in movimientosPosibles:
            if 0 <= movimiento[0] < filas and 0 <= movimiento[1] < columnas: # Verifica que esté dentro del mundo
                if mundo[movimiento[0]][movimiento[1]] != 1:  # Verifica que no es obstáculo
        
                    paquetes = set(nodo.paquetes) # Crea un nuevo set con los paquetes recogidos del nodo padre
                    
                    if movimiento in posPaquetes:
                        paquetes.add(movimiento) # Si la nueva posición es un paquete, se añade la coordenada del paquete recogido

                    nuevoEstado = (movimiento, frozenset(paquetes))
                    
                    if nuevoEstado not in visitadosRama:  # Verifica si el estado actual ya ha sido visitado, para evitar ciclos en esta rama
                        # Se añade el nodo a la pila, junto con los estados visitados en esta rama
                        stack.append((Nodo(movimiento, nodo, paquetes), visitadosRama.copy()))  