# src/enemy.py

import pygame
from settings import ENEMY_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()
    