import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.2
        self.timer = 0

    def update(self):
        self.timer += self.animation_speed
        if self.timer >= 1:
            self.timer = 0
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()  # Destroy the explosion sprite after animation finishes
