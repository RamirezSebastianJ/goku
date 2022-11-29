
from shared.const import WIN_WIDTH


def draw_window(win, players, rocks, base, score, gen, rock_ind, message, bg_img, pygame):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param player: a Player object
    :param rocks: List of rocks
    :param score: score of the game (int)
    :param gen: current generation
    :param rock_ind: index of closest rock
    :return: None
    """
    if gen == 0:
        gen = 1
    win.blit(bg_img, (0, 0))

    for rock in rocks:
        rock.draw(win)

    base.draw(win)

    STAT_FONT = pygame.font.SysFont("comicsans", 30)
    DRAW_LINES = False
    for player in players:
        # draw lines from player to rock
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255, 0, 0), (player.x+player.img.get_width()/2, player.y + player.img.get_height(
                )/2), (rocks[rock_ind].x + rocks[rock_ind].ROCK_TOP.get_width()/2, rocks[rock_ind].height), 5)
                pygame.draw.line(win, (255, 0, 0), (player.x+player.img.get_width()/2, player.y + player.img.get_height(
                )/2), (rocks[rock_ind].x + rocks[rock_ind].ROCK_BOTTOM.get_width()/2, rocks[rock_ind].bottom), 5)
            except:
                pass
        # draw player
        player.draw(win)

    # score
    score_label = STAT_FONT.render(
        "Puntaje: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # alive
    score_label = STAT_FONT.render(
        message, 1, (255, 255, 255))
    win.blit(score_label, (10, 50))

    pygame.display.update()
