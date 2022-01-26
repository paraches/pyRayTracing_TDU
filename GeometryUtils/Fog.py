from .FColor import FColor


class Fog:
    def __init__(self, fog_near=10.0, fog_far=30.0, fog_color=FColor(0.5)):
        self.fog_near = fog_near
        self.fog_far = fog_far
        self.fog_color = fog_color
