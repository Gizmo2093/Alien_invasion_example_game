import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # Функция реагирования на нажатие клавиш (движения)
    if event.key == pygame.K_RIGHT:
        ship.rect.centerx += 1
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.rect.centerx -= 1
        ship.moving_left = True
    # Функция реагирования на нажатие клавиш (выстрела)
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)


def check_kyeup_events(event,ship):
    # Функция реагирования на отпускание клавиш
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Обработка нажатий мыши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        if event.type == pygame.KEYUP:
            check_kyeup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)


def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    # Запуск игры по нажатию кнопки "Play"
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс скорости игры
        ai_settings.initialize_dynamic_settings()
        # Сброс статистики игры
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        pygame.mouse.set_visible(False)

        # Сброс списков пришельце и пуль при сбросе статистики игры
        aliens.empty()
        bullets.empty()

        # Создание нового флота при сбросе статистики игры
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings, screen,stats, sb, ship, aliens, bullets, play_button):
    # Обновляет изображения на экране и обновляет его
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Кнопка Play отображается в неактивном состоянии игры
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen,stats, sb, ship, aliens,bullets):
    # Удаление лишних пуль
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Проверка попадания пули в пришельца и удаление обоих объектов
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)


def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """ Обработка коллизий пуль с пришельцами. """
    # Удаление пуль и пришельцев, участвующих в коллизиях
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота.
        bullets.empty()
        ai_settings.icrease_speed()
        # Увеличение уровня
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_rows(ai_settings, ship_height, alien_height):
    """ Определяет количество рядов, помещающихся на экране. """
    avaliable_space_y = (ai_settings.screen_height -(3 * alien_height) - ship_height)
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings,alien_width):
    """ Вычисляет количество пришельцев в ряду. """
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings,screen,aliens,alien_number, row_number):
    """ Создает пришельца и размещает его в ряду. """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    """ Создает флот пришельцев. """
    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,alien.rect.height)
    # Создание первого ряда пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """ Реагирует на достижение пришельцем края экрана. """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ Опускает весь флот и меняет направление флота """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Обрабатывает столкновение корабля с пришельцем """
    if stats.ships_left > 0:
        # Уменьшает жизни - ship_left
        stats.ships_left -= 1
        # Очитска списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Обновление игровой информации
        sb.prep_ships()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Проверка добрались ли пришельцы до нижней части экрана """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же что и при коллизии с кораблем
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats,sb):
    """ Проверка наличия нового рекорда """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_aliens(ai_settings,screen, stats, sb, ship, aliens, bullets):
    """ Проверяет, достиг ли флот края экрана, после чего обновляет позиции всех пришельцев во флоте """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    """ Проверка коллизии пришелец - корабль """
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

