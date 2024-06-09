import pygame
import sys

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Tamaño de la paleta
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20

# Tamaño de la pelota
BALL_RADIUS = 10

# Clase para la paleta del jugador
class Paddle(pygame.sprite.Sprite):
    def __init__(self, ball):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
        self.speed = 5
        self.ball = ball

    def update(self):
        # Calcular la diferencia entre la posición de la paleta y la posición de la pelota
        diff = self.ball.rect.centerx - self.rect.centerx
        
        # Mover la paleta hacia la posición de la pelota
        if diff < 0:
            self.rect.x -= self.speed
        elif diff > 0:
            self.rect.x += self.speed

        # Asegurarse de que la paleta no se salga de la pantalla
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2])
        self.image.fill(RED)
        pygame.draw.circle(self.image, RED, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = 5
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - BALL_RADIUS * 2:
            self.speed_x = -self.speed_x
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y

    def check_collision_with_bricks(self, bricks):
        collided_bricks = pygame.sprite.spritecollide(self, bricks, True)
        for brick in collided_bricks:
            # Determine the direction of the collision
            if abs(self.rect.right - brick.rect.left) < abs(self.speed_x) and self.speed_x > 0:
                self.speed_x = -self.speed_x
            elif abs(self.rect.left - brick.rect.right) < abs(self.speed_x) and self.speed_x < 0:
                self.speed_x = -self.speed_x
            elif abs(self.rect.bottom - brick.rect.top) < abs(self.speed_y) and self.speed_y > 0:
                self.speed_y = -self.speed_y
            elif abs(self.rect.top - brick.rect.bottom) < abs(self.speed_y) and self.speed_y < 0:
                self.speed_y = -self.speed_y

# Función principal del juego
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arkanoid")

    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()

    ball = Ball()  # Primero creamos la instancia de la pelota

    paddle = Paddle(ball)  # Luego creamos la instancia de la paleta y pasamos la pelota como argumento

    all_sprites.add(paddle)  # Agregamos la paleta a los sprites
    all_sprites.add(ball)  # Agregamos la pelota a los sprites

    # Generar ladrillos
    brick_width = 80
    brick_height = 30
    for row in range(5):
        for column in range(10):
            brick = pygame.sprite.Sprite()
            brick.image = pygame.Surface([brick_width, brick_height])
            brick.image.fill(WHITE)
            brick.rect = brick.image.get_rect()
            brick.rect.x = column * (brick_width + 2) + 1
            brick.rect.y = row * (brick_height + 2) + 50
            bricks.add(brick)
            all_sprites.add(brick)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        # Colisión entre la pelota y la paleta
        if pygame.sprite.collide_rect(ball, paddle):
            ball.speed_y = -ball.speed_y

        # Colisión entre la pelota y los ladrillos
        ball.check_collision_with_bricks(bricks)

        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
