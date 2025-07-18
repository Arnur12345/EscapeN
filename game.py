import pygame
import sys
from constants import (WIDTH, HEIGHT, BG_WIDTH, BG_HEIGHT, FPS, WHITE, LIGHT_RADIUS, DARKNESS_ALPHA,
                      USERS_COLOR, MONEY_COLOR, BAR_BG_COLOR, BAR_BORDER_COLOR, BLACK, GREEN)
from utils import set_polygon_boundaries
from camera import Camera
from character import Character
# from asselya import Asselya  # Temporarily disabled for safe environment
from npc import NPC
from task_manager import TaskManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Escapist Game - Horror Mode")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_over = False
        self.game_over_timer = 0
        self.flicker_timer = 0
        
        # Startup metrics
        self.users = 10  # Starting with 10 users
        self.money = 1000  # Starting with $1000
        self.max_users = 1000000  # 1M users max
        self.max_money = 10000000  # $10M max
        
        # Fade-in effect
        self.fade_alpha = 255  # Start with black screen
        self.fade_speed = 3    # Speed of fade-in
        self.fade_surface = pygame.Surface((WIDTH, HEIGHT))
        self.fade_surface.fill((0, 0, 0))  # Black surface
        
        # Door coordinates (scaled for 1920x1080)
        self.door_x1 = 1800 * 1.5  # 2700
        self.door_y = 815 * 1.5    # 1222.5
        self.door_x2 = 2070 * 1.5  # 3105
        self.door_width = self.door_x2 - self.door_x1  # 405
        self.door_height = 50  # Door height for collision detection
        
        # Create darkness overlay surface
        self.darkness_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Load main background
        try:
            original_bg = pygame.image.load("sprites/bg.png")
            # Scale background proportionally for 1920x1080 (1.5x scaling)
            self.background = pygame.transform.scale(original_bg, (BG_WIDTH, BG_HEIGHT))
            print(f"Main background loaded and scaled: {self.background.get_size()}")
        except pygame.error as e:
            print(f"Could not load main background: {e}")
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
        
        # Create Asselya (following NPC) at her base position - DISABLED
        # self.asselya = Asselya(3200, 1600, "asselya/standing/")
        
        # Create stationary NPC (Bernar) to the left of spawn point
        self.npc = NPC(start_x - 150, start_y, "npc/bernar/bernar", 75, 5)
        
        # Create stationary NPC (Bakhredin) to the right of spawn point
        self.bakhredin = NPC(start_x + 150, start_y, "npc/bakhredin/bahr", 90, 7)
        
        # Initialize task system
        self.task_manager = TaskManager()
        print("Task system initialized")
    
    def check_collision(self):
        """Check if Asselya caught the player - DISABLED"""
        # Asselya collision disabled for safe environment
        return False
        
    def check_door_collision(self):
        """Check if player is touching the door"""
        # Check if player is within door area
        player_x = self.character.world_x + self.character.width // 2
        player_y = self.character.world_y + self.character.height // 2
        
        if (self.door_x1 <= player_x <= self.door_x2 and 
            self.door_y <= player_y <= self.door_y + self.door_height):
            return True
        return False
        
    def teleport_to_lection(self):
        """Teleport player to lection hall (separate game environment)"""
        print("Teleporting to lection hall...")
        
        # Import and start the lection game
        from lection_game import LectionGame
        
        # Quit current pygame instance
        pygame.quit()
        
        # Initialize pygame again for lection game
        pygame.init()
        
        # Start lection game
        lection_game = LectionGame()
        lection_game.run()
    
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
        
        # Reset startup metrics
        self.users = 10
        self.money = 1000
        
        # Reset fade-in effect
        self.fade_alpha = 255
        
        # Reset character position
        start_x = BG_WIDTH // 2
        start_y = 1800
        self.character.world_x = start_x
        self.character.world_y = start_y
        self.character.is_running = False
        
        # Reset Asselya position to base - DISABLED
        # self.asselya.world_x = self.asselya.base_x
        # self.asselya.world_y = self.asselya.base_y
        # self.asselya.wait_timer = 0
        # self.asselya.is_following = False
        # self.asselya.is_running = False
        # self.asselya.returning_to_base = False
        
        # Reset stationary NPCs positions
        self.npc.world_x = start_x - 150
        self.npc.world_y = start_y
        self.bakhredin.world_x = start_x + 150
        self.bakhredin.world_y = start_y
        
        # Reset tasks
        self.task_manager.reset_all_tasks()
        
        # Reset camera
        self.camera.update(self.character.world_x, self.character.world_y)
    
    def get_asselya_distance(self):
        """Get distance between player and Asselya - DISABLED"""
        # Asselya disabled for safe environment
        return 1000  # Return large distance to disable effects
    
    def apply_flicker_effect(self):
        """Apply screen flicker effect based on Asselya proximity - DISABLED"""
        # Asselya disabled for safe environment
        return
        
        # All flicker effect code disabled
        
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
    
    def draw_startup_metrics(self):
        """Draw startup metrics bars (users and money)"""
        bar_width = 300
        bar_height = 25
        bar_x = WIDTH - bar_width - 20  # Right side of screen
        users_bar_y = 20
        money_bar_y = users_bar_y + bar_height + 15
        
        # Draw Users bar
        users_percentage = min(self.users / self.max_users, 1.0)
        users_fill_width = int(bar_width * users_percentage)
        
        # Background
        pygame.draw.rect(self.screen, BAR_BG_COLOR, (bar_x, users_bar_y, bar_width, bar_height))
        # Fill
        pygame.draw.rect(self.screen, USERS_COLOR, (bar_x, users_bar_y, users_fill_width, bar_height))
        # Border
        pygame.draw.rect(self.screen, BAR_BORDER_COLOR, (bar_x, users_bar_y, bar_width, bar_height), 2)
        
        # Users text
        font = pygame.font.Font(None, 28)
        users_text = f"Users: {self.users:,}"
        users_surface = font.render(users_text, True, WHITE)
        self.screen.blit(users_surface, (bar_x, users_bar_y - 25))
        
        # Draw Money bar
        money_percentage = min(self.money / self.max_money, 1.0)
        money_fill_width = int(bar_width * money_percentage)
        
        # Background
        pygame.draw.rect(self.screen, BAR_BG_COLOR, (bar_x, money_bar_y, bar_width, bar_height))
        # Fill
        pygame.draw.rect(self.screen, MONEY_COLOR, (bar_x, money_bar_y, money_fill_width, bar_height))
        # Border
        pygame.draw.rect(self.screen, BAR_BORDER_COLOR, (bar_x, money_bar_y, bar_width, bar_height), 2)
        
        # Money text
        money_text = f"Money: ${self.money:,}"
        money_surface = font.render(money_text, True, WHITE)
        self.screen.blit(money_surface, (bar_x, money_bar_y - 25))
    
    def add_users(self, amount):
        """Add users to the startup"""
        self.users = min(self.users + amount, self.max_users)
        print(f"Added {amount} users. Total: {self.users:,}")
    
    def remove_users(self, amount):
        """Remove users from the startup"""
        self.users = max(self.users - amount, 0)
        print(f"Removed {amount} users. Total: {self.users:,}")
    
    def add_money(self, amount):
        """Add money to the startup"""
        self.money = min(self.money + amount, self.max_money)
        print(f"Added ${amount:,}. Total: ${self.money:,}")
    
    def remove_money(self, amount):
        """Remove money from the startup"""
        self.money = max(self.money - amount, 0)
        print(f"Removed ${amount:,}. Total: ${self.money:,}")
    
    def set_users(self, amount):
        """Set exact number of users"""
        self.users = min(max(amount, 0), self.max_users)
        print(f"Set users to: {self.users:,}")
    
    def set_money(self, amount):
        """Set exact amount of money"""
        self.money = min(max(amount, 0), self.max_money)
        print(f"Set money to: ${self.money:,}")
    
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
                    
                    # Test keys for startup metrics (only during gameplay)
                    elif not self.game_over:
                        # Users control (1-5 keys)
                        if event.key == pygame.K_1:
                            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                                self.remove_users(10)
                            else:
                                self.add_users(10)
                        elif event.key == pygame.K_2:
                            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                                self.remove_users(100)
                            else:
                                self.add_users(100)
                        elif event.key == pygame.K_3:
                            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                                self.remove_users(1000)
                            else:
                                self.add_users(1000)
                        
                        # Money control (6-9 keys)
                        elif event.key == pygame.K_6:
                            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                                self.remove_money(100)
                            else:
                                self.add_money(100)
                        elif event.key == pygame.K_7:
                            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                                self.remove_money(1000)
                            else:
                                self.add_money(1000)
                        elif event.key == pygame.K_8:
                            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                                self.remove_money(10000)
                            else:
                                self.add_money(10000)
                        
                        # Task management keys (F1-F5)
                        elif event.key == pygame.K_F1:
                            self.task_manager.activate_task("first_users")
                        elif event.key == pygame.K_F2:
                            self.task_manager.activate_task("find_investor")
                        elif event.key == pygame.K_F3:
                            self.task_manager.activate_task("hire_developer")
                        elif event.key == pygame.K_F4:
                            self.task_manager.activate_task("launch_product")
                        elif event.key == pygame.K_F5:
                            self.task_manager.activate_task("social_media")
            
            # Get pressed keys for continuous input
            keys_pressed = pygame.key.get_pressed()
            
            # Update game objects only if game is not over
            if not self.game_over:
                self.character.update(keys_pressed)
                # self.asselya.update(self.character.world_x, self.character.world_y)  # DISABLED
                self.npc.update()  # Stationary NPC only needs animation update
                self.bakhredin.update()  # Stationary Bakhredin NPC only needs animation update
                self.camera.update(self.character.world_x, self.character.world_y)
                
                # Startup metrics are now static - controlled manually via functions
                
                # Check collision
                self.check_collision()
                
                # Check task interactions
                task_interaction = self.task_manager.check_task_interactions(
                    self.character.world_x, self.character.world_y,
                    self.character.width, self.character.height
                )
                
                # Handle task completion (press E to complete)
                keys_pressed = pygame.key.get_pressed()
                if task_interaction and keys_pressed[pygame.K_e]:
                    rewards = self.task_manager.complete_task(task_interaction)
                    if rewards:
                        # Apply rewards to player
                        self.add_users(rewards["users"])
                        self.add_money(rewards["money"])
                
                # Check door collision and teleport
                if self.check_door_collision():
                    self.teleport_to_lection()
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
            
            # Draw Asselya (following NPC) - DISABLED
            # self.asselya.draw(self.screen, self.camera)
            
            # Draw stationary NPC (Bernar)
            self.npc.draw(self.screen, self.camera)
            
            # Draw stationary NPC (Bakhredin)
            self.bakhredin.draw(self.screen, self.camera)
            
            # Draw tasks on map
            self.task_manager.draw_tasks(self.screen, self.camera)
            
            # Apply horror lighting effect
            self.apply_horror_lighting()
            
            # Apply flicker effect based on NPC proximity (only if game is not over)
            if not self.game_over:
                self.apply_flicker_effect()
            
            # Draw UI info (only if game is not over)
            if not self.game_over:
                font = pygame.font.Font(None, 36)
                info_text = f"Pos: ({int(self.character.world_x)}, {int(self.character.world_y)}) | Main Map"
                text_surface = font.render(info_text, True, WHITE)
                self.screen.blit(text_surface, (10, 10))
                
                controls_text = "Controls: WASD/Arrows to move, Shift to run, E to complete task, ESC to quit"
                controls_surface = font.render(controls_text, True, WHITE)
                self.screen.blit(controls_surface, (10, 50))
                
                # Startup metrics controls
                metrics_text = "Startup: 1-3 Users (Shift to remove), 6-8 Money (Shift to remove)"
                metrics_surface = font.render(metrics_text, True, (200, 255, 200))
                self.screen.blit(metrics_surface, (10, 90))
                
                # Task controls
                task_text = "Tasks: F1-F5 to activate tasks"
                task_surface = font.render(task_text, True, (255, 215, 0))
                self.screen.blit(task_surface, (10, 130))
                
                # Show door info
                door_collision = self.check_door_collision()
                door_text = f"Door: ({int(self.door_x1)}, {int(self.door_y)}) to ({int(self.door_x2)}, {int(self.door_y + self.door_height)}) | Collision: {door_collision}"
                door_surface = font.render(door_text, True, (255, 255, 0) if door_collision else (200, 200, 200))
                self.screen.blit(door_surface, (10, 170))
                
                # Draw startup metrics bars
                self.draw_startup_metrics()
                
                # Draw tasks UI panel
                self.task_manager.draw_tasks_ui(self.screen)
            
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