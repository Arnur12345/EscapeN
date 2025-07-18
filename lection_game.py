import pygame
import sys
import os
from constants import WIDTH, HEIGHT, BG_WIDTH, BG_HEIGHT, FPS, WHITE, LIGHT_RADIUS, DARKNESS_ALPHA, ANIMATION_SPEED
from camera import Camera
from npc import NPC

class LectionCharacter:
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
    
    def update(self, keys, collision_mask, map_width, map_height):
        """Update character position and animation with collision detection"""
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
        
        # Calculate new position
        new_x, new_y = self.world_x, self.world_y
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += self.speed
            self.facing_right = True
        else:
            self.is_walking = False
            self.is_running = False
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += self.speed
        
        # Check boundaries
        if new_x < 0:
            new_x = 0
        elif new_x + self.width > map_width:
            new_x = map_width - self.width
            
        if new_y < 0:
            new_y = 0
        elif new_y + self.height > map_height:
            new_y = map_height - self.height
        
        # Check collision with objects
        if self.check_collision(new_x, new_y, collision_mask):
            # If collision, don't move
            new_x, new_y = self.world_x, self.world_y
        
        # Update position
        self.world_x, self.world_y = new_x, new_y
        
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
    
    def check_collision(self, x, y, collision_mask):
        """Check if character collides with obstacles"""
        if collision_mask is None:
            return False
            
        # Check collision at character's corners and center
        check_points = [
            (int(x), int(y)),  # Top-left
            (int(x + self.width), int(y)),  # Top-right
            (int(x), int(y + self.height)),  # Bottom-left
            (int(x + self.width), int(y + self.height)),  # Bottom-right
            (int(x + self.width // 2), int(y + self.height // 2))  # Center
        ]
        
        mask_width, mask_height = collision_mask.get_size()
        
        for px, py in check_points:
            if 0 <= px < mask_width and 0 <= py < mask_height:
                # Check if pixel is not transparent (obstacle)
                try:
                    pixel = collision_mask.get_at((px, py))
                    if pixel[3] > 128:  # Alpha > 128 means solid obstacle
                        return True
                except IndexError:
                    continue
        
        return False
        
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
                scale_factor = 2.0  # Increased scaling for better visibility
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
                scale_factor = 2.0  # Increased scaling for better visibility
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
                scale_factor = 2.0  # Increased scaling for better visibility
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
                self.running_sprites.append(sprite)
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
    
    def update(self, keys, collision_mask, map_width, map_height):
        """Update character position and animation with collision detection"""
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
        
        # Calculate new position
        new_x, new_y = self.world_x, self.world_y
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += self.speed
            self.facing_right = True
        else:
            self.is_walking = False
            self.is_running = False
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += self.speed
        
        # Check boundaries
        if new_x < 0:
            new_x = 0
        elif new_x + self.width > map_width:
            new_x = map_width - self.width
            
        if new_y < 0:
            new_y = 0
        elif new_y + self.height > map_height:
            new_y = map_height - self.height
        
        # Check collision with objects
        if self.check_collision(new_x, new_y, collision_mask):
            # If collision, don't move
            new_x, new_y = self.world_x, self.world_y
        
        # Update position
        self.world_x, self.world_y = new_x, new_y
        
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
    
    def check_collision(self, x, y, collision_mask):
        """Check if character collides with obstacles"""
        if collision_mask is None:
            return False
            
        # Check collision at character's corners and center
        check_points = [
            (int(x), int(y)),  # Top-left
            (int(x + self.width), int(y)),  # Top-right
            (int(x), int(y + self.height)),  # Bottom-left
            (int(x + self.width), int(y + self.height)),  # Bottom-right
            (int(x + self.width // 2), int(y + self.height // 2))  # Center
        ]
        
        mask_width, mask_height = collision_mask.get_size()
        
        for px, py in check_points:
            if 0 <= px < mask_width and 0 <= py < mask_height:
                # Check if pixel is not transparent (obstacle)
                try:
                    pixel = collision_mask.get_at((px, py))
                    if pixel[3] > 128:  # Alpha > 128 means solid obstacle
                        return True
                except IndexError:
                    continue
        
        return False
    
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

class LectionGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Escapist Game - Lection Hall")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_over = False
        self.game_over_timer = 0
        
        # Fade-in effect
        self.fade_alpha = 255  # Start with black screen
        self.fade_speed = 3    # Speed of fade-in
        self.fade_surface = pygame.Surface((WIDTH, HEIGHT))
        self.fade_surface.fill((0, 0, 0))  # Black surface
        
        # Create darkness overlay surface
        self.darkness_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Load lection background with smaller scale to make character appear larger
        try:
            original_lection = pygame.image.load("lection.png")
            # Use smaller scale to make character appear larger relative to background
            smaller_bg_width = int(BG_WIDTH * 0.8)  # 80% of original size
            smaller_bg_height = int(BG_HEIGHT * 0.8)  # 80% of original size
            self.background = pygame.transform.scale(original_lection, (smaller_bg_width, smaller_bg_height))
            print(f"Lection background loaded and scaled: {self.background.get_size()}")
        except pygame.error as e:
            print(f"Could not load lection background: {e}")
            # Create a dark background as fallback for lection
            smaller_bg_width = int(BG_WIDTH * 0.8)
            smaller_bg_height = int(BG_HEIGHT * 0.8)
            self.background = pygame.Surface((smaller_bg_width, smaller_bg_height))
            self.background.fill((20, 20, 30))  # Dark blue-gray
        
        # Load collision objects layer
        try:
            self.objects_layer = pygame.image.load("lection_objects.png")
            # Scale to match background
            self.objects_layer = pygame.transform.scale(self.objects_layer, (smaller_bg_width, smaller_bg_height))
        except pygame.error as e:
            print(f"Could not load lection_objects.png: {e}")
            self.objects_layer = None
        
        # Get map dimensions
        self.map_width, self.map_height = smaller_bg_width, smaller_bg_height
        
        # Initialize game objects
        self.camera = Camera()
        
        # No polygon boundaries for lection hall - using pixel-based collision
        # Start character at bottom-left corner
        spawn_x = 50
        spawn_y = self.map_height - 150
        self.character = LectionCharacter(spawn_x, spawn_y)
        
        # Create NPCs for lection hall (optional - can be added later)
        # For now, no NPCs in lection hall
        
    def restart_game(self):
        """Restart the lection game"""
        self.game_over = False
        self.game_over_timer = 0
        
        # Reset fade-in effect
        self.fade_alpha = 255
        
        # Reset character position to spawn at bottom-left corner
        spawn_x = 50
        spawn_y = self.map_height - 150
        self.character.world_x = spawn_x
        self.character.world_y = spawn_y
        self.character.is_running = False
        
        # Reset camera
        self.camera.update(self.character.world_x, self.character.world_y)
    
    def apply_horror_lighting(self):
        """Apply horror lighting effect - darkness with light around character"""
        # Fill darkness surface with semi-transparent black
        self.darkness_surface.fill((0, 0, 0, DARKNESS_ALPHA))
        
        # Get character position on screen
        char_screen_x, char_screen_y = self.camera.apply(
            self.character.world_x + self.character.width // 2,  # Center of character
            self.character.world_y + self.character.height // 2
        )
        
        # Create light circle around character
        # We'll create a gradient light effect
        for radius in range(LIGHT_RADIUS, 0, -5):
            # Calculate alpha for gradient effect (more transparent in center)
            alpha = int((LIGHT_RADIUS - radius) / LIGHT_RADIUS * DARKNESS_ALPHA)
            
            # Create temporary surface for this circle
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (0, 0, 0, alpha), (radius, radius), radius)
            
            # Blit with BLEND_RGBA_SUB to subtract darkness (create light)
            circle_x = char_screen_x - radius
            circle_y = char_screen_y - radius
            
            # Make sure circle is within screen bounds
            if (circle_x < WIDTH and circle_x + radius * 2 > 0 and 
                circle_y < HEIGHT and circle_y + radius * 2 > 0):
                self.darkness_surface.blit(circle_surface, (circle_x, circle_y), special_flags=pygame.BLEND_RGBA_SUB)
        
        # Apply the darkness overlay to the screen
        self.screen.blit(self.darkness_surface, (0, 0))
    
    def draw_game_over_screen(self):
        """Draw game over screen"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Dark overlay
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        font_large = pygame.font.Font(None, 120)
        font_medium = pygame.font.Font(None, 60)
        
        # Main "Game Over" text
        game_over_text = font_large.render("ВЫ ПРОИГРАЛИ", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Subtitle text
        subtitle_text = font_medium.render("Что-то пошло не так!", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Restart instruction
        restart_text = font_medium.render("Нажмите R для перезапуска или ESC для выхода", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Main game loop for lection hall"""
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.restart_game()
            
            # Get pressed keys for continuous input
            keys_pressed = pygame.key.get_pressed()
            
            # Update game objects only if game is not over
            if not self.game_over:
                self.character.update(keys_pressed, self.objects_layer, self.map_width, self.map_height)
                self.camera.update(self.character.world_x, self.character.world_y)
            else:
                # Increment game over timer for effects
                self.game_over_timer += 1
            
            # Draw everything
            # Draw background with camera offset
            bg_x, bg_y = self.camera.apply(0, 0)
            self.screen.blit(self.background, (bg_x, bg_y))
            
            # Draw objects layer on top of background
            if self.objects_layer:
                self.screen.blit(self.objects_layer, (bg_x, bg_y))
            
            # Draw character
            self.character.draw(self.screen, self.camera)
            
            # Apply horror lighting effect
            self.apply_horror_lighting()
            
            # Draw UI info (only if game is not over)
            if not self.game_over:
                font = pygame.font.Font(None, 36)
                info_text = f"Pos: ({int(self.character.world_x)}, {int(self.character.world_y)}) | Lection Hall"
                text_surface = font.render(info_text, True, WHITE)
                self.screen.blit(text_surface, (10, 10))
                
                controls_text = "Controls: WASD/Arrows to move, Shift to run, ESC to quit"
                controls_surface = font.render(controls_text, True, WHITE)
                self.screen.blit(controls_surface, (10, 50))
                
                # Show lection hall info
                lection_text = "Welcome to the Lection Hall - No boundaries, free exploration!"
                lection_surface = font.render(lection_text, True, (200, 255, 200))
                self.screen.blit(lection_surface, (10, 90))
            
            # Draw game over screen if game is over
            if self.game_over:
                self.draw_game_over_screen()
            
            # Apply fade-in effect
            if self.fade_alpha > 0:
                self.fade_alpha -= self.fade_speed
                if self.fade_alpha < 0:
                    self.fade_alpha = 0
                
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        # Quit
        pygame.quit()
        sys.exit()