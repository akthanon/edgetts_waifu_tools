import numpy as np
import cupy as cp
import time
import pygame

# Configuración de Pygame
pygame.init()
screen_width, screen_height = 800, 800
cell_size = 10
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de la Vida con CuPy")

# Configuración de la simulación
limit_x = screen_width // cell_size
limit_y = screen_height // cell_size
initial_density = 0.2
update_interval = 0.1

def initialize_grid(limit_x, limit_y):
    return cp.random.choice([0, 1], size=(limit_y, limit_x), p=[1-initial_density, initial_density])

def update_grid(grid, limit_x, limit_y):
    neighbor_count = cp.zeros_like(grid)
    neighbor_count[:-1, :] += grid[1:, :]  # Vecinos abajo
    neighbor_count[1:, :] += grid[:-1, :]  # Vecinos arriba
    neighbor_count[:, :-1] += grid[:, 1:]  # Vecinos a la derecha
    neighbor_count[:, 1:] += grid[:, :-1]  # Vecinos a la izquierda
    neighbor_count[:-1, :-1] += grid[1:, 1:]  # Vecinos abajo-derecha
    neighbor_count[1:, 1:] += grid[:-1, :-1]  # Vecinos arriba-izquierda
    neighbor_count[1:, :-1] += grid[:-1, 1:]  # Vecinos arriba-derecha
    neighbor_count[:-1, 1:] += grid[1:, :-1]  # Vecinos abajo-izquierda
    
    # Reglas del juego de la vida
    new_grid = (grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3))
    new_grid |= (grid == 0) & (neighbor_count == 3)
    return new_grid.astype(int)

def draw_grid(grid):
    screen.fill((255, 255, 255))
    for y in range(limit_y):
        for x in range(limit_x):
            if grid[y, x] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (x * cell_size, y * cell_size, cell_size, cell_size))
    pygame.display.flip()

def simulate():
    grid = initialize_grid(limit_x, limit_y)
    last_update_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if time.time() - last_update_time >= update_interval:
            grid = update_grid(grid, limit_x, limit_y)
            draw_grid(grid)
            last_update_time = time.time()

    pygame.quit()

if __name__ == "__main__":
    simulate()
