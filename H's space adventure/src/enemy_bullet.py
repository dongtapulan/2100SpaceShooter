import pygame

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 0, 0))  # Red bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

# Initialize pygame and create the screen before using it
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Set your desired window size

# Initialize sprite groups before using them
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

enemy_group.update()
enemy_group.draw(screen)

enemy_bullet_group.update()
enemy_bullet_group.draw(screen)
