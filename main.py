# Main.py
#
# ----------------------- Main project file -----------------------
# Contains the Game class to create the game.
# The Game class doesn't provide the physic and graphic display.
#
#

# Import all necessary library
import pygame
import map

class Game:
    """Main class to run the game
    """

    def __init__(self) -> None:
        """Create a game object
        """
        self.SCREEN_WIDTH = 800 # Width of the screen (const)
        self.SCREEN_HEIGHT = 600 # Height of the screen (const)

    def get_SCREEN_HEIGHT(self) -> int:
        """Return the height of the screen

        Returns:
            int: height of the screen
        """
        return self.SCREEN_HEIGHT

    def get_SCREEN_WIDTH(self) -> int:
        """Return the width of the screen

        Returns:
            int: width of the screen
        """
        return self.SCREEN_WIDTH

    def run(self) -> None:
        """Run the game
        """
        pygame.display.flip()

# If the user directyl executes the file
if __name__ == "__main__":
    # Create and run a game object
    game = Game()
    game.run()