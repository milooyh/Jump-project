import pygame
import sys
from game_over import show_game_over_screen
from stage import init_stage, stages, ChasingEnemy
from portal import Portal

def main():
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
    ORANGE = (255, 165, 0)
    BROWN = (139, 69, 19)

    # 캐릭터 속성 설정
    character_width, character_height = 20, 20
    character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - character_height * 2
    character_speed = 6
    jump_speed = 20
    gravity = 1.4

    # 바닥 속성 설정
    floor_height = 22  # 바닥 두께
    floor_y = SCREEN_HEIGHT - floor_height
    FLOOR_COLOR = (139, 69, 19)

    # 발판 속성 설정
    platform_width, platform_height = 100, 20
    platform_color = BLUE

    # 파워업 속성 설정
    powerup_radius = 10

    # 적 속성 설정
    enemy_width, enemy_height = 35, 35
    enemy_speed = 5

    # 스테이지 설정
    current_stage = 1
    blocks, enemies, powerups, chasing_enemy = init_stage(*stages[current_stage])
    portal = None

    clock = pygame.time.Clock()

    def check_collision(character, objects, width, height):
        for obj in objects:
            if character.colliderect(pygame.Rect(obj.x, obj.y, width, height)):
                return obj
        return None

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

    while running:
        screen.fill(WHITE)
        character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = time_limit - seconds
        if time_left <= 0:
            show_game_over_screen(screen, score)
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
            vertical_momentum = -jump_speed
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
        elif character_y >= floor_y - character_height:
            character_y = floor_y - character_height
            vertical_momentum = 0
            is_on_ground = True
        else:
            is_on_ground = False

        enemy_collided = check_collision(character_rect, enemies, enemy_width, enemy_height)
        if enemy_collided:
            show_game_over_screen(screen, score)
            running = False

        chasing_enemy.update(character_x, character_y)
        if character_rect.colliderect(pygame.Rect(chasing_enemy.x, chasing_enemy.y, enemy_width, enemy_height)):
            show_game_over_screen(screen, score)
            running = False

        powerup_collided = check_collision(character_rect, powerups, powerup_radius * 2, powerup_radius * 2)
        if powerup_collided:
            powerups.remove(powerup_collided)
            score += 10

        if not powerups and portal is None:
            last_block = blocks[-1]
            portal = Portal(last_block.x + platform_width // 2 - 15, last_block.y - 80)

        if portal and character_rect.colliderect(pygame.Rect(portal.x, portal.y, 30, 80)):
            current_stage += 1
            if current_stage in stages:
                blocks, enemies, powerups, chasing_enemy = init_stage(*stages[current_stage])
                portal = None
                character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - character_height * 2
                start_ticks = pygame.time.get_ticks()
            else:
                show_game_over_screen(screen, score)
                running = False

        pygame.draw.rect(screen, FLOOR_COLOR, (0, floor_y, SCREEN_WIDTH, floor_height))
        pygame.draw.rect(screen, RED, character_rect)

        for block in blocks:
            pygame.draw.rect(screen, platform_color, (block.x, block.y, platform_width, platform_height))

        for enemy in enemies:
            enemy.x += enemy_speed * enemy.direction
            if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy_width:
                enemy.direction *= -1
            pygame.draw.rect(screen, GREEN, (enemy.x, enemy.y, enemy_width, enemy_height))

        chasing_enemy.draw(screen)

        for powerup in powerups:
            pygame.draw.circle(screen, YELLOW, (powerup.x + powerup_radius, powerup.y + powerup_radius), powerup_radius)

        if portal:
            portal.draw(screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}  Time Left: {int(time_left)}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
