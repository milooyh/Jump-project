import pygame
from setting import *





class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, platform_color, pygame.Rect(self.x, self.y, platform_width, platform_height))
        
    @staticmethod
    def check_collision(character_x, character_y, character_width, character_height, blocks):  
        for block in blocks:
            if pygame.Rect(character_x, character_y, character_width, character_height).colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
                return block
        return None