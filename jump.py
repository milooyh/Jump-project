import pygame
import sys
import random

# Pygame 초기화
pygame.init()
pygame.font.init()

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # 가로 세로
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("점프 점프")

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FLOOR_COLOR = (144, 228, 144)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 144, 144)
PORTAL_COLOR = (255, 0, 255)

# 캐릭터 속성 설정
character_width, character_height = 20, 20
character_speed = 6
jump_speed = 20
gravity = 1.4

# 상수 정의
LEFT_EDGE = 0
RIGHT_EDGE = SCREEN_WIDTH - character_width

# 바닥 속성 설정
floor_height = 22  # 바닥 두께
floor_y = SCREEN_HEIGHT - floor_height

# 발판 속성 설정
platform_width, platform_height = 100, 20
platform_color = BLUE

# 장애물 속성 설정
obstacle_width, obstacle_height = 80, 30
obstacle_color = BLACK

# # 아이템 속성 설정
# ITEM_WIDTH, ITEM_HEIGHT = 20, 20
# ITEM_COLORS = {
#     "life": GREEN,
#     "jump": BLUE,
#     "speed": RED
# }

# 블록 좌표 설정
blocks_positions = [
    (100, 500),
    (300, 400),
    (500, 300),
    (700, 200)
]

# 장애물 좌표 설정
obstacles_positions = [
    (200, 400),
    (400, 300),
    (600, 200),
    (800, 100)
]

# 블록 클래스 정의
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 포털 클래스 정의
class Portal:
    def __init__(self, x, y):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH - self.width - 20  # 화면 오른쪽에 고정된 x 좌표
        self.y = 20  # 화면 상단에 고정된 y 좌표
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
# 블록, 장애물 리스트 초기화
blocks = [Block(x, y) for x, y in blocks_positions]
obstacles = [Block(x, y) for x, y in obstacles_positions]

clock = pygame.time.Clock()  # 게임 프레임 속도 제어

# 충돌 감지
def check_collision(character, blocks):
    for block in blocks:
        if character.colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
            return block
    return None

# 새로운 발판 추가 함수
def add_new_platform():
    x = random.randint(0, SCREEN_WIDTH - platform_width)
    y = random.randint(0, SCREEN_HEIGHT // 2)
    blocks.append(Block(x, y))
    
# 캐릭터 초기 위치 설정 함수
def set_character_initial_position():
    global character_x, character_y
    character_x = SCREEN_WIDTH // 2
    character_y = SCREEN_HEIGHT - character_height * 2
    life = 3  # 캐릭터의 초기 생명력


def reset_game():
    global character_x, character_y, vertical_momentum, is_on_ground, space_pressed, life, game_clear, game_over, collision_message, collision_time, item_effects, effect_start_time, portal
    set_character_initial_position()
    vertical_momentum = 0
    is_on_ground = True
    space_pressed = False
    life = 3
    game_over = False
    game_clear = False
    collision_message = ""
    collision_time = 0
    item_effects = {}  # 아이텀 효과 초기화
    effect_start_time = {}  # 효과 시작 시간 초기화
    
    # 포털 생성
    if len(blocks) > 0:
        last_block = blocks[-1]
        portal = Portal(last_block.x, last_block.y - 70)  # 마지막 발판 위에 포털 생성
    else:
        portal = None  # 발판이 없으면 포털 생성하지 않음

# 게임 시작 페이지 표시 함수
def show_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 64)
    text = font.render("Press SPACE to Start", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    
# 초기 설정
reset_game()
new_platform_interval = 3000  # 3초마다 새로운 발판 추가
last_platform_time = pygame.time.get_ticks()
new_item_interval = 5000  # 5초마다 새로운 아이템 추가
last_item_time = pygame.time.get_ticks()

# 화면 이동 관련 변수 초기화
screen_move_speed = character_speed
screen_move_threshold = SCREEN_WIDTH // 2
screen_move_height = SCREEN_HEIGHT // 4  # 캐릭터가 점프할 때마다 화면을 이동시킬 높이

# # 아이템 리스트 초기화
# items = []

# 발판 클래스에 현재 위치 저장
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# # 아이템 생성 함수 수정
# def spawn_item():
#     # 발판 중 랜덤하게 선택
#     platform = random.choice(blocks)
#     print("Platform coordinates:", platform.x, platform.y)  # 발판의 좌표 출력
#     # 발판의 좌표를 기준으로 아이템 위치 조정
#     x = random.randint(0, platform_width - ITEM_WIDTH)  # 발판 내부에서 랜덤하게 위치
#     y = -ITEM_HEIGHT  # 발판 위에 위치하도록 조정
#     # 아이템의 실제 좌표는 발판의 위치와 합산하여 설정
#     item_x = platform.x + x
#     item_y = platform.y + y
#     item_type = random.choice(["life", "jump", "speed"])
#     color = ITEM_COLORS[item_type]
#     items.append(Item(item_x, item_y, ITEM_WIDTH, ITEM_HEIGHT, item_type, color))


# # 아이템 그리기 함수
# def draw_items():
#     for item in items:
#         pygame.draw.rect(screen, item.color, (item.x, item.y, item.width, item.height))
        
        

# # 아이템 효과 적용 함수
# def apply_item_effects(character_rect):
#     global life, jump_speed, character_speed, item_effects, effect_start_time
#     for item in items:
#         if character_rect.colliderect(item.rect):
#             if item.item_type == "life":
#                 life += 1
#             elif item.item_type == "jump":
#                 jump_speed += 10
#                 item_effects["jump"] = pygame.time.get_ticks()  # 효과 시작 시간 기록
#                 effect_start_time["jump"] = pygame.time.get_ticks()
#             elif item.item_type == "speed":
#                 character_speed += 10
#                 item_effects["speed"] = pygame.time.get_ticks()  # 효과 시작 시간 기록
#                 effect_start_time["speed"] = pygame.time.get_ticks()
#             items.remove(item)  # 아이템 효과를 적용한 후에는 리스트에서 제거

# # 아이템 효과 해제 함수
# def remove_item_effects():
#     global jump_speed, character_speed, item_effects, effect_start_time
#     current_time = pygame.time.get_ticks()
#     for effect in list(item_effects):
#         if current_time - effect_start_time[effect] > 10000:  # 효과가 10초 지속되도록
#             if effect == "jump":
#                 jump_speed -= 10
#             elif effect == "speed":
#                 character_speed -= 10
#             del item_effects[effect]  # 효과 제거
#             del effect_start_time[effect]


# 게임 시작 페이지 표시
show_start_screen()
            
# 게임 루프
running = True

# 게임 오버 화면에 사용자가 선택할 수 있는 두 가지 버튼을 추가
try_again_button_rect = pygame.Rect(250, 400, 300, 50)
exit_button_rect = pygame.Rect(250, 500, 300, 50)

# 클리어 화면에 사용자가 선택할 수 있는 두 가지 버튼 추가
next_stage_button_rect = pygame.Rect(250, 400, 300, 50)

while running:
    screen.fill(WHITE)
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    if not game_over:
        # 게임 진행 중일 때의 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼 클릭
                    if game_over:
                        if try_again_button_rect.collidepoint(event.pos):
                            reset_game()
                        elif exit_button_rect.collidepoint(event.pos):
                            running = False


        # 일정 간격으로 새로운 발판 추가
        current_time = pygame.time.get_ticks()
        if current_time - last_platform_time > new_platform_interval:
            add_new_platform()
            last_platform_time = current_time
            
        # 스페이스 눌리고 바닥에 있으면 점프
        if space_pressed and is_on_ground:
            vertical_momentum = -jump_speed
            is_on_ground = False

        # 상하좌우 이동키 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x = max(LEFT_EDGE, character_x - character_speed)
        if keys[pygame.K_RIGHT]:
            character_x = min(RIGHT_EDGE, character_x + character_speed)

        # 화면 이동 관련 처리
        if character_x > screen_move_threshold:
            for block in blocks:
                block.x -= screen_move_speed
            for obstacle in obstacles:
                obstacle.x -= screen_move_speed
            character_x -= screen_move_speed

        character_x = max(0, min(SCREEN_WIDTH - character_width, character_x))  # 화면 밖으로 나
        character_x = max(0, min(SCREEN_WIDTH - character_width, character_x))  # 화면 밖으로 나가지 않게
        vertical_momentum += gravity
        character_y += vertical_momentum
        character_y = min(character_y, floor_y - character_height)

        # 바닥에 닿으면 수직 속도를 0으로 하고 바닥에 있다고 표시
        if character_y >= floor_y - character_height:
            character_y = floor_y - character_height
            vertical_momentum = 0
            is_on_ground = True

        # 바닥
        pygame.draw.rect(screen, FLOOR_COLOR, (0, floor_y, SCREEN_WIDTH, floor_height))

        # 장애물 이동 및 그리기
        for obstacle in obstacles:
            obstacle.x -= character_speed // 2  # 캐릭터 속도의 절반만 이동하도록 설정
            if obstacle.x + obstacle_width < 0:  # 장애물이 화면을 벗어나면
                obstacle.x = SCREEN_WIDTH  # 오른쪽에서 다시 나타남
            pygame.draw.rect(screen, obstacle_color, (obstacle.x, obstacle.y, obstacle_width, obstacle_height))

        # # 아이템 생성 및 관리
        # current_time = pygame.time.get_ticks()
        # if current_time - last_item_time > new_item_interval:
        #     spawn_item()
        #     last_item_time = current_time

        # draw_items()
        # apply_item_effects(character_rect)
        # remove_item_effects = current_time
        
        # 충돌 검사 및 처리
        block_collided = check_collision(character_rect, blocks)
        obstacle_collided = check_collision(character_rect, obstacles)
        if block_collided:
            if vertical_momentum > 0:
                character_y = block_collided.y - character_height
                vertical_momentum = 0
                is_on_ground = True
        if obstacle_collided:
            life -= 1
            collision_message = f"Life: {life}"
            collision_time = pygame.time.get_ticks()  # 충돌 시간 기록
            if life == 0:
                game_over = True  # life가 0이 되면 game over 상태로 변경
            else:
                # 충돌 시 캐릭터 위치 초기화
                set_character_initial_position()
                vertical_momentum = 0
                is_on_ground = True
                blocks = [Block(x, y) for x, y in blocks_positions]
                obstacles = [Block(x, y) for x, y in obstacles_positions]

        # 포털 생성 및 충돌 처리
        if portal is None and len(blocks) > 0 and pygame.time.get_ticks() - last_platform_time > new_platform_interval:
            portal = Portal(blocks[-1].x, blocks[-1].y - 70)  # 포털을 마지막 발판 위에 생성
            last_platform_time = pygame.time.get_ticks()

        if portal:
            if character_x > screen_move_threshold:
                dx = character_x - screen_move_threshold
                portal.x -= dx
                
            if character_y < screen_move_height:
                dy = screen_move_height - character_y
                portal.y += dy

        if portal and game_clear:
            if character_rect.colliderect(portal.rect):
                game_clear = True  # 포털에 도달하면 게임 클리어
        
        if portal:
            pygame.draw.rect(screen, PORTAL_COLOR, portal.rect)
            
        # 블록 처리
        for block in blocks:
            pygame.draw.rect(screen, platform_color, (block.x, block.y, platform_width, platform_height))

        # 목숨에 따라 캐릭터 색상 변경
        if life == 3:
            character_color = RED
        elif life == 2:
            character_color = ORANGE
        elif life == 1:
            character_color = YELLOW

        # 캐릭터 처리
        pygame.draw.rect(screen, character_color, character_rect)

        # 목숨 표시
        font = pygame.font.Font(None, 36)
        life_text = font.render(f'Life: {life}', True, BLACK)
        screen.blit(life_text, (10, 10))

        # 충돌 메시지 표시
        if collision_message:
            current_time = pygame.time.get_ticks()
            if current_time - collision_time < 1000:  # 충돌 메시지 1초 동안 표시
                collision_font = pygame.font.Font(None, 74)
                collision_text = collision_font.render(collision_message, True, BLACK)
                collision_rect = collision_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(collision_text, collision_rect)
            else:
                collision_message = ""

        # 캐릭터의 y 위치가 화면 이동 높이에 도달하면 화면을 위로 이동시킴
        if character_y < screen_move_height:
            for block in blocks:
                block.y += screen_move_speed
            for obstacle in obstacles:
                obstacle.y += screen_move_speed
            character_y += screen_move_speed
            
    # 게임 클리어 시 클리어 화면 표시
    if game_clear:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        text = font.render("Stage Clear!", True, GREEN)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        pygame.draw.rect(screen, GREEN, next_stage_button_rect)
        pygame.draw.rect(screen, RED, exit_button_rect)

        font = pygame.font.Font(None, 36)
        next_stage_text = font.render("Next Stage", True, BLACK)
        screen.blit(next_stage_text, (next_stage_button_rect.x + (next_stage_button_rect.width - next_stage_text.get_width()) // 2,
                                      next_stage_button_rect.y + (next_stage_button_rect.height - next_stage_text.get_height()) // 2))

        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (exit_button_rect.x + (exit_button_rect.width - exit_text.get_width()) // 2,
                                exit_button_rect.y + (exit_button_rect.height - exit_text.get_height()) // 2))

        # 마우스가 버튼 위에 있을 때 색상 변경
        if next_stage_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_GREEN, next_stage_button_rect, border_radius=10)
        if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_RED, exit_button_rect, border_radius=10)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_stage_button_rect.collidepoint(event.pos):
                    reset_game()  # 게임 리셋하여 다음 스테이지로 이동
                    # 다음 스테이지 설정 (추가적인 로직 필요)
                if exit_button_rect.collidepoint(event.pos):
                    running = False
            
    if game_over:
        # 게임 오버 메시지 출력
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

        # "Try Again" 버튼 그리기
        pygame.draw.rect(screen, GREEN, try_again_button_rect)
        try_again_font = pygame.font.Font(None, 36)
        try_again_text = try_again_font.render("Try Again", True, BLACK)
        try_again_text_rect = try_again_text.get_rect(center=try_again_button_rect.center)
        screen.blit(try_again_text, try_again_text_rect)

        # "Exit" 버튼 그리기
        pygame.draw.rect(screen, RED, exit_button_rect)
        exit_font = pygame.font.Font(None, 36)
        exit_text = exit_font.render("Exit", True, BLACK)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)

        # 마우스가 버튼 위에 있을 때 색상 변경
        if try_again_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_GREEN, try_again_button_rect, border_radius=10)
        if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_RED, exit_button_rect, border_radius=10)

        # 게임 재시작 또는 종료 버튼 클릭 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 왼쪽 마우스 버튼 클릭
                    if try_again_button_rect.collidepoint(event.pos):
                        reset_game()
                    elif exit_button_rect.collidepoint(event.pos):
                        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
