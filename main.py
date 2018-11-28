#!/usr/bin/env python3

import math
import pygame
from pprint import pprint

# Constants
WINDOW_SIZE = [510, 510]

BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 20
HEIGHT = 20
MARGIN = 5

class Node:
    def __init__(self):
        self._color = None
        self._coordinates = None
        self._grid_coordinates = None
        self._distance_to_end = None
        self._cost = 0
        self._total_weight = 0
        self._parent_node = None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value

    @property
    def distance_to_end(self):
        return self._distance_to_end

    @distance_to_end.setter
    def distance_to_end(self, value):
        self._distance_to_end = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value

    @property
    def grid_coordinates(self):
        return self._grid_coordinates

    @grid_coordinates.setter
    def grid_coordinates(self, value):
        self._grid_coordinates = value

    @property
    def total_weight(self):
        return self._total_weight

    @total_weight.setter
    def total_weight(self, value):
        self._total_weight = value

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value):
        self._parent_node = value


'''
    Find the [x, y] coordinates of a node
'''
def get_node_coordinates(row, column):
    return [row * (WIDTH + MARGIN), column * (HEIGHT + MARGIN)]

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
        if not grid[row][column].color:
            grid[row][column].color = click_color
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
            node = grid[row][column]
            if node.color == 1:
                color = GREEN
            elif node.color == 2:
                color = RED
            elif node.color == 3:
                color = BLACK
            elif node.color == 4:
                color = (255, 10, 10)
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

'''
    Return a list of the adjacent nodes of a node.
'''
def find_adjacent_squares(grid, original_node, open_list, closed_list):
    node_row = original_node.grid_coordinates[0]
    node_column = original_node.grid_coordinates[1]

    for i in range(-1, 2):

        for j in range(-1, 2):
            adjacent_node_row = node_row + i
            adjacent_node_column = node_column + j

            if 0 <= adjacent_node_row <= 19 and 0 <= adjacent_node_column <= 19:
                adjacent_node = grid[adjacent_node_row][adjacent_node_column]

                if adjacent_node not in closed_list and adjacent_node.color != 3:
                    if adjacent_node in open_list:
                        new_total_weight = (original_node.cost + 1) + adjacent_node.distance_to_end

                        if new_total_weight < adjacent_node.total_weight:
                            adjacent_node.cost = original_node.cost + 1
                            adjacent_node.total_weight = adjacent_node.cost + adjacent_node.distance_to_end
                            adjacent_node.parent_node = original_node

                    else:
                        adjacent_node.cost = original_node.cost + 1
                        adjacent_node.total_weight = adjacent_node.cost + adjacent_node.distance_to_end
                        adjacent_node.parent_node = original_node
                        adjacent_node.color = 4
                        open_list.append(adjacent_node)
    return open_list
'''
    Find the best path to get to the end cell and will modify the grid's cell if they are in the best path
'''
def path_finding(grid):
    nodes = []
    for row in grid:
        for node in row:
            node.grid_coordinates = [grid.index(row), row.index(node)]
            node.coordinates = get_node_coordinates(grid.index(row), row.index(node))
            nodes.append(node)

    # Find the end node
    end_node = None
    for node in nodes:
        if node.color == 2:
            end_node = node
            break

    # Find the end node
    start_node = None
    for node in nodes:
        if node.color == 1:
            start_node = node
            break

    for node in nodes:
        x_distance = end_node.coordinates[0] - node.coordinates[0]
        y_distance = end_node.coordinates[1] - node.coordinates[1]

        node.distance_to_end = math.sqrt((x_distance ** 2 )+ (y_distance ** 2))

    # Find the start node

    closed_list = [start_node]
    open_list = []

    open_list = find_adjacent_squares(grid, start_node, open_list, closed_list)

    while open_list:
        if end_node in open_list:
            parent = end_node.parent_node
            while parent is not None:
                parent.color = 1
                parent = parent.parent_node
            break

        open_list.sort(key = lambda x: x.total_weight, reverse=False)
        current_node = open_list[0]
        open_list.remove(current_node)
        closed_list.append(current_node)
        open_list = find_adjacent_squares(grid, current_node, open_list, closed_list)

'''
    Find the position of a cell in the grid.
'''
def find_cell_position(grid, value):
    position = []
    for row in grid:
        for column in row:
            if column == value:
                position = [grid.index(row), row.index(column)]
                break
    return position

'''
    Start function
'''
def main():
    grid = [[Node() for j in range(20)] for i in range(20)]

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path_finding(grid)

        screen.fill(BLACK)
        draw_grid(grid, screen)

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()

