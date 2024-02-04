from config import *
import sys
from button import Button
from board import Board


class Chess:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.board = Board(self.screen)

    @staticmethod
    def check_exit():
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    Chess.exit()
            pygame.event.post(event)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Chess.exit()
            pygame.event.post(event)

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def wait_press(button_arr=None, k_arr=None):
        Chess.check_exit()

        for event in pygame.event.get():
            if k_arr is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key in k_arr:
                        return event.key
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_arr:
                    x, y = pygame.mouse.get_pos()
                    if button.is_clicked(x, y):
                        return button
        return None

    def play(self):
        self.run_loop()

    def run_loop(self):
        self.start_window()
        self.run()

    def start_window(self):
        self.screen.fill(BLACK_CELL)
        self.draw_title()

        font_button = pygame.font.SysFont("timesnewroman", 40)

        button_play = Button(int(self.WIDTH / 2) - 140,
                             int(self.HEIGHT / 2) - 25,
                             280, 50, "PLAY",
                             WHITE_CELL, WHITE_CELL, font_button)

        buttons_arr = [button_play]

        for button in buttons_arr:
            button.draw(self.screen)

        btn = Chess.wait_press(buttons_arr)

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Chess.wait_press(buttons_arr)

    def run(self):
        self.screen.fill(BLACK)
        self.board.reset()
        self.board.draw_board()

        while True:
            pygame.display.update()
            self.clock.tick()
            Chess.check_exit()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    r = self.board.click(x, y)
                    if r == CHECKMATE:
                        return self.end_window(CHECKMATE)

    def end_window(self, end_type):
        pause = pygame.Surface((600, 600), pygame.SRCALPHA)
        pause.fill((*BLACK_CELL, 127))
        self.screen.blit(pause, (0, 0))
        self.draw_end_title(end_type)

        while True:
            pygame.display.update()
            self.clock.tick()
            Chess.check_exit()
            for event in pygame.event.get():
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    return

    def draw_end_title(self, end_type):
        if end_type == CHECKMATE:
            s1 = "Checkmate!!!"
            if self.board.move_color:
                s2 = "Black won!!!"
            else:
                s2 = "White won!!!"

            font = pygame.font.SysFont("timesnewroman", 50)
            text1 = font.render(s1, True, WHITE_CELL)
            rect1 = text1.get_rect()
            rect1.centerx = int(self.WIDTH / 2)
            rect1.y = 100

            text2 = font.render(s2, True, WHITE_CELL)
            rect2 = text2.get_rect()
            rect2.centerx = int(self.WIDTH / 2)
            rect2.centery = int(self.HEIGHT / 2)

            self.screen.blit(text1, rect1)
            self.screen.blit(text2, rect2)

    def draw_title(self):
        font = pygame.font.SysFont("timesnewroman", 50)
        text = font.render("Welcome to chess!!!", True, WHITE_CELL)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 10
        self.screen.blit(text, rect)


if __name__ == "__main__":
    game = Chess()
    game.play()
