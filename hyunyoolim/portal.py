import pygame
from setting import *

# 포털 클래스 정의
class Portal:
    def __init__(self, x, y):
        self.x = 700 # 포털 x 좌표
        self.y = 150 # 포털 y좌표
        self.width = 50 # 포털 너비
        self.height = 50 # 포털 높이
        
        # 포털의 사각 영역 설정
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 포털 이미지 로드 및 크기 조절
        self.image = pygame.image.load('hyunyoolim\portal.png').convert_alpha()  # 이미지 불러오기
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # 이미지 크기 조절
    
    # 포털 화면에 그리기
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
