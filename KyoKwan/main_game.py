import pygame
import sys
from init_settings import *
from game_objects import *

# 이미지 로드 및 크기 조정
left_walk = pygame.image.load('C:/OSSW4/Img/Left_W.png')
left_jump = pygame.image.load('C:/OSSW4/Img/Left_J.png')
right_walk = pygame.image.load('C:/OSSW4/Img/Right_W.png')
right_jump = pygame.image.load('C:/OSSW4/Img/Right_J.png')
user_image = pygame.image.load('C:/OSSW4/Img/User.png')
block_image = pygame.image.load('C:/OSSW4/Img/block.png')
falling_block_image = pygame.image.load('C:/OSSW4/Img/Block.png')
jump_block_image = pygame.image.load('C:/OSSW4/Img/jump.png')
floor_image = pygame.image.load('C:/OSSW4/Img/floor.png')
cloud_image = pygame.image.load('C:/OSSW4/Img/cloud.png')


left_walk = pygame.transform.scale(left_walk, (character_width, character_height))
left_jump = pygame.transform.scale(left_jump, (character_width, character_height))
right_walk = pygame.transform.scale(right_walk, (character_width, character_height))
right_jump = pygame.transform.scale(right_jump, (character_width, character_height))
user_image = pygame.transform.scale(user_image, (character_width, character_height))
block_image = pygame.transform.scale(block_image, (platform_width, platform_height))
falling_block_image = pygame.transform.scale(falling_block_image, (platform_width, platform_height))
jump_block_image = pygame.transform.scale(jump_block_image, (jumping_block_width, platform_height))
floor_image = pygame.transform.scale(floor_image, (800, 150))
cloud_image = pygame.transform.scale(cloud_image, (platform_width, platform_height))

map_modules = [Map_1]
current_map_index = 0
blocks = load_map(map_modules[current_map_index])

del_block_1 = pygame.Rect(220, 350, 100, 100)
add_block_1 = pygame.Rect(50, 340, 30, 30)
trigger_moving_block_zone = pygame.Rect(160, 220, 30, 30)
trigger_falling_block_zone = pygame.Rect(800, 320, 50, 10)
trigger_zone = pygame.Rect(680, 510, 240, 50)
spike_trigger_zone = pygame.Rect(540, 455, 20, 100)
jumping_block = Block(1050, 450)
jumping_block.is_visible = False
jumping_trigger_zone = pygame.Rect(1050, 400, 150, 20)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

block_spawn_time = 0
block_spawn_delay = 2

falling_block = Block(800, 0, speed=10)
falling_block.is_visible = False

attempt_count = 0

# 텔레포트 효과를 위한 변수들
teleporting = False
teleport_frames = 60
teleport_frame_count = 0
teleport_initial_position = (0, 0)
teleport_final_position = (1000, 540)

def check_spike_collision(character_rect, spikes):
    for spike in spikes:
        spike_rect = pygame.Rect(spike[0], spike[1], spike_width, spike_height)
        if character_rect.colliderect(spike_rect):
            return True
    return False

def load_next_map():
    global current_map_index, character_x, character_y, blocks, camera_x
    current_map_index += 1
    if current_map_index < len(map_modules):
        character_x, character_y = 30, SCREEN_HEIGHT - character_height * 2
        camera_x = 0
        blocks = load_map(map_modules[current_map_index])
    else:
        pygame.quit()
        sys.exit()

def reset_game():
    global character_x, character_y, vertical_momentum, is_on_ground, blocks, additional_block_added_1, additional_block_added_2, moving_block_triggered, block_spawn_time, block_spawned, camera_x, trick_hole_visible, trick_hole_y, falling_block, spike_height, spike_positions, spike_triggered, on_jumping_block, jump_timer, down_key_count, attempt_count
    attempt_count += 1
    character_x, character_y = 30, SCREEN_HEIGHT - character_height * 2
    vertical_momentum = 0
    is_on_ground = True
    additional_block_added_1 = False
    additional_block_added_2 = False
    moving_block_triggered = False
    block_spawn_time = 0
    block_spawned = False
    camera_x = 0
    blocks = load_map(map_modules[current_map_index])
    for block in blocks:
        block.is_visible = True
    trick_hole_visible = False
    trick_hole_y = floor_y
    falling_block = Block(800, 0, speed=10)
    falling_block.is_visible = False
    spike_height = 20
    spike_positions = [(x, floor_y - spike_height) for x in range(550, 600, spike_width)]
    spike_triggered = False
    jumping_block.is_visible = False
    on_jumping_block = False
    jump_timer = 0
    down_key_count = 0

running = True
vertical_momentum = 0
is_on_ground = True
space_pressed = False
additional_block_added_1 = False
additional_block_added_2 = False
moving_block_triggered = False
block_spawned = False
camera_x = 0
on_jumping_block = False
jump_timer = 0
down_key_count = 0
teleport_zone = pygame.Rect(5, 540, 10, 10)

while running:
    screen.fill(WHITE)
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True
            if event.key == pygame.K_DOWN:
                if teleport_zone.colliderect(character_rect):
                    down_key_count += 1
                    if down_key_count >= 20 and not teleporting:
                        teleporting = True
                        teleport_frame_count = 0
                        teleport_initial_position = (character_x, character_y)
                else:
                    down_key_count = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    if not teleporting:
        keys = pygame.key.get_pressed()
        character_image = user_image

        if keys[pygame.K_LEFT]:
            character_x -= character_speed
            if not is_on_ground:
                character_image = left_jump
            else:
                character_image = left_walk

        if keys[pygame.K_RIGHT]:
            character_x += character_speed
            if not is_on_ground:
                character_image = right_jump
            else:
                character_image = right_walk

        character_x = max(0, character_x)
        character_x = min(character_x, max_map_width - character_width)

        if space_pressed and is_on_ground:
            vertical_momentum = -jump_speed
            is_on_ground = False

        if not on_jumping_block:
            vertical_momentum += gravity
        character_y += vertical_momentum

        if character_y > SCREEN_HEIGHT:
            reset_game()

        is_on_ground = False
        if character_y >= floor_y - character_height:
            is_in_hole = False
            for hole_start, hole_end in floor_holes:
                if hole_start < character_x < hole_end:
                    is_in_hole = True
                    break

            if not is_in_hole:
                character_y = floor_y - character_height
                vertical_momentum = 0
                is_on_ground = True

        if character_x > SCREEN_WIDTH // 2:
            camera_x = character_x - SCREEN_WIDTH // 2
            camera_x = min(camera_x, max_map_width - SCREEN_WIDTH)
        else:
            camera_x = 0

        pygame.draw.rect(screen, FLOOR_COLOR, (0 - camera_x, floor_y, max_map_width, floor_height))
        for hole_start, hole_end in floor_holes:
            pygame.draw.rect(screen, WHITE, (hole_start - camera_x, floor_y, hole_end - hole_start, floor_height))

        if trick_hole_visible:
            pygame.draw.rect(screen, WHITE, (trick_hole_x - camera_x, trick_hole_y, 30, floor_height))
            if trick_hole_y < SCREEN_HEIGHT:
                trick_hole_y += trick_hole_speed
        else:
            pygame.draw.rect(screen, FLOOR_COLOR, (trick_hole_x - camera_x, floor_y, 220, floor_height))

        if check_trigger_zone_collision(character_rect, trigger_falling_block_zone):
            falling_block.is_visible = True

        if falling_block.is_visible:
            falling_block.y += falling_block.speed
            pygame.draw.rect(screen, platform_color, (falling_block.x - camera_x, falling_block.y, platform_width, platform_height))

        if check_falling_block_collision(character_rect, falling_block):
            reset_game()

        block_collided = check_collision(character_rect, blocks)
        if block_collided:
            if vertical_momentum > 0:
                character_y = block_collided.y - character_height
                vertical_momentum = 0
                is_on_ground = True
            elif check_top_collision(character_rect, block_collided):
                character_y = block_collided.y + platform_height
                vertical_momentum = gravity
                is_on_ground = False

        if check_spike_collision(character_rect, spike_positions):
            reset_game()

        if check_trigger_zone_collision(character_rect, trigger_zone):
            trick_hole_visible = True

        if check_trigger_zone_collision(character_rect, del_block_1):
            blocks[1].is_visible = False

        if check_trigger_zone_collision(character_rect, trigger_moving_block_zone) and not moving_block_triggered and not block_spawned:
            block_spawn_time = pygame.time.get_ticks()
            moving_block_triggered = True

        if moving_block_triggered and not block_spawned and (pygame.time.get_ticks() - block_spawn_time) >= block_spawn_delay * 400:
            moving_block = Block(-platform_width, 230, speed=9)
            blocks.append(moving_block)
            block_spawned = True

        if character_rect.colliderect(add_block_1) and not additional_block_added_1:
            blocks.append(Block(50, 375))
            additional_block_added_1 = True

        if character_rect.colliderect(jumping_trigger_zone):
            jumping_block.is_visible = True

        if jumping_block.is_visible:
            pygame.draw.rect(screen, platform_color, (jumping_block.x - camera_x, jumping_block.y, jumping_block_width, platform_height))
            if character_rect.colliderect(pygame.Rect(jumping_block.x, jumping_block.y, jumping_block_width, platform_height)):
                on_jumping_block = True
                jump_timer = pygame.time.get_ticks()

        if on_jumping_block:
            elapsed_time = pygame.time.get_ticks() - jump_timer
            if elapsed_time < 2000:
                vertical_momentum = -5
            else:
                reset_game()

        for block in blocks:
            if block.speed != 0:
                block.move()
                if block.is_visible and character_rect.colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
                    reset_game()
                    
        screen.blit(cloud_image, (550 - camera_x, 210))
        screen.blit(cloud_image, (1000 - camera_x, 500))
    
        for block in blocks:
            if block.is_visible:
                if (block.x, block.y) == (100, 260) or (block.x, block.y) == (160, 260) :
                    screen.blit(cloud_image, (block.x - camera_x, block.y))
                else:
                    screen.blit(block_image, (block.x - camera_x, block.y))
                
        if falling_block.is_visible:
            screen.blit(falling_block_image, (falling_block.x - camera_x, falling_block.y))
            
        if jumping_block.is_visible:
            screen.blit(jump_block_image, (jumping_block.x - camera_x, jumping_block.y))   

        if check_trigger_zone_collision(character_rect, spike_trigger_zone):
            spike_height = 110
            spike_positions = [(x, floor_y - spike_height) for x in range(550, 580, spike_width)]

        for spike in spike_positions:
            pygame.draw.rect(screen, SPIKE_COLOR, (spike[0] - camera_x, spike[1], spike_width, spike_height))

        # pygame.draw.rect(screen, (0, 255, 0), trigger_falling_block_zone.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 0, 0), del_block_1.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 255, 0), add_block_1.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 0, 255), trigger_moving_block_zone.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 255, 0), trigger_zone.move(-camera_x, 0), 2)
        #pygame.draw.rect(screen, (0, 0, 255), spike_trigger_zone.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (255, 0, 0), teleport_zone, 2)

        portal_angle += 2
        rotated_portal_image = pygame.transform.rotate(portal_image, portal_angle)
        portal_rect = rotated_portal_image.get_rect(center=(portal_position[0] - camera_x + portal_size // 2, portal_position[1] + portal_size // 2))
        screen.blit(rotated_portal_image, portal_rect.topleft)

        if check_portal_collision(character_rect, portal_position, portal_size):
            load_next_map()

        screen.blit(character_image, (character_x - camera_x, character_y))

        attempt_text = font.render(f"Die: {attempt_count}", True, RED)
        screen.blit(attempt_text, (10, 10))

    else:
        # 맵을 유지하면서 텔레포트 애니메이션
        keys = pygame.key.get_pressed()
        character_image = user_image

        if keys[pygame.K_LEFT]:
            character_x -= character_speed
            if not is_on_ground:
                character_image = left_jump
            else:
                character_image = left_walk

        if keys[pygame.K_RIGHT]:
            character_x += character_speed
            if not is_on_ground:
                character_image = right_jump
            else:
                character_image = right_walk

        character_x = max(0, character_x)
        character_x = min(character_x, max_map_width - character_width)

        if space_pressed and is_on_ground:
            vertical_momentum = -jump_speed
            is_on_ground = False

        if not on_jumping_block:
            vertical_momentum += gravity
        character_y += vertical_momentum

        if character_y > SCREEN_HEIGHT:
            reset_game()

        is_on_ground = False
        if character_y >= floor_y - character_height:
            is_in_hole = False
            for hole_start, hole_end in floor_holes:
                if hole_start < character_x < hole_end:
                    is_in_hole = True
                    break

            if not is_in_hole:
                character_y = floor_y - character_height
                vertical_momentum = 0
                is_on_ground = True

        if character_x > SCREEN_WIDTH // 2:
            camera_x = character_x - SCREEN_WIDTH // 2
            camera_x = min(camera_x, max_map_width - SCREEN_WIDTH)
        else:
            camera_x = 0

        pygame.draw.rect(screen, FLOOR_COLOR, (0 - camera_x, floor_y, max_map_width, floor_height))
        for hole_start, hole_end in floor_holes:
            pygame.draw.rect(screen, WHITE, (hole_start - camera_x, floor_y, hole_end - hole_start, floor_height))

        if trick_hole_visible:
            pygame.draw.rect(screen, WHITE, (trick_hole_x - camera_x, trick_hole_y, 30, floor_height))
            if trick_hole_y < SCREEN_HEIGHT:
                trick_hole_y += trick_hole_speed
        else:
            pygame.draw.rect(screen, FLOOR_COLOR, (trick_hole_x - camera_x, floor_y, 220, floor_height))

        if check_trigger_zone_collision(character_rect, trigger_falling_block_zone):
            falling_block.is_visible = True

        if falling_block.is_visible:
            falling_block.y += falling_block.speed
            pygame.draw.rect(screen, platform_color, (falling_block.x - camera_x, falling_block.y, platform_width, platform_height))

        if check_falling_block_collision(character_rect, falling_block):
            reset_game()

        block_collided = check_collision(character_rect, blocks)
        if block_collided:
            if vertical_momentum > 0:
                character_y = block_collided.y - character_height
                vertical_momentum = 0
                is_on_ground = True
            elif check_top_collision(character_rect, block_collided):
                character_y = block_collided.y + platform_height
                vertical_momentum = gravity
                is_on_ground = False

        if check_spike_collision(character_rect, spike_positions):
            reset_game()

        if check_trigger_zone_collision(character_rect, trigger_zone):
            trick_hole_visible = True

        if check_trigger_zone_collision(character_rect, del_block_1):
            blocks[1].is_visible = False

        if check_trigger_zone_collision(character_rect, trigger_moving_block_zone) and not moving_block_triggered and not block_spawned:
            block_spawn_time = pygame.time.get_ticks()
            moving_block_triggered = True

        if moving_block_triggered and not block_spawned and (pygame.time.get_ticks() - block_spawn_time) >= block_spawn_delay * 400:
            moving_block = Block(-platform_width, 230, speed=9)
            blocks.append(moving_block)
            block_spawned = True

        if character_rect.colliderect(add_block_1) and not additional_block_added_1:
            blocks.append(Block(50, 375))
            additional_block_added_1 = True

        if character_rect.colliderect(jumping_trigger_zone):
            jumping_block.is_visible = True

        if jumping_block.is_visible:
            pygame.draw.rect(screen, platform_color, (jumping_block.x - camera_x, jumping_block.y, jumping_block_width, platform_height))
            if character_rect.colliderect(pygame.Rect(jumping_block.x, jumping_block.y, jumping_block_width, platform_height)):
                on_jumping_block = True
                jump_timer = pygame.time.get_ticks()

        if on_jumping_block:
            elapsed_time = pygame.time.get_ticks() - jump_timer
            if elapsed_time < 2000:
                vertical_momentum = -5
            else:
                reset_game()

        for block in blocks:
            if block.speed != 0:
                block.move()
                if block.is_visible and character_rect.colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
                    reset_game()

        for block in blocks:
            if block.is_visible:
                pygame.draw.rect(screen, platform_color, (block.x - camera_x, block.y, platform_width, platform_height))
                screen.blit(block_image, (block.x - camera_x, block.y))

        if falling_block.is_visible:
            screen.blit(falling_block_image, (falling_block.x - camera_x, falling_block.y))
            
        if jumping_block.is_visible:
            screen.blit(jump_block_image, (jumping_block.x - camera_x, jumping_block.y))   
            
        if check_trigger_zone_collision(character_rect, spike_trigger_zone):
            spike_height = 110
            spike_positions = [(x, floor_y - spike_height) for x in range(550, 600, spike_width)]

        for spike in spike_positions:
            pygame.draw.rect(screen, SPIKE_COLOR, (spike[0] - camera_x, spike[1], spike_width, spike_height))

        # pygame.draw.rect(screen, (0, 255, 0), trigger_falling_block_zone.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 0, 0), del_block_1.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 255, 0), add_block_1.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 0, 255), trigger_moving_block_zone.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 255, 0), trigger_zone.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (0, 0, 255), spike_trigger_zone.move(-camera_x, 0), 2)
        # pygame.draw.rect(screen, (255, 0, 0), teleport_zone, 2)

        portal_angle += 2
        rotated_portal_image = pygame.transform.rotate(portal_image, portal_angle)
        portal_rect = rotated_portal_image.get_rect(center=(portal_position[0] - camera_x + portal_size // 2, portal_position[1] + portal_size // 2))
        screen.blit(rotated_portal_image, portal_rect.topleft)

        if check_portal_collision(character_rect, portal_position, portal_size):
            load_next_map()

        screen.blit(character_image, (character_x - camera_x, character_y))
        screen.blit(cloud_image, (550 - camera_x, 210))
        screen.blit(cloud_image, (1000 - camera_x, 500))
        attempt_text = font.render(f"Die: {attempt_count}", True, RED)
        
        screen.blit(attempt_text, (10, 10))
        
        for block in blocks:
            if block.is_visible:
                if (block.x, block.y) == (100, 260) or (block.x, block.y) == (160, 260) :
                    screen.blit(cloud_image, (block.x - camera_x, block.y))
                else:
                    screen.blit(block_image, (block.x - camera_x, block.y))
                    
        # 텔레포트 애니메이션
        teleport_frame_count += 1
        angle = 360 * (teleport_frame_count / teleport_frames)
        scale = 1 - 0.9 * (teleport_frame_count / teleport_frames)
        if teleport_frame_count >= teleport_frames // 2:
            scale = 0.1 + 0.9 * ((teleport_frame_count - teleport_frames // 2) / (teleport_frames // 2))
            character_x, character_y = teleport_final_position

        transformed_character_image = pygame.transform.rotozoom(user_image, angle, scale)
        screen.blit(transformed_character_image, (character_x - camera_x - transformed_character_image.get_width() // 2 + character_width // 2, character_y - transformed_character_image.get_height() // 2 + character_height // 2))

        if teleport_frame_count >= teleport_frames:
            teleporting = False
            down_key_count = 0

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()


#