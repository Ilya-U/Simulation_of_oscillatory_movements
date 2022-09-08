import math
ACCELERATION_OF_FREE_FALL = 9.81
PI = math.pi


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Pendulum:
    def __init__(self, fulcrum: Point, length_of_rope: int, radius: int) -> None:
        self.fulcrum = fulcrum
        self.length_of_rope = length_of_rope
        self.radius = radius

        self.period = 1.5 # Берем наиболее наглядный показатель
        self.maximal_speed = 10 # Тоже самое, берем наиболее наглядный показатель

        self.trajectory: list[Point] = []
        self.generate_trajectory()
        self.current_position: Point = self.trajectory[0]

    def generate_trajectory(self, accuracy=250):
        for i in range(0, int(PI * accuracy), 1):
            corner = i / accuracy

            X = round(self.length_of_rope * math.cos(corner) + self.fulcrum.x)
            Y = round(self.length_of_rope * math.sin(corner) + self.fulcrum.y)

            self.trajectory.append(Point(X, Y))

    @property
    def speed(self):
        return self.maximal_speed * math.cos(self.cyclic_frequency * self.deviation_from_equilibrium_point())

    def deviation_from_equilibrium_point(self) -> float:
        """ Находим решением треугольника по трем сторонам.
        alpha - угол до точки до равновесия, то есть искомый угол. """
        alpha = math.acos(
            (self.length_of_rope ** 2 + self.length_of_rope ** 2 - self.way_to_equilibrium_point ** 2) /
            2 * self.length_of_rope ** 2
        )
        return alpha

    @property
    def way_to_equilibrium_point(self):
        return math.sqrt(
            (self.current_position.x - self.__position_at_equilibrium_point.x) ** 2 +
            (self.current_position.y - self.__position_at_equilibrium_point.y) ** 2
        )

    @property
    def cyclic_frequency(self):
        return PI * 2 / self.period
    
    @property
    def __position_at_equilibrium_point(self) -> Point:
        x = self.fulcrum.x
        y = self.fulcrum.y + self.length_of_rope
        return Point(x, y)
