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
import sprite

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
        self.SCREEN_WIDTH = 505 # Width of the screen (const)
        self.SCREEN_HEIGHT = 505 # Height of the screen (const)

        pygame.init() # Activate the pygame display
        self.window = pygame.display.set_mode((self.get_SCREEN_WIDTH(), self.get_SCREEN_HEIGHT()))

        self.map = map.Map(self) # Create the map
        self.player = player.Player(self) # Create the player
        self.leopard2 = sprite.Sprite(self, (252, 200), 3, 8, "ressources/textures/leopard2.png") #Create a Leopard 2
        #self.leopard2 = sprite.Sprite(self, (275, 252), 3, 8, "ressources/textures/leopard2.png") #Create a Leopard 2

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
    
    def get_sprites(self) -> list:
        """Return a list of all the sprites in the game

        Returns:
            list: list of all the sprites in the game
        """
        return [self.leopard2]
    
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
                elif event.key == pygame.K_q:
                    self.pressed_keys.append("q")
                elif event.key == pygame.K_d:
                    self.pressed_keys.append("d")
                elif event.key == pygame.K_a:
                    self.pressed_keys.append("a")
                elif event.key == pygame.K_e:
                    self.pressed_keys.append("e")
            elif event.type == pygame.KEYUP: # If a key is released
                if event.key == pygame.K_LEFT and self.pressed_keys.count("left") > 0: # If the left arrow is pressed
                    self.pressed_keys.remove("left")
                elif event.key == pygame.K_RIGHT and self.pressed_keys.count("right") > 0:
                    self.pressed_keys.remove("right")
                elif event.key == pygame.K_q:
                    self.pressed_keys.remove("q")
                elif event.key == pygame.K_d:
                    self.pressed_keys.remove("d")
                elif event.key == pygame.K_a:
                    self.pressed_keys.remove("a")
                elif event.key == pygame.K_e:
                    self.pressed_keys.remove("e")
        
        if self.pressed_keys.count("left") > 0: # If the left arrow is pressed, turn at the left
            self.player.turn_turret(self.get_delta_time())
        
        if self.pressed_keys.count("right") > 0: # If the right arrow is pressed, turn at the right
            self.player.turn_turret(self.get_delta_time(), -1)

        if self.pressed_keys.count("q") > 0: # If the Q key is pressed, turn at left
            self.player.turn_commander_view(self.get_delta_time())
        
        if self.pressed_keys.count("d") > 0: # If the D key is pressed, turn at left
            self.player.turn_commander_view(self.get_delta_time(), -1)

        if self.pressed_keys.count("a") > 0: # Set commander view
            self.player.set_view(0)

        if self.pressed_keys.count("e") > 0: # Set shooter view
            self.player.set_view(1)

    def run(self) -> None:
        """Run the game
        """
        clock = pygame.time.Clock()
        self.surface = 0
        while self.get_running():
            self.handle_event() #Handle all the events during this frame
            if not self.get_running(): break # If the user wants to quit

            self.game_surface = self.player.projection3D()
            self.window.blit(self.game_surface, (0, 0, self.game_surface.get_width(), self.game_surface.get_height()))

            pygame.display.flip() # Update the pygame window

            self.delta_time = clock.get_time() # Update the frame between each frame
            #if clock.get_time() != 0: print(1000/clock.get_time())
            clock.tick(250)

m = map.MapGenerator()
m.generate()

# If the user directyl executes the file
if __name__ == "__main__":
    # Create and run a game object
    game = Game()
    game.run()