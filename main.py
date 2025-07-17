#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escapist Game - Main Entry Point

A horror-style escape game with modular architecture.
All classes have been separated into individual modules for better maintainability.
"""

import pygame
import sys
from game import Game

def main():
    """
    Main function to initialize and run the game.
    """
    try:
        # Initialize Pygame
        pygame.init()
        
        # Create and run the game
        game = Game()
        game.run()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()