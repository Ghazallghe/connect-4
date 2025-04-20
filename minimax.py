import math
import numpy as np

from single_player import SinglePlayer


class MinimaxAlgorithm(SinglePlayer):
    W_MIDDLE_COL = 3
    W_FOUR_IN_A_ROW = 100
    W_THREE_IN_A_ROW = 5
    W_TWO_IN_A_ROW = 2
    W_OPPONENT_3 = -5
    W_OPPONENT_2 = -1
    LINE_SIZE = 4
    MAX_SCORE = 10000000000
    MIN_SCORE = -10000000000

    def __init__(self, selected_color, easy_mode):
        super().__init__(selected_color)
        if easy_mode:
            self.depth = 4
        else:
            self.depth = 7

    def calculate_score(self, line, piece):
        score = 0

        opp_piece = self.opponent_piece.value
        if piece == self.opponent_piece.value:
            opp_piece = self.ai_piece.value

        if line.count(piece) == 4:
            score = self.W_FOUR_IN_A_ROW
        elif line.count(piece) == 3 and line.count(0) == 1:
            score = self.W_THREE_IN_A_ROW
        elif line.count(piece) == 2 and line.count(0) == 2:
            score = self.W_TWO_IN_A_ROW

        if line.count(opp_piece) == 3 and line.count(0) == 1:
            score += self.W_OPPONENT_3
        elif line.count(opp_piece) == 2 and line.count(0) == 2:
            score += self.W_OPPONENT_2

        return score

    def utility_function(self, board, piece):
        score = 0

        # check if player has any pieces in the middle column
        center = self.COLUMN // 2
        center_column = (board[:, center]).tolist()
        score += center_column.count(piece) * self.W_MIDDLE_COL

        # check each row
        for row in range(self.ROW):
            r = board[row, :]
            for col in range(self.COLUMN - 3):
                line = r[col:col + self.LINE_SIZE]
                score += self.calculate_score(line.tolist(), piece)

        # check each column
        for col in range(self.COLUMN):
            c = board[:, col]
            for row in range(self.ROW - 3):
                line = c[row:row + self.LINE_SIZE]
                score += self.calculate_score(line.tolist(), piece)

        # check positive diagonal
        for row in range(self.ROW - 3):
            for col in range(self.COLUMN - 3):
                line = np.zeros(self.LINE_SIZE)
                for l in range(self.LINE_SIZE):
                    line[l] = board[row + l][col + l]
                score += self.calculate_score(line.tolist(), piece)

        # check negative diagonal
        for row in range(self.ROW - 1, 2, -1):
            for col in range(self.COLUMN - 1, 2, -1):
                line = np.zeros(self.LINE_SIZE)
                for l in range(self.LINE_SIZE):
                    line[l] = board[row - l][col - l]
                score += self.calculate_score(line.tolist(), piece)
        return score

    def valid_columns(self, board):
        columns = [c for c in range(self.COLUMN) if self.is_valid(board, c)]
        return columns

    def minimax(self, board, depth, max_turn):
        columns = self.valid_columns(board)

        if depth == 0:
            return -1, self.utility_function(board, self.ai_piece.value)

        if self.fully_goal_test(board, self.ai_piece.value):
            return -1, self.MAX_SCORE

        if self.fully_goal_test(board, self.opponent_piece.value):
            return -1, self.MIN_SCORE

        if len(columns) == 0:
            return -1, 0

        if max_turn:
            column = score = -(math.inf)
            for c in columns:
                board_copy = board.copy()
                self.select_place(board_copy, c, self.ai_piece.value)
                _, new_score = self.minimax(
                    board_copy, depth - 1, False)
                if new_score > score:
                    score, column = new_score, c

            return column, score

        else:
            column = score = math.inf
            for c in columns:
                board_copy = board.copy()
                self.select_place(board_copy, c, self.opponent_piece.value)
                _, new_score = self.minimax(
                    board_copy, depth - 1, True)
                if new_score < score:
                    score, column = new_score, c

            return column, score

    def minimax_alpha_beta(self, board, depth, alpha, beta, max_turn):
        columns = self.valid_columns(board)

        if depth == 0:
            return -1, self.utility_function(board, self.ai_piece.value)

        if self.fully_goal_test(board, self.ai_piece.value):
            return -1, self.MAX_SCORE

        if self.fully_goal_test(board, self.opponent_piece.value):
            return -1, self.MIN_SCORE

        if len(columns) == 0:
            return -1, 0

        if max_turn:
            column = score = -(math.inf)
            for c in columns:
                board_copy = board.copy()
                self.select_place(board_copy, c, self.ai_piece.value)
                _, new_score = self.minimax_alpha_beta(
                    board_copy, depth - 1, alpha, beta, False)
                if new_score > score:
                    score, column = new_score, c
                    alpha = max(alpha, score)
                if score >= beta:
                    break

            return column, score

        else:
            column = score = math.inf
            for c in columns:
                board_copy = board.copy()
                self.select_place(board_copy, c, self.opponent_piece.value)
                _, new_score = self.minimax_alpha_beta(
                    board_copy, depth - 1, alpha, beta, True)
                if new_score < score:
                    score, column = new_score, c
                    beta = min(beta, score)
                if score <= alpha:
                    break

            return column, score

    def ai_turn(self):
        count = 0
        if self.depth == 7:
            col, _ = self.minimax_alpha_beta(
                self.board, self.depth, -math.inf, math.inf, True)
        else:
            col, _ = self.minimax(self.board, self.depth, True)

        if self.is_valid(self.board, col):
            row = self.select_row(self.board, col)
            self.select_place(self.board, col, self.ai_piece.value)

            if self.goal_test(self.board, col, row):
                label = self.my_font.render(
                    self.ai_piece.name + " wins!!", 1, self.ai_piece.color)
                self.screen.blit(label, (40, 10))
                self.is_finished = True

            self.draw_board()

            self.turn = not self.turn
            count += 1
        return count


g = MinimaxAlgorithm(selected_color=2, easy_mode=True)
g.start_game()
