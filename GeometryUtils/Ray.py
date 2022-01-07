from PVector import PVector


class Ray:
    def __init__(self, start=PVector(), direction=PVector()):
        self.start = start.copy()
        self.direction = direction.copy()

    def __str__(self):
        return f'[start: {self.start}, direction: {self.direction}]'

    def get_point(self, t: float):
        return PVector.sigma(self.start, t, self.direction)

