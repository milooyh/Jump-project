import pygame

class Spike:
    def __init__(self, x, y):
        width, height = 20, 20
        self.rect = pygame.Rect(x, y, width, height)

spikes = [
    Spike(100, 250),
    Spike(100, 280),
    Spike(150, 250),
    Spike(150, 280),
    Spike(200, 250),
    Spike(200, 280),
    Spike(300, 250),
    Spike(300, 280),
    Spike(350, 250),
    Spike(350, 280),
    Spike(400, 250),
    Spike(400, 280),
    Spike(500, 250),
    Spike(500, 280),
    Spike(550, 250),
    Spike(550, 280),
    Spike(600, 250),
    Spike(600, 280),
    ]
