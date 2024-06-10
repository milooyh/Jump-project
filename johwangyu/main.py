import pygame
import sys
import subprocess
from game_over import show_game_over_screen
from stage import init_stage, stages
from spike import Spike

# 이미지 로딩 및 크기 조정
left_walk = pygame.image.load('C:/OSSW4/Img/Left_W.png')
left_jump = pygame.image.load('C:/OSSW4/Img/Left_J.png')
right_walk = pygame.image.load('C:/OSSW4/Img/Right_W.png')
right_jump = pygame.image.load('C:/OSSW4/Img/Right_J.png')
user_image = pygame.image.load('C:/OSSW4/Img/User.png')
block_image = pygame.image.load('C:/OSSW4/Img/block.png')

left_walk = pygame.transform.scale(left_walk, (20, 20))
left_jump = pygame.transform.scale(left_jump, (20, 20))
right_walk = pygame.transform.scale(right_walk, (20, 20))
right_jump = pygame.transform.scale(right_jump, (20, 20))
user_image = pygame.transform.scale(user_image, (20, 20))
block_image = pygame.transform.scale(block_image, (100, 20))

def check_collision(character_rect, objects, obj_width, obj_height):
    for obj in objects:
        obj_rect = pygame.Rect(obj.x, obj.y, obj_width, obj_height)
        if character_rect.colliderect(obj_rect):
            return obj
    return None

def check_spike_collision(character_rect, spike_rect):
    return character_rect.colliderect(spike_rect)

def remove_floor_section(blocks, x_position, width):
    for block in blocks:
        if block.x == x_position:
            blocks.remove(block)
            return True
    return False

def main():
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("점프 점프")

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 223, 0)
    PURPLE = (128, 0, 128)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)
    BROWN = (139, 69, 19)
    FLOOR_COLOR = (144, 228, 144)

    character_width, character_height = 20, 20
    character_x, character_y = 30, SCREEN_HEIGHT - character_height * 2
    character_speed = 6
    jump_speed = 20
    gravity = 1.4

    floor_height = 150
    floor_y = SCREEN_HEIGHT - floor_height

    platform_width, platform_height = 100, 20

    powerup_radius = 10
    enemy_width, enemy_height = 33, 33
    enemy_speed = 5

    current_stage = 1
    blocks, enemies, powerups, portal = init_stage(*stages[current_stage])

    second_block_x, second_block_y = 500, 350

    spike = Spike(505, floor_y - 1, 90, 20)

    clock = pygame.time.Clock()
    current_image = user_image
    is_jumping = False

    running = True
    vertical_momentum = 0
    is_on_ground = True
    space_pressed = False
    score = 0
    time_limit = 20
    start_ticks = pygame.time.get_ticks()
    current_image = user_image
    floor_removed = False

    while running:
        screen.fill(WHITE)
        character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = time_limit - seconds

        if check_spike_collision(character_rect, spike.rect) or check_collision(character_rect, enemies, enemy_width, enemy_height):
            character_x, character_y = 30, SCREEN_HEIGHT - character_height * 2
            blocks, enemies, powerups, portal = init_stage(*stages[current_stage])
            start_ticks = pygame.time.get_ticks()
            score = 0

        if time_left <= 0:
            choice = show_game_over_screen(screen, score)
            if choice == "restart":
                pass
            else:
                running = False

        if check_spike_collision(character_rect, spike):
            choice = show_game_over_screen(screen, score)
            if choice == "restart":
                pass
            else:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= character_speed
            if not is_on_ground:
                current_image = left_jump
            else:
                current_image = left_walk
        if keys[pygame.K_RIGHT]:
            character_x += character_speed
            if not is_on_ground:
                current_image = right_jump
            else:
                current_image = right_walk

        if space_pressed and is_on_ground:
            vertical_momentum = -jump_speed
            is_on_ground = False
            space_pressed = False

        character_x = max(0, min(SCREEN_WIDTH - character_width, character_x))
        vertical_momentum += gravity
        character_y += vertical_momentum
        character_y = min(character_y, floor_y - character_height)

        block_collided = check_collision(character_rect, blocks, platform_width, platform_height)
        if block_collided:
            if vertical_momentum > 0:
                character_y = block_collided.y - character_height
                vertical_momentum = 0
                floor_removed = True

        if character_y >= floor_y - character_height:
            character_y = floor_y - character_height
            vertical_momentum = 0
            is_on_ground = True

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
                character_x, character_y = character_width, SCREEN_HEIGHT - character_height * 2
                start_ticks = pygame.time.get_ticks()
            else:
                subprocess.run([sys.executable, "./KyoKwan/main_game.py"], check=True)
                running = False

        if floor_removed:
            remove_floor_section(blocks, second_block_x, platform_width)

        pygame.draw.rect(screen, (144, 228, 144), (0, floor_y, SCREEN_WIDTH, floor_height))

        pygame.draw.rect(screen, FLOOR_COLOR, (0, floor_y, SCREEN_WIDTH, floor_height))

        for block in blocks:
            screen.blit(block_image, (block.x, block.y))

        for enemy in enemies:
            pygame.draw.rect(screen, GREEN, (enemy.x, enemy.y, enemy_width, enemy_height))

        for powerup in powerups:
            pygame.draw.circle(screen, YELLOW, (powerup.x + powerup_radius, powerup.y + powerup_radius), powerup_radius)

        if portal:
            portal.draw(screen)

        pygame.draw.rect(screen, (0, 0, 0), spike.rect)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}  Time Left: {int(time_left)}", True, BLACK)
        screen.blit(text, (10, 10))

        current_image = pygame.transform.scale(current_image, (character_width, character_height))
        screen.blit(current_image, (character_x, character_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
