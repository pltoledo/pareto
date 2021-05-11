from abc import ABC, abstractmethod
import numpy as np

class BaseEvolver(ABC):
    
    @abstractmethod
    def generate_pop(self) -> None:
        """
        Abstract method that is implemented in classes that inherit it
        """
        pass
    @abstractmethod
    def evolve(self) -> None:
        """
        Abstract method that is implemented in classes that inherit it
        """
        pass