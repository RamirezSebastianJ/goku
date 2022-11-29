from data.models.base import *
from data.models.player import *
from data.models.rock import *
from graphic.window import draw_window

from shared.const import FLOOR, WIN_WIDTH


def manual(window, pygame, base_img, rock_img, player_images, bg_img):
    base = Base(FLOOR, base_img)
    rocks = [Rock(700, pygame, rock_img)]
    score = 0
    lives = 3
    livesCopy = 3
    win = window
    player = [Player(230, 350, player_images, pygame)]
    clock = pygame.time.Clock()
    scores = []
    while lives > 0:

        livesCopy = lives
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player[0].jump()

        rock_ind = 0
        if lives > 0:
            if len(rocks) > 1 and player[0].x > rocks[0].x + rocks[0].ROCK_TOP.get_width():
                # rock on the screen for neural network input
                rock_ind = 1

        player[0].move()
        rem = []
        add_rock = False
        for rock in rocks:
            rock.move()
            # check for collision
            if rock.collide(player[0]):
                lives -= 1
                break
            elif lives == livesCopy:
                if rock.x + rock.ROCK_TOP.get_width() < 0:
                    rem.append(rock)

                if not rock.passed and rock.x < player[0].x:
                    rock.passed = True
                    add_rock = True

        if lives == livesCopy:
            if add_rock:
                score += 1
                rocks.append(Rock(WIN_WIDTH,  pygame, rock_img))

            for r in rem:
                rocks.remove(r)

            if player[0].y + player[0].img.get_height() - 10 >= FLOOR or player[0].y < -50:
                lives -= 1
                player = [Player(230, 350, player_images, pygame)]

            if lives == livesCopy:

                draw_window(window, player, rocks, base, score,
                            0, rock_ind, "Vidas: "+str(lives), bg_img, pygame)
            else:
                base = Base(FLOOR, base_img)
                rocks = [Rock(700, pygame, rock_img)]
                scores.append(score)
                score = 0

        else:
            base = Base(FLOOR, base_img)
            rocks = [Rock(700,  pygame, rock_img)]
            scores.append(score)
            score = 0

    return max(scores)
