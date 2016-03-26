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

def intersect_sphere(ray):
    A = vector_sub(ray.origin, SPHERE.center)
    B = vector_dot(A, ray.direction)
    C = vector_dot(A,A) - SPHERE.radius**2
    # max with zero because for t, we can't raise negative D to fractional power.
    D = max(0, B**2 - C)
    t = (-B) - D**0.5
    if (D > 0) and (t > 0):
        normal = vector_sub(ray.position(t), SPHERE.center).to_unit()
        return Hit(t, SPHERE.color, normal)
    else:
        return None

def intersect_cube(ray):
    edges = CUBE.vertices()
    t_near = float("-inf")
    t_far = float("inf")
    for edge in edges:
        pass
        # check if parallel
        # if ray.direction == 
    return

def intersect(ray):
    if SHAPE=="sphere":
        return intersect_sphere(ray)
    else:
        return intersect_cube(ray)

def shadowed(shape_surface_vector):
    nudge = vector_add(shape_surface_vector, SCENE_LIGHT.direction.scale(0.0001))
    to_the_light = Ray(nudge, SCENE_LIGHT.direction)
    return intersect(to_the_light) != None

def lighting_sphere(ray, hit):
    if shadowed(ray.position(hit.dist)):
        return Rgb_modulate(hit.surf_color, AMBIENT_LIGHT_COLOR)
    else:
        scale = max(0, vector_dot(hit.surf_normal, SCENE_LIGHT.direction))
        product = Rgb_add(SCENE_LIGHT.color.scale(scale), AMBIENT_LIGHT_COLOR)
        return Rgb_modulate(hit.surf_color, product)

def lighting_cube(ray, hit):
    return

def lighting(ray, hit):
    if SHAPE=="sphere":
        return lighting_sphere(ray, hit)
    else:
        return lighting_cube(ray, hit)

im = Image.new("RGB", (IMG_W, IMG_H), BGCOLOR.to_color())

for x in range(IMG_W):
    for y in range(IMG_H):
        position = Posn(x,y)
        logical_position = logical_loc(position, IMG_W, IMG_H)

        ray_origin = origin = Vector(0,0,CAMERA_Z)
        ray_vector = vector_sub(logical_position, ray_origin).to_unit()
        cast_ray = Ray(ray_origin, ray_vector)
        
        hit = intersect(cast_ray)
        if hit != None:
            color = lighting(cast_ray, hit)
            truecolor = color.to_color()
            im.putpixel((x,y),truecolor)

im.save("sphere" + str(int(time())) + ".png", "PNG")
