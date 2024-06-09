import pygame # 파이게임 모듈 임포트
from setting import *
from screen import Screen
from block import Block
from obstacle import Obstacle
from portal import Portal
from item import *

# character 클래스 정의
class Character:
    def __init__(self, blocks, obstacles, portal, items):
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
        self.items = items
        self.colors = [RED, ORANGE, YELLOW]
        self.current_color_index = 0
        self.show_life = False
        self.life_counter = 0
        self.invincible = False
        self.invincible_timer = 0
        self.speed_boost_timer = 0
        self.invincible_remaining_time = 0
        self.speed_boost_remaining_time = 0
        self.heart_item_eaten = False
        
        self.image = pygame.image.load('hyunyoolim\character.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def set_initial_position(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - self.height * 2

    def update_game_state(self):
        current_time = pygame.time.get_ticks()
        
        if self.space_pressed and self.is_on_ground:
            self.vertical_momentum = -self.jump_speed
            self.is_on_ground = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x = max(LEFT_EDGE, self.x - self.speed)
        if keys[pygame.K_RIGHT]:
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
        if block_collided:
            if self.vertical_momentum > 0:
                self.y = block_collided.y - self.height
                self.vertical_momentum = 0
                self.is_on_ground = True

        if obstacle_collided and not self.invincible:
            self.life -= 1
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

        # 무적 효과가 끝나면 무적 해제
        if self.invincible and current_time - self.invincible_timer > 5000:
            self.invincible = False

        # 스피드 효과가 끝나면 장애물 속도 복원
        if self.speed_boost_timer and current_time - self.speed_boost_timer > 5000:
            for obstacle in self.obstacles:
                obstacle.speed *= 2
            self.speed_boost_timer = 0
            
        self.check_item_collision()

    def draw_game_elements(self, screen, blocks, obstacles, portal):
        screen.blit(self.image, (self.x, self.y))
        for block in blocks:
            block.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        portal.draw(screen)

        if self.show_life:
            font = pygame.font.Font(None, 36)
            text = font.render(f"life : {self.life}", True, BLACK)
            current_time = pygame.time.get_ticks()
            if current_time - self.life_counter >= 1000:  # 1초 동안만 표시
                self.show_life = False

        # 남은 시간 표시
        if self.invincible:
            remaining_time = 5 - (pygame.time.get_ticks() - self.invincible_timer) // 1000
            font = pygame.font.Font(None, 36)
            text = font.render(f"Invincible: {remaining_time}", True, BLACK)
            screen.blit(text, (10, 50))

        if self.speed_boost_timer:
            remaining_time = 5 - (pygame.time.get_ticks() - self.speed_boost_timer) // 1000
            font = pygame.font.Font(None, 36)
            text = font.render(f"Speed Boost: {remaining_time}", True, BLACK)
            screen.blit(text, (10, 80))

    def check_item_collision(self):
        character_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for item in self.items:
            if character_rect.colliderect(item.rect):
                self.handle_item_collision(item)

    def handle_item_collision(self, item):
        if isinstance(item, HeartItem):
            if not self.heart_item_eaten:
                self.life += 1
                self.heart_item_eaten = True
                item.x = -100  # Move off-screen
        elif isinstance(item, SpeedItem):
            for obstacle in self.obstacles:
                obstacle.speed /= 2  # Halve speed
            self.speed_boost_timer = pygame.time.get_ticks()  # Start timer
            item.x = -100  # Move off-screen
        elif isinstance(item, InvincibilityItem):
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()  # Start timer
            item.x = -100  # Move off-screen
