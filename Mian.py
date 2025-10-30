import pygame
import random
import sys
import os

def main():

    # Inicializa pygame
    pygame.init()

    # --- Configuración de la Pantalla ---
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Captura el Objeto")

    # --- Colores ---
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    ROJO = (255, 0, 0)
    AZUL = (0, 0, 255)
    VERDE_LIMA = (50, 205, 50)

    # --- Carga de Imágenes (Opcional) ---
    try:
        assets_path = os.path.join(os.path.dirname(__file__), 'assets', 'img')
        
        fondo_img = pygame.image.load(os.path.join(assets_path,'fondo.png')).convert()
        fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))
    except (pygame.error, FileNotFoundError):
        fondo_img = None

    try:
        assets_path = os.path.join(os.path.dirname(__file__), 'assets', 'img')
        jugador_img = pygame.image.load(os.path.join(assets_path, 'Jugador.png')).convert_alpha()
        jugador_img = pygame.transform.scale(jugador_img, (50, 60)) # Redimensionar la imagen del jugador
    except (pygame.error, FileNotFoundError):
        jugador_img = None

    try:
        assets_path = os.path.join(os.path.dirname(__file__), 'assets', 'img')
        objeto_img = pygame.image.load(os.path.join(assets_path, 'Objeto.jpg')).convert_alpha()
        objeto_img = pygame.transform.scale(objeto_img, (30, 30)) # Redimensionar la imagen del objeto
    except (pygame.error, FileNotFoundError):
        objeto_img = None

    # --- Jugador ---
    jugador_ancho, jugador_alto = 50, 50
    if jugador_img:
        jugador_ancho, jugador_alto = jugador_img.get_size()
    jugador_rect = pygame.Rect(ANCHO // 2 - jugador_ancho // 2, ALTO - jugador_alto - 10, jugador_ancho, jugador_alto)
    jugador_color = ROJO
    jugador_velocidad = 7

    objeto_ancho, objeto_alto = 30, 30
    if objeto_img:
        objeto_ancho, objeto_alto = objeto_img.get_size()
    objeto_rect = pygame.Rect(random.randint(0, ANCHO - objeto_ancho), 0, objeto_ancho, objeto_alto)
    objeto_velocidad = 5

    score = 0

    fuente = pygame.font.Font(None, 36)


    animacion_captura_contador = 0

    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
                
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_rect.left > 0:
            jugador_rect.x -= jugador_velocidad
        if teclas[pygame.K_RIGHT] and jugador_rect.right < ANCHO:
            jugador_rect.x += jugador_velocidad
        if teclas[pygame.K_UP] and jugador_rect.top > 0:
            jugador_rect.y -= jugador_velocidad
        if teclas[pygame.K_DOWN] and jugador_rect.bottom < ALTO:
            jugador_rect.y += jugador_velocidad


        objeto_rect.y += objeto_velocidad
        if objeto_rect.top > ALTO:
            objeto_rect.y = -objeto_alto
            objeto_rect.x = random.randint(0, ANCHO - objeto_ancho)


        if jugador_rect.colliderect(objeto_rect):
            score += 1 # Aumentar puntuación
            jugador_color = VERDE_LIMA
            animacion_captura_contador = 10
            objeto_rect.y = -objeto_alto
            objeto_rect.x = random.randint(0, ANCHO - objeto_ancho)

        # --- Manejo de la Animación ---
        if animacion_captura_contador > 0:
            animacion_captura_contador -= 1
        else:
            jugador_color = ROJO

        # --- Dibujado en Pantalla ---
        # Fondo
        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            pantalla.fill(BLANCO)

        # Jugador
        if jugador_img:
            pantalla.blit(jugador_img, jugador_rect.topleft)
        else:
            # Solo dibuja el rectángulo con color si no hay imagen
            pygame.draw.rect(pantalla, jugador_color, jugador_rect)

        # Objeto
        if objeto_img:
            pantalla.blit(objeto_img, objeto_rect.topleft)
        else:
            pygame.draw.rect(pantalla, AZUL, objeto_rect)

        # Puntuación
        texto_score = fuente.render(f"Score: {score}", True, NEGRO)
        pantalla.blit(texto_score, (10, 10))

        # --- Actualizar la Pantalla ---
        pygame.display.flip()

        # --- Controlar FPS ---
        clock.tick(60)

    # --- Fin de Pygame ---
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()