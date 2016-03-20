from PIL import Image
from time import time

class Vec3():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z	
    def l2_norm(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def scale(self,s):
        return Vec3(self.x * s, self.y * s, self.z * s)
    def is_unit(self):
        return 0.999 <= self.l2_norm() <= 1.0001
    def is_zero(self):
        return 0 <= self.l2_norm() <= 0.0001
    def to_unit(self):
        if self.is_zero():
            return Vec3(0,0,0)
        else:
            magnitude = self.l2_norm()
            return Vec3(self.x/magnitude, self.y/magnitude, self.z/magnitude)

class Posn():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class rgb():
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    def to_color(self):
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255))
    def scale(self, x):
        r = max(0, min(1, self.r * x))
        g = max(0, min(1, self.g * x))
        b = max(0, min(1, self.b * x))
        return rgb(r,g,b)

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

class Sphere():
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

class Light():
    def __init__(self, direction, color):
        self.direction = direction
        self.color = color

class Scene():
    def __init__(self, bgcolor, spheres, light, amb):
        self.bgcolor = bgcolor
        self.spheres = spheres
        self.light = light
        self.amb = amb

class Camera():
    def __init__(self, z, img_w, img_h):
        self.z = z
        self.img_w = img_w
        self.img_h = img_h

class Hit():
    def __init__(self, dist, surf_color, surf_normal):
        self.dist = dist
        self.surf_color = surf_color
        self.surf_normal = surf_normal

def vector_add(v1,v2):
    return Vec3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
 
def vector_sub(v1,v2):
    return Vec3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
        
def vector_dot(v1,v2):
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)

def rgb_modulate(c1, c2):
    r_component = c1.r * c2.r
    g_component = c1.g * c2.g
    b_component = c1.b * c2.b
    return rgb(r_component, g_component, b_component)

def rgb_add(c1,c2):
    r = c1.r + c2.r
    r = max(0, min(1, r))

    g = c1.g + c2.g
    g = max(0, min(1, g))
    
    b = c1.b + c2.b
    b = max(0, min(1, b))
    return rgb(r,g,b)

def position(r, t):
    return vector_add(r.origin, r.direction.scale(t))
