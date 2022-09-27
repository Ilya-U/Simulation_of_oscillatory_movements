import math
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

        self.graph_drawner = PendulumGraphDrawer()

    def update(self) -> None:
        self.update_pendulum()
        #self.draw_graph()

    def update_pendulum(self):
        self.pendulum.move()
        self.rect.center = (self.pendulum.current_position.x, self.pendulum.current_position.y)

    def draw_graph(self):
        self.graph_drawner.update(self.pendulum)



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

        self.time = 1

    def move(self) -> None:
        try: # TODO придумать что-нибудь более изобретательное
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
    def speed(self):
        return -self.maximal_speed * math.sin(self.time * self.cyclic_frequency)

    @property
    def maximal_speed(self):
        return self.maximal_deviation * self.cyclic_frequency

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


class PendulumGraphDrawer:
    def __init__(self) -> None:
        self.fig = plt.figure()

        self.trajectory_graph = self.fig.add_subplot(2, 1, 1)   
        self.trajectory_graph.set_xlim((0, 60))
        self.trajectory_graph.set_ylim((-400, 400))
        self.trajectory_graph_data_x = []
        self.trajectory_graph_data_y = []
        
        self.speed_graph = self.fig.add_subplot(2, 1, 2)
        self.speed_graph.set_xlim((0, 60))
        self.speed_graph.set_ylim((-400, 400))
        self.speed_graph_data_x = []
        self.speed_graph_data_y = []

    def update(self, pendulum: Pendulum):
        self.update_trajectory_graph(pendulum)
        self.update_speed_graph(pendulum)
        plt.draw()
        plt.clf()

    def update_trajectory_graph(self, pendulum: Pendulum):
        self.trajectory_graph_data_x.append(pendulum.time)
        self.trajectory_graph_data_y.append(pendulum.math_position_in_trajectory)
        self.trajectory_graph.clear()
        self.trajectory_graph.plot(
            self.trajectory_graph_data_x, 
            self.trajectory_graph_data_y,
            color="red"
        )

    def update_speed_graph(self, pendulum: Pendulum):
        self.speed_graph_data_x.append(pendulum.time)
        self.speed_graph_data_y.append(pendulum.speed)
        self.speed_graph.clear()
        self.speed_graph.plot(
            self.speed_graph_data_x,
            self.speed_graph_data_y,
            color="orange"
        )


FPS = 50
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("TEST")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

pendulum = PendulumDrawner(Point(600, 0), 350, 2, 40)
all_sprites.add(pendulum)

# Цикл игры
running = True
paused = False

while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_SPACE:
            paused = True
    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()


pygame.quit()
# pyinstaller -F --add-data "sprites\\pendulum.png;." pendulum.pyw          |Компиляция с картинками
# pyinstaller -F --add-data "sprites\\pendulum.png;.\sprites" pendulum.pyw  |
