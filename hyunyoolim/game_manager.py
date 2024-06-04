# game_manager.py

import pygame
import sys
from setting import *
from character import Character
from screen import Screen
from block import Block
from obstacle import Obstacle
from portal import Portal
from item import *

class GameManager:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("점프 점프")

        self.clock = pygame.time.Clock()

        # 게임 시작 페이지 표시
        Screen.show_start_screen(self.screen)

        # 초기 설정
        self.floor_y = floor_y

        self.blocks = [Block(x, y) for x, y in blocks_positions]
        self.obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]

        highest_block_x = max([block.x for block in self.blocks])
        highest_block_y = max([block.y for block in self.blocks])
        self.portal = Portal(highest_block_x, highest_block_y - 100)

        self.heart_item = HeartItem(350, 350)  # 예시 좌표로 설정
        self.speed_item = SpeedItem(600, 250)  # 예시 좌표로 설정
        self.invincibility_item = InvincibilityItem(500, 150)  # 예시 좌표로 설정
        
        self.items = [self.heart_item, self.speed_item, self.invincibility_item]
        self.character = Character(self.blocks, self.obstacles, self.portal, self.items)

        self.game_over = False
        self.game_clear = False

    def reset_game(self):
        self.character.set_initial_position()
        self.character.life = 3
        self.character.game_over = False
        self.character.current_color_index = 0
        self.obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]

    def reset_items_and_obstacles(self):
        """아이템과 장애물 위치 재설정"""
        self.heart_items = HeartItem(250,400)
        self.speed_item = SpeedItem(650,400)
    # 게임 시작 함수
    def run_game(self):
        running = True
        font = pygame.font.Font(None, 36)
        obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]


        while running:
            self.screen.fill(WHITE)
            character_rect = pygame.Rect(self.character.x, self.character.y, self.character.width, self.character.height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print('게임 강제 종료')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.character.space_pressed = True
                        print('스페이스바 눌림')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.character.space_pressed = False
                        print('스페이스바 안 눌림')

            if not self.character.game_over and not self.character.game_clear:
                self.character.update_game_state()  # 게임 상태 업데이트
                print('게임 상태 업데이트')

                self.character.draw_game_elements(self.screen, self.blocks, self.obstacles, self.portal)  # 게임 요소 그리기
                print('게임 요소 그리기')

                # 장애물 위치 업데이트
                for obstacle in self.obstacles:
                    obstacle.update_position()
                    if obstacle.x < -obstacle_width:
                        obstacle.x = SCREEN_WIDTH

                life_text = font.render(f"Life: {self.character.life}", True, BLACK)
                life_rect = life_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
                self.screen.blit(life_text, life_rect)
                
                self.heart_item.draw(self.screen)
                self.speed_item.draw(self.screen)
                self.invincibility_item.draw(self.screen)
                print('아이템 그리기')

                if self.character.game_clear:
                    Screen.show_clear_screen(self.screen)
                    print('게임 클리어')
                elif self.character.game_over:
                    Screen.show_game_over_screen(self.screen, self)
                    print('게임오버')

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
