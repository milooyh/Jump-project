import os
import pygame
import sys
import importlib
from block import Block, MovingBlock
from obstacle import Spike
from portal import Portal
from character import Character
import map

pygame.init()

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# 색깔 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
FLOOR_COLOR = (144, 228, 144)

# 캐릭터 속성 설정
character_speed = 6
jump_speed = 16
gravity = 1

# 바닥 속성 설정
floor_height = 22
floor_y = SCREEN_HEIGHT - floor_height

# 발판 속성 설정
platform_color = BLUE

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("점프 점프")

        self.blocks = []
        self.spikes = []
        self.portals = []

        self.map_index = 0
        self.load_map(map.maps[self.map_index])

        self.character = Character(self.initial_character_x, self.initial_character_y, speed=character_speed, jump_speed=jump_speed)

        self.clock = pygame.time.Clock()

    def load_map(self, game_map):
        self.blocks = [block if isinstance(block, MovingBlock) else Block(block.x, block.y) for block in game_map.blocks]
        self.spikes = getattr(game_map, 'spikes', [])
        self.portals = game_map.portals

        self.initial_character_x = game_map.initial_character_x
        self.initial_character_y = game_map.initial_character_y

    def next_stage(self):
        self.map_index += 1
        if self.map_index < len(map.maps):
            self.load_map(map.maps[self.map_index])
            self.character.reset(self.initial_character_x, self.initial_character_y)
        else:
            print("All stages completed!")
            pygame.quit()
            sys.exit()

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.character.jump()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.character.move_left()
            elif keys[pygame.K_RIGHT]:
                self.character.move_right()
            else:
                self.character.image_state = "idle"

            self.character.apply_gravity(gravity)
            self.character.apply_movement()
            self.character.apply_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)

            # 충돌 검사 및 처리
            block_collided = self.character.rect.collidelist([pygame.Rect(block.x, block.y, block.width, block.height) for block in self.blocks])
            if block_collided != -1:
                if self.character.vertical_momentum > 0:
                    self.character.y = self.blocks[block_collided].y - self.character.height
                    self.character.vertical_momentum = 0
                    self.character.is_on_ground = True
            elif self.character.y >= floor_y - self.character.height:
                self.character.y = floor_y - self.character.height
                self.character.vertical_momentum = 0
                self.character.is_on_ground = True
            else:
                self.character.is_on_ground = False

            # 포탈 충돌 검사 및 처리
            portal_collided = self.character.rect.collidelist([portal.rect for portal in self.portals])
            if portal_collided != -1:
                self.next_stage()
                continue

            # 가시 충돌 검사 및 처리
            spike_collided = self.character.rect.collidelist([spike.rect for spike in self.spikes])
            if spike_collided != -1:
                print("Character hit a spike! Respawning...")
                self.character.reset(self.initial_character_x, self.initial_character_y)

            # 바닥과 충돌하면 게임 리셋
            if self.character.y >= floor_y - self.character.height:
                self.character.reset(self.initial_character_x, self.initial_character_y)

            # 발판 그리기
            for block in self.blocks:
                block.move()
                pygame.draw.rect(self.screen, block.color, (block.x, block.y, block.width, block.height))

            # 포탈 그리기
            for portal in self.portals:
                pygame.draw.rect(self.screen, (255, 0, 255), portal.rect)

            # 가시 그리기
            for spike in self.spikes:
                pygame.draw.rect(self.screen, (0, 0, 0), spike.rect)  # 가시 색상은 검정색으로 설정

            # 캐릭터 생성
            self.character.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
