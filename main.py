import pygame
# import sys  ← больше не нужен

from game import Game
from starting_page import StartingPage

def main():
    try:
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for audio
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Escapist Game")

        starting_page = StartingPage()
        result = starting_page.run()

        if result == "start_game":
            game = Game()
            game.run()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        # sys.exit(0)  ← удалить

if __name__ == "__main__":
    main()
