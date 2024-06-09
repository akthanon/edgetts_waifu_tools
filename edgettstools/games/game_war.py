import pygame
import random

# Inicializar pygame
pygame.init()

# Definir dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Parámetros de simulación
ARMY_SIZE = 20
UNIT_RADIUS = 10
ATTACK_RANGE = 50
ATTACK_DAMAGE = 10
MOVE_SPEED = 2
RANDOM_MOVE_FREQ = 0.02
RANDOM_ATTACK_FREQ = 0.02

# Clase para representar un ejército
class Army:
    def __init__(self, color, start_x):
        self.color = color
        self.units = []
        self.start_x = start_x

    # Agregar una unidad al ejército
    def add_unit(self):
        unit_type = random.choice(["infantry", "cavalry", "archer"])
        unit = Unit(self.color, self.start_x, unit_type)
        self.units.append(unit)

    # Mover todas las unidades hacia adelante
    def move_units(self, target_army):
        for unit in self.units:
            unit.move(target_army)

    # Realizar ataques
    def attack(self, target_army):
        for unit in self.units:
            unit.attack(target_army)

# Clase para representar una unidad
class Unit:
    def __init__(self, color, x, unit_type):
        self.color = color
        self.x = x
        self.y = random.randint(50, HEIGHT - 50)
        self.health = 100
        self.unit_type = unit_type
        self.random_move_counter = 0
        self.random_attack_counter = 0

    # Mover la unidad hacia adelante
    def move(self, target_army):
        if random.random() < RANDOM_MOVE_FREQ:
            self.random_move_counter = random.randint(1, 30)
        if self.random_move_counter > 0:
            self.x += random.choice([-1, 1]) * MOVE_SPEED
            self.random_move_counter -= 1
        else:
            if target_army.units:
                target = target_army.units[random.randint(0, len(target_army.units) - 1)]
                if target.x < self.x:
                    self.x -= MOVE_SPEED
                else:
                    self.x += MOVE_SPEED

    # Realizar ataques
    def attack(self, target_army):
        if random.random() < RANDOM_ATTACK_FREQ:
            self.random_attack_counter = random.randint(1, 30)
        if self.random_attack_counter > 0:
            return
        for target in target_army.units:
            if abs(target.x - self.x) <= ATTACK_RANGE and self.color != target.color:
                target.health -= ATTACK_DAMAGE
                if target.health <= 0:
                    target_army.units.remove(target)

# Inicializar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de guerra")

# Crear ejércitos
red_army = Army(RED, 50)
blue_army = Army(BLUE, WIDTH - 50)

# Llenar ejércitos con unidades
for _ in range(ARMY_SIZE):
    red_army.add_unit()
    blue_army.add_unit()

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mover y atacar ejércitos
    red_army.move_units(blue_army)
    blue_army.move_units(red_army)
    red_army.attack(blue_army)
    blue_army.attack(red_army)

    # Dibujar ejércitos en la pantalla
    screen.fill(WHITE)
    for unit in red_army.units:
        if unit.unit_type == "infantry":
            pygame.draw.circle(screen, RED, (unit.x, unit.y), UNIT_RADIUS)
        elif unit.unit_type == "cavalry":
            pygame.draw.rect(screen, RED, pygame.Rect(unit.x - UNIT_RADIUS, unit.y - UNIT_RADIUS, UNIT_RADIUS * 2, UNIT_RADIUS * 2))
        elif unit.unit_type == "archer":
            pygame.draw.polygon(screen, RED, [(unit.x, unit.y - UNIT_RADIUS), (unit.x - UNIT_RADIUS, unit.y + UNIT_RADIUS), (unit.x + UNIT_RADIUS, unit.y + UNIT_RADIUS)])
    for unit in blue_army.units:
        if unit.unit_type == "infantry":
            pygame.draw.circle(screen, BLUE, (unit.x, unit.y), UNIT_RADIUS)
        elif unit.unit_type == "cavalry":
            pygame.draw.rect(screen, BLUE, pygame.Rect(unit.x - UNIT_RADIUS, unit.y - UNIT_RADIUS, UNIT_RADIUS * 2, UNIT_RADIUS * 2))
        elif unit.unit_type == "archer":
            pygame.draw.polygon(screen, BLUE, [(unit.x, unit.y - UNIT_RADIUS), (unit.x - UNIT_RADIUS, unit.y + UNIT_RADIUS), (unit.x + UNIT_RADIUS, unit.y + UNIT_RADIUS)])

    # Actualizar pantalla
    pygame.display.flip()

    # Limitar velocidad de fotogramas
    clock.tick(30)

# Salir del juego
pygame.quit()
