import datetime
import time

class RateGirl:
    def rategirl(self, user_id: float):
        """
        Using pseudo RNG, generate 2 numbers between 0-10 (float)
        The RNG formula is based on day and month as well as the user ID given
        :param user_id: float
        :return: Hot(Float) , Crazy (Float)
        """
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
