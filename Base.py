"""
    Base.py
    Author: David Gurevich
    Date Last Modified: January 20th, 2018
    Python Version: 3.X
"""

import pygame

BASE_HEIGHT = 112
BASE_WIDTH = 336


class Base(object):
    def __init__(self):
        self.x = 288
        self.y = 400
        self.x_vel = -3  # px

    def draw(self, screen):
        screen.blit(pygame.image.load("assets/sprites/base.png"), (self.x, self.y))

    def update(self):
        self.x += self.x_vel
