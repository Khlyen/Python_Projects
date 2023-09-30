import pygame
from math import *

from polygon import Polygon as Poly
from border import Border
from random import randint
from math_calculations import *
from sympy import symbols, solve
from shapely.geometry import Point, Polygon
from threading import Thread

class Game():
    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 1200
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (100, 100, 100)
    GREY2 = (200, 200, 200)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)


    def __init__(self):
        self.is_running = True
        pygame.init()
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Çokgen")
        # pygame.display.set_icon(pygame.image.load(""))
        self.collision_sound = pygame.mixer.Sound(r"C:\Users\Berke\Desktop\Projects\Python\çokgen\hit_sound.wav")
        self.center = [self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2]
        self.pressed_keys = []
        self.c_slowing_factor = 0.125
        self.c_acceleration = 0.75 + self.c_slowing_factor
        self.c_velocity_x = 0
        self.c_velocity_y = 0
        self.c_max_velocity = 10
        self.c_point1 = [0 - 20, 0 - 10]
        self.c_point2 = [0 - 10, 0]
        self.c_point3 = [0 - 20, 0 + 10]
        self.c_point4 = [0 + 10, 0]
        self.map_max_width = 300  # in both directions(total is x2)
        self.map_max_height = 300  # in both directions(total is x2)
        self.mouse_x = 0
        self.mouse_y = 0
        self.circles = []
        self.lines = []
        self.c_offset_x = 0
        self.c_offset_y = 0
        self.border_width = 5
        self.polygons = Poly.polygons
        #points start from top left and goes clockwise direction
        border1_points = [[-self.map_max_width - self.border_width, -self.map_max_height-  self.border_width],
                          [-self.map_max_width, -self.map_max_height-  self.border_width],
                          [-self.map_max_width, +self.map_max_height +  self.border_width],
                          [-self.map_max_width-self.border_width, +self.map_max_height +  self.border_width]]
        border2_points = [[-self.map_max_width, -self.map_max_height-  self.border_width],
                          [+self.map_max_width, -self.map_max_height-  self.border_width],
                          [+self.map_max_width, -self.map_max_height],
                          [-self.map_max_width, -self.map_max_height]]
        border3_points = [[+self.map_max_width, -self.map_max_height-  self.border_width],
                          [+self.map_max_width+self.border_width, -self.map_max_height-  self.border_width],
                          [+self.map_max_width+self.border_width, +self.map_max_height+  self.border_width],
                          [+self.map_max_width, +self.map_max_height+  self.border_width]]
        border4_points = [[-self.map_max_width, +self.map_max_height],
                          [+self.map_max_width, +self.map_max_height],
                          [+self.map_max_width, +self.map_max_height+  self.border_width],
                          [-self.map_max_width, +self.map_max_height +  self.border_width]]
        border1_center = [-self.map_max_width-self.border_width/2, 0] #left border
        border2_center = [+self.map_max_width+self.border_width/2, 0] #right border
        border3_center = [0, self.map_max_height+ self.border_width/2] #bottom border
        border4_center = [0, -self.map_max_height-self.border_width/2] #top border
        Border(border1_center[0], border2_center[1], self.YELLOW, border1_points)
        Border(border2_center[0], border2_center[1], self.YELLOW, border2_points)
        Border(border3_center[0], border3_center[1], self.YELLOW, border3_points)
        Border(border4_center[0], border4_center[1], self.YELLOW, border4_points)
        self.create_polygons(2,3,self.RED, 20, 1, 50, 1)
        self.create_polygons(2,4, self.BLUE, 30, 1, 50, 1)
        self.create_polygons(2,5, self.BLACK, 40, 1, 50, 1)
        # self.create_polygons(3,4,self.GREEN, 25, 1, 50, 2)
        # self.create_polygons(2,5,self.WHITE, 30, 1, 50, 2)
        # self.create_polygons(1,8,self.RED, 100, 1, 100, 1)
        self.clock = pygame.time.Clock()
        self.mainloop()

    def mainloop(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
            pygame.display.update()



    def create_polygons(self, number_of_object, n, color, radius, density, factor1, factor2):
        i = 0
        while i < number_of_object:
            is_collided = False
            x = randint(-self.map_max_width + 1.2*radius, self.map_max_height- 1.2*radius)
            y = randint(-self.map_max_width + 1.2*radius, self.map_max_height - 1.2*radius)
            teta = randint(0, 360)/180*pi
            poly1 = Poly(n, x, y, teta, color, radius, density, factor1, factor2)
            for poly2 in Poly.polygons[:-1]:
                if do_polygons_intersect(poly1.points, poly2.points):
                    is_collided = True
                    break
            if is_collided:
                Poly.polygons.pop(-1)
                continue
            i += 1


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
        # self.pressed_keys = pygame.key.get_pressed()
        # if self.pressed_keys[pygame.K_w]:
        #     self.c_velocity_y += self.c_acceleration
        #     if self.c_velocity_y > self.c_max_velocity:
        #         self.c_velocity_y = self.c_max_velocity
        # if self.pressed_keys[pygame.K_s]:
        #     self.c_velocity_y -= self.c_acceleration
        #     if self.c_velocity_y < -self.c_max_velocity:
        #         self.c_velocity_y = -self.c_max_velocity
        # if self.pressed_keys[pygame.K_a]:
        #     self.c_velocity_x += self.c_acceleration
        #     if self.c_velocity_x > self.c_max_velocity:
        #         self.c_velocity_x = self.c_max_velocity
        # if self.pressed_keys[pygame.K_d]:
        #     self.c_velocity_x -= self.c_acceleration
        #     if self.c_velocity_x < -self.c_max_velocity:
        #         self.c_velocity_x = -self.c_max_velocity

    def render(self):

        # render background
        self.window.fill(self.GREY)
        # render polygons
        for polygon in self.polygons+Border.borders:
            polygon.render_self(self.window, self.center[0], self.center[1])
        # # render character
        # pygame.draw.polygon(self.window, self.BLUE, [[self.c_point1[0]+self.center[0], self.c_point1[1]+self.center[1]],
        #                                              [self.c_point2[0]+self.center[0], self.c_point2[1]+self.center[1]],
        #                                              [self.c_point3[0]+self.center[0], self.c_point3[1]+self.center[1]],
        #                                              [self.c_point4[0]+self.center[0], self.c_point4[1]+self.center[1]]])
        pygame.display.update()
        # reset character points for rotating algorithm
        self.c_point1 = [0 - 20, 0 - 10]
        self.c_point2 = [0 - 10, 0]
        self.c_point3 = [0 - 20, 0 + 10]
        self.c_point4 = [0 + 10, 0]
        #render circles for debugging
        for circle in self.circles:
            pygame.draw.circle(self.window, self.BLACK,
                               [circle[0]+self.c_offset_x-(self.WINDOW_WIDTH / 2 - self.map_max_width),circle[1]+self.c_offset_y-(self.WINDOW_HEIGHT / 2 - self.map_max_height)], 3, 1)
        #render lines for debugging
        for line in self.lines:
            pygame.draw.line(self.window, self.BLACK,line[0], line[1], width=3)

    def update(self):
        # update character angle
        [self.mouse_x, self.mouse_y] = pygame.mouse.get_pos()
        vec1 = [1, 0]
        vec2 = [self.mouse_x-self.center[0], self.mouse_y-self.center[1]]
        try:
            teta = angle_btwn_two_vecs(vec2, vec1)
        except ZeroDivisionError:
            teta = 0
        if self.mouse_y < self.center[1]:
            teta = -teta
        #print(teta*180/pi)
        self.c_point1 = rotate_point(self.c_point1, teta, [0,0])
        self.c_point2 = rotate_point(self.c_point2, teta, [0,0])
        self.c_point3 = rotate_point(self.c_point3, teta, [0,0])
        self.c_point4 = rotate_point(self.c_point4, teta, [0,0])
        # update character position
        self.c_offset_x += self.c_velocity_x
        self.c_offset_y += self.c_velocity_y
        if self.c_velocity_x < 0:
            self.c_velocity_x += self.c_slowing_factor
        elif self.c_velocity_x > 0:
            self.c_velocity_x -= self.c_slowing_factor
        if self.c_velocity_y < 0:
            self.c_velocity_y += self.c_slowing_factor
        elif self.c_velocity_y > 0:
            self.c_velocity_y -= self.c_slowing_factor

        # for polygon in self.polygons:
        #     polygon.update_self(self.c_offset_x, self.c_offset_y)
        # self.collision_detection()
        # update polygons
        for polygon in self.polygons:
            a = polygon.velocity_x/polygon.factor2
            b = polygon.velocity_y/polygon.factor2
            c = polygon.angular_velocity/polygon.factor2
            polygon.total_update_time = min(round(max(a,b,c)),polygon.max_update_time)
            polygon.update_time_remaining = polygon.total_update_time
            if polygon.total_update_time == 0:
                polygon.update_time_remaining = 1
                polygon.total_update_time = 1

        #print(self.clock.get_fps())
        is_update_done = False
        to_be_updated_polygons = Poly.polygons + Border.borders
        #print(to_be_updated_polygons)
        while not is_update_done:
            if len(to_be_updated_polygons) == 0:
                is_update_done = True
            for polygon in to_be_updated_polygons:
                if polygon.update_time_remaining == 0:
                    to_be_updated_polygons.remove(polygon)
                polygon.update_self(self.c_offset_x, self.c_offset_y)
            self.collision_detection()

    def collision_detection(self):
        # collision between polygons
        temp = self.polygons.copy()
        for polygon1 in self.polygons:
            temp.remove(polygon1)
            for polygon2 in temp + Border.borders:
                if do_polygons_intersect(polygon1.points, polygon2.points):
                    # polygon1.points = [[round(p[0], 1),round(p[1], 1)] for p in polygon1.points]
                    # polygon2.points = [[round(p[0], 1),round(p[1], 1)] for p in polygon2.points]
                    # print(polygon1.points, polygon2.points)
                    """Collision is detected"""
                    self.collision_sound.play()
                    poly_that_collides = None #this is the polygon which has a point that is inside of the other polygon
                    poly_that_is_collided = None
                    impact_point = None
                    unit_normal_vec = None #this is the normal vector of line where the collision happened
                    collision_line = []
                    impact_point_candidates = []
                    for point in polygon1.points:
                        p = Point(point[0], point[1])
                        poly = Polygon(polygon2.points)
                        if poly.touches(p) or poly.contains(p):
                            impact_point_candidates.append(point)
                    # if len(impact_point_candidates) == 2 and impact_point_candidates[0] == impact_point_candidates[1]:
                    #     impact_point = impact_point_candidates[0]
                    if len(impact_point_candidates) == 2:
                        impact_point = [(impact_point_candidates[0][0] + impact_point_candidates[1][0]) / 2,
                                        (impact_point_candidates[0][1] + impact_point_candidates[1][1]) / 2]
                        poly_that_collides = polygon1
                        poly_that_is_collided = polygon2
                    else:
                        a = len(impact_point_candidates)
                        for point in polygon2.points:
                            p = Point(point[0], point[1],3)
                            poly = Polygon(polygon1.points)
                            if poly.touches(p) or poly.contains(p):
                                impact_point_candidates.append(point)
                        if len(impact_point_candidates) >= 2:
                            if impact_point_candidates[0] == impact_point_candidates[1]:
                                """collision point at corner"""
                                impact_point = impact_point_candidates[0]
                                poly_that_collides = polygon1
                                poly_that_is_collided = polygon2
                                unit_normal_vec = [poly_that_collides.velocity_x-poly_that_is_collided.velocity_x, poly_that_collides.velocity_y-poly_that_is_collided.velocity_y]

                            impact_point = [(impact_point_candidates[0][0] + impact_point_candidates[1][0]) / 2,
                                            (impact_point_candidates[0][1] + impact_point_candidates[1][1]) / 2]
                            poly_that_collides = polygon1
                            poly_that_is_collided = polygon2
                        elif len(impact_point_candidates) == 1:
                            impact_point = impact_point_candidates[0]
                            if a == 1:
                                poly_that_is_collided =polygon1
                                poly_that_collides = polygon2
                            else:
                                poly_that_is_collided = polygon2
                                poly_that_collides = polygon1
                        else:
                            print("Error:{} points".format(len(impact_point_candidates)))

                    if unit_normal_vec == None:
                        for i in range(-1, len(poly_that_collides.points)-1):
                            if impact_point == poly_that_collides.points[i]:
                                collision_line = [poly_that_collides.points[i + 1],poly_that_collides.points[i]]
                            if point_in_line([poly_that_collides.points[i],poly_that_collides.points[i+1]], impact_point):
                                collision_line = [poly_that_collides.points[i],poly_that_collides.points[i+1]]
                        unit_normal_vec = normalize_vec(normal_of_line(collision_line[0],collision_line[1]))
                    # unit_normal_vec = [poly_that_collides.velocity_x - poly_that_is_collided.velocity_x,
                    #                    poly_that_collides.velocity_y - poly_that_is_collided.velocity_y]

                    polygon1.x -= 1*polygon1.velocity_x/polygon1.total_update_time
                    polygon2.x -= 1*polygon2.velocity_x/polygon2.total_update_time
                    polygon1.y -= 1*polygon1.velocity_y/polygon1.total_update_time
                    polygon2.y -= 1*polygon2.velocity_y/polygon2.total_update_time
                    polygon1.teta -= 1*polygon1.angular_velocity/polygon1.total_update_time
                    polygon2.teta -= 1*polygon2.angular_velocity/polygon2.total_update_time
                    if polygon1.type == "polygon":
                        polygon1.points = []
                        for i in range(polygon1.n):
                            polygon1.relative_points[i] = rotate_point(polygon1.relative_points[i], -1*polygon1.angular_velocity/polygon1.total_update_time, [0, 0])
                            polygon1.points.append([(polygon1.x + polygon1.relative_points[i][0] + self.c_offset_x),
                                                   (polygon1.y + polygon1.relative_points[i][1] + self.c_offset_y)])
                    if polygon2.type == "polygon":
                        polygon2.points = []
                        for i in range(polygon2.n):
                            polygon2.relative_points[i] = rotate_point(polygon2.relative_points[i], -1*polygon2.angular_velocity/polygon2.total_update_time, [0, 0])
                            polygon2.points.append([(polygon2.x + polygon2.relative_points[i][0] + self.c_offset_x),
                                                   (polygon2.y + polygon2.relative_points[i][1] + self.c_offset_y)])
                    # thread = Thread(target=self.handle_collision, args=(poly_that_is_collided, poly_that_collides, impact_point, unit_normal_vec, collision_line))
                    # thread.start()
                    # thread.join()
                    self.handle_collision(poly_that_is_collided, poly_that_collides, impact_point, unit_normal_vec, collision_line)

    def handle_collision(self, poly1, poly2, contact_p, impuls_unit_vec, contact_line):
        # self.circles.append(contact_p)
        # self.circles.append([poly1.x, poly1.y])
        # self.lines.append(contact_line)
        # self.lines.append([contact_p, [contact_p[0]+20*impuls_unit_vec[0],contact_p[1]+20*impuls_unit_vec[1]]])
        pygame.display.update()
        # print("contact_point:", contact_p)
        # print("impuls_unit_vec:", impuls_unit_vec)
        # print("collision_line:", contact_line)
        J = symbols('J')
        rcx, rcy = contact_p[0], contact_p[1]
        # print("çarpışma öncesi hızlar")
        # print(poly1.velocity_x, poly1.velocity_y, poly1.angular_velocity)
        # print(poly2.velocity_x, poly2.velocity_y, poly2.angular_velocity)

        #polygon1 calculations
        jx, jy = impuls_unit_vec[0], impuls_unit_vec[1]
        rx, ry = poly1.x, poly1.y
        cross_product = jy*(rcx-rx)-jx*(rcy-ry)
        # print("crosspr", cross_product)
        E_initial = 1/2*poly1.mass*(poly1.velocity_x**2+poly1.velocity_y**2)+1/2*poly1.moment_of_inertia*poly1.angular_velocity**2
        E_final_part1 = 1/2*poly1.mass*((poly1.velocity_x+J*jx/poly1.mass)**2+(poly1.velocity_y+J*jy/poly1.mass)**2)
        E_final_part2 = 1/2*poly1.moment_of_inertia*(poly1.angular_velocity+J/poly1.moment_of_inertia*cross_product)**2

        impuls = solve(E_initial - (E_final_part1+E_final_part2), J)
        #print(J)
        if len(impuls) == 1:
            impuls = 0
        elif abs(impuls[0]) > abs(impuls[1]):
            impuls = impuls[0]
        else:
            impuls = impuls[1]

        # print("impuls{}".format(impuls))
        poly1.velocity_x = poly1.velocity_x + impuls*jx/poly1.mass
        poly1.velocity_y = poly1.velocity_y + impuls*jy/poly1.mass
        poly1.angular_velocity = poly1.angular_velocity + impuls*cross_product/poly1.moment_of_inertia
        if abs(poly1.velocity_x) < 0.000000001:
            poly1.velocity_x = 0
        if abs(poly1.velocity_y) < 0.000000001:
            poly1.velocity_y = 0
        if abs(poly1.angular_velocity) < 0.000000001:
            poly1.angular_velocity = 0
        # print("çarpışma sonrası hızlar")
        # print(poly1.velocity_x, poly1.velocity_y, poly1.angular_velocity)
        poly1.total_update_time = min(round(max(abs(poly1.velocity_x/poly1.factor2),abs(poly1.velocity_y/poly1.factor2),abs(poly1.angular_velocity/poly1.factor2))),poly1.max_update_time)
        if poly1.total_update_time == 0:
            poly1.total_update_time = 1
            poly1.update_time_remaining = 0
        else:
            poly1.update_time_remaining = round((poly1.update_time_remaining/poly1.total_update_time)*poly1.total_update_time)

        #print(poly1.angular_velocity)

        # if poly1.velocity_x > poly1.max_velocity:
        #     poly1.velocity_x = poly1.max_velocity
        # elif poly1.velocity_x < -poly1.max_velocity:
        #     poly1.velocity_x = -poly1.max_velocity
        # if poly1.velocity_y > poly1.max_velocity:
        #     poly1.velocity_y = poly1.max_velocity
        # elif poly1.velocity_y < -poly1.max_velocity:
        #     poly1.velocity_y = -poly1.max_velocity
        # if poly1.angular_velocity > poly1.max_angular_velocity:
        #     poly1.angular_velocity = poly1.max_angular_velocity
        # elif poly1.angular_velocity < -poly1.max_angular_velocity:
        #     poly1.angular_velocity = -poly1.max_angular_velocity

        # #polygon2 calculations

        jx, jy = -impuls_unit_vec[0], -impuls_unit_vec[1]
        rx, ry = poly2.x, poly2.y
        cross_product = jy*(rcx-rx)-jx*(rcy-ry)
        poly2.velocity_x = poly2.velocity_x + impuls*jx/poly2.mass
        poly2.velocity_y = poly2.velocity_y + impuls*jy/poly2.mass
        poly2.angular_velocity = poly2.angular_velocity + impuls*cross_product/poly2.moment_of_inertia
        #print("çarpışma sonra hız obje 2 yuvarlama öncesi",poly2.velocity_x, poly2.velocity_y, poly2.angular_velocity)
        if abs(poly2.velocity_x) < 0.000000001:
            poly2.velocity_x = 0
        if abs(poly2.velocity_y) < 0.000000001:
            poly2.velocity_y = 0
        if abs(poly2.angular_velocity) < 0.000000001:
            poly2.angular_velocity = 0

        # print(poly2.velocity_x, poly2.velocity_y, poly2.angular_velocity)
        poly2.total_update_time = min(round(max(abs(poly2.velocity_x)/poly2.factor2,abs(poly2.velocity_y/poly2.factor2),abs(poly2.angular_velocity/poly2.factor2))),poly2.max_update_time)
        if poly2.total_update_time == 0:
            poly2.total_update_time = 1
            poly2.update_time_remaining = 0
        else:
            poly2.update_time_remaining = round((poly2.update_time_remaining/poly2.total_update_time)*poly2.total_update_time)

        # print("obje 1 total update frame:{}, kalan update frame:{}".format(poly1.total_update_time, poly1.update_time_remaining))
        # print("obje 2 total update frame:{}, kalan update frame:{}".format(poly2.total_update_time, poly2.update_time_remaining))
        # poly1.update_self(self.c_offset_x, self.c_offset_y)
        # poly2.update_self(self.c_offset_x, self.c_offset_y)


        # if poly2.velocity_x > poly2.max_velocity:
        #     poly2.velocity_x = poly2.max_velocity
        # elif poly2.velocity_x < -poly2.max_velocity:
        #     poly2.velocity_x = -poly2.max_velocity
        # if poly2.velocity_y > poly2.max_velocity:
        #     poly2.velocity_y = poly2.max_velocity
        # elif poly2.velocity_y < -poly2.max_velocity:
        #     poly2.velocity_y = -poly2.max_velocity
        # if poly2.angular_velocity > poly2.max_angular_velocity:
        #     poly2.angular_velocity = poly2.max_angular_velocity
        # elif poly2.angular_velocity < -poly2.max_angular_velocity:
        #     poly2.angular_velocity = -poly2.max_angular_velocity


if __name__ == '__main__':
    game = Game()
