import pygame
import os
import sys

pygame.init()
SIZE = WI, HE = 620, 620
FPS = 60
TILE_S = 60
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Игре нужно название")
clock = pygame.time.Clock()


def load_level(filename):
    filename = "maps/" + filename
    with open(filename, "r", encoding="utf8") as mapFile:
        level_map = [line.strip() for line in mapFile]
    return list(map(lambda x: x.ljust(10, "."), level_map))


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
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == "wall":
            super().__init__(block_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x+10, TILE_S * pos_y+10)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x+10, TILE_S * pos_y+10)


class Board:
    def __init__(self):
        self.cell_size = TILE_S
        self.player = None

    def load_map(self, filename="map0_0.txt"):
        board = load_level(filename)
        x, y = None, None
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == '.':
                    Tile('empty', x, y)
                elif board[y][x] == '#':
                    Tile('wall', x, y)
                elif board[y][x] == '@':
                    Tile('empty', x, y)
                    if not self.player:
                        self.player = Player(x, y)
                    else:
                        self.player.rect.x, self.player.rect.y = x, y


class Game:
    def __init__(self, Size=(300, 300), Fps=30):
        self.running = True
        self.size = self.wi, self.he = Size
        self.screen = pygame.Surface(self.size)
        self.fps = Fps
        self.board = Board()
        self.board.load_map()

    def __bool__(self):
        return self.running

    def quit(self):
        self.running = False


if __name__ == '__main__':
    ex = Game(SIZE, FPS)
    while ex:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex.quit()

        ex.screen.fill(pygame.Color(0, 0, 0))
        all_sprites.draw(ex.screen)
        tiles_group.draw(ex.screen)
        player_group.draw(ex.screen)
        block_group.draw(ex.screen)
        all_sprites.update(event)
        tiles_group.update(event)
        player_group.update(event)
        block_group.update(event)
        screen.blit(ex.screen, (0, 0))
        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()