import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X = 50
BIRD_Y = 300
GRAVITY = 0.6
JUMP_STRENGTH = -8  # Reduced jump strength
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_VELOCITY = -3

# Colors
WHITE = (255, 255, 255)
PIPE_COLORS = [(0, 200, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)]  # Green, Red, Blue, Orange
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 255, 0)

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load Bird Image
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))  # Resize bird

# Font
font = pygame.font.SysFont(None, 36)
high_score = 0  # High score variable

def welcome_screen():
    screen.fill((255, 192, 203))
    welcome_text = font.render("CREATE BY SHUBHAM", True, BLACK)
    screen.blit(welcome_text, (WIDTH // 10, HEIGHT // 2))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

welcome_screen()
def game_loop():
    global high_score
    bird_y = BIRD_Y
    bird_y_velocity = 0
    score = 0
    pipes = [(WIDTH, random.randint(50, HEIGHT - 250), random.choice(PIPE_COLORS), random.randint(150, 220))]
    running = True
    
    while running:
        screen.fill((255, 192, 203))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_velocity = JUMP_STRENGTH
        
        # Apply Gravity
        bird_y += bird_y_velocity
        bird_y_velocity += GRAVITY

        # Pipe Movement & Collision
        new_pipes = []
        for pipe_x, pipe_height, pipe_color, pipe_gap in pipes:
            pipe_x += PIPE_VELOCITY
            if pipe_x + PIPE_WIDTH > 0:
                new_pipes.append((pipe_x, pipe_height, pipe_color, pipe_gap))
                pygame.draw.rect(screen, pipe_color, (pipe_x, 0, PIPE_WIDTH, pipe_height))
                pygame.draw.rect(screen, pipe_color, (pipe_x, pipe_height + pipe_gap, PIPE_WIDTH, HEIGHT))
                
                # Collision Check
                if BIRD_X + 40 > pipe_x and BIRD_X < pipe_x + PIPE_WIDTH:
                    if bird_y < pipe_height or bird_y + 30 > pipe_height + pipe_gap:
                        running = False
        
        pipes = new_pipes
        
        # Generate New Pipe
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            pipes.append((WIDTH, random.randint(50, HEIGHT - 250), random.choice(PIPE_COLORS), random.randint(150, 220)))
            score += 1
            if score > high_score:
                high_score = score  # Update high score
        
        # Bird Drawing
        screen.blit(bird_img, (BIRD_X, int(bird_y)))

        # Score Display
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(high_score_text, (10, 40))
        
        pygame.display.update()
        clock.tick(30)
    
    game_over()

def game_over():
    pygame.quit()
    return
            
game_loop()
