import pygame
import numpy as np

# Ініціалізація Pygame
pygame.init()

# Розмір екрану та параметри клітин
width, height = 800, 600
cell_size: int = 10

white_color: tuple = (255, 255, 255)
black_color: tuple = (0, 0, 0)

# Створення матриці для зберігання стану клітин (1 - жива, 0 - мертва)
rows, cols = height // cell_size, width // cell_size
grid: np.array = np.zeros((rows, cols), dtype=int)


# Функція для заповнення випадковим чином початкового стану
def randomize_grid():
    grid[:, :] = np.random.choice([0, 1], size=(rows, cols))


# Функція для відображення стану клітин
def draw_grid(surface):
    surface.fill(white_color)  # Заповнення фону білим кольором

    for row in range(rows):
        for col in range(cols):
            color: tuple = white_color if grid[row, col] == 1 else black_color
            pygame.draw.rect(
                surface,
                color,
                (col * cell_size, row * cell_size, cell_size, cell_size),
            )


# Функція для обчислення нового стану клітин за правилами гри "Життя"
def update_grid():
    new_grid = np.zeros((rows, cols), dtype=int)

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            sum_ = np.sum(grid[row - 1:row + 2, col - 1:col + 2])
            neighbors_sum = sum_ - grid[row, col]

            if grid[row, col] and (neighbors_sum < 2 or neighbors_sum > 3):
                new_grid[row, col] = False
            elif not grid[row, col] and neighbors_sum == 3:
                new_grid[row, col] = True
            else:
                new_grid[row, col] = grid[row, col]

    grid[:, :] = new_grid


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

running = True
randomize_grid()  # Заповнення випадковим чином початкового стану

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_grid()  # Обчислення нового стану клітин
    draw_grid(screen)  # Відображення стану клітин на екрані
    pygame.display.flip()
    pygame.time.delay(100)  # Затримка для візуалізації

pygame.quit()
