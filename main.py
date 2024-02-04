import pygame
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
        self.screen.fill(BLACK)
        self.draw_title()

        font_button = pygame.font.SysFont("timesnewroman", 40)

        button_play = Button(int(self.WIDTH / 2) - 140,
                             int(self.HEIGHT / 2) - 25,
                             280, 50, "PLAY",
                             WHITE, WHITE, font_button)

        buttons_arr = [button_play]

        for button in buttons_arr:
            button.draw(self.screen)

        btn = Chess.wait_press(buttons_arr)

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Chess.wait_press(buttons_arr)

    def run(self):
        self.board.reset()
        self.board.draw_board()

        while True:
            pygame.display.update()
            self.clock.tick()
            Chess.check_exit()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.board.click(x, y)


    def draw_title(self):
        font = pygame.font.SysFont("timesnewroman", 50)
        text = font.render("Welcome to chess!!!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 10
        self.screen.blit(text, rect)


if __name__ == "__main__":
    game = Chess()
    game.play()
