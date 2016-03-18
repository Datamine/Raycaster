# John Loeber | Python 2.7.10 | March 10, 2016

from PIL import Image
from raycaster_classes import *
import time

# Configuration ################################################################

# (Width, Height) of output image
# (0,0) in the top left corner. (w,0) in the top right. (w,h) in the bottom right.
DIMENSIONS = (250,250)

SHAPE_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, 0)
CAMERA_LOC = Vector(DIMENSIONS[0]/2, DIMENSIONS[1]/2, -5)
LIGHT_DIR = Vector(3,0.3,-5).to_unit()
LIGHT_COLOR = Color(255,255,255)
BG_COLOR = Color(128,67,55)

# Shape Specific
SPHERE_RAD = 4.995
SPHERE_COLOR = Color(0,100,255)
sphere_object = Sphere(SHAPE_LOC, SPHERE_RAD, SPHERE_COLOR)

SHAPE = "SPHERE"

ambient_light = Light(LIGHT_DIR, LIGHT_COLOR)
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
    direction = vector_sub(position, sphere.center).to_unit()
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
        #closer = -B - D**0.5
        further = -B - D**0.5
        t = further
        if t <=0:
            return None
        else:
            surface_normal = get_normal(ray, t, sphere)
            return Hit(sphere.color, surface_normal)

def throw_ray(x,y):
    """
    throw a ray from the camera into the view plane. test for sphere intersection.
    assuming that the z-coord of the view plane is 0.
    """
    origin = CAMERA_LOC
    direction = vector_sub(Vector(x,y,0),origin).to_unit()
    ray = Ray(origin, direction)
    return detect_collision_sphere(ray, sphere_object)

def check_shadow(hit_object):
    """
    Bool: whether a point on the sphere is in shadow or not.
    (Check whether light intersects the object before the point.)
    """
    # pitfall: "self-shadowing" where we register intersection on the position.
    # so we nudge the position toward the light vector.
    to_the_light = ambient_light.direction.scalar_mult(-1)
    nudge = to_the_light.scalar_mult(0.001)
    lifted_origin = vector_add(hit_object.normal.origin, nudge)
    outgoing_ray = Ray(lifted_origin, to_the_light)
    in_shadow = detect_collision_sphere(outgoing_ray, sphere_object)
    if in_shadow == None:
        return False
    else:
        return True

def lighting(in_shadow, hit_object):
    """
    determines the overall lighting (and thus color) at a given hit.
    """
    if in_shadow:
        modulated_light = color_modulate(hit_object.color, ambient_light.color)
        print "here"
        return hit_object.color.to_tuple()
    else:
        scaling_factor = max(0, vector_dot(hit_object.normal.direction.to_unit(), ambient_light.direction.to_unit()))
        diffuse_light = ambient_light.color.scale(scaling_factor)
        sum_light_colors = color_add(ambient_light.color, diffuse_light)
        modulated_light = color_modulate(hit_object.color, sum_light_colors)
    return modulated_light.to_tuple()

im = Image.new("RGB", DIMENSIONS, BG_COLOR.to_tuple())

for x in range(DIMENSIONS[0]):
    for y in range(DIMENSIONS[1]):
        hit = throw_ray(x,y)
        if hit != None:
            in_shadow = check_shadow(hit)
            color = lighting(in_shadow,hit)
            im.putpixel((x,y),color)

# using a timestamp to give images unique identifiers, so it's easier
# to generate lots of images in a batch
im.save(SHAPE.lower() + str(int(time.time())) + ".png", "PNG")