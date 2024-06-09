import pygame
import sys
import os
import subprocess
from character import Character
from map import *

pygame.init()

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("점프 점프")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 캐릭터 속성 설정
character_speed = 6
jump_speed = 16
gravity = 1

# 바닥 속성 설정
floor_height = 22
floor_y = SCREEN_HEIGHT - floor_height

# 현재 스크립트 파일의 디렉토리를 기준으로 경로 설정
current_dir = os.path.dirname(__file__)
hyunyoolim_path = os.path.abspath(os.path.join(current_dir, "../hyunyoolim"))

# 충돌 감지
def check_collision(character, blocks):
    for block in blocks:
        if character.rect.colliderect(pygame.Rect(block.x, block.y, block.width, block.height)):
            return block
    return None

# 포탈 충돌 감지
def check_portal_collision(character, portal):
    if character.rect.colliderect(portal.rect):
        return portal
    return None

# 바닥과 충돌 시 초기 위치로
def reset_game(character, initial_x, initial_y):
    character.reset(initial_x, initial_y)

# 가시 충돌 감지
def check_spike_collision(character, spikes):
    for spike in spikes:
        if character.rect.colliderect(spike.rect):
            return spike
    return None

# 게임 클래스
class Game:
    def __init__(self):
        self.stage_index = 0
        self.stages = [Map1, Map2, Map3, Map4]
        self.load_stage(self.stage_index)

    def load_stage(self, index):
        self.stage = self.stages[index]()
        self.blocks = self.stage.blocks
        self.spikes = getattr(self.stage, 'spikes', [])
        self.portal = self.stage.portal
        self.character = Character(self.stage.initial_character_x, self.stage.initial_character_y, speed=character_speed, jump_speed=jump_speed)

    def next_stage(self):
        self.stage_index = (self.stage_index + 1) % len(self.stages)
        self.load_stage(self.stage_index)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        space_pressed = False

        while running:
            screen.fill(WHITE)
            character_rect = self.character.rect

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        space_pressed = False

            if space_pressed and self.character.is_on_ground:
                self.character.jump()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.character.move_left()
            if keys[pygame.K_RIGHT]:
                self.character.move_right()

            # 화면 범위 제한 및 바닥 충돌 처리
            self.character.apply_gravity(gravity)
            self.character.apply_movement()
            self.character.apply_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)

            # 충돌 검사 및 처리
            block_collided = check_collision(self.character, self.blocks)
            if block_collided:
                if self.character.vertical_momentum > 0:
                    self.character.y = block_collided.y - self.character.height
                    self.character.vertical_momentum = 0
                    self.character.is_on_ground = True
            elif self.character.y >= floor_y - self.character.height:
                self.character.y = floor_y - self.character.height
                self.character.vertical_momentum = 0
                self.character.is_on_ground = True
            else:
                self.character.is_on_ground = False

            # 포탈 충돌 검사 및 처리
            if check_portal_collision(self.character, self.portal):
                if self.stage_index == len(self.stages) - 1:  # 만약 마지막 스테이지라면
                    # hyunyoolim 폴더 안에 있는 main 모듈의 main 함수 실행
                    try:
                        subprocess.run(["python", os.path.join(hyunyoolim_path, "main.py")])
                    except Exception as e:
                        print("Failed to run hyunyoolim:", e)
                    pygame.quit()
                    sys.exit()
                else:
                    self.next_stage()
                continue

            # 가시 충돌 검사 및 처리
            spike_collided = check_spike_collision(self.character, self.spikes)
            if spike_collided:
                print("Character hit a spike! Respawning...")
                reset_game(self.character, self.stage.initial_character_x, self.stage.initial_character_y)

            # 바닥과 충돌하면 게임 리셋
            if self.character.y >= floor_y - self.character.height:
                reset_game(self.character, self.stage.initial_character_x, self.stage.initial_character_y)

            # 발판 그리기, 움직임 구현
            for block in self.blocks:
                block.move()
                pygame.draw.rect(screen, BLUE, (block.x, block.y, block.width, block.height))
            for block in self.blocks:
                block.draw(screen)  # 변경된 draw 메소드 사용

            # 포탈 그리기
            self.portal.draw(screen)

            # 가시 그리기
            for spike in self.spikes:
                pygame.draw.rect(screen, (0, 0, 0), spike.rect)  # 가시 색상은 검정색으로 설정

            # 캐릭터 그리기
            self.character.draw(screen)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()