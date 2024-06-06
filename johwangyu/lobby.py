import pygame
import sys

def show_lobby_screen(screen_width, screen_height):
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("lobby")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FONT_SIZE = 60

    font = pygame.font.Font(None, FONT_SIZE)
    start_text = font.render("start", True, BLACK)
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

    quit_text = font.render("exit", True, BLACK)
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    return "start"
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    show_lobby_screen(800, 600)