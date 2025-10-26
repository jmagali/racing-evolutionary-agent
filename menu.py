import pygame, sys
from button import Button
from training import play_training
import parameters

pygame.init()

SCREEN = parameters.window_params.window
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def parameter_screen():
    input_active = [False, False, False, False]
    user_text = [
        str(parameters.car_params.acceleration),
        str(parameters.car_params.velocity),
        str(parameters.car_params.angle),
        str(parameters.neat_params.population_size)
    ]

    input_boxes = [
        pygame.Rect(500, 300, 200, 40),
        pygame.Rect(500, 360, 200, 40),
        pygame.Rect(500, 420, 200, 40),
        pygame.Rect(500, 480, 200, 40),
    ]

    APPLY_BUTTON = Button(None, (640, 580), "APPLY", get_font(50), "Black", "Gray")
    BACK_BUTTON = Button(None, (100, 100), "BACK", get_font(40), "Black", "Gray")

    while True:
        SCREEN.fill("white")
        MOUSE_POS = pygame.mouse.get_pos()

        labels = [
            "Acceleration:",
            "Initial Speed:",
            "Rotation Angle:",
            "Population:"
        ]

        for i, label in enumerate(labels):
            text_surface = get_font(30).render(label, True, "Black")
            SCREEN.blit(text_surface, (25, input_boxes[i].y + 5))

        for i, box in enumerate(input_boxes):
            color = "Black" if input_active[i] else "Gray"
            pygame.draw.rect(SCREEN, color, box, 2)

            text_surface = get_font(30).render(user_text[i], True, "Black")
            SCREEN.blit(text_surface, (box.x + 5, box.y + 5))

        APPLY_BUTTON.changeColor(MOUSE_POS)
        APPLY_BUTTON.update(SCREEN)
        BACK_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    input_active[i] = box.collidepoint(event.pos)

                if APPLY_BUTTON.checkForInput(MOUSE_POS):
                    try:
                        acc = int(user_text[0])
                        vel = int(user_text[1])
                        ang = int(user_text[2])
                        pop = int(user_text[3])

                        parameters.car_params.update(acc, vel, ang)
                        parameters.neat_params.update(pop)
                        SCREEN.fill("black")
                        play_training()
                    except:
                        print("Invalid input: integers only")

                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    SCREEN.fill("black")
                    play_training()

            if event.type == pygame.KEYDOWN:
                for i in range(len(user_text)):
                    if input_active[i]:
                        if event.key == pygame.K_BACKSPACE:
                            user_text[i] = user_text[i][:-1]
                        elif event.unicode.isdigit():
                            user_text[i] += event.unicode
                        elif event.key == pygame.K_RETURN:
                            input_active[i] = False

        pygame.display.update()

def main_menu():
    MENU_X = 622
    MENU_Y = 300
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(45).render("Racing Evolutionary Agent", True, "white")
        
        MENU_RECT = MENU_TEXT.get_rect(center=(MENU_X, MENU_Y))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(MENU_X, MENU_Y+200),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(MENU_X, MENU_Y+400),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.event.clear()    
                    play_training()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()