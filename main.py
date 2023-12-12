# Main.py
#
# ----------------------- Main project file -----------------------
# Contains the Game class to create the game.
# The Game class provides assembles the graphics parts.
#
#

# Import all necessary library
import map
import mmath
import player
import pygame

class Game:
    """Main class to run the game
    """

    def __init__(self) -> None:
        """Create a game object
        """
        self.delta_time = 0 # Time between the last frame and this frame
        self.game_surface = 0 # Main graphics pygame Surface of the game
        self.pressed_keys = [] # List of all pressed keys
        self.running = True # If the game is running
        self.SCREEN_WIDTH = 1010 # Width of the screen (const)
        self.SCREEN_HEIGHT = 1010 # Height of the screen (const)

        pygame.init() # Activate the pygame display
        self.window = pygame.display.set_mode((self.get_SCREEN_WIDTH(), self.get_SCREEN_HEIGHT()))

        self.map = map.Map(self) # Create the map
        self.player = player.Player(self) # Create the player

    def get_delta_time(self) -> float:
        """Return the time between the last frame and this frame

        Returns:
            float: time between the last frame and this frame
        """
        return self.delta_time
    
    def get_game_surface(self) -> pygame.Surface:
        """Return the main surface of the game

        Returns:
            pygame.Surface: main surface of the game
        """
        return self.game_surface
    
    def get_map(self) -> map.Map:
        """Return the main Map in the game

        Returns:
            map.Map: main Map in the game
        """
        return self.map

    def get_running(self) -> bool:
        """Return if the game is running

        Returns:
            bool: if the game is running
        """
        return self.running

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
    
    def get_window(self) -> pygame.Surface:
        """Return the main window of the game

        Returns:
            pygame.Surface: main window of the game
        """
        return self.window
    
    def handle_event(self) -> None:
        """Handle the games event
        """
        events = pygame.event.get()
        for event in events: # Browse the events
            if event.type == pygame.QUIT:
                pygame.quit() # Quit pygame if the user wants to
                self.running = False
            elif event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_LEFT: # If the left arrow is pressed
                    self.pressed_keys.append("left")
                elif event.key == pygame.K_RIGHT:
                    self.pressed_keys.append("right")
            elif event.type == pygame.KEYUP: # If a key is released
                if event.key == pygame.K_LEFT and self.pressed_keys.count("left") > 0: # If the left arrow is pressed
                    self.pressed_keys.remove("left")
                elif event.key == pygame.K_RIGHT and self.pressed_keys.count("right") > 0:
                    self.pressed_keys.remove("right")
        
        if self.pressed_keys.count("left") > 0: #If the left arrow is pressed, turn at the left
            self.player.turn_player_turret(self.get_delta_time())
        
        if self.pressed_keys.count("right") > 0: #If the right arrow is pressed, turn at the right
            self.player.turn_player_turret(self.get_delta_time(), -1)

    def run(self) -> None:
        """Run the game
        """
        clock = pygame.time.Clock()
        self.surface = 0
        while self.get_running():
            self.handle_event() #Handle all the events during this frame
            if not self.get_running(): break # If the user wants to quit

            if self.surface == 0:
                self.surface = self.map.display2D()

            self.game_surface = self.surface.copy()

            raycast = self.player.ray_cast(self.player.get_player_turret_angle())
            vector = mmath.direction_vector(self.player.get_player_turret_angle())
            pygame.draw.line(self.game_surface, (255, 0, 0), ((self.get_SCREEN_WIDTH() - 1) / 2, (self.get_SCREEN_HEIGHT() - 1) / 2), (raycast[1][0] * (self.get_SCREEN_WIDTH() / self.get_map().get_map_WIDTH()), raycast[1][1] * (self.get_SCREEN_HEIGHT() / self.get_map().get_map_HEIGHT())), 2)
            
            self.window.blit(self.game_surface, (0, 0, self.game_surface.get_width(), self.game_surface.get_height()))

            pygame.display.update() # Update the pygame window

            self.delta_time = clock.get_time() # Update the frame between each frame
            clock.tick(60)

m = map.MapGenerator()
m.generate()

# If the user directyl executes the file
if __name__ == "__main__":
    # Create and run a game object
    game = Game()
    game.run()