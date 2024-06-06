import pygame

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1

class ChasingEnemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, player_x, player_y):
        if player_x > self.x:
            self.x += self.speed
        elif player_x < self.x:
            self.x -= self.speed

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), [(self.x + 35//2, self.y),
                                                (self.x + 35, self.y + 35//2),
                                                (self.x + 35//2, self.y + 35),
                                                (self.x, self.y + 35//2)])

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Portal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.ellipse(screen, (128, 0, 128), (self.x, self.y, 30, 80))

def init_stage(blocks_positions, enemy_positions, powerup_positions):
    blocks = [Block(x, y) for x, y in blocks_positions]
    enemies = [Enemy(x, y) for x, y in enemy_positions]
    powerups = [PowerUp(x, y) for x, y in powerup_positions]
    chasing_enemy = ChasingEnemy(650, 150, 2)
    return blocks, enemies, powerups, chasing_enemy

stages = {
    1: ([(200, 350), (500, 350),], # 파란색 발판
        
        [(750, 315)], # 초록색 적
        
        [(240, 315),]), # 노란색 코인
########################################################################
    2: ([(170, 350), (80, 200), (50, 275), (375, 300), (420, 210), (520, 130), (730, 300), (520, 350)],
        
        [(5, 315), (120, 165), (560, 95)],
        
        [(120, 165), (560, 95)]),
########################################################################
    3: ([(100, 450),
         (250, 350),
         (400, 250),
         (600, 150),
         (550, 300)],
        
        [(100, 400),
         (250, 300),
         (400, 200),
         (650, 100),
         (600, 250)],
        
        [(100 + (100 // 2 - 10), 450 - 20),
         (250 + (100 // 2 - 10), 350 - 20),
         (400 + (100 // 2 - 10), 250 - 20)])
}
