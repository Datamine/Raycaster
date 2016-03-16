class Vector():
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
    # should I be using a color library instead?
    def __init__(self,r,g,b):
        # where r,g,b are integers in [0,255]
        self.r = r
        self.g = g
        self.b = b
    def to_tuple(self):
        """
        return a tuple so it can be parsed by the Image library.
        """
        return (self.r, self.g, self.b)

class Ray():
    def __init__(self, origin, direction):
        # where o,d are vectors
        self.origin = origin
        self.direction = direction

class Sphere():
    def __init__(self, center, radius, color):
        # c is a vector, r is a float, s is a color
        self.center = center
        self.radius = radius
        self.color = color

class Hit():
    """
    A hit object is created if a ray strikes the camera,
    otherwise Null. Note: surface_normal is a ray.
    """
    def __init__(self, distance, surface_color, surface_normal):
        self.distance = distance
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
      