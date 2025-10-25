import pygame
import os
import math
import sys
from car import Car

WIN_WIDTH = 1244
WIN_HEIGHT = 1016
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
TRACK = pygame.image.load(os.path.join("assets", "track.png"))        
    
car = pygame.sprite.GroupSingle(Car())

def play():
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.blit(TRACK, (0, 0))
        
        # User input
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            car.sprite.drive_state = False
            car.sprite.direction = 0
        
        # Drive
        if user_input[pygame.K_UP]:
            car.sprite.drive_state = True
            
        # Steer
        if user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1
        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1
            
        if not car.sprite.alive:
            pygame.quit()
            sys.exit()
            break
            
        car.draw(WINDOW)
        car.update()
        pygame.display.update()
        
play()