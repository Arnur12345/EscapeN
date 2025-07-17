import pygame
import os
from constants import *
from utils import check_polygon_collision

class Character:
    def __init__(self, x, y):
        self.world_x = x
        self.world_y = y
        self.speed = 5
        self.width = 50
        self.height = 100
        
        # Animation
        self.current_frame = 0
        self.animation_counter = 0
        self.facing_right = True
        
        # Movement states
        self.is_walking = False
        self.is_running = False
        
        # Load sprites
        self.standing_sprites = []
        self.walking_sprites = []
        self.running_sprites = []
        
        self.load_standing_sprites()
        self.load_walking_sprites()
        self.load_running_sprites()
        
    def load_standing_sprites(self):
        """Load standing animation sprites"""
        sprites_path = "sprites/standing/"
        for i in range(1, 7):  # stand1.png to stand6.png
            sprite_file = f"stand{i}.png"
            sprite_path = os.path.join(sprites_path, sprite_file)
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale sprite proportionally for 1920x1080
                original_size = sprite.get_size()
                scale_factor = 1.5 / 1.3  # 1.15x total scaling
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
                self.standing_sprites.append(sprite)
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
    
    def load_walking_sprites(self):
        """Load walking animation sprites"""
        sprites_path = "sprites/walking/"
        for i in range(1, 11):  # walk1.png to walk10.png
            sprite_file = f"walk{i}.png"
            sprite_path = os.path.join(sprites_path, sprite_file)
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale sprite proportionally for 1920x1080
                original_size = sprite.get_size()
                scale_factor = 1.5 / 1.3  # 1.15x total scaling
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
                self.walking_sprites.append(sprite)
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
    
    def load_running_sprites(self):
        """Load running animation sprites"""
        sprites_path = "sprites/running/"
        for i in range(1, 11):  # run1.png to run10.png
            sprite_file = f"run{i}.png"
            sprite_path = os.path.join(sprites_path, sprite_file)
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale sprite proportionally for 1920x1080
                original_size = sprite.get_size()
                scale_factor = 1.5 / 1.3  # 1.15x total scaling
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
                self.running_sprites.append(sprite)
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
    
    def update(self, keys):
        """Update character position and animation"""
        old_x, old_y = self.world_x, self.world_y
        
        # Handle movement
        self.is_walking = False
        self.is_running = False
        
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.speed = 8
            self.is_running = True
        else:
            self.speed = 5
            self.is_walking = True
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x = self.world_x - self.speed
            if not check_polygon_collision(new_x, self.world_y, self.width, self.height):
                self.world_x = new_x
                self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x = self.world_x + self.speed
            if not check_polygon_collision(new_x, self.world_y, self.width, self.height):
                self.world_x = new_x
                self.facing_right = True
        else:
            self.is_walking = False
            self.is_running = False
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y = self.world_y - self.speed
            if not check_polygon_collision(self.world_x, new_y, self.width, self.height):
                self.world_y = new_y
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y = self.world_y + self.speed
            if not check_polygon_collision(self.world_x, new_y, self.width, self.height):
                self.world_y = new_y
        
        # Update animation
        if self.world_x != old_x or self.world_y != old_y:
            self.animation_counter += 1
            if self.animation_counter >= ANIMATION_SPEED:
                self.animation_counter = 0
                if self.is_running and self.running_sprites:
                    self.current_frame = (self.current_frame + 1) % len(self.running_sprites)
                elif self.is_walking and self.walking_sprites:
                    self.current_frame = (self.current_frame + 1) % len(self.walking_sprites)
        else:
            # Standing animation
            self.animation_counter += 1
            if self.animation_counter >= ANIMATION_SPEED * 2:  # Slower standing animation
                self.animation_counter = 0
                if self.standing_sprites:
                    self.current_frame = (self.current_frame + 1) % len(self.standing_sprites)
    
    def draw(self, screen, camera):
        """Draw character on screen"""
        screen_x, screen_y = camera.apply(self.world_x, self.world_y)
        
        # Choose sprite based on state
        if self.is_running and self.running_sprites:
            sprite = self.running_sprites[self.current_frame % len(self.running_sprites)]
        elif self.is_walking and self.walking_sprites:
            sprite = self.walking_sprites[self.current_frame % len(self.walking_sprites)]
        elif self.standing_sprites:
            sprite = self.standing_sprites[self.current_frame % len(self.standing_sprites)]
        else:
            # Fallback rectangle if no sprites
            pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y, self.width, self.height))
            return
        
        # Flip sprite if facing left
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        screen.blit(sprite, (screen_x, screen_y))