import pygame

SIZE = (660, 660)


class FightScreen:
    def __init__(self):
        self.screen = pygame.Surface(SIZE)

    def draw(self, Enemys, Heroes, Hp):
        self.screen.fill(pygame.Color(50, 50, 50))
        font = pygame.font.Font(None, 25)

        fight_bg = pygame.transform.scale(pygame.image.load('Images/fight_background.png'), (660, 560))
        self.screen.blit(fight_bg, fight_bg.get_rect(bottomright=(660, 560)))

        text = font.render("A Атака", True, (255, 100, 125))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 560, 210, 25), 5)
        self.screen.blit(text, (10, 560))
        text = font.render("S Умение", True, (155, 155, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 585, 210, 25), 5)
        self.screen.blit(text, (10, 585))
        text = font.render("D Зацита", True, (50, 55, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 610, 210, 25), 5)
        self.screen.blit(text, (10, 610))
        text = font.render("F Предметы", True, (255, 255, 100))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 635, 210, 25), 5)
        self.screen.blit(text, (10, 635))

        text = font.render("Дантэ", True, (255, 0, 0))
        pygame.draw.rect(self.screen, (75, 75, 75), (210, 560, 510, 25), 5)
        self.screen.blit(text, (220, 560))
        text = font.render("Левап", True, (155, 0, 155))
        pygame.draw.rect(self.screen, (75, 75, 75), (210, 585, 510, 25), 5)
        self.screen.blit(text, (220, 585))
        text = font.render("Ашадия", True, (255, 255, 100))
        pygame.draw.rect(self.screen, (75, 75, 75), (210, 610, 510, 25), 5)
        self.screen.blit(text, (220, 610))
        text = font.render("Лилиан", True, (100, 255, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (210, 635, 510, 25), 5)
        self.screen.blit(text, (220, 635))

        text = font.render("ОЗ", True, (0, 255, 0))
        self.screen.blit(text, (320, 560))
        self.screen.blit(text, (320, 585))
        self.screen.blit(text, (320, 610))
        self.screen.blit(text, (320, 635))

        for i in range(len(Enemys)):
            cof = 120 if i % 2 else 20
            pygame.draw.rect(self.screen, (255, 75, 75), (cof, 95 * i + 80, 95, 95))
        for i in range(4):
            cof = 500 if i % 2 else 400
            pygame.draw.rect(self.screen, (75, 155, 255), (cof, 95 * i + 120, 95, 95))
        for i in range(len(Hp)):
            text = font.render(f"{Hp[i]}/{Heroes[i][1]}", True, (0, 255, 0))
            self.screen.blit(text, (360, 560 + 25 * i))