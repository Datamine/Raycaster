from PIL import Image
from time import time
import math

# This file contains classes for objects used in raycaster.py,
# and helper functions for dealing with those objects.
# All code related to actually determining locations of intersections
# and plotting points is in raycaster.py.

class Vector():
    """
    for handling vectors of length three.
    that is: for handling positions in the logical view.
    """
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z  
    def l2_norm(self):
        """
        return the l2 (euclidean) norm of the vector.
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def scale(self,s):
        """
        multiply the vector by a scalar.
        """
        return Vector(self.x * s, self.y * s, self.z * s)
    def is_zero(self):
        """
        check if the vector is the zero vector.
        """
        return -0.0001 <= self.l2_norm() <= 0.0001
    def to_unit(self):
        """
        normalize the vector, i.e. scale it to a unit vector.
        """
        if self.is_zero():
            return Vector(0,0,0)
        else:
            magnitude = self.l2_norm()
            return Vector(self.x/magnitude, self.y/magnitude, self.z/magnitude)

class Posn():
    """
    for handling vectors of length two.
    that is: for handling positions in the image.
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Rgb():
    """
    for handling colors. note that r,g,b are all in [0,1].
    we scale them to [0,255] only to place the colored pixel.
    """
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    def to_color(self):
        """
        scales a Rgb() to an (r,g,b) tuple that the python imaging
        library can use in putpixel().
        """
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255))
    def scale(self, x):
        """
        multiply an Rgb() by a scalar. Capped in [0,1].
        """
        r = max(0, min(1, self.r * x))
        g = max(0, min(1, self.g * x))
        b = max(0, min(1, self.b * x))
        return Rgb(r,g,b)

class Ray():
    """
    For handling rays in the image. A ray has an origin
    and a direction, both are of type Vector(x,y,z).
    """
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    def position(self, t):
        """
        Calculate the resulting position from moving t "timesteps"
        along the vector.
        """
        return vector_add(self.origin, self.direction.scale(t))

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

class Cube():
    """
    A cube has:
        * a center : Vector(x,y,z)
        * a rotation around the x-axis: [0,90] degrees
        * a rotation around the y-axis: [0,90] degrees
        * a distance from the center to any vertex: float
    """
    def __init__(self, center, rot_x, rot_y, distance):
        self.center = center
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.distance = distance
    def vertices(self):
        """
        returns the eight vertices characterizing a cube.
        We first locate all the eight vertices, then we use trigonometry
        to figure out by how much to change their positions.
        """
        radians_x = math.radians(rot_x)
        radians_y = math.radians(rot_y)
        # pythagorean theorem, noting all edge lengths are equal
        half_edge_length = distance / 2**0.5
        vertex_distances = [(half_edge_length, half_edge_length, half_edge_length),
                            (half_edge_length, half_edge_length, -half_edge_length),
                            (half_edge_length, -half_edge_length, half_edge_length),
                            (half_edge_length, -half_edge_length, -half_edge_length),
                            (-half_edge_length, half_edge_length, half_edge_length),
                            (-half_edge_length, half_edge_length, -half_edge_length),
                            (-half_edge_length, -half_edge_length, half_edge_length),
                            (-half_edge_length, -half_edge_length, -half_edge_length)]
        rotated_vertex_distances = []
        for (x,y,z) in vertex_distances:
            # rotate around the x-axis first
            x1 = x
            y1 = y * math.cos(radians_x) - z * math.sin(radians_x)
            z1 = y * math.sin(radians_x) + z * math.cos(radians_x)
            # now rotate around the y-axis. Note: we update our coords to (x,y1,z1) first.
            z2 = z1 * math.cos(radians_y) - x1 * math.sin(radians_y)
            x2 = z1 * math.sin(radians_y) + x2 * math.cos(radians_y)
            y2 = y1
            rotated_vertex_distances.append((x2))

        eight_vertices = map(lambda x: add_vector(self.center, x), vertex_distances)
        distance * 

class Light():
    """
    The light has two components:
        * direction: Vector(x,y,z)
        * color: Rgb()
    Note that direction is a vector pointing *at* the light,
    not coming from the light.
    """
    def __init__(self, direction, color):
        self.direction = direction
        self.color = color

class Hit():
    """
    If a ray hits a shape, then a Hit() object is created.
    (If not, we return None in intersect().)
    A hit contains:
        * dist: number of "timesteps" along the vector to the shape.
        * color: surface color of the object it hits.
        * surf_normal : unit normal vector to the surface of the shape.
    """
    def __init__(self, dist, surf_color, surf_normal):
        self.dist = dist
        self.surf_color = surf_color
        self.surf_normal = surf_normal
        
def vector_add(v1,v2):
    """
    add two vectors.
    """
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
 
def vector_sub(v1,v2):
    """
    subtract the second vector from the first.
    """
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
        
def vector_dot(v1,v2):
    """
    take the dot product of two vectors.
    """
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)

def Rgb_modulate(c1, c2):
    """
    pointwise multiplication of two Rgbs.
    """
    r_component = c1.r * c2.r
    g_component = c1.g * c2.g
    b_component = c1.b * c2.b
    return Rgb(r_component, g_component, b_component)

def Rgb_add(c1,c2):
    """
    add two Rgbs. each coordinate is capped in [0,1].
    """
    r = c1.r + c2.r
    r = max(0, min(1, r))

    g = c1.g + c2.g
    g = max(0, min(1, g))
    
    b = c1.b + c2.b
    b = max(0, min(1, b))
    return Rgb(r,g,b)

def logical_loc(position, width, height):
    """
    determine the coordinate (Vector(x,y,z)) in the logical view
    corresponding to a position (Posn(x,y)) in the physical image.
    width, height are the width and height of the image in px.
    
    Recall that the logical plane has a (0,0,0) as its origin,
    whereas the physical plane has (0,0) in the top-left corner and
    (width, height) in the bottom right.
    """
    # ratio between widths of the logical and physical view
    rw = 2.0 / width
    rh = 2.0 / height
    # logical width or height of a pixel in the physical view if:
    # width >= height
    rw2 = rw / 2.0
    # height >= width
    rh2 = rh / 2.0
    if width == height:
        if position.x == 0:
            x = rw2 - 1
        else:
            x = (-1) + (position.x * rw) + rw2

        if position.y == 0:
            y = 1 - rh2
        else:
            y = 1 - (position.y * rh) - rh2

    # i'm not sure why you would want a non-square image, but it's supported.
    if width > height:
        if position.x == 0:
            x = rw2 - 1
        else:
            x = (-1) + (position.x * rw) + rw2

        if position.y == 0:
            y = (height / float(width)) - rw2
        else:
            y = (height / float(width)) - (position.y * rw) - rw2
    
    if width < height:
        if position.x == 0:
            x = rh2 - (width / float(height))
        else:
            x = (position.x * rh) - (width / float(height)) + rh2
    
        if position.y == 0:
            y = 1 - rh2
        else:
            y = 1 - (position.y * rh) - rh2

    return Vector(x,y,0)