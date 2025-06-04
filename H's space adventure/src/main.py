import pygame
import sys
import random

from settings import *
from utils import load_image, load_sound
from player import Player
from bullet import Bullet
from enemy import Enemy

# Star class for animated background
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 2)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.size)

# Explosion class for handling explosion animations
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, scale=1.0, speed=5):
        super().__init__()
        self.frames = [pygame.transform.scale(frame, (int(frame.get_width()*scale), int(frame.get_height()*scale))) for frame in frames]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= self.speed:
            self.index += 1
            self.timer = 0
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]

# UI Button
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(pos)

# Game Menu
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((5, 5, 20))
        
        self.title_font = pygame.font.Font("assets/font/ARCADE_R.TTF", 28)
        self.title_text = self.title_font.render("2100: Space Adventure", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        button_width = 200
        button_height = 50
        x_center = SCREEN_WIDTH // 2 - button_width // 2
        self.start_button = Button(x_center, SCREEN_HEIGHT // 2, button_width, button_height, "Start Game", (0, 100, 0), (0, 150, 0))
        self.quit_button = Button(x_center, SCREEN_HEIGHT // 2 + 70, button_width, button_height, "Quit", (100, 0, 0), (150, 0, 0))
        self.stars = [Star() for _ in range(100)]

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if self.start_button.is_clicked(mouse_pos, event):
                    return "story"  # Start Story Screen first before game
                if self.quit_button.is_clicked(mouse_pos, event):
                    return "quit"

            for star in self.stars:
                star.update()
            self.start_button.check_hover(mouse_pos)
            self.quit_button.check_hover(mouse_pos)

            self.screen.blit(self.background, (0, 0))
            for star in self.stars:
                star.draw(self.screen)
            self.screen.blit(self.title_text, self.title_rect)
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

class GameOverScreen:
    def __init__(self, screen, score, high_score):
        self.screen = screen
        self.score = score
        self.high_score = high_score
        self.font = pygame.font.Font("assets/font/ARCADE_R.TTF", 32)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "Play Again", (0, 0, 128), (0, 0, 180))
        self.menu_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50, "Main Menu", (100, 0, 0), (150, 0, 0))

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if self.restart_button.is_clicked(mouse_pos, event):
                    return "game"
                if self.menu_button.is_clicked(mouse_pos, event):
                    return "menu"

            self.restart_button.check_hover(mouse_pos)
            self.menu_button.check_hover(mouse_pos)

            self.screen.fill((0, 0, 0))
            game_over_text = self.font.render("YOU DIED", True, (255, 0, 0))
            score_text = self.small_font.render(f"Your Score: {self.score}", True, (255, 255, 255))
            high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, (255, 255, 100))

            self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60)))
            self.screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))
            self.screen.blit(high_score_text, high_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10)))
            self.restart_button.draw(self.screen)
            self.menu_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

# Flash screen animation before Game Over
def flash_screen(screen, duration=400):
    flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    flash_surface.fill((255, 255, 255))
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
#Main game loop
def game_loop(screen):
    clock = pygame.time.Clock()
    stars = [Star() for _ in range(50)]
    bg_color = (5, 5, 20)

    try:
        player_img = load_image("assets/images/player.png")
        bullet_img = load_image("assets/images/bullet.png")
        enemy_img = load_image("assets/images/enemy.png")
        shoot_sound = load_sound("assets/sounds/shoot.wav")
        explosion_sound = load_sound("assets/sounds/explosion.wav")
        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.play(-1 )
    except Exception as e:
        print(f"Error loading assets: {e}")
        return "menu"

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, player_img)
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    try:
        explosion_sheet = load_image("assets/images/explosion.png")
        frame_w, frame_h = 64, 64
        frames = [explosion_sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, frame_h)) for i in range(explosion_sheet.get_width() // frame_w)]
    except Exception as e:
        print(f"Failed to load explosion frames: {e}")
        return "menu"

    score = 0
    health = 10
    if not hasattr(game_loop, "high_score"):
        game_loop.high_score = 0
    font = pygame.font.Font(None, 30)
    enemy_spawn_timer = 0

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, bullet_img)
                    bullets.add(bullet)
                    shoot_sound.play()

        if enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            enemy = Enemy(random.randint(30, SCREEN_WIDTH - 30), -50, enemy_img)
            enemies.add(enemy)
            enemy_spawn_timer = 5
        else:
            enemy_spawn_timer += 1

        player_group.update(keys)
        bullets.update()
        enemies.update()
        explosions.update()
        for star in stars:
            star.update()

        for bullet in bullets:
            hit = pygame.sprite.spritecollide(bullet, enemies, True)
            if hit:
                bullet.kill()
                for e in hit:
                    explosions.add(Explosion(e.rect.centerx, e.rect.centery, frames, scale=1.5, speed=4))
                score += 100
                explosion_sound.play()

        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            health -= 1
            explosions.add(Explosion(player.rect.centerx, player.rect.centery, frames, scale=2, speed=4))
            explosion_sound.play()
            if health <= 0:
                flash_screen(screen)
                if score > game_loop.high_score:
                    game_loop.high_score = score
                return "game_over", score, game_loop.high_score

        screen.fill(bg_color)
        for star in stars:
            star.draw(screen)
        player_group.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)
        explosions.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        health_text = font.render(f"Health: {health}", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (SCREEN_WIDTH - 120, 10))
        
        

        pygame.display.flip()

# Story screen showing a simple narrative with Continue button
class StoryScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/font/ARCADE_R.TTF", 12)
        self.small_font = pygame.font.Font(None, 12)
        self.text_lines = [
            "In the year 2100, humanity fights for survival...",
            "You are the last hope to defend Earth from alien invaders.",
            "Prepare your spaceship, sharpen your skills, and",
            "blast your way through waves of enemies.",
            "",
            "Good luck, pilot!"
        ]
        button_width = 200
        button_height = 50
        self.continue_button = Button(SCREEN_WIDTH//2 - button_width//2, SCREEN_HEIGHT - 100, button_width, button_height, "Continue", (0, 100, 0), (0, 150, 0))
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((5, 5, 20))
        self.stars = [Star() for _ in range(80)]

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if self.continue_button.is_clicked(mouse_pos, event):
                    return "game"

            for star in self.stars:
                star.update()

            self.continue_button.check_hover(mouse_pos)
            self.screen.blit(self.background, (0, 0))
            for star in self.stars:
                star.draw(self.screen)

            # Draw the text lines centered horizontally
            start_y = SCREEN_HEIGHT // 4
            for i, line in enumerate(self.text_lines):
                rendered_text = self.font.render(line, True, (255, 255, 255))
                rect = rendered_text.get_rect(center=(SCREEN_WIDTH//2, start_y + i * 35))
                self.screen.blit(rendered_text, rect)

            self.continue_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2100: Space Adventure")
    current_screen = "menu"
    score = 0
    high_score = 0

    menu = Menu(screen)
    story = StoryScreen(screen)
    game_over_screen = None

    while True:
        if current_screen == "menu":
            result = menu.run()
            if result == "story":
                current_screen = "story"
            elif result == "quit":
                break

        elif current_screen == "story":
            result = story.run()
            if result == "game":
                current_screen = "game"
            elif result == "quit":
                break

        elif current_screen == "game":
            result = game_loop(screen)
            if isinstance(result, tuple) and result[0] == "game_over":
                _, score, high_score = result
                game_over_screen = GameOverScreen(screen, score, high_score)
                current_screen = "game_over"
            elif result == "menu":
                current_screen = "menu"
            elif result == "quit":
                break

        elif current_screen == "game_over":
            result = game_over_screen.run()
            if result == "game":
                current_screen = "game"
            elif result == "menu":
                current_screen = "menu"
            elif result == "quit":
                break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
