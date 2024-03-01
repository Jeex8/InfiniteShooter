import pygame
import os
import sys
import random
import math


def load_image(name, colorkey=None):
    # Функция загрузки пути изображения
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def fire(hero_x, hero_y):
    # Функция пуска и вычисления полета пули
    global ammo
    if ammo != 0:
        root = os.path.join('data', 'stvol.mp3')
        sound = pygame.mixer.Sound(root)
        sound.set_volume(0.22)
        sound.play()
        ammo -= 1
        bullet = pygame.sprite.Sprite()
        bullet.image = load_image('bullet.png')
        colorkey3 = bullet.image.get_at((0, 0))
        bullet.image.set_colorkey(colorkey3)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bullet.rect = bullet.image.get_rect()
        bullet.rect.x = hero_x + 20
        bullet.rect.y = hero_y + 30
        # Формулы вычисляющие координаты полета и придающие скорость
        bullet.speed_y = (mouse_y - bullet.rect.y) / 5
        bullet.speed_x = (mouse_x - bullet.rect.x) / 5

        bullets.add_internal(bullet)
        shoot(bullet.speed_x, bullet.speed_y, bullet)


def shoot(speed_x, speed_y, bullet):
    # Функция функция движения пули
    bullet.rect.x += speed_x
    bullet.rect.y += speed_y
    if bullet.rect.x > 1270 or bullet.rect.x < 10 or bullet.rect.y > 710 or bullet.rect.y < 10:
        bullets.remove_internal(bullet)


def enemy_shoot(speed_x, speed_y, enemy_bullet):
    # Функция полета пули врага, и её столкновения с персонажем
    global player_hp
    global player_armor
    enemy_bullet.rect.x += speed_x
    enemy_bullet.rect.y += speed_y
    if pygame.sprite.spritecollide(enemy_bullet, all_sprites, False):
        root = os.path.join('data', 'stvol.mp3')
        sound = pygame.mixer.Sound(root)
        sound.set_volume(0.03)
        sound.play()
        if player_armor - 5 < 0:
            root = os.path.join('data', 'stvol.mp3')
            sound = pygame.mixer.Sound(root)
            sound.set_volume(0.22)
            sound.play()
            armor_pier = player_armor - 5
            player_hp += armor_pier
        else:
            root = os.path.join('data', 'hit.mp3')
            sound = pygame.mixer.Sound(root)
            sound.set_volume(0.22)
            sound.play()
            player_armor -= 5
    if enemy_bullet.rect.x > 1270 or enemy_bullet.rect.x < 10 or enemy_bullet.rect.y > 710 or enemy_bullet.rect.y < 10:
        enemy_bullets.remove_internal(enemy_bullet)


def armor(vest):
    # Функция подбирания брони
    global player_armor
    stuff.remove_internal(vest)
    player_armor += 40
    if player_armor > 100:
        player_armor = 100


def enemiesai(enemy, hero_x, hero_y):
    # Функция ИИ противников: алгоритм движения, смерти, замечен ли персонаж, или нет.
    global enemy_ticks
    if pygame.sprite.spritecollide(enemy, bullets, True):
        enemy.hp -= 20
    if enemy.hp <= 0:
        armor_vest = pygame.sprite.Sprite()
        armor_vest.image = load_image('armor2.png')
        colorkey2 = armor_vest.image.get_at((0, 0))
        armor_vest.image.set_colorkey(colorkey2)
        armor_vest.rect = armor_vest.image.get_rect()
        armor_vest.rect.x = enemy.rect.x
        armor_vest.rect.y = enemy.rect.y
        stuff.add_internal(armor_vest)
        root = os.path.join('data', 'dead.mp3')
        sound = pygame.mixer.Sound(root)
        sound.set_volume(0.20)
        sound.play()
        enemies_sprites.remove_internal(enemy)
    if 0 < hero_x - enemy.rect.x < 150 or 0 < hero_y - enemy.rect.y < 150 or \
            0 > hero_x - enemy.rect.x > -150 or 0 > hero_y - enemy.rect.y > -150:
        if enemy.wait is False:
            enemy_ticks = pygame.time.get_ticks()
            enemy.wait = True
        else:
            if (pygame.time.get_ticks() - enemy_ticks) / 120 > 4:
                enemiesshoot(enemy, hero_x, hero_y)
    else:
        if enemy.rect.x < 640:
            enemy.rect.x += 2
        elif enemy.rect.x > 640:
            enemy.rect.x -= 2
        if enemy.rect.y < 360:
            enemy.rect.y += 2
        elif enemy.rect.y > 360:
            enemy.rect.y -= 2


def enemiesshoot(enemy, hero_x, hero_y):
    # Функция стрельбы противников
    enemy.wait = False
    rel_x, rel_y = sprite.rect.x - enemy.rect.x, sprite.rect.y - enemy.rect.y
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    enemy.image = pygame.transform.rotate(load_image('chel3.png'), int(angle))
    colorkey3 = enemy.image.get_at((0, 0))
    enemy.image.set_colorkey(colorkey3)
    enemy_bullet = pygame.sprite.Sprite()
    enemy_bullet.image = load_image('bullet.png')
    colorkey3 = enemy_bullet.image.get_at((0, 0))
    enemy_bullet.image.set_colorkey(colorkey3)
    enemy_bullet.rect = enemy_bullet.image.get_rect()
    enemy_bullet.rect.x = enemy.rect.x
    enemy_bullet.rect.y = enemy.rect.y
    # Переработанная формула стрельбы для противников
    enemy_bullet.speed_y = (hero_y + 12.5 - enemy_bullet.rect.y) / 2
    enemy_bullet.speed_x = (hero_x - 12.5 - enemy_bullet.rect.x) / 2

    enemy_bullets.add_internal(enemy_bullet)
    enemy_bullet.rect.x += enemy_bullet.speed_x
    enemy_bullet.rect.y += enemy_bullet.speed_y


def enemies(wave):
    # Функция спавна противников
    for v in range(wave):
        enemy = pygame.sprite.Sprite()
        enemy.image = load_image('chel3.png')
        enemy.image.set_colorkey(colorkey1)
        enemy.rect = enemy.image.get_rect()
        enemy_random_spawn1 = random.choice([0, 1280, 1, 720])
        enemy.wait = False
        if enemy_random_spawn1 == 0 or enemy_random_spawn1 == 1280:
            enemy_random_spawn2 = random.randint(0, 720)
            enemy.rect.x = enemy_random_spawn1
            enemy.rect.y = enemy_random_spawn2
        elif enemy_random_spawn1 == 1 or enemy_random_spawn1 == 720:
            enemy_random_spawn2 = random.randint(0, 1280)
            enemy.rect.x = enemy_random_spawn2
            enemy.rect.y = enemy_random_spawn1
        elif enemy_random_spawn1 == 1 or enemy_random_spawn1 == 0:
            enemy_random_spawn2 = random.randint(0, 720)
            enemy.rect.x = enemy_random_spawn1
            enemy.rect.y = enemy_random_spawn2
        elif enemy_random_spawn1 == 1 or enemy_random_spawn1 == 1:
            enemy_random_spawn2 = random.randint(0, 1280)
            enemy.rect.x = enemy_random_spawn2
            enemy.rect.t = enemy_random_spawn1
        enemy.hp = 40
        enemies_sprites.add_internal(enemy)


pygame.init()
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('InfiniteShooter')
fps = 60
x_player = 640
y_player = 360
karta = load_image('karta.jpg')
sprite = pygame.sprite.Sprite()
sprite.image = load_image('chel3.png').convert_alpha(screen)
colorkey1 = sprite.image.get_at((0, 0))
sprite.image.set_colorkey(colorkey1)
sprite.rect = sprite.image.get_rect()
sprite.rect.x = x_player
sprite.rect.y = y_player
all_sprites = pygame.sprite.Group()
all_sprites.add(sprite)
stuff = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
ammo = 10
wave_count = 0
player_hp = 100
player_armor = 100
reloading = False
start_ticks = pygame.time.get_ticks()
enemy_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True
end = False
font_game = pygame.font.Font(None, 35)
reload_message = font_game.render('Press R to reload', True,
                                  (15, 15, 15))
wave_message = font_game.render('Press G to start new wave', True,
                                (15, 15, 15))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or player_hp <= 0:
            end = True
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            sprite.rect.top -= 3
            if sprite.rect.top < 5:
                sprite.rect.top += 4
        if key[pygame.K_s]:
            sprite.rect.top += 3
            if sprite.rect.top > 650:
                sprite.rect.top -= 4
        if key[pygame.K_a]:
            sprite.rect.left -= 3
            if sprite.rect.left < 5:
                sprite.rect.left += 4
        if key[pygame.K_d]:
            sprite.rect.left += 3
            if sprite.rect.left > 1210:
                sprite.rect.left -= 4
        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = pygame.mouse.get_pos()
            rel_x, rel_y = mousex - sprite.rect.x, mousey - sprite.rect.y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            sprite.image = pygame.transform.rotate(load_image('chel3.png'), int(angle))
            sprite.image.set_colorkey(colorkey1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            fire(sprite.rect.x, sprite.rect.y, )
        if key[pygame.K_g] and event.type == pygame.KEYDOWN:
            stuff = pygame.sprite.Group()
            player_hp = 100
            wave_count += 1
            enemies(wave_count)
        if key[pygame.K_r]:
            ammo = 0
            reloading = True
            start_ticks = pygame.time.get_ticks()
        if reloading is True:
            if (pygame.time.get_ticks() - start_ticks) / 120 > 10:
                ammo = 10
                reloading = False
    for e in stuff.sprites():
        if pygame.sprite.spritecollide(e, all_sprites, False):
            root = os.path.join('data', 'armor.mp3')
            sound = pygame.mixer.Sound(root)
            sound.set_volume(0.40)
            sound.play()
            armor(e)
        else:
            break
    for i in bullets.sprites():
        shoot(i.speed_x, i.speed_y, i)
    for j in enemy_bullets.sprites():
        enemy_shoot(j.speed_x, j.speed_y, j)
    for w in enemies_sprites.sprites():
        enemiesai(w, sprite.rect.x, sprite.rect.y)
    screen.blit(load_image('karta.jpg'), (0, 0))
    if wave_count == 0:
        screen.blit(reload_message, (970, 650))
        screen.blit(wave_message, (970, 690))
    pygame.draw.rect(screen, (230, 40, 70),
                     (2, 2, 110, 35), 6)
    pygame.draw.rect(screen, (70, 90, 220),
                     (2, 40, 110, 35), 6)
    pygame.draw.rect(screen, (230, 40, 70),
                     (8, 2, player_hp, 29))
    pygame.draw.rect(screen, (70, 90, 220),
                     (8, 40, player_armor, 29))
    stuff.draw(screen)
    bullets.draw(screen)
    enemy_bullets.draw(screen)
    all_sprites.draw(screen)
    enemies_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.draw.rect(screen, (255, 255, 255),
                 (0, 0, 1280, 720))
font = pygame.font.Font(None, 72)
font2 = pygame.font.Font(None, 52)
final = font.render('Игра окончена', True,
                    (55, 55, 55))
final1 = font2.render('Вы смогли прожить', True,
                      (55, 55, 55))
final2 = font2.render('Волн', True,
                      (55, 55, 55))
wave_count_message = font2.render(str(wave_count), True,
                                  (55, 55, 55))
screen.blit(final, (500, 150))
screen.blit(final1, (350, 400))
screen.blit(final2, (780, 400))
screen.blit(wave_count_message, (720, 400))
root = os.path.join('data', 'dead.mp3')
sound = pygame.mixer.Sound(root)
sound.set_volume(0.40)
sound.play()
while end is True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            end = False
            break
        pygame.display.flip()
        clock.tick(fps)
