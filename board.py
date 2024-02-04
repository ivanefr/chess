import chess
import chess.svg
from config import *
import cairosvg


class Board:
    def __init__(self, screen: pygame.Surface):
        self.board = chess.Board()
        self.screen = screen

        self.WIDTH, self.HEIGHT = screen.get_size()

        self.BLOCK_WIDTH = self.WIDTH / 8
        self.BLOCK_HEIGHT = self.HEIGHT / 8

        self.is_clicked = None
        self.legal_move = []

        self.move_color = True

        self.checkmate = False

    def __str__(self):
        return str(self.board)

    def move(self, square_from, square_to):
        m = chess.Move(square_from, square_to)
        self.board.push(m)
        self.move_color = not self.move_color
        if self.board.is_checkmate():
            self.draw_checkmate()
            self.checkmate = True
            return
        if self.board.is_check():
            self.draw_check()
        else:
            self.del_check()

    def draw_piece(self, x, y):
        piece = self.board.piece_at(Board.square(x, y))
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
                self.draw_cell(x, y)

    def reset(self):
        self.board.reset()

    @staticmethod
    def square(x, y):
        return 8 * y + x

    def draw_cell(self, x, y, color=None):
        if color is not None:
            pygame.draw.rect(self.screen, color, (x * self.BLOCK_WIDTH, (7 - y) * self.BLOCK_HEIGHT,
                                                  self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
            self.draw_piece(x, y)
            return
        if x % 2 == y % 2:
            pygame.draw.rect(self.screen, BLACK_CELL, (x * self.BLOCK_WIDTH, (7 - y) * self.BLOCK_HEIGHT,
                                                       self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
        else:
            pygame.draw.rect(self.screen, WHITE_CELL, (x * self.BLOCK_WIDTH, (7 - y) * self.BLOCK_HEIGHT,
                                                       self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
        self.draw_piece(x, y)

    def click(self, x, y):
        x //= self.BLOCK_WIDTH
        y //= self.BLOCK_HEIGHT
        y = int(7 - y)
        x = int(x)
        if (x, y) in self.legal_move:
            self.move(Board.square(*self.is_clicked), Board.square(x, y))
            self.draw_cell(*self.is_clicked)
            for legal_x, legal_y in self.legal_move:
                self.draw_cell(legal_x, legal_y)
            self.is_clicked = None
            self.legal_move = []
            if self.checkmate:
                return CHECKMATE
            return
        piece = self.board.piece_at(Board.square(x, y))
        if piece is not None and piece.color == self.move_color:

            if self.is_clicked:
                self.draw_cell(*self.is_clicked)
                for legal_x, legal_y in self.legal_move:
                    self.draw_cell(legal_x, legal_y)
                self.legal_move = []
            if self.is_clicked != (x, y):
                self.draw_cell(x, y, GREEN_CELL)
                self.is_clicked = (x, y)
            else:
                self.is_clicked = None
                self.legal_move = []
            if self.is_clicked:
                for to_y in range(8):
                    for to_x in range(8):
                        if self.board.is_legal(chess.Move(Board.square(x, y), Board.square(to_x, 7 - to_y))):
                            self.legal_move.append((to_x, 7 - to_y))
                            self.draw_legal_move(to_x, to_y)
        else:
            if self.is_clicked:
                self.draw_cell(*self.is_clicked)
                self.is_clicked = None
                for legal_x, legal_y in self.legal_move:
                    self.draw_cell(legal_x, legal_y)
                self.legal_move = []

    def draw_check(self):
        square = self.board.king(self.move_color)
        x, y = Board.coor_by_square(square)
        self.draw_cell(x, y, RED_CELL)

    def del_check(self):
        square = self.board.king(not self.move_color)
        x, y = Board.coor_by_square(square)
        self.draw_cell(x, y)

    def draw_checkmate(self):
        square = self.board.king(self.move_color)
        x, y = Board.coor_by_square(square)
        self.draw_cell(x, y, PURPLE_CELL)

    @staticmethod
    def coor_by_square(square):
        y = square // 8
        x = square % 8
        return x, y

    def draw_legal_move(self, x, y):
        piece = self.board.piece_at(Board.square(x, 7 - y))
        if piece:
            pygame.draw.rect(self.screen, GREEN_CELL,
                             (
                                 x * self.BLOCK_WIDTH, y * self.BLOCK_HEIGHT,
                                 self.BLOCK_WIDTH, self.BLOCK_HEIGHT
                             ), 3
                             )
        else:
            pygame.draw.circle(self.screen, GREEN_CELL,
                               (
                                   (x + 0.5) * self.BLOCK_WIDTH,
                                   (y + 0.5) * self.BLOCK_HEIGHT
                               ),
                               0.1 * self.BLOCK_HEIGHT)
