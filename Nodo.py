class Nodo():
    def __init__(self, posición, padre=None, paquetes=None):
        self.posición = posición
        self.padre = padre
        #self.accion = accion
        self.paquetes = paquetes if paquetes else set() 

    def construirCamino(self):
        """Reconstruye el camino desde el nodo raíz hasta este nodo."""
        camino = []
        nodo = self
        while nodo: # Mientras exista un nodo padre
            camino.append(nodo.posición)
            nodo = nodo.padre
        return camino[::-1]  # Se invierte para que el camino sea de inicio a fin