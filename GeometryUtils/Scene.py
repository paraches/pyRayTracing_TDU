import sys
from .FColor import FColor
from .Ray import Ray


class Scene:
    def __init__(self, shapes, light_sources, ambient_intensity=FColor(0.01)):
        self.shapes = shapes
        self.light_sources = light_sources
        self.ambient_intensity = ambient_intensity

    def test_intersection_with_all(self, ray: Ray, max_dist: float = sys.float_info.max, exit_once_found: bool = False):
        nearest_shape = None
        nearest_intersection = None
        for shape in self.shapes:
            intersection = shape.test_intersection(ray)
            if intersection is not None and intersection.distance < max_dist:
                if nearest_intersection is None or intersection.distance < nearest_intersection.distance:
                    nearest_shape = shape
                    nearest_intersection = intersection
                    if exit_once_found:
                        return nearest_shape, nearest_intersection
        if nearest_intersection is not None:
            return nearest_shape, nearest_intersection
        return None, None
