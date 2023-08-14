import pygame
import random

pygame.init()

# Set up display
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake initial position and speed
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_speed = 15

# Food position
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
food_spawn = True

# Obstacles
obstacles = []
for _ in range(10):  # Add 10 obstacles
    obstacle_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
    obstacles.append(obstacle_pos)

# Direction
direction = 'RIGHT'
change_to = direction

# Score
score = 0

# Game Over
game_over = False

# Main function
def gameLoop():
    global change_to
    global direction
    global snake_speed
    global snake_pos
    global snake_body
    global food_pos
    global food_spawn
    global score
    global game_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))

        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
            food_spawn = True

        # Draw Snake
        win.fill(WHITE)
        for pos in snake_body:
            pygame.draw.rect(win, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw Food
        pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Draw obstacles
        for pos in obstacles:
            pygame.draw.rect(win, RED, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        win.blit(text, (10, 10))

        # Game Over conditions
        if (
            snake_pos[0] < 0 or snake_pos[0] > WIDTH or
            snake_pos[1] < 0 or snake_pos[1] > HEIGHT or
            check_collision(snake_pos, snake_body) or
            snake_pos in obstacles
        ):
            game_over = True

        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

    # Game Over screen
    show_game_over_screen()

def check_collision(snake_pos, snake_body):
    if snake_pos in snake_body[1:]:
        return True
    return False

def reset_game():
    global game_over
    global snake_pos
    global snake_body
    global direction
    global change_to
    global score

    game_over = False
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0

def show_game_over_screen():
    global game_over
    global snake_pos
    global snake_body
    global direction
    global change_to
    global score

    while True:
        win.fill(WHITE)
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, BLACK)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Your Score: {score}", True, BLACK)
        win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 30))

        restart_text = font.render("Press SPACE to Restart", True, BLACK)
        win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    gameLoop()  # Restart the game loop

# Start the game loop
gameLoop()
