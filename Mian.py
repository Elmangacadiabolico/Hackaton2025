import pygame
import random
import sys
import os


pygame.init()


ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Guardian del Aire")


BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE_LIMA = (50, 205, 50)
AZUL = (0, 100, 255)
GRIS = (200, 200, 200)


fuente = pygame.font.Font(None, 40)
fuente_titulo = pygame.font.Font(None, 70)


def cargar_imagen(nombre, ancho, alto):
    try:
        assets_path = os.path.join(os.path.dirname(__file__), 'assets', 'img')
        img = pygame.image.load(os.path.join(assets_path, nombre)).convert_alpha()
        return pygame.transform.scale(img, (ancho, alto))
    except:
        return None


jugador_img = cargar_imagen("Jugador.png", 60, 60)
objeto_bueno_img = cargar_imagen("ObjetoBueno.png", 40, 40)
objeto_malo_img = cargar_imagen("ObjetoMalo.png", 40, 40)
fondo_img = cargar_imagen("fondo.png", ANCHO, ALTO)


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = jugador_img if jugador_img else pygame.Surface((60, 60))
        if not jugador_img:
            self.image.fill(ROJO)
        self.rect = self.image.get_rect(midbottom=(ANCHO // 2, ALTO - 10))
        self.velocidad = 8

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad


class Objeto(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo 
        if tipo == "bueno":
            self.image = objeto_bueno_img if objeto_bueno_img else pygame.Surface((40, 40))
            if not objeto_bueno_img:
                self.image.fill(VERDE_LIMA)
        else:
            self.image = objeto_malo_img if objeto_malo_img else pygame.Surface((40, 40))
            if not objeto_malo_img:
                self.image.fill(ROJO)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocidad = random.randint(4, 7)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()


def dibujar_texto(texto, fuente, color, superficie, x, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y))
    superficie.blit(render, rect)


def menu_principal():
    while True:
        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            pantalla.fill(GRIS)

        dibujar_texto("Guardian del Aire", fuente_titulo, AZUL, pantalla, ANCHO//2, 150)
        dibujar_texto("1. Jugar", fuente, NEGRO, pantalla, ANCHO//2, 300)
        dibujar_texto("2. Instrucciones", fuente, NEGRO, pantalla, ANCHO//2, 360)
        dibujar_texto("3. Salir", fuente, NEGRO, pantalla, ANCHO//2, 420)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    juego()
                elif event.key == pygame.K_2:
                    instrucciones()
                elif event.key == pygame.K_3:
                    pygame.quit(); sys.exit()


def instrucciones():
    esperando = True
    while esperando:
        pantalla.fill(BLANCO)
        dibujar_texto("🧤 Instrucciones 🧤", fuente_titulo, AZUL, pantalla, ANCHO//2, 100)
        dibujar_texto("Mueve al jugador con las flechas ← →", fuente, NEGRO, pantalla, ANCHO//2, 200)
        dibujar_texto("Atrapa objetos buenos: guantes, casco, planta, etc.", fuente, VERDE_LIMA, pantalla, ANCHO//2, 260)
        dibujar_texto("Evita objetos malos: CO₂, NOx, monolito caliente, etc.", fuente, ROJO, pantalla, ANCHO//2, 320)
        dibujar_texto("Tenés 60 segundos. Si tocás algo malo, perdés.", fuente, NEGRO, pantalla, ANCHO//2, 380)
        dibujar_texto("Presioná ESPACIO para volver al menú", fuente, NEGRO, pantalla, ANCHO//2, 500)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                esperando = False


def juego():
    jugador = Jugador()
    todos = pygame.sprite.Group()
    objetos = pygame.sprite.Group()
    todos.add(jugador)

    clock = pygame.time.Clock()
    score = 0
    tiempo_inicio = pygame.time.get_ticks()
    duracion = 60000 
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

       
        if random.randint(1, 25) == 1:
            tipo = "malo" if random.random() < 0.3 else "bueno" 
            objeto = Objeto(tipo)
            objetos.add(objeto)
            todos.add(objeto)

        todos.update()

     
        colisiones = pygame.sprite.spritecollide(jugador, objetos, True)
        for obj in colisiones:
            if obj.tipo == "bueno":
                score += 1
            else:
                game_over = True

        tiempo_restante = max(0, duracion - (pygame.time.get_ticks() - tiempo_inicio))
        segundos = tiempo_restante // 1000

        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            pantalla.fill(BLANCO)

        todos.draw(pantalla)

        texto_score = fuente.render(f"Puntos: {score}", True, NEGRO)
        pantalla.blit(texto_score, (10, 10))

        texto_tiempo = fuente.render(f"Tiempo: {segundos}", True, NEGRO)
        pantalla.blit(texto_tiempo, (ANCHO - 200, 10))

        pygame.display.flip()
        clock.tick(60)

       
        if tiempo_restante <= 0:
            game_over = True

    pantalla.fill(BLANCO)
    if tiempo_restante <= 0:
        mensaje = "¡Tiempo terminado!"
    else:
        mensaje = "¡Perdiste! Tocaste algo peligroso 😵"
    dibujar_texto(mensaje, fuente_titulo, ROJO, pantalla, ANCHO//2, 250)
    dibujar_texto(f"Puntaje final: {score}", fuente, NEGRO, pantalla, ANCHO//2, 320)
    dibujar_texto("Presioná ESPACIO para volver al menú", fuente, NEGRO, pantalla, ANCHO//2, 400)
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                esperando = False

# Iniciar
if __name__ == "__main__":
    menu_principal()
