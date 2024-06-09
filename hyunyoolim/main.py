import pygame # 파이게임 라이브러리 임포트
import sys
from setting import *
from game_manager import GameManager
from screen import Screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump Game")

    game_manager = GameManager()
    Screen.show_start_screen(screen)
    game_manager.run_game()

if __name__ == "__main__":
    main() 
