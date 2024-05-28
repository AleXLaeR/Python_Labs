from tkinter import (
    Tk as Window,
    Canvas,
)
import numpy as np

from grid_templates import *
from math import floor
from cell import Cell

class GameOfLife:
    _cell_px_size: int = 10
    _grid_width: int = 80
    _grid_height: int = 50

    def __init__(self, wd: Window, grid_width: int = _grid_width, grid_height: int = _grid_height,
                 *, grid_template: GridGenerationStrategy = None, upd_interval: float = 200):
        self.display = wd
        self.delay = upd_interval
        self.display.title(GameOfLife.__name__)

        self.grid_width = grid_width
        self.grid_height = grid_height

        self.canvas = Canvas(wd,
                             width=grid_width * GameOfLife._cell_px_size,
                             height=grid_height * GameOfLife._cell_px_size)
        self.canvas.pack()

        self._set_template(grid_width, grid_height, grid_template)
        self.grid_cells = self._create_cells(self.canvas)

    def run(self) -> None:
        self._next_generation()

    def _set_template(self, grid_width: int, grid_height: int, grid_template: GridGenerationStrategy) -> None:
        if grid_template is None:
            grid_template = EmptyGenerationStrategy(grid_width, grid_height)
        self.grid = grid_template.generate()

    def _create_cells(self, canvas: Canvas) -> dict[tuple, Cell]:
        rectangles: dict[tuple, Cell] = {}

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rectangles[(x, y)] = Cell(x, y, GameOfLife._cell_px_size, canvas)

        return rectangles

    def _count_neighbors(self, x_coord: int, y_coord: int) -> np.ndarray:
        abscissa_neighbors = slice(x_coord - 1, x_coord + 2 % self.grid_width)
        ordinate_neighbors = slice(y_coord - 1, y_coord + 2 % self.grid_height)

        alive_nearest = np.sum(self.grid[abscissa_neighbors, ordinate_neighbors])
        cell_state = self.grid[x_coord, y_coord]

        return alive_nearest - cell_state

    def _next_generation(self) -> None:
        new_grid = np.zeros((self.grid_width, self.grid_height), dtype=bool)

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                current_cell = self.grid[x, y]
                # Отримуємо кількість "живих" сусідів
                alive_neighbors = self._count_neighbors(x, y)

                if current_cell == 1:
                    # Якщо у живої клітини є менше 2 або більше 3 живих сусідів, вона вмирає
                    # від "самотності" або "перенаселення" наступного кроку.
                    if not (2 <= alive_neighbors <= 3):
                        new_grid[x, y] = False
                    else:
                        # Якщо у живої клітини є 2-3 живі сусіди, то вона залишається такою ж наступного кроку.
                        new_grid[x, y] = current_cell

                # Якщо у мертвої клітини точно є 3 живі сусіди, то вона стає живою наступного кроку.
                elif alive_neighbors == 3:
                    new_grid[x, y] = True

        # color painting
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.grid[x, y] != new_grid[x, y]:
                    self.grid[x, y] = new_grid[x, y]
                    fill_color = "black" if new_grid[x, y] else "white"
                    self.grid_cells[(x, y)].update_canvas_cell(fill_color)

        self.display.after(floor(self.delay), self._next_generation)