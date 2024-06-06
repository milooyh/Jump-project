import pygame

def show_game_over(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Press 'R' to Restart", True, (255, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 'R' 키를 누르면 재시작
                    return

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height()))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))

        pygame.display.update()