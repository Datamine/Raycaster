# John Loeber | March 2016 | Python 2.7.10 | contact@johnloeber.com

from cube_specific_helpers import *

CAMERA_Z = -5
IMG_W = 180
IMG_H = 180

BGCOLOR = Rgb(0.3, 0.6, 1.0)
AMBIENT_LIGHT_COLOR = Rgb(0.2, 0.2, 0.2)

SCENE_LIGHT = Light(Vector(-1,1,-1).to_unit(), Rgb(1,1,1))

CUBE = Cube(Vector(0,0,3), 0, 0, 1, Rgb(0.8, 0.8, 0.8))

def intersect_cube(ray):
    """
    rotating a cube and handling the raycasting geometry can get tricky.
    it's easier to equivalently rotate the camera and light source around 
    the cube, such that the cube becomes an axis-aligned bounding box,
    which it is easy to compute intersections for.
    """
    # note that this is not actually the correct rotation
    radians_x = math.radians(CUBE.rot_x)
    radians_y = math.radians(CUBE.rot_y)
    # ray.origin is the position of the camera 
    new_camera_loc = rotate(ray.origin, radians_x, radians_y)
    new_light_dir = rotate(SCENE_LIGHT.direction, radians_x, radians_y)
    # change the global lighting. not passing lighting as an arg was a bad
    # decision on my part -- need to fix
    SCENE_LIGHT = Light(new_light_dir, SCENE_LIGHT.color)

    edges = CUBE.vertices()
    t_near = float("-inf")
    t_far = float("inf")
    for edge in edges:
        pass
        # check if parallel
        # if ray.direction == 
    return

def shadowed(shape_surface_vector):
    nudge = vector_add(shape_surface_vector, SCENE_LIGHT.direction.scale(0.0001))
    to_the_light = Ray(nudge, SCENE_LIGHT.direction)
    return intersect(to_the_light) != None

def lighting_cube(ray, hit):
    return

im = Image.new("RGB", (IMG_W, IMG_H), BGCOLOR.to_color())

for x in range(IMG_W):
    for y in range(IMG_H):
        position = Posn(x,y)
        logical_position = logical_loc(position, IMG_W, IMG_H)

        ray_origin = Vector(0,0,CAMERA_Z)
        ray_vector = vector_sub(logical_position, ray_origin).to_unit()
        cast_ray = Ray(ray_origin, ray_vector)
        
        hit = intersect(cast_ray)
        if hit != None:
            color = lighting(cast_ray, hit)
            truecolor = color.to_color()
            im.putpixel((x,y),truecolor)

im.save("sphere" + str(int(time())) + ".png", "PNG")
