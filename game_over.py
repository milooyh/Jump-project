import pygame
import sys

def show_game_over_screen(screen, score):
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    restart_text = pygame.font.SysFont(None, 36).render("Press R to Restart", True, (0, 0, 0))
    quit_text = pygame.font.SysFont(None, 36).render("Press Q to Quit", True, (0, 0, 0))

    screen.fill((255, 255, 255))
    screen.blit(game_over_text, (screen.get_width()//2 - game_over_text.get_width()//2, screen.get_height()//2 - 100))
    screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2))
    screen.blit(restart_text, (screen.get_width()//2 - restart_text.get_width()//2, screen.get_height()//2 + 100))
    screen.blit(quit_text, (screen.get_width()//2 - quit_text.get_width()//2, screen.get_height()//2 + 150))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # 게임을 다시 시작
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
