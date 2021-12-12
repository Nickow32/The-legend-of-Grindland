import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 60

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, Screen):
        Screen.fill(pygame.Color(0, 0, 0))
        col = pygame.Color(255, 255, 255)
        left, top = self.left, self.top
        size = self.cell_size
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                pygame.draw.rect(Screen, col, (left + size * j, top + size * i, size, size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, pos):
        left, top = self.left, self.top
        size = self.cell_size
        x = (pos[0] - left) // size
        y = (pos[1] - top) // size
        if (len(self.board[0]) - 1 < x or x < 0) \
                or (len(self.board) - 1 < y or y < 0):
            return None
        return x, y

    def on_click(self, cell):
        pass


class Game:
    def __init__(self, Size=(300, 300), Fps=30):
        self.running = True
        self.size = self.wi, self.he = Size
        self.screen = pygame.Surface(self.size)
        self.fps = Fps
        self.board = Board(10, 10)

    def render(self):
        self.board.render(self.screen)

    def get_click(self,pos):
        self.board.get_click(pos)

    def __bool__(self):
        return self.running

    def quit(self):
        self.running = False


if __name__ == '__main__':
    pygame.init()
    size = wi, he = 620, 620
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Игре нужно название")
    fps = 60
    ex = Game(size, fps)
    clock = pygame.time.Clock()
    while ex:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ex.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ex.get_click(event.pos)
        ex.render()
        clock.tick(fps)
        screen.fill(pygame.Color(0, 0, 0))
        screen.blit(ex.screen, (0, 0))
        pygame.display.flip()
    pygame.quit()