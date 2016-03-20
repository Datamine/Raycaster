from raycaster_rewrite import *

c = Camera(-2, 7,12)
p = Posn(3,4)

v = logical_loc(c,p)
print v.x, v.y, v.z
