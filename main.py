import chess
import chess.svg
import pygame
from config import *
import sys
import os
import cairosvg


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        return None
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


class Board:
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

    def draw_piece(self, x, y):
        square = 8 * y + x
        piece = self.board.piece_at(square)
        if piece is None:
            return
        if piece.color:
            file = f"piece_{str(piece).lower()}b.png"
        else:
            file = f"piece_{str(piece).lower()}w.png"
        image = load_image(file)
        if image is None:
            svg_image = chess.svg.piece(piece, int(self.BLOCK_WIDTH))
            cairosvg.svg2png(bytestring=svg_image, write_to=f"data/{file}")
            image = load_image(file)
        rect = image.get_rect()
        rect.center = (int((x + 0.5) * self.BLOCK_WIDTH), int((7.5 - y) * self.BLOCK_HEIGHT))
        self.screen.blit(image, rect)

    def draw_board(self):
        self.screen.fill(WHITE_CELL)
        for y in range(8):
            for x in range(8):
                if x % 2 == y % 2:
                    pygame.draw.rect(self.screen, BLACK_CELL, (x * self.BLOCK_WIDTH, (7 - y) * self.BLOCK_HEIGHT,
                                                               self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
                else:
                    pygame.draw.rect(self.screen, WHITE_CELL, (x * self.BLOCK_WIDTH, (7 - y) * self.BLOCK_HEIGHT,
                                                               self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
                self.draw_piece(x, y)


class Chess:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.chess = Board(self.screen)

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
            Chess.check_exit()


if __name__ == "__main__":
    game = Chess()
    game.show()
