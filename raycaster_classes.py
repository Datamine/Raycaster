class Vector():
    """
    for handling vectors of length three.
    """
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def l2_norm(self):
        """
        return the l2 norm of the vector.
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def to_unit(self):
        """
        return the unit vector corresponding to the vector.
        """
        magnitude = self.l2_norm()
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
    """
    for handling RGB colors. Should I use a color library instead?
    """
    def __init__(self,r,g,b):
        """
        where r,g,b are integers in [0,1]
        """
        self.r = r
        self.g = g
        self.b = b
    def to_color_tuple(self):
        """
        return a tuple so it can be parsed by the Image library.
        """
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255))
    def scale(self, x):
        """
        scale a color by some scalar, within [0,1] bounds.
        """
        r = max(0, min(1, self.r * x))
        g = max(0, min(1, self.g * x))
        b = max(0, min(1, self.b * x))
        return Color(r,g,b)
    def print_c(self):
        """
        print the color. for debugging.
        """
        print (self.r, self.g, self.b)

class Ray():
    """
    A camera or shadow ray is characterized by
    its origin and direction vectors.
    """
    def __init__(self, origin, direction):
        # where o,d are vectors
        self.origin = origin
        self.direction = direction

class Light():
    """
    direction and color of scene light.
    """
    def __init__(self, direction, color):
        self.direction = direction
        self.color = color

class Sphere():
    """
    defines a sphere in the image.
    """
    def __init__(self, center, radius, color):
        """
        center is a Vector, radius is a float, color is a Color
        """
        self.center = center
        self.radius = radius
        self.color = color

class Hit():
    """
    A hit object is created if a ray strikes the camera,
    otherwise Null. Note: surface_normal is a ray.
    """
    def __init__(self, surface_color, surface_normal):
        self.color = surface_color
        self.normal = surface_normal

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
        
def vector_dot(v1,v2):
    """
    take the dot product of two vectors.
    """
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)

def color_modulate(c1, c2):
    """
    pointwise multiplication of two colors.
    """
    r_component = c1.r * c2.r
    g_component = c1.g * c2.g
    b_component = c1.b * c2.b
    return Color(r_component, g_component, b_component)

def color_add(c1,c2):
    r = c1.r + c2.r
    r = max(0, min(1, r))

    g = c1.g + c2.g
    g = max(0, min(1, g))
    
    b = c1.b + c2.b
    b = max(0, min(1, b))
    return Color(r,g,b)