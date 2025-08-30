import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

BACKGROUND_PATH = os.path.join(ASSETS_DIR, "background.png")
SNAKE_PATH = os.path.join(ASSETS_DIR, "snake.png")
APPLE_PATH = os.path.join(ASSETS_DIR, "apple.png")

# Screen settings
width, HEIGHT = 600, 400
win = pygame.display.set_mode((width, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

# Colors hai bhae
WHITE = (255, 255, 255)

# images load hongi 
background = pygame.image.load(BACKGROUND_PATH)
background = pygame.transform.scale(background, (width, HEIGHT))

snake_img = pygame.image.load(SNAKE_PATH)
snake_img = pygame.transform.scale(snake_img, (30, 30))  # Snake block size

apple_img = pygame.image.load(APPLE_PATH)
apple_img = pygame.transform.scale(apple_img, (40, 40))  # Bigger apple

# waqt
clock = pygame.time.Clock()
snake_speed = 8  # Slower snake

# Sanp settings
snake_block = 20
snake_list = []
snake_length = 1

# Font
font = pygame.font.SysFont("comicsansms", 25)

def message(msg, color, x, y):
    mesg = font.render(msg, True, color)
    win.blit(mesg, [x, y])

def game_loop():
    global snake_list, snake_length

    game_over = False
    x, y = width // 2, HEIGHT // 2
    dx, dy = 0, 0

    snake_list = []
    snake_length = 1

    apple_x = random.randrange(0, width - 30, 20)
    apple_y = random.randrange(0, HEIGHT - 30, 20)

    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -snake_block, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = snake_block, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -snake_block
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, snake_block

        x += dx
        y += dy

        # Wrap snake around screen instead of game over at border
        if x >= width:
            x = 0
        elif x < 0:
            x = width - snake_block
        if y >= HEIGHT:
            y = 0
        elif y < 0:
            y = HEIGHT - snake_block

        win.blit(background, (0, 0))
        win.blit(apple_img, (apple_x, apple_y))

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]
 
        # Check self collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        # Draw snake
        for block in snake_list:
            win.blit(snake_img, (block[0], block[1]))

        # Eating apple
        if x in range(apple_x - 10, apple_x + 30) and y in range(apple_y - 10, apple_y + 30):
            apple_x = random.randrange(0, width - 30, 20)
            apple_y = random.randrange(0, HEIGHT - 30, 20)
            snake_length += 1
            score += 1

        # Show score
        message(f"Score: {score}", WHITE, 10, 10)

        pygame.display.update()
        clock.tick(snake_speed)

    # Game over screen
    win.fill((0, 0, 0))
    message("Game Over! Press Q to Quit or R to Restart", WHITE, 50, HEIGHT//2)
    pygame.display.update()

    # Wait for user
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    game_loop()

# Start game
game_loop()
