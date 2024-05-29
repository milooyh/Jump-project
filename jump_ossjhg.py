import pygame
import sys
import random

pygame.init()

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("점프 점프")

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 223, 0)
PURPLE = (128, 0, 128)
FLOOR_COLOR = (144, 228, 144)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)  # 새로운 적 색깔

# 캐릭터 속성 설정
character_width, character_height = 20, 20
character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - character_height * 2
character_speed = 6
jump_speed = 20
gravity = 1.4

# 바닥 속성 설정
floor_height = 22  # 바닥 두께
floor_y = SCREEN_HEIGHT - floor_height

# 발판 속성 설정
platform_width, platform_height = 100, 20
platform_color = BLUE

# 파워업 속성 설정
powerup_radius = 10

# 적 속성 설정
enemy_width, enemy_height = 35, 35
enemy_speed = 5

# 스테이지 1 설정
stage1_blocks_positions = [
    (100, 500),
    (300, 400),
    (500, 300),
    (700, 200)
]
stage1_enemy_positions = [
    (150, 450),
    (350, 350),
    (550, 250),
    (750, 150)
]
stage1_powerup_positions = [
    (100 + (platform_width // 2 - powerup_radius), 500 - powerup_radius * 2),
    (300 + (platform_width // 2 - powerup_radius), 400 - powerup_radius * 2),
    (500 + (platform_width // 2 - powerup_radius), 300 - powerup_radius * 2)
]

# 스테이지 2 설정
stage2_blocks_positions = [
    (150, 450),
    (350, 350),
    (500, 200),
    (700, 150),
    (200, 250),  # 변경된 위치 - 추가 발판
    (600, 300)   # 변경된 위치 - 추가 발판
]
stage2_enemy_positions = [
    (100, 450),
    (250, 350),
    (400, 250),
    (600, 150),
    (200, 400),  # 변경된 위치 - 추가 발판
    (550, 300)   # 변경된 위치 - 추가 발판
]
stage2_powerup_positions = [
    (150 + (platform_width // 2 - powerup_radius), 450 - powerup_radius * 2),
    (350 + (platform_width // 2 - powerup_radius), 350 - powerup_radius * 2),
    (500 + (platform_width // 2 - powerup_radius), 200 - powerup_radius * 2)
]

# 스테이지 3 설정
stage3_blocks_positions = [
    (100, 450),
    (250, 350),
    (400, 250),
    (600, 150),
    (550, 300)   # 변경된 위치 - 추가 발판
]
stage3_enemy_positions = [
    (100, 400),
    (250, 300),
    (400, 200),
    (650, 100),
    (600, 250)
]
stage3_powerup_positions = [
    (100 + (platform_width // 2 - powerup_radius), 450 - powerup_radius * 2),
    (250 + (platform_width // 2 - powerup_radius), 350 - powerup_radius * 2),
    (400 + (platform_width // 2 - powerup_radius), 250 - powerup_radius * 2)
]

# 블록 클래스 정의
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 적 클래스 정의
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1

# 새로운 추적형 적 클래스 정의
class ChasingEnemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, player_x, player_y):
        if player_x > self.x:
            self.x += self.speed
        elif player_x < self.x:
            self.x -= self.speed

    def draw(self, screen):
        # 가시공 모양 그리기
        pygame.draw.polygon(screen, BLACK, [(self.x + enemy_width//2, self.y),  # 꼭짓점 1
                                            (self.x + enemy_width, self.y + enemy_height//2),  # 꼭짓점 2
                                            (self.x + enemy_width//2, self.y + enemy_height),  # 꼭짓점 3
                                            (self.x, self.y + enemy_height//2)])  # 꼭짓점 4

# 파워업 클래스 정의
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 포탈 클래스 정의
class Portal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 스테이지 초기화 함수
def init_stage(blocks_positions, enemy_positions, powerup_positions):
    blocks = [Block(x, y) for x, y in blocks_positions]
    enemies = [Enemy(x, y) for x, y in enemy_positions]
    powerups = [PowerUp(x, y) for x, y in powerup_positions]
    chasing_enemy = ChasingEnemy(650, 150, 2)  # 새로운 추적형 적 추가
    return blocks, enemies, powerups, chasing_enemy

# 초기 스테이지 설정
current_stage = 1
blocks, enemies, powerups, chasing_enemy = init_stage(stage1_blocks_positions, stage1_enemy_positions, stage1_powerup_positions)

# 포탈 초기화
portal = None

clock = pygame.time.Clock()

# 충돌 감지
def check_collision(character, objects, width, height):
    for obj in objects:
        if character.colliderect(pygame.Rect(obj.x, obj.y, width, height)):
            return obj
    return None

# 게임 루프
running = True
vertical_momentum = 0
is_on_ground = True
space_pressed = False
score = 0
time_limit = 20  # 게임 시간 제한 (초)
start_ticks = pygame.time.get_ticks()  # 시작 시간
powerup_effect_duration = 5  # 파워업 효과 지속 시간 (초)
powerup_effect_start_time = 0  # 파워업 효과 시작 시간
powerup_effect = None

while running:
    screen.fill(WHITE)
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

    # 남은 시간 계산
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # 경과 시간(초)
    time_left = time_limit - seconds
    if time_left <= 0:
        running = False  # 시간이 다 되면 게임 종료

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                space_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    if space_pressed and is_on_ground:
        vertical_momentum = -jump_speed
        is_on_ground = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed

    # 파워업 효과 적용
    if powerup_effect:
        if powerup_effect == "speed":
            character_speed = 10  # 속도 증가 효과
        elif powerup_effect == "jump":
            jump_speed = 25  # 점프 높이 증가 효과
        
        # 파워업 효과 지속 시간 체크
        if (pygame.time.get_ticks() - powerup_effect_start_time) / 1000 > powerup_effect_duration:
            character_speed = 7.5
            jump_speed = 20
            powerup_effect = None

    # 화면 범위 제한 및 바닥 충돌 처리
    character_x = max(0, min(SCREEN_WIDTH - character_width, character_x))
    vertical_momentum += gravity
    character_y += vertical_momentum
    character_y = min(character_y, floor_y - character_height)

    # 충돌 검사 및 처리
    block_collided = check_collision(character_rect, blocks, platform_width, platform_height)
    if block_collided:
        if vertical_momentum > 0:
            character_y = block_collided.y - character_height
            vertical_momentum = 0
            is_on_ground = True
    elif character_y >= floor_y - character_height:
        character_y = floor_y - character_height
        vertical_momentum = 0
        is_on_ground = True
    else:
        is_on_ground = False

    # 적 충돌 검사 및 처리
    enemy_collided = check_collision(character_rect, enemies, enemy_width, enemy_height)
    if enemy_collided:
        running = False  # 적과 충돌하면 게임 종료

    # 추적형 적 업데이트 및 충돌 검사
    chasing_enemy.update(character_x, character_y)
    if character_rect.colliderect(pygame.Rect(chasing_enemy.x, chasing_enemy.y, enemy_width, enemy_height)):
        running = False  # 추적형 적과 충돌하면 게임 종료

    # 파워업 충돌 검사 및 처리
    powerup_collided = check_collision(character_rect, powerups, powerup_radius * 2, powerup_radius * 2)
    if powerup_collided:
        powerups.remove(powerup_collided)
        score += 10  # 파워업 수집 시 점수 증가
        
    # 모든 파워업을 수집하면 포탈 생성
    if not powerups and not portal:
        last_block = blocks[-1]
        portal = Portal(last_block.x + platform_width - 30, last_block.y - 80)

    # 포탈 충돌 검사 및 처리
    portal_rect = None
    if portal:
        portal_rect = pygame.Rect(portal.x, portal.y, 30, 80)
        if character_rect.colliderect(portal_rect):
            if current_stage == 1:
                # 스테이지 2로 이동
                blocks, enemies, powerups, chasing_enemy = init_stage(stage2_blocks_positions, stage2_enemy_positions, stage2_powerup_positions)
                current_stage = 2
                portal = None
                character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - character_height * 2
                start_ticks = pygame.time.get_ticks()  # 새로운 스테이지에서 시간 초기화
            elif current_stage == 2:
                # 스테이지 3로 이동
                blocks, enemies, powerups, chasing_enemy = init_stage(stage3_blocks_positions, stage3_enemy_positions, stage3_powerup_positions)
                current_stage = 3
                portal = None
                character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - character_height * 2
                start_ticks = pygame.time.get_ticks()  # 새로운 스테이지에서 시간 초기화
            else:
                running = False  # 스테이지 3에서 포탈에 도달하면 게임 종료 (또는 다음 스테이지로 이동 가능)

    # 적 이동 및 화면 그리기
    for enemy in enemies:
        enemy.x += enemy_speed * enemy.direction
        if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy_width:
            enemy.direction *= -1  # 화면 끝에 도달하면 방향 전환
        pygame.draw.rect(screen, GREEN, (enemy.x, enemy.y, enemy_width, enemy_height))

    # 추적형 적 그리기
    chasing_enemy.draw(screen)

    # 바닥 그리기
    pygame.draw.rect(screen, FLOOR_COLOR, (0, floor_y, SCREEN_WIDTH, floor_height))

    # 발판 그리기
    for block in blocks:
        pygame.draw.rect(screen, platform_color, (block.x, block.y, platform_width, platform_height))
        
    # 파워업 그리기
    for powerup in powerups:
        pygame.draw.circle(screen, YELLOW, (powerup.x + powerup_radius, powerup.y + powerup_radius), powerup_radius)

    # 포탈 그리기
    if portal:
        pygame.draw.ellipse(screen, PURPLE, portal_rect)

    # 캐릭터 그리기
    pygame.draw.rect(screen, RED, character_rect)

    # 점수 표시
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # 남은 시간 표시
    time_text = font.render(f"Time left: {int(time_left)}", True, (0, 0, 0))
    screen.blit(time_text, (SCREEN_WIDTH - 200, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
