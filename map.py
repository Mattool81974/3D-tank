# Map.py
#
# ------------------ File used to handle the map ------------------
# Contains the Map class to handle the map.
# The Map class provides the graphic display of the map.
# Contains the MapGenerator class to generate a map.
#

# Import all necessary library
import pygame
import random
import struct

class MapGenerator:
    """Class used to generate a map
    """

    def __init__(self) -> None:
        """Construct a map generator
        """
        self.elements = {"nothing": 1, "tree": 2, "brick wall": 4, "player's tank": 7} # Every number for the map element with their names

        self.map_WIDTH = 505 # Width of the map (in square)
        self.map_HEIGHT = 505 # Height of the map (in square)

        self.player_tank_WIDTH = 5 # Width of the square of the player tank

    def generate(self, path: str = "map.agmff") -> None:
        """Generate a map, stored into the path

        Args:
            path (str, optional): path where the ap is stored. Defaults to "map.agmff".
        """
        binary_width = struct.pack("H", self.get_map_WIDTH())
        binary_height = struct.pack("H", self.get_map_HEIGHT()) # Store the size of the map
        binary_part = []

        current_element = 0
        current_number = 0
        last_element = 0
        last_number = 0
        i = 0
        j = 0
        while i < self.get_map_HEIGHT():
            while j < self.get_map_WIDTH(): # Check each square to see if the square content
                loop_element = ""
                if i >= (self.get_map_WIDTH() - self.get_player_tank_WIDTH()) / 2 and i < (self.get_map_WIDTH() + self.get_player_tank_WIDTH()) / 2 and j > (self.get_map_HEIGHT() - self.get_player_tank_WIDTH()) / 2 and j < (self.get_map_HEIGHT() + self.get_player_tank_WIDTH()) / 2:
                    # If we're on a user part
                    loop_element = self.get_elements("player's tank")
                    current_number += 1
                elif j == 252 and i == 199:
                    loop_element = self.get_elements("brick wall")
                    current_number += 1
                else:
                    """
                    elif i == 80 or i == 420 or j == 80 or j == 420:
                        loop_element = self.get_elements("tree")
                        current_number += 1
                    elif (i == 270 or i == 230) and (j <= 270 or j >= 230) and (i % 2 == 0 and j % 2 == 0):
                        loop_element = self.get_elements("tree")
                        current_number += 1
                    """
                    # If we're on an empty space
                    random_element = random.randint(0, 250)
                    if random_element == 0:
                        loop_element = self.get_elements("tree")
                    else:
                        loop_element = self.get_elements("nothing")
                    current_number += 1

                if loop_element != current_element: # If the last element was the last of it
                    last_element = current_element
                    last_number = current_number - 1
                    current_number = 1

                    if last_number > 0:
                        binary_part.append(struct.pack("I", last_number))
                        binary_part.append(struct.pack("b", last_element)) # Add the element

                current_element = loop_element
                j += 1
            j = 0
            i += 1

        if current_element != 0: # If the last element hasn't be added yet
            binary_part.append(struct.pack("I", current_number))
            binary_part.append(struct.pack("b", current_element)) # Add the element
            j += last_number - 1

        file = open(path, "wb") # Open the map file
        file.write(binary_width) # Write the datas of the map into the file
        file.write(binary_height)
        for b in binary_part: file.write(b)
        file.close() # Close the file

    def get_elements(self, name: str) -> int:
        """Return the number of an elements by its name

        Args:
            name (str): name of the element to return

        Returns:
            int: number of the elements to return
        """
        return self.elements[name]

    def get_map_HEIGHT(self) -> int:
        """Return the height of the map (in square)

        Returns:
            int: height of the map (in square)
        """
        return self.map_HEIGHT

    def get_map_WIDTH(self) -> int:
        """Return the width of the map (in square)

        Returns:
            int: width of the map (in square)
        """
        return self.map_WIDTH
    
    def get_player_tank_WIDTH(self) -> int:
        """Return the width of the player's tank on the map

        Returns:
            int: width of the player's tank on the map
        """
        return self.player_tank_WIDTH

class Map:
    """Class used to handle an in-game map
    """

    def __init__(self, game) -> None:
        """Construct an in-game map handler
        """
        self.elements = {"nothing": 1, "tree": 2, "brick wall": 4, "player's tank": 7} # Every number for the map element with their names
        self.game = game # Pointer towards the main Game object
        self.parts = [] # 2D list of every parts
        self.parts_data = {0: {"height": 0, "y": 0}, 2: {"height": 10, "y": 0}, 4: {"height": 5, "y": 0}} # Datas about a part of the map

        self.map_HEIGHT = 505 # Height of the map
        self.map_WIDTH = 505 # Width of the map

        self.load()

    def display2D(self) -> pygame.Surface:
        """Return a pygame Surface of the map displayed in 2D

        Returns:
            pygame.Surface: Surface of the map displayed in 2D
        """
        screen_width = self.game.get_SCREEN_WIDTH()
        screen_height = self.game.get_SCREEN_HEIGHT()

        color = {0: (0, 0, 0), 1: (0, 255, 0), 2: (25, 51, 0), 7: (255, 0, 0)}
        surface_to_return = pygame.Surface((self.get_map_WIDTH(), self.get_map_HEIGHT()), pygame.SRCALPHA) # Generate the surface

        for i in range(len(self.get_parts())):
            for j in range(len(self.get_parts()[i])): # Browse the parts
                pygame.draw.rect(surface_to_return, color[self.get_part(i, j)], (j, i, 1, 1))

        return pygame.transform.scale(surface_to_return, (screen_width, screen_height))
    
    def get_elements(self, element: str) -> int:
        """Return the number of an element with his name

        Args:
            element (str): name of an element

        Returns:
            int: number of an element with his name
        """
        if self.elements.__contains__(element):
            return self.elements[element]
        else:
            return 0
    
    def get_map_HEIGHT(self) -> int:
        """Return the height of the map

        Returns:
            int: height of the map
        """
        return self.map_HEIGHT
    
    def get_map_WIDTH(self) -> int:
        """Return the width of the map

        Returns:
            int: width of the map
        """
        return self.map_WIDTH
    
    def get_part(self, x: int, y: int) -> int:
        """Return the part at the x, y coordinates

        Args:
            x (int): x coordinates
            y (int): y coordinates

        Returns:
            int: elements at this coordinates
        """
        return self.get_parts()[y][x]

    def get_parts(self) -> list:
        """Return the 2D list of every parts

        Returns:
            list: 2D list of every parts
        """
        return self.parts
    
    def get_parts_data(self, part: int) -> dict:
        """Return the datas about a part of the map

        Args:
            part (int): part to analyze

        Returns:
            dict: datas about a part of the map
        """
        return self.parts_data[part]

    def load(self, path: str = "map.agmff") -> None:
        """Load the map

        Args:
            path (str, optional): path of the map to load. Defaults to "map.agmff".
        """
        file = open(path, "rb") # Open the map file
        content = file.read()
        file.close() # Close the file

        map_width = struct.unpack("H", content[:2])[0] # Read the width of the map
        map_height = struct.unpack("H", content[2:4])[0] # Read the height of the map

        self.map_HEIGHT = map_height # Defines the const size
        self.map_WIDTH = map_width

        start = 4
        total_size = 0
        while total_size < map_width * map_height: # While we haven't found the total number of map parts
            number = struct.unpack("I", content[start: start + 4])[0]
            element = struct.unpack("b", content[start + 4: start + 5])[0]

            current_list = [] # Create the current list to add ther parts ...
            if len(self.get_parts()) > 0: # Or get the last list in the parts if not completed
                current_list = self.get_parts()[-1]
            else:
                self.get_parts().append(current_list)

            for i in range(number): # Add all the elements
                if len(current_list) >= map_width:
                    current_list = []
                    self.get_parts().append(current_list)
                current_list.append(element)

            start += 5
            total_size += number