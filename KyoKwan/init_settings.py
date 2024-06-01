import pygame
import Map_1

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("점프 점프")

# 색깔
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FLOOR_COLOR = (144, 228, 144)
SPIKE_COLOR = (0, 0, 0)

# 캐릭터 속성
character_width, character_height = 25, 42
character_x, character_y = 30, SCREEN_HEIGHT - character_height * 2
character_speed = 6
jump_speed = 20
gravity = 1.4

# 캐릭터 이미지 로드
character_image = pygame.image.load('KyoKwan\User.png')
character_image = pygame.transform.scale(character_image, (character_width, character_height))

# 바닥 속성
floor_height = 40
floor_y = SCREEN_HEIGHT - floor_height

# 발판 속성
platform_width, platform_height = 50, 20
platform_color = BLUE

# 가시 속성 및 위치
spike_width, spike_height = 10, 20  # 이 부분 수정
spike_positions = [(x, floor_y - spike_height) for x in range(550, 600, spike_width)]

# 맵의 최대 크기
max_map_width = 1200

# 바닥 구멍 정보 로드
floor_holes = Map_1.floor_holes

# 포탈 속성
portal_position = Map_1.portal_position
portal_size = 70

# 포탈 이미지 로드
portal_image = pygame.image.load('KyoKwan\portal_image.png')
portal_image = pygame.transform.scale(portal_image, (portal_size, portal_size))
portal_angle = 0

# trick_hole 속성 추가
trick_hole_x, trick_hole_y = 700, floor_y
trick_hole_visible = False
trick_hole_speed = 2

# 점프 블록의 가로 길이 설정
jumping_block_width = platform_width + 100
