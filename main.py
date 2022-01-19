import sqlite3

import pygame
import os
import sys

from random import randint
from Sprites import Tile, Enemy, Player, \
    all_sprites, block_group, tiles_group, enemy_group, player_group
from Fight import FightScreen

pygame.init()
SIZE = WI, HE = 660, 660
FPS = 50
TILE_S = 66
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Игре нужно название")
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        return
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': pygame.transform.scale(load_image('box.png'), (66, 66)),
    'enemy': pygame.transform.scale(load_image('box.png'), (66, 66)),
    'empty': pygame.transform.scale(load_image('grass.png'), (66, 66))
}
player_image = pygame.transform.scale(load_image('mar.png'), (66, 66))

PLAYER = Player(5, 5, player_image)


def load_level(filename):
    # Функция загрузки уровня из тхт файла
    filename = "maps/" + filename
    with open(filename, "r", encoding="utf8") as mapFile:
        level_map = [line.strip() for line in mapFile]
    return list(map(lambda x: x.ljust(10, "."), level_map))


def load_map(filename="map1_1"):
    # Функия загрузки уровня на экран
    all_sprites.empty()
    block_group.empty()
    enemy_group.empty()
    tiles_group.empty()
    board = load_level(filename + '.txt')
    x, y = None, None
    global PLAYER
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == '.':
                Tile(x, y, tile_images['empty'], "empty")
            elif board[y][x] == 'E':
                Tile(x, y, tile_images['empty'], "empty")
                Enemy(x, y, tile_images['enemy'])
            elif board[y][x] == '#':
                Tile(x, y, tile_images['wall'], "wall")
            elif board[y][x] == '@':
                Tile(x, y, tile_images['empty'], "empty")
                PLAYER.rect.x, PLAYER.rect.y = x * TILE_S, y * TILE_S


if __name__ == '__main__':
    # Переменные для применения умений, защиты и атаки героев
    cur_motion = 0
    cur_attack = 0
    cur_skill = 0
    cur_buff = 0
    SKILLS = {}
    con = sqlite3.connect("Stats.db")
    cur = con.cursor()
    s = 'select * from skills'
    res = cur.execute(s).fetchall()
    for i in res:
        li = SKILLS.get(i[2], [])
        li.append([i[1]] + list(i[3:]))
        SKILLS[i[2]] = li
    con.close()
    ch_s = False
    choosing_hero = False
    choosing_enemy = False
    Heroes_Status = ["N/a", "N/a", "N/a", "N/a"]

    # Переменные для игрового прогресса
    Level = 1
    EXP = [0, 500]
    Boss = 1

    # Переменные для контроля состояния игры: переход между картами, боевой и небоевой режимы
    ex = FightScreen()
    cur_map = [1, 1]
    load_map()
    FIGHT = False
    running = False if not PLAYER else True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not FIGHT:
                # Осуществление движения героя вне боя

                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                    if PLAYER.rect.y < 0:
                        cur_map[1] -= 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                    if PLAYER.rect.y >= 660:
                        cur_map[1] += 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                    if PLAYER.rect.x < 0:
                        cur_map[0] -= 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)
                    if PLAYER.rect.x >= 660:
                        cur_map[0] += 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                # Проверка начала боя
                enemy_group.update()
                from Sprites import FIGHT
                from Sprites import ENEMYES, ENEMYES_HP, HEROES, HEROES_HP, QUEUE

                Heroes_Status = ["N/a", "N/a", "N/a", "N/a"]

            if event.type == pygame.KEYDOWN and FIGHT:
                # Осуществление действий героев в бою

                # Аттака героев
                if event.key == pygame.K_a and QUEUE[cur_motion] in HEROES \
                        and not choosing_enemy and not choosing_hero and not ch_s:
                    choosing_enemy = True
                if event.key == pygame.K_SPACE and QUEUE[cur_motion] in HEROES and choosing_enemy:
                    choosing_enemy = False
                    while ENEMYES_HP[cur_attack] <= 0:
                        cur_attack = (cur_attack + 1) % len(ENEMYES_HP)
                    ENEMYES_HP[cur_attack] = ENEMYES_HP[cur_attack] \
                                             - (QUEUE[cur_motion][2] - ENEMYES[cur_attack][3])
                    cur_motion = (cur_motion + 1) % len(QUEUE)
                    while ENEMYES_HP[cur_attack] <= 0 and \
                            len(list(filter(lambda x: x > 0, ENEMYES_HP))):
                        cur_attack = (cur_attack + 1) % len(ENEMYES_HP)
                if event.key == pygame.K_DOWN and choosing_enemy:
                    cur_attack = (cur_attack + 1) % len(ENEMYES_HP)
                    while ENEMYES_HP[cur_attack] <= 0:
                        cur_attack = (cur_attack + 1) % len(ENEMYES_HP)
                if event.key == pygame.K_UP and choosing_enemy:
                    cur_attack = (cur_attack - 1) % len(ENEMYES_HP)
                    while ENEMYES_HP[cur_attack] <= 0:
                        cur_attack = (cur_attack - 1) % len(ENEMYES_HP)

                # Защита героев
                if event.key == pygame.K_d and QUEUE[cur_motion] in HEROES \
                        and not choosing_enemy and not choosing_hero and not ch_s:
                    Heroes_Status[HEROES.index(QUEUE[cur_motion])] = ["Defence", 1]
                    cur_motion = (cur_motion + 1) % len(QUEUE)

                # Навыки героев
                if event.key == pygame.K_s and QUEUE[cur_motion] in HEROES \
                        and not choosing_enemy and not choosing_hero and not ch_s:
                    ch_s = True
                if event.key == pygame.K_DOWN and QUEUE[cur_motion] in HEROES \
                        and ch_s and not choosing_hero:
                    cur_skill = (cur_skill - 1) % len(SKILLS[QUEUE[cur_motion][-1]])
                if event.key == pygame.K_UP and QUEUE[cur_motion] in HEROES \
                        and ch_s and not choosing_hero:
                    cur_skill = (cur_skill + 1) % len(SKILLS[QUEUE[cur_motion][-1]])
                if event.key == pygame.K_SPACE and QUEUE[cur_motion] in HEROES \
                        and ch_s and not choosing_hero:
                    skill = SKILLS[QUEUE[cur_motion][-1]][cur_skill]
                    if skill[-1] == 0:
                        continue
                    while ENEMYES_HP[cur_attack] <= 0 and \
                            len(list(filter(lambda x: x > 0, ENEMYES_HP))):
                        cur_attack = (cur_attack + 1) % len(ENEMYES_HP)
                    if skill[2] == "Damage":
                        ENEMYES_HP[cur_attack] -= QUEUE[cur_motion][2] * skill[-2]
                        skill[-1] -= 1
                    elif skill[2] == "DamageAOE":
                        for i in range(len(ENEMYES_HP)):
                            ENEMYES_HP[i] -= QUEUE[cur_motion][2] * skill[-2]
                        skill[-1] -= 1
                    elif skill[2] in ["Buff", "Heal"]:
                        choosing_hero = True
                        continue
                    ch_s = False
                    cur_motion = (cur_motion + 1) % len(QUEUE)

                # Выбор цели(героя) на которой будет применён бафф
                if event.key == pygame.K_DOWN and QUEUE[cur_motion] in HEROES and choosing_hero:
                    cur_buff = (cur_buff + 1) % len(Heroes_Status)
                if event.key == pygame.K_UP and QUEUE[cur_motion] in HEROES and choosing_hero:
                    cur_buff = (cur_buff - 1) % len(Heroes_Status)
                if event.key == pygame.K_SPACE and QUEUE[cur_motion] in HEROES and choosing_hero:
                    skill = SKILLS[QUEUE[cur_motion][-1]][cur_skill]
                    Buffs = {"Уворот": "Dodge", "Прикрытие": "Defence"}
                    if skill[2] == "Buff":
                        Heroes_Status[cur_buff] = [Buffs[skill[0]], skill[-2]]
                    elif skill[2] == "Heal":
                        HEROES_HP[cur_buff] += skill[-2] * QUEUE[cur_motion][2]
                    skill[-1] -= 1
                    cur_motion = (cur_motion + 1) % len(QUEUE)
                    choosing_hero = False
                    ch_s = False

                # Обработка эскейпа
                if event.key == pygame.K_ESCAPE and choosing_enemy:
                    choosing_enemy = False
                if event.key == pygame.K_ESCAPE and ch_s:
                    ch_s = False
                if event.key == pygame.K_ESCAPE and choosing_hero:
                    choosing_hero = False

        screen.fill(pygame.Color(0))
        if not FIGHT:
            # Обработка карты
            cur_motion = 0
            cur_attack = 0
            all_sprites.draw(screen)
            all_sprites.update()
            player_group.draw(screen)
            player_group.update()
        elif FIGHT:
            # Обработка боя
            if QUEUE[cur_motion] in HEROES:
                charges = [i[-1] for i in SKILLS[QUEUE[cur_motion][-1]]]
            else:
                charges = []
            ex.draw(ENEMYES, ENEMYES_HP, HEROES, HEROES_HP,
                    cur_attack, cur_skill, QUEUE[cur_motion], cur_buff,
                    charges,
                    choosing_enemy, choosing_hero, ch_s)
            screen.blit(ex.screen, (0, 0))

            # Аттака монстров
            if QUEUE[cur_motion] in ENEMYES:
                ind = randint(0, 3)
                if Heroes_Status[ind][0] == 'Defence':
                    HEROES_HP[ind] = HEROES_HP[ind] - (QUEUE[cur_motion][2] - HEROES[ind][3] * 1.5)
                    Heroes_Status[ind][1] -= 1
                    if Heroes_Status[ind][1] == 0:
                        Heroes_Status[ind] = "N/a"
                elif Heroes_Status[ind][0] == 'Dodge':
                    Heroes_Status[ind][1] -= 1
                    if Heroes_Status[ind][1] == 0:
                        Heroes_Status[ind] = "N/a"
                else:
                    HEROES_HP[ind] = HEROES_HP[ind] - (QUEUE[cur_motion][2] - HEROES[ind][3])
                cur_motion = (cur_motion + 1) % len(QUEUE)

            # Проверка победа или поражение
            if len(list(filter(lambda x: x > 0, HEROES_HP))) == 0:
                running, FIGHT = False, False
            if len(list(filter(lambda x: x > 0, ENEMYES_HP))) == 0:
                # Перезарядка навыков
                con = sqlite3.connect("Stats.db")
                cur = con.cursor()
                s = 'select distinct classId from skills'
                res = [i[0] for i in cur.execute(s).fetchall()]
                for i in res:
                    s = f'select charges from skills where classId = {i}'
                    res2 = [i[0] for i in cur.execute(s).fetchall()]
                    for j in range(len(res2)):
                        SKILLS[i][j][-1] = res2[j]
                con.close()

                # Начисление опыта
                EXP[0] += 25 * sum(list(map(lambda x: x[-1], ENEMYES)))
                if EXP[0] >= EXP[1]:
                    EXP[0] -= EXP[1]
                    EXP[1] *= 1.5
                    Level += 1
                FIGHT = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
