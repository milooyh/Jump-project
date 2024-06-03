import pygame

class Portal:
    def __init__(self, x, y, width, height, target_stage):
        self.rect = pygame.Rect(x, y, width, height)
        self.target_stage = target_stage