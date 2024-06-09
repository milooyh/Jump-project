import pygame

class Block:
    def __init__(self, x, y, width=100, height=20, color=(0, 0, 255), image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.image.load(image_path) if image_path else None

    def draw(self, screen):
        if self.image:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        pass  



class MovingBlock(Block):
    def __init__(self, x, y, width=100, height=20, color=(0, 0, 255), move_range=100, speed=2, image_path=None):
        super().__init__(x, y, width, height, color, image_path)  # 부모 클래스의 생성자에 image_path 추가
        self.move_range = move_range
        self.speed = speed
        self.initial_x = x
        self.direction = 1

    def move(self):
        self.x += self.speed * self.direction
        if self.x > self.initial_x + self.move_range or self.x < self.initial_x - self.move_range:
            self.direction *= -1
