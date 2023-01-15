import pygame
import time

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
        self.width = w

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self, screen):
        width = self.width
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


class MainMenu:
    def __init__(self) -> None:
        self.electronic_button = Button(250, 150, 300, 50, COLOR_INACTIVE, "Электромгнитные колебания")
        self.pendulum_button = Button(250, 200, 300, 50, COLOR_INACTIVE, "Механчиеские колебания")
        self.next_stage = None

    def update(self, screen, events):
        for event in events:
            self.handle_event(event)
        self.electronic_button.update(screen)
        self.pendulum_button.update(screen)
        self.make_logic()

    def handle_event(self, event):
        self.electronic_button.handle_event(event)
        self.pendulum_button.handle_event(event)

    def make_logic(self):
        if self.electronic_button.active:
            self.next_stage = ElectronicMenu()
            return
        if self.pendulum_button.active:
            self.next_stage = PendulumMenu()
            return
    
    def user_sprite(self):
        return None

    def get_next_stage(self):
        return self.next_stage


class ElectronicMenu:
    def __init__(self) -> None:
        self.electronic_period_button = InputBox(250, 150, 300, 50, COLOR_INACTIVE, text="Период, с")
        self.electronic_next_button = Button(250, 200, 300, 50, COLOR_INACTIVE, "Продолжить")
        self.sprite = None
        self.next_stage = None

    def update(self, screen, events):
        for event in events:
            self.handle_event(event)
        self.electronic_period_button.update(screen)
        self.electronic_next_button.update(screen)
        self.make_logic()

    def handle_event(self, event):
        self.electronic_period_button.handle_event(event)
        self.electronic_next_button.handle_event(event)

    def make_logic(self):
        if self.electronic_next_button.active:
            try:
                period = float(self.electronic_period_button.text)
            except ValueError:
                self.electronic_period_button.text = "Неверно"
            else:
                self.init_sprite(period)
                self.electronic_next_button.active = False
                self.next_stage = NoMenu()

    def init_sprite(self, period):
        self.sprite = ElectronicOscillatorDrawer(
            Point(400, 200), # центр спрайта колебательного контура
            30, # Максимальный заряд
            period,
            "electronic_oscillator.png",
            screen
        )
    
    def user_sprite(self):
        return self.sprite
    
    def get_next_stage(self):
        return self.next_stage


class PendulumMenu:
    def __init__(self) -> None:
        self.pendulum_period_button = InputBox(250, 100, 300, 50, COLOR_INACTIVE, text="Период")
        self.pendulum_max_deviation_button = InputBox(250, 150, 300, 50, COLOR_INACTIVE, text="Макс. отклонение")
        self.pendulum_next_button = Button(250, 200, 300, 50, COLOR_INACTIVE, "Продолжить")
        self.sprite = None
        self.next_stage = None

    def update(self, screen, events):
        for event in events:
            self.handle_event(event)
        self.pendulum_period_button.update(screen)
        self.pendulum_max_deviation_button.update(screen)
        self.pendulum_next_button.update(screen)
        self.make_logic()

    def handle_event(self, event):
        self.pendulum_period_button.handle_event(event)
        self.pendulum_max_deviation_button.handle_event(event)
        self.pendulum_next_button.handle_event(event)

    def make_logic(self):
        if self.pendulum_next_button.active:
            try:
                period = float(self.pendulum_period_button.text)
                max_devaition = float(self.pendulum_max_deviation_button.text)
            except ValueError:
                self.pendulum_period_button.text = "Неверно"
                self.pendulum_max_deviation_button.text = "Неверно"
            else:
                self.init_sprite(period, max_devaition)
                self.pendulum_next_button.active = False
                self.next_stage = NoMenu()

    def init_sprite(self, period, max_deviation):
        self.sprite = PendulumDrawer(
            Point(400, 0), # Точка опоры
            300, # Длинна веревки
            period,
            max_deviation,
            'pendulum.png',
            screen
        )

    def user_sprite(self):
        return self.sprite

    def get_next_stage(self):
        return self.next_stage


class NoMenu:
    def update(self, screen, events):
        pass

    def user_sprite(self):
        return None

    def get_next_stage(self):
        return None

    def handle_event(self, event):
        pass


def abort_all_sprites(sprites_group):
    sprites = sprites_group.sprites()
    for i in sprites:
        i.abort()

FPS = 20
WIDTH = 800
HEIGHT = 400
BLACK = (0, 0, 0)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
running = True
paused = False
clock = pygame.time.Clock()

app = MainMenu()

while running:
    pygame_events = pygame.event.get()
    screen.fill(BLACK)
    clock.tick(FPS)
    sprite = app.user_sprite()
    next_menu_stage = app.get_next_stage()
    app.update(screen, pygame_events)

    app = next_menu_stage if next_menu_stage is not None else app
    
    if sprite is not None:
        if isinstance(sprite, ElectronicOscillatorDrawer):
            FPS = 15
        if isinstance(sprite, PendulumDrawer):
            FPS = 20
        all_sprites.add(sprite)

    for event in pygame_events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_ESCAPE:
                app = MainMenu()
                abort_all_sprites(all_sprites)
                all_sprites.empty()
                paused = False

    if paused:
        continue
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
