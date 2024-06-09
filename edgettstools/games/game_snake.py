import pygame
import random
from collections import deque
import time
from datetime import datetime

# Eliminar el contenido del archivo messages.txt al iniciar el programa
with open("messages_game.txt", "w") as file:
    file.write("")

def read_messages_from_file():
    with open("messages_game.txt", "r") as file:
        return file.readlines()

def save_messages_to_file(messages):
    with open("messages_game.txt", "w") as file:
        file.writelines(messages)

class MessageLogger:
    def __init__(self, filename, max_messages=10):
        self.filename = filename
        self.max_messages = max_messages
        self.messages = []

    def log(self, message):
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)
        self.messages.append(datetime.now().strftime("[%H:%M:%S]")+message)
        self.write_to_file()

    def write_to_file(self):
        with open(self.filename, 'w') as file:
            for message in self.messages:
                file.write(message + '\n')

# Crear una instancia de MessageLogger
logger = MessageLogger("messages_game.txt")

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configuraciones de la pantalla
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
FPS = 5
RESTART_DELAY = 5000  # 5 segundos en milisegundos

# Direcciones
UP = (0, -CELL_SIZE)
DOWN = (0, CELL_SIZE)
LEFT = (-CELL_SIZE, 0)
RIGHT = (CELL_SIZE, 0)

# Función para generar comida en una posición aleatoria
def generate_food(snake):
    while True:
        food_x = random.randint(0, WIDTH - CELL_SIZE)
        food_y = random.randint(0, HEIGHT - CELL_SIZE)
        food_pos = (food_x // CELL_SIZE * CELL_SIZE, food_y // CELL_SIZE * CELL_SIZE)
        if food_pos not in snake:
            return food_pos

# Función para mover la serpiente automáticamente hacia la comida
def auto_move(snake, food):
    # Usar búsqueda en anchura (BFS) para encontrar el camino más corto
    visited = set()
    queue = deque([(snake[0], [])])  # Cola de posiciones y camino
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == food:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in snake and 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
                queue.append(((new_x, new_y), path + [(new_x, new_y)]))

    # Si no se puede encontrar un camino, ir en cualquier dirección disponible
    head_x, head_y = snake[0]
    for dx, dy in [UP, DOWN, LEFT, RIGHT]:
        new_x, new_y = head_x + dx, head_y + dy
        if (new_x, new_y) not in snake and 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            return [(new_x, new_y)]

# Función principal del juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 36)

    running = True
    winlose_number = 1  # Inicializar food_number
    logger.log(f">Juego nuevo número {winlose_number} iniciado")
    while running:
        snake = [(WIDTH // 2, HEIGHT // 2)]
        direction = RIGHT  # Dirección inicial
        food = generate_food(snake)

        restart_time = 0
        game_over = False
        food_number = 0  # Inicializar food_number
        
        while not game_over:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = True

            # Mover la serpiente automáticamente hacia la comida
            path_to_food = auto_move(snake, food)
            if path_to_food:
                direction = (path_to_food[0][0] - snake[0][0], path_to_food[0][1] - snake[0][1])
            else:
                game_over = True

            # Mover la serpiente
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, new_head)
            if new_head == food:
                food = generate_food(snake)
                if food_number % 30 == 0:
                    logger.log(f">La serpiente ha comido {food_number} manzanas")
                food_number += 1  # Incrementar food_number
            else:
                snake.pop()

            # Dibujar la pantalla
            screen.fill(BLACK)
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()

            # Control de velocidad
            clock.tick(FPS)

            # Verificar si la serpiente chocó consigo misma o con los bordes de la pantalla
            if (snake[0] in snake[1:]) or (snake[0][0] < 0 or snake[0][0] >= WIDTH or snake[0][1] < 0 or snake[0][1] >= HEIGHT):
                game_over_text = font.render("PERDISTE", True, WHITE)
                logger.log(f">La serpiente ha chocado con su cola habiendo comido {food_number} manzanas. Muertes Totales: {winlose_number}")
                winlose_number += 1  # Incrementar food_number
                game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(game_over_text, game_over_text_rect)
                pygame.display.flip()
                if current_time - restart_time >= RESTART_DELAY:
                    game_over = True
                    restart_time = current_time
                    time.sleep(5)               
                    food_number = 0  # Inicializar food_number
                    logger.log(f">Juego nuevo número {winlose_number} iniciado")

    pygame.quit()

if __name__ == "__main__":
    main()
