import pygame

class Character:
    def __init__(self, x, y, speed, jump_speed, image_path):
        self.x = x
        self.y = y
        self.speed = speed
        self.jump_speed = jump_speed
        self.vertical_momentum = 0
        self.is_on_ground = True
        self.image = pygame.image.load(image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def move_left(self):
        self.x -= self.speed
        self.rect.x = self.x

    def move_right(self):
        self.x += self.speed
        self.rect.x = self.x

    def jump(self):
        if self.is_on_ground:
            self.vertical_momentum = -self.jump_speed
            self.is_on_ground = False

    def apply_gravity(self, gravity):
        self.vertical_momentum += gravity

    def apply_movement(self):
        self.y += self.vertical_momentum
        self.rect.y = self.y

    def apply_bounds(self, screen_width, screen_height):
        self.x = max(0, min(screen_width - self.width, self.x))
        self.y = min(self.y, screen_height - self.height)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.vertical_momentum = 0
        self.is_on_ground = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
