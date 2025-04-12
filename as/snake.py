import pygame
import time
import random
import math

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)
purple = (128, 0, 128)
gray = (200, 200, 200)  # Grid color
light_blue = (173, 216, 230)  # Light blue for gradient background

# Set display dimensions
display_width = 800
display_height = 600

# Create display
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game with Power-Ups & Obstacles')

# Set game clock
clock = pygame.time.Clock()

# Snake block size and speed
snake_block = 10
initial_snake_speed = 15
snake_speed = initial_snake_speed

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render(f"Score: {score}", True, black)
    dis.blit(value, [0, 0])

def draw_gradient_background():
    """Draws a gradient background."""
    for y in range(display_height):
        color = (
            int(135 + (y / display_height) * 120),  # Red channel
            int(206 - (y / display_height) * 50),  # Green channel
            int(250 - (y / display_height) * 50)   # Blue channel
        )
        pygame.draw.line(dis, color, (0, y), (display_width, y))

def our_snake(snake_block, snake_list, color):
    """Draws a snake using circles instead of rectangles."""
    for x in snake_list:
        pygame.draw.circle(dis, color, (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 2)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])

def draw_grid():
    """Draws a grid on the background."""
    for x in range(0, display_width, snake_block):  # Vertical lines
        pygame.draw.line(dis, gray, (x, 0), (x, display_height))
    for y in range(0, display_height, snake_block):  # Horizontal lines
        pygame.draw.line(dis, gray, (0, y), (display_width, y))

def gameLoop():
    global snake_speed
    
    game_over = False
    game_close = False

    # Starting position for Player 1
    x1 = display_width / 2
    y1 = display_height / 2
    x1_change = 0
    y1_change = 0

    # Snake body
    snake_List = []
    Length_of_snake = 1

    # Food position and types
    food_types = [
        {"color": red, "effect": "normal", "points": 1},  # Normal food
        {"color": yellow, "effect": "golden", "points": 2},  # Golden food
        {"color": purple, "effect": "poison", "points": -1},  # Poison food
        {"color": blue, "effect": "teleport", "points": 1}  # Teleport food
    ]
    current_food = random.choice(food_types)
    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    # Power-ups
    powerups = []
    powerup_types = [
        {"color": (0, 255, 255), "effect": "speed_boost", "duration": 5},  # Speed boost (cyan)
        {"color": (255, 100, 100), "effect": "slow_down", "duration": 5},  # Slow down (light red)
        {"color": (255, 255, 255), "effect": "invincible", "duration": 5},  # Invincible (white)
        {"color": (255, 215, 0), "effect": "double_points", "duration": 5},  # Double points (gold)
        {"color": (200, 0, 200), "effect": "shrink", "duration": 0}  # Shrink (magenta)
    ]
    active_powerups = {}
    powerup_spawn_time = 0

    # Obstacles
    obstacles = []
    for _ in range(5):  # Generate 5 random obstacles
        obstacle_x = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
        obstacle_y = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
        obstacles.append([obstacle_x, obstacle_y])

    # Moving obstacles
    moving_obstacles = []
    for _ in range(3):  # Generate 3 moving obstacles
        moving_x = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
        moving_y = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
        moving_obstacles.append([moving_x, moving_y, random.choice([-snake_block, snake_block]), random.choice([-snake_block, snake_block])])

    # Bullets
    bullets = []

    # Game state
    score_multiplier = 1
    invincible = False
    last_powerup_time = 0

    while not game_over:
        current_time = time.time()

        while game_close:
            draw_gradient_background()
            draw_grid()
            message("Game Over! Press Q-Quit or C-Play Again", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Player controls
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_SPACE:  # Shoot bullet
                    bullets.append([x1, y1, x1_change, y1_change])

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Check boundary collisions (unless invincible)
        if not invincible:
            if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
                game_close = True

        # Wrap around if invincible
        if invincible:
            if x1 >= display_width:
                x1 = 0
            elif x1 < 0:
                x1 = display_width - snake_block
            if y1 >= display_height:
                y1 = 0
            elif y1 < 0:
                y1 = display_height - snake_block

        # Draw gradient background and grid
        draw_gradient_background()
        draw_grid()

        # Draw food
        pygame.draw.rect(dis, current_food["color"], [foodx, foody, snake_block, snake_block])

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(dis, (100, 100, 100), [obstacle[0], obstacle[1], snake_block, snake_block])

        # Update and draw moving obstacles
        for obstacle in moving_obstacles:
            obstacle[0] += obstacle[2]
            obstacle[1] += obstacle[3]
            # Bounce off walls
            if obstacle[0] >= display_width or obstacle[0] < 0:
                obstacle[2] *= -1
            if obstacle[1] >= display_height or obstacle[1] < 0:
                obstacle[3] *= -1
            pygame.draw.rect(dis, (150, 150, 150), [obstacle[0], obstacle[1], snake_block, snake_block])

        # Spawn power-ups occasionally
        if current_time - powerup_spawn_time > 10 and random.random() < 0.02:  # ~2% chance per frame after 10 seconds
            powerup_x = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            powerup_y = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            powerups.append([powerup_x, powerup_y, random.choice(powerup_types), current_time])
            powerup_spawn_time = current_time

        # Draw power-ups
        for powerup in powerups[:]:
            pygame.draw.rect(dis, powerup[2]["color"], [powerup[0], powerup[1], snake_block, snake_block])
            # Remove power-ups after 5 seconds if not collected
            if current_time - powerup[3] > 5:
                powerups.remove(powerup)

        # Update snake body
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check self-collisions (unless invincible)
        if not invincible:
            for segment in snake_List[:-1]:
                if segment == snake_Head:
                    game_close = True

        # Check collision with obstacles
        for obstacle in obstacles + [[obs[0], obs[1]] for obs in moving_obstacles]:
            if x1 == obstacle[0] and y1 == obstacle[1] and not invincible:
                game_close = True

        # Draw snake
        snake_color = green
        if invincible:
            snake_color = (255, 255, 255)  # White when invincible
        our_snake(snake_block, snake_List, snake_color)

        # Update and draw bullets
        new_bullets = []
        for bullet in bullets:
            bullet[0] += bullet[2] * 2  # Bullets move faster
            bullet[1] += bullet[3] * 2
            if 0 <= bullet[0] < display_width and 0 <= bullet[1] < display_height:
                new_bullets.append(bullet)
                pygame.draw.rect(dis, yellow, [bullet[0], bullet[1], 5, 5])
        bullets = new_bullets

        # Check food collisions
        if x1 == foodx and y1 == foody:
            # Apply food effect
            if current_food["effect"] == "normal":
                Length_of_snake += current_food["points"]
            elif current_food["effect"] == "golden":
                Length_of_snake += current_food["points"]
            elif current_food["effect"] == "poison":
                Length_of_snake += current_food["points"]
                if Length_of_snake < 1:
                    game_close = True
            elif current_food["effect"] == "teleport":
                Length_of_snake += current_food["points"]
                x1 = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
                y1 = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
                snake_List = [[x1, y1]]  # Reset snake to avoid self-collision
            
            # Spawn new food
            current_food = random.choice(food_types)
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

        # Check power-up collisions
        for powerup in powerups[:]:
            if x1 == powerup[0] and y1 == powerup[1]:
                effect = powerup[2]["effect"]
                if effect == "speed_boost":
                    snake_speed = initial_snake_speed * 2
                    active_powerups["speed_boost"] = current_time + powerup[2]["duration"]
                elif effect == "slow_down":
                    snake_speed = initial_snake_speed // 2
                    active_powerups["slow_down"] = current_time + powerup[2]["duration"]
                elif effect == "invincible":
                    invincible = True
                    active_powerups["invincible"] = current_time + powerup[2]["duration"]
                elif effect == "double_points":
                    score_multiplier = 2
                    active_powerups["double_points"] = current_time + powerup[2]["duration"]
                elif effect == "shrink":
                    Length_of_snake = max(1, Length_of_snake // 2)
                powerups.remove(powerup)

        # Check active power-ups
        for effect in list(active_powerups.keys()):
            if current_time > active_powerups[effect]:
                if effect == "speed_boost":
                    snake_speed = initial_snake_speed
                elif effect == "slow_down":
                    snake_speed = initial_snake_speed
                elif effect == "invincible":
                    invincible = False
                elif effect == "double_points":
                    score_multiplier = 1
                del active_powerups[effect]

        # Display score
        your_score((Length_of_snake - 1) * score_multiplier)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()