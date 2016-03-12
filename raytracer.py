# John Loeber | Python 2.7.10 | March 10, 2016

from PIL import Image
import time

class Vector():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def norm(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def unit_vector(self):
        magnitude = self.norm()
        return Vector(self.x/magnitude, self.y/magnitude, self.z/magnitude)
    def scalar_mult(self,s):
        return Vector(self.x * s, self.y * s, self.z * s)

class Color():
    # should I be using a color library instead?
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    def tocolor(self):
        return (self.r, self.g, self.b)

def vector_add(v1,v2):
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
 
def vector_sub(v1,v2):
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
        
def dot_product(v1,v2):
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)
      
# Configuration ################################################################

# (Width, Height) of output image
# (0,0) in the top left corner. (w,0) in the top right. (w,h) in the bottom right.
DIMENSIONS = (480,480)
SHAPE_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, 0)
CAMERA_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, -5)
# LIGHT_DIR = Vector(-1,1,1)
BG_COLOR = Color(128,67,55)

# Shape Specific

SPHERE_RAD = 20
SPHERE_COLOR = Color(40,255,40)
# Shape options: SPHERE | CUBE
SHAPE = "SPHERE"

################################################################################

def get_normal(direction, distance):
    """
    get the surface normal to a sphere at a given point
    """
    position = direction.scalar_mult(distance)
    surf_vector = vector_sub(position, SHAPE_LOC)
    return surf_vector.unit_vector()

def throw_ray(x,y):
    """
    throw a ray from the camera into the view plane. test for sphere intersection.
    equation from https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
    assuming that the z-coord of the view plane is 0.
    returns (d,w)
        d = distance along the line at which it intersects a sphere
        w = normal vector to the surface of the sphere
    """
    line_origin = CAMERA_LOC
    sphere_center = SHAPE_LOC
    line_direction = vector_sub(Vector(x,y,0),line_origin).unit_vector()
    loc = dot_product(line_direction, vector_sub(line_origin, sphere_center))
    d_part1 = -loc
    discriminant = loc**2 - vector_sub(line_origin,sphere_center).norm()**2 + SPHERE_RAD
    # creating some leeway for floating-point error
    if discriminant < -0.00001:
        # no real solution to the quadratic exists -> no intersection exists.
        return None
    else:
        elif -0.00001 <= discriminant <= 0.00001:
            position = line_direction.scalar_mult(d_part1)
            surf_vector = vector_sub(position,sphere_center)
            surface_normal = surf_vector.unit_vector()
            return d_part1
        else:
            plus = d_part1 + discriminant**0.5
            minus = d_part1 - discriminant**0.5
            # two intersections: use the closer of the two intersections
            closer = min(plus,minus)
            normal = get_normal(line_direction, closer)
            return

im = Image.new("RGB", DIMENSIONS, BG_COLOR.tocolor())

for x in range(DIMENSIONS[0]):
    for y in range(DIMENSIONS[1]):
        color = throw_ray(x,y)
        if color!= None:
            im.putpixel((x,y),(255,255,0))
        
im.save(SHAPE.lower() + str(int(time.time())) + ".png", "PNG")
