import pygame
import sys
from random import randrange

# Color Definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (127, 127, 127)

# Grid Settings
CELL_WIDTH = 30
CELL_HEIGHT = 30
GRID_SIZE = 10
CELL_MARGIN = 5
UI_MARGIN = 40

# Mouse Buttons
LEFT_BUTTON = 1
RIGHT_BUTTON = 3

# Main Game Class
class MinesweeperGame:
    def __init__(self):
        self.grid = [[Cell(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.game_initialized = False
        self.game_lost = False
        self.game_won = False
        self.total_bombs = 10
        self.grid_width = GRID_SIZE
        self.grid_height = GRID_SIZE
        self.needs_resize = False
        self.flags_placed = 0

    def draw_grid(self):
        screen.fill(COLOR_BLACK)
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                cell_color = COLOR_WHITE
                if self.grid[row][col].is_revealed:
                    cell_color = COLOR_RED if self.grid[row][col].has_bomb else COLOR_GRAY
                elif self.grid[row][col].is_flagged:
                    cell_color = COLOR_BLUE
                pygame.draw.rect(screen,
                                cell_color,
                                [(CELL_MARGIN + CELL_WIDTH) * col + CELL_MARGIN,
                                 (CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN + UI_MARGIN,
                                 CELL_WIDTH,
                                 CELL_HEIGHT])
                self.grid[row][col].render_text()

    def resize_grid(self, new_width, new_height):
        global screen
        self.grid_width = (new_width - CELL_MARGIN) // (CELL_WIDTH + CELL_MARGIN)
        self.grid_height = (new_height - CELL_MARGIN - UI_MARGIN) // (CELL_HEIGHT + CELL_MARGIN)
        if self.grid_width < 8:
            self.grid_width = 8
        if self.grid_height < 8:
            self.grid_height = 8
        if self.total_bombs > (self.grid_width * self.grid_height) // 3:
            self.total_bombs = self.grid_width * self.grid_height // 3
        self.grid = [[Cell(x, y) for x in range(self.grid_width)] for y in range(self.grid_height)]
        size = ((self.grid_width * (CELL_WIDTH + CELL_MARGIN) + CELL_MARGIN),
                (self.grid_height * (CELL_HEIGHT + CELL_MARGIN) + CELL_MARGIN + UI_MARGIN))
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    def reveal_all_cells(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.grid[row][col].has_bomb:
                    self.grid[row][col].is_revealed = True
                self.grid[row][col].is_flagged = False

    def update_bomb_count(self, bomb_delta):
        self.total_bombs += bomb_delta
        if self.total_bombs < 1:
            self.total_bombs = 1
        elif self.total_bombs > (self.grid_width * self.grid_height) // 3:
            self.total_bombs = self.grid_width * self.grid_height // 3
        self.reset_game()

    def place_bombs(self, init_row, init_col):
        bombs_placed = 0
        while bombs_placed < self.total_bombs:
            x = randrange(self.grid_height)
            y = randrange(self.grid_width)
            if not self.grid[x][y].has_bomb and not (init_row == x and init_col == y):
                self.grid[x][y].has_bomb = True
                bombs_placed += 1
        self.update_all_bomb_counts()
        if self.grid[init_row][init_col].adjacent_bombs != 0:
            self.reset_game()
            self.place_bombs(init_row, init_col)

    def update_all_bomb_counts(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                self.grid[row][col].calculate_adjacent_bombs(self.grid_height, self.grid_width)

    def reset_game(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                self.game_initialized = False
                self.grid[row][col].reset()
                self.game_lost = False
                self.game_won = False
                self.flags_placed = 0

    def check_for_victory(self):
        revealed_count = sum(1 for row in range(self.grid_height) for col in range(self.grid_width) if self.grid[row][col].is_revealed)
        total_cells = self.grid_width * self.grid_height
        if (total_cells - revealed_count) == self.total_bombs and not self.game_lost:
            self.game_won = True
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    if self.grid[row][col].has_bomb:
                        self.grid[row][col].is_flagged = True

    def count_flags(self):
        self.flags_placed = sum(1 for row in range(self.grid_height) for col in range(self.grid_width) if self.grid[row][col].is_flagged)

    def handle_click(self, row, col, button):
        if button == LEFT_BUTTON and self.game_won:
            self.reset_game()
        elif button == LEFT_BUTTON and not self.grid[row][col].is_flagged:
            if not self.game_lost:
                if not self.game_initialized:
                    self.place_bombs(row, col)
                    self.game_initialized = True
                self.grid[row][col].is_revealed = True
                self.grid[row][col].is_flagged = False
                if self.grid[row][col].has_bomb:
                    self.reveal_all_cells()
                    self.game_lost = True
                elif self.grid[row][col].adjacent_bombs == 0:
                    self.grid[row][col].reveal_neighbours(self.grid_height, self.grid_width)
                self.check_for_victory()
            else:
                self.game_lost = False
                self.reset_game()
        elif button == RIGHT_BUTTON and not self.game_won:
            if not self.grid[row][col].is_flagged:
                if self.flags_placed < self.total_bombs and not self.grid[row][col].is_revealed:
                    self.grid[row][col].is_flagged = True
            else:
                self.grid[row][col].is_flagged = False
            self.count_flags()

# Cell Class for each grid cell
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_revealed = False
        self.has_bomb = False
        self.adjacent_bombs = 0
        self.text = ""
        self.calculated = False
        self.is_flagged = False

    def render_text(self):
        if self.is_revealed:
            self.text = font.render(str(self.adjacent_bombs), True, COLOR_BLACK) if self.adjacent_bombs > 0 else font.render("", True, COLOR_BLACK)
            screen.blit(self.text, (self.x * (CELL_WIDTH + CELL_MARGIN) + 12, self.y * (CELL_HEIGHT + CELL_MARGIN) + 10 + UI_MARGIN))

    def calculate_adjacent_bombs(self, grid_height, grid_width):
        if not self.calculated:
            self.calculated = True
            if not self.has_bomb:
                for col in range(self.x - 1, self.x + 2):
                    for row in range(self.y - 1, self.y + 2):
                        if (0 <= row < grid_height and 0 <= col < grid_width
                            and not (col == self.x and row == self.y)
                            and minesweeper.grid[row][col].has_bomb):
                            self.adjacent_bombs += 1

    def reveal_neighbours(self, grid_height, grid_width):
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                if ((row_offset == 0 or col_offset == 0) and row_offset != col_offset
                    and 0 <= self.y + row_offset < grid_height and 0 <= self.x + col_offset < grid_width):
                    neighbour = minesweeper.grid[self.y + row_offset][self.x + col_offset]
                    neighbour.calculate_adjacent_bombs(grid_height, grid_width)
                    if not neighbour.is_revealed and not neighbour.has_bomb:
                        neighbour.is_revealed = True
                        neighbour.is_flagged = False
                        if neighbour.adjacent_bombs == 0:
                            neighbour.reveal_neighbours(grid_height, grid_width)

    def reset(self):
        self.is_revealed = False
        self.has_bomb = False
        self.adjacent_bombs = 0
        self.calculated = False
        self.is_flagged = False

# UI Class for the Menu
class GameMenu:
    def __init__(self):
        self.width = pygame.display.get_surface().get_width() - 2 * CELL_MARGIN
        self.decrement_button = Button(10, 10, 20, 20, "-", 6, -3)
        self.increment_button = Button(60, 10, 20, 20, "+", 3, -4)
        self.flag_icon = Button(280, 16, 10, 10, "")
        self.flag_icon.background_color = COLOR_BLUE
        self.bombs_label = Label(30, 10)
        self.status_label = Label(100, 10)
        self.flags_label = Label(self.width - 50, 10)

    def handle_click(self, game_instance):
        if self.decrement_button.check_click():
            game_instance.update_bomb_count(-1)
        if self.increment_button.check_click():
            game_instance.update_bomb_count(1)

    def draw(self, game_instance):
        self.width = pygame.display.get_surface().get_width() - 2 * CELL_MARGIN
        pygame.draw.rect(screen, COLOR_GRAY, [CELL_MARGIN, 0, self.width, UI_MARGIN])
        self.decrement_button.draw(screen)
        self.increment_button.draw(screen)
        self.flag_icon.draw(screen)
        self.bombs_label.render(screen, game_instance.total_bombs)
        self.flags_label.render(screen, game_instance.flags_placed)
        if game_instance.game_lost:
            self.status_label.render(screen, "Game Over")
        elif game_instance.game_won:
            self.status_label.render(screen, "You Won!")

class Label:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.text = ""

    def render(self, surface, value):
        text = str(value)
        self.text = font.render(text, True, COLOR_BLACK)
        surface.blit(self.text, (self.x, self.y))

class Button:
    def __init__(self, x, y, width, height, text, x_offset=0, y_offset=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background_color = COLOR_WHITE
        self.text = text
        self.x_offset = x_offset
        self.y_offset = y_offset

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.background_color, [self.x, self.y, self.width, self.height], 0)
        text = font.render(self.text, True, COLOR_BLACK)
        surface.blit(text, (self.x + self.x_offset, self.y + self.y_offset))

    def check_click(self):
        pos = pygame.mouse.get_pos()
        return self.x <= pos[0] <= (self.x + self.width) and self.y <= pos[1] <= (self.y + self.height)

# Initialize Pygame
pygame.init()
initial_size = (GRID_SIZE * (CELL_WIDTH + CELL_MARGIN) + CELL_MARGIN, (GRID_SIZE * (CELL_HEIGHT + CELL_MARGIN) + CELL_MARGIN) + UI_MARGIN)
screen = pygame.display.set_mode(initial_size, pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper")
font = pygame.font.Font('freesansbold.ttf', 24)

# Game and Menu Instances
minesweeper = MinesweeperGame()
menu = GameMenu()
game_clock = pygame.time.Clock()

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            col = position[0] // (CELL_WIDTH + CELL_MARGIN)
            row = (position[1] - UI_MARGIN) // (CELL_HEIGHT + CELL_MARGIN)
            if row >= minesweeper.grid_height:
                row = minesweeper.grid_height - 1
            if col >= minesweeper.grid_width:
                col = minesweeper.grid_width - 1
            if row >= 0:
                minesweeper.handle_click(row, col, event.button)
            else:
                menu.handle_click(minesweeper)
        elif event.type == pygame.VIDEORESIZE:
            if minesweeper.needs_resize:
                minesweeper.resize_grid(event.w, event.h)
                minesweeper.reset_game()
            else:
                minesweeper.needs_resize = True

    minesweeper.draw_grid()
    menu.draw(minesweeper)
    game_clock.tick(60)
    pygame.display.flip()
