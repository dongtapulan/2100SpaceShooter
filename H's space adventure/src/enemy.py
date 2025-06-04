import pygame
import random
from settings import ENEMY_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = ENEMY_SPEED
        self.speed_x = random.choice([-2, 2])  # Move left or right randomly
        self.shoot_delay = random.randint(60, 120)  # frames between shots
        self.shoot_timer = 0

    def update(self):
        # Move enemy
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # Reverse direction if it hits screen bounds
        if self.rect.left <= 0 or self.rect.right >= 800:  # Assuming screen width = 800
            self.speed_x *= -1

        # Shoot timer
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot()
            self.shoot_timer = 0

        # Remove enemy if off screen
        if self.rect.top > 600:  # Assuming screen height = 600
            self.kill()

    def shoot(self):
        from enemy_bullet import EnemyBullet  # Avoid circular import
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        self.groups()[0].add(bullet)  # Add to same group
