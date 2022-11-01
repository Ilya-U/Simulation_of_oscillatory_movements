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
    def __init__(self, left_corner: Point, right_corner: Point, maximal_light: tuple) -> None:
        self.left_corner = left_corner
        self.right_corner = right_corner

        self.width = self.right_corner.x - self.left_corner.x
        self.height = self.right_corner.y - self.left_corner.y
        
        self.x_maximal_distance = self.width / 2
        self.y_maximal_distance = self.height / 2

        self.center = Point(self.x_maximal_distance, self.y_maximal_distance)

        self.maximal_light = maximal_light

        self.colors_of_points: list[list[tuple]] = [[None] * self.width] * self.height

    def set_maximal_light(self, value):
        self.maximal_light = value

    def update(self, screen):
        self.count_all_points()
        self.draw_all_points(screen)

    def draw_all_points(self, screen):
        for x in range(len(self.colors_of_points)):
            for y in range(len(self.colors_of_points[x])):
                current_color = self.colors_of_points[x][y]
                x_for_screen = x + self.left_corner.x
                y_for_screen = y + self.left_corner.y

                gfxdraw.pixel(screen, x_for_screen, y_for_screen, current_color)

    def count_all_points(self):
        for x in range(len(self.colors_of_points)):
            for y in range(len(self.colors_of_points[x])):
                red, green, blue = self.maximal_light
                current_coefficient = self.get_coefficient(x, y)
                
                red *= current_coefficient
                green *= current_coefficient
                blue *= current_coefficient

                self.colors_of_points[x][y] = (
                    int(round(red)),
                    int(round(green)),
                    int(round(blue))
                )

    def get_coefficient(self, x, y):
        current_distance = self.get_distance(x, y)
        result = -(current_distance / self.y_maximal_distance) ** 2 + 1
        
        return result if result > 0 else 0
    
    def get_distance(self, x, y):
        x_distance = self.center.x - x
        y_distance = self.center.y - y

        return math.sqrt(
            (x_distance) ** 2 +
            y_distance ** 2
        )

FPS = 20
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400))

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
area = Area(Point(0, 0),
    Point(400, 400),
    (0, 0, 0)
    )
i = 0
while True:
        clock.tick(FPS)
        area.set_maximal_light((0, 0, i))
        start = time.time()
        area.update(screen)
        i += 100
        end = time.time()
        print(start - end)
        pygame.display.flip()
