import pygame
from constants import WIDTH, HEIGHT, BG_WIDTH, BG_HEIGHT

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