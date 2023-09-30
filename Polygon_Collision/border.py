from polygon import Polygon as Poly

class Border(Poly):
    """
    Border polygon class inherits from general polygon class
    """
    borders = []


    def __init__(self, x, y, color, points):

        self.x = x  # center point x
        self.y = y  # center point y
        self.teta = 0
        self.type = "border"
        self.n = 4
        self.factor2 = 0.5
        self.color = color
        self.angular_velocity = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.mass = 999999999999999999999999
        self.moment_of_inertia = 999999999999999999999999
        self.points = points
        self.total_update_time = 1
        self.update_time_remaining = 1
        self.borders.append(self)


    def update_self(self, offset_x, offset_y):

        if self.update_time_remaining > 0:
            self.update_time_remaining -= 1
        pass

    def destroy_self(self):
        super().destroy_self()
