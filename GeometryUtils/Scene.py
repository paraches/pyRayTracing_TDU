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
                 camera=Camera(), width: int = 512, height: int = 512):
        self.shapes = shapes
        self.light_sources = light_sources
        self.ambient_intensity = ambient_intensity
        self.global_refraction_index = global_refraction_index
        self.camera = camera
        self.width = width
        self.height = height

        # EX-2
        # df = pt - pe, normalize
        df = self.camera.look_at.sub(self.camera.position).normalize()
        # dx = ey x df, ty = (0, 1, )
        self.dx = PVector(0, 1, 0).cross(df)
        # dy = df x dx
        self.dy = df.cross(self.dx)
        # pm = pe +mdf
        self.pm = self.camera.position.add(df.mult(self.camera.screen_distance))

        # EX-3
        self.screen_width = 2.0
        self.ws = self.screen_width if width >= height else self.screen_width * width / height
        self.hs = self.screen_width * height / width if width > height else self.screen_width

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
        # fx = Wsxs / (W - 1) - Ws / 2
        fx = (self.ws * float(x)) / (self.width - 1) - (self.ws / self.screen_width)
        # fy = -Hsys / (H - 1) + Hs / 2
        fy = -(self.hs * float(y)) / (self.height - 1) + (self.hs / self.screen_width)
        fxdx = self.dx.mult(fx)
        fxdy = self.dy.mult(fy)
        # pw = pm + fxdx + fydy
        return self.pm.add(fxdx).add(fxdy)
