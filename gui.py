import pygame
import os
from PIL import Image, ImageSequence
from BúsquedaNoInformada.amplitud import amplitud
from BúsquedaNoInformada.costoUniforme import costoUniforme
from BúsquedaNoInformada.profundidad import profundidad
from BúsquedaInformada.avara import avara
from BúsquedaInformada.aStar import aStar
from Nodo import Nodo

pygame.init()

# Constantes - Ventana principal
ancho_principal, alto_principal = 1100, 600
celdaTamano = 60
fuente = pygame.font.SysFont('Arial', 24)
fuente_pequena = pygame.font.SysFont('Arial', 20)
pantalla_principal = pygame.display.set_mode((ancho_principal, alto_principal))
pygame.display.set_caption("Smart Dron Packer")
clock = pygame.time.Clock()

# Constantes - Ventana emergente
ancho_emergente = 350
alto_emergente = 150  # Reduje la altura
fuente_emergente = pygame.font.SysFont('Arial', 18)

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS_OSCURO = (40, 40, 40)
GRIS_MEDIO = (60, 60, 60)
GRIS_CLARO = (80, 80, 80)
AZUL_BOTON = (0, 150, 255)
ROJO_ERROR = (150, 50, 50)
VERDE_INFO = (50, 150, 50)

# Cargar imágenes
img_valla = pygame.transform.scale(pygame.image.load("Smart-drone/assets/valla.png"), (celdaTamano, celdaTamano))
img_caja = pygame.transform.scale(pygame.image.load("Smart-drone/assets/box.png"), (celdaTamano, celdaTamano))
img_campo = pygame.transform.scale(pygame.image.load("Smart-drone/assets/campo-magnetico.png"), (celdaTamano, celdaTamano))
img_piso = pygame.transform.scale(pygame.image.load("Smart-drone/assets/fondo.png"), (celdaTamano, celdaTamano))

# Cargar GIF dron
ruta_gif = "Smart-drone/assets/dron-moving.gif"
imagen_gif = Image.open(ruta_gif)
frames = []
for frame in ImageSequence.Iterator(imagen_gif):
    frame = frame.convert("RGBA")
    img_pygame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    img_pygame = pygame.transform.scale(img_pygame, (celdaTamano, celdaTamano))
    frames.append(img_pygame)

# Funciones auxiliares
def cargar_mapa(nombre_archivo):
    ruta_completa = os.path.join("Smart-drone/maps", nombre_archivo)
    with open(ruta_completa, "r") as archivo:
        return [list(map(int, linea.strip().split())) for linea in archivo]

def buscar_posiciones(mundo):
    pos_inicial = None
    pos_paquetes = []
    for i, fila in enumerate(mundo):
        for j, celda in enumerate(fila):
            if celda == 2:
                pos_inicial = (i, j)
            elif celda == 4:
                pos_paquetes.append((i, j))
    return pos_inicial, pos_paquetes

def mostrar_ventana_emergente(texto):
    ventana_emergente = pygame.Surface((ancho_emergente, alto_emergente))
    ventana_emergente.fill(GRIS_OSCURO)
    pygame.draw.rect(ventana_emergente, GRIS_CLARO, ventana_emergente.get_rect(), 3)

    lineas = texto.split('\n')
    y_offset = 20
    for i, linea in enumerate(lineas):
        texto_render = fuente_emergente.render(linea, True, BLANCO)
        ventana_emergente.blit(texto_render, (20, y_offset + i * 20))
        if y_offset + i * 20 > alto_emergente - 40: # Evitar que el texto se salga
            break

    boton_cerrar_rect = pygame.Rect(ancho_emergente // 2 - 50, alto_emergente - 40, 100, 30)
    pygame.draw.rect(ventana_emergente, ROJO_ERROR, boton_cerrar_rect)
    texto_cerrar = fuente_emergente.render("Cerrar", True, BLANCO)
    texto_rect = texto_cerrar.get_rect(center=boton_cerrar_rect.center)
    ventana_emergente.blit(texto_cerrar, texto_rect)

    # Posicionar la ventana emergente en la parte derecha, sin tapar la izquierda
    x_emergente = 100  # Ajusta la posición X según lo necesites
    y_emergente = alto_principal // 2 - alto_emergente // 2
    pantalla_principal.blit(ventana_emergente, (x_emergente, y_emergente))
    pygame.display.flip()

    esperando_cerrar = True
    while esperando_cerrar:
        for evento_emergente in pygame.event.get():
            if evento_emergente.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento_emergente.type == pygame.MOUSEBUTTONDOWN:
                x_e, y_e = evento_emergente.pos
                rect_cerrar_absoluto = pygame.Rect(x_emergente + boton_cerrar_rect.x, y_emergente + boton_cerrar_rect.y, boton_cerrar_rect.width, boton_cerrar_rect.height)
                if rect_cerrar_absoluto.collidepoint(x_e, y_e):
                    esperando_cerrar = False
    return True

# Archivos y algoritmos disponibles
archivos = [f for f in os.listdir("Smart-drone/maps") if f.endswith(".txt")]
algoritmos_no_informados = [
    ("AMPLITUD", "Amplitud"),
    ("COSTO_UNIFORME", "Costo Uniforme"),
    ("PROFUNDIDAD", "Profundidad")
]
algoritmos_informados = [
    ("AVARA", "Avara"),
    ("A_ESTRELLA", "A*")
]

# Variables de estado
archivo_seleccionado = archivos[0] if archivos else ""
clave_algoritmo = None
nombre_algoritmo = ""
mostrar_lista_mapas = False
mostrar_no_informados = False
mostrar_informados = False
boton_ejecutar_activo = False
mapa_cargado = False
mostrar_info = False
texto_info = ""
busqueda_completada = False  # Nuevo estado para controlar cuando la búsqueda ha terminado
mostrar_resultado = False # Nuevo estado para mostrar la ventana emergente al finalizar
scroll_mapas_offset = 0
scroll_no_informados_offset = 0
scroll_informados_offset = 0
arrastrando_scroll_mapas = False
scroll_click_y = 0

# Posiciones y entorno
mundo = []
pos_inicial = None
pos_paquetes = []
camino = []
rastros = []
pos_dron = None

# Animación
index_frame = 0
animar = False
ejecutando = True

# Rectángulos de la interfaz - Ajustados para la nueva ventana más grande
rect_seleccionar_mapa = pygame.Rect(750, 50, 300, 30)
lista_mapas_altura_visible = 2 * 30  # Mostrar solo 2 elementos
rect_lista_mapas_visible = pygame.Rect(750, 80, 300, lista_mapas_altura_visible)
boton_cargar_mapa_rect = pygame.Rect(750, rect_lista_mapas_visible.bottom + 10, 300, 40)
rect_seleccionar_algoritmo = pygame.Rect(750, boton_cargar_mapa_rect.bottom + 35, 300, 30)
altura_no_informados = len(algoritmos_no_informados) * 30
rect_no_informados_visible = pygame.Rect(750, rect_seleccionar_algoritmo.bottom + 10, 300, altura_no_informados)
rect_seleccionar_algoritmo_informado = pygame.Rect(750, rect_no_informados_visible.bottom + 15, 300, 30)
altura_informados = len(algoritmos_informados) * 30
rect_informados_visible = pygame.Rect(750, rect_seleccionar_algoritmo_informado.bottom + 10, 300, altura_informados)
boton_rect = pygame.Rect(750, 550, 300, 50)  # Movido más abajo

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos

            # Mostrar/ocultar lista de mapas y activar arrastre
            if rect_seleccionar_mapa.collidepoint(x, y):
                mostrar_lista_mapas = not mostrar_lista_mapas
                mostrar_no_informados = False
                mostrar_informados = False
                arrastrando_scroll_mapas = False
            elif mostrar_lista_mapas and rect_lista_mapas_visible.collidepoint(x, y):
                # Verificar si se hizo clic en un elemento de la lista para seleccionar
                indice_seleccionado = (y - rect_lista_mapas_visible.y + scroll_mapas_offset) // 30
                if 0 <= indice_seleccionado < len(archivos):
                    archivo_seleccionado = archivos[indice_seleccionado]
                    # mostrar_lista_mapas = False # Se mantiene visible hasta otra acción
                else:
                    # Si el clic no fue en un elemento, iniciar el arrastre
                    arrastrando_scroll_mapas = True
                    scroll_click_y = y

            # Botón de cargar mapa (siempre activo)
            if boton_cargar_mapa_rect.collidepoint(x, y):
                try:
                    mundo = cargar_mapa(archivo_seleccionado)
                    pos_inicial, pos_paquetes = buscar_posiciones(mundo)
                    pos_dron = pos_inicial
                    camino = []
                    rastros = []
                    animar = False
                    mapa_cargado = True
                    busqueda_completada = False
                    mostrar_resultado = False
                    clave_algoritmo = None
                    nombre_algoritmo = ""
                    texto_info = f"Mapa cargado: {archivo_seleccionado}\nTamaño: {len(mundo)}x{len(mundo[0])}\nPaquetes: {len(pos_paquetes)}"
                    # mostrar_ventana_emergente(texto_info) # Ya no se muestra al cargar
                    mostrar_info = True
                    mostrar_lista_mapas = False # Ocultar al cargar
                    boton_ejecutar_activo = mapa_cargado and clave_algoritmo
                except Exception as e:
                    texto_info = f"Error al cargar mapa:\n{str(e)}"
                    # mostrar_ventana_emergente(texto_info) # Ya no se muestra al error de carga
                    mostrar_info = True
                    mostrar_lista_mapas = False # Ocultar en caso de error
                    boton_ejecutar_activo = False

            # Mostrar/ocultar algoritmos no informados
            if rect_seleccionar_algoritmo.collidepoint(x, y):
                mostrar_no_informados = not mostrar_no_informados
                mostrar_informados = False
                mostrar_lista_mapas = False
                arrastrando_scroll_mapas = False

            # Seleccionar algoritmo no informado
            if mostrar_no_informados and rect_no_informados_visible.collidepoint(x, y):
                indice_seleccionado = (y - rect_no_informados_visible.y) // 30
                if 0 <= indice_seleccionado < len(algoritmos_no_informados):
                    clave_algoritmo, nombre_algoritmo = algoritmos_no_informados[indice_seleccionado]
                    mostrar_no_informados = False
                    texto_info = f"Algoritmo seleccionado:\n{nombre_algoritmo}\n(Tipo: No informado)"
                    # mostrar_ventana_emergente(texto_info) # Ya no se muestra al seleccionar algoritmo
                    mostrar_info = True
                    boton_ejecutar_activo = mapa_cargado and clave_algoritmo
                    arrastrando_scroll_mapas = False

            # Mostrar/ocultar algoritmos informados
            if rect_seleccionar_algoritmo_informado.collidepoint(x, y):
                mostrar_informados = not mostrar_informados
                mostrar_no_informados = False
                mostrar_lista_mapas = False
                arrastrando_scroll_mapas = False

            # Seleccionar algoritmo informado
            if mostrar_informados and rect_informados_visible.collidepoint(x, y):
                indice_seleccionado = (y - rect_informados_visible.y) // 30
                if 0 <= indice_seleccionado < len(algoritmos_informados):
                    clave_algoritmo, nombre_algoritmo = algoritmos_informados[indice_seleccionado]
                    mostrar_informados = False
                    texto_info = f"Algoritmo seleccionado:\n{nombre_algoritmo}\n(Tipo: Informado)"
                    # mostrar_ventana_emergente(texto_info) # Ya no se muestra al seleccionar algoritmo
                    mostrar_info = True
                    boton_ejecutar_activo = mapa_cargado and clave_algoritmo
                    arrastrando_scroll_mapas = False

            # Botón de búsqueda
            if boton_rect.collidepoint(evento.pos) and boton_ejecutar_activo and not animar and mapa_cargado and clave_algoritmo:
                try:
                    if clave_algoritmo == "AMPLITUD":
                        resultado = amplitud(mundo, len(mundo), len(mundo[0]), pos_paquetes, pos_inicial)
                        if resultado[0]:  # Se encontró un camino
                            camino = resultado[0]
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_solucion = resultado[3]
                            texto_info = f"Búsqueda por amplitud\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad de la solución: {profundidad_solucion}\n"
                        else:
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_maxima = resultado[3]
                            texto_info = f"Búsqueda por amplitud\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad máxima alcanzada: {profundidad_maxima}\n" \
                                        f"No se encontró solución."
                        mostrar_resultado = True
                        mostrar_info = True
                    elif clave_algoritmo == "PROFUNDIDAD":
                        resultado = profundidad(mundo, len(mundo), len(mundo[0]), pos_paquetes, pos_inicial)
                        print(resultado)

                        if resultado[0]:  # Se encontró un camino
                            camino = resultado[0]
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_solucion = resultado[3]
                            texto_info = f"Búsqueda por profundidad\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad de la solución: {profundidad_solucion}\n"
                        else:
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_maxima = resultado[3]
                            texto_info = f"Búsqueda por profundidad\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad máxima alcanzada: {profundidad_maxima}\n" \
                                        f"No se encontró solución."
                        mostrar_resultado = True
                        mostrar_info = True
                    elif clave_algoritmo == "COSTO_UNIFORME":
                        resultado = costoUniforme(mundo, len(mundo), len(mundo[0]), pos_paquetes, pos_inicial)
                        print(resultado)

                        if resultado[0]:  # Se encontró un camino
                            camino = resultado[0]
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_solucion = resultado[3]
                            costo_total = resultado[4]
                            texto_info = f"Búsqueda por costo uniforme\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad de la solución: {profundidad_solucion}\n" \
                                        f"Costo total: {costo_total}\n"
                        else:
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_maxima = resultado[3]
                            texto_info = f"Búsqueda por costo uniforme\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad máxima alcanzada: {profundidad_maxima}\n" \
                                        f"No se encontró solución."
                        mostrar_resultado = True
                        mostrar_info = True
                    elif clave_algoritmo == "AVARA":
                        resultado = avara(mundo, len(mundo), len(mundo[0]), pos_paquetes, pos_inicial)
                        print(resultado)

                        if resultado[0]:  # Se encontró un camino
                            camino = resultado[0]
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_solucion = resultado[3]
                            costo_total = resultado[4]
                            texto_info = f"Búsqueda por Avara\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad de la solución: {profundidad_solucion}\n" \
                                        f"Costo total: {costo_total}\n"
                        else:
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_maxima = resultado[3]
                            texto_info = f"Búsqueda por Avara\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad máxima alcanzada: {profundidad_maxima}\n" \
                                        f"No se encontró solución."
                        ## texto_info = "Algoritmo Avara seleccionado (sin implementar)."
                        mostrar_resultado = True
                        mostrar_info = True
                    elif clave_algoritmo == "A_ESTRELLA":
                        resultado = aStar(mundo, len(mundo), len(mundo[0]), pos_paquetes, pos_inicial)
                        print(pos_paquetes)
                        print(pos_inicial)
                        print(resultado)

                        if resultado[0]:  # Se encontró un camino
                            camino = resultado[0]
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_solucion = resultado[3]
                            costo_total = resultado[4]
                            texto_info = f"Búsqueda por A*\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad de la solución: {profundidad_solucion}\n" \
                                        f"Costo total: {costo_total}\n"
                        else:
                            tiempo_ejecucion = resultado[1]
                            nodos_expandidos_count = resultado[2]
                            profundidad_maxima = resultado[3]
                            texto_info = f"Búsqueda por A*\n" \
                                        f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos\n" \
                                        f"Nodos expandidos: {nodos_expandidos_count}\n" \
                                        f"Profundidad máxima alcanzada: {profundidad_maxima}\n" \
                                        f"No se encontró solución."
                        mostrar_resultado = True
                        mostrar_info = True

                    if camino and clave_algoritmo in ["AMPLITUD", "PROFUNDIDAD", "COSTO_UNIFORME"]:
                        animar = True
                        pos_dron = pos_inicial
                        rastros = []
                        boton_ejecutar_activo = False
                        busqueda_completada = False
                        mostrar_resultado = False
                        mostrar_info = True
                        mostrar_lista_mapas = False # Ocultar al iniciar búsqueda
                        arrastrando_scroll_mapas = False
                    elif camino is None and clave_algoritmo in ["AMPLITUD", "PROFUNDIDAD", "COSTO_UNIFORME"]:
                        texto_info = "No se encontró solución\npara este problema."
                        mostrar_resultado = True # Mostrar ventana al finalizar (sin solución)
                        mostrar_info = True
                        busqueda_completada = True
                        mostrar_lista_mapas = False # Ocultar si no hay solución
                        arrastrando_scroll_mapas = False
                except Exception as e:
                    texto_info = f"Error en el algoritmo:\n{str(e)}"
                    mostrar_resultado = True # Mostrar ventana en caso de error
                    mostrar_info = True
                    mostrar_lista_mapas = False # Ocultar en caso de error
                    arrastrando_scroll_mapas = False

        elif evento.type == pygame.MOUSEBUTTONUP:
            arrastrando_scroll_mapas = False

        elif evento.type == pygame.MOUSEMOTION:
            if arrastrando_scroll_mapas:
                dy = evento.y - scroll_click_y
                scroll_mapas_offset = max(0, min(scroll_mapas_offset - dy, len(archivos) * 30 - rect_lista_mapas_visible.height))
                scroll_click_y = evento.y

        elif evento.type == pygame.MOUSEWHEEL:
            if mostrar_lista_mapas:
                scroll_mapas_offset = max(0, min(scroll_mapas_offset - evento.y * 30, len(archivos) * 30 - rect_lista_mapas_visible.height))
            elif mostrar_no_informados:
                pass # Deshabilitar scroll para no informados
            elif mostrar_informados:
                pass # Deshabilitar scroll para informados

    # Dibujar fondo negro para todo excepto el área del mapa
    pantalla_principal.fill(NEGRO)

    # Calcular el área del mapa
    mapa_ancho = len(mundo[0]) * celdaTamano if mundo else 0
    mapa_alto = len(mundo) * celdaTamano if mundo else 0
    offset_x = (700 - mapa_ancho) // 2 if mapa_ancho < 700 else 0
    offset_y = (alto_principal - mapa_alto) // 2 if mapa_alto < alto_principal else 0
    mapa_rect = pygame.Rect(offset_x, offset_y, mapa_ancho, mapa_alto)

    # Dibujar el fondo blanco solo en el área del mapa
    pygame.draw.rect(pantalla_principal, BLANCO, mapa_rect)

    # Dibujar mapa
    if mundo:
        for fila in range(len(mundo)):
            for columna in range(len(mundo[fila])):
                x, y = columna * celdaTamano + offset_x, fila * celdaTamano + offset_y
                if pos_dron and (fila, columna) == pos_dron and mundo[fila][columna] == 4:
                    mundo[fila][columna] = 0
                if mundo[fila][columna] == 1:
                    pantalla_principal.blit(img_valla, (x, y))
                elif mundo[fila][columna] == 3:
                    pantalla_principal.blit(img_campo, (x, y))
                elif mundo[fila][columna] == 4:
                    pantalla_principal.blit(img_caja, (x, y))
                else:
                    pantalla_principal.blit(img_piso, (x, y))

        # Rastros
        for fila, columna in rastros:
            x, y = columna * celdaTamano + offset_x, fila * celdaTamano + offset_y
            rastro = pygame.Surface((celdaTamano, celdaTamano))
            rastro.set_alpha(100)
            rastro.fill((0, 150, 255))
            pantalla_principal.blit(rastro, (x, y))

        # Animación del dron
        if animar and camino:
            pos_dron = camino.pop(0)
            rastros.append(pos_dron)
        elif animar and not camino:
            if pos_dron not in rastros:
                rastros.append(pos_dron)
            animar = False
            busqueda_completada = True
            mostrar_resultado = True # Mostrar ventana al finalizar la animación
            mostrar_info = True

        # Dibujar dron
        if pos_dron:
            x = pos_dron[1] * celdaTamano + offset_x
            y = pos_dron[0] * celdaTamano + offset_y
            pantalla_principal.blit(frames[index_frame], (x, y))
            index_frame = (index_frame + 1) % len(frames)

    # Panel lateral derecho (fondo negro)
    pygame.draw.rect(pantalla_principal, GRIS_OSCURO, (700, 0, 400, alto_principal))

    # Mostrar arriba el texto de referencia (opcional)
    pantalla_principal.blit(fuente.render("Mapa seleccionado:", True, BLANCO), (750, 20))

    # Dibujar botón con el nombre del archivo seleccionado
    texto_boton_mapa = archivo_seleccionado if archivo_seleccionado else "Seleccionar mapa"
    pygame.draw.rect(pantalla_principal, GRIS_MEDIO, rect_seleccionar_mapa, 0)
    pantalla_principal.blit(fuente.render(texto_boton_mapa, True, BLANCO), (rect_seleccionar_mapa.x + 5, rect_seleccionar_mapa.y + 2))

    # Lista de mapas con scroll manual y persistencia
    if mostrar_lista_mapas:
        pygame.draw.rect(pantalla_principal, GRIS_CLARO, rect_lista_mapas_visible)
        for i, archivo in enumerate(archivos):
            if 0 <= i * 30 - scroll_mapas_offset < rect_lista_mapas_visible.height:
                y_pos = rect_lista_mapas_visible.top + (i * 30 - scroll_mapas_offset)
                texto_archivo = archivo if len(archivo) <= 30 else archivo[:27] + "..."
                texto_render = fuente_pequena.render(texto_archivo, True, BLANCO)
                rect_archivo = pygame.Rect(rect_lista_mapas_visible.x, y_pos, rect_lista_mapas_visible.width, 30)
                color_fondo = (90, 90, 90) if rect_archivo.collidepoint(pygame.mouse.get_pos()) else GRIS_CLARO
                pygame.draw.rect(pantalla_principal, color_fondo, rect_archivo)
                pantalla_principal.blit(texto_render, (rect_lista_mapas_visible.x + 5, y_pos + 5))

    # Botón de cargar mapa (siempre activo)
    pygame.draw.rect(pantalla_principal, AZUL_BOTON, boton_cargar_mapa_rect)
    pantalla_principal.blit(fuente.render("Cargar mapa", True, NEGRO), (760, boton_cargar_mapa_rect.y + 5))

    # Sección de selección de algoritmo no informado
    pygame.draw.rect(pantalla_principal, GRIS_MEDIO, rect_seleccionar_algoritmo, 2)
    texto_algoritmo_no_informado = nombre_algoritmo if nombre_algoritmo and clave_algoritmo in [alg[0] for alg in algoritmos_no_informados] else "Seleccione"
    pantalla_principal.blit(fuente.render(texto_algoritmo_no_informado, True, BLANCO), (755, rect_seleccionar_algoritmo.y + 2))
    pantalla_principal.blit(fuente.render("Algoritmo No Informado:", True, BLANCO), (755, rect_seleccionar_algoritmo.top - 25))

    # Lista de algoritmos no informados
    if mostrar_no_informados:
        pygame.draw.rect(pantalla_principal, (70, 70, 90), rect_no_informados_visible)
        y_offset = -10+ rect_no_informados_visible.top
        for i, (clave, nombre) in enumerate(algoritmos_no_informados):
            rect_opcion = pygame.Rect(rect_no_informados_visible.x, y_offset + i * 30, rect_no_informados_visible.width, 30)
            color = (100, 100, 120) if rect_opcion.collidepoint(pygame.mouse.get_pos()) else (70, 70, 90)
            pygame.draw.rect(pantalla_principal, color, rect_opcion)
            pantalla_principal.blit(fuente.render(nombre, True, BLANCO), (rect_opcion.x + 5, rect_opcion.y + 5))

    # Sección para mostrar/ocultar algoritmos informados
    pygame.draw.rect(pantalla_principal, GRIS_MEDIO, rect_seleccionar_algoritmo_informado, 2)
    texto_informados_boton = nombre_algoritmo if nombre_algoritmo and clave_algoritmo in [alg[0] for alg in algoritmos_informados] else "Seleccione"
    pantalla_principal.blit(fuente_pequena.render(texto_informados_boton, True, BLANCO), (755, rect_seleccionar_algoritmo_informado.y + 5))
    pantalla_principal.blit(fuente.render("Algoritmo Informado:", True, BLANCO), (755, rect_seleccionar_algoritmo_informado.top - 25))

    if rect_seleccionar_algoritmo_informado.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        mostrar_informados = not mostrar_informados
        mostrar_no_informados = False
        mostrar_lista_mapas = False
        arrastrando_scroll_mapas = False

    # Lista de algoritmos informados
    if mostrar_informados:
        pygame.draw.rect(pantalla_principal, (90, 70, 70), rect_informados_visible)
        y_offset = rect_informados_visible.top
        for i, (clave, nombre) in enumerate(algoritmos_informados):
            rect_opcion = pygame.Rect(rect_informados_visible.x, y_offset + i * 30, rect_informados_visible.width, 30)
            color = (120, 100, 100) if rect_opcion.collidepoint(pygame.mouse.get_pos()) else (90, 70, 70)
            pygame.draw.rect(pantalla_principal, color, rect_opcion)
            pantalla_principal.blit(fuente.render(nombre, True, BLANCO), (rect_opcion.x + 5, rect_opcion.y + 5))

    # Botón de búsqueda - Activo solo si mapa cargado y algoritmo seleccionado
    boton_ejecutar_activo = mapa_cargado and clave_algoritmo and not busqueda_completada and not animar
    color_boton = (150, 150, 150) if not boton_ejecutar_activo else AZUL_BOTON
    pygame.draw.rect(pantalla_principal, color_boton, boton_rect)
    texto_boton = "Ejecutar búsqueda" if boton_ejecutar_activo else "Ejecutar búsqueda" if not busqueda_completada else "Búsqueda completada"
    pantalla_principal.blit(fuente.render(texto_boton, True, NEGRO), (760, boton_rect.y + 10))

    if mostrar_resultado:
        if mostrar_ventana_emergente(texto_info):
            mostrar_resultado = False

    pygame.display.flip()
    clock.tick(5)

pygame.quit()