import pygame
import sys
import importlib
from block import Block, MovingBlock  # MovingBlock 추가
from obstacle import Spike
from portal import Portal
import map
from character import Character

pygame.init()

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FLOOR_COLOR = (144, 228, 144)

# 캐릭터 속성 설정
initial_character_x, initial_character_y = 50, 500
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

        self.character = Character(initial_character_x, initial_character_y, speed=character_speed, jump_speed=jump_speed)

        self.blocks = []
        self.spikes = []
        self.portals = []

        self.load_map(map.Map4)

        self.clock = pygame.time.Clock()

    def load_map(self, game_map):
        self.blocks = [block if isinstance(block, MovingBlock) else Block(block.x, block.y) for block in game_map.blocks]
        self.spikes = getattr(game_map, 'spikes', [])
        portal_width, portal_height = 40, 40
        self.portals = [Portal(745, 50, portal_width, portal_height, 'stage5')]

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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.character.is_on_ground = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.character.move_left()
            if keys[pygame.K_RIGHT]:
                self.character.move_right()

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
                stage_module = importlib.import_module(self.portals[portal_collided].target_stage)
                stage_module.run_stage()
                running = False

            # 가시 충돌 검사 및 처리
            spike_collided = self.character.rect.collidelist([spike.rect for spike in self.spikes])
            if spike_collided != -1:
                print("Character hit a spike! Respawning...")
                self.character.reset(initial_character_x, initial_character_y)

            # 바닥과 충돌하면 게임 리셋
            if self.character.y >= floor_y - self.character.height:
                self.character.reset(initial_character_x, initial_character_y)

            # 발판 그리기
            for block in self.blocks:
                block.move()
                pygame.draw.rect(self.screen, block.color, (block.x, block.y, block.width, block.height))

            # 포탈 그리기
            for portal in self.portals:
                pygame.draw.rect(self.screen, (255, 0, 255), portal.rect)

            # 캐릭터 생성
            pygame.draw.rect(self.screen, RED, self.character.rect)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
