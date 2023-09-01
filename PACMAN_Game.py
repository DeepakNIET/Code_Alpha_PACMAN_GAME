import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

# Colors
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Set up game objects
pacman_x, pacman_y = width // 2, height // 2
food_positions = [(100, 100), (200, 200), (300, 300)]
ghost_positions = [(50, 50), (400, 300)]
ghost_speeds = [(2, 2), (-2, -2)]  # Ghost movement speeds

game_over = False  # Tracks game over state
score = 0
highest_score = 0

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        # Move Pac-Man
        if keys[pygame.K_LEFT]:
            pacman_x -= 5
        if keys[pygame.K_RIGHT]:
            pacman_x += 5
        if keys[pygame.K_UP]:
            pacman_y -= 5
        if keys[pygame.K_DOWN]:
            pacman_y += 5

        # Boundary checks to prevent Pac-Man from crossing the borders
        pacman_x = max(0, min(pacman_x, width - 32))
        pacman_y = max(0, min(pacman_y, height - 32))

        # Check for collisions with ghosts
        for i, ghost_pos in enumerate(ghost_positions):
            ghost_positions[i] = (
                ghost_positions[i][0] + ghost_speeds[i][0],
                ghost_positions[i][1] + ghost_speeds[i][1]
            )

            if ghost_positions[i][0] <= 0 or ghost_positions[i][0] >= width - 32:
                ghost_speeds[i] = (-ghost_speeds[i][0], ghost_speeds[i][1])
            if ghost_positions[i][1] <= 0 or ghost_positions[i][1] >= height - 32:
                ghost_speeds[i] = (ghost_speeds[i][0], -ghost_speeds[i][1])

            if pygame.Rect(pacman_x, pacman_y, 32, 32).colliderect(pygame.Rect(ghost_pos[0], ghost_pos[1], 32, 32)):
                game_over = True

        # Check for collisions with food
        eaten_food = []
        for food_pos in food_positions.copy():
            if pygame.Rect(pacman_x, pacman_y, 32, 32).colliderect(pygame.Rect(food_pos[0], food_pos[1], 16, 16)):
                eaten_food.append(food_pos)
                score += 10

        for food_pos in eaten_food:
            food_positions.remove(food_pos)

        # Spawn new food if all food is eaten
        if not food_positions:
            new_food_x = random.randint(0, width - 16)
            new_food_y = random.randint(0, height - 16)
            food_positions.append((new_food_x, new_food_y))

    # Update highest score
    if score > highest_score:
        highest_score = score

    # Update the display
    screen.fill(black)
    pygame.draw.circle(screen, yellow, (pacman_x, pacman_y), 16)
    for food_pos in food_positions:
        pygame.draw.circle(screen, yellow, food_pos, 8)
    for ghost_pos in ghost_positions:
        pygame.draw.rect(screen, blue, pygame.Rect(ghost_pos[0], ghost_pos[1], 32, 32))

    if game_over:
        # Display game over text and restart option
        text = font.render("Game Over! Press 'R' to Restart", True, yellow)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game state
            pacman_x, pacman_y = width // 2, height // 2
            food_positions = [(100, 100), (200, 200), (300, 300)]
            ghost_positions = [(50, 50), (400, 300)]
            score = 0
            game_over = False

    # Display scores
    score_text = font.render(f"Score: {score}", True, white)
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(highest_score_text, (10, 40))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
