from .FColor import FColor


class Toon:
    def __init__(self, level=5.0, edge_thickness=0.3, edge_color=FColor()):
        self.level = level
        self.edge_thickness = edge_thickness
        self.edge_color = edge_color

