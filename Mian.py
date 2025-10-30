import pygame
import random
import sys
import os


pygame.init()
pygame.mixer.init()


ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Guardián del Aire")


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
        ruta = os.path.join(os.path.dirname(__file__), 'assets', nombre)
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, (ancho, alto))
    except Exception as e:
        print(f" No se pudo cargar {nombre}: {e}")
        return None

jugador_img = cargar_imagen("jugador2.png", 70, 80)
fondo_img = cargar_imagen("fondo.jpg", ANCHO, ALTO)

imagenes_buenas = [
    "casco-removebg-preview.png",
    "gafas-removebg-preview.png",
    "casco.png",
    "planta.png",
    "descarga.jpg",
]
imagenes_malas = [
    "ch4-removebg-preview.png",
    "co2-removebg-preview.png",
    "n20-removebg-preview.png",
    "pfc-removebg-preview.png",
    "hump-removebg-preview.png"
]

objetos_buenos_imgs = [cargar_imagen(img, 40, 40) for img in imagenes_buenas]
objetos_malos_imgs = [cargar_imagen(img, 40, 40) for img in imagenes_malas]

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
            self.image = random.choice(objetos_buenos_imgs)
        else:
            self.image = random.choice(objetos_malos_imgs)
        
        if not self.image:
            self.image = pygame.Surface((40, 40))
            self.image.fill(VERDE_LIMA if tipo == "bueno" else ROJO)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocidad = random.randint(2, 4)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()


def dibujar_texto(texto, fuente, color, superficie, x, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y))
    superficie.blit(render, rect)


def menu_principal():
    pygame.mixer.music.stop()
    while True:
        if fondo_img:
            pantalla.blit(fondo_img, (0, 0))
        else:
            pantalla.fill(GRIS)

        dibujar_texto(" Guardián del Aire ", fuente_titulo, AZUL, pantalla, ANCHO//2, 150)
        dibujar_texto("1. Jugar", fuente, NEGRO, pantalla, ANCHO//2, 300)
        dibujar_texto("2. Instrucciones", fuente, NEGRO, pantalla, ANCHO//2, 360)
        dibujar_texto("3. Salir", fuente, NEGRO, pantalla, ANCHO//2, 420)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    try:
                        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets', 'Musica_1.mp3'))
                        pygame.mixer.music.play(-1)
                    except Exception as e:
                        print(f"No se pudo cargar la música: {e}")
                    juego()
                elif event.key == pygame.K_2:
                    instrucciones()
                elif event.key == pygame.K_3:
                    pygame.quit(); sys.exit()


def instrucciones():
    esperando = True
    while esperando:
        pantalla.fill(BLANCO)
        dibujar_texto(" Instrucciones ", fuente_titulo, AZUL, pantalla, ANCHO//2, 100)
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
            obj = Objeto(tipo)
            objetos.add(obj)
            todos.add(obj)

        
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
        pantalla.blit(fuente.render(f"Puntos: {score}", True, NEGRO), (10, 10))
        pantalla.blit(fuente.render(f"Tiempo: {segundos}", True, NEGRO), (ANCHO - 200, 10))
        pygame.display.flip()
        clock.tick(60)

       
        if tiempo_restante <= 0:
            game_over = True

    
    pygame.mixer.music.stop()
    pantalla.fill(BLANCO)
    mensaje = "¡Tiempo terminado!" if tiempo_restante <= 0 else "¡Perdiste! Tocaste algo peligroso "
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

if __name__ == "__main__":
    menu_principal()
