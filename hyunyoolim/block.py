import pygame
from setting import *

# block 클래스 정의
class Block:
    def __init__(self, x, y):
        # 블록 초기 위치 설정
        self.x = x
        self.y = y

    # 화면에 블록 그리기
    def draw(self, screen):
        pygame.draw.rect(screen, platform_color, pygame.Rect(self.x, self.y, platform_width, platform_height))
        
    @staticmethod
    def check_collision(character_x, character_y, character_width, character_height, blocks):  
        for block in blocks:
            if pygame.Rect(character_x, character_y, character_width, character_height).colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
                return block
        return None