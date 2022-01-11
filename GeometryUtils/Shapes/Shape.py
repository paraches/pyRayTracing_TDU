from abc import ABC, abstractmethod
from ..Ray import Ray
from ..Material import Material


class Shape(ABC):
    def __init__(self, material=Material()):
        self.material = material

    @abstractmethod
    def test_intersection(self, ray: Ray):
        pass
