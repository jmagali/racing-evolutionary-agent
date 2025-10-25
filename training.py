import pygame
import os
import math
import sys
import neat
import time
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
    
def remove(index):
    cars.pop(index)
    ge.pop(index)
    networks.pop(index)
    
def eval_genomes(genomes, config):
    global cars, ge, networks
    
    cars = []
    ge = []
    networks = []
    
    for _, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)
        genome.fitness = 0
    
    # Training loop
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Add the track to the buffer
        WINDOW.blit(TRACK, (0, 0))
        
        # End generation when no genomes are left
        if len(cars) == 0:
            break
        
        # Give fitness for positive qualities
        for i, car in enumerate(cars):
            ge[i].fitness += 1
            # Remove dead genomes
            if not car.sprite.alive:
                remove(i)

        for i, car in enumerate(cars):
            output = networks[i].activate(car.sprite.data())
            if output[0] > 0.7:
                car.sprite.direction = 1
                ge[i].fitness += 0.3
            if output[1] > 0.7:
                car.sprite.direction = -1
                ge[i].fitness += 0.3
            if output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0

        # Update visuals
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