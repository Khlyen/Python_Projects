from math import *

def rotate_point(p1, teta, p0):
    return [(p1[0] - p0[0]) * cos(teta) - (p1[1] - p0[1]) * sin(teta) + p0[0], (p1[0] - p0[0]) * sin(teta) + (p1[1] - p0[1]) * cos(teta) + p0[1]]


def angle_btwn_two_vecs(vec1, vec2):
    return acos((vec1[0] * vec2[0] + vec1[1] * vec2[1]) / (
                sqrt(vec1[0] ** 2 + vec1[1] ** 2) * sqrt(vec2[0] ** 2 + vec2[1] ** 2)))


def detect_rect_collision(rect1_x, rect1_y, rect1_w, rect1_h, rect2_x, rect2_y, rect2_w, rect2_h):
    if rect1_x + rect1_w > rect2_x and rect1_x < rect2_x + rect2_w:
        if rect1_y + rect1_h > rect2_y and rect1_y < rect2_y + rect2_h:
            return True
    return False


def normal_of_line(point1, point2):
    #there is two normal vectors first one is (dy, -dx), second one is (-dy, dx)
    dx, dy = point2[0] - point1[0], point2[1] - point1[1]
    return [dy, -dx]

def normalize_vec(vec):
    magnitude = sqrt(vec[0]**2+vec[1]**2)
    return [vec[0]/magnitude, vec[1]/magnitude]


def vector_projection(vec1, vec2):
    """vec1 is projected on vec2"""
    return [vec1[0]*vec2[0]/sqrt(vec2[0]**2+vec2[1]**2),
            vec1[1]*vec2[1]/sqrt(vec2[0]**2+vec2[1]**2)]


def distance(point1, point2):
    return sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)




def point_in_line(line_ps, point, tolerance = 1):
    if abs(distance(line_ps[0],line_ps[1])-(distance(line_ps[0], point) + distance(line_ps[1], point))) < tolerance:
        return True
    return False
            

"""LAST 2 FUNCTIONS ARE NOT WRITTEN BY MYSELF"""
"""LAST 2 FUNCTIONS ARE NOT WRITTEN BY MYSELF"""
"""LAST 2 FUNCTIONS ARE NOT WRITTEN BY MYSELF"""
"""LAST 2 FUNCTIONS ARE NOT WRITTEN BY MYSELF"""

def point_inside_polygon(x, y, poly, include_edges=True):
    '''
    Test if point (x,y) is inside polygon poly.

    poly is N-vertices polygon defined as
    [(x1,y1),...,(xN,yN)] or [(x1,y1),...,(xN,yN),(x1,y1)]
    (function works fine in both cases)

    Geometrical idea: point is inside polygon if horisontal beam
    to the right from point crosses polygon even number of times.
    Works fine for non-convex polygons.
    '''
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if p1y == p2y:
            if y == p1y:
                if min(p1x, p2x) <= x <= max(p1x, p2x):
                    # point is on horisontal edge
                    inside = include_edges
                    break
                elif x < min(p1x, p2x):  # point is to the left from current edge
                    inside = not inside
        else:  # p1y!= p2y
            if min(p1y, p2y) <= y <= max(p1y, p2y):
                xinters = (y - p1y) * (p2x - p1x) / float(p2y - p1y) + p1x

                if x == xinters:  # point is right on the edge
                    inside = include_edges
                    break

                if x < xinters:  # point is to the left from current edge
                    inside = not inside

        p1x, p1y = p2x, p2y

    return inside


def do_polygons_intersect(a, b):
    """
 * Helper function to determine whether there is an intersection between the two polygons described
 * by the lists of vertices. Uses the Separating Axis Theorem
 *
 * @param a an ndarray of connected points [[x_1, y_1], [x_2, y_2],...] that form a closed polygon
 * @param b an ndarray of connected points [[x_1, y_1], [x_2, y_2],...] that form a closed polygon
 * @return true if there is any intersection between the 2 polygons, false otherwise
    """

    polygons = [a, b];
    minA, maxA, projected, i, i1, j, minB, maxB = None, None, None, None, None, None, None, None

    for i in range(len(polygons)):

        # for each polygon, look at each edge of the polygon, and determine if it separates
        # the two shapes
        polygon = polygons[i];
        for i1 in range(len(polygon)):

            # grab 2 vertices to create an edge
            i2 = (i1 + 1) % len(polygon);
            p1 = polygon[i1];
            p2 = polygon[i2];

            # find the line perpendicular to this edge
            normal = { 'x': p2[1] - p1[1], 'y': p1[0] - p2[0] };

            minA, maxA = None, None
            # for each vertex in the first shape, project it onto the line perpendicular to the edge
            # and keep track of the min and max of these values
            for j in range(len(a)):
                projected = normal['x'] * a[j][0] + normal['y'] * a[j][1];
                if (minA is None) or (projected < minA):
                    minA = projected

                if (maxA is None) or (projected > maxA):
                    maxA = projected

            # for each vertex in the second shape, project it onto the line perpendicular to the edge
            # and keep track of the min and max of these values
            minB, maxB = None, None
            for j in range(len(b)):
                projected = normal['x'] * b[j][0] + normal['y'] * b[j][1]
                if (minB is None) or (projected < minB):
                    minB = projected

                if (maxB is None) or (projected > maxB):
                    maxB = projected

            # if there is no overlap between the projects, the edge we are looking at separates the two
            # polygons, and we know there is no overlap
            if (maxA < minB) or (maxB < minA):
               # print("polygons don't intersect!")
                return False;

    return True

