"""
    Pipe.py
    Author: David Gurevich
    Date Last Modified: January 20th, 2018
    Python Version: 3.X
"""

import random

import pygame

PIPE_GAP = 100  # px
MIN_Y = 512 - 112  # px

PIPE_HEIGHT = 320  # px
PIPE_WIDTH = 52  # px

PLAYING_FIELD = 400

PIPE_IMAGES = [
    [
        pygame.image.load("assets/sprites/pipe-green.png"),
        pygame.transform.rotate(pygame.image.load("assets/sprites/pipe-green.png"), 180)
    ],
    [
        pygame.image.load("assets/sprites/pipe-red.png"),
        pygame.transform.rotate(pygame.image.load("assets/sprites/pipe-red.png"), 180)
    ]
]

PIPE_LOWER = random.randrange(PIPE_GAP + 30, MIN_Y - 30)
PIPE_UPPER = PIPE_LOWER - PIPE_GAP - PIPE_HEIGHT


class LowerPipe(pygame.sprite.Sprite):
    def __init__(self, col):
        pygame.sprite.Sprite.__init__(self)

        self.col = col

        self.x = 298
        self.y = PIPE_LOWER

        self.x_vel = -3

        self.image = PIPE_IMAGES[self.col][0]
        self.surface = pygame.surface.Surface((288, 512), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))
        self.image = PIPE_IMAGES[self.col][0]
        self.surface.blit(self.image, (self.x, self.y))

        self.image = self.surface
        self.mask = pygame.mask.from_surface(self.surface)
        screen.blit(self.surface, (self.surface.get_rect().x, self.surface.get_rect().y))

    def update(self):
        self.x += self.x_vel


class UpperPipe(pygame.sprite.Sprite):
    def __init__(self, col):
        pygame.sprite.Sprite.__init__(self)

        self.col = col

        self.x = 298
        self.y = PIPE_UPPER

        self.x_vel = -3

        self.image = PIPE_IMAGES[self.col][1]
        self.surface = pygame.surface.Surface((288, 512), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))
        self.image = PIPE_IMAGES[self.col][1]
        self.surface.blit(self.image, (self.x, self.y))

        self.image = self.surface
        self.mask = pygame.mask.from_surface(self.surface)
        screen.blit(self.surface, (self.surface.get_rect().x, self.surface.get_rect().y))

    def update(self):
        self.x += self.x_vel
