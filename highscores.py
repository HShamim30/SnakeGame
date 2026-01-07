import pygame
import json
import os
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("High Scores")
clock = pygame.time.Clock()

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont("arial", 48, bold=True)
subtitle_font = pygame.font.SysFont("arial", 32, bold=True)
score_font = pygame.font.SysFont("arial", 26)
button_font = pygame.font.SysFont("arial", 28, bold=True)

# ---------------- COLORS ----------------
BG_COLOR = (15, 15, 35)
TEXT_COLOR = (255, 255, 255)
PANEL_COLOR = (25, 25, 50)
HIGHLIGHT_COLOR = (80, 200, 255)
BUTTON_COLOR = (40, 40, 70)
BUTTON_HOVER = (60, 60, 100)
ACCENT_GREEN = (50, 255, 150)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

FILE = "scores.json"

# ---------------- HELPER FUNCTIONS ----------------
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

def draw_button(surface, text, rect, hover=False):
    """Draw a modern button with hover effect"""
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    border_color = HIGHLIGHT_COLOR if hover else (100, 100, 150)
    
    # Button shadow
    shadow_rect = pygame.Rect(rect[0] + 3, rect[1] + 3, rect[2], rect[3])
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
        pygame.draw.rect(surface, border_color, rect, 4, border_radius=10)
        glow_rect = pygame.Rect(rect[0] - 2, rect[1] - 2, rect[2] + 4, rect[3] + 4)
        pygame.draw.rect(surface, (*HIGHLIGHT_COLOR[:3], 100), glow_rect, 2, border_radius=12)
    else:
        pygame.draw.rect(surface, border_color, rect, 3, border_radius=10)
    
    # Button text
    text_color = HIGHLIGHT_COLOR if hover else TEXT_COLOR
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(rect[0] + rect[2]//2, rect[1] + rect[3]//2))
    surface.blit(text_surf, text_rect)

def get_rank_color(rank):
    """Get color based on rank"""
    if rank == 0:
        return GOLD
    elif rank == 1:
        return SILVER
    elif rank == 2:
        return BRONZE
    else:
        return (150, 150, 200)

# ---------------- SCORE MANAGEMENT ----------------
def load_scores():
    if not os.path.exists(FILE):
        return {"level": [], "survival": []}
    with open(FILE, "r") as f:
        return json.load(f)

def save_score(mode, score):
    data = load_scores()
    data[mode].append(score)
    data[mode] = sorted(data[mode], reverse=True)[:5]

    with open(FILE, "w") as f:
        json.dump(data, f)

# ---------------- HIGH SCORES SCREEN ----------------
def show_highscores():
    scores = load_scores()
    
    # Button setup
    level_btn = pygame.Rect(80, 520, 200, 50)
    survival_btn = pygame.Rect(300, 520, 200, 50)
    menu_btn = pygame.Rect(520, 520, 200, 50)
    
    current_mode = "level"  # Start with level mode
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Background with gradient effect
        screen.fill(BG_COLOR)
        
        # Background decorative panels
        for i in range(3):
            alpha = 20 - i * 5
            rect_surface = pygame.Surface((WIDTH - i * 100, HEIGHT - i * 100))
            rect_surface.set_alpha(alpha)
            rect_surface.fill(PANEL_COLOR)
            screen.blit(rect_surface, (i * 50, i * 50))
        
        # Title
        draw_text_with_shadow(screen, "HIGH SCORES", title_font, ACCENT_GREEN, 240, 30)
        
        # Mode indicator
        mode_text = "LEVEL MODE" if current_mode == "level" else "SURVIVAL MODE"
        mode_color = HIGHLIGHT_COLOR
        draw_text_with_shadow(screen, mode_text, subtitle_font, mode_color, 270, 90)
        
        # Scores panel
        panel_rect = (100, 140, 600, 350)
        draw_panel(screen, panel_rect, alpha=220)
        
        # Display scores
        y_offset = 160
        current_scores = scores[current_mode]
        
        if not current_scores:
            no_score_text = score_font.render("No scores yet!", True, (150, 150, 150))
            screen.blit(no_score_text, no_score_text.get_rect(center=(WIDTH // 2, 300)))
        else:
            for i, score in enumerate(current_scores):
                rank_color = get_rank_color(i)
                
                # Rank number with medal icon
                if i < 3:
                    medal = ["🥇", "🥈", "🥉"][i]
                    rank_text = f"{medal} #{i+1}"
                else:
                    rank_text = f"#{i+1}"
                
                # Draw rank
                rank_surf = score_font.render(rank_text, True, rank_color)
                screen.blit(rank_surf, (150, y_offset))
                
                # Draw score with highlight
                score_text = f"{score:,}"
                score_surf = score_font.render(score_text, True, TEXT_COLOR)
                screen.blit(score_surf, (450, y_offset))
                
                # Separator line
                if i < len(current_scores) - 1:
                    pygame.draw.line(screen, (60, 60, 80), 
                                   (130, y_offset + 35), 
                                   (670, y_offset + 35), 2)
                
                y_offset += 60
        
        # Draw mode selection buttons
        level_hover = level_btn.collidepoint(mouse_pos)
        survival_hover = survival_btn.collidepoint(mouse_pos)
        menu_hover = menu_btn.collidepoint(mouse_pos)
        
        # Highlight current mode
        if current_mode == "level":
            draw_button(screen, "LEVEL", level_btn, True)
        else:
            draw_button(screen, "LEVEL", level_btn, level_hover)
            
        if current_mode == "survival":
            draw_button(screen, "SURVIVAL", survival_btn, True)
        else:
            draw_button(screen, "SURVIVAL", survival_btn, survival_hover)
        
        draw_button(screen, "MENU", menu_btn, menu_hover)
        
        pygame.display.update()
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_btn.collidepoint(mouse_pos):
                    current_mode = "level"
                elif survival_btn.collidepoint(mouse_pos):
                    current_mode = "survival"
                elif menu_btn.collidepoint(mouse_pos):
                    running = False
                    return

if __name__ == "__main__":
    show_highscores()