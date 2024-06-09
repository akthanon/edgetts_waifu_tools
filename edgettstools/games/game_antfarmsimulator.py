import pygame
import random
import heapq

# Configuración de la ventana
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_COLOR = (255, 255, 255)
ANT_COLOR = (0, 0, 0)
FOOD_COLOR = (0, 255, 0)
COLONY_COLOR = (255, 0, 0)
CAVE_COLOR = (100, 100, 100)
ANT_SIZE = 5
FOOD_SIZE = 7
CELL_SIZE = 15
COLONY_SIZE = 20
INSIDE_COLONY_SIZE=10
FOOD_NUMBER = 3
MOVEMENT_SPEED = 0.2  # Número de celdas que se mueven las hormigas en cada bucle

# Eliminar el contenido del archivo messages.txt al iniciar el programa
def initialize_file():
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
        self.messages.append(message)
        self.write_to_file()

    def write_to_file(self):
        with open(self.filename, 'w') as file:
            for message in self.messages:
                file.write(message + '\n')

# Crear una instancia de MessageLogger
logger = MessageLogger("messages_game.txt")

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ant:
    def __init__(self, colony, x, y):
        self.colony = colony
        self.x = x
        self.y = y
        self.has_food = False
        self.path = []
        self.direction = None
        self.direction_timer = 0

    def move(self):
        if not self.has_food:
            # Busca comida
            self.search_food()
        else:
            # Sigue el camino más corto al hormiguero
            self.follow_path()

    def search_food(self):
        if self.direction is None or self.direction_timer <= 0:
            self.direction = random.choice(['up', 'down', 'left', 'right', 'stop'])
            if self.direction == 'up':
                self.direction_timer = random.randint(5, 20)
            elif self.direction == 'down':
                self.direction_timer = random.randint(5, 20)
            elif self.direction == 'left':
                self.direction_timer = random.randint(5, 20)
            elif self.direction == 'right':
                self.direction_timer = random.randint(5, 20)
            elif self.direction == 'stop':
                self.direction_timer = random.randint(5, 20)

        if self.direction == 'up':
            new_y = self.y - CELL_SIZE * MOVEMENT_SPEED
            if not self.colony.caves.is_wall(self.x, new_y):
                self.y = new_y
        elif self.direction == 'down':
            new_y = self.y + CELL_SIZE * MOVEMENT_SPEED
            if not self.colony.caves.is_wall(self.x, new_y):
                self.y = new_y
        elif self.direction == 'left':
            new_x = self.x - CELL_SIZE * MOVEMENT_SPEED
            if not self.colony.caves.is_wall(new_x, self.y):
                self.x = new_x
        elif self.direction == 'right':
            new_x = self.x + CELL_SIZE * MOVEMENT_SPEED
            if not self.colony.caves.is_wall(new_x, self.y):
                self.x = new_x
        elif self.direction == 'stop':
            pass

        self.direction_timer -= 1

        # Comprobar si está dentro de los límites
        self.check_boundaries()

        # Comprobar si encontró comida
        for food in self.colony.food_sources:
            if self.x // CELL_SIZE == food.x // CELL_SIZE and self.y // CELL_SIZE == food.y // CELL_SIZE:
                self.has_food = True
                self.colony.food_sources.remove(food)
                self.path = self.a_star_path((self.x, self.y), (self.colony.x, self.colony.y))
                #print(f"Hormiga encontró comida en [{self.x}, {self.y}]")
                #logger.log(f"Hormiga encontró comida en [{self.x}, {self.y}]")

    def follow_path(self):
        if self.path:
            next_pos = self.path[0]
            target_x, target_y = next_pos

            # Calcular el movimiento hacia el siguiente punto en el camino
            dx = target_x - self.x
            dy = target_y - self.y

            dist = (dx**2 + dy**2)**0.5

            if dist <= CELL_SIZE * MOVEMENT_SPEED:
                # Si está cerca del siguiente punto, moverse directamente a él y quitarlo del camino
                self.x, self.y = next_pos
                self.path.pop(0)
            else:
                # Movimiento gradual hacia el siguiente punto
                self.x += (dx / dist) * CELL_SIZE * MOVEMENT_SPEED
                self.y += (dy / dist) * CELL_SIZE * MOVEMENT_SPEED

        # Comprobar si llegó al hormiguero
        if self.x == self.colony.x and self.y == self.colony.y:
            self.has_food = False
            self.colony.food_collected += 1
            #print(f"Hormiga volvió al hormiguero con comida. Total comida: {self.colony.food_collected}")
            logger.log(f">Hormigas vuelven con comida. Total comida: {self.colony.food_collected}")

    def check_boundaries(self):
        # Comprobar si la hormiga está fuera de los límites
        if self.x < 0:
            self.x = WINDOW_WIDTH - CELL_SIZE
        elif self.x >= WINDOW_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = WINDOW_HEIGHT - CELL_SIZE
        elif self.y >= WINDOW_HEIGHT:
            self.y = 0

    def a_star_path(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start_cell = (start[0] // CELL_SIZE, start[1] // CELL_SIZE)
        goal_cell = (goal[0] // CELL_SIZE, goal[1] // CELL_SIZE)

        open_set = []
        heapq.heappush(open_set, (0, start_cell))
        came_from = {}
        g_score = {start_cell: 0}
        f_score = {start_cell: heuristic(start_cell, goal_cell)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal_cell:
                path = []
                while current in came_from:
                    path.append((current[0] * CELL_SIZE + CELL_SIZE // 2, current[1] * CELL_SIZE + CELL_SIZE // 2))
                    current = came_from[current]
                path.reverse()
                return path

            neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                         (current[0], current[1] + 1), (current[0], current[1] - 1)]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < self.colony.caves.cols and 0 <= neighbor[1] < self.colony.caves.rows:
                    if self.colony.caves.grid[int(neighbor[1])][int(neighbor[0])]:
                        continue

                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal_cell)
                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

class Colony:
    def __init__(self, x, y, num_ants, caves):
        self.x = x
        self.y = y
        self.caves = caves
        self.ants = [Ant(self, x, y) for _ in range(num_ants)]
        self.food_sources = []
        self.food_collected = 0
        self.food_timer = random.randint(800, 3000)  # Tiempo inicial antes de generar la primera comida
        self.food_interval = random.randint(800, 3000)  # Intervalo entre generación de comida

    def generate_food(self):
        # Generar una nueva fuente de comida en una ubicación aleatoria del mapa
        while True:
            x = random.randint(0, WINDOW_WIDTH - CELL_SIZE)
            y = random.randint(0, WINDOW_HEIGHT - CELL_SIZE)
            if not self.caves.is_wall(x, y):
                self.food_sources.append(Food(x, y))
                break

    def add_food_source(self, food):
        self.food_sources.append(food)

    def update(self):
        self.food_timer -= 1
        if self.food_timer <= 0:
            self.generate_food()
            self.food_timer = self.food_interval
        for ant in self.ants:
            ant.move()

    def draw(self, screen):
        # Dibujar el hormiguero
        pygame.draw.circle(screen, COLONY_COLOR, (self.x, self.y), ANT_SIZE)
        
        # Dibujar las hormigas
        for ant in self.ants:
            color = ANT_COLOR if not ant.has_food else FOOD_COLOR
            pygame.draw.circle(screen, color, (ant.x, ant.y), ANT_SIZE)
        
        # Dibujar las fuentes de comida
        for food in self.food_sources:
            pygame.draw.circle(screen, FOOD_COLOR, (food.x, food.y), FOOD_SIZE)

class CaveSystem:
    def __init__(self):
        self.rows = (WINDOW_HEIGHT) // CELL_SIZE
        self.cols = (WINDOW_WIDTH) // CELL_SIZE
        self.grid = [[True for _ in range(self.cols)] for _ in range(self.rows)]
        self.generate_caves()

    def generate_caves(self):
        # Inicializar con muros sólidos
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = True

        # Generar cuevas usando Recursive Backtracking
        stack = [(1, 1)]
        self.grid[1][1] = False
        while stack:
            current_cell = stack[-1]
            x, y = current_cell
            neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
            unvisited_neighbors = [neighbor for neighbor in neighbors if self.is_valid_cell(neighbor)]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                next_x, next_y = next_cell
                wall_x, wall_y = (next_x + x) // 2, (next_y + y) // 2
                if 0 <= wall_x < self.rows and 0 <= wall_y < self.cols:  # Verificar límites
                    self.grid[wall_x][wall_y] = False
                    self.grid[next_x][next_y] = False
                    if random.random() < 0.01:  # Probabilidad de crear una cámara grande
                        xsize = random.randint(5, 15)  # Modificar el rango para un área más grande
                        ysize = random.randint(5, 15)  # Modificar el rango para un área más grande
                        for i in range(xsize):
                            for j in range(ysize):
                                new_x, new_y = wall_x + i, wall_y + j
                                if 0 <= new_x < self.rows and 0 <= new_y < self.cols:  # Verificar límites
                                    self.grid[new_x][new_y] = False
                stack.append(next_cell)
            else:
                stack.pop()

    def is_valid_cell(self, cell):
        x, y = cell
        return 0 < x < self.rows - 1 and 0 < y < self.cols - 1 and self.grid[x][y]

    def is_wall(self, x, y):
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return True  # Considerar fuera de los límites como pared

    def is_chamber(self, x, y):
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)
        # Verificar si el área 3x3 alrededor del punto central está libre
        for i in range(-1, 2):
            for j in range(-1, 2):
                check_col = col + i
                check_row = row + j
                if 0 <= check_row < self.rows and 0 <= check_col < self.cols:
                    if self.grid[check_row][check_col]:
                        return True
                else:
                    return True

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col]:
                    pygame.draw.rect(screen, CAVE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Granja de Hormigas")

# Crear el sistema de cuevas
caves = CaveSystem()

# Generar posición aleatoria para el hormiguero en una celda vacía
while True:
    colony_x = (random.randint(1, caves.cols - 2) * CELL_SIZE) + CELL_SIZE // 2
    colony_y = (random.randint(1, caves.rows - 2) * CELL_SIZE) + CELL_SIZE // 2
    if not caves.is_chamber(colony_x, colony_y):
        break

# Crear la colonia
colony = Colony(colony_x, colony_y, INSIDE_COLONY_SIZE, caves)

# Añadir fuentes de comida dentro del sistema de cuevas
for _ in range(FOOD_NUMBER):
    while True:
        x = (random.randint(1, caves.cols - 2) * CELL_SIZE) + CELL_SIZE // 2
        y = (random.randint(1, caves.rows - 2) * CELL_SIZE) + CELL_SIZE // 2
        if not caves.is_wall(x, y):
            colony.add_food_source(Food(x, y))
            break

# Añadir hormigas dentro del sistema de cuevas
for _ in range(COLONY_SIZE):
    while True:
        x = (random.randint(1, caves.cols - 2) * CELL_SIZE) + CELL_SIZE // 2
        y = (random.randint(1, caves.rows - 2) * CELL_SIZE) + CELL_SIZE // 2
        if not caves.is_wall(x, y):
            colony.ants.append(Ant(colony, x, y))
            break

# Bucle principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar la colonia
    colony.update()

    # Dibujar todo
    screen.fill(BACKGROUND_COLOR)
    caves.draw(screen)
    colony.draw(screen)
    pygame.display.flip()
    
    clock.tick(60)  # Velocidad del bucle