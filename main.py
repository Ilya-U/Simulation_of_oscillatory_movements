import pygame

from pendulum import PendulumDrawner
from electronic_oscillator import ElectronicOscillatorDrawer

pygame.init()
FONT = pygame.font.Font(None, 32)
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


WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
running = True
paused = False
clock = pygame.time.Clock()


class App:
    MAIN_MENU = "main_menu"
    ELECTRONIC_MENU = "electronic_menu"
    PENDULUM_MENU = "electronic_menu"
    ELECTRONIC_OSCILLATOR = "electronic_oscillator"
    PENDULUM = "pendulum"
    STATUS = MAIN_MENU
    FPS = 20

    def __init__(self) -> None:
        self.init_main_menu_button()
        self.electronic_input_button = InputBox(370, 180, 60, 20, COLOR_INACTIVE)
        self.electronic_next_button = Button(370, 220, 60, 20, COLOR_INACTIVE, "Продолжить")
    
    def main(self):
        while running:
            if STATUS == App.MAIN_MENU:
                for event in pygame.event.get():
                    self.electronic_button.handle_event(event)
                    self.pendulum_button.handle_event(event)

                

                if self.electronic_button.active:
                    STATUS = App.ELECTRONIC_MENU
                    continue

                if self.pendulum_button.active:
                    STATUS = App.PENDULUM_MENU
                    continue

            elif STATUS == App.ELECTRONIC_MENU:
                for event in pygame.event.get():
                    self.electronic_input_button.handle_event(event)

                

            elif STATUS == App.PENDULUM_MENU:
                pass

            elif STATUS == App.ELECTRONIC_OSCILLATOR:
                pass

            elif STATUS == App.PENDULUM:
                pass

    def init_main_menu_button(self):
        self.electronic_button = Button(370, 180, 60, 20, COLOR_INACTIVE, "Электромгнитные колебания")
        self.pendulum_button = Button(370, 220, 60, 20, COLOR_INACTIVE, "Механчиеские колебания")
