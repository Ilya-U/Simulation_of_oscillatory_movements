import math
import pygame
from pygame import gfxdraw
import os
import time

from point import Point
from graph_drawer import GraphDrawer

PI = math.pi


class ElectronicOscillatorDrawer:
    def __init__(self, maximal_charge: float, period: float, sprite: str) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.electronic_osciliator = ElectronicOscillator(maximal_charge, period)
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, "sprites")
        self.image = pygame.image.load(os.path.join(self.img_folder, sprite)).convert()

        self.rect = self.image.get_rect()

        self.graph_drawer = GraphDrawer(self.electronic_osciliator.maximal_charge+10, self.electronic_osciliator.maximal_amerage+10, "Заряд", "Сила тока")
        # Прибавляем по 10 к каждому значению, чтобы графики не "упирались" в границы.


class ElectronicOscillator:
    def __init__(self, maximal_charge: float, period: float) -> None:
        self.maximal_charge = maximal_charge
        self.period = period

        self.timer: float = 0

    def process(self) -> None:
        self.add_time()

    def add_time(self) -> None:
        self.timer += 0.05 # Т.к. обнвление кадра происходит 20 раз в сек. добаляем 1 / 20

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
    def __init__(self, center: Point, radius: int, maximal_color) -> None:
        # ну наконец-то!
        # Все дело в несоответсвии фаткического центра и 
        # центра внутри массива!
        self.screen_center = center
        self.center = Point(
            radius,
            radius
        )
        self.radius = radius
        self.width = self.radius * 2
        self.maximal_color = maximal_color

        self.left_corner = Point(
            self.screen_center.x - self.radius,
            self.screen_center.y - self.radius
        )
        self.all_points: list[list[tuple]] = [(self.width) * [None]] * (self.width)
        self.distances: list[list[tuple]] = [(self.width) * [None]] * (self.width) # Удалить после дебага!
        self.ratios: list[list[tuple]] = [(self.width) * [None]] * (self.width) # Удалить после дебага!

    def set_maximal_light(self, value):
        self.maximal_color = value

    def update(self, screen):
        self.count_all_points()
        self.draw_all_points(screen)

    def count_all_points(self):
        for y in range(len(self.all_points)):
            for x in range(len(self.all_points[y])):
                if x == 19 and y == 19:
                    pass
                distance = self.get_distance(x, y)
                ratio = -((distance / self.radius) ** 2) + 1
                red, green, blue = self.maximal_color
                red *= ratio
                green *= ratio
                blue *= ratio
                self.distances[y][x] = round(distance, 4)# Удалить после дебага!
                self.ratios[y][x] = round(ratio, 2)# Удалить после дебага!
                self.all_points[y][x] = (red, green, blue)

    def get_distance(self, x, y):
        if x == 10 and y == 0:
            pass
        if x == 0 and y == 10:
            pass
        if x == 10 and y == 10:
            pass
        x_distance = self.center.x - x
        y_distance = self.center.y - y
        ans = math.sqrt(
            x_distance ** 2 +
            y_distance ** 2
        )
        return ans if ans <= self.radius else self.radius

    def draw_all_points(self, screen):
        for y in range(len(self.all_points)):
            for x in range(len(self.all_points[y])):
                current_color = self.all_points[y][x]
                x_for_screen = x + self.left_corner.x
                y_for_screen = y + self.left_corner.y
                gfxdraw.pixel(screen, x_for_screen, y_for_screen, current_color)


FPS = 20
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400))

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
area = Area(Point(400, 200),
    10,
    (255, 255, 255)
    )
i = 0
while i <= 255:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    
        clock.tick(FPS)
        start = time.time()
        area.update(screen)
        end = time.time()
        print(start - end)
        pygame.display.flip()
