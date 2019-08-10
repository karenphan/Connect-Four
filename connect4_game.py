import pygame
import connectfour as cf


class ConnectFourGame:
    def __init__(self, p1, p2):
        """
        Initialize variables and the states of certain aspects of the game
        (such as errors and the game running state).
        """
        self._running = True
        self._state = cf.new_game()
        self._error = False
        self._winner = 0
        self._square_size = (100 - ((cf.BOARD_COLUMNS//5) * 7) -
                             ((cf.BOARD_ROWS//5) * 7))
        self._radius = self._square_size//2 - 5
        self._width = cf.BOARD_COLUMNS * self._square_size
        self._height = (cf.BOARD_ROWS + 1) * self._square_size
        self._board = (self._width, self._height)
        self._board_color = (0, 0, 255)
        self._empty = (250, 250, 250)
        self._p1_color = p1
        self._p2_color = p2

    def run(self):
        """Run the game."""
        pygame.init()
        pygame.display.set_mode((self._board))
        clock = pygame.time.Clock()

        while self._running:
            clock.tick(30)
            self._handle_events()
            self._draw_board()

        pygame.quit()

    def _handle_events(self):
        """
        Determine what action the game will take depending
        on the event type.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos, event.button)
        self._gameover()

    def _draw_board(self):
        """Draw the connect four board."""
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(250, 250, 250))
        self._draw_player_turn()
        self._draw_circles()
        if self._error:
            self._draw_error()
        if self._winner:
            self._draw_winner()

        pygame.display.flip()

    def _draw_circles(self):
        """Draw the empty circle slots on the board."""
        surface = pygame.display.get_surface()
        board_row = cf.BOARD_ROWS
        board_col = cf.BOARD_COLUMNS
        for row in range(board_row):
            for col in range(board_col):
                pygame.draw.rect(
                        surface,
                        self._board_color,
                        (col*self._square_size,
                         row*self._square_size + self._square_size,
                         self._square_size,
                         self._square_size)
                        )
                if self._state.board[col][row] == 0:
                    pygame.draw.circle(
                        surface,
                        self._empty,
                        (col*self._square_size + self._square_size//2,
                         row*self._square_size + self._square_size +
                         self._square_size//2
                         ),
                        self._radius)
                elif self._state.board[col][row] == 1:
                    pygame.draw.circle(
                        surface,
                        self._p1_color,
                        (col*self._square_size + self._square_size//2,
                         row*self._square_size + self._square_size +
                         self._square_size//2
                         ),
                        self._radius)
                elif self._state.board[col][row] == 2:
                    pygame.draw.circle(
                        surface,
                        self._p2_color,
                        (col*self._square_size + self._square_size//2,
                         row*self._square_size + self._square_size +
                         self._square_size//2
                         ),
                        self._radius)

    def _draw_player_turn(self):
        """Display the player turn at the top of the screen."""
        surface = pygame.display.get_surface()
        turn = "It's Player {}'s Turn!".format(self._state.turn)
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render(turn, True, (0, 0, 0))
        surface.blit(text, (10, 10))

    def _draw_error(self):
        """Display an error is an invalid move is made."""
        surface = pygame.display.get_surface()
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Invalid move! Try again!", True, (255, 0, 0))
        surface.blit(text, (self._width - 370, self._height -
                            (cf.BOARD_ROWS * self._square_size + 90)))

    def _draw_winner(self):
        """Display the winner of the game."""
        surface = pygame.display.get_surface()
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render("Gamer Over! Winner is Player " +
                           str(self._winner) + "!", True, (255, 0, 0))
        surface.blit(text, (8, 50))
        pygame.draw.rect(
            surface,
            (200, 240, 180),
            (self._width - 200,
             self._height - (cf.BOARD_ROWS * self._square_size + 90),
             100, 35))
        # Give the players the option to restart the game.
        font1 = pygame.font.Font('freesansbold.ttf', 20)
        restart = font1.render('Restart?', True, (0, 0, 0))
        surface.blit(restart, (self._width - 190, self._height -
                               (cf.BOARD_ROWS * self._square_size + 80)))

    def _handle_click(self, pos, left_right):
        """
        Assign moves to the mouse so that if the player right clicks,
        a piece is dropped and if the player left clicks, a piece is
        popped.
        """
        x = pos[0]
        _on_col = x // self._square_size
        restart = pygame.Rect(self._width - 200,
                              self._height -
                              (cf.BOARD_ROWS * self._square_size + 90),
                              100, 35)
        if self._gameover():
            if restart.collidepoint(pos):
                self._state = cf.new_game()
        else:
            try:
                if left_right == 1:
                    self._state = cf.drop(self._state, _on_col)
                elif left_right == 3:
                    self._state = cf.pop(self._state, _on_col)
                self._error = False
            except cf.InvalidMoveError:
                self._error = True

    def _gameover(self):
        """Determine the winner """
        self._winner = cf.winner(self._state)
        return self._winner != 0

    def _end_game(self):
        """End the game."""
        self._running = False
