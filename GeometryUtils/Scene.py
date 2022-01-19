import sys
from .FColor import FColor
from .Ray import Ray
from .PVector import PVector


class Camera:
    def __init__(self, position=PVector(0, 0, -5), look_at=PVector(), screen_distance: float = 5):
        self.position = position
        self.look_at = look_at
        self.screen_distance = screen_distance


class Scene:
    def __init__(self, shapes, light_sources, ambient_intensity=FColor(0.01), global_refraction_index=1.000293,
                 camera=Camera()):
        self.shapes = shapes
        self.light_sources = light_sources
        self.ambient_intensity = ambient_intensity
        self.global_refraction_index = global_refraction_index
        self.camera = camera

        # EX-2
        # df = pt - pe, normalize
        df = self.camera.look_at.sub(self.camera.position).normalize()
        # dx = ey x df, ty = (0, 1, )
        self.dx = PVector(0, 1, 0).cross(df)
        # dy = df x dx
        self.dy = df.cross(self.dx)
        # pm = pe +mdf
        self.pm = self.camera.position.add(df.mult(self.camera.screen_distance))

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

    # pw = pe + mdf + fxdx + fydy
    def world_from_screen_coordinate(self, x: int, y: int):
        # fx = 2xs / (W - 1) - 1.0
        fx = (2 * float(x)) / (512 - 1) - 1.0
        # fy = -2yx / (H - 1) + 1.0
        fy = (-2 * float(y)) / (512 - 1) + 1.0
        fxdx = self.dx.mult(fx)
        fxdy = self.dy.mult(fy)
        # pw = pm + fxdx + fydy
        return self.pm.add(fxdx).add(fxdy)
