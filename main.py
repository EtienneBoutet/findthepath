#!/usr/bin/env python3

import pygame

# Constants
WINDOW_SIZE = [510, 510]
BLACK = (0, 0 ,0)

'''
    Start function
'''
def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Find the path")

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(BLACK)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()

