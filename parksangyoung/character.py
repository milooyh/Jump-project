import pygame

class Character:
    def __init__(self, x, y, width=20, height=20, speed=6, jump_speed=16):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.jump_speed = jump_speed
        self.vertical_momentum = 0
        self.is_on_ground = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def jump(self):
        if self.is_on_ground:
            self.vertical_momentum = -self.jump_speed
            self.is_on_ground = False

    def apply_gravity(self, gravity):
        self.vertical_momentum += gravity
        self.y += self.vertical_momentum

    def apply_movement(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def apply_bounds(self, screen_width, screen_height):
        self.x = max(0, min(screen_width - self.width, self.x))
        self.y = min(screen_height - self.height, self.y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.vertical_momentum = 0
        self.is_on_ground = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
