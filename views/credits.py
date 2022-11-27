from data.storage.data import *
from shared.fonts import *


def draw_credits(window, pygame):
    credits = get_credits()
    clock = pygame.time.Clock()
    quit = False
    while not quit:
        TITLE_TEXT = get_font(pygame, 40).render("CREDITOS", True, "#b68f40")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(300, 60))
        window.blit(TITLE_TEXT, TITLE_RECT)

        f = get_font(pygame, 12)

        y = 160

        for creator in credits['creators']:
            window.blit(
                f.render('--------------------------', True, (255, 255, 255)), (30, y))
            y += 30
            window.blit(
                f.render('Nombre: ' + creator['name'], True, (255, 255, 255)), (30, y))
            y += 20
            window.blit(
                f.render('Correo: ' + creator['email'], True, (255, 255, 255)), (30, y))
            y += 20
            window.blit(
                f.render('Programa: ' + creator['program'], True, (255, 255, 255)), (30, y))
            y += 20

        y += 40
        window.blit(f.render(
            credits['university'], True, (255, 255, 255)), (30, y))
        y += 20
        window.blit(
            f.render('Programa: ' + credits['program'], True, (255, 255, 255)), (30, y))
        y += 20
        window.blit(
            f.render('Semestre: ' + credits['semester'], True, (255, 255, 255)), (30, y))

        quit = pygame.event.get(pygame.QUIT)
        pygame.display.flip()
        clock.tick(60)
