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

        self.commander_view_angle = 0 # Angle of the commander view (like the trigonometrical circle)
        self.commander_view_rotation_speed = 180 # Number of angle the commander view turn by seconds
        self.fov = 45
        self.screen_distance = (math.ceil(self.game.get_map().get_map_WIDTH() / 2) / math.tan(math.radians(self.get_fov() / 2)))
        self.turret_angle = 0 # Angle of the player (like the trigonometrical circle)
        self.turret_rotation_speed = 60 # Number of angle the turret turn by seconds
        self.view = 0 # Current view of the player

    def get_commander_view_angle(self) -> float:
        """Return the angle of the commander view (like the trigonometrical circle)

        Returns:
            float: angle of thecommander view
        """
        return self.commander_view_angle
    
    def get_commander_view_rotation_speed(self) -> float:
        """Return the number of angle the commander view turn by seconds

        Returns:
            float: number of angle the commander view turn by seconds
        """
        return self.commander_view_rotation_speed
    
    def get_fov(self) -> float:
        """Return the FOV of the player view

        Returns:
            float: FOV of the player view
        """
        return self.fov
    
    def get_screen_distance(self) -> float:
        """Return the distance of the projection screen from the player

        Returns:
            float: distance of the projection screen from the player
        """
        return self.screen_distance

    def get_turret_angle(self) -> float:
        """Return the angle of the player (like the trigonometrical circle)

        Returns:
            float: angle of the player
        """
        return self.turret_angle
    
    def get_turret_rotation_speed(self) -> float:
        """Return the number of angle the turret turn by seconds

        Returns:
            float: number of angle the turret turn by seconds
        """
        return self.turret_rotation_speed
    
    def get_view(self) -> int:
        """Return the current view of the player

        Returns:
            int: current view of the player
        """
        return self.view
    
    def projection3D(self) -> pygame.Surface:
        """Return a pygame surface with the 3D projection on it

        Returns:
            pygame.Surface: surface with the 3D projection on it
        """
        raycast = self.ray_cast_commander_view() # Do the raycast for the commander view
        map_size = (self.game.get_map().get_map_WIDTH(), self.game.get_map().get_map_HEIGHT())
        screen_size = (self.game.get_SCREEN_WIDTH(), self.game.get_SCREEN_HEIGHT())
        surface_to_return = pygame.Surface((map_size[0], map_size[1]), pygame.SRCALPHA) # Generate the surface
        surface_to_return.fill((0, 0, 0))
        pygame.draw.rect(surface_to_return, (0, 255, 0), (0, math.floor(map_size[0] / 2), map_size[0], math.ceil(map_size[1] / 2)))
        pygame.draw.rect(surface_to_return, (0, 0, 255), (0, 0, map_size[0], math.ceil(map_size[1] / 2)))

        i = 0
        for r in raycast: # Calculate with each raycast
            length = r[0]

            height = (self.get_screen_distance() / (length + 0.000001)) * 5 # Calculate the projection height
            scale = map_size[0] / len(raycast)

            color = (255 / (math.sqrt(length)), 255 / math.sqrt(length), 255 / (math.sqrt(length)))
            if length < 0: color = (255, 255, 255)
            pygame.draw.rect(surface_to_return, color, (i * scale, map_size[1] // 2 - (height) // 2, scale * 2, height))
            i += 1

        return pygame.transform.scale(surface_to_return, (screen_size[0], screen_size[1]))
    
    def ray_cast(self, angle: float, fov: float = 0, fov_raycast: float = 0) -> list:
        """Return the length between the player and an object on an angle

        Args:
            angle (float): angle to do the ray-cast
            fov (float, optional): fov of the raycast. Defaults to 0.
            fov_raycast (float, optional): number of raycast in the FOV. Defaults to 0.

        Returns:
            list: list of element containing the length between the object and the player and a list of point
        """
        angle = mmath.normalize_angle(angle)
        map_size = (self.game.get_map().get_map_WIDTH(), self.game.get_map().get_map_HEIGHT())

        base_pos = (math.ceil(map_size[0] / 2), math.ceil(map_size[1] / 2))
        
        if fov == 0: # If we don't need a FOV
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

            horizontals_intersection_length = mmath.distance2D(base_pos[0], base_pos[1], horizontals_intersection_x, horizontals_intersection_y) #Calculate total distance
            verticals_intersection_length = mmath.distance2D(base_pos[0], base_pos[1], verticals_intersection_x, verticals_intersection_y)
            
            if verticals_intersection_length < horizontals_intersection_length: # Return the nearest cast length
                return verticals_intersection_length, (verticals_intersection_x, verticals_intersection_y)
            return horizontals_intersection_length, (horizontals_intersection_x, horizontals_intersection_y)
        # If we need a FOV
        result = []
        for i in range(fov_raycast): # Do FOV raycast
            result.append(self.ray_cast(angle - ((fov / 2) + fov*(i/fov_raycast))))

        return result # Return the result
    
    def ray_cast_commander_view(self) -> tuple:
        """Return the length between the commander view and an object on an angle

        Returns:
            tuple: tuple of element containing the length between the object and the turret and a list of point
        """
        return self.ray_cast(self.get_commander_view_angle(), self.get_fov(), 255)
    
    def ray_cast_turret(self) -> tuple:
        """Return the length between the turret and an object on an angle

        Returns:
            tuple: tuple of element containing the length between the object and the turret and a list of point
        """
        return self.ray_cast(self.get_turret_angle())
    
    def set_view(self, view: int) -> None:
        """Change the current player view

        Args:
            view (int): new current player view.
                        If 0, commander view.
                        If 1, shooter view.
        """
        self.view = view
        if self.get_view() == 0:
            self.fov = 45
        elif self.get_view() == 1:
            self.fov = 10
    
    def turn_commander_view(self, delta_time: float, multiplicator: float = 1) -> None:
        """Turn the commander view

        Args:
            delta_time (float): time between the last frame and this frame
            multiplicator (float, optional): value to multiplie for turning. Defaults to 1.
        """
        delta_time = delta_time / 1000
        self.commander_view_angle += delta_time * self.get_commander_view_rotation_speed() * multiplicator
    
    def turn_turret(self, delta_time: float, multiplicator: float = 1) -> None:
        """Turn the turret of the player tank

        Args:
            delta_time (float): time between the last frame and this frame
            multiplicator (float, optional): value to multiplie for turning. Defaults to 1.
        """
        delta_time = delta_time / 1000
        self.turret_angle += delta_time * self.get_turret_rotation_speed() * multiplicator