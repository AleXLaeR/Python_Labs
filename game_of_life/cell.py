from tkinter import Canvas
from typing import Literal

class Cell:
    def __init__(self, x: int, y: int, px_size: int, canvas: Canvas):
        self.canvas = canvas
        self.figure_id = Cell._draw_cell(x, y, px_size, canvas)

    @staticmethod
    def _draw_cell(x: int, y: int, px_size: int, canvas: Canvas) -> int:
        return canvas.create_rectangle(
            x * px_size,
            y * px_size,
            (x + 2) * px_size,
            (y + 2) * px_size,
        )

    def update_canvas_cell(self, color: Literal["black", "white"]) -> None:
        self.canvas.itemconfig(self.figure_id, fill=color)
