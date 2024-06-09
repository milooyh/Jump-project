import pygame # 파이게임 라이브러리 임포트
import sys # 시스템과 상호작용하기 위해 임포트
from setting import * # 설정 파일에서 모든 설정 가져오기
from game_manager import GameManager # 게임 관리자 모듈 임포트
from screen import Screen # 화면 관련 모듈 임포트

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump Game")

    game_manager = GameManager()
    Screen.show_start_screen(screen)
    game_manager.run_game()

if __name__ == "__main__":
    main() 
