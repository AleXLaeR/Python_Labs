from abc import ABC, abstractmethod
import numpy as np


class GridGenerationStrategy(ABC):
    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height

    @abstractmethod
    def generate(self) -> np.array:
        pass


class RandomGenerationStrategy(GridGenerationStrategy):
    def generate(self) -> np.ndarray:
        grid_size: tuple[int, int] = (self.grid_width, self.grid_height)
        return np.random.randint(low=0, high=2, size=grid_size, dtype=bool)


class EmptyGenerationStrategy(GridGenerationStrategy):
    def generate(self) -> np.ndarray:
        grid_size: tuple[int, int] = (self.grid_width, self.grid_height)
        return np.zeros(grid_size, dtype=bool)
