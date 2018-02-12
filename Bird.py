"""
    Bird.py
    Author: David Gurevich
    Date Last Modified: January 20th, 2018
    Python Version: 3.X
"""

import pygame

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

PLAYERS_LIST = [
    [
        pygame.image.load("assets/sprites/redbird-upflap.png"),
        pygame.image.load("assets/sprites/redbird-midflap.png"),
        pygame.image.load("assets/sprites/redbird-downflap.png")
    ],
    [
        pygame.image.load("assets/sprites/bluebird-upflap.png"),
        pygame.image.load("assets/sprites/bluebird-midflap.png"),
        pygame.image.load("assets/sprites/bluebird-downflap.png")
    ],
    [
        pygame.image.load("assets/sprites/yellowbird-upflap.png"),
        pygame.image.load("assets/sprites/yellowbird-midflap.png"),
        pygame.image.load("assets/sprites/yellowbird-downflap.png")
    ]
]

FLAP_LIST = [0, 0, 0, 1, 1, 1, 2, 2, 2]
WELCOME_ANIMATION_RANGE = list(range(int((SCREEN_HEIGHT - PLAYERS_LIST[0][0].get_height()) / 2) - 20,
                                     int((SCREEN_HEIGHT - PLAYERS_LIST[0][0].get_height()) / 2))) + \
                          list(range(int((SCREEN_HEIGHT - PLAYERS_LIST[0][0].get_height()) / 2) - 1,
                                     int((SCREEN_HEIGHT - PLAYERS_LIST[0][0].get_height()) / 2) - 20, -1))


class Bird(pygame.sprite.Sprite):
    def __init__(self, col):
        pygame.sprite.Sprite.__init__(self)

        self.col = col
        self.x = int(SCREEN_WIDTH * 0.2)
        self.y = int((SCREEN_HEIGHT - PLAYERS_LIST[0][0].get_height()) / 2)
        self.angle = 0
        self.jumped = False
        self.flap = 0
        self.obj_y = self.y - 50

        self.dead_bool = False

        self.welcome_animation = True
        self.welcome_animation_index = 0

        self.image = PLAYERS_LIST[self.col][1]
        self.surface = pygame.surface.Surface((288, 512), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))

        if self.jumped:
            self.image = pygame.transform.rotate(PLAYERS_LIST[self.col][0], self.angle)
            self.surface.blit(self.image, (self.x, self.y))
        else:
            self.image = pygame.transform.rotate(PLAYERS_LIST[self.col][FLAP_LIST[self.flap]], self.angle)
            self.surface.blit(self.image, (self.x, self.y))

        self.image = self.surface
        self.mask = pygame.mask.from_surface(self.surface)
        screen.blit(self.surface, (self.surface.get_rect().x, self.surface.get_rect().y))

    def jump(self):
        self.jumped = True
        self.angle = 25

        self.obj_y = self.y - 40

        self.update()

    def update(self):
        self.flap = (self.flap + 1) % len(FLAP_LIST)

        if self.welcome_animation:
            self.y = WELCOME_ANIMATION_RANGE[self.welcome_animation_index % len(WELCOME_ANIMATION_RANGE)]
            self.welcome_animation_index += 2
        else:
            if self.dead_bool:
                self.dead()
            else:
                if not self.jumped and (not self.angle <= -90) and (not self.dead_bool):
                    self.angle -= int(2 + abs(0.15 * self.angle))

                if self.jumped and (not self.y == self.obj_y) and (not self.dead_bool):
                    self.y -= 7

                if self.jumped and self.y <= self.obj_y and (not self.dead_bool):
                    self.jumped = False

                if self.angle < 5 and not self.jumped and not self.dead_bool:
                    self.y += int(5 + 0.15 * abs(self.angle))

        self.rect = self.surface.get_rect()

    def dead(self):
        self.flap = 5
        if self.angle > -90:
            self.angle -= int(5 + abs(0.1 * self.angle))
        if self.y <= 370:
            self.y += int(8 + 0.15 * abs(self.angle))
