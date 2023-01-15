import math
import os
import time

import pygame
from pygame import gfxdraw

from graph_drawer import GraphDrawer
from point import Point

PI = math.pi
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class PendulumDrawer(pygame.sprite.Sprite):
    def __init__(self, fulcrum: Point, length_of_rope: int, peroid: float, amplitude: float, sprite: str, screen) -> None:
        self.pendulum = Pendulum(fulcrum, length_of_rope, peroid, amplitude)
        self.init_pg_sprite(sprite)

        self.graph_drawer = GraphDrawer(self.pendulum.maximal_deviation+10, self.pendulum.maximal_speed+10, "Смещение", "Скорость")
        # Прибавляем по 10 к каждому значению, чтобы графики не "упирались" в границы.
        self.screen = screen
        self.fulcrum = fulcrum

    def init_pg_sprite(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, "sprites")
        self.image = pygame.image.load(os.path.join(self.img_folder, sprite)).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (self.pendulum.current_position.x, self.pendulum.current_position.y)

    def update(self) -> None:
        self.update_pendulum()
        self.draw_rope()
        self.draw_graph()

    def draw_rope(self):
        gfxdraw.line(
            self.screen,
            self.fulcrum.x,
            self.fulcrum.y,
            self.pendulum.current_position.x,
            self.pendulum.current_position.y,
            WHITE
        )

    def update_pendulum(self) -> None:
        self.pendulum.move()
        self.rect.center = (self.pendulum.current_position.x, self.pendulum.current_position.y)

    def draw_graph(self) -> None:
        self.graph_drawer.update(self.pendulum.timer,
        self.pendulum.math_position_in_trajectory, 
        self.pendulum.speed)

    def abort(self):
        self.graph_drawer.close()


class Pendulum:
    def __init__(self, fulcrum: Point, length_of_rope: int, peroid: float, amplitude: float) -> None:
        self.fulcrum = fulcrum
        self.length_of_rope = length_of_rope
        self.amplitude = amplitude

        self.period = peroid

        self.trajectory: list[Point] = []
        self.generate_trajectory()
        self.current_position_in_trajectory: float = 0

        self.current_position: Point = self.trajectory[self.current_position_in_trajectory]

        self.timer: float = 0.

    def move(self) -> None:
        try: # TODO придумать что-нибудь более изобретательное
            self.current_position = self.trajectory[int(round(self.current_position_in_trajectory))]
        except IndexError:
            self.current_position = self.trajectory[int(round(self.current_position_in_trajectory)) - 1]
        
        self.current_position_in_trajectory = self.math_position_in_trajectory + self.maximal_deviation
        self.add_time()

    def add_time(self) -> None:
        self.timer += 0.05 # Т.к. обнвление кадра происходит 20 раз в сек. добаляем 1 / 20

    @property
    def math_position_in_trajectory(self) -> float:
        return self.maximal_deviation * math.cos(self.cyclic_frequency * self.timer)

    @property
    def speed(self) -> float:
        return -self.maximal_speed * math.sin(self.cyclic_frequency * self.timer)

    @property
    def maximal_speed(self) -> float:
        return self.maximal_deviation * self.cyclic_frequency

    @property
    def maximal_deviation(self) -> float:
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

    def converted_amplitude(self) -> tuple:
        in_radians = self.amplitude * PI / 180
        return PI/2 - in_radians, PI/2 + in_radians


#FPS = 20
#pygame.init()
#pygame.mixer.init()
#screen = pygame.display.set_mode((800, 400))
#pygame.display.set_caption("TEST")
#clock = pygame.time.Clock()
#all_sprites = pygame.sprite.Group()
#
#pendulum = PendulumDrawner(Point(400, 0), 300, 2, 360, 'pendulum.png')
#all_sprites.add(pendulum)
#
## Цикл игры
#running = True
#paused = False
#
#while running:
#    # Держим цикл на правильной скорости
#    clock.tick(FPS)
#    # Ввод процесса (события)
#    for event in pygame.event.get():
#        # check for closing window
#        if event.type == pygame.QUIT:
#            running = False
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_SPACE:
#                paused = not paused
#
#    if paused:
#        continue
#    
#    # Обновление
#    start = time.time()
#    all_sprites.update()
#    
#    # Рендеринг
#    screen.fill((0, 0, 0))
#    all_sprites.draw(screen)
#
#    # После отрисовки всего, переворачиваем экран
#    pygame.display.flip()
#    end = time.time()
#    print(end - start)
#
#
#pygame.quit()


# pyinstaller -F --add-data "sprites\\pendulum.png;.\sprites" pendulum.pyw
