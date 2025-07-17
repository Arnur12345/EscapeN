import pygame
import sys
from constants import WIDTH, HEIGHT, BG_WIDTH, BG_HEIGHT, FPS, WHITE, LIGHT_RADIUS, DARKNESS_ALPHA
from utils import set_polygon_boundaries
from camera import Camera
from character import Character
from asselya import Asselya
from npc import NPC

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Escapist Game - Horror Mode")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_over = False
        self.game_over_timer = 0
        self.flicker_timer = 0
        
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
        
        # Create Asselya (following NPC) at her base position
        self.asselya = Asselya(3200, 1600, "asselya/standing/")
        
        # Create stationary NPC (Bernar) to the left of spawn point
        self.npc = NPC(start_x - 150, start_y, "npc/bernar/bernar", 75, 5)
        
        # Create stationary NPC (Bakhredin) to the right of spawn point
        self.bakhredin = NPC(start_x + 150, start_y, "npc/bakhredin/bahr", 90, 7)
    
    def check_collision(self):
        """Check if Asselya caught the player"""
        distance = self.get_asselya_distance()
        
        # If Asselya is very close to player (caught)
        if distance < 30:  # Collision threshold
            self.game_over = True
            return True
        return False
    
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
        subtitle_text = font_medium.render("Asselya вас поймала!", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Restart instruction
        restart_text = font_medium.render("Нажмите R для перезапуска или ESC для выхода", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """Restart the game"""
        self.game_over = False
        self.game_over_timer = 0
        self.flicker_timer = 0
        
        # Reset character position
        start_x = BG_WIDTH // 2
        start_y = 1800
        self.character.world_x = start_x
        self.character.world_y = start_y
        self.character.is_running = False
        
        # Reset Asselya position to base
        self.asselya.world_x = self.asselya.base_x
        self.asselya.world_y = self.asselya.base_y
        self.asselya.wait_timer = 0
        self.asselya.is_following = False
        self.asselya.is_running = False
        self.asselya.returning_to_base = False
        
        # Reset stationary NPCs positions
        self.npc.world_x = start_x - 150
        self.npc.world_y = start_y
        self.bakhredin.world_x = start_x + 150
        self.bakhredin.world_y = start_y
        
        # Reset camera
        self.camera.update(self.character.world_x, self.character.world_y)
    
    def get_asselya_distance(self):
        """Get distance between player and Asselya"""
        dx = self.character.world_x - self.asselya.world_x
        dy = self.character.world_y - self.asselya.world_y
        return (dx**2 + dy**2)**0.5
    
    def apply_flicker_effect(self):
        """Apply screen flicker effect based on Asselya proximity"""
        distance = self.get_asselya_distance()
        
        # Only flicker when Asselya is following (after wait period)
        if not self.asselya.is_following:
            return
        
        # Calculate flicker intensity based on distance
        max_flicker_distance = 500  # Distance at which flickering starts
        min_flicker_distance = 50   # Distance at which flickering is most intense
        
        if distance > max_flicker_distance:
            return  # No flicker if too far
        
        # Calculate intensity (0.0 to 1.0)
        if distance < min_flicker_distance:
            intensity = 1.0
        else:
            intensity = 1.0 - (distance - min_flicker_distance) / (max_flicker_distance - min_flicker_distance)
        
        # Update flicker timer
        self.flicker_timer += 1
        
        # Calculate flicker frequency based on intensity
        flicker_speed = int(20 - (intensity * 15))  # Faster flicker when closer
        if flicker_speed < 2:
            flicker_speed = 2
        
        # Create flicker effect
        if self.flicker_timer % flicker_speed < flicker_speed // 2:
            # Create red flicker overlay
            flicker_alpha = int(intensity * 100)  # Max alpha of 100
            flicker_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flicker_surface.fill((255, 255, 255, flicker_alpha))  # Red flicker
            self.screen.blit(flicker_surface, (0, 0))
        
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
                    elif event.key == pygame.K_r and self.game_over:
                        self.restart_game()
            
            # Get pressed keys for continuous input
            keys_pressed = pygame.key.get_pressed()
            
            # Update game objects only if game is not over
            if not self.game_over:
                self.character.update(keys_pressed)
                self.asselya.update(self.character.world_x, self.character.world_y)
                self.npc.update()  # Stationary NPC only needs animation update
                self.bakhredin.update()  # Stationary Bakhredin NPC only needs animation update
                self.camera.update(self.character.world_x, self.character.world_y)
                
                # Check collision
                self.check_collision()
            else:
                # Increment game over timer for effects
                self.game_over_timer += 1
            
            # Draw everything
            # Draw background with camera offset
            bg_x, bg_y = self.camera.apply(0, 0)
            self.screen.blit(self.background, (bg_x, bg_y))
            
            # Draw polygon boundaries
            self.draw_polygon_boundaries(self.screen)
            
            # Draw character
            self.character.draw(self.screen, self.camera)
            
            # Draw Asselya (following NPC)
            self.asselya.draw(self.screen, self.camera)
            
            # Draw stationary NPC (Bernar)
            self.npc.draw(self.screen, self.camera)
            
            # Draw stationary NPC (Bakhredin)
            self.bakhredin.draw(self.screen, self.camera)
            
            # Apply horror lighting effect
            self.apply_horror_lighting()
            
            # Apply flicker effect based on NPC proximity (only if game is not over)
            if not self.game_over:
                self.apply_flicker_effect()
            
            # Draw UI info (only if game is not over)
            if not self.game_over:
                font = pygame.font.Font(None, 36)
                info_text = f"Pos: ({int(self.character.world_x)}, {int(self.character.world_y)}) | Camera: ({int(self.camera.x)}, {int(self.camera.y)})"
                text_surface = font.render(info_text, True, WHITE)
                self.screen.blit(text_surface, (10, 10))
                
                controls_text = "Controls: WASD/Arrows to move, Shift to run, ESC to quit"
                controls_surface = font.render(controls_text, True, WHITE)
                self.screen.blit(controls_surface, (10, 50))
            
            # Draw game over screen if game is over
            if self.game_over:
                self.draw_game_over_screen()
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        # Quit
        pygame.quit()
        sys.exit()