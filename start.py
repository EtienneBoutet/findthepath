import pygame


def colorCells(grid, mouseEventType):
    pos = pygame.mouse.get_pos()
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)
    if mouseEventType == (1, 0, 0):
        grid[row][column] = 1
    else:
        grid[row][column] = 2
    return grid


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 20
HEIGHT = 20
MARGIN = 5

# creating the grid (10 x 10)
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append(0)

pygame.init()

WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Array Backed Grid")

done = False

clock = pygame.time.Clock()

draging = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            draging = True
            colorCells(grid, pygame.mouse.get_pressed())
        elif event.type == pygame.MOUSEBUTTONUP:
            draging = False
        elif event.type == pygame.MOUSEMOTION:
            if draging:
                colorCells(grid, pygame.mouse.get_pressed())

    screen.fill(BLACK)

    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 2:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    clock.tick(60)

    pygame.display.flip()

pygame.quit()
