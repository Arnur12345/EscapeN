import pygame
import os
from constants import ANIMATION_SPEED

class NPC:
    def __init__(self, x, y, sprite_prefix, target_width=50, frame_count=4):
        self.world_x = x
        self.world_y = y
        self.sprite_prefix = sprite_prefix
        self.target_width = target_width
        self.frame_count = frame_count
        self.width = target_width
        self.height = int(target_width)  # More proportional aspect ratio
        
        # Animation
        self.current_frame = 0
        self.animation_counter = 0
        self.facing_right = True
        
        # Load sprites
        self.sprites = []
        self.load_sprites()
        
    def load_sprites(self):
        """Load NPC sprites with proportional scaling"""
        for i in range(1, self.frame_count + 1):
            sprite_path = f"{self.sprite_prefix}{i}.png"
            if os.path.exists(sprite_path):
                sprite = pygame.image.load(sprite_path).convert_alpha()
                # Get original size and scale proportionally
                original_size = sprite.get_size()
                scale_factor = self.width / original_size[0]
                new_height = int(original_size[1] * scale_factor)
                sprite = pygame.transform.scale(sprite, (self.width, new_height))
                self.sprites.append(sprite)
                # Update height based on actual sprite proportions
                if i == 1:  # Set height based on first sprite
                    self.height = new_height
    
    def update(self):
        """Update NPC animation"""
        self.animation_counter += 1
        if self.animation_counter >= ANIMATION_SPEED * 2:  # Slower animation
            self.animation_counter = 0
            if self.sprites:
                self.current_frame = (self.current_frame + 1) % len(self.sprites)
    
    def draw(self, screen, camera):
        """Draw NPC on screen"""
        screen_x, screen_y = camera.apply(self.world_x, self.world_y)
        
        if self.sprites:
            sprite = self.sprites[self.current_frame % len(self.sprites)]
            
            # Flip sprite if facing left
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            
            screen.blit(sprite, (screen_x, screen_y))
        else:
            # Fallback rectangle if no sprites
            pygame.draw.rect(screen, (255, 255, 0), (screen_x, screen_y, self.width, self.height))