from .FColor import FColor


class Material:
    def __init__(self, ambient_factor=FColor(), diffuse_factor=FColor(), specular_factor=FColor(), shininess=float(0),
                 use_perfect_reflectance=False, catadioptric_factor=FColor()):
        self.ambient_factor = ambient_factor
        self.diffuse_factor = diffuse_factor
        self.specular_factor = specular_factor
        self.shininess = shininess
        self.use_perfect_reflectance = use_perfect_reflectance
        self.catadioptric_factor = catadioptric_factor
