class GameStats():
    """Отслеживание статистики"""

    def __init__(self, ai_game) -> None:
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True
        #Игра запускается в неактивном состоянии
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
