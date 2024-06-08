import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Definir constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CAR_WIDTH = 30
CAR_HEIGHT = 60
CAR_SPEED = 2

# Clase para representar un automóvil
class Car:
    def __init__(self, x, y, color, path):
        self.x = x
        self.y = y
        self.color = color
        self.path = path
        self.target_index = 0
        self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)

    def move(self):
        if self.target_index < len(self.path):
            target = self.path[self.target_index]
            dx = target[0] - self.x
            dy = target[1] - self.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist <= CAR_SPEED:
                self.x = target[0]
                self.y = target[1]
                self.target_index += 1
            else:
                angle = math.atan2(dy, dx)
                self.x += math.cos(angle) * CAR_SPEED
                self.y += math.sin(angle) * CAR_SPEED

            self.rect.x = self.x
            self.rect.y = self.y

    def draw(self, screen):
        # Calcular la dirección de movimiento
        if self.target_index < len(self.path) - 1:
            target = self.path[self.target_index + 1]
            dx = target[0] - self.x
            dy = target[1] - self.y
            angle = math.degrees(math.atan2(-dy, dx))  # Invertir dy para que la rotación siga la dirección del movimiento

            # Crear una superficie con la imagen del automóvil
            car_image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(car_image, self.color, (0, 0, CAR_WIDTH, CAR_HEIGHT))

            # Rotar la imagen del automóvil
            rotated_car = pygame.transform.rotate(car_image, angle)
            rotated_rect = rotated_car.get_rect()

            # Establecer la posición de la imagen rotada
            rotated_rect.center = (self.x, self.y)

            # Dibujar la imagen rotada en la pantalla
            screen.blit(rotated_car, rotated_rect)

# Función para generar un camino aleatorio
def generate_path():
    num_points = random.randint(5, 10)
    path = []
    for _ in range(num_points):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        path.append((x, y))
    return path

# Función para verificar colisiones entre un automóvil y los edificios
def check_collisions(car, buildings):
    for building in buildings:
        if car.rect.colliderect(building):
            return True
    return False

# Función principal del juego
def main():
    # Configurar la pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simulador de Tráfico")

    # Crear edificios (obstáculos)
    buildings = []
    num_buildings = random.randint(5, 10)
    for _ in range(num_buildings):
        width = random.randint(100, 200)
        height = random.randint(100, 200)
        x = random.randint(0, SCREEN_WIDTH - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        buildings.append(pygame.Rect(x, y, width, height))

    # Crear automóviles
    cars = []
    for _ in range(5):
        x = random.randint(0, SCREEN_WIDTH - CAR_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT - CAR_HEIGHT)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        path = generate_path()
        car = Car(x, y, color, path)
        # Verificar que el automóvil no colisione con los edificios
        while check_collisions(car, buildings):
            car.x = random.randint(0, SCREEN_WIDTH - CAR_WIDTH)
            car.y = random.randint(0, SCREEN_HEIGHT - CAR_HEIGHT)
            car.rect.x = car.x
            car.rect.y = car.y
        cars.append(car)

    clock = pygame.time.Clock()

    # Bucle principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mover los automóviles
        for car in cars:
            car.move()

        # Dibujar el fondo y los edificios
        screen.fill(WHITE)
        for building in buildings:
            pygame.draw.rect(screen, BLACK, building)

        # Dibujar los automóviles
        for car in cars:
            car.draw(screen)

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
