import pygame
import random

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Clase para representar organismos
class Organism(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = random.randrange(SCREEN_HEIGHT)
        self.speedx = speed
        self.speedy = speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Si sale de la pantalla, rebota
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speedx *= -1
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
            self.speedy *= -1

# Clase para el organismo depredador
class Predator(Organism):
    def __init__(self):
        super().__init__(RED, 20, 20, 2)

# Clase para el organismo presa
class Prey(Organism):
    def __init__(self):
        super().__init__(GREEN, 15, 15, 1)

# Clase para el organismo de planta
class Plant(Organism):
    def __init__(self):
        super().__init__(BLUE, 10, 10, 0)

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Simulador de Ecosistema")
clock = pygame.time.Clock()

# Lista de todos los sprites
all_sprites = pygame.sprite.Group()

# Lista de organismos
organisms = []

# Crear organismos
for _ in range(5):
    predator = Predator()
    all_sprites.add(predator)
    organisms.append(predator)

for _ in range(20):
    prey = Prey()
    all_sprites.add(prey)
    organisms.append(prey)

for _ in range(30):
    plant = Plant()
    all_sprites.add(plant)
    organisms.append(plant)

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar
    all_sprites.update()

# Lista de organismos de presa
    prey_group = pygame.sprite.Group([o for o in organisms if isinstance(o, Prey)])

    # Interacciones entre organismos
    for organism in organisms:
        # Predador se alimenta de presas
        if isinstance(organism, Predator):
            prey_hit_list = pygame.sprite.spritecollide(organism, prey_group, True)
            for prey in prey_hit_list:
                organisms.remove(prey)
                all_sprites.remove(prey)


        # Presa se reproduce
        if isinstance(organism, Prey) and random.random() < 0.01:
            new_prey = Prey()
            all_sprites.add(new_prey)
            organisms.append(new_prey)

        # Planta se reproduce
        if isinstance(organism, Plant) and random.random() < 0.005:
            new_plant = Plant()
            all_sprites.add(new_plant)
            organisms.append(new_plant)

    # Dibujar en la pantalla
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Refrescar la pantalla
    pygame.display.flip()

    # Limitar la velocidad de fotogramas
    clock.tick(30)

# Cerrar Pygame
pygame.quit()
