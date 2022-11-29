import neat
import pygame
import os
from graphic.window import draw_window

from shared.const import *
from shared.fonts import *
from button import Button
from views.credits import draw_credits
from views.gameOver import draw_game_over
from views.manual import manual
from views.scores import draw_Scores

from data.models.player import Player
from graphic.window import draw_window
from shared.const import FLOOR, WIN_WIDTH
from data.models.rock import *
from data.models.base import *
from views.menu_ia import *


pygame.init()
pygame.font.init()  # init font

pygame.mixer.music.load('imgs/music.mp3')
pygame.mixer.music.play(1)
pygame.mixer.music.set_volume(0.4)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

BG = pygame.image.load("imgs/Background.png")

pipe_img = pygame.transform.scale2x(pygame.image.load(
    os.path.join("imgs", "rock.png")).convert_alpha())

bg_img = pygame.transform.scale(pygame.image.load(
    os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900))
player_images = [pygame.transform.scale2x(pygame.image.load(
    os.path.join("imgs", "player" + str(x) + ".png"))) for x in range(1, 4)]
base_img = pygame.transform.scale2x(pygame.image.load(
    os.path.join("imgs", "base.png")).convert_alpha())
background_menu = pygame.transform.scale(pygame.image.load(
    os.path.join("imgs", "Background.png")).convert_alpha(), (600, 900))


def draw_menu(config_file,):

    WIN.blit(background_menu, (0, 0))

    gen = 0

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(pygame, 40).render(
            "MENU PRINCIPAL", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 60))

        PLAY_BUTTON_IA = Button(image=pygame.image.load("imgs/Play Rect.png"), pos=(300, 250),
                                text_input="Que juegue la IA", font=get_font(pygame, 20), base_color="#d7fcd4", hovering_color="White")
        PLAY_BUTTON = Button(image=pygame.image.load("imgs/Play Rect.png"), pos=(300, 400),
                             text_input="Arriesgarme", font=get_font(pygame, 20), base_color="#d7fcd4", hovering_color="White")
        SCORES_BUTTON = Button(image=pygame.image.load("imgs/Play Rect.png"), pos=(300, 550),
                               text_input="Puntuaciones", font=get_font(pygame, 20), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("imgs/Play Rect.png"), pos=(300, 700),
                             text_input="Créditos", font=get_font(pygame, 20), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON_IA, PLAY_BUTTON, SCORES_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    score = manual(WIN, pygame, base_img,
                                   pipe_img, player_images, bg_img)
                    draw_game_over(score, WIN, pygame, background_menu)
                    WIN.blit(background_menu, (0, 0))
                if PLAY_BUTTON_IA.checkForInput(MENU_MOUSE_POS):
                    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                                config_file)
                    p = neat.Population(config)
                    p.add_reporter(neat.StdOutReporter(True))
                    stats = neat.StatisticsReporter()
                    p.add_reporter(stats)
                    winner = p.run(eval_genomes, 50)
                    WIN.blit(background_menu, (0, 0))
                if SCORES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    draw_Scores(WIN, pygame, WIN_WIDTH, WIN_HEIGHT)
                    WIN.blit(background_menu, (0, 0))
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    WIN.blit(background_menu, (0, 0))
                    draw_credits(WIN, pygame)
                    WIN.blit(background_menu, (0, 0))

        pygame.display.update()


def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    players and sets their fitness based on the distance they
    reach in the game.
    """
    win = WIN
    gen = 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # player object that uses that network to play
    nets = []
    players = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(230, 350, player_images, pygame))
        ge.append(genome)

    base = Base(FLOOR, base_img)
    pipes = [Rock(700,  pygame, pipe_img)]
    score = 0

    clock = pygame.time.Clock()

    run = True

    while run and len(players) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(players) > 0:
            # determine whether to use the first or second
            if len(pipes) > 1 and players[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                # rock on the screen for neural network input
                pipe_ind = 1

        # give each player a fitness of 0.1 for each frame it stays alive
        for x, player in enumerate(players):
            ge[x].fitness += 0.1
            player.move()

            # send player location, top rock location and bottom rock location and determine from network whether to jump or not
            output = nets[players.index(player)].activate((player.y, abs(
                player.y - pipes[pipe_ind].height), abs(player.y - pipes[pipe_ind].bottom)))

            # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            if output[0] > 0.5:
                player.jump()

        base.move()

        rem = []
        add_pipe = False
        for rock in pipes:
            rock.move()
            # check for collision
            for player in players:
                if rock.collide(player):
                    ge[players.index(player)].fitness -= 1
                    nets.pop(players.index(player))
                    ge.pop(players.index(player))
                    players.pop(players.index(player))

            if rock.x + rock.PIPE_TOP.get_width() < 0:
                rem.append(rock)

            if not rock.passed and rock.x < player.x:
                rock.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for genome in ge:
                genome.fitness += 5
            pipes.append(Rock(WIN_WIDTH, pygame, pipe_img))

        for r in rem:
            pipes.remove(r)

        for player in players:
            if player.y + player.img.get_height() - 10 >= FLOOR or player.y < -50:
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))

        draw_window(win, players, pipes, base, score, gen,
                    pipe_ind, 'Agentes: '+str(len(players)), bg_img, pygame)
