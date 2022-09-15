import math
import pygame
import time
import os
ACCELERATION_OF_FREE_FALL = 9.81
PI = math.pi


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class PendulumDrawner(pygame.sprite.Sprite):
    def __init__(self, fulcrum: Point, length_of_rope: int, peroid: float, maximal_speed: float, color: tuple) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.pendulum = Pendulum(fulcrum, length_of_rope, peroid, maximal_speed)
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'sprites')
        self.image = pygame.image.load(os.path.join(self.img_folder, 'pendulum.png')).convert()

        self.rect = self.image.get_rect()
        self.rect.center = (self.pendulum.current_position.x, self.pendulum.current_position.y)

    def update(self) -> None:
        self.pendulum.move()
        self.rect.center = (self.pendulum.current_position.x, self.pendulum.current_position.y)


class Pendulum:
    def __init__(self, fulcrum: Point, length_of_rope: int, peroid: float, maximal_speed: float) -> None:
        self.fulcrum = fulcrum
        self.length_of_rope = length_of_rope

        self.period = peroid
        self.maximal_speed = maximal_speed  

        self.trajectory: list[Point] = []
        self.generate_trajectory()
        self.current_position_in_trajectory: float = 1
        self.current_position: Point = self.trajectory[self.current_position_in_trajectory]

        self.__direction = 1

    def move(self) -> None:
        self.current_position = self.trajectory[int(round(self.current_position_in_trajectory))]
        self.current_position_in_trajectory += self.speed

    @property
    def speed(self) -> float:
        return self.maximal_speed * math.cos(self.deviation_from_equilibrium_point)  * self.cyclic_frequency * self.direction

    @property
    def direction(self) -> int:
        return self.__direction

    @direction.getter
    def direction(self) -> int: # TODO Найти что-нибудь более изобретательное.
        if round(self.current_position_in_trajectory) == 0 or round(self.current_position_in_trajectory) == len(self.trajectory)-1:
            self.__direction *= -1  

        return self.__direction

    @property
    def deviation_from_equilibrium_point(self) -> float:
        # Находим решением треугольника по трем сторонам.
        # alpha - угол до точки равновесия, то есть искомый угол.
        alpha = math.acos(
            (self.length_of_rope ** 2 + self.length_of_rope ** 2 - self.way_to_equilibrium_point ** 2) /
            (2 * (self.length_of_rope ** 2))
        )
        return alpha

    @property
    def cyclic_frequency(self) -> float:
        return PI * 2 / self.period

    @property
    def way_to_equilibrium_point(self) -> float:
        return math.sqrt(
            (self.current_position.x - self.__position_at_equilibrium_point.x) ** 2 +
            (self.current_position.y - self.__position_at_equilibrium_point.y) ** 2
        )
    
    @property
    def __position_at_equilibrium_point(self) -> Point:
        x = self.fulcrum.x
        y = self.fulcrum.y + self.length_of_rope
        return Point(x, y)

    def generate_trajectory(self, accuracy=250) -> None:
        for i in range(0, int(PI * accuracy), 1):
            corner = i / accuracy

            X = round(self.length_of_rope * math.cos(corner) + self.fulcrum.x)
            Y = round(self.length_of_rope * math.sin(corner) + self.fulcrum.y)

            self.trajectory.append(Point(X, Y))


start = time.time()
FPS = 50
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("TEST")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

pendulum = PendulumDrawner(Point(600, 0), 400, 1, 1, (0, 0, 255))
all_sprites.add(pendulum)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
end = time.time()
print(end - start)
pygame.quit()