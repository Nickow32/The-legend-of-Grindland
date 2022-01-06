import pygame

SIZE = (600, 600)


class FightScreen:
    def __init__(self):
        self.screen = pygame.Surface(SIZE)

    def draw(self, Enemys, Heroes, Hp):
        self.screen.fill(pygame.Color(50, 50, 50))
        font = pygame.font.Font(None, 25)

        fight_bg = pygame.image.load('Images/fight_background.png')
        self.screen.blit(fight_bg, fight_bg.get_rect(bottomright=(600, 500)))

        text = font.render("A Атака", True, (255, 100, 125))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 500, 150, 25), 5)
        self.screen.blit(text, (10, 500))
        text = font.render("S Умение", True, (155, 155, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 550, 150, 25), 5)
        self.screen.blit(text, (10, 525))
        text = font.render("D Зацита", True, (50, 55, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 525, 150, 25), 5)
        self.screen.blit(text, (10, 550))
        text = font.render("F Предметы", True, (255, 255, 100))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 575, 150, 25), 5)
        self.screen.blit(text, (10, 575))

        text = font.render("Дантэ", True, (255, 0, 0))
        pygame.draw.rect(self.screen, (75, 75, 75), (150, 500, 450, 25), 5)
        self.screen.blit(text, (160, 500))
        text = font.render("Левап", True, (155, 0, 155))
        pygame.draw.rect(self.screen, (75, 75, 75), (150, 525, 450, 25), 5)
        self.screen.blit(text, (160, 525))
        text = font.render("Ашадия", True, (255, 255, 100))
        pygame.draw.rect(self.screen, (75, 75, 75), (150, 550, 450, 25), 5)
        self.screen.blit(text, (160, 550))
        text = font.render("Лилиан", True, (100, 255, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (150, 575, 450, 25), 5)
        self.screen.blit(text, (160, 575))

        text = font.render("ОЗ", True, (0, 255, 0))
        self.screen.blit(text, (260, 500))
        self.screen.blit(text, (260, 525))
        self.screen.blit(text, (260, 550))
        self.screen.blit(text, (260, 575))

        for i in range(len(Enemys)):
            cof = 120 if i % 2 else 20
            pygame.draw.rect(self.screen, (255, 75, 75), (cof, 80 * i + 100, 80, 80))
        for i in range(4):
            cof = 500 if i % 2 else 400
            pygame.draw.rect(self.screen, (75, 155, 255), (cof, 80 * i + 140, 80, 80))
        for i in range(len(Hp)):
            text = font.render(f"{Hp[i]}/{Heroes[i][1]}", True, (0, 255, 0))
            self.screen.blit(text, (300, 500 + 25 * i))