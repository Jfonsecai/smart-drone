from BúsquedaNoInformada.costoUniforme import costoUniforme
from BúsquedaNoInformada.amplitud import amplitud
from BúsquedaNoInformada.profundidad import profundidad

def main():

    mundo = [
        [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [0, 2, 0, 3, 4, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [3, 3, 0, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    # Tamaño del mundo
    filas = len(mundo)
    columnas = len(mundo[0])

    # Almacenar las posiciones de los paquetes y el dron
    posPaquetes = []

    for i in range (filas):
        for j in range (columnas):
            if (mundo[i][j] == 2):
                posInicial = (i, j)
            if (mundo[i][j] == 4):
                posPaquetes.append((i, j))

    #camino = amplitud(mundo, filas, columnas, posPaquetes, posInicial)
    #camino = costoUniforme(mundo, filas, columnas, posPaquetes, posInicial)
    camino = profundidad(mundo, filas, columnas, posPaquetes, posInicial)
    print(camino)

    # Visualizar el camino en el mundo
    for i in range(10):
        for j in range(10):
            if (i, j) in camino:
                print("D", end=" ")  # Marca el dron en el camino
            elif mundo[i][j] == 1:
                print("█", end=" ")  # Obstáculo
            elif mundo[i][j] == 3:
                print("~", end=" ")  # Campo electromagnético
            elif mundo[i][j] == 4:
                print("P", end=" ")  # Paquete
            elif mundo[i][j] == 2:
                print("S", end=" ")  # Posición inicial
            else:
                print(".", end=" ")  # Espacio libre
        print()

if __name__ == "__main__":
    main()