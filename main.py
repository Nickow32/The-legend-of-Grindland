import pygame
import os
import sys

from Sprites import *
from Fight import FightScreen

pygame.init()
SIZE = WI, HE = 600, 600
FPS = 60
TILE_S = 60
PLAYER = None
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


def load_level(filename):
    # Функция загрузки уровня из тхт файла
    filename = "maps/" + filename
    with open(filename, "r", encoding="utf8") as mapFile:
        level_map = [line.strip() for line in mapFile]
    return list(map(lambda x: x.ljust(10, "."), level_map))


def load_map(filename="map0_0.txt"):
    # Функия загрузки уровня на экран
    board = load_level(filename)
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
                if not PLAYER:
                    PLAYER = Player(x, y, player_image)
                else:
                    PLAYER.rect.x, PLAYER.rect.y = x, y


if __name__ == '__main__':
    ex = FightScreen()
    load_map()
    running = False if not PLAYER else True
    while running:
        from Sprites import FIGHT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not FIGHT:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                    if PLAYER.rect.y < 0:
                        PLAYER.move(0, 1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                    if PLAYER.rect.y >= 600:
                        PLAYER.move(0, -1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                    if PLAYER.rect.x < 0:
                        PLAYER.move(1, 0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)
                    if PLAYER.rect.x >= 600:
                        PLAYER.move(-1, 0)
        screen.fill(pygame.Color(0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.draw(screen)
        if FIGHT:
            screen.blit(ex.screen, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
