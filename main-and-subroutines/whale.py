"""
Style: main and subroutines
Components: main program and subroutines
Connectors: procedure calls
Constraints: components can't communicate using shared memory (e.g. global 
variables) 
Gains: change the implementation of a subroutine without affecting the main 
program.  
"""

from random import randint

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_w, K_s, K_a, K_d


############################################################

def process_input(prev_game_status, prev_direction):
    game_status = prev_game_status
    direction = prev_direction
    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = 0 # 0 for game over, 1 for play
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                game_status = 0
            elif key == K_SPACE:#pauses the game
                game_status = 1 if game_status == 2 else 2 
            elif key == K_w:
                direction = (0, -1)
            elif key == K_s:
                direction = (0, 1)
            elif key == K_a:
                direction = (-1, 0)
            elif key == K_d:
                direction = (1, 0)
    return game_status, direction

############################################################

def draw_everything(screen, mybox, pellets, borders):
    screen.fill((0, 100, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 101, 255), b) for b in borders]  # # Deep Sky Blue
    [pygame.draw.rect(screen, (205, 192, 103), p) for p in pellets]  # pink
    pygame.draw.rect(screen, (0, 191, 155), mybox)  # Deep Sky Blue
    pygame.display.update()

############################################################

def create_box(dims):
    w, h = dims
    box = pygame.Rect(w / 2, h / 2, 10, 10)  # start in middle of the screen
    direction = 0, 1  # start direction: down
    return box, direction

############################################################

def collide(box, boxes):
    # return True if box collides with any entity in boxes
    return box.collidelist(boxes) != -1
    
############################################################

def move(box, direction): 
    return box.move(direction[0]*2, direction[1]*2) 

############################################################

def create_borders(dims, thickness=2):
    w, h = dims
    return [pygame.Rect(0, 0, thickness, h),
            pygame.Rect(0, 0, w, thickness),
            pygame.Rect(w - thickness, 0, thickness, h),
            pygame.Rect(0, h - thickness, w, thickness),
            pygame.Rect(10, 50, 80, thickness),
            pygame.Rect(30, 80, thickness, 100)]
    
############################################################

def create_pellet(dims, offset):
    w, h = dims
    return pygame.Rect(randint(offset, w - offset),
                       randint(offset, h - offset), 5, 5)

def create_pellets(dims, qty, offset=10): 
    # this is the only subroutine independent of Pygame
    return [create_pellet(dims, offset) for _ in range(qty)]
    
def eat_and_replace_colliding_pellet(box, pellets, dims, offset=10):
    p_index = box.collidelist(pellets)
    if p_index != -1:  # ate a pellet: grow, and replace a pellet
        pellets[p_index] = create_pellet(dims, offset)
        box.size = box.width * 1.2, box.height * 1.2
    return box, pellets
    
############################################################

pygame.init()
clock = pygame.time.Clock()

# display
dims = 400, 300
screen = pygame.display.set_mode(dims)

# game objects
borders = create_borders(dims)
pellets = create_pellets(dims, 4)
mybox, direction = create_box(dims)

# game loop
game_status = 1  # 0 for game over, 1 for play, 2 for paused
while game_status:

    game_status, direction = process_input(game_status, direction)
    
    if game_status == 1:
    	mybox = move(mybox, direction)
    	if collide(mybox, borders):
        	mybox, direction = create_box(dims)
    	mybox, pellets = eat_and_replace_colliding_pellet(mybox, pellets, dims)
    
    	draw_everything(screen, mybox, pellets, borders)
    
    clock.tick(50)  # or sleep(.02) to have the loop Pygame-independent