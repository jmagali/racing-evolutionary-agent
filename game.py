import pygame
import os
import sys

WIN_WIDTH = 1244
WIN_HEIGHT = 1016
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
TRACK = pygame.image.load(os.path.join("assets", "track.png"))        
        
class Car (pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.org_img = pygame.image.load(os.path.join("assets", "car.png"))
        self.image = self.org_img
        self.rect = self.image.get_rect(center=(490, 820))
        self.drive_state = False
        self.vel = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0

    def update (self):
        self.drive()
        self.rotate()
        
    def drive (self):
        if self.drive_state:
            self.rect.center += self.vel * 6
            
    def rotate (self):
        ROTATION = 0.1
        
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel.rotate_ip(self.rotation_vel)
            
        self.image = pygame.transform.rotozoom(self.org_img, self.angle, ROTATION)
        self.rect = self.image.get_rect(center=self.rect.center)
    
car = pygame.sprite.GroupSingle(Car())

def eval_genomes():
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


        car.draw(WINDOW)
        car.update()
        pygame.display.update()
        
eval_genomes()