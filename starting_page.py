import pygame
import sys
from constants import WIDTH, HEIGHT

class StartingPage:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Escapist Game")
        self.clock = pygame.time.Clock()
        
        # Load background image
        try:
            self.background = pygame.image.load("starting.png")
            # Scale to fit screen if needed
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            print("Starting background loaded successfully")
        except pygame.error as e:
            print(f"Could not load starting.png: {e}")
            # Create a fallback background
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((50, 50, 50))
        
        # Load button image for reference (but make it invisible)
        try:
            self.button_image = pygame.image.load("button.png")
            print("Button image loaded successfully")
        except pygame.error as e:
            print(f"Could not load button.png: {e}")
            # Create a fallback button
            self.button_image = pygame.Surface((200, 80))
            self.button_image.fill((100, 100, 100))
            font = pygame.font.Font(None, 36)
            text = font.render("START", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.button_image.get_rect().center)
            self.button_image.blit(text, text_rect)
        
        # Button properties (invisible clickable area)
        # Create rectangle button area: from (645, 459) to (1288, 704)
        button_width = 1288 - 645  # 643 pixels wide
        button_height = 704 - 459  # 245 pixels tall
        self.button_rect = pygame.Rect(645, 459, button_width, button_height)
        
        # Create invisible button surface
        self.invisible_button = pygame.Surface((button_width, button_height))
        self.invisible_button.set_alpha(0)  # Make it completely transparent
        
        # Button state
        self.button_hovered = False
        
    def handle_events(self):
        """Handle events for the starting page"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.button_rect.collidepoint(event.pos):
                        return "start_game"
            elif event.type == pygame.MOUSEMOTION:
                # Check if mouse is hovering over button
                self.button_hovered = self.button_rect.collidepoint(event.pos)
        
        return "continue"
    
    def draw(self):
        """Draw the starting page"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw invisible button (no visual representation)
        # The button area is still clickable but not visible
        self.screen.blit(self.invisible_button, self.button_rect)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Run the starting page loop"""
        running = True
        while running:
            result = self.handle_events()
            
            if result == "quit":
                return "quit"
            elif result == "start_game":
                return "start_game"
            
            self.draw()
            self.clock.tick(60)
        
        return "quit"