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

        Args:
            game: main game object
        """
        self.game = game

        self.binoculars = 0 # Surface of a binocular effect
        self.commander_view_angle = 0 # Angle of the commander view (like the trigonometrical circle)
        self.commander_view_rotation_speed = 180 # Number of angle the commander view turn by seconds
        self.fov = 45
        self.screen_distance = (math.ceil(self.game.get_map().get_map_WIDTH() / 2) / math.tan(math.radians(self.get_fov() / 2)))
        self.turret_angle = 0 # Angle of the player (like the trigonometrical circle)
        self.turret_rotation_speed = 60 # Number of angle the turret turn by seconds
        self.view = 0 # Current view of the player

        self.generate_binoculars()

    def generate_binoculars(self) -> None:
        """Generate a binoculars surface
        """
        map_size = (self.game.get_map().get_map_WIDTH(), self.game.get_map().get_map_HEIGHT())

        self.binoculars = pygame.Surface(map_size, pygame.SRCALPHA)
        self.binoculars.fill((0, 0, 0))
        pygame.draw.circle(self.binoculars, (0, 0, 0, 0), (math.floor(map_size[0] / 3), math.floor(map_size[0] / 2)), math.floor(map_size[0] / 3))
        pygame.draw.circle(self.binoculars, (0, 0, 0, 0), (math.ceil(map_size[0] / (3/2)), math.floor(map_size[0] / 2)), math.floor(map_size[0] / 3))

    def get_base_pos(self) -> tuple:
        """Return the base pos of the player

        Returns:
            tuple: base pos of the player
        """
        return self.base_pos

    def get_binoculars(self) -> str:
        """Return a binocular surface

        Returns:
            str: binocular surface
        """
        return self.binoculars

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

        sprites = self.game.get_sprites()
        sprites_angles = {}
        sprites_length = {}
        for s in sprites:
            angle = mmath.normalize_angle(math.degrees(math.atan(abs(self.get_base_pos()[0] - s.get_pos()[0]) / abs(self.get_base_pos()[1] - s.get_pos()[1]))))
            if angle > 270: angle = 360 - angle
            elif angle > 180: angle += 180
            elif angle > 90: angle = 180 - angle
            sprites_angles[s] = angle
            sprites_length[s] = mmath.distance2D(self.get_base_pos()[0], self.get_base_pos()[1], s.get_pos()[0], s.get_pos()[1])

        i = 0
        for r in raycast: # Calculate with each raycast
            length = r[0]
            pos = r[1]
            part = r[2]
            side = r[3]
            angle = r[4]
            
            visibles_sprites = []
            for s in sprites:
                angle_sprite = sprites_angles[s]
                length_sprite = sprites_length[s]
                zoom = (self.get_screen_distance() / (length_sprite + 0.000001))
                fov_sprites = math.degrees(math.atan((s.get_length() / 2) / length_sprite))
                if angle_sprite > angle - fov_sprites and angle_sprite < angle + fov_sprites:
                    visibles_sprites.append(s)

            if part != 0:
                height = (self.get_screen_distance() / (length + 0.000001)) # Calculate the projection height
                datas = self.game.get_map().get_parts_data(r[2])
                final_height = height * datas["height"] # Calculate the real height
                scale = map_size[0] / len(raycast)

                color = (255 / (math.sqrt(length)), 255 / math.sqrt(length), 255 / (math.sqrt(length)))
                if length < 0: color = (255, 255, 255)

                if part == self.game.get_map().get_elements("tree"):
                    if side == 0 or side == 2:
                        test_pos = abs(pos[0] - math.floor(pos[0])) # Calculate the color of the tree
                    else:
                        test_pos = abs(pos[1] - math.floor(pos[1]))

                    if test_pos < 0.2 or test_pos > 0.8:
                        color = (51, 25, 0)
                    else:
                        color = (102, 51, 0)

                pygame.draw.rect(surface_to_return, color, (i * scale, map_size[1] // 2 - (final_height) // 2, scale * 2, final_height))
            i += 1

        if self.get_view() == 1: # Add a binocualr effect
            surface_to_return.blit(self.get_binoculars(), (0, 0, surface_to_return.get_width(), surface_to_return.get_height()))

        return pygame.transform.scale(surface_to_return, (screen_size[0], screen_size[1]))
    
    def ray_cast(self, angle: float, fov: float = 0, fov_raycast: float = 0) -> list:
        """Return the length between the player and an object on an angle

        Args:
            angle (float): angle to do the ray-cast
            fov (float, optional): fov of the raycast. Defaults to 0.
            fov_raycast (float, optional): number of raycast in the FOV. Defaults to 0.

        Returns:
            list: list of element containing the length between the object and the player, a list of point, the part touched and the side touched
        """
        angle = mmath.normalize_angle(angle)
        map_size = (self.game.get_map().get_map_WIDTH(), self.game.get_map().get_map_HEIGHT())

        self.base_pos = (math.ceil(map_size[0] / 2), math.ceil(map_size[1] / 2))
        
        if fov == 0: # If we don't need a FOV
            vector_direction = mmath.direction_vector(angle)
            x_to_y = 100000
            if vector_direction[1] != 0: # Calculate the x ratio to y if y isn't 0
                x_to_y = vector_direction[0] / (vector_direction[1])

            verticals_intersection_length = mmath.distance2D(0, 0, 2, 2 / x_to_y)
            verticals_intersection_x = self.get_base_pos()[0] # Calculate the vertical contact pos
            verticals_intersection_y = self.get_base_pos()[1]

            horizontals_intersection_length = 0
            horizontals_intersection_x = self.get_base_pos()[0] # Calculate the horizontal contact pos
            horizontals_intersection_y = self.get_base_pos()[1]

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

            real_horizontals_intersection_length = -1
            horizontals_intersection_length = mmath.distance2D(self.get_base_pos()[0], self.get_base_pos()[1], horizontals_intersection_x, horizontals_intersection_y) #Calculate total horizontal distance
            if horizontals_intersection_x >= 0 and horizontals_intersection_y >= 0 and horizontals_intersection_x < map_size[0] and horizontals_intersection_y < map_size[1]:
                real_horizontals_intersection_length = horizontals_intersection_length

            real_verticals_intersection_length = -1
            verticals_intersection_length = mmath.distance2D(self.get_base_pos()[0], self.get_base_pos()[1], verticals_intersection_x, verticals_intersection_y) # Calculate total vertical distance
            if verticals_intersection_x >= 0 and verticals_intersection_y >= 0 and verticals_intersection_x < map_size[0] and verticals_intersection_y < map_size[1]:
                real_verticals_intersection_length = verticals_intersection_length

            vertical_or_horizontal = "h"

            if verticals_intersection_length < horizontals_intersection_length: # Return the nearest cast length
                vertical_or_horizontal = "v"
            
            side = 0
            if angle < 180: # Calculate the touched side
                if vertical_or_horizontal == "h":
                    side = 2
                else:
                    if angle < 90:
                        side = 1
                    else:
                        side = 3
            else:
                if vertical_or_horizontal == "h":
                    side = 0
                else:
                    if angle > 270:
                        side = 1
                    else:
                        side = 3

            part = 0
            if vertical_or_horizontal == "v": # Return the nearest cast length
                if real_verticals_intersection_length != -1:
                    part = self.game.get_map().get_part(math.floor(verticals_intersection_y), verticals_intersection_x)
                return real_verticals_intersection_length, (verticals_intersection_x, verticals_intersection_y), part, side, angle
            
            if real_horizontals_intersection_length != -1:
                part = self.game.get_map().get_part(horizontals_intersection_y, math.floor(horizontals_intersection_x))
            return real_horizontals_intersection_length, (horizontals_intersection_x, horizontals_intersection_y), part, side, angle
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