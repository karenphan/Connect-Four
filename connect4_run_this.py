import pygame
import connectfour as cf
import connect4_game as game

color_inactive = pygame.Color(255, 255, 255)
color_active = pygame.Color(0, 191, 255)
custom_board = []


class ConnectFourGame:
    def __init__(self):
        """
        Initialize variables and the states of certain aspects of the game
        (such as errors and the game running state).
        """
        self._running = True
        self._screen = 1
        self.col = cf.BOARD_COLUMNS
        self.row = cf.BOARD_ROWS
        self._col_text = ''
        self._col_active = False
        self._col_error = False
        self._color_col_box = color_inactive
        self._row_text = ''
        self._row_active = False
        self._row_error = False
        self._color_row_box = color_inactive
        self._p1_color = (255, 0, 0)
        self._p2_color = (255, 255, 0)

    def run(self):
        """Run the game."""
        pygame.init()
        pygame.display.set_mode((600, 600))
        clock = pygame.time.Clock()

        while self._running:
            clock.tick(30)
            self._handle_events()
            try:
                self._draw_screen()
            except pygame.error:
                break

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
                self._handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key, event.unicode)

    def _draw_screen(self):
        """Draw the screen based on what number self._screen is."""
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(48, 69, 94))
        if self._screen == 1:
            self._start_screen()
        elif self._screen == 2:
            self._welcome_screen()
        elif self._screen == 3:
            self._customize_column_screen()
            self._customize_row_screen()
            self._customize_color_screen()
            surface = pygame.display.get_surface()
            font = pygame.font.Font('freesansbold.ttf', 17)
            if self._col_error is True:
                error = font.render('Invalid input! '
                                    'Please enter an integer greater than 3.',
                                    True, (255, 0, 0))
                surface.blit(error, (50, 160))

            if self._row_error is True:
                error = font.render('Invalid input! '
                                    'Please enter an integer greater than 3.',
                                    True, (255, 0, 0))
                surface.blit(error, (50, 290))

            font2 = pygame.font.Font('freesansbold.ttf', 20)
            status = pygame.font.Font('freesansbold.ttf', 20)
            # Show the current number of columns and rows.
            # The number changes when the user enters a valid
            # input in the box.
            col_instruct2 = font2.render('Current columns: {} '
                                         'Current rows: {}'
                                         .format(cf.BOARD_COLUMNS,
                                                 cf.BOARD_ROWS),
                                         True, (199, 221, 243))
            surface.blit(col_instruct2, (100, 400))

            # Show the current color for each player.
            # The color changes when the user presses on
            # any color option button.
            color_status = font2.render("Player 1:         Player 2:",
                                        True, (199, 221, 243))
            surface.blit(color_status, (100, 430))
            self._create_button(surface, self._p1_color, (205, 430, 20, 20),
                                'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
            self._create_button(surface, self._p2_color, (330, 430, 20, 20),
                                'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        elif self._screen == 4:
            self._game_screen()

        pygame.display.flip()

    def _handle_click(self, pos):
        """
        Determine what happens when the player clicks buttons
        on certain areas of the screen.
        """
        if self._screen == 1:
            start_button = pygame.Rect(200, 350, 200, 75)
            if start_button.collidepoint(pos):
                self._screen = 2
        elif self._screen == 2:
            yes_button = pygame.Rect(150, 475, 75, 50)
            no_button = pygame.Rect(350, 475, 75, 50)
            if yes_button.collidepoint(pos):
                self._screen = 3
            elif no_button.collidepoint(pos):
                self._screen = 4
        elif self._screen == 3:
            # To change the row or column, click on the input box
            # to activate it before entering input.
            col_input_box = pygame.Rect(100, 120, 200, 32)
            if col_input_box.collidepoint(pos):
                self._col_active = True
                self._color_col_box = color_active
            else:
                self._col_active = False
                self._color_col_box = color_inactive

            row_input_box = pygame.Rect(100, 250, 200, 32)
            if row_input_box.collidepoint(pos):
                self._row_active = True
                self._color_row_box = color_active
            else:
                self._row_active = False
                self._color_row_box = color_inactive
            play_button = pygame.Rect(150, 475, 100, 50)
            back_button = pygame.Rect(350, 475, 110, 50)
            if play_button.collidepoint(pos):
                self._screen = 4
            elif back_button.collidepoint(pos):
                self._screen = 2

            # Click on the button of the desired color
            # to change the player's color.
            c11 = pygame.Rect(40, 340, 20, 20)
            c12 = pygame.Rect(80, 340, 20, 20)
            c13 = pygame.Rect(120, 340, 20, 20)
            c14 = pygame.Rect(160, 340, 20, 20)
            c15 = pygame.Rect(200, 340, 20, 20)
            if c11.collidepoint(pos):
                self._p1_color = (250, 0, 0)
            elif c12.collidepoint(pos):
                self._p1_color = (250, 50, 50)
            elif c13.collidepoint(pos):
                self._p1_color = (250, 100, 100)
            elif c14.collidepoint(pos):
                self._p1_color = (250, 150, 150)
            elif c15.collidepoint(pos):
                self._p1_color = (250, 200, 200)

            c21 = pygame.Rect(310, 340, 20, 20)
            c22 = pygame.Rect(350, 340, 20, 20)
            c23 = pygame.Rect(390, 340, 20, 20)
            c24 = pygame.Rect(430, 340, 20, 20)
            c25 = pygame.Rect(470, 340, 20, 20)
            if c21.collidepoint(pos):
                self._p2_color = (250, 250, 0)
            elif c22.collidepoint(pos):
                self._p2_color = (200, 250, 50)
            elif c23.collidepoint(pos):
                self._p2_color = (150, 250, 100)
            elif c24.collidepoint(pos):
                self._p2_color = (100, 250, 150)
            elif c25.collidepoint(pos):
                self._p2_color = (50, 250, 200)

    def _handle_key(self, key, code):
        """
        Allow the user to enter input on the screen. An error is
        raised when the inputs are invalid.
        """
        if self._screen == 3:
            if self._col_active:
                if key == pygame.K_RETURN:
                    try:
                        col = int(self._col_text)
                        assert col > 3
                        cf.BOARD_COLUMNS = col
                        self._col_error = False
                    except ValueError:
                        self._col_error = True
                    except AssertionError:
                        self._col_error = True

                elif key == pygame.K_BACKSPACE:
                    self._col_text = self._col_text[:-1]
                else:
                    self._col_text += code

                if len(custom_board) == 2:
                    self._screen = 4

            if self._row_active:
                if key == pygame.K_RETURN:
                    try:
                        row = int(self._row_text)
                        assert row > 3
                        cf.BOARD_ROWS = row
                        self._row_error = False
                    except ValueError:
                        self._row_error = True
                    except AssertionError:
                        self._row_error = True

                elif key == pygame.K_BACKSPACE:
                    self._row_text = self._row_text[:-1]
                else:
                    self._row_text += code

    def _start_screen(self):
        """Display the start screen."""
        surface = pygame.display.get_surface()
        font = pygame.font.Font('Broadway.ttf', 75)
        title = font.render('Connect Four', True, (199, 221, 243))
        title_rect = title.get_rect()
        title_rect.center = (300, 200)
        surface.blit(title, title_rect)

        self._create_button(surface, (0, 240, 0), (200, 350, 200, 75),
                            'Broadway.ttf', 50, (0, 0, 0), 'START', (215, 355))

    def _welcome_screen(self):
        """
        Display the welcome screen which welcomes the players
        and gives instructions on how to play the game. This screen
        also asks the players if they want to customize the board.
        """
        surface = pygame.display.get_surface()
        font = pygame.font.Font('freesansbold.ttf', 25)

        welcome_message = ['** Welcome to Connectfour! **',
                           'This is a two-player game in',
                           'which you win by having four',
                           'connecting tokens.', ' ',
                           '---------Instructions---------',
                           'Player 1: ', 'Player 2: ',
                           'LEFT CLICK on column to DROP',
                           'RIGHT CLICK on column to POP',
                           'Standard board is 7 x 6.',
                           ' ', ' ',
                           'Do you wish to customize the board?']

        y_pos = 40
        for message in welcome_message:
            text = font.render(message, True, (199, 221, 243))
            text_rect = text.get_rect()
            text_rect.center = (300, y_pos)
            surface.blit(text, text_rect)
            y_pos += 30

        self._create_button(surface, self._p1_color, (370, 210, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, self._p2_color, (370, 240, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (0, 240, 0), (150, 475, 75, 50),
                            'Castellar.ttf', 30, (0, 0, 0), 'YES', (160, 480))
        self._create_button(surface, (240, 0, 0), (350, 475, 75, 50),
                            'Castellar.ttf', 30, (0, 0, 0), 'NO', (360, 480))

    def _customize_column_screen(self):
        """
        Create an input box that allows the players to enter an integer
        and customize the number of columns.
        """
        surface = pygame.display.get_surface()
        col_input_box = pygame.Rect(100, 120, 140, 32)
        font = pygame.font.Font('freesansbold.ttf', 30)
        txt_surface = font.render(self._col_text, True, self._color_col_box)
        # Allow the box to resize if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        col_input_box.w = width

        col_instruct1 = font.render('Enter an integer for columns:',
                                    True, (199, 221, 243))
        surface.blit(col_instruct1, (50, 50))

        surface.blit(txt_surface, (col_input_box.x+5, col_input_box.y+5))
        font2 = pygame.font.Font('freesansbold.ttf', 20)
        col_instruct2 = font2.render('Press ENTER to continue',
                                     True, (199, 221, 243))
        surface.blit(col_instruct2, (100, 90))

        pygame.draw.rect(surface, self._color_col_box, col_input_box, 2)

    def _customize_row_screen(self):
        """
        Create an input box that allows the players to enter an integer
        and customize the number of rows.
        """
        surface = pygame.display.get_surface()
        row_input_box = pygame.Rect(100, 250, 140, 32)
        font = pygame.font.Font('freesansbold.ttf', 30)
        txt_surface = font.render(self._row_text, True, self._color_row_box)
        # Allow the box to resize if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        row_input_box.w = width

        row_instruct = font.render('Enter an integer for rows:',
                                   True, (199, 221, 243))
        surface.blit(row_instruct, (50, 180))
        surface.blit(txt_surface, (row_input_box.x+5, row_input_box.y+5))
        font2 = pygame.font.Font('freesansbold.ttf', 20)
        col_instruct2 = font2.render('Press ENTER to continue',
                                     True, (199, 221, 243))
        surface.blit(col_instruct2, (100, 220))

        pygame.draw.rect(surface, self._color_row_box, row_input_box, 2)

    def _customize_color_screen(self):
        """Display the color options for player 1 and player 2."""
        surface = pygame.display.get_surface()
        font = pygame.font.Font('freesansbold.ttf', 20)
        p1_color = font.render("Pick a color for Player 1:", True,
                               (199, 221, 243))
        p2_color = font.render("Pick a color for Player 2:", True,
                               (199, 221, 243))
        surface.blit(p1_color, (40, 310))
        surface.blit(p2_color, (310, 310))

        # Color options for player 1.
        self._create_button(surface, (250, 0, 0), (40, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (250, 50, 50), (80, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (250, 100, 100), (120, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (250, 150, 150), (160, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (250, 200, 200), (200, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))

        # Color options for player 2.
        self._create_button(surface, (250, 250, 0), (310, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (200, 250, 50), (350, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (150, 250, 100), (390, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (100, 250, 150), (430, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (50, 250, 200), (470, 340, 20, 20),
                            'Castellar.ttf', 30, (0, 0, 0), '', (360, 480))
        self._create_button(surface, (0, 240, 0), (150, 475, 100, 50),
                            'Castellar.ttf', 30, (0, 0, 0), 'PLAY', (160, 480))

        self._create_button(surface, (240, 0, 0), (350, 475, 110, 50),
                            'Castellar.ttf', 30, (0, 0, 0), 'BACK', (360, 480))

    def _create_button(self, surface, color, dimension, font_type, font_size,
                       font_color, text, pos):
        """Create a button using these parameters."""
        pygame.draw.rect(surface, color, dimension)
        font = pygame.font.Font(font_type, font_size)
        button_text = font.render(text, True, font_color)
        surface.blit(button_text, pos)

    def _game_screen(self):
        """Display the game board and play the game."""
        game.ConnectFourGame(self._p1_color, self._p2_color).run()
        pygame.quit()

    def _end_game(self):
        """End the game."""
        self._running = False

if __name__ == "__main__":
    ConnectFourGame().run()
