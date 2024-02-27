import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления снарядами выпущеными кораблем"""

    def __init__(self, ai_game) -> None:
        """Создает объект снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Создани снаряда в позиции (0,0) и назначение правильной позиции.
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,
                                self.settings.bullet_heigth)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        #Обновление позиции снаряда в вещественном формате
        self.y -= self.settings.bullet_speed
        #обновлении позиции прмоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)