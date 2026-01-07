import pygame
import os
import wave
import struct
import math

pygame.init()

# ---------------- SETUP ----------------
BLOCK = 32
SAMPLE_RATE = 44100

os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/sounds", exist_ok=True)

# ---------------- SOUND MAKER ----------------
def make_sound(filename, freq=440, duration=0.25):
    wav = wave.open(f"assets/sounds/{filename}", "w")
    wav.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))

    for i in range(int(SAMPLE_RATE * duration)):
        value = int(32767 * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))
        wav.writeframesraw(struct.pack("<h", value))

    wav.close()

# ---------------- APPLE ----------------
def make_apple():
    s = pygame.Surface((BLOCK, BLOCK), pygame.SRCALPHA)
    pygame.draw.circle(s, (220, 0, 0), (16, 16), 12)
    pygame.draw.rect(s, (0, 180, 0), (15, 2, 2, 6))
    pygame.image.save(s, "assets/images/apple.png")

# ---------------- BOMB ----------------
def make_bomb():
    s = pygame.Surface((BLOCK, BLOCK), pygame.SRCALPHA)
    pygame.draw.circle(s, (40, 40, 40), (16, 18), 12)
    pygame.draw.line(s, (255, 200, 0), (16, 4), (22, 10), 3)
    pygame.draw.circle(s, (255, 0, 0), (24, 8), 3)
    pygame.image.save(s, "assets/images/bomb.png")

# ---------------- MAGNET ----------------
def make_magnet():
    s = pygame.Surface((BLOCK, BLOCK), pygame.SRCALPHA)
    pygame.draw.rect(s, (200, 0, 0), (6, 6, 6, 18))
    pygame.draw.rect(s, (200, 0, 0), (20, 6, 6, 18))
    pygame.draw.rect(s, (180, 180, 180), (6, 22, 6, 4))
    pygame.draw.rect(s, (180, 180, 180), (20, 22, 6, 4))
    pygame.image.save(s, "assets/images/magnet.png")

# ---------------- SCISSOR ----------------
def make_scissor():
    s = pygame.Surface((BLOCK, BLOCK), pygame.SRCALPHA)
    pygame.draw.circle(s, (200, 200, 200), (10, 22), 5, 2)
    pygame.draw.circle(s, (200, 200, 200), (22, 22), 5, 2)
    pygame.draw.line(s, (200, 200, 200), (10, 18), (22, 6), 2)
    pygame.draw.line(s, (200, 200, 200), (22, 18), (10, 6), 2)
    pygame.image.save(s, "assets/images/scissor.png")

# ---------------- OBSTACLE ----------------
def make_obstacle():
    s = pygame.Surface((BLOCK, BLOCK))
    s.fill((120, 120, 120))
    pygame.draw.rect(s, (80, 80, 80), (0, 0, BLOCK, BLOCK), 2)
    pygame.image.save(s, "assets/images/obstacle.png")

# ---------------- CREATE ALL ----------------
make_apple()
make_bomb()
make_magnet()
make_scissor()
make_obstacle()

make_sound("eat.wav", 600)
make_sound("bomb.wav", 120)
make_sound("power.wav", 900)
make_sound("gameover.wav", 200)

print("🔥 REAL ICON ASSETS GENERATED SUCCESSFULLY 🔥")
