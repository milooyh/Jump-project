import pygame # 파이게임 라이브러리 임포트
import os # 운영체제와 상호작용하기 위해 os 모듈 임포트
from setting import * # 설정 파일에서 모든 설정 가져오기

# 아이템 클래스 정의
class Item:
    def __init__(self, x, y, image_path):
        self.x = x # x좌표 설정
        self.y = y # y좌표 설정
        self.width = 50 # 아이템 너비 설정
        self.height = 50
        base_path = os.path.dirname(os.path.realpath(__file__))
        image_full_path = os.path.join(base_path, image_path)
        self.image = pygame.image.load(image_full_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class HeartItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'heart.png')

class SpeedItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'slow.png')

class InvincibilityItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'star.png')
