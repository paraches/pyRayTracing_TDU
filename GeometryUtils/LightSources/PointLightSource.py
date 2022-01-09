from .LightSource import LightSource
from ..PVector import PVector
from ..FColor import FColor
from ..Lighting import Lighting


class PointLightSource(LightSource):
    def __init__(self, position=PVector(), intensity=FColor(1.0)):
        self.position = position.copy()
        self.intensity = intensity.copy()

    def __str__(self):
        return f'[position: {self.position}, intensity: {self.intensity}]'

    def lighting_at(self, position: PVector):
        direction = self.position.sub(position)
        distance = direction.mag()
        result = Lighting(distance, self.intensity.copy(), direction.normalize())
        return result
