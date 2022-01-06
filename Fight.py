import pygame

SIZE = (600, 600)


class FightScreen:
    def __init__(self):
        self.screen = pygame.Surface(SIZE)
        fight_bg = pygame.image.load('Images/Sprite-0001.png')
        self.screen.blit(fight_bg, fight_bg.get_rect(bottomright=(600, 500)))

        pygame.draw.line(self.screen, pygame.Color(255, 255, 255), (0, 500), (600, 500), 5)

        font = pygame.font.Font(None, 25)

        text = font.render("A Attack", True, (255, 100, 125))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 500, 150, 25), 5)
        self.screen.blit(text, (10, 500))

        text = font.render("S Skills", True, (155, 155, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 550, 150, 25), 5)
        self.screen.blit(text, (10, 525))

        text = font.render("D Defense", True, (50, 55, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 525, 150, 25), 5)
        self.screen.blit(text, (10, 550))

        text = font.render("F Items", True, (255, 255, 100))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 575, 150, 25), 5)
        self.screen.blit(text, (10, 575))

    def draw(self, Enemys):
        for i in range(len(Enemys)):
            cof = 100 if i % 2 else 0
            pygame.draw.rect(self.screen, (255, 75, 75), (cof, 100 * i, 100, 100))
        for i in range(5):
            cof = 500 if i % 2 else 400
            pygame.draw.rect(self.screen, (75, 155, 255), (cof, 100 * i, 100, 100))
