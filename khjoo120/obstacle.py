import pygame


class Spike:
    def __init__(self, x, y):
        width, height = 20, 20
        self.rect = pygame.Rect(x, y, width, height)

spikes = [
    Spike(100, 250, spike_width, spike_height),
    Spike(100, 280, spike_width, spike_height),
    Spike(150, 250, spike_width, spike_height),
    Spike(150, 280, spike_width, spike_height),
    Spike(200, 250, spike_width, spike_height),
    Spike(200, 280, spike_width, spike_height),
    Spike(300, 250, spike_width, spike_height),
    Spike(300, 280, spike_width, spike_height),
    Spike(350, 250, spike_width, spike_height),
    Spike(350, 280, spike_width, spike_height),
    Spike(400, 250, spike_width, spike_height),
    Spike(400, 280, spike_width, spike_height),
    Spike(500, 250, spike_width, spike_height),
    Spike(500, 280, spike_width, spike_height),
    Spike(550, 250, spike_width, spike_height),
    Spike(550, 280, spike_width, spike_height),
    Spike(600, 250, spike_width, spike_height),
    Spike(600, 280, spike_width, spike_height),
    ]
