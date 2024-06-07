import pygame
import sys
from game_over import show_game_over_screen
from stage import init_stage, stages
from lobby import show_lobby_screen
from spike import Spike

def main():
    pygame.init()

    # 화면 크기 설정
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("점프 점프")

    # 로비 화면 표시
    lobby_choice = show_lobby_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    if lobby_choice == "start":
        print("game start!")
        # 게임 시작 코드 작성
    elif lobby_choice == "quit":
        print("Exit Game")
        pygame.quit()
        sys.exit()

    # 색깔 정의
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 223, 0)
    PURPLE = (128, 0, 128)
    FLOOR_COLOR = (144, 228, 144)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)
    BROWN = (139, 69, 19)

    # 캐릭터 속성 설정
    character_width, character_height = 20, 20
    character_x, character_y = character_width, SCREEN_HEIGHT - character_height * 2
    character_speed = 6
    jump_speed = 17
    gravity = 1.4

    # 바닥 속성 설정
    floor_height = 150
    floor_y = SCREEN_HEIGHT - floor_height
    FLOOR_COLOR = (139, 69, 19)
    
    # 발판 속성 설정
    platform_width, platform_height = 100, 20
    platform_color = BLUE

    # 파워업 속성 설정
    powerup_radius = 10

    # 적 속성 설정
    enemy_width, enemy_height = 33, 33
    enemy_speed = 5

    # 스테이지 설정
    current_stage = 1
    blocks, enemies, powerups, portal = init_stage(*stages[current_stage])

    # 추가된 부분: 두 번째 블록의 좌표 설정
    second_block_x, second_block_y = 500, 350  # 예시 좌표
    
    # 가시 돌 생성
    spike = Spike(505, floor_y - 1, 90, 20)

    clock = pygame.time.Clock()

    def check_collision(character, objects, width, height):
        for obj in objects:
            if character.colliderect(pygame.Rect(obj.x, obj.y, width, height)):
                return obj
        return None

    # 추가된 함수: 바닥을 지우는 함수
    def remove_floor_section(x, width):
        # 바닥의 색깔을 흰색으로 덮어서 지움
        pygame.draw.rect(screen, WHITE, (x, floor_y, width, floor_height))

# 추가된 함수: 플레이어와 가시 돌의 충돌 확인
    def check_spike_collision(player_rect, spike_rect):
        if player_rect.colliderect(spike_rect):
            return True
        return False

    running = True
    vertical_momentum = 0
    is_on_ground = True
    space_pressed = False
    score = 0
    time_limit = 20
    start_ticks = pygame.time.get_ticks()
    powerup_effect_duration = 5
    powerup_effect_start_time = 0
    powerup_effect = None

    floor_removed = False  # 바닥이 지워졌는지 여부를 추적하는 변수

    while running:
        screen.fill(WHITE)
        character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = time_limit - seconds
        if time_left <= 0:
            choice = show_game_over_screen(screen, score)
            if choice == "restart":
                # 재시작
                # 캐릭터 및 게임 상태 초기화 코드 작성
                pass
            else:
                running = False
                
        # 추가된 부분: 가시 돌과 플레이어의 충돌 확인
        if check_spike_collision(character_rect, spike.rect):
            choice = show_game_over_screen(screen, score)
            if choice == "restart":
                # 재시작
                # 캐릭터 및 게임 상태 초기화 코드 작성
                pass
            else:
                running = False

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
            vertical_momentum = -         jump_speed
            is_on_ground = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= character_speed
        if keys[pygame.K_RIGHT]:
            character_x += character_speed

        character_x = max(0, min(SCREEN_WIDTH - character_width, character_x))
        vertical_momentum += gravity
        character_y += vertical_momentum
        character_y = min(character_y, floor_y - character_height)

        block_collided = check_collision(character_rect, blocks, platform_width, platform_height)
        if block_collided:
            if vertical_momentum > 0:
                character_y = block_collided.y - character_height
                vertical_momentum = 0
                is_on_ground = True
                # 수정된 부분: 두 번째 블록을 밟으면 바닥을 지우고 블록을 제거
                if block_collided.x == second_block_x and block_collided.y == second_block_y:
                    blocks.remove(block_collided)
                    floor_removed = True
        elif character_y >= floor_y - character_height:
            character_y = floor_y - character_height
            vertical_momentum = 0
            is_on_ground = True
        else:
            is_on_ground = False

        enemy_collided = check_collision(character_rect, enemies, enemy_width, enemy_height)
        if enemy_collided:
            choice = show_game_over_screen(screen, score)
            if choice == "restart":
                # 재시작
                # 캐릭터 및 게임 상태 초기화 코드 작성
                pass
            else:
                running = False

        for enemy in enemies:
            enemy.x += enemy_speed * enemy.direction
            if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy_width:
                enemy.direction *= -1

        powerup_collided = check_collision(character_rect, powerups, powerup_radius * 2, powerup_radius * 2)
        if powerup_collided:
            powerups.remove(powerup_collided)
            score += 1

        if portal and character_rect.colliderect(pygame.Rect(portal.x, portal.y, 30, 80)):
            current_stage += 1
            if current_stage in stages:
                blocks, enemies, powerups, portal = init_stage(*stages[current_stage])
                # 캐릭터 시작 위치를 왼쪽 끝에 가깝게 설정
                character_x, character_y = character_width, SCREEN_HEIGHT - character_height * 2
                start_ticks = pygame.time.get_ticks()
            else:
                choice = show_game_over_screen(screen, score)
                if choice == "restart":
                    # 재시작
                    # 캐릭터 및 게임 상태 초기화 코드 작성
                    pass
                else:
                    running = False

        # 바닥이 지워진 경우 지우기
        if floor_removed:
            remove_floor_section(second_block_x, platform_width)

        pygame.draw.rect(screen, FLOOR_COLOR, (0, floor_y, SCREEN_WIDTH, floor_height))
        pygame.draw.rect(screen, RED, character_rect)

        for block in blocks:
            pygame.draw.rect(screen, platform_color, (block.x, block.y, platform_width, platform_height))

        for enemy in enemies:
            pygame.draw.rect(screen, GREEN, (enemy.x, enemy.y, enemy_width, enemy_height))

        for powerup in powerups:
            pygame.draw.circle(screen, YELLOW, (powerup.x + powerup_radius, powerup.y + powerup_radius), powerup_radius)

        if portal:
            portal.draw(screen)
            
        # 추가된 부분: 가시 돌 그리기
        pygame.draw.rect(screen, BLACK, spike.rect)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}  Time Left: {int(time_left)}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
