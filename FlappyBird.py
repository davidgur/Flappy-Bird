#!/usr/bin/env python
"""
    FlappyBird.py
    Author: David Gurevich
    Date Last Modified: January 20th, 2018
    Python Version: 3.X
"""
# --------IMPORTS--------
import random
import sys

import pygame
from pygame.locals import *

import Base
import Bird
import Pipe

pygame.init()

# -------- GAME INFO -----------

WIDTH = 288
HEIGHT = 512

FPS = 30
CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - David Gurevich")
pygame.display.set_icon(pygame.image.load('flappy.ico'))

BACKGROUNDS = [pygame.image.load("assets/sprites/background-day.png"),
               pygame.image.load("assets/sprites/background-night.png")]

base_img = pygame.image.load("assets/sprites/base.png")
digits = [pygame.image.load('assets/sprites/0.png'),
          pygame.image.load('assets/sprites/1.png'),
          pygame.image.load('assets/sprites/2.png'),
          pygame.image.load('assets/sprites/3.png'),
          pygame.image.load('assets/sprites/4.png'),
          pygame.image.load('assets/sprites/5.png'),
          pygame.image.load('assets/sprites/6.png'),
          pygame.image.load('assets/sprites/7.png'),
          pygame.image.load('assets/sprites/8.png'),
          pygame.image.load('assets/sprites/9.png')]

SCORE = 0

SOUNDS = {
    'die': pygame.mixer.Sound('assets/audio/die.ogg'),
    'hit': pygame.mixer.Sound('assets/audio/hit.ogg'),
    'point': pygame.mixer.Sound('assets/audio/point.ogg'),
    'wing': pygame.mixer.Sound('assets/audio/wing.ogg')
}


# --------- GENERATOR FUNCTIONS ---------


def gen_pipes():
    global pipe_col
    pipe_col = random.randint(0, 1)

    lower_new_pipe_1 = Pipe.LowerPipe(pipe_col)
    upper_new_pipe_1 = Pipe.UpperPipe(pipe_col)

    Pipe.PIPE_LOWER = random.randrange(Pipe.PIPE_GAP + 30, Pipe.MIN_Y - 30)
    Pipe.PIPE_UPPER = Pipe.PIPE_LOWER - Pipe.PIPE_GAP - Pipe.PIPE_HEIGHT

    lower_new_pipe_2 = Pipe.LowerPipe(pipe_col)
    lower_new_pipe_2.x += (WIDTH * 0.5)

    global lower_pipe_list
    lower_pipe_list = [lower_new_pipe_1, lower_new_pipe_2]

    upper_new_pipe_2 = Pipe.UpperPipe(pipe_col)
    upper_new_pipe_2.x += (WIDTH * 0.5)

    global upper_pipe_list
    upper_pipe_list = [upper_new_pipe_1, upper_new_pipe_2]


def gen_background():
    global background
    background = random.choice(BACKGROUNDS)


def gen_base():
    global base_list

    new_base_1 = Base.Base()
    new_base_1.x = 0

    new_base_2 = Base.Base()

    base_list = [new_base_1, new_base_2]


def gen_bird():
    global bird_col
    bird_col = random.randrange(0, 3)

    global bird
    bird = Bird.Bird(bird_col)


# --------- DRAWING FUNCTIONS ---------

def redraw_screen():
    SCREEN.blit(background, (0, 0))

    for pipe in lower_pipe_list:
        pipe.draw(SCREEN)

    for pipe in upper_pipe_list:
        pipe.draw(SCREEN)

    for base in base_list:
        base.draw(SCREEN)

    bird.draw(SCREEN)
    show_score(SCORE)

    pygame.display.update()


def show_score(score):
    score_digits = [int(x) for x in list(str(score))]
    total_width = 0

    for digit in score_digits:
        total_width += digits[digit].get_width()

    x_offset = (WIDTH - total_width) / 2

    for digit in score_digits:
        SCREEN.blit(digits[digit], (x_offset, HEIGHT * 0.1))
        x_offset += digits[digit].get_width()


# --------- UPDATER FUNCTIONS ---------

def update_pipe_list():
    Pipe.PIPE_LOWER = random.randrange(Pipe.PIPE_GAP + 30, Pipe.MIN_Y - 30)
    Pipe.PIPE_UPPER = Pipe.PIPE_LOWER - Pipe.PIPE_GAP - Pipe.PIPE_HEIGHT

    if 0 < lower_pipe_list[0].x < 3:
        new_pipe = Pipe.LowerPipe(pipe_col)
        lower_pipe_list.append(new_pipe)

    if lower_pipe_list[0].x < 0 - Pipe.PIPE_WIDTH:
        lower_pipe_list.pop(0)

    if 0 < upper_pipe_list[0].x < 3:
        new_pipe = Pipe.UpperPipe(pipe_col)
        upper_pipe_list.append(new_pipe)

    if upper_pipe_list[0].x < 0 - Pipe.PIPE_WIDTH:
        upper_pipe_list.pop(0)


def update_base_list():
    if -337 < base_list[0].x < -334:
        new_base = Base.Base()
        base_list.append(new_base)

    if base_list[0].x < -336:
        base_list.pop(0)


# --------- DETECTOR FUNCTIONS ---------

def detect_collision():
    if (bird.y + Bird.PLAYERS_LIST[0][1].get_height()) >= 400 - 5:
        if not bird.dead_bool:
            SOUNDS['hit'].play()
        bird.dead_bool = True
        return True
    else:
        for upper_pipe, lower_pipe in zip(upper_pipe_list, lower_pipe_list):
            if (pygame.sprite.collide_mask(bird, upper_pipe) is not None) or \
                    (pygame.sprite.collide_mask(bird, lower_pipe) is not None):
                if not bird.dead_bool:
                    SOUNDS['hit'].play()
                    SOUNDS['die'].play()
                bird.dead_bool = True
                return True
    return False


def check_for_score():
    player_mid_pos = bird.x + Bird.PLAYERS_LIST[0][1].get_width() / 2

    for pipe in upper_pipe_list:
        pipe_mid_pos = pipe.x + Pipe.PIPE_IMAGES[0][0].get_width() / 2
        if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4 and not bird.dead_bool:
            global SCORE
            SCORE += 1
            SOUNDS['point'].play()

# --------- MAIN GAME FUNCTIONS ---------


def show_welcome_animation():
    gen_background()
    gen_bird()
    gen_base()

    welcome_message = pygame.image.load('assets/sprites/message.png').convert_alpha()

    message_x = int((WIDTH - welcome_message.get_width()) / 2)
    message_y = int(HEIGHT * 0.12)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE) or event.type == MOUSEBUTTONDOWN:
                bird.welcome_animation = False
                return

        SCREEN.blit(background, (0, 0))
        SCREEN.blit(welcome_message, (message_x, message_y))
        bird.draw(SCREEN)
        bird.update()
        update_base_list()
        for base in base_list:
            base.update()
            base.draw(SCREEN)
        pygame.display.update()
        CLOCK.tick(FPS)


def main_loop():
    global SCORE
    SCORE = 0

    show_welcome_animation()
    gen_pipes()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and
                                                        (event.key == K_UP or event.key == K_SPACE))) and \
                    (not bird.y <= 0) and not bird.dead_bool:
                bird.jump()
                SOUNDS['wing'].play()

            elif bird.dead_bool and (event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE) or
                                             event.type == MOUSEBUTTONDOWN):
                main_loop()

        update_pipe_list()
        update_base_list()
        check_for_score()

        for pipe in lower_pipe_list:
            pipe.update()

        for pipe in upper_pipe_list:
            pipe.update()

        for base in base_list:
            base.update()

        bird.update()

        if detect_collision():
            for upper_pipe, lower_pipe in zip(upper_pipe_list, lower_pipe_list):
                upper_pipe.x_vel = 0
                lower_pipe.x_vel = 0

            for base in base_list:
                base.x_vel = 0

        redraw_screen()

        CLOCK.tick(FPS)


main_loop()  # GAME INITIALIZER
