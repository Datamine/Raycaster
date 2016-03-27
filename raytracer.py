# John Loeber | March 2016 | Python 2.7.10 | contact@johnloeber.com
from raytracer_plumbing import *

# following are configuration options for the scene.

CAMERA_Z = -5
IMG_W = 180
IMG_H = 180

BGCOLOR = Rgb(0.3, 0.6, 1.0)
AMBIENT_LIGHT_COLOR = Rgb(0.2, 0.2, 0.2)

SCENE_LIGHT = Light(Vector(-1,1,-1).to_unit(), Rgb(1,1,1))

# your SHAPE is either "sphere" or "cube". Specify the shape
# accordingly using "SPHERE =" or "CUBE =".
SHAPE = "cube"
SPHERE = Sphere(Vector(0,0,3), 1, Rgb(0.8, 0.8, 0.8))
#SPHERE = Sphere(Vector(1,1,3), 0.5, Rgb(1, 11.0/17, 0))
CUBE = Cube(Vector(0,0,3), 0, 0, 1, Rgb(0.8, 0.8, 0.8))

def shadowed(shape_surface_vector):
    nudge = vector_add(shape_surface_vector, SCENE_LIGHT.direction.scale(0.0001))
    to_the_light = Ray(nudge, SCENE_LIGHT.direction)
    return intersect(to_the_light) != None