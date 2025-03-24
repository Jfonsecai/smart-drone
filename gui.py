import pygame
from PIL import Image, ImageSequence

# Iniciamos el game
pygame.init()

ancho, alto = 600, 600
celdaTamano = 60

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Smart dron Packer")

# imagenes
img_valla = pygame.image.load("assets/valla.png")
img_caja = pygame.image.load("assets/box.png")
img_campo = pygame.image.load("assets/campo-magnetico.png")
img_piso = pygame.image.load("assets/piso.png")

#redimensionar
img_valla = pygame.transform.scale(img_valla, (celdaTamano, celdaTamano))
img_caja = pygame.transform.scale(img_caja, (celdaTamano, celdaTamano))
img_campo = pygame.transform.scale(img_campo, (celdaTamano, celdaTamano))
img_piso = pygame.transform.scale(img_piso, (celdaTamano, celdaTamano))


# Acomodamos animaciones
ruta_gif = "assets/dron-moving.gif"
imagen_gif = Image.open(ruta_gif)
frames = []
for frame in ImageSequence.Iterator(imagen_gif):
    frame = frame.convert("RGBA")
    modo, datos = frame.mode, frame.tobytes()
    img_pygame = pygame.image.fromstring(datos, frame.size, modo)
    img_pygame = pygame.transform.scale(img_pygame, (celdaTamano, celdaTamano))
    frames.append(img_pygame)

mundo = [
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 2, 0, 3, 4, 4, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [3, 3, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Buscar posicion inicial del dron
pos_dron = None
for i, fila in enumerate(mundo):
    for j, celda in enumerate(fila):
        if celda == 2:
            pos_dron = (i, j)  
            break

# Simulación de camino del dron
camino = [(2,1),(2,2),(1,2),(0,2), (0,3), (0,4),(1,4),(2,4),(2,5)]  

# Variables de animación
index_frame = 0
clock = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
# Fondo
    pantalla.fill((255, 255, 255)) 
    
    # Dibujar el mundo
    for fila in range(len(mundo)):
        for columna in range(len(mundo[fila])):
            x = columna * celdaTamano 
            y = fila * celdaTamano

            #Dron recoge paquete
            if (pos_dron) == (fila, columna) and mundo[fila][columna] == 4:
                mundo[fila][columna] = 0
            if mundo[fila][columna] == 1:  # Valla (pared)
                pantalla.blit(img_valla, (x, y))
            elif mundo[fila][columna] == 3:  # Campo magnético
                pantalla.blit(img_campo, (x, y))
            elif mundo[fila][columna] == 4: #Caja
                pantalla.blit(img_caja, (x, y))
            else: pantalla.blit(img_piso, (x,y)) #Piso

          

    # Mover el dron por el camino
    if camino:
        pos_dron = camino.pop(0)
        print("El dron esta en",pos_dron)  # Mover a la siguiente posición

    # Dibujar el dron animado
    x = pos_dron[1] * (celdaTamano -1)
    y = pos_dron[0] * (celdaTamano - 7)

    pantalla.blit(frames[index_frame], (x, y))
    index_frame = (index_frame + 1) % len(frames)  # Cambiar frame de animación

    pygame.display.update()
    clock.tick(2)  # Controlar velocidad

pygame.quit()
