import sys

from button import Button
from data.storage.data import saveRecord
from shared.fonts import get_font


def draw_game_over(score, window, pygame, background_menu):

    user_text = ''
    input_rect = pygame.Rect(230, 400, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')

    clock = pygame.time.Clock()

    color = color_passive

    active = False

    saved = True

    while saved:
        window.blit(background_menu, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(pygame, 40).render("GAME OVER", True, "#FF5733")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 60))
        window.blit(MENU_TEXT, MENU_RECT)

        DESCRIPTION_TEXT = get_font(pygame, 25).render(
            "Puntaje: " + str(score), True, "#FFFFFF")
        DESCRIPTION_RECT = DESCRIPTION_TEXT.get_rect(center=(300, 140))
        window.blit(DESCRIPTION_TEXT, DESCRIPTION_RECT)

        QUESTION_TEXT = get_font(pygame, 10).render(
            "Si quieres guardar tu punaje escribe tu nombre", True, "#FFFFFF")
        QUESTION_RECT = QUESTION_TEXT.get_rect(center=(300, 180))
        window.blit(QUESTION_TEXT, QUESTION_RECT)

        SAVE_BUTTON = Button(image=pygame.image.load("imgs/small_button.png"), pos=(300, 550),
                             text_input="GUARDAR", font=get_font(pygame, 12), base_color="#d7fcd4", hovering_color="White")

        NO_SAVE_BUTTON = Button(image=pygame.image.load("imgs/small_button.png"), pos=(300, 630),
                                text_input="NO GUARDAR", font=get_font(pygame, 12), base_color="#d7fcd4", hovering_color="White")

        for button in [SAVE_BUTTON, NO_SAVE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():

            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if SAVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    saveRecord(score, user_text)
                    saved = False
                    break

                if NO_SAVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    saved = False
                    break

            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode

        if active:
            color = color_active
        else:
            color = color_passive

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(window, color, input_rect)

        text_surface = get_font(pygame, 10).render(
            user_text, True, (255, 255, 255))

        # render at position stated in arguments
        window.blit(text_surface, (input_rect.x+5, input_rect.y+5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)
