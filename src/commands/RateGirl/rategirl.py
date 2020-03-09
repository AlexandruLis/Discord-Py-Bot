import datetime
import time
from classified.globals import not_a_girl


class RateGirl:

    def __init__(self):
        self.zones = {
            'No-go zone': [(100, 699), (100, 100), (599, 100), (599, 1100)],
            not_a_girl: [(100, 700), (100, 1100), (1100, 1100), (1100, 700)],
            'Danger zone': [(601, 399), (601, 100), (1100, 99)],
            'Fun zone': [(600, 700), (799, 700), (799, 279), (600, 400)],
            'Date zone': [(800, 399), (1101, 399), (1101, 100), (800, 280)],
            'wife zone': [(800, 400), (1101, 400), (800, 599), (1101, 599)],
            'Unicorn': [(800, 600), (1101, 600), (800, 700), (1101, 700)]
        }

    @staticmethod
    def generate_point_coords(hot, crazy):
        xcoord = int((hot + 1) * 100)
        ycoord = 1200 - int((crazy + 1) * 100)
        return xcoord, ycoord

    @staticmethod
    def point_in_poly(vcoord_x: list, vcoord_y: list, pcoord: list):  # ray casting to the right
        inside = False
        j = len(vcoord_x) - 1
        for i in range(len(vcoord_x)):
            if (((vcoord_y[i] > pcoord[1]) != (vcoord_y[j] > pcoord[1])) and
                    (pcoord[0] < (vcoord_x[j] - vcoord_x[i]) * (pcoord[1] - vcoord_y[i]) / (vcoord_y[j] - vcoord_y[i]) +
                     vcoord_x[i])):
                inside = not inside
            j = i

        return inside

    def determine_zone(self, point):
        zones = self.zones
        for zone in zones:
            xcoord, ycoord = self.poly_format(zones[zone])
            if self.point_in_poly(xcoord, ycoord, point):
                return zone
        return 'error'

    @staticmethod
    def poly_format(zone: list):
        x_coords = []
        y_coords = []
        for x in zone:
            x_coords.append(x[0])
        for y in zone:
            y_coords.append(y[1])
        return x_coords, y_coords

    @staticmethod
    def generate_random_values(user_id: float):
        a = 12345
        m = 2 ** 32
        seed = int(time.mktime(datetime.date.today().timetuple()) / 100000)
        # PRNG
        seed = ((a * seed + user_id) % m)
        hot = round((seed / m) * 10, 2)
        for i in range(5):
            seed = ((a * seed + user_id) % m)
        crazy = round((seed / m) * 10, 2)

        # is above?

        return hot, crazy

    def rategirl(self, user_id: float):
        """
        Using pseudo RNG, generate 2 numbers between 0-10 (float)
        The RNG formula is based on day and month as well as the user ID given
        :param user_id: float
        :return: Hot(Float) , Crazy (Float)
        """
        xpoint, ypoint = self.generate_random_values(user_id)
        print(xpoint, ypoint)
        xpoint_safe, ypoint_safe = self.generate_point_coords(xpoint, ypoint)
        result = self.determine_zone([xpoint_safe, ypoint_safe])
        print(result)
        return xpoint, ypoint, xpoint_safe, ypoint_safe, result
