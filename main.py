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
from starting_page import StartingPage

def main():
    """
    Main function to initialize and run the game.
    """
    try:
        # Initialize Pygame
        pygame.init()
        
        # Show starting page first
        starting_page = StartingPage()
        result = starting_page.run()
        
        if result == "start_game":
            # Create and run the actual game
            game = Game()
            game.run()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()