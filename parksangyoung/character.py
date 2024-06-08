import pygame
import os

class Character:
    def __init__(self, x, y, speed, jump_speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.jump_speed = jump_speed
        self.vertical_momentum = 0
        self.is_on_ground = True
        self.direction = "right"
        self.image_state = "idle"

        # 이미지 로드
        self.images = {
            "idle": self.load_image("idle.png"),
            "walk_left": self.load_image("walk_left.png"),
            "walk_right": self.load_image("walk_right.png"),
            "jump_left": self.load_image("jump_left.png"),
            "jump_right": self.load_image("jump_right.png"),
        }

        self.image = self.images["idle"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def load_image(self, filename):
        path = os.path.join(os.path.dirname(__file__), "images", filename)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"No file '{path}' found")
        return pygame.image.load(path)

    def move_left(self): #왼쪽으로 이동
        self.x -= self.speed
        self.rect.x = self.x
        self.direction = "left"
        self.image_state = "walk_left"

    def move_right(self):
        self.x += self.speed
        self.rect.x = self.x
        self.direction = "right"
        self.image_state = "walk_right"

    def jump(self):
        if self.is_on_ground:
            self.vertical_momentum = -self.jump_speed
            self.is_on_ground = False
            self.image_state = f"jump_{self.direction}"

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
        self.direction = "right"
        self.image_state = "idle"

    def update_image(self):
        if not self.is_on_ground:
            self.image_state = f"jump_{self.direction}"
        elif self.image_state.startswith("jump"):
            self.image_state = f"walk_{self.direction}" if self.image_state.startswith("jump") else "idle"
        self.image = self.images[self.image_state]

    def draw(self, screen):
        self.update_image()
        screen.blit(self.image, (self.x, self.y))