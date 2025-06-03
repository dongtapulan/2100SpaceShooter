# src/utils.py

import pygame

def load_image(path):
    return pygame.image.load(path).convert_alpha()

def load_sound(path):
    return pygame.mixer.Sound(path)

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def draw_health_bar(surface, x, y, health, max_health):
    bar_width = 100
    bar_height = 15
    fill = (health / max_health) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)

    pygame.draw.rect(surface, (255, 0, 0), fill_rect)  # red bar
    pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)  # white border

    font = pygame.font.Font(None, 24)
    health_text = font.render(f"Health: {health}", True, (255, 0, 0))
    surface.blit(health_text, (10, 40))