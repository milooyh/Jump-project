import pygame

class Item:
    def __init__(self, x, y, width, height, item_type, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item_type = item_type
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

