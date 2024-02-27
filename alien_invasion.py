import sys
import pygame
from settings import Game_Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button

from game_stats import GameStats

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""
    def __init__(self):
        pygame.init()
        self.settings = Game_Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_heigth = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Создание кнопки
        self.play_button = Button(self, "Play")

        # НАЗНАЧЕНИЕ ЦВЕТА ФОНА
        self.bg_color = self.settings.bg_color

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
               
            
    def _check_events(self):
        # Отслеживание событий клавиатуры и мыши
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                #Тут забиндили проверку событие нажатия на клавиатуру, типа если нажали, то проверять на следующие события
                elif event.type == pygame.KEYDOWN:
                    #тут проверяем нажали ли конкретно на клаве стрелку вправо и если да то выставляем флаг в тру
                    self._check_keydown_events(event)
                #А тут проверяме отпустили ли кнопку нажатую, если отпустили, то флаг в фолс
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Сброс игровой статистики
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            #Очистка списка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(True)
                
    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        #Обновление позиций снаряда
        self.bullets.update()
        #Удаление снарядов вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)     
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        #Проверка попаданий в пришельцев
        #При обнаружении попадания дулаить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if not self.aliens:
            #Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()
        #Проверка коллизий пришелец-корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Проверить добрались ли пришельцы до нижнего края крана
        self._check_aliens_bottom()

    def _update_screen(self):
         #Тут у нас перерисовывается экран
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

            #Кнопка Плэй отображается в том случае, если игра не активна
            if not self.stats.game_active:
                self.play_button.draw_button()

            #Отображение последнего прорисованного экрана
            pygame.display.flip()

    def _check_keydown_events(self,event):
         """Реагирует на нажатие клавиш"""
         if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = True
         if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
         elif event.key == pygame.K_q:
            sys.exit()
         elif event.key == pygame.K_SPACE:
             self._fire_bullet()

    def _check_keyup_events(self, event):
         """Реагирует на отпускание клаваишь"""
         if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = False
         if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Создание флота вторжения"""
        #Создание пришельца и вычисление кол-ва пришельцев в ряду
        #Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_heigth = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        #Определяет кол-во рядов помещающихся на экране
        ship_heigth = self.ship.rect.height
        available_space_y = (self.settings.screen_heigth - (3 * alien_heigth) - ship_heigth)
        number_rows = available_space_y // (2 * alien_heigth)

        #Создание первого ряда пришельцев
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                #Создание пришельца и размещение его в ряду
                self._create_alien(alien_number, row_number)
           

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_heigth = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """опускает весь флот и меняет его направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обработка столкновения корабля с пришельцем"""
        if self.stats.ships_left > 0:
            #Уменьшение шип лефт
            self.stats.ships_left -= 1

            #очитска списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            #Создание нового флота
            self._create_fleet()
            self.ship.center_ship()

            #Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до низа экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #ПРоисходит то же что и при столкновении с кораблем
                self._ship_hit()
                break

if __name__ == '__main__':
    #СОздание экземляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()