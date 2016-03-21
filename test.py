from raytracer_plumbing import *

CUBE = Cube(Vector(0,0,3), 0, 0, 1, Rgb(0.8, 0.8, 0.8))

for vector in CUBE.slabs():
    print "(", vector.x, vector.y, vector.z, ")"
    
