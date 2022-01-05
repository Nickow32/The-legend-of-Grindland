import pygame

SIZE = (600, 600)


class FightScreen:
    def __init__(self):
        self.screen = pygame.Surface(SIZE)

        pygame.draw.line(self.screen, pygame.Color(255, 255, 255), (300, 0), (300, 500))
        pygame.draw.line(self.screen, pygame.Color(255, 255, 255), (0, 500), (600, 500))

        font = pygame.font.Font(None, 25)

        text = font.render("Attack", True, (255, 100, 125))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 500, 150, 25), 5)
        self.screen.blit(text, (10, 500))

        text = font.render("Defense", True, (50, 55, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 525, 150, 25), 5)
        self.screen.blit(text, (10, 525))

        text = font.render("Skills", True, (155, 155, 255))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 550, 150, 25), 5)
        self.screen.blit(text, (10, 550))

        text = font.render("Items", True, (255, 255, 100))
        pygame.draw.rect(self.screen, (75, 75, 75), (0, 575, 150, 25), 5)
        self.screen.blit(text, (10, 575))
