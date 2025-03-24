import pygame
from PIL import Image, ImageSequence

pygame.init()

ANCHO, ALTO = 500, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Animación del Dron")

# Cargar imágenes

dron_gif = "assets/dron-moving.gif"
valla_img = pygame.image.load("assets/valla.png")
box_img = pygame.image.load("assets/box.png")

# Cargar el GIF con PIL
imagen_gif = Image.open(dron_gif)


# Extraemos los frames del GIF
frames = []
for frame in ImageSequence.Iterator(imagen_gif):
    frame = frame.convert("RGBA")  # Convertir para evitar problemas
    modo, datos = frame.mode, frame.tobytes()
    img_pygame = pygame.image.fromstring(datos, frame.size, modo)
    frames.append(img_pygame)

# Variables de animación
index_frame = 0
clock = pygame.time.Clock()

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Limpiar pantalla
    pantalla.fill((255, 255, 255))  # Fondo blanco

    # Dibujar el frame actual del GIF
    pantalla.blit(frames[index_frame], (ANCHO // 2 - frames[0].get_width() // 2, ALTO // 2 - frames[0].get_height() // 2))

    # Cambiar de frame
    index_frame = (index_frame + 1) % len(frames)
    # Dibujar la valla en (100, 200)
    pantalla.blit(valla_img, (100, 200))

    # Dibujar la caja en (300, 400)
    pantalla.blit(box_img, (300, 400))

    pygame.display.update()
    clock.tick(10)  # Control de velocidad (FPS)

pygame.quit()
