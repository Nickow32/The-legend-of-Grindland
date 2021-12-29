import pygame
import os
import sys

from Sprites import Tile, Player


pygame.init()
SIZE = WI, HE = 620, 620
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
    'wall': load_image('box.png'),
    'enemy': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


def load_level(filename):
    # Функция загрузки уровня из тхт файла
    filename = "maps/" + filename
    with open(filename, "r", encoding="utf8") as mapFile:
        level_map = [line.strip() for line in mapFile]
    return list(map(lambda x: x.ljust(10, "."), level_map))


def load_map(filename="map0_0.txt"):
    # Функия загрузки уровня на экран
    board = load_level(filename)
    player, x, y = None, None, None
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == '.':
                Tile(x, y, tile_images['empty'], all_sprites, tiles_group)
            elif board[y][x] == 'E':
                Tile(x, y, tile_images['enemy'], all_sprites, enemy_group)
            elif board[y][x] == '#':
                Tile(x, y, tile_images['wall'], all_sprites, block_group)
            elif board[y][x] == '@':
                Tile(x, y, tile_images['empty'], all_sprites, tiles_group)
                if not player:
                    player = Player(x, y, player_image, all_sprites, player_group)
                else:
                    player.rect.x, player.rect.y = x, y


class FightScreen:
    pass  # Загатовка на будущее


if __name__ == '__main__':
    ex = FightScreen()
    fighting, running = False, True
    load_map()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color(0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update(event)
        player_group.draw(screen)
        if fighting:
            pass
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
