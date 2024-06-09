import random
import pygame
import time

# Configuración de Pygame
pygame.init()
screen_width, screen_height = 1200, 800  # Ancho incrementado para margen derecho
cell_size = 10
simulation_width = 800  # Mantener el área de simulación de 800x800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulación de Bacterias")
font = pygame.font.SysFont(None, 24)

# Configuración de la simulación
limit_x = simulation_width // cell_size
limit_y = screen_height // cell_size
initial_bacteria_count = 100
max_bacteria_count = 2000
reproduction_energy_threshold = 6
reproduction_probability = 0.4
mutation_probability = 0.2
food_probability = 0.1
food_energy = 40
max_age = 100

# Colores
colors = {'A': (255, 0, 0), 'B': (0, 255, 0), 'C': (0, 0, 255), 'X': (128, 128, 128), 'F': (255, 255, 0)}

class Bacteria:
    def __init__(self, x, y, bacteria_type):
        self.x = x
        self.y = y
        self.energy = random.randint(2, 5)
        self.obstacle_avoidance = random.uniform(0.5, 1.0)
        self.bacteria_type = bacteria_type
        self.age = 0
        self.consumption_distance = random.randint(1, 2)
        self.move_distance = random.randint(1, 2)

    def move(self, obstacles, bacteria_list, food_list):
        for _ in range(self.move_distance):
            new_x = self.x + random.choice([-1, 0, 1])
            new_y = self.y + random.choice([-1, 0, 1])

            if random.uniform(0, 1) < self.obstacle_avoidance:
                if (0 <= new_x < limit_x and 0 <= new_y < limit_y and 
                    (new_y, new_x) not in obstacles and 
                    not any(b.x == new_x and b.y == new_y for b in bacteria_list)):
                    self.x = new_x
                    self.y = new_y

    def reproduce(self):
        if random.uniform(0, 1) < reproduction_probability:
            if random.uniform(0, 1) < mutation_probability:
                mutated_type = random.choice(['A', 'B', 'C'])
                return [Bacteria(self.x, self.y, mutated_type) for _ in range(2)]
            else:
                return [Bacteria(self.x, self.y, self.bacteria_type) for _ in range(2)]
        else:
            return []

def draw_grid(bacteria_list, obstacles, food_list):
    screen.fill((255, 255, 255))
    for bacteria in bacteria_list:
        pygame.draw.rect(screen, colors[bacteria.bacteria_type], 
                         (bacteria.x * cell_size, bacteria.y * cell_size, cell_size, cell_size))

    for obstacle in obstacles:
        pygame.draw.rect(screen, colors['X'], 
                         (obstacle[1] * cell_size, obstacle[0] * cell_size, cell_size, cell_size))

    for food in food_list:
        pygame.draw.rect(screen, colors['F'], 
                         (food[1] * cell_size, food[0] * cell_size, cell_size, cell_size))

    pygame.display.flip()

def draw_stats(bacteria_list, food_list, start_time):
    total_bacteria = len(bacteria_list)
    bacteria_a = sum(1 for b in bacteria_list if b.bacteria_type == 'A')
    bacteria_b = sum(1 for b in bacteria_list if b.bacteria_type == 'B')
    bacteria_c = sum(1 for b in bacteria_list if b.bacteria_type == 'C')
    elapsed_time = int(time.time() - start_time)
    total_food = len(food_list)

    stats_text = [
        f"Bacterias totales: {total_bacteria}",
        f"Bacterias tipo A: {bacteria_a}",
        f"Bacterias tipo B: {bacteria_b}",
        f"Bacterias tipo C: {bacteria_c}",
        f"Tiempo de simulación: {elapsed_time} segundos",
        f"Total de comida: {total_food}"
    ]

    y_offset = 10
    for line in stats_text:
        img = font.render(line, True, (0, 0, 0))
        screen.blit(img, (simulation_width + 10, y_offset))
        y_offset += 30

def consume_bacteria(consumer, prey):
    if consumer != prey and consumer.bacteria_type != prey.bacteria_type:
        consumer.energy += prey.energy
        prey.energy = 0

def consume_food(bacteria, food_list):
    for food in food_list:
        if bacteria.x == food[0] and bacteria.y == food[1]:
            bacteria.energy += food_energy
            food_list.remove(food)
            break

def simulate():
    global bacteria_list
    bacteria_list = [Bacteria(random.randint(0, limit_x - 1), random.randint(0, limit_y - 1), random.choice(['A', 'B', 'C'])) for _ in range(initial_bacteria_count)]
    obstacles = [(random.randint(0, limit_y - 1), random.randint(0, limit_x - 1)) for _ in range(5)]
    food_list = [(random.randint(0, limit_x - 1), random.randint(0, limit_y - 1)) for _ in range(5)]
    start_time = time.time()
    
    running = True
    while running:
        screen.fill((255, 255, 255))  # Limpiar la pantalla antes de dibujar
        draw_grid(bacteria_list, obstacles, food_list)
        draw_stats(bacteria_list, food_list, start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for bacteria in bacteria_list:
            bacteria.move(obstacles, bacteria_list, food_list)
            bacteria.age += 1

            consume_food(bacteria, food_list)

            for other_bacteria in bacteria_list:
                if (abs(bacteria.x - other_bacteria.x) <= bacteria.consumption_distance and
                        abs(bacteria.y - other_bacteria.y) <= bacteria.consumption_distance):
                    
                    consume_bacteria(bacteria, other_bacteria)

                    if bacteria.energy >= reproduction_energy_threshold:
                        new_bacteria_list = bacteria.reproduce()
                        for new_bacteria in new_bacteria_list:
                            new_bacteria.energy = bacteria.energy // 2
                        bacteria_list.extend(new_bacteria_list)
                        bacteria.energy = 0

                    break

            if bacteria.age >= max_age:
                # Convertir bacterias muertas en comida
                food_list.append((bacteria.x, bacteria.y))
                bacteria_list.remove(bacteria)

#NO MODIFICAR ESTE BLOQUE DE CODIGO
        if len(bacteria_list) >= max_bacteria_count:
            break

        if len(bacteria_list) == 0:
            break

        types_present = set(bacteria.bacteria_type for bacteria in bacteria_list)
        max_change_attempts = 10
        while len(types_present) < 3 and max_change_attempts > 0:
            new_type = random.choice(['A', 'B', 'C'])
            bacteria_change = random.choice(bacteria_list)
            if bacteria_change.bacteria_type != new_type:
                bacteria_change.bacteria_type = new_type
                types_present.add(new_type)
            max_change_attempts -= 1

        if random.uniform(0, 1) < food_probability:
            food_list.append((random.randint(0, limit_x - 1), random.randint(0, limit_y - 1)))

        pygame.display.flip()
        time.sleep(0.1)

#FIN DE BLOQUE INMODIFICABLE

#NO MODIFICAR ESTA SECCIÓN
if __name__ == "__main__":
    while True:
        simulate()
        break
#FIN DE SECCIÓN INMODIFICABLE

pygame.quit()

