import math
import os
import time

import pygame
from pygame import gfxdraw

from graph_drawer import GraphDrawer
from point import Point

PI = math.pi
BLACK = (0, 0, 0)
PURPLE = (139, 0, 255)
BLUE = (0, 0, 255)


class ElectronicOscillatorDrawer(pygame.sprite.Sprite):
    def __init__(self, center: Point, maximal_charge: float, period: float, sprite: str, screen) -> None:
        self.electronic_osciliator = ElectronicOscillator(maximal_charge, period)
        self.init_pg_sprite(center, sprite)

        self.graph_drawer = GraphDrawer(self.electronic_osciliator.maximal_charge+10, self.electronic_osciliator.maximal_amerage+10, "Заряд", "Сила тока")
        # Прибавляем по 10 к каждому значению, чтобы графики не "упирались" в границы.

        self.inductor_coil_distacne: int = 120
        self.capacitor_distance: int = 120

        self.init_areas(center, screen)

    def init_pg_sprite(self, center, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, "sprites")
        self.image = pygame.image.load(os.path.join(self.img_folder, sprite)).convert()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (center.x, center.y)

    def init_areas(self, center, screen):
        self.amperage_area = Area(
            Point(center.x + self.inductor_coil_distacne, center.y),
            0,
            PURPLE,
            screen
        )
        self.charge_area = Area(
            Point(center.x - self.capacitor_distance, center.y),
            0,
            BLUE,
            screen
        )

    def update(self):
        self.electronic_osciliator.process()
        self.update_areas()
        self.update_graph()

    def update_areas(self):
        self.charge_area.set_radius(int(abs(round(self.electronic_osciliator.charge))))
        self.amperage_area.set_radius(int(abs(round(self.electronic_osciliator.amperage))))
        self.charge_area.update()
        self.amperage_area.update()

    def update_graph(self):
        self.graph_drawer.update(
            self.electronic_osciliator.timer,
            self.electronic_osciliator.charge,
            self.electronic_osciliator.amperage
        )

    def abort(self):
        self.graph_drawer.close()


class ElectronicOscillator:
    def __init__(self, maximal_charge: float, period: float) -> None:
        self.maximal_charge = maximal_charge
        self.period = period

        self.timer: float = 0

    def process(self) -> None:
        self.add_time()

    def add_time(self) -> None:
        self.timer += 0.066 # Т.к. обнвление кадра происходит 15 раз в сек. добаляем 1 / 15

    @property
    def charge(self) -> float:
        return self.maximal_charge * math.cos(self.cyclic_frequency * self.timer)

    @property
    def amperage(self) -> float:
        return -self.maximal_amerage * math.sin(self.cyclic_frequency * self.timer)

    @property
    def maximal_amerage(self) -> float:
        return self.cyclic_frequency * self.maximal_charge

    @property
    def cyclic_frequency(self) -> float:
        return 2 * PI / self.period


class Area:
    def __init__(self, center: Point, radius: int, maximal_color: tuple, screen) -> None:
        self.center = center
        self.radius = radius
        self.width = self.radius * 2
        self.maximal_color = maximal_color
        self.screen = screen

        self.make_corners()
        self.sqaure: int = 5
        # В целях оптимизации, мы отрисовывавем не каждый пиксель, а "квадраты".
        # Все вычесление производятся для центра квадрата. self.square - это длинна стороны такого квадрата.

    def make_corners(self):
        self.left_corner = Point(
            self.center.x - self.radius,
            self.center.y - self.radius
        )
        self.right_corner = Point(
            self.center.x + self.radius,
            self.center.y + self.radius
        )

    def set_radius(self, value):
        if value == 0:
            value = 1
        self.radius = value
        self.make_corners()

    def update(self):
        for y in range(self.left_corner.y, self.right_corner.y+1, self.sqaure):
            for x in range(self.left_corner.x, self.right_corner.x+1, self.sqaure):
                self.draw_area(x, y)

    def draw_area(self, x, y):
        distance = self.get_distance(x+self.sqaure/2, y+self.sqaure/2)
        ratio = -(distance/self.radius)**2 + 1 # Формула, выведенная мной для вычисления яркости.
        red, green, blue = self.maximal_color
        red *= ratio
        green *= ratio
        blue *= ratio
        self.draw_square(x, y, (red, green, blue))

    def get_distance(self, x, y):
        x_distance = self.center.x - x
        y_distance = self.center.y - y
        result = math.sqrt(
            x_distance ** 2 + y_distance ** 2
        )
        return result if result <= self.radius else self.radius

    def draw_square(self, x, y, color):
        for i in range(y, y+self.sqaure):
            for j in range(x, x+self.sqaure):
                gfxdraw.pixel(self.screen, j, i, color)


#FPS = 15
#pygame.mixer.init()
#screen = pygame.display.set_mode((800, 400))
#
#clock = pygame.time.Clock()
#all_sprites = pygame.sprite.Group()
#electr = ElectronicOscillatorDrawer(
#    Point(400, 200),
#    30,
#    2,
#    "electronic_oscillator.png",
#    screen
#)
#all_sprites.add(electr)
#
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
#    screen.fill((0, 0, 0))
#    start = time.time()
#
#
#    # Рендеринг
#    all_sprites.update()
#    all_sprites.draw(screen)
#
#    # После отрисовки всего, переворачиваем экран
#    pygame.display.flip()
#    end = time.time()
#    print(end - start)
#
#
#pygame.quit()
#