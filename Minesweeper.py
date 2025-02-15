import pygame
import sys
from random import randrange

# Initialize Pygame
pygame.init()

# Color Definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (180, 180, 180)

# Grid Settings
CELL_SIZE = 30
CELL_MARGIN = 5
GRID_SIZE = 10
UI_MARGIN = 40
TOTAL_BOMBS = 10

# Mouse Buttons
LEFT_BUTTON = 1
RIGHT_BUTTON = 3

# Font
font = pygame.font.Font(None, 24)

# Pygame Screen Setup
WINDOW_SIZE = (GRID_SIZE * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN,
               GRID_SIZE * (CELL_SIZE + CELL_MARGIN) + UI_MARGIN + CELL_MARGIN)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper")


class Cell:
    """ Represents each cell in the Minesweeper grid. """
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.is_revealed = False
        self.has_bomb = False
        self.adjacent_bombs = 0
        self.is_flagged = False

    def reveal(self):
        """ Reveals the cell and returns True if it's a bomb. """
        if not self.is_flagged:
            self.is_revealed = True
            return self.has_bomb
        return False

    def toggle_flag(self):
        """ Toggles the flagged state of a cell. """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

    def draw(self):
        """ Draws the cell on the screen. """
        x_pos = self.x * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
        y_pos = self.y * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN + UI_MARGIN
        color = COLOR_WHITE

        if self.is_revealed:
            color = COLOR_RED if self.has_bomb else COLOR_GRAY
        elif self.is_flagged:
            color = COLOR_BLUE

        pygame.draw.rect(screen, color, [x_pos, y_pos, CELL_SIZE, CELL_SIZE])

        if self.is_revealed and self.adjacent_bombs > 0 and not self.has_bomb:
            text_surface = font.render(str(self.adjacent_bombs), True, COLOR_BLACK)
            screen.blit(text_surface, (x_pos + 10, y_pos + 5))


class MinesweeperGame:
    """ The main Minesweeper game logic. """
    def __init__(self):
        self.grid = [[Cell(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.game_initialized = False
        self.game_over = False
        self.game_won = False
        self.total_bombs = TOTAL_BOMBS
        self.flags_placed = 0

    def place_bombs(self, first_click_x, first_click_y):
        """ Randomly places bombs on the grid, avoiding the first clicked cell. """
        bombs_placed = 0
        while bombs_placed < self.total_bombs:
            x, y = randrange(GRID_SIZE), randrange(GRID_SIZE)
            if not self.grid[y][x].has_bomb and (x != first_click_x or y != first_click_y):
                self.grid[y][x].has_bomb = True
                bombs_placed += 1

        self.update_adjacent_counts()

    def update_adjacent_counts(self):
        """ Updates the number of adjacent bombs for each cell. """
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if not self.grid[y][x].has_bomb:
                    count = sum(
                        self.grid[ny][nx].has_bomb
                        for nx in range(max(0, x - 1), min(GRID_SIZE, x + 2))
                        for ny in range(max(0, y - 1), min(GRID_SIZE, y + 2))
                        if (nx, ny) != (x, y)
                    )
                    self.grid[y][x].adjacent_bombs = count

    def reveal_empty_neighbors(self, x, y):
        """ Recursively reveals empty neighboring cells. """
        for nx in range(max(0, x - 1), min(GRID_SIZE, x + 2)):
            for ny in range(max(0, y - 1), min(GRID_SIZE, y + 2)):
                neighbor = self.grid[ny][nx]
                if not neighbor.is_revealed and not neighbor.has_bomb:
                    neighbor.reveal()
                    if neighbor.adjacent_bombs == 0:
                        self.reveal_empty_neighbors(nx, ny)

    def reveal_all_cells(self):
        """ Reveals all cells when the game is over. """
        for row in self.grid:
            for cell in row:
                cell.is_revealed = True

    def check_victory(self):
        """ Checks if all non-bomb cells are revealed. """
        revealed_count = sum(1 for row in self.grid for cell in row if cell.is_revealed)
        if (GRID_SIZE * GRID_SIZE - revealed_count) == self.total_bombs:
            self.game_won = True
            for row in self.grid:
                for cell in row:
                    if cell.has_bomb:
                        cell.is_flagged = True

    def handle_click(self, x, y, button):
        """ Handles left and right mouse clicks on the grid. """
        if self.game_over or self.game_won:
            self.reset_game()
            return

        cell = self.grid[y][x]

        if button == LEFT_BUTTON and not cell.is_flagged:
            if not self.game_initialized:
                self.place_bombs(x, y)
                self.game_initialized = True

            if cell.reveal():
                self.reveal_all_cells()
                self.game_over = True
            elif cell.adjacent_bombs == 0:
                self.reveal_empty_neighbors(x, y)

            self.check_victory()

        elif button == RIGHT_BUTTON:
            cell.toggle_flag()
            self.flags_placed = sum(1 for row in self.grid for cell in row if cell.is_flagged)

    def reset_game(self):
        """ Resets the game state. """
        self.grid = [[Cell(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.game_initialized = False
        self.game_over = False
        self.game_won = False
        self.flags_placed = 0

    def draw_grid(self):
        """ Draws the entire grid and UI. """
        screen.fill(COLOR_BLACK)

        for row in self.grid:
            for cell in row:
                cell.draw()

        # UI Display
        text = f"Bombs: {self.total_bombs} | Flags: {self.flags_placed}"
        label = font.render(text, True, COLOR_WHITE)
        screen.blit(label, (10, 10))


# Game Loop
minesweeper = MinesweeperGame()
running = True

while running:
    screen.fill(COLOR_BLACK)
    minesweeper.draw_grid()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // (CELL_SIZE + CELL_MARGIN)
            grid_y = (my - UI_MARGIN) // (CELL_SIZE + CELL_MARGIN)
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                minesweeper.handle_click(grid_x, grid_y, event.button)

pygame.quit()
sys.exit()
