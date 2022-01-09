import pygame
import os
import sys

from Sprites import Tile, Enemy, Player, \
    all_sprites, block_group, tiles_group, enemy_group, player_group
from Fight import FightScreen

pygame.init()
SIZE = WI, HE = 600, 600
FPS = 60
TILE_S = 60
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Игре нужно название")
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    # Функция загрузки изображений
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
    'wall': pygame.transform.scale(load_image('box.png'), (60, 60)),
    'enemy': pygame.transform.scale(load_image('box.png'), (60, 60)),
    'empty': pygame.transform.scale(load_image('grass.png'), (60, 60))
}
player_image = pygame.transform.scale(load_image('mar.png'), (60, 60))

PLAYER = Player(0, 0, player_image)


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
    ex = FightScreen()
    cur_motion = 0
    cur_map = [1, 1]
    load_map()
    FIGHT = False
    running = False if not PLAYER else True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not FIGHT:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                    if PLAYER.rect.y < 0:
                        cur_map[1] -= 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                    if PLAYER.rect.y >= 600:
                        cur_map[1] += 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                    if PLAYER.rect.x < 0:
                        cur_map[0] -= 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)
                    if PLAYER.rect.x >= 600:
                        cur_map[0] += 1
                        load_map(f"map{cur_map[0]}_{cur_map[1]}")
                enemy_group.update()
                from Sprites import FIGHT
                from Sprites import ENEMYES, ENEMYES_HP, HEROES, HEROES_HP, QUEUE
            if event.type == pygame.KEYDOWN and FIGHT:
                if event.key == pygame.K_a and QUEUE[cur_motion] in HEROES:
                    ENEMYES_HP[0] -= QUEUE[cur_motion][2]
                    print(ENEMYES_HP, sum(ENEMYES_HP))
                    cur_motion = (cur_motion + 1) % len(QUEUE)
        screen.fill(pygame.Color(0))
        if not FIGHT:
            all_sprites.draw(screen)
            all_sprites.update()
            player_group.draw(screen)
        elif FIGHT:
            ex.draw(ENEMYES, HEROES, HEROES_HP)
            screen.blit(ex.screen, (0, 0))
            print(ENEMYES_HP, sum(ENEMYES_HP), FIGHT)
            if QUEUE[cur_motion] in ENEMYES:
                HEROES_HP[0] -= QUEUE[cur_motion][2]
                cur_motion = (cur_motion + 1) % len(QUEUE)
            if sum(HEROES_HP) <= 0:
                running, FIGHT = False, False
            if sum(ENEMYES_HP) <= 0:
                FIGHT = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
