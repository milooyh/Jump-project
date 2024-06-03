import pygame


class Spike:
    def __init__(self, x, y):
        width, height = 20, 20
        self.rect = pygame.Rect(x, y, width, height)