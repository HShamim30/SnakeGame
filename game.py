import pygame, random, sys
from highscores import save_score

pygame.init()
pygame.mixer.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 600
BLOCK = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Modern Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 26)
title_font = pygame.font.SysFont("arial", 48, bold=True)
menu_font = pygame.font.SysFont("arial", 32)

# ---------------- COLORS ----------------
BG_COLOR = (15, 15, 35)
SNAKE_COLOR = (50, 255, 150)
SNAKE_BORDER = (30, 200, 120)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 100)
PANEL_COLOR = (25, 25, 50)
HIGHLIGHT_COLOR = (80, 200, 255)
GAME_OVER_RED = (255, 50, 50)

# ---------------- LOAD ASSETS ----------------
IMG = lambda x: pygame.transform.scale(
    pygame.image.load(f"assets/images/{x}"), (BLOCK, BLOCK))

apple_img   = IMG("apple.png")
bomb_img    = IMG("bomb.png")
magnet_img  = IMG("magnet.png")
scissor_img = IMG("scissor.png")
obstacle_img= IMG("obstacle.png")

eat_snd   = pygame.mixer.Sound("assets/sounds/eat.wav")
bomb_snd  = pygame.mixer.Sound("assets/sounds/bomb.wav")
power_snd = pygame.mixer.Sound("assets/sounds/power.wav")
over_snd  = pygame.mixer.Sound("assets/sounds/gameover.wav")

# ---------------- COMMON ----------------
def spawn():
    return (random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK))

def draw_text_with_shadow(surface, text, font, color, x, y, shadow_offset=2):
    """Draw text with shadow effect"""
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (x + shadow_offset, y + shadow_offset))
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (x, y))

def draw_panel(surface, rect, alpha=200):
    """Draw a semi-transparent panel"""
    panel = pygame.Surface((rect[2], rect[3]))
    panel.set_alpha(alpha)
    panel.fill(PANEL_COLOR)
    surface.blit(panel, (rect[0], rect[1]))
    pygame.draw.rect(surface, HIGHLIGHT_COLOR, rect, 2, border_radius=10)

def draw_snake_segment(surface, pos, is_head=False):
    """Draw snake segment with gradient effect"""
    rect = pygame.Rect(pos[0], pos[1], BLOCK, BLOCK)
    
    # Border
    pygame.draw.rect(surface, SNAKE_BORDER, rect, border_radius=5)
    
    # Inner fill
    inner_rect = rect.inflate(-4, -4)
    pygame.draw.rect(surface, SNAKE_COLOR, inner_rect, border_radius=4)
    
    # Head highlight
    if is_head:
        highlight = pygame.Rect(pos[0] + 4, pos[1] + 4, BLOCK - 8, BLOCK - 8)
        pygame.draw.rect(surface, (100, 255, 200), highlight, border_radius=3)

def draw_button(surface, text, rect, hover=False):
    """Draw a button with hover effect"""
    color = HIGHLIGHT_COLOR if hover else PANEL_COLOR
    border_color = (150, 220, 255) if hover else HIGHLIGHT_COLOR
    
    # Button background
    btn_surface = pygame.Surface((rect[2], rect[3]))
    btn_surface.set_alpha(220)
    btn_surface.fill(color)
    surface.blit(btn_surface, (rect[0], rect[1]))
    
    # Button border
    pygame.draw.rect(surface, border_color, rect, 3, border_radius=10)
    
    # Button text
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=(rect[0] + rect[2]//2, rect[1] + rect[3]//2))
    surface.blit(text_surf, text_rect)

def game_over_menu(score=0, mode="survival"):
    """Modern game over screen with buttons"""
    restart_btn = pygame.Rect(250, 310, 150, 50)
    menu_btn = pygame.Rect(420, 310, 150, 50)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        restart_hover = restart_btn.collidepoint(mouse_pos)
        menu_hover = menu_btn.collidepoint(mouse_pos)
        
        # Draw dark overlay
        screen.fill(BG_COLOR)
        
        # Draw game over panel
        panel_rect = (200, 150, 400, 250)
        draw_panel(screen, panel_rect)
        
        # Title
        draw_text_with_shadow(screen, "GAME OVER", title_font, GAME_OVER_RED, 260, 180)
        
        # Score
        draw_text_with_shadow(screen, f"Score: {score}", menu_font, TEXT_COLOR, 320, 250)
        
        # Buttons
        draw_button(screen, "RESTART", restart_btn, restart_hover)
        draw_button(screen, "MENU", menu_btn, menu_hover)
        
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if restart_hover: return "RESTART"
                if menu_hover: return "MENU"

def main_menu():
    """Modern main menu"""
    selected = 0
    options = ["Survival Mode", "Level Mode", "Quit"]
    
    while True:
        screen.fill(BG_COLOR)
        
        # Title
        draw_text_with_shadow(screen, "SNAKE GAME", title_font, HIGHLIGHT_COLOR, 220, 100)
        
        # Menu options
        for i, option in enumerate(options):
            color = HIGHLIGHT_COLOR if i == selected else TEXT_COLOR
            y_pos = 250 + i * 60
            
            if i == selected:
                # Draw selection box
                select_rect = (250, y_pos - 10, 300, 50)
                draw_panel(screen, select_rect, alpha=100)
            
            draw_text_with_shadow(screen, option, menu_font, color, 280, y_pos)
        
        pygame.display.update()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    if selected == 0:
                        start_survival_mode()
                    elif selected == 1:
                        start_level_mode()
                    elif selected == 2:
                        pygame.quit()
                        sys.exit()

# =====================================================
# ================= SURVIVAL MODE =====================
# =====================================================
def start_survival_mode():
    while True:
        result = survival_game()
        if result == "MENU": 
            return
        # Agar RESTART hai to loop continue karega

def survival_game():
    snake = [(100, 100)]
    direction = (BLOCK, 0)
    food = spawn()
    bomb = None
    magnet = None
    scissor = None
    magnet_active = False
    magnet_time = 0
    score = 0

    while True:
        speed = 10
        if len(snake) >= 10: speed = 20

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != (0, BLOCK): 
                    direction = (0, -BLOCK)
                if e.key == pygame.K_DOWN and direction != (0, -BLOCK): 
                    direction = (0, BLOCK)
                if e.key == pygame.K_LEFT and direction != (BLOCK, 0): 
                    direction = (-BLOCK, 0)
                if e.key == pygame.K_RIGHT and direction != (-BLOCK, 0): 
                    direction = (BLOCK, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Wall collision
        if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            over_snd.play()
            save_score("survival", score)
            return game_over_menu(score, "survival")
        
        # Self collision
        if head in snake:
            over_snd.play()
            save_score("survival", score)
            return game_over_menu(score, "survival")

        snake.insert(0, head)

        # APPLE
        if head == food:
            eat_snd.play()
            score += 10
            food = spawn()
        else:
            snake.pop()

        # BOMB - Proper collision detection
        if not bomb and random.randint(1, 150) == 1:
            bomb = spawn()
            while bomb in snake or bomb == food:
                bomb = spawn()
                
        if bomb and head == bomb:
            bomb_snd.play()
            save_score("survival", score)
            return game_over_menu(score, "survival")

        # MAGNET
        if len(snake) >= 15 and not magnet and random.randint(1, 200) == 1:
            magnet = spawn()
            while magnet in snake or magnet == food or magnet == bomb:
                magnet = spawn()
                
        if magnet and head == magnet:
            power_snd.play()
            magnet_active = True
            magnet_time = pygame.time.get_ticks()
            magnet = None

        # SCISSOR
        if len(snake) >= 25 and not scissor and random.randint(1, 250) == 1:
            scissor = spawn()
            while scissor in snake or scissor == food or scissor == bomb:
                scissor = spawn()
                
        if scissor and head == scissor:
            power_snd.play()
            snake = snake[:-10] if len(snake) > 10 else snake
            scissor = None

        # MAGNET EFFECT
        if magnet_active:
            hx, hy = head
            fx, fy = food
            pygame.draw.circle(screen, (0, 255, 255), (hx + 10, hy + 10), 120, 2)
            if abs(hx - fx) < 120 and abs(hy - fy) < 120:
                snake.insert(0, food)
                eat_snd.play()
                score += 10
                food = spawn()
            if pygame.time.get_ticks() - magnet_time > 5000:
                magnet_active = False

        # DRAW
        screen.fill(BG_COLOR)
        
        # Draw snake
        for i, s in enumerate(snake):
            draw_snake_segment(screen, s, is_head=(i == 0))
        
        # Draw items with glow effect
        screen.blit(apple_img, food)
        if bomb: 
            pygame.draw.circle(screen, (255, 50, 50), (bomb[0] + 10, bomb[1] + 10), 15, 2)
            screen.blit(bomb_img, bomb)
        if magnet: 
            pygame.draw.circle(screen, (100, 200, 255), (magnet[0] + 10, magnet[1] + 10), 15, 2)
            screen.blit(magnet_img, magnet)
        if scissor: 
            pygame.draw.circle(screen, (255, 200, 100), (scissor[0] + 10, scissor[1] + 10), 15, 2)
            screen.blit(scissor_img, scissor)

        # HUD Panel
        hud_rect = (10, 10, 200, 60)
        draw_panel(screen, hud_rect, alpha=180)
        draw_text_with_shadow(screen, f"Score: {score}", font, TEXT_COLOR, 20, 20)
        draw_text_with_shadow(screen, f"Length: {len(snake)}", font, TEXT_COLOR, 20, 45)
        
        pygame.display.update()
        clock.tick(speed)

# =====================================================
# ================= LEVEL MODE ========================
# =====================================================
def start_level_mode():
    while True:
        level = 1
        total_score = 0
        
        while level <= 4:
            result, level_score = level_game(level, total_score)
            
            if result == "MENU":
                return  # Main menu pe jaao
            elif result == "RESTART":
                break  # Level mode restart karo
            elif result == "NEXT":
                total_score += level_score
                level += 1

def level_game(level, total_score):
    LEVELS = {
        1: (5, 10, 0),
        2: (6, 14, 12),
        3: (6, 16, 15),
        4: (6, 20, 15)
    }

    need, speed, obs_count = LEVELS[level]
    snake = [(100, 100)]
    direction = (BLOCK, 0)
    food = spawn()
    obstacles = [spawn() for _ in range(obs_count)]
    apples = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != (0, BLOCK): 
                    direction = (0, -BLOCK)
                if e.key == pygame.K_DOWN and direction != (0, -BLOCK): 
                    direction = (0, BLOCK)
                if e.key == pygame.K_LEFT and direction != (BLOCK, 0): 
                    direction = (-BLOCK, 0)
                if e.key == pygame.K_RIGHT and direction != (-BLOCK, 0): 
                    direction = (BLOCK, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        
        # Wall collision
        if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            over_snd.play()
            save_score("level", total_score + apples * 10)
            return game_over_menu(total_score + apples * 10, "level"), apples * 10
        
        # Obstacle collision - Static obstacles
        if head in obstacles:
            over_snd.play()
            save_score("level", total_score + apples * 10)
            return game_over_menu(total_score + apples * 10, "level"), apples * 10
        
        # Self collision
        if head in snake:
            over_snd.play()
            save_score("level", total_score + apples * 10)
            return game_over_menu(total_score + apples * 10, "level"), apples * 10

        snake.insert(0, head)

        if head == food:
            eat_snd.play()
            apples += 1
            food = spawn()
            while food in obstacles or food in snake:
                food = spawn()
        else:
            snake.pop()

        if apples >= need:
            return "NEXT", apples * 10

        # DRAW
        screen.fill(BG_COLOR)
        
        # Draw snake
        for i, s in enumerate(snake):
            draw_snake_segment(screen, s, is_head=(i == 0))
        
        # Draw obstacles with warning glow
        for o in obstacles:
            pygame.draw.circle(screen, (255, 100, 100), (o[0] + 10, o[1] + 10), 18, 2)
            screen.blit(obstacle_img, o)
        
        # Draw food
        screen.blit(apple_img, food)

        # HUD Panel
        hud_rect = (10, 10, 280, 110)
        draw_panel(screen, hud_rect, alpha=180)
        draw_text_with_shadow(screen, f"Level {level}", font, HIGHLIGHT_COLOR, 20, 20)
        draw_text_with_shadow(screen, f"Apples: {apples}/{need}", font, TEXT_COLOR, 20, 50)
        draw_text_with_shadow(screen, f"Total Score: {total_score + apples * 10}", font, TEXT_COLOR, 20, 80)
        
        pygame.display.update()
        clock.tick(speed)

# =====================================================
# ================= MAIN GAME LOOP ====================
# =====================================================
if __name__ == "__main__":
    main_menu()