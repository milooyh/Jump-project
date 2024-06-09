# obstacle.py

import pygame # 파이게임 라이브러리 임포트
from setting import * # 설정 파일에서 모든 설정 가져오기

# 장애물 클래스 정의
class Obstacle:
    def __init__(self, x, y, speed):
        self.x = x # 장애물 x좌표 설정
        self.y = y # 장애물 y좌표 설정
        self.speed = speed # 장애물 속도 설정

    # 위치 업데이트 함수
    def update_position(self):
        self.x -= self.speed
        print('update_position 함수 불림 !')

    # 화면 요소 그리는 함수
    def draw(self, screen):
        pygame.draw.rect(screen, obstacle_color, pygame.Rect(self.x, self.y, obstacle_width, obstacle_height))
        print('draw 함수 불림 ! - 장애물')
    
    @staticmethod
    def check_collision(character_x, character_y, character_width, character_height, obstacles):  
        for obstacle in obstacles:
            if pygame.Rect(character_x, character_y, character_width, character_height).colliderect(pygame.Rect(obstacle.x, obstacle.y, obstacle_width, obstacle_height)):
                return obstacle
        return None
