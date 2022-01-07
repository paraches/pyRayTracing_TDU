from abc import ABCMeta, abstractmethod
from ..PVector import PVector


class LightSource(metaclass=ABCMeta):
    @abstractmethod
    def lighting_at(self, position: PVector):
        pass
