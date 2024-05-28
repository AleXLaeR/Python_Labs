from tkinter import Tk as Window

from grid_templates import RandomGenerationStrategy
from game import GameOfLife


def main():
    grid_size = {"grid_width": 80, "grid_height": 50}
    board_template = RandomGenerationStrategy(**grid_size)

    GameOfLife(root := Window(), grid_template=board_template, **grid_size, upd_interval=30).run()
    root.eval("tk::PlaceWindow . center")
    root.mainloop()


if __name__ == "__main__":
    main()
