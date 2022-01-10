import pygame
import sqlite3
from random import randint

FIGHT = False
TILE_S = 66
HEROES = []
ENEMYES = []
HEROES_HP = []
ENEMYES_HP = []
QUEUE = []
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

    def update(self, *args):
        global FIGHT, ENEMYES, ENEMYES_HP, HEROES, HEROES_HP, QUEUE
        FIGHT, ENEMYES, ENEMYES_HP, HEROES, HEROES_HP, QUEUE = False, [], [], [], [], []


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites, enemy_group)
        self.image = image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x, TILE_S * pos_y)

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, player_group):
            self.start_fight()
            self.kill()

    def start_fight(self):
        global FIGHT, ENEMYES, ENEMYES_HP, HEROES, HEROES_HP, QUEUE
        FIGHT = True
        con = sqlite3.connect("Stats.db")
        cur = con.cursor()
        res = cur.execute("select * from Heroes").fetchall()
        for i in res:
            HEROES.append(i[1:])
        HEROES_HP = list(map(lambda x: x[1], HEROES))
        res = cur.execute("select * from Monsters").fetchall()
        n = randint(1, 5)
        for i in range(n):
            ENEMYES.append(res[randint(0, len(res) - 1)][1:])
        ENEMYES_HP = list(map(lambda x: x[1], ENEMYES))
        QUEUE = sorted(HEROES + ENEMYES, key=lambda x: -x[-2])
        con.close()


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