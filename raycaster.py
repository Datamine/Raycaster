# John Loeber | Python 2.7.10 | March 10, 2016

from PIL import Image
import time
import raycaster_classes


# Configuration ################################################################

# (Width, Height) of output image
# (0,0) in the top left corner. (w,0) in the top right. (w,h) in the bottom right.
DIMENSIONS = (500,500)
SHAPE_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, 4)
CAMERA_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, -5)
LIGHT_DIR = Vector(1,-1,-1).to_unit()
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
    position = vector_add(direction.scalar_mult(distance), CAMERA_LOC)
    surf_vector = vector_sub(position, SHAPE_LOC)
    return surf_vector.to_unit(), position

def detect_collision(line_direction, origin):
    """
    given a unit vector (line_direction) and an origin coordinate,
    check whether that vector intersects with the sphere.
    return None if there is no collision, otherwise a tuple
    (normal vector to the surface at collision, coordinate of collision) 
    """
    ro = origin
    rd = line_direction
    sc = SHAPE_LOC
    sr = SPHERE_RAD
    A = vector_sub(ro,sc)
    B = vector_dot(A, rd)
    C = vector_dot(A,A) - sr**2
    D = B**2 - C
    """
    sphere_center = SHAPE_LOC
    # test for sphere intersection
    # equation from https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
    eqn = vector_dot(line_direction, vector_sub(origin, sphere_center))
    quadratic_part1 = -eqn
    discriminant = eqn**2 - vector_sub(origin,sphere_center).norm()**2 + SPHERE_RAD
    # creating some leeway for floating-point error
    # i'll need to add some comments here...
    """
    if D < 0.00001:
        return None, None
    else:
        closer = max(-B - D**0.5,0)
        further = -B + D**0.5
        t = min(closer, further)
        if t <=0:
            return None, None
        else:
            return get_normal(line_direction, t)
    """
    if discriminant < 0.00001:
        # no real solution to the quadratic exists -> no intersection exists.
        return None,None
    else:
        plus = quadratic_part1+ discriminant**0.5
        minus = quadratic_part1 - discriminant**0.5
        closer = min(plus,minus)
        if closer < 0.00001:
            return None, None
        else:
         return get_normal(line_direction, closer)
    """

def throw_ray(x,y):
    """
    throw a ray from the camera into the view plane. test for sphere intersection.
    assuming that the z-coord of the view plane is 0.
    """
    line_origin = CAMERA_LOC
    line_direction = vector_sub(Vector(x,y,0),line_origin).to_unit()
    return detect_collision(line_direction, line_origin)

def check_shadow(normal_vector, position):
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
    if in_shadow == (None, None):
        return False
    else:
        return True

def lighting(in_shadow,surface_normal):
    """
    in_shadow: bool. surface_normal: vector.
    """
    diffuse = max(0, vector_dot(surface_normal, LIGHT_DIR))
    
im = Image.new("RGB", DIMENSIONS, BG_COLOR.to_tuple())

for x in range(DIMENSIONS[0]):
    for y in range(DIMENSIONS[1]):
        surface_normal, position = throw_ray(x,y)
        if (surface_normal, position) != (None, None):
            in_shadow = check_shadow(surface_normal, position)
            #color = lighting(in_shadow,surface_normal)
            if in_shadow:
                im.putpixel((x,y),(0,0,0))
            else:    
                im.putpixel((x,y),(255,255,255))
        
im.save(SHAPE.lower() + str(int(time.time())) + ".png", "PNG")
