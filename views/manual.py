from data.models.base import *
from data.models.player import *
from data.models.rock import *
from graphic.window import draw_window

from shared.const import FLOOR, WIN_WIDTH


def manual(window, pygame, base_img, pipe_img, bird_images, bg_img):
    base = Base(FLOOR, base_img)
    pipes = [Rock(700, pygame, pipe_img)]
    score = 0
    lives = 3
    livesCopy = 3
    win = window
    player = [Player(230, 350, bird_images, pygame)]
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

        pipe_ind = 0
        if lives > 0:
            if len(pipes) > 1 and player[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                # rock on the screen for neural network input
                pipe_ind = 1

        player[0].move()
        rem = []
        add_pipe = False
        for rock in pipes:
            rock.move()
            # check for collision
            if rock.collide(player[0]):
                lives -= 1
                break
            elif lives == livesCopy:
                if rock.x + rock.PIPE_TOP.get_width() < 0:
                    rem.append(rock)

                if not rock.passed and rock.x < player[0].x:
                    rock.passed = True
                    add_pipe = True

        if lives == livesCopy:
            if add_pipe:
                score += 1
                pipes.append(Rock(WIN_WIDTH,  pygame, pipe_img))

            for r in rem:
                pipes.remove(r)

            if player[0].y + player[0].img.get_height() - 10 >= FLOOR or player[0].y < -50:
                lives -= 1
                player = [Player(230, 350, bird_images, pygame)]

            if lives == livesCopy:

                draw_window(window, player, pipes, base, score,
                            0, pipe_ind, "Vidas: "+str(lives), bg_img, pygame)
            else:
                base = Base(FLOOR, base_img)
                pipes = [Rock(700, pygame, pipe_img)]
                scores.append(score)
                score = 0

        else:
            base = Base(FLOOR, base_img)
            pipes = [Rock(700,  pygame, pipe_img)]
            scores.append(score)
            score = 0

    return max(scores)
