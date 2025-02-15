import pygame
import random

# Constants
GRID_SIZE = 10
CELL_SIZE = 40
MINE_COUNT = 15
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, (GRID_SIZE * CELL_SIZE) + 50

# Colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Font
font = pygame.font.Font(None, 36)

# Board Setup
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
mines = set()

# Place Mines
while len(mines) < MINE_COUNT:
    r, c = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    if (r, c) not in mines:
        mines.add((r, c))
        grid[r][c] = -1  # -1 represents a mine

# Calculate Numbers
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        if grid[r][c] == -1:
            continue
        count = sum((nr, nc) in mines for nr in range(r-1, r+2) for nc in range(c-1, c+2) if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE)
        grid[r][c] = count

# Function to reveal a cell and its immediate zero neighbors
def reveal_cell(r, c):
    if revealed[r][c] or grid[r][c] == -1:
        return
    revealed[r][c] = True

    # Only reveal immediate "0" neighbors
    if grid[r][c] == 0:
        for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and not revealed[nr][nc]:
                revealed[nr][nc] = True

# Main Game Loop
running = True
while running:
    screen.fill(WHITE)

    # Draw Board
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY if revealed[r][c] else BLACK, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)

            if revealed[r][c]:
                if grid[r][c] == -1:
                    pygame.draw.rect(screen, RED, rect)
                elif grid[r][c] > 0:
                    text = font.render(str(grid[r][c]), True, BLACK)
                    screen.blit(text, (c * CELL_SIZE + 10, r * CELL_SIZE + 5))

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if row < GRID_SIZE:
                reveal_cell(row, col)

    pygame.display.flip()

pygame.quit()
