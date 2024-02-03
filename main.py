import chess
import pygame
from config import *
import sys


class Chess:
    def __init__(self, screen: pygame.Surface):
        self.board = chess.Board()
        self.screen = screen

        self.WIDTH, self.HEIGHT = screen.get_size()

        self.BLOCK_WIDTH = self.WIDTH / 8
        self.BLOCK_HEIGHT = self.HEIGHT / 8

    def __str__(self):
        return str(self.board)

    def move(self, move_from, move_to):
        m = chess.Move.from_uci(f"{move_from}{move_to}")
        self.board.push(m)

    def draw_board(self):
        self.screen.fill(WHITE_CELL)
        for y in range(8):
            for x in range(y % 2, 8, 2):
                pygame.draw.rect(self.screen, BLACK_CELL, (x * self.BLOCK_WIDTH, y * self.BLOCK_HEIGHT,
                                                           self.BLOCK_WIDTH, self.BLOCK_HEIGHT))



class Game:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.chess = Chess(self.screen)

    @staticmethod
    def check_exit():
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    Game.exit()
            pygame.event.post(event)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()
            pygame.event.post(event)

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    def show(self):
        self.run_loop()

    def run_loop(self):
        self.start_window()

    def start_window(self):
        self.screen.fill(WHITE)
        self.chess.draw_board()
        while True:
            pygame.display.update()
            self.clock.tick()
            Game.check_exit()


if __name__ == "__main__":
    game = Game()
    game.show()
