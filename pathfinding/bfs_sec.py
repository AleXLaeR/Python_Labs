import pygame
import random
from queue import Queue
from abc import ABC, abstractmethod

# Constants
WIDTH = 1200
HEIGHT = 800
ROWS = 40
COLS = 60
CELL_SIZE = WIDTH // COLS
WHITE = (144, 238, 144)
BLACK = (210, 62, 91)
RED = (27, 27, 27)
PATH_COLOR = (146, 161, 207)

# Define directions (up, right, down, left)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class CanvasFigure(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

class Cell(CanvasFigure):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.borders = {'up': True, 'right': True, 'bottom': True, 'left': True}
        self._visited = False

    def mark_visited(self) -> None:
        self._visited = True

    def was_visited(self) -> bool:
        return self._visited

    def _draw_borders(self, x: int, y: int, screen: pygame.Surface) -> None:
        if self.borders['up']:
            self._draw_upper_border(x, y, screen)
        if self.borders['right']:
            self._draw_right_border(x, y, screen)
        if self.borders['bottom']:
            self._draw_lower_border(x, y, screen)
        if self.borders['left']:
            self._draw_left_border(x, y, screen)

    @staticmethod
    def _draw_upper_border(x: int, y: int, screen: pygame.Surface) -> None:
        start_coords = (x, y)
        end_coords = (x + CELL_SIZE, y)
        pygame.draw.line(screen, BLACK, start_coords, end_coords, 3)

    @staticmethod
    def _draw_lower_border(x: int, y: int, screen: pygame.Surface) -> None:
        start_coords = (x, y + CELL_SIZE)
        end_coords = (x + CELL_SIZE, y + CELL_SIZE)
        pygame.draw.line(screen, BLACK, start_coords, end_coords, 3)

    @staticmethod
    def _draw_right_border(x: int, y: int, screen: pygame.Surface) -> None:
        start_coords = (x + CELL_SIZE, y)
        end_coords = (x + CELL_SIZE, y + CELL_SIZE)
        pygame.draw.line(screen, BLACK, start_coords, end_coords, 3)

    @staticmethod
    def _draw_left_border(x: int, y: int, screen: pygame.Surface) -> None:
        start_coords = (x, y + CELL_SIZE)
        end_coords = (x, y)
        pygame.draw.line(screen, BLACK, start_coords, end_coords, 3)


    def draw(self, screen: pygame.Surface) -> None:
        x: int = self.col * CELL_SIZE
        y: int = self.row * CELL_SIZE

        if self.was_visited():
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        self._draw_borders(x, y, screen)

    def highlight_point(self, screen: pygame.Surface, color: tuple) -> None:
        x = self.col * CELL_SIZE + CELL_SIZE // 2
        y = self.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, color, (x, y), 7.5)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 3)

class MazeComposite(CanvasFigure):
    def __init__(self):
        self.grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]
        self.current_cell = self.grid[0][0]

    def draw(self, on_canvas: pygame.Surface) -> None:
        for row in self.grid:
            for cell in row:
                cell.draw(on_canvas)

    def generate_maze(self) -> None:
        stack: list[Cell] = [self.current_cell]

        while len(stack) != 0:
            current_cell = stack.pop()
            current_cell.mark_visited()

            neighbors: list[Cell] = self.get_unvisited_neighbors(current_cell)

            if len(neighbors) == 0:
                continue

            stack.append(current_cell)
            next_cell = random.choice(neighbors)
            self.remove_wall(current_cell, next_cell)

            next_cell.mark_visited()
            stack.append(next_cell)

    def get_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []

        for dr, dc in DIRECTIONS:
            new_row = cell.row + dr
            new_col = cell.col + dc

            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                neighbor = self.grid[new_row][new_col]
                if not neighbor.was_visited():
                    neighbors.append(neighbor)

        return neighbors

    def remove_wall(self, current_cell, next_cell: Cell) -> None:
        if current_cell.row == next_cell.row:
            if current_cell.col < next_cell.col:
                current_cell.borders['right'] = False
                next_cell.borders['left'] = False
            else:
                current_cell.borders['left'] = False
                next_cell.borders['right'] = False
        else:
            if current_cell.row < next_cell.row:
                current_cell.borders['bottom'] = False
                next_cell.borders['up'] = False
            else:
                current_cell.borders['up'] = False
                next_cell.borders['bottom'] = False

    def bfs(self, start, end):
        visited = set()
        queue = Queue()
        parent = {}

        queue.put(start)
        visited.add(start)

        while not queue.empty():
            current = queue.get()
            if current == end:
                break
            for dr, dc in DIRECTIONS:
                new_row, new_col = current.row + dr, current.col + dc
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    neighbor = self.grid[new_row][new_col]
                    if not neighbor in visited and not self.has_wall(current, neighbor):
                        queue.put(neighbor)
                        visited.add(neighbor)
                        parent[neighbor] = current

        path = []
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)

        return list(reversed(path))

    def has_wall(self, cell1: Cell, cell2: Cell) -> bool:
        if cell1.row == cell2.row:
            if cell1.col < cell2.col:
                return cell1.borders['right']
            else:
                return cell1.borders['left']
        else:
            if cell1.row < cell2.row:
                return cell1.borders['bottom']
            else:
                return cell1.borders['up']


def get_path_points(maze: MazeComposite, from_cell: Cell, to_cell: Cell) -> list[tuple[int, int]]:
    hor_point_center = lambda cell: cell.col * CELL_SIZE + CELL_SIZE // 2
    vert_point_center = lambda cell: cell.row * CELL_SIZE + CELL_SIZE // 2

    found_path: list[Cell] = maze.bfs(from_cell, to_cell)
    connected_path_points = [(hor_point_center(cell), vert_point_center(cell)) for cell in found_path]

    return connected_path_points


def main():
    pygame.init()
    canvas = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Лабиринт - поиск пути")

    maze = MazeComposite()
    maze.generate_maze()

    start_point = maze.grid[ROWS - 1][0]
    end_point = maze.grid[0][COLS - 1]

    is_game_running = True
    while is_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False

        maze.draw(on_canvas=canvas)

        path_points = get_path_points(maze, start_point, end_point)
        pygame.draw.lines(canvas, PATH_COLOR, False, path_points, 5)

        start_point.highlight_point(canvas, RED)
        end_point.highlight_point(canvas, RED)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
