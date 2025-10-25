import pygame
import game
import sys

def eval_genomes():
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(TRACK, (0, 0))
        
        user_input = pygame.key.get_pressed()