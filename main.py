import pygame

from pendulum import PendulumDrawer
from electronic_oscillator import ElectronicOscillatorDrawer
from point import Point

pygame.init()
FONT = pygame.font.Font(None, 30)
COLOR_INACTIVE = (255, 255, 255)

class InputBox:
    def __init__(self, x, y, w, h, color, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self, screen):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, x, y, w, h, color, text) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.active = False
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

    def update(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

FPS = 20
WIDTH = 800
HEIGHT = 400
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
running = True
paused = False
clock = pygame.time.Clock()

MAIN_MENU = "main_menu"
ELECTRONIC_MENU = "electronic_menu"
PENDULUM_MENU = "electronic_menu"
ELECTRONIC_OSCILLATOR = "electronic_oscillator"
PENDULUM = "pendulum"
STATUS = MAIN_MENU

class App:
    def __init__(self) -> None:
        self.init_main_menu()

    def mainloop(self):
        # mainloop выглядит громоздко и уродливо, но,
        # видимо, только так они и пишутся.
        global STATUS, running, paused
        screen.fill(BLACK)
        while running:
            if STATUS == MAIN_MENU:
                for event in pygame.event.get():
                    self.electronic_button.handle_event(event)
                    self.pendulum_button.handle_event(event)

                self.electronic_button.update(screen)
                self.pendulum_button.update(screen)
                if self.electronic_button.active:
                    self.init_electronic_menu()
                    STATUS = ELECTRONIC_MENU
                    continue
                if self.pendulum_button.active:
                    self.init_penulum_menu()
                    STATUS = PENDULUM_MENU
            
            elif STATUS == ELECTRONIC_MENU:
                for event in pygame.event.get():
                    self.electronic_period_button.handle_event(event)
                    self.electronic_next_button.handle_event(event)
                self.electronic_period_button.update(screen)
                self.electronic_next_button.update(screen)
                
                if self.electronic_next_button.active:
                    try:
                        period = int(self.electronic_period_button.text)
                    except ValueError:
                        self.electronic_period_button.text = "Неверно"
                        continue
                    self.init_electronic_oscillator(period)
                    STATUS = ELECTRONIC_OSCILLATOR
            
            elif STATUS == PENDULUM_MENU:
                for event in pygame.event.get():
                    self.pendulum_period_button.handle_event(event)
                    self.pendulum_max_deviation_button.handle_event(event)
                    self.pendulum_next_button.handle_event(event)
                
                self.pendulum_period_button.update(screen)
                self.pendulum_max_deviation_button.update(screen)
                self.pendulum_next_button.update(screen)

                if self.pendulum_next_button.active:
                    try:
                        period = int(self.pendulum_period_button.text)
                        max_devaition = int(self.pendulum_max_deviation_button.text)
                    except ValueError:
                        self.pendulum_period_button.text = "Неверно"
                        self.pendulum_max_deviation_button.text = "Неверно"
                        continue
                    self.init_pendulum(period, max_devaition)
                    STATUS = PENDULUM

            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        if event.key == pygame.K_ESCAPE:
                            self.clear()
                            STATUS = MAIN_MENU
            if paused:
                continue
            all_sprites.update()
            pygame.display.flip()

    def clear(self):
        all_sprites.empty()

    def init_main_menu(self):
        self.electronic_button = Button(250, 150, 300, 50, COLOR_INACTIVE, "Электромгнитные колебания")
        self.pendulum_button = Button(250, 200, 300, 50, COLOR_INACTIVE, "Механчиеские колебания")

    def init_electronic_menu(self):
        self.electronic_period_button = InputBox(250, 150, 300, 50, COLOR_INACTIVE)
        self.electronic_next_button = Button(250, 200, 300, 50, COLOR_INACTIVE, "Продолжить")

    def init_penulum_menu(self):
        self.pendulum_period_button = InputBox(250, 100, 300, 50, COLOR_INACTIVE)
        self.pendulum_max_deviation_button = InputBox(250, 150, 60, 50, COLOR_INACTIVE)
        self.pendulum_next_button = Button(250, 200, 300, 50, COLOR_INACTIVE, "Продолжить")

    def init_electronic_oscillator(self, period):
        global FPS
        FPS = 15
        self.electronic_oscillator = ElectronicOscillatorDrawer(
            Point(400, 200), # центр спрайта колебательного контура
            30, # Максимальный заряд
            period,
            "electronic_oscillator.png",
            screen
        )
        all_sprites.add(self.electronic_oscillator)

    def init_pendulum(self, period, max_deviation):
        global FPS
        FPS = 20
        self.pendulum = PendulumDrawer(
            Point(400, 0), # Точка опоры
            300, # Длинна веревки
            period,
            max_deviation,
            'pendulum.png'
        )
        all_sprites.add(self.pendulum)

#a = Button(250, 150, 300, 50, COLOR_INACTIVE, "Электромгнитные колебания")
#while True:
#    
#    for event in pygame.event.get():
#        a.handle_event(event)
#    print(a.active)
#    pygame.display.flip()
#    screen.fill(BLACK)
app = App()
app.mainloop()