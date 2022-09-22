import math
import pygame
import time
import os

PI = math.pi


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class PendulumDrawner(pygame.sprite.Sprite):
    def __init__(self, fulcrum: Point, length_of_rope: int, peroid: float, amplitude: float) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.pendulum = Pendulum(fulcrum, length_of_rope, peroid, amplitude)
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'sprites')
        self.image = pygame.image.load(os.path.join(self.img_folder, 'pendulum.png')).convert()

        self.rect = self.image.get_rect()
        self.rect.center = (self.pendulum.current_position.x, self.pendulum.current_position.y)

    def update(self) -> None:
        self.pendulum.move()
        self.rect.center = (self.pendulum.current_position.x, self.pendulum.current_position.y)


class Pendulum:
    def __init__(self, fulcrum: Point, length_of_rope: int, peroid: float, amplitude: float) -> None:
        self.fulcrum = fulcrum
        self.length_of_rope = length_of_rope
        self.amplitude = amplitude

        self.period = peroid

        self.trajectory: list[Point] = []
        self.generate_trajectory()
        self.current_position_in_trajectory: float = 10

        self.current_position: Point = self.trajectory[self.current_position_in_trajectory]

        self.time = 1

    def move(self) -> None:
        try: # TODO придумать что-нибудь более изобретательнее
            self.current_position = self.trajectory[int(round(self.current_position_in_trajectory))]
        except IndexError:
            self.current_position = self.trajectory[int(round(self.current_position_in_trajectory)) - 1]
        
        self.current_position_in_trajectory = self.math_position_in_trajectory + self.maximal_deviation
        self.add_time()

    def add_time(self):
        self.time += 0.02 # Т.к. обнвление кадра происходит 50 раз в сек. добаляем 1 / 50

    @property
    def math_position_in_trajectory(self) -> float:
        return self.maximal_deviation * math.cos(self.cyclic_frequency * self.time)

    @property
    def maximal_deviation(self):
        return len(self.trajectory) / 2

    @property
    def cyclic_frequency(self) -> float:
        return PI * 2 / self.period

    def generate_trajectory(self, accuracy=250) -> None:
        start_trajectory, end_trajectory = self.converted_amplitude()

        for i in range(int(start_trajectory * accuracy), int(end_trajectory * accuracy), 1):
            corner = i / accuracy

            X = round(self.length_of_rope * math.cos(corner) + self.fulcrum.x)
            Y = round(self.length_of_rope * math.sin(corner) + self.fulcrum.y)

            self.trajectory.append(Point(X, Y))

    def converted_amplitude(self) -> range:
        in_radians = self.amplitude * PI / 180
        return PI/2 - in_radians, PI/2 + in_radians


start = time.time()
FPS = 50
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("TEST")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

pendulum = PendulumDrawner(Point(600, 0), 300, 7.5, 45)
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
