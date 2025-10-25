import pygame
import os

class CarParameters:
    def __init__(self):
        # Physics parameters
        self.velocity = 0.8
        self.rotation_vel = 5
        
        # Collision parameters
        self.collision_radius = 45
        self.collision_angle = 18
        
        # Radar parameter
        self.radar_count = 5
        
class NEATParameters:
    def __init__(self):
        # Training Parameters
        self.population_size = 50
        self.generations = 50
        self.fitness_threshold = 1000
        self.stagnation_threshold = 20
        self.mutation_rate = 0.3
        
        # Network parameters
        self.num_inputs = car_params.radar_count
        self.num_outputs = 2  # Left/Right control
        self.num_hidden = 1
        
class WindowParameters:
    def __init__ (self):
        self.width = 1244
        self.height = 1016
        self.window = pygame.display.set_mode((self.width, self.height))
        self.track = pygame.image.load(os.path.join("assets", "track.png"))        

# Global instances
car_params = CarParameters()
neat_params = NEATParameters()
window_params = WindowParameters()