import pygame, sys
from game import start_level_mode, start_survival_mode
from highscores import show_highscores

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Monster Snake")
clock = pygame.time.Clock()

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont("arial", 72, bold=True)
subtitle_font = pygame.font.SysFont("arial", 28)
button_font = pygame.font.SysFont("arial", 32, bold=True)

# ---------------- COLORS ----------------
BG_COLOR = (15, 15, 35)
TEXT_COLOR = (255, 255, 255)
PANEL_COLOR = (25, 25, 50)
HIGHLIGHT_COLOR = (80, 200, 255)
BUTTON_COLOR = (40, 40, 70)
BUTTON_HOVER = (60, 60, 100)
ACCENT_GREEN = (50, 255, 150)

# ---------------- PARTICLE SYSTEM ----------------
class Particle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = (pygame.time.get_ticks() % 100 - 50) / 10
        self.vy = (pygame.time.get_ticks() % 100 - 50) / 10
        self.size = 2
        self.alpha = 255
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= 3
        
    def draw(self, surface):
        if self.alpha > 0:
            color = (*ACCENT_GREEN, int(self.alpha))
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

particles = []

# ---------------- HELPER FUNCTIONS ----------------
def draw_text_with_shadow(surface, text, font, color, x, y, shadow_offset=3):
    """Draw text with shadow effect"""
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (x + shadow_offset, y + shadow_offset))
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (x, y))

def draw_button(surface, text, rect, hover=False):
    """Draw a modern button with hover effect"""
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    border_color = HIGHLIGHT_COLOR if hover else (100, 100, 150)
    
    # Button shadow
    shadow_rect = pygame.Rect(rect[0] + 4, rect[1] + 4, rect[2], rect[3])
    shadow_surface = pygame.Surface((rect[2], rect[3]))
    shadow_surface.set_alpha(100)
    shadow_surface.fill((0, 0, 0))
    surface.blit(shadow_surface, (shadow_rect[0], shadow_rect[1]))
    
    # Button background
    btn_surface = pygame.Surface((rect[2], rect[3]))
    btn_surface.set_alpha(240)
    btn_surface.fill(color)
    surface.blit(btn_surface, (rect[0], rect[1]))
    
    # Button border with glow effect
    if hover:
        pygame.draw.rect(surface, border_color, rect, 4, border_radius=12)
        # Glow effect
        glow_rect = pygame.Rect(rect[0] - 2, rect[1] - 2, rect[2] + 4, rect[3] + 4)
        pygame.draw.rect(surface, (*HIGHLIGHT_COLOR[:3], 100), glow_rect, 2, border_radius=14)
    else:
        pygame.draw.rect(surface, border_color, rect, 3, border_radius=12)
    
    # Button text
    text_color = HIGHLIGHT_COLOR if hover else TEXT_COLOR
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(rect[0] + rect[2]//2, rect[1] + rect[3]//2))
    surface.blit(text_surf, text_rect)

def draw_snake_animation(surface, offset_y=0):
    """Draw animated snake decoration"""
    time = pygame.time.get_ticks() / 1000
    for i in range(5):
        x = WIDTH // 2 - 100 + i * 20
        y = 150 + offset_y + int(10 * pygame.math.Vector2(1, 0).rotate(time * 180 + i * 72).y)
        size = 18 if i == 0 else 15
        color = ACCENT_GREEN if i == 0 else (30, 200, 120)
        pygame.draw.circle(surface, color, (x, y), size)
        pygame.draw.circle(surface, (20, 150, 90), (x, y), size, 2)

# ---------------- MAIN MENU ----------------
def main_menu():
    """Modern main menu with buttons"""
    
    # Button positions
    btn_width, btn_height = 300, 60
    btn_x = (WIDTH - btn_width) // 2
    
    level_btn = pygame.Rect(btn_x, 250, btn_width, btn_height)
    survival_btn = pygame.Rect(btn_x, 330, btn_width, btn_height)
    highscore_btn = pygame.Rect(btn_x, 410, btn_width, btn_height)
    exit_btn = pygame.Rect(btn_x, 490, btn_width, btn_height)
    
    buttons = [
        (level_btn, "LEVEL MODE", start_level_mode),
        (survival_btn, "SURVIVAL MODE", start_survival_mode),
        (highscore_btn, "HIGH SCORES", show_highscores),
        (exit_btn, "EXIT", None)
    ]
    
    particle_timer = 0
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Background with gradient effect
        screen.fill(BG_COLOR)
        
        # Add some visual flair with rectangles
        for i in range(3):
            alpha = 30 - i * 10
            rect_surface = pygame.Surface((WIDTH - i * 100, HEIGHT - i * 100))
            rect_surface.set_alpha(alpha)
            rect_surface.fill(PANEL_COLOR)
            screen.blit(rect_surface, (i * 50, i * 50))
        
        # Particle effects
        particle_timer += 1
        if particle_timer % 10 == 0:
            for _ in range(2):
                particles.append(Particle())
        
        particles_copy = particles.copy()
        for p in particles_copy:
            p.update()
            if p.alpha <= 0:
                particles.remove(p)
            else:
                p.draw(screen)
        
        # Draw animated snake decoration
        draw_snake_animation(screen)
        
        # Title with glow effect
        title_text = "ARCADE MONSTER"
        title_surf = title_font.render(title_text, True, ACCENT_GREEN)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
        
        # Glow effect for title
        glow_surf = title_font.render(title_text, True, (*ACCENT_GREEN[:3], 100))
        for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            screen.blit(glow_surf, (title_rect.x + offset[0], title_rect.y + offset[1]))
        
        screen.blit(title_surf, title_rect)
        
        # Subtitle
        subtitle = subtitle_font.render("SNAKE", True, HIGHLIGHT_COLOR)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 130)))
        
        # Draw buttons
        for btn_rect, btn_text, _ in buttons:
            hover = btn_rect.collidepoint(mouse_pos)
            draw_button(screen, btn_text, btn_rect, hover)
        
        # Footer text
        footer = pygame.font.SysFont("arial", 16).render("Click buttons to start", True, (150, 150, 150))
        screen.blit(footer, footer.get_rect(center=(WIDTH // 2, HEIGHT - 30)))
        
        pygame.display.update()
        clock.tick(60)
        
        # Event handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                for btn_rect, btn_text, action in buttons:
                    if btn_rect.collidepoint(mouse_pos):
                        if action:
                            action()
                        else:
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    main_menu()