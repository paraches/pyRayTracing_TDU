from PVector import PVector
from FColor import FColor


class Lighting:
    def __init__(self, distance: float, intensity=FColor(), direction=PVector()):
        self.distance = distance
        self.intensity = intensity
        self.direction = direction

    def __str__(self):
        return f'[distance: {self.distance}, intensity: {self.intensity}, direction: {self.direction}]'
