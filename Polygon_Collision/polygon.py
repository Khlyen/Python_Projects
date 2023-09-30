import pygame.draw
from math_calculations import rotate_point
from math import pi, sin, cos, tan
from random import choice


class Polygon():
    """General polygon class for regular(equilateral and equiangular) convex polygons"""

    polygons = [] # list of every polygon object created from this class
    max_update_time = 50

    def __init__(self, n, x, y, teta, color, radius, density, factor1, factor2):
        """
        :param n: number of points polygon have
        :param x: starting x coordinate of center
        :param y: starting y coordinate of center
        :param teta: starting angle of polygon (positive means clockwise) [unit:radian]
        :param color: color of polygon (r,g,b)
        :param radius: radius from center to any one of the points
        :param density: density of polygon
        :param factor1: random velocity division factor (higher values mean smaller random velocities)
        :param factor2: polygon update number factor (in each frame polygon is updated maxvelocity/factor2 times)
        """
        self.x = x # x coordinate of center point
        self.y  = y # y coordinate of center point
        self.teta = teta
        self.color = color
        self.n = n  # number of points polygon have
        self.mass = None
        self.type = "polygon"
        self.factor2 = factor2
        self.radius = radius # distance between center of polygon and any of polygons points
        self.velocity_x = None
        self.velocity_y = None
        self.angular_velocity = None
        self.moment_of_inertia = None  # mass moment of inertia
        self.relative_points = [] # polygon point coordinates relative to the center
        self.points = []
        self.total_update_time = None # number of times to be updated per frame
                                      # has high values for polygons moving fast and vice versa
                                      # this value might have different values per frame because it changes after collisions
        self.update_time_remaining = None # remaining update times per frame
        self.polygons.append(self)
        self._calculate_attributes(density)
        self._create_random_velocities(factor1, factor2)
        self._create_relative_points()

    def _calculate_attributes(self, density):
        length = 2*self.radius*sin(pi/self.n)
        area = 1/4*length**2*self.n*1/tan((pi/self.n))
        self.mass = area*density
        self.moment_of_inertia = self.mass*length**2/24*(1+3*(1/tan(pi/self.n))**2)

    def _create_random_velocities(self, factor1, factor2):
        values = list(range(-100, 101))
        values.remove(0)
        self.velocity_x = choice(values)/factor1
        self.velocity_y = choice(values)/factor1
        self.angular_velocity = choice(values)/(factor1*100)
        
        self.total_update_time = min(max(self.angular_velocity/factor2, self.velocity_x/factor2, self.velocity_y/factor2),
                                         self.max_update_time)
        self.update_time_remaining = self.total_update_time


    def _create_relative_points(self):
        """
            First relative point is created above center point + starting teta.
            This defines their starting orientation.
            Points are created in clockwise direction.
        """
        delta_angle = 2*pi/self.n
        angle = self.teta
        for i in range(self.n):
            pointx = self.radius*sin(angle)
            pointy = self.radius*cos(angle)
            self.relative_points.append([pointx, pointy])
            angle += delta_angle
            self.points.append([(self.x + self.relative_points[i][0]),
                               (self.y + self.relative_points[i][1])])


    def update_self(self, offset_x, offset_y):
        if self.update_time_remaining > 0:
            self.update_time_remaining -= 1
        self.x += self.velocity_x/self.total_update_time
        self.y += self.velocity_y/self.total_update_time
        self.teta += self.angular_velocity/self.total_update_time
        # self.x += self.velocity_x
        # self.y += self.velocity_y
        # self.teta += self.angular_velocity
        #print(self.teta)
        while True:
            if self.teta > 2*pi:
                self.teta -= 2*pi
            elif self.teta < 0:
                self.teta += 2*pi
            else:
                break
        self.points = []
        for i in range(self.n):

            self.relative_points[i] = rotate_point(self.relative_points[i], self.angular_velocity/self.total_update_time, [0, 0])
            #self.relative_points[i] = rotate_point(self.relative_points[i], self.angular_velocity, [0, 0])
            self.points.append([(self.x + self.relative_points[i][0] + offset_x),
                               (self.y + self.relative_points[i][1] + offset_y)])


    def render_self(self, window, x , y):
        points = []
        for i, point in enumerate(self.points):
            points.append([point[0]+x, point[1]+y])
        pygame.draw.polygon(window, self.color, points)


    def destroy_self(self):
        self.polygons.remove(self)

