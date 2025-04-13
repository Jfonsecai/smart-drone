from Nodo import Nodo
import time

def profundidad(mundo, filas, columnas, posPaquetes, posInicial):
    inicio_tiempo = time.time()
    nodoInicial = Nodo(posInicial, None, set(), profundidad=0)
    stack = [(nodoInicial, set())]
    nodos_expandidos = 0  # ✅ Contador en lugar de lista
    profundidad_maxima = 0
    iteracion = 0

    while stack:
        iteracion += 1
        nodo, visitadosRama = stack.pop()
        nodos_expandidos += 1  # ✅ Incrementamos solo al expandir

        profundidad_maxima = max(profundidad_maxima, nodo.profundidad)

        if iteracion == 1:
            print(f"\nIteración: {iteracion} | Stack: {stack} | Profundidad actual: {nodo.profundidad}")
            print(f"Posición actual: {nodo.posición} | Paquetes: {len(nodo.paquetes)}/{len(posPaquetes)}")

        if len(nodo.paquetes) == len(posPaquetes):
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo

            print("\n[SOLUCIÓN ENCONTRADA]")
            print(f"Profundidad de la solución: {nodo.profundidad}")
            print(f"Nodos expandidos: {nodos_expandidos}")
            print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
            print(f"Profundidad máxima alcanzada: {profundidad_maxima}")

            camino = nodo.construirCamino()
            print("\n[CAMINO SOLUCIÓN]")
            for i, paso in enumerate(camino):
                print(f"Paso {i+1}: {paso}")

            return camino, tiempo_ejecucion, nodos_expandidos, nodo.profundidad

        estado = (nodo.posición, frozenset(nodo.paquetes))
        visitadosRama.add(estado)

        movimientosPosibles = [
            (nodo.posición[0] - 1, nodo.posición[1]),  # Arriba
            (nodo.posición[0], nodo.posición[1] - 1),  # Izquierda
            (nodo.posición[0] + 1, nodo.posición[1]),  # Abajo
            (nodo.posición[0], nodo.posición[1] + 1)   # Derecha
        ]

        for movimiento in movimientosPosibles:
            if 0 <= movimiento[0] < filas and 0 <= movimiento[1] < columnas:
                if mundo[movimiento[0]][movimiento[1]] != 1:
                    paquetes = set(nodo.paquetes)

                    if movimiento in posPaquetes and movimiento not in paquetes:
                        paquetes.add(movimiento)
                        print(f"\n¡PAQUETE RECOGIDO! Posición: {movimiento} | Total: {len(paquetes)}/{len(posPaquetes)}")

                    nuevoEstado = (movimiento, frozenset(paquetes))

                    if nuevoEstado not in visitadosRama:
                        nuevo_nodo = Nodo(movimiento, nodo, paquetes, profundidad=nodo.profundidad + 1)
                        stack.append((nuevo_nodo, visitadosRama.copy()))
                        print(f"  Nodo creado: Posición {movimiento}, Profundidad {nuevo_nodo.profundidad}")

    fin_tiempo = time.time()
    tiempo_ejecucion = fin_tiempo - inicio_tiempo

    print("\n[NO SE ENCONTRÓ SOLUCIÓN]")
    print(f"Profundidad máxima alcanzada: {profundidad_maxima}")
    print(f"Nodos expandidos: {nodos_expandidos}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")

    return None, tiempo_ejecucion, nodos_expandidos, profundidad_maxima
