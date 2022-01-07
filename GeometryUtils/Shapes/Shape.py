from abc import ABCMeta, abstractmethod
from ..Ray import Ray


class Shape(metaclass=ABCMeta):
    @abstractmethod
    def test_intersection(self, ray: Ray):
        pass
