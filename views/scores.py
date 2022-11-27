from data.storage.data import *
from shared.fonts import *


def draw_Scores(window, pygame, WIN_WIDTH, WIN_HEIGHT):
    scores = get_records()
    intermediate = pygame.surface.Surface((WIN_WIDTH, WIN_HEIGHT))
    i_a = intermediate.get_rect()
    MENU_TEXT = get_font(pygame, 40).render("Puntuaciones", True, "#b68f40")

    intermediate.blit(MENU_TEXT, (10, 10))

    y = 80

    f = get_font(pygame, 20)
    index = 1
    for score in scores:
        intermediate.blit(f.render(str(index) + '. ' + score['name'] + ' --> ' +
                          str(score['score']) + ' pts', True, (255, 255, 255)), (30, y))
        y += 30
        index += 1

    clock = pygame.time.Clock()

    quit = False

    scroll_y = 0

    while not quit:
        quit = pygame.event.get(pygame.QUIT)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    scroll_y = min(scroll_y + 15, 0)
                if e.button == 5:
                    scroll_y = max(scroll_y - 15, -300)

        window.blit(intermediate, (0, scroll_y))
        pygame.display.flip()
        clock.tick(60)
