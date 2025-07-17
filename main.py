import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1920
HEIGHT = 1080
FPS = 60
ANIMATION_SPEED = 12  # Frames between sprite changes

# Background constants
BG_WIDTH = 6144  # 4096 * 1.5
BG_HEIGHT = 3072  # 2048 * 1.5

# Polygon collision system
POLYGON_COORDINATES = []

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Horror lighting constants
LIGHT_RADIUS = 150  # Radius of light around character
DARKNESS_ALPHA = 250  # Transparency of darkness (0-255, higher = darker)

def point_in_polygon(x, y, polygon):
    """Check if point (x, y) is inside polygon using ray casting algorithm"""
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def check_polygon_collision(x, y, width=50, height=100):
    """Check if the character position is inside the allowed polygon area"""
    if not POLYGON_COORDINATES:
        return False  # No polygon defined, allow movement
    
    # Check all four corners of the character rectangle
    corners = [
        (x, y),                    # Top-left
        (x + width, y),            # Top-right
        (x, y + height),           # Bottom-left
        (x + width, y + height)    # Bottom-right
    ]
    
    # If any corner is outside the polygon, block movement
    for corner_x, corner_y in corners:
        if not point_in_polygon(corner_x, corner_y, POLYGON_COORDINATES):
            return True  # Collision detected
    
    return False  # All corners inside polygon, allow movement

def set_polygon_boundaries(coordinates):
    """Set the polygon coordinates for movement boundaries"""
    global POLYGON_COORDINATES
    POLYGON_COORDINATES = coordinates
    print(f"Polygon boundaries set with {len(coordinates)} points")

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def update(self, target_x, target_y):
        """Update camera position to follow target"""
        # Center camera on target
        self.x = target_x - WIDTH // 2
        self.y = target_y - HEIGHT // 2
        
        # Clamp camera to background boundaries
        self.x = max(0, min(self.x, BG_WIDTH - WIDTH))
        self.y = max(0, min(self.y, BG_HEIGHT - HEIGHT))
        
    def apply(self, x, y):
        """Apply camera offset to world coordinates"""
        return x - self.x, y - self.y

class Character:
    def __init__(self, x, y):
        self.world_x = x  # World position
        self.world_y = y
        self.standing_sprites = []
        self.walking_sprites = []
        self.running_sprites = []
        self.current_sprite = 0
        self.animation_counter = 0
        self.is_moving = False
        self.is_running = False
        self.facing_right = True
        self.walk_speed = 3
        self.run_speed = 6
        
        # Character dimensions (will be set after loading sprites)
        self.width = 50   # Default width
        self.height = 100 # Default height
        
        # Load sprites
        self.load_standing_sprites()
        self.load_walking_sprites()
        self.load_running_sprites()
        
        # Set actual dimensions based on loaded sprites
        if self.standing_sprites:
            self.width = self.standing_sprites[0].get_width()
            self.height = self.standing_sprites[0].get_height()
        
    def load_standing_sprites(self):
        """Load all standing sprite images"""
        sprites_path = "sprites/standing/"
        
        for i in range(1, 7):  # stand1.png to stand6.png
            sprite_file = f"stand{i}.png"
            sprite_path = os.path.join(sprites_path, sprite_file)
            
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale sprite proportionally for 1920x1080 (1.5x from 1280x720, then /1.3x for smaller character = 1.15x total)
                original_size = sprite.get_size()
                scale_factor = 1.5 / 1.3  # 1.15x total scaling
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
                self.standing_sprites.append(sprite)
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
                
        if not self.standing_sprites:
            print("No standing sprites loaded!")
            
    def load_walking_sprites(self):
        """Load all walking sprite images"""
        sprites_path = "sprites/walking/"
        
        for i in range(1, 11):  # walk1.png to walk10.png
            sprite_file = f"walk{i}.png"
            sprite_path = os.path.join(sprites_path, sprite_file)
            
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale sprite proportionally for 1920x1080 (1.5x from 1280x720, then /1.3x for smaller character = 1.15x total)
                original_size = sprite.get_size()
                scale_factor = 1.5 / 1.3  # 1.15x total scaling
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
                self.walking_sprites.append(sprite)
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
                
        if not self.walking_sprites:
            print("No walking sprites loaded!")
            
    def load_running_sprites(self):
        """Load all running sprite images"""
        sprites_path = "sprites/running/"
        
        # Load run1.png to run10.png
        for i in range(1, 11):  # run1.png to run10.png
            sprite_file = f"run{i}.png"
            sprite_path = os.path.join(sprites_path, sprite_file)
            
            try:
                sprite = pygame.image.load(sprite_path)
                # Scale sprite proportionally for 1920x1080 (1.5x from 1280x720, then /1.3x for smaller character = 1.15x total)
                original_size = sprite.get_size()
                scale_factor = 1.5 / 1.3  # 1.15x total scaling
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
                self.running_sprites.append(sprite)
            except pygame.error as e:
                print(f"Could not load sprite {sprite_path}: {e}")
                
        if not self.running_sprites:
            print("No running sprites loaded!")
            
    def update(self, keys_pressed):
        """Update character animation and movement"""
        # Check for movement input (4 directions)
        moving_right = keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]
        moving_left = keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]
        moving_up = keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]
        moving_down = keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]
        shift_pressed = keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]
        
        # Store previous states to detect changes
        prev_moving = self.is_moving
        prev_running = self.is_running
        
        self.is_moving = moving_right or moving_left or moving_up or moving_down
        self.is_running = self.is_moving and shift_pressed
        
        # Reset animation if state changed
        if (prev_moving != self.is_moving) or (prev_running != self.is_running):
            self.current_sprite = 0
            self.animation_counter = 0
        
        # Update facing direction (only for left/right movement)
        if moving_right:
            self.facing_right = True
        elif moving_left:
            self.facing_right = False
        
        # Move character with collision detection
        if self.is_moving:
            speed = self.run_speed if self.is_running else self.walk_speed
            new_x = self.world_x
            new_y = self.world_y
            
            # Calculate new position
            if moving_right:
                new_x += speed
            elif moving_left:
                new_x -= speed
                
            if moving_up:
                new_y -= speed
            elif moving_down:
                new_y += speed
            
            # Apply collision detection
            # Check horizontal movement
            if not check_polygon_collision(new_x, self.world_y, self.width, self.height):
                # Also check world boundaries
                new_x = max(0, min(new_x, BG_WIDTH - self.width))
                self.world_x = new_x
            
            # Check vertical movement
            if not check_polygon_collision(self.world_x, new_y, self.width, self.height):
                # Also check world boundaries
                new_y = max(0, min(new_y, BG_HEIGHT - self.height))
                self.world_y = new_y
        
        # Update animation
        self.animation_counter += 1
        
        if self.is_running and self.running_sprites:
            # Running animation - very smooth and fast
            if self.animation_counter >= 2:  # Very fast animation for smooth running
                self.animation_counter = 0
                self.current_sprite = (self.current_sprite + 1) % len(self.running_sprites)
        elif self.is_moving and self.walking_sprites:
            # Walking animation
            if self.animation_counter >= ANIMATION_SPEED // 2:  # Medium speed for walking
                self.animation_counter = 0
                self.current_sprite = (self.current_sprite + 1) % len(self.walking_sprites)
        elif self.standing_sprites:
            # Standing animation
            if self.animation_counter >= ANIMATION_SPEED:
                self.animation_counter = 0
                self.current_sprite = (self.current_sprite + 1) % len(self.standing_sprites)
                
    def draw(self, screen, camera):
        """Draw the character on screen with camera offset"""
        sprite = None
        
        if self.is_running and self.running_sprites:
            # Draw running sprite
            if self.current_sprite < len(self.running_sprites):
                sprite = self.running_sprites[self.current_sprite]
        elif self.is_moving and self.walking_sprites:
            # Draw walking sprite
            if self.current_sprite < len(self.walking_sprites):
                sprite = self.walking_sprites[self.current_sprite]
        elif self.standing_sprites:
            # Draw standing sprite
            if self.current_sprite < len(self.standing_sprites):
                sprite = self.standing_sprites[self.current_sprite]
        
        if sprite:
            # Flip sprite horizontally if facing left
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            
            # Apply camera offset
            screen_x, screen_y = camera.apply(self.world_x, self.world_y)
            screen.blit(sprite, (screen_x, screen_y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Escapist Game - Horror Mode")
        self.clock = pygame.time.Clock()
        
        # Create darkness overlay surface
        self.darkness_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Load background
        try:
            original_bg = pygame.image.load("sprites/bg.png")
            # Scale background proportionally for 1920x1080 (1.5x scaling)
            self.background = pygame.transform.scale(original_bg, (BG_WIDTH, BG_HEIGHT))
            print(f"Background loaded and scaled: {self.background.get_size()}")
        except pygame.error as e:
            print(f"Could not load background: {e}")
            # Create a simple gradient background as fallback
            self.background = pygame.Surface((BG_WIDTH, BG_HEIGHT))
            for y in range(BG_HEIGHT):
                color_value = int(50 + (y / BG_HEIGHT) * 100)
                pygame.draw.line(self.background, (color_value, color_value, color_value), (0, y), (BG_WIDTH, y))
        
        # Initialize game objects
        self.camera = Camera()
        
        # Create polygon walls from user coordinates (scaled for 1920x1080)
        polygon_coordinates = [
            (0, 1725),      # 0:1150 * 1.5
            (258, 1724),    # 172:1149 * 1.5
            (260, 1368),    # 173:912 * 1.5
            (420, 1385),    # 280:923 * 1.5
            (450, 1727),    # 300:1151 * 1.5
            (2600, 1727),   # 1733:1151 * 1.5
            (2604, 1383),   # 1736:922 * 1.5
            (2694, 1370),   # 1796:913 * 1.5
            (1620, 1212),   # 1080:808 * 1.5
            (3117, 1215),   # 2078:810 * 1.5
            (3113, 1368),   # 2075:912 * 1.5
            (3225, 1377),   # 2150:918 * 1.5
            (3225, 1725),   # 2150:1150 * 1.5
            (3630, 1725),   # 2420:1150 * 1.5
            (3645, 1335),   # 2430:890 * 1.5
            (3840, 1335),   # 2560:890 * 1.5
            (3840, 1725),   # 2560:1150 * 1.5
            (4245, 1725),   # 2830:1150 * 1.5
            (4245, 1364),   # 2830:909 * 1.5
            (4350, 1370),   # 2900:913 * 1.5
            (4350, 1208),   # 2900:805 * 1.5
            (4773, 1200),   # 3182:800 * 1.5
            (4770, 1350),   # 3180:900 * 1.5
            (4890, 1353),   # 3260:902 * 1.5
            (4890, 1725),   # 3260:1150 * 1.5
            (5625, 1725),   # 3750:1150 * 1.5
            (5625, 1455),   # 3750:970 * 1.5
            (5706, 1455),   # 3804:970 * 1.5
            (5700, 1725),   # 3800:1150 * 1.5
            (6144, 1725),   # 4096:1150 * 1.5
            (6144, 1905),   # 4096:1270 * 1.5
            (5745, 1905),   # 3830:1270 * 1.5
            (5745, 2160),   # 3830:1440 * 1.5
            (5625, 2160),   # 3750:1440 * 1.5
            (5610, 1905),   # 3740:1270 * 1.5
            (3900, 1905),   # 2600:1270 * 1.5
            (3900, 2250),   # 2600:1500 * 1.5
            (3581, 2250),   # 2387:1500 * 1.5
            (3581, 1905),   # 2387:1270 * 1.5
            (525, 1905),    # 350:1270 * 1.5
            (525, 2250),    # 350:1500 * 1.5
            (203, 2250),    # 135:1500 * 1.5
            (203, 1905),    # 135:1270 * 1.5
            (0, 1905),      # 0:1270 * 1.5
        ]
        
        set_polygon_boundaries(polygon_coordinates)
        print(f"Set polygon boundaries with {len(polygon_coordinates)} coordinates")
        
        # Start character in a safe area
        start_x = BG_WIDTH // 2
        start_y = 1800  # Between the walls
        self.character = Character(start_x, start_y)
        
    def draw_polygon_boundaries(self, screen):
        """Draw polygon boundaries (optional - for debugging)"""
        # Polygon boundaries are now invisible - no drawing needed
        # Uncomment below lines if you want to see polygon boundaries for debugging:
        # if len(POLYGON_COORDINATES) > 2:
        #     points = []
        #     for coord in POLYGON_COORDINATES:
        #         screen_pos = self.camera.apply(coord[0], coord[1])
        #         points.append(screen_pos)
        #     if len(points) > 2:
        #         pygame.draw.polygon(screen, (255, 0, 0), points, 2)
        pass
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Get pressed keys for continuous input
            keys_pressed = pygame.key.get_pressed()
            
            # Update game objects
            self.character.update(keys_pressed)
            self.camera.update(self.character.world_x, self.character.world_y)
            
            # Draw everything
            # Draw background with camera offset
            bg_x, bg_y = self.camera.apply(0, 0)
            self.screen.blit(self.background, (bg_x, bg_y))
            
            # Draw polygon boundaries
            self.draw_polygon_boundaries(self.screen)
            
            # Draw character
            self.character.draw(self.screen, self.camera)
            
            # Apply horror lighting effect
            self.apply_horror_lighting()
            
            # Draw UI info
            font = pygame.font.Font(None, 36)
            info_text = f"Pos: ({int(self.character.world_x)}, {int(self.character.world_y)}) | Camera: ({int(self.camera.x)}, {int(self.camera.y)})"
            text_surface = font.render(info_text, True, WHITE)
            self.screen.blit(text_surface, (10, 10))
            
            controls_text = "Controls: WASD/Arrows to move, Shift to run, ESC to quit"
            controls_surface = font.render(controls_text, True, WHITE)
            self.screen.blit(controls_surface, (10, 50))
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        # Quit
        pygame.quit()
        sys.exit()
    
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

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()