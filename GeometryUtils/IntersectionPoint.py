from .PVector import PVector


class IntersectionPoint:
    def __init__(self, distance: float = 0, position=PVector(), normal=PVector()):
        self.distance = distance
        self.position = position
        self.normal = normal

    def __str__(self):
        return f'[distance: {self.distance}, position: {self.position}, normal: {self.normal}]'
