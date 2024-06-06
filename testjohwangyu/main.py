import pygame
import sys
import stage1
from portal import Portal
import game_over

pygame.init()

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("점프 점프")

# 스테이지 1 초기화
stage1.initialize(SCREEN_HEIGHT)

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 캐릭터 속성 설정
character_width, character_height = 20, 20
character_x, character_y = character_width // 2, SCREEN_HEIGHT - character_height * 2
character_speed = 6
jump_speed = 20
gravity = 1.4

clock = pygame.time.Clock()

# 게임 루프
running = True
vertical_momentum = 0
is_on_ground = False  # 초기에는 땅에 있지 않음

while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_on_ground:
                vertical_momentum = -jump_speed
                is_on_ground = False

    # 캐릭터 이동 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed

    # 화면 범위 제한
    character_x = max(0, min(SCREEN_WIDTH - character_width, character_x))

    # 발판과 충돌 검사
    block_collided = stage1.check_collision(pygame.Rect(character_x, character_y, character_width, character_height), stage1.blocks)
    if block_collided:
        if vertical_momentum > 0:  # 캐릭터가 발판을 위로 올라가는 중일 때만
            character_y = block_collided.y - character_height
            vertical_momentum = 0
            is_on_ground = True

    # 캐릭터 수직 이동 처리
    vertical_momentum += gravity
    character_y += vertical_momentum

    # 땅에 닿았는지 확인
    if character_y >= stage1.floor_y - character_height:
        character_y = stage1.floor_y - character_height
        vertical_momentum = 0
        is_on_ground = True

    # 캐릭터와 빨간색 발판 충돌 검사
    red_spike_collided = pygame.Rect(character_x, character_y, character_width, character_height).colliderect(pygame.Rect(stage1.blocks_positions[0][0], stage1.floor_y - stage1.platform_height * 2, stage1.platform_width, stage1.platform_height))
    if red_spike_collided:
        game_over.show_game_over(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    # 스테이지 1 그리기
    stage1.draw(screen)

    # 캐릭터 그리기
    pygame.draw.rect(screen, RED, (character_x, character_y, character_width, character_height))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()