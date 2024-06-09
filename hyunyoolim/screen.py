# screen.py

import pygame
import sys
from setting import *
from obstacle import Obstacle
from block import Block
from portal import Portal   

# 화면 관련 클래스 정의
class Screen:
    def __init__(self):
        pass

    # 시작 화면 표시 함수
    @staticmethod
    def show_start_screen(screen):
        screen.fill(WHITE) # 화면 흰색으로 채움
        font = pygame.font.Font(None, 64) # 폰트 설정
        text = font.render("Press SPACE to Start", True, BLACK) # 텍스트 렌더링
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # 텍스트 위치 설정
        screen.blit(text, text_rect) # 화면에 텍스트 그리기
        pygame.display.update() # 화면 업데이트
        Screen.wait_for_space() # 스페이스바 입력 대기
        print('show_start_screen 햠수 불려짐')

    # 스페이스바 입력 대기 함수
    @staticmethod
    def wait_for_space():
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    @staticmethod
    def show_clear_screen(screen):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 64)
        text = font.render("Game Clear!", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)

    @staticmethod
    def show_game_over_screen(screen, game_manager):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 64)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

        try_again_button = pygame.Rect(250, 400, 300, 50)
        pygame.draw.rect(screen, GREEN, try_again_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Try Again", True, BLACK)
        text_rect = text.get_rect(center=try_again_button.center)
        screen.blit(text, text_rect)

        exit_button = pygame.Rect(250, 475, 300, 50)
        pygame.draw.rect(screen, RED, exit_button)
        text = font.render("Exit", True, WHITE)
        text_rect = text.get_rect(center=exit_button.center)
        screen.blit(text, text_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if try_again_button.collidepoint(event.pos):
                        print("한 번 더 !!")
                        game_manager.reset_game()
                        return  # 메인 루프로 돌아가기 위해 반환
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    @staticmethod
    def draw_game_elements(screen, character_rect):
        pygame.draw.rect(screen, RED, character_rect)
        for block in Block:
            pygame.draw.rect(screen, platform_color, pygame.Rect(block.x, block.y, platform_width, platform_height))
        for obstacle in Obstacle:
            pygame.draw.rect(screen, obstacle_color, pygame.Rect(obstacle.x, obstacle.y, obstacle_width, obstacle_height))
        if Portal:
            pygame.draw.rect(screen, PORTAL_COLOR, Portal.rect)
