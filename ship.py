import pygame

class Ship():
    """Класс для управления кораблем"""

    def __init__(self, ai_game) -> None:
        """Инициализирует корабль и задает его начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings
        #Флаги перемещения
        self.moving_rigth = False
        self.moving_left = False

        #Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        #Каждый новый корабль появляется у нижней части экрана
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        #Обновляет атрибут х объекта ship, не rect
        if self.moving_rigth and self.rect.right < self.screen_rect.width:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Обновление атрибута rect на основании self.x
        self.rect.x = self.x

    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)