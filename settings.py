class Settings:
    def __init__(self):
        # Настройки игры
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # Настройки корабля
        self.ship_limit = 3

        # Настройки для пуль
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255,56,71
        self.bullet_allowed = 5

        # Настройки флота пришельцев
        self.fleet_drop_speed = 10
        
        # Изменение скорости игры
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    # Объединяет динамические значения объектов для дальнейшего из менения
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 0.8

        # Посчет очков
        self.alien_points = 50

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

    #Увеличение скорости,стоимости объектов пропорционально уровню сложности
    def icrease_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
    

        



        
