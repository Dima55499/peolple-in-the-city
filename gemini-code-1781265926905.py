import pygame
import random
import sys

# --- INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("People on the City")
clock = pygame.time.Clock()

# --- COLORS ---
SKY_COLOR = (26, 12, 46)
STREET_COLOR = (51, 51, 51)
LINE_COLOR = (102, 102, 102)
PLAYER_COLOR = (0, 123, 255)  # Blue
CAR_COLOR = (255, 51, 51)     # Red
BUILDING_COLOR = (45, 30, 65)  # Dark purple/grey for background
TEXT_COLOR = (255, 255, 255)

# --- GAME VARIABLES ---
game_speed = 5
score = 0
game_over = False

# --- OBJECTS ---
# Player (Blue Man)
player_width, player_height = 30, 50
player_x, player_y = 100, 300
player_vy = 0
gravity = 0.6
jump_force = -13
is_jumping = False

# Obstacle (Car)
car_width, car_height = 60, 30
car_x = WIDTH + 100
car_y = 320

# Background Buildings (x_position, width, height)
buildings = [
    [50, 80, 200], [200, 120, 280],
    [400, 70, 180], [550, 100, 250],
    [750, 90, 220]
]

# Fonts
font = pygame.font.SysFont("Segoe UI", 24)
large_font = pygame.font.SysFont("Segoe UI", 40, bold=True)

def reset_game():
    global game_speed, score, game_over, player_y, player_vy, is_jumping, car_x
    game_speed = 5
    score = 0
    game_over = False
    player_y = 300
    player_vy = 0
    is_jumping = False
    car_x = WIDTH + random.randint(0, 300)

# --- MAIN GAME LOOP ---
while True:
    # 1. Handle Inputs (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                elif not is_jumping:
                    player_vy = jump_force
                    is_jumping = True
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            elif not is_jumping:
                player_vy = jump_force
                is_jumping = True

    if not game_over:
        # 2. Physics & Logic Updates
        
        # Player physics
        player_vy += gravity
        player_y += player_vy
        if player_y >= 300:
            player_y = 300
            player_vy = 0
            is_jumping = False

        # Move obstacle (Car)
        car_x -= game_speed
        if car_x + car_width < 0:
            car_x = WIDTH + random.randint(0, 400)
            score += 1
            game_speed += 0.2  # Make the game faster

        # Move buildings (Parallax Effect)
        for b in buildings:
            b[0] -= game_speed * 0.2
            if b[0] + b[1] < 0:
                b[0] = WIDTH

        # 3. Collision Detection
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        
        if player_rect.colliderect(car_rect):
            game_over = True

    # 4. Drawing Everything
    screen.fill(SKY_COLOR)  # Draw Sky

    # Draw Buildings
    for b in buildings:
        pygame.draw.rect(screen, BUILDING_COLOR, (b[0], HEIGHT - b[2], b[1], b[2]))

    # Draw Road
    pygame.draw.rect(screen, STREET_COLOR, (0, 350, WIDTH, 50))
    pygame.draw.rect(screen, LINE_COLOR, (0, 350, WIDTH, 4))

    # Draw Car (Body + Wheels)
    pygame.draw.rect(screen, CAR_COLOR, (car_x, car_y, car_width, car_height))
    pygame.draw.circle(screen, (0, 0, 0), (car_x + 15, car_y + 30), 8)
    pygame.draw.circle(screen, (0, 0, 0), (car_x + 45, car_y + 30), 8)

    # Draw Player (Body + Head)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height))
    pygame.draw.circle(screen, PLAYER_COLOR, (player_x + 15, player_y - 10), 10)

    # Draw Score & Title UI
    title_text = font.render("PEOPLE ON THE CITY", True, TEXT_COLOR)
    score_text = font.render(f"Scor: {score}", True, TEXT_COLOR)
    screen.blit(title_text, (20, 20))
    screen.blit(score_text, (WIDTH - 120, 20))

    # Draw Game Over Screen
    if game_over:
        # Dim background
        dim_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        
        # Game over texts
        over_text = large_font.render("AI FOST LOVIT!", True, (255, 51, 51))
        restart_text = font.render("Apasă SPACE sau Click pentru a juca din nou", True, TEXT_COLOR)
        
        screen.blit(over_text, (WIDTH // 2 - 140, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 190, HEIGHT // 2 + 30))

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)  # Caps game at 60 Frames Per Second