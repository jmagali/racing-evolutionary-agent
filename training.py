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

global generation
generation = 0

WIN_WIDTH = parameters.window_params.width
WIN_HEIGHT = parameters.window_params.height
WINDOW = parameters.window_params.window   
TRACK = parameters.window_params.track
    
def remove(index):
    cars.pop(index)
    ge.pop(index)
    networks.pop(index)

def eval_genomes(genomes, config):
    from menu import main_menu
    from menu import parameter_screen
    from menu import get_font
    from button import Button

    global generation
    global cars, ge, networks
    font = get_font(25)

    cars = []
    ge = []
    networks = []
    
    generation += 1
    
    for _, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)
        genome.fitness = 0

    run = True
    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TRAINING_BACK.checkForInput(MOUSE_POS):
                    main_menu()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PARAMETER_BTN.checkForInput(MOUSE_POS):
                    parameter_screen()
                    
        winning_fitness = -1

        # Add the track to the buffer
        WINDOW.blit(TRACK, (0, 0))
        
        # End generation when no genomes are left
        if len(cars) == 0:
            break

        counter += 1

        # Give fitness for positive qualities
        for i, car in enumerate(cars):
            ge[i].fitness += car.sprite.distance / 50.0
            # Remove dead genomes
            if not car.sprite.alive:
                remove(i)

        for i, car in enumerate(cars):
            output = networks[i].activate(car.sprite.data())
            choice = output.index(max(output))
            if choice == 0:
                car.sprite.angle += parameters.car_params.angle  # Left
            elif choice == 1:
                car.sprite.angle -= parameters.car_params.angle  # Right
            elif choice == 2:
                if (car.sprite.speed - parameters.car_params.acceleration >= 12):
                    car.sprite.speed -= parameters.car_params.acceleration  # Slow Down
            else:
                car.sprite.speed += parameters.car_params.acceleration  # Speed Up
            
            # The greater the time lived, the greater the fitness
            ge[i].fitness += counter * 0.01
            
            if ge[i].fitness > winning_fitness:
                winning_fitness = ge[i].fitness

        # Update visuals
        for car in cars:
            car.draw(WINDOW)
            car.update()

        MOUSE_POS = pygame.mouse.get_pos()

        TRAINING_BACK = Button(image=None, pos=(75, 50), text_input="BACK", font=get_font(25), base_color="Black",
                              hovering_color="Gray")

        TRAINING_BACK.changeColor(MOUSE_POS)
        TRAINING_BACK.update(WINDOW)
        
        PARAMETER_BTN = Button(image=None, pos=(1000, 50), text_input="Change Parameters", font=get_font(25), base_color="Black",
            hovering_color="Gray")
        
        PARAMETER_BTN.changeColor(MOUSE_POS)
        PARAMETER_BTN.update(WINDOW)

        # Display car parameters
        acc_text = font.render(f'Acceleration: {parameters.car_params.acceleration} m/s^2', False, (0, 0, 0))
        WINDOW.blit(acc_text, (25,900))
        speed_text = font.render(f'Initial Speed: {parameters.car_params.velocity} m/s', False, (0, 0, 0))
        WINDOW.blit(speed_text, (25,930))
        angle_text = font.render(f'Rotation Angle: {parameters.car_params.angle}°', False, (0, 0, 0))
        WINDOW.blit(angle_text, (25,960))
        
        # Display training parameters
        fitness_text = font.render(f'Max Fitness: {int(winning_fitness)}', False, (0, 0, 0))
        WINDOW.blit(fitness_text, (750,900))
        population_text = font.render(f'Population: {len(cars)}', False, (0, 0, 0))
        WINDOW.blit(population_text, (750,930))
        generation_text = font.render(f'Generation: {generation}', False, (0, 0, 0))
        WINDOW.blit(generation_text, (750,960))
        
        pygame.display.update()

def run (config_path):
    global pop, generation
    generation = 0
    GENERATAIONS = 50

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    # Override config values with GUI entries
    config.pop_size = parameters.neat_params.population_size

    pop = neat.Population(config)
    
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, GENERATAIONS)
    
    pygame.quit()
    sys.exit()
    
def play_training():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)