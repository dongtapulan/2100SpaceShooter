import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_HEALTH, FONT_NAME, FONT_SIZE

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(FONT_NAME, 36)
        
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((5, 5, 20))
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.title_font = pygame.font.Font(FONT_NAME, 72)
        
        # Game state variables
        self.current_score = 0
        self.high_score = 0
        
        # Initialize UI elements
        self.init_ui()
        
        # Stars for background
        self.stars = []
        self.init_stars()
    
    def init_ui(self):
        """Initialize all UI elements"""
        # Title
        self.title_text = self.title_font.render("H's Space Adventure", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        
        # Buttons
        button_width = 200
        button_height = 50
        start_x = SCREEN_WIDTH//2 - button_width//2
        
        self.start_button = Button(
            start_x, SCREEN_HEIGHT//2, 
            button_width, button_height,
            "Start Game", (0, 100, 0), (0, 150, 0)
        )
        
        self.quit_button = Button(
            start_x, SCREEN_HEIGHT//2 + 70, 
            button_width, button_height,
            "Quit", (100, 0, 0), (150, 0, 0)
        )
        
        # Score display
        self.score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 100))
    
    def init_stars(self):
        """Initialize starfield background"""
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2),
                'size': random.randint(1, 3)
            })
    
    def update_stars(self):
        """Update star positions"""
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw_stars(self):
        """Draw starfield background"""
        for star in self.stars:
            pygame.draw.circle(
                self.screen, 
                (255, 255, 255), 
                (int(star['x']), int(star['y'])), 
                star['size']
            )
    
    def draw_health_bar(self, current_health, max_health):
        """Draw health bar at top of screen"""
        bar_width = 200
        bar_height = 20
        health_ratio = current_health / max_health
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, bar_width, bar_height))
        # Current health
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, bar_width * health_ratio, bar_height))
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, bar_width, bar_height), 2)
        
        # Health text
        health_text = self.font.render(f"Health: {current_health}/{max_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (bar_width + 20, 10))
    
    def show_game_over(self, final_score):
        """Display game over screen with final score"""
        running = True
        
        # Update high score if needed
        if final_score > self.high_score:
            self.high_score = final_score
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return "menu"
                if self.quit_button.is_clicked(mouse_pos, event):
                    return "quit"
            
            # Update
            self.update_stars()
            self.quit_button.check_hover(mouse_pos)
            
            # Draw
            self.screen.blit(self.background, (0, 0))
            self.draw_stars()
            
            # Game over text
            game_over_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
            score_text = self.font.render(f"Final Score: {final_score}", True, (255, 255, 255))
            high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
            prompt_text = self.font.render("Press ENTER to continue", True, (255, 255, 255))
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            self.screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(prompt_text, (SCREEN_WIDTH//2 - prompt_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
            
            self.quit_button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return "quit"
    
    def run(self):
        """Main menu loop"""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if self.start_button.is_clicked(mouse_pos, event):
                    return "game"
                if self.quit_button.is_clicked(mouse_pos, event):
                    return "quit"
            
            # Update
            self.update_stars()
            self.start_button.check_hover(mouse_pos)
            self.quit_button.check_hover(mouse_pos)
            
            # Draw
            self.screen.blit(self.background, (0, 0))
            self.draw_stars()
            
            # Draw title and buttons
            self.screen.blit(self.title_text, self.title_rect)
            self.screen.blit(self.score_text, (SCREEN_WIDTH//2 - self.score_text.get_width()//2, SCREEN_HEIGHT//4 + 100))
            
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return "quit"