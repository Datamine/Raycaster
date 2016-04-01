# John Loeber | March 2016 | Python 2.7.10 | contact@johnloeber.com

from raytracer_plumbing import *

class Cube():
    """
    A cube has:
        * a center : Vector(x,y,z)
        * a rotation around the x-axis: [0,90] degrees
        * a rotation around the y-axis: [0,90] degrees
        * a distance from the center to any vertex: float
        * a surface color: Rgb(r,g,b)
    """
    def __init__(self, center, rot_x, rot_y, distance, color):
        self.center = center
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.distance = distance
        self.color = color
    def vertices(self):
        """
        returns the eight vertices characterizing the cube.
        """
        # pythagorean theorem, noting all edge lengths are equal
        half_edge_length = self.distance / 2**0.5
        vertex_distances = [(half_edge_length, half_edge_length, half_edge_length),
                            (half_edge_length, half_edge_length, -half_edge_length),
                            (half_edge_length, -half_edge_length, half_edge_length),
                            (half_edge_length, -half_edge_length, -half_edge_length),
                            (-half_edge_length, half_edge_length, half_edge_length),
                            (-half_edge_length, half_edge_length, -half_edge_length),
                            (-half_edge_length, -half_edge_length, half_edge_length),
                            (-half_edge_length, -half_edge_length, -half_edge_length)]

        vertex_distances = map(lambda x: Vector(x[0], x[1], x[2]), vertex_distances)
        eight_vertices = map(lambda x: vector_add(x, self.center), vertex_distances)
        return eight_vertices

def rotate(point, x_angle, y_angle):
    """
    x_angle, y_angle are in radians, giving the rotation of the point
    around the origin on the (x,y) and (y,z) axes, respectively.
    """
    x = point.x
    y = point.y
    z = point.z

    radians_x = math.radians(x_angle)
    radians_y = math.radians(y_angle)

    # rotate on the (x,y) axis
    x1 = x
    y1 = y * math.cos(radians_x) - z * math.sin(radians_x)
    z1 = y * math.sin(radians_x) + z * math.cos(radians_x)
    # now rotate on the (y,z) axis. Note: we update our coords to (x,y1,z1) first.
    z2 = z1 * math.cos(radians_y) - x1 * math.sin(radians_y)
    x2 = z1 * math.sin(radians_y) + x1 * math.cos(radians_y)
    y2 = y1
    return Vector(x2,y2,z2)