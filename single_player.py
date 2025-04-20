import numpy as np
import pygame

import math
import sys

import game


class SinglePlayer(game.Connect4):

    def __init__(self, selected_color):
        super().__init__()
        if selected_color == 1:
            self.opponent_piece = game.Piece(
                self.CHETWODE_BLUE, 1, 1, "Player 1")
            self.ai_piece = game.Piece(self.POWDER_BLUE, 2, 0, "Player 2")
        else:
            self.ai_piece = game.Piece(self.CHETWODE_BLUE, 1, 1, "Player 1")
            self.opponent_piece = game.Piece(
                self.POWDER_BLUE, 2, 0, "Player 2")

    def opp_turn(self, col):
        count = 0
        if self.is_valid(self.board, col):
            row = self.select_row(self.board, col)
            self.select_place(
                self.board, col, self.opponent_piece.value)

            if self.goal_test(self.board, col, row):
                label = self.my_font.render(
                    self.opponent_piece.name + " wins!!", 1, self.opponent_piece.color)
                self.screen.blit(label, (40, 10))
                self.is_finished = True

            self.turn = not self.turn
            count += 1

            self.draw_board()
        return count

    def ai_turn(self):
        pass

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
                        count_pieces += self.opp_turn(col)

            if self.turn == self.ai_piece.turn and not self.is_finished:
                count_pieces += self.ai_turn()

            if count_pieces == 42:
                self.is_tied()

            if self.is_finished:
                pygame.time.wait(5000)
