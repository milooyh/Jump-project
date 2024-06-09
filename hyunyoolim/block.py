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
        # platform_color: 블록의 색상 (setting 모듈에서 가져옴)
        # platform_width: 블록의 너비 (setting 모듈에서 가져옴)
        # platform_height: 블록의 높이 (setting 모듈에서 가져옴)
        pygame.draw.rect(screen, platform_color, pygame.Rect(self.x, self.y, platform_width, platform_height))
        
    
    # 캐릭터와 블록 간의 충돌 검사
    @staticmethod
    def check_collision(character_x, character_y, character_width, character_height, blocks):  
        for block in blocks:
            if pygame.Rect(character_x, character_y, character_width, character_height).colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
                return block
        return None