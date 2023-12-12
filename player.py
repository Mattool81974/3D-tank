# Player.py
#
# ---------------- File used to handle the player -----------------
# Contains the Player class to handle the player.
# The Player class provides the player handling.
#
#

# Import all necessary library
import math
import mmath
import pygame
import random
import struct

class Player:
    """Class used to handle the player behavior
    """

    def __init__(self, game) -> None:
        """Construct a player class
        """
        self.game = game

        self.player_turret_angle = 0 # Angle of the player (like the trigonometrical circle)
        self.turret_rotation_speed = 60 # Number of angle the turret turn by seconds

    def get_player_turret_angle(self) -> float:
        """Return the angle of the player (like the trigonometrical circle)

        Returns:
            float: angle of the player
        """
        return self.player_turret_angle
    
    def get_turret_rotation_speed(self) -> float:
        """Return the number of angle the turret turn by seconds

        Returns:
            float: number of angle the turret turn by seconds
        """
        return self.turret_rotation_speed
    
    def ray_cast(self, angle: float) -> float:
        """Return the length between the player and an object on an angle

        Args:
            angle (float): angle to do the ray-cast

        Returns:
            float: length between the object and the player
        """
        angle = mmath.normalize_angle(angle)
        base_pos = (252, 252)
        map_size = (self.game.get_map().get_map_WIDTH(), self.game.get_map().get_map_HEIGHT())
        vector_direction = mmath.direction_vector(angle)
        x_to_y = 100000
        if vector_direction[1] != 0: # Calculate the x ratio to y if y isn't 0
            x_to_y = vector_direction[0] / (vector_direction[1])

        verticals_intersection_length = mmath.distance2D(0, 0, 2, 2 / x_to_y)
        verticals_intersection_x = base_pos[0] # Calculate the vertical contact pos
        verticals_intersection_y = base_pos[1]

        horizontals_intersection_length = 0
        horizontals_intersection_x = base_pos[0] # Calculate the horizontal contact pos
        horizontals_intersection_y = base_pos[1]

        while verticals_intersection_x >= 0 and verticals_intersection_y >= 0 and verticals_intersection_x < map_size[0] and verticals_intersection_y < map_size[1] and (self.game.get_map().get_part(math.floor(verticals_intersection_y), verticals_intersection_x) == 1 or self.game.get_map().get_part(math.floor(verticals_intersection_y), verticals_intersection_x) == 7):
            # Ray-cast into the verticals axes
            if angle > 90 and angle < 270:
                verticals_intersection_x -= 1
                verticals_intersection_y += 1 / x_to_y
            else:
                verticals_intersection_x += 1
                verticals_intersection_y -= 1 / x_to_y
        
        while horizontals_intersection_x >= 0 and horizontals_intersection_y >= 0 and horizontals_intersection_x < map_size[0] and horizontals_intersection_y < map_size[1] and (self.game.get_map().get_part(horizontals_intersection_y, math.floor(horizontals_intersection_x)) == 1 or self.game.get_map().get_part(horizontals_intersection_y, math.floor(horizontals_intersection_x)) == 7):
            # Ray-cast into the horizontals axes
            if angle > 180:
                horizontals_intersection_x -= 1 * x_to_y
                horizontals_intersection_y += 1
            else:
                horizontals_intersection_x += 1 * x_to_y
                horizontals_intersection_y -= 1

        horizontals_intersection_length = mmath.distance2D(253, 253, horizontals_intersection_x, horizontals_intersection_y) #Calculate total distance
        verticals_intersection_length = mmath.distance2D(253, 253, verticals_intersection_x, verticals_intersection_y)
        
        if verticals_intersection_length < horizontals_intersection_length: # Return the nearest cast length
            return verticals_intersection_length, (verticals_intersection_x, verticals_intersection_y)
        return horizontals_intersection_length, (horizontals_intersection_x, horizontals_intersection_y)
    
    def turn_player_turret(self, delta_time: float, multiplicator: float = 1) -> None:
        """Turn the turret of the player tank

        Args:
            delta_time (float): time between the last frame and this frame
        """
        delta_time = delta_time / 1000
        self.player_turret_angle += delta_time * self.get_turret_rotation_speed() * multiplicator