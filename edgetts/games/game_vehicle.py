import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Carreras Infinitas")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clase para el jugador (automóvil)
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.centery = HEIGHT // 2
        self.speed_y = 0

    def update(self):
        self.rect.x += 5  # El automóvil se mueve automáticamente hacia adelante
        self.rect.y += self.speed_y

        # Limitar la posición del automóvil dentro de la pantalla
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Clase para los obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randrange(50, 200)  # Aparecer más adelante en la pantalla
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

    def update(self):
        self.rect.x -= 5  # Los obstáculos se mueven hacia la izquierda

# Función principal del juego
def main():
    clock = pygame.time.Clock()
    FPS = 60
    running = True

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    car = Car()
    all_sprites.add(car)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    car.speed_y = -5
                elif event.key == pygame.K_DOWN:
                    car.speed_y = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    car.speed_y = 0

        # Generación de nuevos obstáculos
        if len(obstacles) < 5 and random.randint(0, 100) < 10:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        # Colisión entre el automóvil y los obstáculos
        hits = pygame.sprite.spritecollide(car, obstacles, False)
        if hits:
            running = False

        # Actualizar y dibujar
        all_sprites.update()

        # Ajustar la posición de la cámara para que siga al automóvil
        screen.fill((0, 0, 0))
        for entity in all_sprites:
            screen.blit(entity.image, (entity.rect.x - car.rect.x + WIDTH // 4, entity.rect.y))
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
