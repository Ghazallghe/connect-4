import numpy as np
import pygame


class Piece():
    def __init__(self, color, value, turn, name):
        self.color = color
        self.value = value
        self.turn = turn
        self.name = name


class Connect4:
    ROW = 6
    COLUMN = 7

    # colors
    BLUE_GREY = '#9fafca'
    SAPPHIRE_BLUE = '#0e387a'
    POWDER_BLUE = '#a9dce3'
    CHETWODE_BLUE = '#7689de'
    EQUAL_COLOR = '#6633FF'
    BLACK = '#000000'

    # screen size
    SQUARE_SIZE = 100

    # width and height of board
    width = COLUMN * SQUARE_SIZE
    height = (ROW + 1) * SQUARE_SIZE

    size = (width, height)

    RADIUS = int(SQUARE_SIZE / 2 - 5)

    def __init__(self):
        self.board = self.create_board()
        self.is_finished = False
        self.turn = 1

        pygame.init()
        self.my_font = pygame.font.Font(
            "assets/TechnoRaceItalic-eZRWe.otf", 75)
        self.screen = pygame.display.set_mode(self.size)

    def create_board(self):
        return np.zeros((self.ROW, self.COLUMN))

    def is_valid(self, board, column):
        return (0 <= column < 8) and board[self.ROW - 1][column] == 0

    def select_row(self, board, column):
        for r in range(self.ROW):
            if board[r][column] == 0:
                return r
        return -1

    def select_place(self, board, column, value):
        row = self.select_row(board, column)
        board[row][column] = value

    def goal_test(self, board, column, row):
        value = board[row][column]
        if value == 0:
            return False

        # check the row containing the piece
        for c in range(self.COLUMN - 3):
            if board[row][c] == board[row][c + 1] == board[row][c + 2] == board[row][c + 3] == value:
                return True

        # check the column containing the piece
        for r in range(self.ROW - 3):
            if board[r][column] == board[r + 1][column] == board[r + 2][column] == board[r + 3][column] == value:
                return True

        # check the positive diagonal containing the piece
        start_col = 0
        start_row = 0
        if row > column:
            start_row = row - column
            start_col = 0
        elif row < column:
            start_row = 0
            start_col = column - row

        for r in range(start_row, self.ROW - 3):
            for c in range(start_col, self.COLUMN - 3):
                if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == value:
                    return True

        # check the negative diagonal containing the piece
        for row in range(self.ROW - 1, 2, -1):
            for col in range(self.COLUMN - 3):
                if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == value:
                    return True

        return False

    def fully_goal_test(self, board, piece):

        for row in range(self.ROW):
            for col in range(self.COLUMN - 3):
                if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == piece:
                    return True

        for col in range(self.COLUMN):
            for row in range(self.ROW - 3):
                if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == piece:
                    return True

        for row in range(self.ROW - 3):
            for col in range(self.COLUMN - 3):
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == piece:
                    return True

        for row in range(self.ROW - 1, 2, -1):
            for col in range(self.COLUMN - 3):
                if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == piece:
                    return True

        return False

    def is_tied(self):
        self.is_finished = True
        label = self.my_font.render("The game is tied", 1, self.EQUAL_COLOR)
        self.screen.blit(label, (40, 10))
        self.draw_board()

    def draw_board(self):
        for c in range(self.COLUMN):
            for r in range(self.ROW):
                pygame.draw.rect(self.screen, self.SAPPHIRE_BLUE, (c * self.SQUARE_SIZE, r *
                                                                   self.SQUARE_SIZE + self.SQUARE_SIZE,
                                                                   self.SQUARE_SIZE, self.SQUARE_SIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(
                    c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2),
                    int(r * self.SQUARE_SIZE + self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.RADIUS)

        for c in range(self.COLUMN):
            for r in range(self.ROW):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.CHETWODE_BLUE, (int(
                        c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2),
                        self.height - int(r * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.POWDER_BLUE, (int(
                        c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2),
                        self.height - int(r * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.RADIUS)
        pygame.display.update()
