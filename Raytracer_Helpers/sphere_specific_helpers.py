# John Loeber | March 2016 | Python 2.7.10 | contact@johnloeber.com

from raytracer_plumbing import *

class Sphere():
    """
    A sphere has:
        * center: Vector(x,y,z)
        * radius: float
        * color: Rgb()
    """
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color 