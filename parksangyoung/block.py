class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self):
        pass

# 움직이는 블록 클래스 정의 (Block 클래스 상속)
class MovingBlock(Block):
    def __init__(self, x, y, move_range=100, speed=2):
        super().__init__(x, y)
        self.move_range = move_range
        self.speed = speed
        self.initial_x = x
        self.direction = 1

    def move(self):
        self.x += self.speed * self.direction
        if self.x > self.initial_x + self.move_range or self.x < self.initial_x - self.move_range:
            self.direction *= -1