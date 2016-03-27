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
    def slabs(self):
        """
        returns the six slabs characterizing a cube.
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

        eight_vertices = map(lambda x: vector_add(x, self.center), rotated_vertex_distances)
        """
        possible_edges = list(itertools.combinations(eight_vertices, 2))
        distances = [((a,b),vector_sub(a,b).l2_norm()) for (a,b) in possible_edges]
        twelve_smallest = sorted(distances, key = lambda x: x[1], reverse=True)[:12]
        twelve_edges = [x[0] for x in twelve_smallest]
        twelve_vectors = [vector_sub(a,b) if a.l2_norm() > b.l2_norm() else vector_sub(b,a) for (a,b) in twelve_edges]
        twelve_unit_vectors = map(lambda x: x.to_unit(), twelve_vectors)
        """
        """
        xy = map(lambda v: Vector(v.x,v.y,0), eight_vertices)
        yz = map(lambda v: Vector(0,v.y,v.z), eight_vertices)
        xz = map(lambda v: Vector(v.x,0,v.z), eight_vertices)
        uniques = []
        # iterate over all vectors
        for i in eight_vertices:
            # for any vector, compare it only to the ones that it hasn't been compared to yet
            for u in uniques:
                if vector_equal(i,u):
                    break
            else:
                uniques.append(i)
        """
        return eight_vertices

def rotate(point, x_angle, y_angle):
    """
    x_angle, y_angle are in radians, giving the rotation of the point
    around the origin on the (x,y) and (y,z) axes, respectively.
    """
    x = point.x
    y = point.y
    z = point.z

    # rotate on the (x,y) axis
    x1 = x
    y1 = y * math.cos(radians_x) - z * math.sin(radians_x)
    z1 = y * math.sin(radians_x) + z * math.cos(radians_x)
    # now rotate on the (y,z) axis. Note: we update our coords to (x,y1,z1) first.
    z2 = z1 * math.cos(radians_y) - x1 * math.sin(radians_y)
    x2 = z1 * math.sin(radians_y) + x1 * math.cos(radians_y)
    y2 = y1
    return Vector(x2,y2,z2)