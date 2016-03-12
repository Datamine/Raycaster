# John Loeber | Python 2.7.10 | March 10, 2016

from PIL import Image
import time

class Vector():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def norm(self):
        """
        return the l2 norm of the vector.
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def to_unit(self):
        """
        return the unit vector corresponding to the vector.
        """
        magnitude = self.norm()
        return Vector(self.x/magnitude, self.y/magnitude, self.z/magnitude)
    def scalar_mult(self,s):
        """
        multiply the vector by a scalar.
        """
        return Vector(self.x * s, self.y * s, self.z * s)
    def print_v(self):
        """
        print the vector. for debugging.
        """
        print (self.x, self.y, self.z)

class Color():
    # should I be using a color library instead?
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    def to_tuple(self):
        """
        return a tuple so it can be parsed by the Image library.
        """
        return (self.r, self.g, self.b)

def vector_add(v1,v2):
    """
    add two vectors.
    """
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
 
def vector_sub(v1,v2):
    """
    subtract the second vector from the first vector.
    """
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
        
def dot_product(v1,v2):
    """
    take the dot product of two vectors.
    """
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)
      
# Configuration ################################################################

# (Width, Height) of output image
# (0,0) in the top left corner. (w,0) in the top right. (w,h) in the bottom right.
DIMENSIONS = (180,180)
SHAPE_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, 4)
CAMERA_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, -5)
LIGHT_DIR = Vector(0.69,0.75,-0.8).to_unit()
BG_COLOR = Color(128,67,55)
SHADOW_COLOR = Color(0,0,0)

# Shape Specific

SPHERE_RAD = 80
SPHERE_COLOR = Color(40,255,40)
# Shape options: SPHERE | CUBE
SHAPE = "SPHERE"

################################################################################

def get_normal(direction, distance):
    """
    get the surface normal to sphere, if the ray hits it. direction is a unit 
    vector, distance a scalar along the unit vector, from camera to sphere.
    return (normal vector to the surface at collision, coordinate of collision) 
    """
    position = direction.scalar_mult(distance)
    surf_vector = vector_sub(position, SHAPE_LOC)
    return (surf_vector.to_unit(), position)

def detect_collision(line_direction, origin):
    """
    given a unit vector (line_direction) and an origin coordinate,
    check whether that vector intersects with the sphere.
    return None if there is no collision, otherwise a tuple
    (normal vector to the surface at collision, coordinate of collision) 
    """
    sphere_center = SHAPE_LOC
    # test for sphere intersection
    # equation from https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
    eqn = dot_product(line_direction, vector_sub(origin, sphere_center))
    quadratic_part1 = -eqn
    discriminant = eqn**2 - vector_sub(origin,sphere_center).norm()**2 + SPHERE_RAD
    # creating some leeway for floating-point error
    if discriminant < -0.00001:
        # no real solution to the quadratic exists -> no intersection exists.
        return None
    else:
        if -0.00001 <= discriminant <= 0.00001:
            return get_normal(line_direction, quadratic_part1)
        else:
            plus = quadratic_part1+ discriminant**0.5
            minus = quadratic_part1 - discriminant**0.5
            # two intersections: use the closer of the two intersections
            closer = min(plus,minus)
            return get_normal(line_direction, closer)

def throw_ray(x,y):
    """
    throw a ray from the camera into the view plane. test for sphere intersection.
    assuming that the z-coord of the view plane is 0.
    """
    line_origin = CAMERA_LOC
    line_direction = vector_sub(Vector(x,y,0),line_origin).to_unit()
    return detect_collision(line_direction, line_origin)

def check_shadow((normal_vector, position)):
    """
    check whether a point on the sphere is in shadow or not. returns bool.
    to check if it's in shadow, we check whether the light vector intersects
    a sphere before hitting the position.
    """
    # pitfall: "self-shadowing" where we register intersection on the position.
    # so we nudge the position toward the light vector.
    to_the_light = LIGHT_DIR.scalar_mult(-1)
    nudge = to_the_light.scalar_mult(0.001)
    lifted = vector_add(position,nudge)
    in_shadow = detect_collision(to_the_light,position)
    if in_shadow != None:
        in_shadow[0].print_v(), in_shadow[1].print_v()
        return True
    else:
        return False

im = Image.new("RGB", DIMENSIONS, BG_COLOR.to_tuple())

for x in range(DIMENSIONS[0]):
    for y in range(DIMENSIONS[1]):
        surface_normal = throw_ray(x,y)
        if surface_normal!= None:
            in_shadow = check_shadow(surface_normal)
            if in_shadow:
                im.putpixel((x,y),SHADOW_COLOR.to_tuple())
            else:
                im.putpixel((x,y),SPHERE_COLOR.to_tuple())
        
im.save(SHAPE.lower() + str(int(time.time())) + ".png", "PNG")
