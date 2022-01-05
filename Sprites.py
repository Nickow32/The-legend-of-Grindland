import pygame

FIGHT = False
TILE_S = 60
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, type):
        if type == "wall":
            super().__init__(all_sprites, block_group)
        elif type == "empty":
            super().__init__(all_sprites, tiles_group)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x, TILE_S * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites, enemy_group)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x, TILE_S * pos_y)

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, player_group):
            global FIGHT
            FIGHT = True
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites, player_group)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x, TILE_S * pos_y)

    def move(self, x, y):
        self.rect.x += (TILE_S * x)
        self.rect.y += (TILE_S * y)
        if pygame.sprite.spritecollideany(self, block_group):
            self.rect.x -= (TILE_S * x)
            self.rect.y -= (TILE_S * y)