import numpy as np
import pygame

import sys
import math

from single_player import SinglePlayer
from build_q_table import BuildQTable


class QLearning(SinglePlayer):

    def __init__(self, selected_color, *args):
        super().__init__(selected_color)

        if len(args) == 1:
            self.q_table = np.genfromtxt(args[0] + '.csv', delimiter=',')
        else:
            build_q_table = BuildQTable(*args)
            self.q_table = build_q_table.start_training()

    def select_place(self, board, column, value):
        row = self.select_row(board, column)
        board[row][column] = value
        return row

    def find_state_from_board(self, location):
        return location[0] * self.COLUMN + location[1]

    def start_game(self):
        self.draw_board()
        count_pieces = 0
        while not self.is_finished:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.BLACK,
                                     (0, 0, self.width, self.SQUARE_SIZE))
                    posx = event.pos[0]
                    if self.turn == self.opponent_piece.turn:
                        pygame.draw.circle(
                            self.screen, self.opponent_piece.color, (posx, int(self.SQUARE_SIZE / 2)), self.RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.BLACK,
                                     (0, 0, self.width, self.SQUARE_SIZE))
                    if self.turn == self.opponent_piece.turn:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARE_SIZE))
                        if self.is_valid(self.board, col):
                            row = self.select_place(
                                self.board, col, self.opponent_piece.value)
                            if self.fully_goal_test(self.board, self.opponent_piece.value):
                                label = self.my_font.render(
                                    self.opponent_piece.name + " wins!!", 1, self.opponent_piece.color)
                                self.screen.blit(label, (40, 10))
                                self.is_finished = True
                            state = self.find_state_from_board((row, col))

                            self.turn = not self.turn
                            count_pieces += 1
                            self.draw_board()

            if self.turn == self.ai_piece.turn and not self.is_finished:
                action = np.argmax(self.q_table[state, :])
                pygame.time.wait(500)
                self.select_place(self.board, action, self.ai_piece.value)
                if self.fully_goal_test(self.board, self.ai_piece.value):
                    label = self.my_font.render(
                        self.ai_piece.name + " wins!!", 1, self.ai_piece.color)
                    self.screen.blit(label, (40, 10))
                    self.is_finished = True
                self.turn = not self.turn
                count_pieces += 1
                self.draw_board()

            if count_pieces == 42:
                self.is_tied()

            if self.is_finished:
                pygame.time.wait(5000)


# q = QLearning(1, '../my_array')
# q.start_game()
q = QLearning(1, 0.01, 0.9, 0.3, 20, './abcd')
q.start_game()
