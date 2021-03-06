import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    # Класс корабля игрока
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        # Инициализируем корабль и задаем начальную позицию
        self.screen = screen
        self.ai_settings = ai_settings
        # Загружаем изображение корабля и получаем прямоугольник
        self.image = pygame.image.load('images/ship.png')

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Каждый новый корабль появляется у нижней части экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохранение вещественной координаты центра
        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False


    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
            #self.rect.centerx += 1
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            #self.rect.centerx -= 1
        self.rect.centerx = self.center


    def blitme(self):
        # Рисует корабль в текущей позиции
        self.screen.blit(self.image,self.rect)


    def center_ship(self):
        """ Размещает корабль в дефолтной позиции. """
        self.center = self.screen_rect.centerx
