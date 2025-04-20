import pygame
import sys
import math

import game


class TwoPlayers(game.Connect4):
    def __init__(self):
        super().__init__()
        self.player1 = game.Piece(
            self.CHETWODE_BLUE, 1, 1, "Player 1")
        self.player2 = game.Piece(self.POWDER_BLUE, 2, 0, "Player 2")

    def start_game(self):
        self.draw_board()
        while not self.is_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.BLACK,
                                     (0, 0, self.width, self.SQUARE_SIZE))
                    pos_x = event.pos[0]

                    if self.turn == self.player1.turn:
                        pygame.draw.circle(
                            self.screen, self.player1.color, (pos_x, int(self.SQUARE_SIZE / 2)), self.RADIUS)
                    else:
                        pygame.draw.circle(
                            self.screen, self.player2.color, (pos_x, int(self.SQUARE_SIZE / 2)), self.RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self
                                     .BLACK, (0, 0, self.width, self.SQUARE_SIZE))

                    if self.turn == self.player1.turn:
                        message = "Player 1 wins!!"
                        color = self.player1.color
                        value = self.player1.value
                    else:
                        message = "Player 2 wins!!"
                        color = self.player2.color
                        value = self.player2.value

                    pos_x = event.pos[0]
                    col = int(math.floor(pos_x / self.SQUARE_SIZE))

                    if self.is_valid(self.board, col):
                        r = self.select_row(self.board, col)
                        self.select_place(self.board, col, value)
                        if self.goal_test(self.board, col, r):
                            self.is_finished = True
                            label = self.my_font.render(message, 1, color)
                            self.screen.blit(label, (40, 10))

                        self.turn = not self.turn

                self.draw_board()

                if self.is_finished:
                    pygame.time.wait(6000)


g = TwoPlayers()
g.start_game()
