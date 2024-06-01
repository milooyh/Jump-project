import pygame
from setting import *
from screen import Screen
from block import Block
from obstacle import Obstacle
from portal import Portal

class Character:
    def __init__(self, blocks, obstacles, portal):
        self.width = 20
        self.height = 20
        self.speed = 6
        self.jump_speed = 20
        self.gravity = 1.4
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - self.height * 2
        self.vertical_momentum = 0
        self.is_on_ground = True
        self.space_pressed = False
        self.life = 3
        self.game_over = False
        self.game_clear = False
        self.blocks = blocks
        self.obstacles = obstacles
        self.portal = portal
        self.colors = [RED, ORANGE, YELLOW]
        self.current_color_index = 0
        self.show_life = False
        self.life_counter = 0

    def set_initial_position(self):
        """장애물에 닿으면 초기 위치로 돌아옴"""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - self.height * 2

    def update_game_state(self):
        """게임 상태를 업데이트"""
        current_time = pygame.time.get_ticks()
        print("스페이스 바 눌림 여부:", self.space_pressed)

        if self.space_pressed and self.is_on_ground:
            print('점프 중')
            self.vertical_momentum = -self.jump_speed
            self.is_on_ground = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            print('왼쪽키 눌림')
            self.x = max(LEFT_EDGE, self.x - self.speed)
        if keys[pygame.K_RIGHT]:
            print('오른쪽키 눌림')
            self.x = min(RIGHT_EDGE, self.x + self.speed)

        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.vertical_momentum += self.gravity
        self.y += self.vertical_momentum
        self.y = min(self.y, floor_y - self.height)

        if self.y >= floor_y - self.height:
            self.y = floor_y - self.height
            self.vertical_momentum = 0
            self.is_on_ground = True

        block_collided = Block.check_collision(self.x, self.y, self.width, self.height, self.blocks)
        obstacle_collided = Obstacle.check_collision(self.x, self.y, self.width, self.height, self.obstacles)
        
        if block_collided and self.vertical_momentum > 0:
            self.y = block_collided.y - self.height
            self.vertical_momentum = 0
            self.is_on_ground = True
                
        if obstacle_collided:
            print("장애물과 충돌 여부:", obstacle_collided)
            self.life -= 1
            print('라이프 개수:', self.life)
            self.show_life = True
            self.life_counter = current_time
            if self.life == 0:
                self.game_over = True
            else:
                self.current_color_index = min(len(self.colors) - 1, self.current_color_index + 1)
                self.set_initial_position()
                self.vertical_momentum = 0
                self.is_on_ground = True
        
        if pygame.Rect(self.x, self.y, self.width, self.height).colliderect(self.portal.rect):
            self.game_clear = True

    def draw_game_elements(self, screen):
        """게임 요소를 화면에 그림"""
        pygame.draw.rect(screen, self.colors[self.current_color_index], pygame.Rect(self.x, self.y, self.width, self.height))
        for block in self.blocks:
            block.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        self.portal.draw(screen)
        
        if self.show_life:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Life: {self.life}", True, BLACK)
            screen.blit(text, (10, 10))
            current_time = pygame.time.get_ticks()
            if current_time - self.life_counter >= 1000:  # 1초 동안만 표시
                self.show_life = False
