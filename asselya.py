import pygame
import os
import math
from constants import ANIMATION_SPEED

class Asselya:
    def __init__(self, x, y, sprite_folder):
        self.world_x = x
        self.world_y = y
        self.base_x = x  # Store initial position
        self.base_y = y
        self.sprite_folder = sprite_folder
        self.speed = 7  # One unit slower than player's max speed (8)
        self.width = 50
        self.height = 100
        self.vision_radius = 1000  # 1000-pixel vision radius (doubled)
        self.returning_to_base = False
        
        # Animation
        self.current_frame = 0
        self.animation_counter = 0
        self.facing_right = True
        
        # Following behavior
        self.is_following = False
        self.is_running = False
        self.wait_timer = 0
        self.wait_duration = 60  # frames to wait before following
        
        # Load sprites
        self.standing_sprites = []
        self.running_sprites = []
        
        self.load_standing_sprites()
        self.load_running_sprites()
        
    def load_standing_sprites(self):
        """Load standing animation sprites"""
        standing_folder = "asselya/standing"
        if os.path.exists(standing_folder):
            for i in range(1, 5):  # stand1.png to stand4.png
                sprite_path = os.path.join(standing_folder, f"stand{i}.png")
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    # Scale sprite proportionally
                    original_size = sprite.get_size()
                    scale_factor = 1.5 / 1.3  # Same scaling as character
                    new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                    sprite = pygame.transform.scale(sprite, new_size)
                    self.standing_sprites.append(sprite)
    
    def load_running_sprites(self):
        """Load running animation sprites"""
        running_folder = "asselya/running"
        if os.path.exists(running_folder):
            # Get target size from standing sprites
            target_size = None
            if self.standing_sprites:
                target_size = self.standing_sprites[0].get_size()
            
            for i in range(1, 10):  # run1.png to run9.png
                sprite_path = os.path.join(running_folder, f"run{i}.png")
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    
                    if target_size:
                        # Scale to match standing sprite size
                        sprite = pygame.transform.scale(sprite, target_size)
                    else:
                        # Fallback: scale running sprites to approximate standing size
                        # Running: 270*360, Standing: 56*74 (after scaling)
                        # Calculate scale factor to match standing sprite proportions
                        original_size = sprite.get_size()
                        scale_factor_x = 56 * (1.5 / 1.3) / 270  # Target standing width / running width
                        scale_factor_y = 74 * (1.5 / 1.3) / 360  # Target standing height / running height
                        scale_factor = min(scale_factor_x, scale_factor_y)  # Use smaller to maintain proportions
                        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                        sprite = pygame.transform.scale(sprite, new_size)
                    
                    self.running_sprites.append(sprite)
    
    def update(self, player_x, player_y):
        """Update Asselya's position and behavior with vision system"""
        # Calculate distance to player
        distance_to_player = math.sqrt((player_x - self.world_x) ** 2 + (player_y - self.world_y) ** 2)
        
        # Calculate distance to base
        distance_to_base = math.sqrt((self.base_x - self.world_x) ** 2 + (self.base_y - self.world_y) ** 2)
        
        # Check if player is within vision radius
        player_in_vision = distance_to_player <= self.vision_radius
        
        if player_in_vision and not self.returning_to_base:
            # Player is within vision, pursue them without stopping
            self.wait_timer += 1
            if self.wait_timer >= self.wait_duration:
                self.is_following = True
                self.is_running = True
                
                # Move towards player
                dx = player_x - self.world_x
                dy = player_y - self.world_y
                
                # Normalize and apply speed
                if distance_to_player > 0:
                    self.world_x += (dx / distance_to_player) * self.speed
                    self.world_y += (dy / distance_to_player) * self.speed
                
                # Update facing direction
                if dx > 0:
                    self.facing_right = True
                elif dx < 0:
                    self.facing_right = False
        else:
            # Player is out of vision or we're returning to base
            if not player_in_vision:
                self.returning_to_base = True
            
            if self.returning_to_base:
                if distance_to_base > 10:  # Return to base
                    self.is_following = True
                    self.is_running = True
                    
                    # Move towards base
                    dx = self.base_x - self.world_x
                    dy = self.base_y - self.world_y
                    
                    # Normalize and apply speed
                    if distance_to_base > 0:
                        self.world_x += (dx / distance_to_base) * self.speed
                        self.world_y += (dy / distance_to_base) * self.speed
                    
                    # Update facing direction
                    if dx > 0:
                        self.facing_right = True
                    elif dx < 0:
                        self.facing_right = False
                else:
                    # Reached base, stop returning
                    self.returning_to_base = False
                    self.is_following = False
                    self.is_running = False
                    self.wait_timer = 0
            else:
                # Wait at current position
                self.is_following = False
                self.is_running = False
                self.wait_timer = 0
        
        # Update animation
        self.animation_counter += 1
        if self.is_running and self.running_sprites:
            if self.animation_counter >= ANIMATION_SPEED:
                self.animation_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.running_sprites)
        else:
            # Standing animation
            if self.animation_counter >= ANIMATION_SPEED * 2:  # Slower standing animation
                self.animation_counter = 0
                if self.standing_sprites:
                    self.current_frame = (self.current_frame + 1) % len(self.standing_sprites)
    
    def draw(self, screen, camera):
        """Draw Asselya on screen"""
        screen_x, screen_y = camera.apply(self.world_x, self.world_y)
        
        # Choose sprite based on state
        if self.is_running and self.running_sprites:
            sprite = self.running_sprites[self.current_frame % len(self.running_sprites)]
        elif self.standing_sprites:
            sprite = self.standing_sprites[self.current_frame % len(self.standing_sprites)]
        else:
            # Fallback rectangle if no sprites
            pygame.draw.rect(screen, (255, 0, 255), (screen_x, screen_y, self.width, self.height))
            return
        
        # Flip sprite if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        screen.blit(sprite, (screen_x, screen_y))