import pygame
import os
from setting import *

class Item:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        base_path = os.path.dirname(os.path.realpath(__file__))
        image_full_path = os.path.join(base_path, image_path)
        self.image = pygame.image.load(image_full_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class HeartItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'heart.png')

class SpeedItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'slow.png')

class InvincibilityItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'star.png')
