import pygame
import sqlite3
from random import randint

FIGHT = False
TILE_S = 66
HEROES = []
ENEMYES = []
QUEUE = []
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


# Классы спрайтов и их функции
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, type):
        self.frames = []
        if type == "wall":
            super().__init__(all_sprites, block_group)
            self.cut_sheet(image, 2, 1)
        elif type == "empty":
            super().__init__(all_sprites, tiles_group)
            self.cut_sheet(image, 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x, TILE_S * pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (66, 66)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
        global FIGHT, ENEMYES, HEROES, QUEUE
        FIGHT = True
        con = sqlite3.connect("Stats.db")
        cur = con.cursor()
        res = cur.execute("select * from Heroes").fetchall()
        for i in res:
            HEROES.append(i[1:])
        res = cur.execute("select * from Monsters").fetchall()
        n = randint(1, 5)
        for i in range(n):
            ENEMYES.append(res[randint(0, len(res) - 1)][1:])
        QUEUE = sorted(HEROES + ENEMYES, key=lambda x: -x[-2])
        con.close()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(all_sprites, player_group)
        self.core_image = image
        self.image = image
        self.rect = self.image.get_rect().move(
            TILE_S * pos_x, TILE_S * pos_y)

    def move(self, x, y, vec):
        if vec == "N":
            self.image = pygame.transform.rotate(self.core_image, 180)
        elif vec == "S":
            self.image = pygame.transform.rotate(self.core_image, 0)
        elif vec == "W":
            self.image = pygame.transform.rotate(self.core_image, 270)
        elif vec == "E":
            self.image = pygame.transform.rotate(self.core_image, 90)
        self.rect.x += (TILE_S * x)
        self.rect.y += (TILE_S * y)
        if pygame.sprite.spritecollideany(self, block_group):
            self.rect.x -= (TILE_S * x)
            self.rect.y -= (TILE_S * y)

    def update(self, *args):
        global FIGHT, ENEMYES, HEROES, QUEUE
        FIGHT, ENEMYES, HEROES, QUEUE = False, [], [], []