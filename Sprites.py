import pygame

TILE_S = 60


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, *groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x+10, TILE_S * pos_y+10)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, *groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x+10, TILE_S * pos_y+10)
