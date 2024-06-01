import pygame
from init_settings import SCREEN_WIDTH, platform_width, platform_height, spike_width, spike_height  # 수정된 부분

class Block:
    def __init__(self, x, y, speed=0, cloud=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.cloud = cloud
        self.is_visible = True

    def move(self):
        if self.speed != 0:
            self.x += self.speed
            if self.x > SCREEN_WIDTH:
                self.is_visible = False

def load_map(map_module):
    blocks = [Block(x, y, cloud=(y == 260 and x in [100])) for x, y in map_module.blocks_positions]
    return blocks

def check_collision(character, blocks):
    for block in blocks:
        if block.is_visible and not block.cloud and character.colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
            return block
    return None

def check_bottom_collision(character, block):
    if block.cloud:
        if character.bottom >= block.y and character.top < block.y and character.right > block.x and character.left < block.x + platform_width:
            return True
    else:
        block_rect = pygame.Rect(block.x, block.y, platform_width, platform_height)
        if character.bottom >= block_rect.top and character.top < block_rect.top and character.right > block_rect.left and character.left < block_rect.right:
            return True
    return False

def check_top_collision(character, block):  # 이 함수 추가
    block_rect = pygame.Rect(block.x, block.y, platform_width, platform_height)
    if (character.top <= block_rect.bottom and character.bottom > block_rect.bottom and
            character.right > block_rect.left and character.left < block_rect.right):
        return True
    return False

def check_spike_collision(character, spikes):
    for spike in spikes:
        if character.colliderect(pygame.Rect(spike[0], spike[1], spike_width, spike_height)):
            return True
    return False

def check_trigger_zone_collision(character, trigger_zone):
    return character.colliderect(trigger_zone)

def check_falling_block_collision(character, block):
    block_rect = pygame.Rect(block.x, block.y, platform_width, platform_height)
    if character.colliderect(block_rect):
        return True
    return False

def check_portal_collision(character, portal_pos, portal_size):
    portal_rect = pygame.Rect(portal_pos[0], portal_pos[1], portal_size, portal_size)
    return character.colliderect(portal_rect)