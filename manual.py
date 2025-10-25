import pygame
import os
import math
import sys
from car import Car
import parameters

# Window
global WIN_WIDTH
global WIN_HEIGHT
global WINDOW
    
WIN_WIDTH = parameters.window_params.width
WIN_HEIGHT = parameters.window_params.height
WINDOW = parameters.window_params.window   
TRACK = parameters.window_params.track      
    
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