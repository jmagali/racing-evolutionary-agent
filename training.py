import pygame
import os
import math
import sys
import neat

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
        self.vel = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []
        
    def update (self):
        self.radars.clear()
        self.drive()
        self.rotate()
        for radar_angle in (-60, -45, -30, 0, 30, 45, 60):
            self.radar(radar_angle)
        self.collision()
        self.data()
        
    def collision (self):
        length = 45
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length)]
        collision_point_left = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length)]
        
        # Die on Collision
        if WINDOW.get_at(collision_point_right) == pygame.Color(2, 105, 31, 255) \
                or WINDOW.get_at(collision_point_left) == pygame.Color(2, 105, 31, 255):
            self.alive = False

        # Draw Collision Points
        pygame.draw.circle(WINDOW, (0, 255, 255, 0), collision_point_right, 6)
        pygame.draw.circle(WINDOW, (0, 255, 255, 0), collision_point_left, 6)
        
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

        while True:  # Maximum radar length of 200 pixels
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
        input = [0] * 7
        
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        
        return input
    
def remove(index):
    cars.pop(index)
    ge.pop(index)
    networks.pop(index)
    
def eval_genomes(genomes, config):
    global cars, ge, networks
    
    cars = []
    ge = []
    networks = []
    
    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)
        genome.fitness = 0
    
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.blit(TRACK, (0, 0))
        
        if len(cars) == 0:
            break
        
        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if not car.sprite.alive:
                remove(i)

        for i, car in enumerate(cars):
            output = networks[i].activate(car.sprite.data())
            if output[0] > 0.7:
                car.sprite.direction = 1
            if output[1] > 0.7:
                car.sprite.direction = -1
            if output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0

        for car in cars:
            car.draw(WINDOW)
            car.update()
        
        pygame.display.update()
        
def run (config_path):
    global pop
    GENERATAIONS = 50
    
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, GENERATAIONS)
    
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)