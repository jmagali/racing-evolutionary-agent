import pygame
import os
import math
import sys
import neat
import parameters
        
class Car (pygame.sprite.Sprite):
    # Window
    global WIN_WIDTH
    global WIN_HEIGHT
    global WINDOW
    
    WIN_WIDTH = parameters.window_params.width
    WIN_HEIGHT = parameters.window_params.height
    WINDOW = parameters.window_params.window
    
    def __init__ (self):
        super().__init__()
        
        # Visuals
        self.org_img = pygame.image.load(os.path.join("assets", "car.png"))
        self.image = self.org_img
        self.rect = self.image.get_rect(center=(490, 820))
        
        # Movement
        self.vel = pygame.math.Vector2(parameters.car_params.velocity, 0)
        self.angle = 0
        self.rotation_vel = parameters.car_params.rotation_vel
        self.direction = 0
        
        # Misc
        self.alive = True
        self.radars = []
        self.radar_angles = []
        
        self.calculate_radar_angles()
        
    def update (self):
        self.radars.clear()
        self.drive()
        self.rotate()
        
        for radar_angle in self.radar_angles:
            self.radar(radar_angle)
        self.collision()
        self.data()
        
    def calculate_radar_angles (self):
        increment = 120 // parameters.car_params.radar_count
        current = -60
        
        for i in range(parameters.car_params.radar_count):
            angle = current + increment
            current += increment
            self.radar_angles.append(angle)
        
    def collision (self):   
        length = 45
        back_extension = 1.2
        radius = 1
        
        # Front collision points
        collision_point_front_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + parameters.car_params.collision_angle)) * length),
                                     int(self.rect.center[1] - math.sin(math.radians(self.angle + parameters.car_params.collision_angle)) * length)]
        collision_point_front_left = [int(self.rect.center[0] + math.cos(math.radians(self.angle - parameters.car_params.collision_angle)) * length),
                                    int(self.rect.center[1] - math.sin(math.radians(self.angle - parameters.car_params.collision_angle)) * length)]
        
        # Back collision points
        collision_point_back_right = [int(self.rect.center[0] - math.cos(math.radians(self.angle + parameters.car_params.collision_angle)) * length * back_extension),
                                    int(self.rect.center[1] + math.sin(math.radians(self.angle + parameters.car_params.collision_angle)) * length * back_extension)]
        collision_point_back_left = [int(self.rect.center[0] - math.cos(math.radians(self.angle - parameters.car_params.collision_angle)) * length * back_extension),
                                   int(self.rect.center[1] + math.sin(math.radians(self.angle - parameters.car_params.collision_angle)) * length * back_extension)]
        
        # Die on Collision
        if (WINDOW.get_at(collision_point_front_right) == pygame.Color(2, 105, 31, 255) or
            WINDOW.get_at(collision_point_front_left) == pygame.Color(2, 105, 31, 255) or
            WINDOW.get_at(collision_point_back_right) == pygame.Color(2, 105, 31, 255) or
            WINDOW.get_at(collision_point_back_left) == pygame.Color(2, 105, 31, 255)):
            self.alive = False
        
    def drive (self):
        self.rect.center += self.vel * 5
            
    def rotate (self):
        SIZE = 0.1
        
        # Calculate rotation
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel.rotate_ip(-self.rotation_vel)
            
        # Display rotation
        self.image = pygame.transform.rotozoom(self.org_img, self.angle, SIZE)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        # Extend radars to boundary
        while length < 200:
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)
            
            # Check if we're out of bounds
            if x < 0 or x >= WIN_WIDTH or y < 0 or y >= WIN_HEIGHT:
                break
                
            # Check if we've hit the track boundary
            try:
                if WINDOW.get_at((x, y)) == pygame.Color(2, 105, 31, 255):
                    break
            except IndexError:
                break
                
            length += 1

        # Draw Radar
        pygame.draw.line(WINDOW, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(WINDOW, (0, 255, 0, 0), (x, y), 3)
        
        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2)
                             + math.pow(self.rect.center[1] - y, 2)))
        
        self.radars.append([radar_angle, dist])
        
    def data(self):
        input = [0] * parameters.car_params.radar_count
        
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        
        return input