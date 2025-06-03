# src/bullet.py

import pygame
from settings import PLAYER_BULLET_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_BULLET_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
