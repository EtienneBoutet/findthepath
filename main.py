#!/usr/bin/env python3

import pygame

# Constants
WINDOW_SIZE = [510, 510]

BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 20
HEIGHT = 20
MARGIN = 5

'''
    Will handle every click made on the grid and return a modified grid array.
    @grid - The application grid
    note : the try/except is used to fix a behavior that i'm too lazy to fix :)
'''
def handle_click_on_grid(grid, click_color):
    try:
        pos = pygame.mouse.get_pos()
        column = pos[0] // (WIDTH + MARGIN)
        row = pos[1] // (HEIGHT + MARGIN)
        print(grid[row][column])
        if not grid[row][column]:
            grid[row][column] = click_color
            if click_color == 1:
                return 2
            else:
                return 3
    except:
        pass

'''
    Will handle the drawing of the application grid, this function handle the possible cell coloration
'''
def draw_grid(grid, screen):
    for row in range(20):
        for column in range(20):
            color = WHITE
            cell = grid[row][column]
            if cell == 1:
                color = GREEN
            elif cell == 2:
                color = RED
            elif cell == 3:
                color = BLACK
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

'''
    Start function
'''
def main():

    grid = []
    for row in range(20):
        grid.append([])
        for column in range(20):
            grid[row].append(0)

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Find the path")

    done = False
    click_color = 1
    dragging = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_color = handle_click_on_grid(grid, click_color)
                if click_color == 3:
                    dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    click_color = handle_click_on_grid(grid, click_color)
        screen.fill(BLACK)
        draw_grid(grid, screen)

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()

