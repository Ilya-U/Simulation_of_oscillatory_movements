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
    def __init__(self, center: Point, radius: int, maximal_color: tuple, screen) -> None:
        self.center = center
        self.radius = radius
        self.width = self.radius * 2
        self.maximal_color = maximal_color
        self.screen = screen

        self.left_corner = Point(
            self.center.x - self.radius,
            self.center.y - self.radius
        )
        self.right_corner = Point(
            self.center.x + self.radius,
            self.center.y + self.radius
        )

    def update(self):
        for y in range(self.left_corner.y, self.right_corner.y+1):
            for x in range(self.left_corner.x, self.right_corner.x+1):
                self.draw_point(x, y)

    def draw_point(self, x, y):
        distance = self.get_distance(x, y)
        ratio = -(distance/self.radius)**2 + 1
        red, green, blue = self.maximal_color
        red *= ratio
        green *= ratio
        blue *= ratio
        gfxdraw.pixel(screen, x, y, (red, green, blue))

    def get_distance(self, x, y):
        x_distance = self.center.x - x
        y_distance = self.center.y - y
        result = math.sqrt(
            x_distance ** 2 + y_distance ** 2
        )
        return result if result <= self.radius else self.radius

FPS = 20
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400))

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
area = Area(Point(400, 200),
    100,
    (128, 0, 255),
    screen
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
        area.update()
        end = time.time()
        print(end - start)
        pygame.display.flip()
