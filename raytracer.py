# John Loeber | Python 2.7.10 | March 10, 2016

from PIL import Image
from raycaster_classes import *
import time

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
sphere_object = Sphere(SHAPE_LOC, SPHERE_RAD, SPHERE_COLOR)
################################################################################

def get_position(ray, distance):
	"""
	taking a ray object, determine the position it reaches
	after covering the distance.
	"""
	direction_scaled = ray.direction.scalar_mult(distance)
	position = vector_add(direction_scaled, ray.origin)
	return position

def get_normal(ray, distance, sphere):
    """
    get the surface normal to sphere, given ray and distance.
    """
    position = get_position(ray, distance)
    direction = vector_sub(position, sphere.radius).to_unit()
    return Ray(position, direction)

def detect_collision_sphere(ray, sphere):
    """
    check whether a ray intersects with the sphere.
    return None if there is no collision, otherwise Hit() object.
    test for intersection: https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
    """
    A = vector_sub(ray.origin, sphere.center)
    B = vector_dot(A, ray.direction)
    C = vector_dot(A,A) - sphere.radius**2
    D = B**2 - C
    # creating some leeway for floating-point error
    if D < 0.00001:
        return None
    else:
        closer = max(-B - D**0.5,0)
        further = -B + D**0.5
        t = min(closer, further)
        if t <=0:
            return None
        else:
        	surface_normal = get_normal(ray, t, sphere)
            return Hit(t, sphere.color, surface_normal)

def throw_ray(x,y):
    """
    throw a ray from the camera into the view plane. test for sphere intersection.
    assuming that the z-coord of the view plane is 0.
    """
    origin = CAMERA_LOC
    direction = vector_sub(Vector(x,y,0),line_origin).to_unit()
    ray = Ray(origin, direction)
    return detect_collision(ray, sphere_object)

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
        
# using a timestamp to give images unique identifiers, so it's easier
# to generate lots of images in a batch
im.save(SHAPE.lower() + str(int(time.time())) + ".png", "PNG")