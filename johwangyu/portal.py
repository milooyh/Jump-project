import pygame
import os

class Portal:
    def __init__(self, x, y, target_stage):
        self.x = x - 30
        self.y = y
        self.target_stage = target_stage

    def draw(self, screen):
        pygame.draw.ellipse(screen, (128, 0, 128), (self.x, self.y, 30, 80))

    def check_collision(self, player_rect):
        portal_rect = pygame.Rect(self.x, self.y, 30, 80)
        return player_rect.colliderect(portal_rect)

    def load_target_stage(self):
        if self.target_stage == 1:
            os.system("python /path/to/johwangyu/main_game.py")
        elif self.target_stage == 2:
            os.system("python /path/to/kyokwan/main_game.py")
