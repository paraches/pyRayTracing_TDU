from LightSource import LightSource
from ..PVector import PVector
from ..FColor import FColor
from ..Lighting import Lighting
import sys


class DirectionLightSource(LightSource):
    def __init__(self, direction=PVector(0, -1, 0), intensity=FColor(1.0)):
        self.direction = direction.copy().normalize()
        self.intensity = intensity.copy()

    def __str__(self):
        return f'[direction: {self.direction}, intensity: {self.intensity}]'

    def lighting_at(self, position: PVector):
        direction = self.direction.reverse()
        intensity = self.intensity.copy()
        distance = sys.float_info.max
        result = Lighting(distance, intensity, direction)
        return result
