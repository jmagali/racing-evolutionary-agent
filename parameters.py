import pygame
import os

class CarParameters:
    def __init__(self):
        # Physics parameters
        self.velocity = 20
        self.acceleration = 2
        self.angle = 10
        
        # Collision parameters
        self.collision_radius = 45
        self.collision_angle = 18
        
        # Radar parameter
        self.radar_count = 5
    
    def update(self, acc, vel, ang):
        self.acceleration = acc
        self.velocity = vel
        self.angle = ang
                
class NEATParameters:
    def __init__(self):
        # Training Parameters
        self.population_size = 50
        
        # Network parameters
        self.num_inputs = car_params.radar_count
        self.num_outputs = 2  # Left/Right control
        self.num_hidden = 1
        
    def update(self, population):
        self.population_size = population
        
class WindowParameters:
    def __init__ (self):
        self.width = 1244
        self.height = 1016
        self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.track = pygame.image.load(os.path.join("assets", "track.png"))

# Global instances
car_params = CarParameters()
neat_params = NEATParameters()
window_params = WindowParameters()