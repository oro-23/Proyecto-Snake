import pygame
import sys
import random

# --- Inicialización de Pygame ---
pygame.init()

# --- Configuración de la Pantalla ---
ancho_pantalla = 800
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Juego de la Serpiente con Menú")

# --- Colores ---
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# --- Reloj (para controlar los FPS) ---
reloj = pygame.time.Clock()
velocidad_serpiente = 15

# --- Fuentes ---
fuente_menu = pygame.font.SysFont('calibri', 50)
fuente_puntuacion = pygame.font.SysFont('calibri', 35)

def mostrar_texto(texto, fuente, color, superficie, x, y):
    """
    Función para renderizar y mostrar texto en la pantalla.
    """
    objeto_texto = fuente.render(texto, True, color)
    rectangulo_texto = objeto_texto.get_rect()
    rectangulo_texto.center = (x, y)
    superficie.blit(objeto_texto, rectangulo_texto)

def menu_principal():
    """
    Función para mostrar el menú principal.
    """
    while True:
        pantalla.fill(azul)
        mostrar_texto('Juego de la Serpiente', fuente_menu, blanco, pantalla, ancho_pantalla / 2, alto_pantalla / 4)

        mx, my = pygame.mouse.get_pos()

        boton_iniciar = pygame.Rect(ancho_pantalla / 2 - 150, alto_pantalla / 2 - 50, 300, 70)
        boton_salir = pygame.Rect(ancho_pantalla / 2 - 150, alto_pantalla / 2 + 50, 300, 70)

        if boton_iniciar.collidepoint((mx, my)):
            pygame.draw.rect(pantalla, verde, boton_iniciar)
        else:
            pygame.draw.rect(pantalla, rojo, boton_iniciar)

        if boton_salir.collidepoint((mx, my)):
            pygame.draw.rect(pantalla, verde, boton_salir)
        else:
            pygame.draw.rect(pantalla, rojo, boton_salir)

        mostrar_texto('Iniciar Juego', fuente_puntuacion, blanco, pantalla, ancho_pantalla / 2, alto_pantalla / 2 - 15)
        mostrar_texto('Salir', fuente_puntuacion, blanco, pantalla, ancho_pantalla / 2, alto_pantalla / 2 + 85)


        click = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    click = True

        if boton_iniciar.collidepoint((mx, my)):
            if click:
                juego()
        if boton_salir.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        reloj.tick(15)

def juego():
    """
    Función principal del juego.
    """
    game_over = False

    x1 = ancho_pantalla / 2
    y1 = alto_pantalla / 2

    x1_cambio = 0
    y1_cambio = 0

    cuerpo_serpiente = []
    longitud_serpiente = 1
    
    velocidad_actual = velocidad_serpiente

    comida_x = round(random.randrange(0, ancho_pantalla - 20) / 20.0) * 20.0
    comida_y = round(random.randrange(0, alto_pantalla - 20) / 20.0) * 20.0

    while not game_over:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_cambio = -20
                    y1_cambio = 0
                elif evento.key == pygame.K_RIGHT:
                    x1_cambio = 20
                    y1_cambio = 0
                elif evento.key == pygame.K_UP:
                    y1_cambio = -20
                    x1_cambio = 0
                elif evento.key == pygame.K_DOWN:
                    y1_cambio = 20
                    x1_cambio = 0

        if x1 >= ancho_pantalla or x1 < 0 or y1 >= alto_pantalla or y1 < 0:
            game_over = True
        x1 += x1_cambio
        y1 += y1_cambio
        pantalla.fill(azul)
        pygame.draw.rect(pantalla, rojo, [comida_x, comida_y, 20, 20])
        cabeza_serpiente = []
        cabeza_serpiente.append(x1)
        cabeza_serpiente.append(y1)
        cuerpo_serpiente.append(cabeza_serpiente)
        if len(cuerpo_serpiente) > longitud_serpiente:
            del cuerpo_serpiente[0]

        for x in cuerpo_serpiente[:-1]:
            if x == cabeza_serpiente:
                game_over = True

        for segmento in cuerpo_serpiente:
            pygame.draw.rect(pantalla, verde, [segmento[0], segmento[1], 20, 20])
        
        mostrar_texto("Puntuación: " + str(longitud_serpiente - 1), fuente_puntuacion, blanco, pantalla, 100, 30)

        pygame.display.update()

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, ancho_pantalla - 20) / 20.0) * 20.0
            comida_y = round(random.randrange(0, alto_pantalla - 20) / 20.0) * 20.0
            longitud_serpiente += 1
            # Aumentar la velocidad cada 5 puntos
            if (longitud_serpiente -1) % 5 == 0:
                velocidad_actual += 1


        reloj.tick(velocidad_actual)

    pantalla.fill(negro)
    mostrar_texto("¡Perdiste! Presiona C para jugar de nuevo o Q para salir", fuente_puntuacion, rojo, pantalla, ancho_pantalla/2, alto_pantalla/2)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_c:
                    juego()


# --- Iniciar el Menú Principal ---
menu_principal()