import pygame
import time

# Define screen dimensions
SCREEN_WIDTH = 800  # Set this to your game's screen width
SCREEN_HEIGHT = 640  # Set this to your game's screen height

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.invulnerable = False
        self.invulnerable_time = 0
        
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
            
        # Update invulnerability timer
        if self.invulnerable and pygame.time.get_ticks() > self.invulnerable_time:
            self.invulnerable = False
            
    def make_invulnerable(self, duration):
        self.invulnerable = True
        self.invulnerable_time = pygame.time.get_ticks() + duration