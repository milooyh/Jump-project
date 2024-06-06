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

def init_stage(blocks_positions, enemy_positions, powerup_positions, portal_position):
    blocks = [Block(x, y) for x, y in blocks_positions]
    enemies = [Enemy(x, y) for x, y in enemy_positions]
    powerups = [PowerUp(x, y) for x, y in powerup_positions]
    portal = Portal(*portal_position)
    return blocks, enemies, powerups, portal

stages = {
    1: ([(180, 350), (500, 350), (130, 200), (255, 270)],  # 파란색 발판
        [(600, 315), (200, 165)],  # 초록색 적
        [(240, 315), (170, 165)],  # 노란색 코인
         (760, 365)),  # 포탈 위치 추가
####################################################################################################
    2: ([(170, 350), (80, 200), (50, 275), (375, 300), (420, 210), (550, 130), (760, 350)],
        [(5, 315), (300, 165), (590, 95)],
        [(120, 165), (590, 95)],
        (762, 270)),
####################################################################################################
    3: ([(250, 350), (400, 250), (600, 150), (550, 300)],
        [(100, 315),(250, 265), (400, 115), (600, 250)],
        [(290, 315), (590, 265), (640, 115)],
        (760, 365))
}
