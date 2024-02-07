import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivors")

# Placeholder colors
BACKGROUND_COLOR = (0, 0, 0)     # Black
PLAYER_COLOR = (255, 0, 0)       # Red
ENEMY_COLOR = (0, 0, 255)        # Blue
DOOR_COLOR = (0, 255, 0)         # Green
TRIANGLE_COLOR = (255, 255, 0)   # Yellow
CIRCLE_COLOR = (255, 255, 255)   # White
HP_BAR_COLOR = (255, 0, 0)       # Green
HP_BAR_COLOR2 = (100, 0, 0)       # Green
EXP_BAR_COLOR_LIGHT = (0, 200, 255)    # Exp Blue
EXP_BAR_COLOR_MEDIUM = (0, 130, 255)    # Exp Blue
EXP_BAR_COLOR_DARK = (0, 65, 125)    # Exp Blue

# Game constants
PLAYER_SIZE = 50
ENEMY_SIZE = 50
DOOR_SIZE = 50
TRIANGLE_SIZE = 50
CIRCLE_RADIUS = 100
MAX_HP = 3
ENEMY_SPAWN_INTERVAL = 1  # Spawn an enemy every 1 second
DOOR_SPAWN_INTERVAL = 5  # Spawn a door every 5 seconds
MAX_ENEMIES_PER_DOOR = 4
CIRCLE_DAMAGE_INTERVAL = 1000  # Damage enemies every 1 second
EXP_BOX = 1  # Experience gained from defeating a box enemy
EXP_TRIANGLE = 2  # Experience gained from defeating a triangle enemy
EXP_TO_LEVEL_UP_BASE = 10  # Experience required to level up initially
EXP_TO_LEVEL_UP_INCREMENT = 5  # Increase in experience required to level up per level

# Player position
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT // 2 - PLAYER_SIZE // 2

# Player movement
move_left = False
move_right = False
move_up = False
move_down = False

# Enemies
enemy_speed = 5
enemies = []

# Triangle enemy
triangle_enemy_speed = 3
triangle_enemy_x = -TRIANGLE_SIZE
triangle_enemy_y = random.randint(0, HEIGHT - TRIANGLE_SIZE)
triangle_enemy_direction = (1, 0)

# Doors
doors = []

# Health Points (HP)
hp = MAX_HP
ENEMY_BOX_HP = 2
ENEMY_TRIANGLE_HP = 4

# Circle timer
last_circle_damage_time = 0

# Game state
game_state = "menu"

clock = pygame.time.Clock()
last_enemy_spawn_time = 0
last_door_spawn_time = 0
last_hit_time = 0
start_time = 0

# Camera
camera_x = 0
camera_y = 0

# Experience
exp = 0
level = 1
exp_to_level_up = EXP_TO_LEVEL_UP_BASE

def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 36)
    title_text = font.render("Vampire Survivors", True, (255, 255, 255))
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title_text, title_text_rect)
    start_text = font.render("Press SPACE to start", True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(start_text, start_text_rect)
    pygame.display.flip()

def draw_game():
    # Draw the background
    screen.fill(BACKGROUND_COLOR)

    # Calculate the camera position
    camera_x = player_x - WIDTH // 2
    camera_y = player_y - HEIGHT // 2

    # Draw the player
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x - camera_x, player_y - camera_y, PLAYER_SIZE, PLAYER_SIZE))

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy["x"] - camera_x, enemy["y"] - camera_y, ENEMY_SIZE, ENEMY_SIZE))

    # Draw the doors
    for door in doors:
        pygame.draw.rect(screen, DOOR_COLOR, (door["x"] - camera_x, door["y"] - camera_y, DOOR_SIZE, DOOR_SIZE))

    # Draw the triangle enemy
    pygame.draw.polygon(screen, TRIANGLE_COLOR, [
        (triangle_enemy_x - camera_x + TRIANGLE_SIZE // 2, triangle_enemy_y - camera_y),
        (triangle_enemy_x - camera_x, triangle_enemy_y - camera_y + TRIANGLE_SIZE),
        (triangle_enemy_x - camera_x + TRIANGLE_SIZE, triangle_enemy_y - camera_y + TRIANGLE_SIZE)
    ])

    # Draw the HP bar
    hp_bar_width = int(WIDTH * 0.8 * (hp / MAX_HP))
    hp_bar_width2 = int(WIDTH * 0.8 * (MAX_HP / MAX_HP))
    pygame.draw.rect(screen, HP_BAR_COLOR2, (WIDTH * 0.1, HEIGHT - 30, hp_bar_width2, 20), border_radius= 5)
    pygame.draw.rect(screen, HP_BAR_COLOR, (WIDTH * 0.1, HEIGHT - 30, hp_bar_width, 20), border_radius= 5)
    pygame.draw.rect(screen, HP_BAR_COLOR, (WIDTH * 0.1, HEIGHT - 30, hp_bar_width2, 20), 2, border_radius= 5)

    # Draw the Exp bar
    exp_bar_width = int(WIDTH * 0.8 * (exp / exp_to_level_up))
    exp_bar_width2 = int(WIDTH * 0.8 * (exp_to_level_up / exp_to_level_up))
    pygame.draw.rect(screen, EXP_BAR_COLOR_DARK, (WIDTH * 0.1, HEIGHT - 10, exp_bar_width2, 60), 10, border_top_left_radius= 5, border_top_right_radius= 5)
    pygame.draw.rect(screen, EXP_BAR_COLOR_LIGHT, (WIDTH * 0.1, HEIGHT - 10, exp_bar_width, 60), 10, border_top_left_radius= 5, border_top_right_radius= 5)
    pygame.draw.rect(screen, EXP_BAR_COLOR_MEDIUM, (WIDTH * 0.1, HEIGHT - 10, exp_bar_width2, 10), 2, border_top_left_radius= 5, border_top_right_radius= 5)  # width = 3
 
    # Draw the HP text
    font = pygame.font.Font(None, 24)
    hp_text = font.render(f"HP: {hp}/{MAX_HP}", True, (255, 255, 255))
    screen.blit(hp_text, (WIDTH * 0.11, HEIGHT - 27))

    # Draw the level text
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 40))

    # Draw the timer
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    minutes = elapsed_time // 60000
    seconds = (elapsed_time % 60000) // 1000
    timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 70))

    # Draw the damaging circle around the player
    pygame.draw.circle(screen, CIRCLE_COLOR, (player_x + PLAYER_SIZE // 2 - camera_x, player_y + PLAYER_SIZE // 2 - camera_y), CIRCLE_RADIUS, 1)

    # Draw the restart button if game over
    if game_state == "game over":
        restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), restart_button_rect)
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Restart", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)

    # Draw the restart button if game over
    if game_state == "game over":
        restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), restart_button_rect)
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Restart", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)

    # Draw the experience text
    exp_text = font.render(f"Exp: {exp}/{exp_to_level_up}", True, (255, 255, 255))
    screen.blit(exp_text, (10, 100))

    # Update the display
    pygame.display.flip()

def game_over_screen():
    global game_state
    game_state = "game over"

def restart_game():
    global game_state, player_x, player_y, hp, enemies, doors, triangle_enemy_x, triangle_enemy_y, start_time, last_hit_time, exp, level, exp_to_level_up
    game_state = "playing"
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    player_y = HEIGHT // 2 - PLAYER_SIZE // 2
    hp = MAX_HP
    enemies = []
    doors = []
    triangle_enemy_x = -TRIANGLE_SIZE
    triangle_enemy_y = random.randint(0, HEIGHT - TRIANGLE_SIZE)
    start_time = pygame.time.get_ticks()  # Reset the timer
    last_hit_time = 0
    exp = 0
    level = 1
    exp_to_level_up = EXP_TO_LEVEL_UP_BASE

def handle_menu_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restart_game()

def handle_game_events():
    global game_state, player_x, player_y, move_left, move_right, move_up, move_down

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_d:
                move_right = True
            elif event.key == pygame.K_w:
                move_up = True
            elif event.key == pygame.K_s:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False
            elif event.key == pygame.K_w:
                move_up = False
            elif event.key == pygame.K_s:
                move_down = False

def update_player_position():
    global player_x, player_y

    if move_left:
        player_x -= 5
    if move_right:
        player_x += 5
    if move_up:
        player_y -= 5
    if move_down:
        player_y += 5

def update_enemy_positions():
    global enemies

    for enemy in enemies:
        direction_x = player_x - enemy["x"]
        direction_y = player_y - enemy["y"]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        enemy["x"] += direction_x * enemy_speed
        enemy["y"] += direction_y * enemy_speed

def update_triangle_enemy_position():
    global triangle_enemy_x, triangle_enemy_y, triangle_enemy_direction

    triangle_enemy_x += triangle_enemy_direction[0] * triangle_enemy_speed
    triangle_enemy_y += triangle_enemy_direction[1] * triangle_enemy_speed

    # Wrap around the screen
    if triangle_enemy_x > WIDTH:
        triangle_enemy_x = -TRIANGLE_SIZE
    elif triangle_enemy_x < -TRIANGLE_SIZE:
        triangle_enemy_x = WIDTH
    if triangle_enemy_y > HEIGHT:
        triangle_enemy_y = -TRIANGLE_SIZE
    elif triangle_enemy_y < -TRIANGLE_SIZE:
        triangle_enemy_y = HEIGHT

    # Update the direction towards the player
    direction_x = player_x - triangle_enemy_x
    direction_y = player_y - triangle_enemy_y
    distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

    if distance != 0:
        triangle_enemy_direction = (direction_x / distance, direction_y / distance)

def spawn_enemy(door, enemy_type):
    global enemies
    enemy_x = door["x"]
    enemy_y = door["y"]

    # Check for collision with other enemies
    for enemy in enemies:
        if (enemy_x < enemy["x"] + ENEMY_SIZE and
                enemy_x + ENEMY_SIZE > enemy["x"] and
                enemy_y < enemy["y"] + ENEMY_SIZE and
                enemy_y + ENEMY_SIZE > enemy["y"]):
            # Adjust position to avoid overlap
            if enemy_x < WIDTH // 2:
                enemy_x += ENEMY_SIZE
            else:
                enemy_x -= ENEMY_SIZE

    # Assign HP based on enemy type
    if enemy_type == "box":
        hp = ENEMY_BOX_HP
        exp = EXP_BOX
    elif enemy_type == "triangle":
        hp = ENEMY_TRIANGLE_HP
        exp = EXP_TRIANGLE

    enemies.append({"x": enemy_x, "y": enemy_y, "hp": hp, "exp": exp})

def spawn_door():
    global doors
    door_x = random.randint(0, WIDTH - DOOR_SIZE)
    door_y = random.randint(0, HEIGHT - DOOR_SIZE)

    # Check for collision with other doors
    for door in doors:
        if (door_x < door["x"] + DOOR_SIZE and
                door_x + DOOR_SIZE > door["x"] and
                door_y < door["y"] + DOOR_SIZE and
                door_y + DOOR_SIZE > door["y"]):
            # Adjust position to avoid overlap
            if door_x < WIDTH // 2:
                door_x += DOOR_SIZE
            else:
                door_x -= DOOR_SIZE

    doors.append({"x": door_x, "y": door_y, "enemies_spawned": 0})

def check_collision():
    global game_state, hp, last_hit_time

    current_time = pygame.time.get_ticks()  # Get current time in milliseconds

    # Check collision with enemies
    for enemy in enemies:
        if (player_x < enemy["x"] + ENEMY_SIZE and
                player_x + PLAYER_SIZE > enemy["x"] and
                player_y < enemy["y"] + ENEMY_SIZE and
                player_y + PLAYER_SIZE > enemy["y"]):
            if current_time - last_hit_time >= 1000:  # 1 second interval between hits
                last_hit_time = current_time
                hp -= 1
                if hp <= 0:
                    game_state = "game over"
            break

    # Check collision with triangle enemy
    if (player_x < triangle_enemy_x + TRIANGLE_SIZE and
            player_x + PLAYER_SIZE > triangle_enemy_x and
            player_y < triangle_enemy_y + TRIANGLE_SIZE and
            player_y + PLAYER_SIZE > triangle_enemy_y):
        if current_time - last_hit_time >= 1000:  # 1 second interval between hits
            last_hit_time = current_time
            hp -= 1
            if hp <= 0:
                game_state = "game over"

# Game loop
while game_state != "quit":
    if game_state == "menu":
        handle_menu_events()
        draw_menu()
    elif game_state == "playing":
        handle_game_events()
        update_player_position()
        update_enemy_positions()
        update_triangle_enemy_position()
        check_collision()

        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        # Spawn an enemy every ENEMY_SPAWN_INTERVAL seconds
        if current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL * 1000:
            try:
                for door in doors:
                    if door["enemies_spawned"] < MAX_ENEMIES_PER_DOOR:
                        # Spawning box enemy
                        spawn_enemy(door, "box")
                        # Spawning triangle enemy
                        spawn_enemy(door, "triangle")
                        door["enemies_spawned"] += 1
                        last_enemy_spawn_time = current_time
                        break  # Spawned an enemy, exit the loop
            except Exception as e:
                print("Error spawning enemy:", e)

        # Spawn a door every DOOR_SPAWN_INTERVAL seconds
        if current_time - last_door_spawn_time >= DOOR_SPAWN_INTERVAL * 1000:
            try:
                if len(doors) < 2:  # Maximum of 2 doors
                    spawn_door()
                    last_door_spawn_time = current_time
            except Exception as e:
                print("Error spawning door:", e)

        # Damage enemies in the circle every CIRCLE_DAMAGE_INTERVAL milliseconds
        if current_time - last_circle_damage_time >= CIRCLE_DAMAGE_INTERVAL:
            for enemy in enemies:
                enemy_center_x = enemy["x"] + ENEMY_SIZE // 2
                enemy_center_y = enemy["y"] + ENEMY_SIZE // 2
                distance = math.sqrt((player_x + PLAYER_SIZE // 2 - enemy_center_x) ** 2 + (player_y + PLAYER_SIZE // 2 - enemy_center_y) ** 2)
                if distance <= CIRCLE_RADIUS:
                    enemy["hp"] -= 1
                    if enemy["hp"] <= 0:
                        enemies.remove(enemy)
                        exp += enemy["exp"]
                        if exp >= exp_to_level_up:
                            level += 1
                            exp -= exp_to_level_up
                            exp_to_level_up += EXP_TO_LEVEL_UP_INCREMENT
            last_circle_damage_time = current_time

        draw_game()
    elif game_state == "game over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
                if restart_button_rect.collidepoint(mouse_pos):
                    restart_game()
                    break  # Exit the event loop to prevent further button presses from being registered
        draw_game()

    clock.tick(30)  # Limit the game to 30 frames per second

# Quit Pygame
pygame.quit()


######  this one works  ######