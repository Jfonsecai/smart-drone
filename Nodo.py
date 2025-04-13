class Nodo():
    def __init__(self, posición, padre=None, paquetes=None, costo=0, profundidad=0):
        self.posición = posición
        self.padre = padre
        #self.accion = accion
        self.paquetes = paquetes if paquetes else set()
        self.costo = costo
        self.profundidad = profundidad

    def construirCamino(self):
        """Reconstruye el camino desde el nodo raíz hasta este nodo."""
        camino = []
        nodo = self
        while nodo: # Mientras exista un nodo padre
            camino.append(nodo.posición)
            nodo = nodo.padre
        return camino[::-1]  # Se invierte para que el camino sea de inicio a fin

    def __lt__(self, otro):
        return self.costo < otro.costo  # Comparación por costo