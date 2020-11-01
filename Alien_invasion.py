import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
import sys
from game_stats import GameStats
from Button import Button
from scoreboard import Scoreboard

def run_game():
    # Создает объект экрана
    pygame.init()
    title = pygame.display.set_caption("Alien Invasion version.2")

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    bg_color = (ai_settings.bg_color)

    # Экземпляр корабля
    ship = Ship(ai_settings,screen)

    # Экземпляр пришельца
    alien = Alien(ai_settings,screen)

    # Группы пуль и флота пришельцев
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)
    bullets = Group()

    # Экземпляры Gamestats и Scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    # Кнопка Play
    play_button = Button(ai_settings, screen, "Play")

    # Главный цикл игры
    while True:
        gf.check_events(ai_settings, screen,stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen,stats,sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets, play_button)

run_game()
