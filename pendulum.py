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

        self.position_of_object: Point = Point(-1, -1)
        self.trajectory = []
        self.generate_trajectory()

    def generate_trajectory(self, accuracy=250):
        for i in range(0, int(PI * accuracy), 1):
            corner = i / accuracy

            X = round(self.length_of_rope * math.cos(corner) + self.fulcrum.x)
            Y = round(self.length_of_rope * math.sin(corner) + self.fulcrum.y)

            self.trajectory.append(Point(X, Y))

print(Pendulum(Point(0, 0), 1000, 10).trajectory)