import pygame

class Portal:
    def __init__(self, x, y):
        self.x = x - 30
        self.y = y

    def draw(self, screen):
        pygame.draw.ellipse(screen, (128, 0, 128), (self.x, self.y, 30, 80))
