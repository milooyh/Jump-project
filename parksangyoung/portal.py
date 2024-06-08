import pygame
import os

class Portal:
    def __init__(self, x, y, width, height, target_stage, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.target_stage = target_stage
        self.image = self.load_image(image_path)
        self.width = width
        self.height = height

    def load_image(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"No file '{path}' found")
        return pygame.image.load(path)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))#