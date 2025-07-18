import pygame
import os
from constants import ANIMATION_SPEED

class ClickableCharacter:
    def __init__(self, x, y, sprite_path, target_width=70, target_height=100):
        self.world_x = x
        self.world_y = y
        self.sprite_path = sprite_path
        self.width = target_width
        self.height = target_height
        
        # Animation (single frame for now)
        self.current_frame = 0
        self.animation_counter = 0
        
        # Click and dialogue state
        self.is_clicked = False
        self.show_message = False
        self.message_timer = 0
        self.message_duration = 90  # frames (1.5 seconds at 60 FPS)
        self.message = "ГО В МАССАЖКУ"
        
        # Load sprite
        self.sprite = None
        self.load_sprite()
        
        # Load sound
        self.sound = None
        self.load_sound()
        
    def load_sprite(self):
        """Load and scale the sprite to match asselya size"""
        if os.path.exists(self.sprite_path):
            try:
                self.sprite = pygame.image.load(self.sprite_path).convert_alpha()
                # Scale to match asselya size (70x100)
                self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
                print(f"Clickable character sprite loaded: {self.sprite_path}")
            except pygame.error as e:
                print(f"Error loading sprite {self.sprite_path}: {e}")
        else:
            print(f"Sprite file not found: {self.sprite_path}")
    
    def load_sound(self):
        """Load the massazh sound"""
        try:
            self.sound = pygame.mixer.Sound("massazh.mp3")
            print("Massazh sound loaded successfully")
        except pygame.error as e:
            print(f"Error loading massazh.mp3: {e}")
    
    def check_click(self, mouse_pos, camera):
        """Check if the character was clicked"""
        screen_x, screen_y = camera.apply(self.world_x, self.world_y)
        mouse_x, mouse_y = mouse_pos
        
        # Check if click is within character bounds
        if (screen_x <= mouse_x <= screen_x + self.width and
            screen_y <= mouse_y <= screen_y + self.height):
            return True
        return False
    
    def on_click(self):
        """Handle click event"""
        self.show_message = True
        self.message_timer = 0
        
        # Play sound
        if self.sound:
            self.sound.play()
            print("Playing massazh sound")
    
    def update(self):
        """Update character state"""
        # Update message timer
        if self.show_message:
            self.message_timer += 1
            if self.message_timer >= self.message_duration:
                self.show_message = False
                self.message_timer = 0
    
    def draw(self, screen, camera):
        """Draw character and message on screen"""
        screen_x, screen_y = camera.apply(self.world_x, self.world_y)
        
        # Draw sprite
        if self.sprite:
            screen.blit(self.sprite, (screen_x, screen_y))
        else:
            # Fallback rectangle if no sprite
            pygame.draw.rect(screen, (255, 0, 255), (screen_x, screen_y, self.width, self.height))
        
        # Draw message if active
        if self.show_message:
            font = pygame.font.Font(None, 48)
            text_surface = font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            
            # Position text above character
            text_x = screen_x + self.width // 2 - text_rect.width // 2
            text_y = screen_y - text_rect.height - 20
            
            # Draw background for text
            background_rect = pygame.Rect(text_x - 10, text_y - 5, text_rect.width + 20, text_rect.height + 10)
            pygame.draw.rect(screen, (0, 0, 0, 180), background_rect)
            pygame.draw.rect(screen, (255, 255, 255), background_rect, 2)
            
            # Draw text
            screen.blit(text_surface, (text_x, text_y)) 