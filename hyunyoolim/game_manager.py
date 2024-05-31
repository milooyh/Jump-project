import pygame
import sys
from setting import *
from character import Character
from screen import Screen
from hyunyoolim.block import Block
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

        Screen.show_start_screen(self.screen)

        self.floor_y = floor_y

        self.blocks = [Block(x, y) for x, y in blocks_positions]
        self.obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]

        highest_block_x = max([block.x for block in self.blocks])
        highest_block_y = max([block.y for block in self.blocks])

        self.portal = Portal(highest_block_x, highest_block_y - 100)

        self.character = Character(self.blocks, self.obstacles, self.portal)

        # 아이템들의 초기 위치 설정
        self.heart_item = HeartItem(100, 550)  # 고정 위치 (x, y) 값으로 변경
        self.speed_item = SpeedItem(300, 450)  # 고정 위치 (x, y) 값으로 변경
        self.invincibility_item = InvincibilityItem(400,450)  # 고정 위치 (x, y) 값으로 변경

        # 아이템 효과 지속 시간을 기록할 변수들 추가
        self.speed_item_effect_start_time = None
        self.invincibility_item_effect_start_time = None
        
        self.game_over = False
        self.game_clear = False

    def reset_game(self):
        self.character.set_initial_position()
        self.character.life = 3
        self.character.game_over = False
        self.character.current_color_index = 0
        self.obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]

        # 아이템들의 초기 위치 재설정
        self.heart_item.rect.x = 100
        self.heart_item.rect.y = 550
        self.speed_item.rect.x = 300
        self.speed_item.rect.y = 450
        self.invincibility_item.rect.x = 400
        self.invincibility_item.rect.y = 450
        
    def run_game(self):
        running = True
        font = pygame.font.Font(None, 36)

        while running:
            self.screen.fill(WHITE)
            character_rect = pygame.Rect(self.character.x, self.character.y, self.character.width, self.character.height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.character.space_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.character.space_pressed = False

            if not self.character.game_over and not self.character.game_clear:
                self.character.update_game_state()
                self.character.draw_game_elements(self.screen, self.blocks, self.obstacles, self.portal)
                self.character.check_item_collision(self.heart_item, self.speed_item, self.invincibility_item)

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

                # 포털과 캐릭터의 충돌 감지
                if character_rect.colliderect(self.portal.rect):
                    self.character.game_clear = True
                
                if self.character.game_clear:
                    Screen.show_clear_screen(self.screen)

            elif self.character.game_over:
                Screen.show_game_over_screen(self.screen, self)
                
            # 아이템 먹기
            heart_item_eaten = self.character.check_item_collision(self.heart_item, self.speed_item, self.invincibility_item)
            speed_item_eaten = self.character.check_item_collision(self.heart_item, self.speed_item, self.invincibility_item)
            invincibility_item_eaten = self.character.check_item_collision(self.heart_item, self.speed_item, self.invincibility_item)
                
            if heart_item_eaten:
                self.heart_item.rect.x = -1000  # 아이템 위치를 화면 밖으로 이동시켜 표시하지 않음
                self.heart_item.rect.y = -1000
                self.heart_item_eaten = True  # 아이템을 먹은 상태로 표시
                
            if speed_item_eaten:
                self.speed_item.rect.x = -1000
                self.speed_item.rect.y = -1000
                self.speed_item_eaten = True
                self.speed_item_effect_start_time = pygame.time.get_ticks()  # 아이템 효과 시작 시간 기록
                
            if invincibility_item_eaten:
                self.invincibility_item.rect.x = -1000
                self.invincibility_item.rect.y = -1000
                self.invincibility_item_eaten = True
                self.invincibility_item_effect_start_time = pygame.time.get_ticks()  # 아이템 효과 시작 시간 기록

            # 아이템 효과 지속 시간 체크 및 효과 제거
            current_time = pygame.time.get_ticks()
            if self.speed_item_effect_start_time is not None and current_time - self.speed_item_effect_start_time > 5000:
                self.speed_item_effect_start_time = None
                for obstacle in self.obstacles:
                    obstacle.speed *= 2  # 속도 다시 두배로
            
            if self.invincibility_item_effect_start_time is not None and current_time - self.invincibility_item_effect_start_time > 5000:
                self.invincibility_item_effect_start_time = None
                self.invincible = False
    
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
