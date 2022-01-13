from .FColor import FColor
from .Ray import Ray


class Scene:
    def __init__(self, shapes, light_sources, ambient_intensity=FColor(0.01)):
        self.shapes = shapes
        self.light_sources = light_sources
        self.ambient_intensity = ambient_intensity

    def test_intersection_with_all(self, ray: Ray):
        intersections = [(shape, shape.test_intersection(ray)) for shape in self.shapes if shape.test_intersection(ray) is not None]
        if len(intersections) == 0:
            return None, None

        nearest_shape, nearest_intersection = min(intersections, key=lambda intersection: intersection[1].distance)

        return nearest_shape, nearest_intersection
