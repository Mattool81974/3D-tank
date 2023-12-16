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
        self.commander_view_elevation = 0
        self.commander_view_elevation_maximum = self.game.get_map().get_map_WIDTH() // 2.2
        self.commander_view_elevation_minimum = -100
        self.commander_view_elevation_speed = 100 # Speed of the commander view elevation speed
        self.commander_view_fov = 45 # FOV of the commander view
        self.commander_view_rotation_speed = 180 # Number of angle the commander view turn by seconds
        self.floor_offset = game.get_map().get_map_HEIGHT() // 2
        self.fov = 45
        self.screen_distance = (math.ceil(self.game.get_map().get_map_WIDTH() / 2) / math.tan(math.radians(self.get_fov() / 2)))
        self.shooter_view_fov = 10 # FOV of the shooter viewn
        self.turret_angle = 0 # Angle of the player (like the trigonometrical circle)
        self.turret_rotation_speed = 60 # Number of angle the turret turn by seconds
        self.view = 0 # Current view of the player
        self.y_offset = 1 # Offset of the y

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
    
    def get_commander_view_elevation(self) -> float:
        """Return the elevation of the commander view

        Returns:
            float: elevation of the commander view
        """
        return self.commander_view_elevation
    
    def get_commander_view_elevation_speed(self) -> float:
        """Return the speed of the elevation of the commander view

        Returns:
            float: speed of the elevation of the commander view
        """
        return self.commander_view_elevation_speed
    
    def get_commander_view_elevation_maximum(self) -> float:
        """Return the max angle of the elevation angle

        Returns:
            float: max angle of the elevation angle
        """
        return self.commander_view_elevation_maximum
    
    def get_commander_view_elevation_minimum(self) -> float:
        """Return the min angle of the elevation angle

        Returns:
            float: min angle of the elevation angle
        """
        return self.commander_view_elevation_minimum
    
    def get_commander_view_fov(self) -> float:
        """Return the fov of the commander view

        Returns:
            float: fov of the commander view
        """
        return self.commander_view_fov
    
    def get_commander_view_rotation_speed(self) -> float:
        """Return the number of angle the commander view turn by seconds

        Returns:
            float: number of angle the commander view turn by seconds
        """
        return self.commander_view_rotation_speed
    
    def get_floor_offset(self) -> float:
        """Return thr offset of the floor

        Returns:
            float: offset of the floor
        """
        return self.floor_offset
    
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
    
    def get_shooter_view_fov(self) -> float:
        """Return the shooter view fov

        Returns:
            float: shooter view fov
        """
        return self.shooter_view_fov

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
    
    def get_y_offset(self) -> float:
        """Return the y offset

        Returns:
            float: y offset
        """
        return self.y_offset
    
    def projection3D(self) -> pygame.Surface:
        """Return a pygame surface with the 3D projection on it

        Returns:
            pygame.Surface: surface with the 3D projection on it
        """
        raycast = self.ray_cast_commander_view() # Do the raycast for the commander view
        map_size = (self.game.get_map().get_map_WIDTH(), self.game.get_map().get_map_HEIGHT())
        floor_offset = map_size[0] - self.get_floor_offset() # Get the offset of the floor
        screen_size = (self.game.get_SCREEN_WIDTH(), self.game.get_SCREEN_HEIGHT())
        surface_to_return = pygame.Surface((map_size[0], map_size[1]), pygame.SRCALPHA) # Generate the surface
        surface_to_return.fill((0, 0, 0))
        pygame.draw.rect(surface_to_return, (0, 0, 255), (0, 0, map_size[0], map_size[1]))
        pygame.draw.rect(surface_to_return, (0, 255, 0), (0, floor_offset, map_size[0], map_size[1] - floor_offset))

        sprites = self.game.get_sprites()
        sprites_angles = {}
        sprites_length = {}
        for s in sprites: # Calculate how to display the sprite
            angle = mmath.normalize_angle(math.degrees(math.atan(abs(self.get_base_pos()[0] - s.get_pos()[0]) / abs(self.get_base_pos()[1] - s.get_pos()[1]))))
            if angle > 270: angle = 360 - angle
            elif angle > 180: angle += 180
            elif angle > 90: angle = 180 - angle
            sprites_angles[s] = angle + 180
            sprites_length[s] = mmath.distance2D(self.get_base_pos()[0], self.get_base_pos()[1], s.get_pos()[0], s.get_pos()[1])

        i = 0
        scale = math.ceil(map_size[0] / len(raycast))
        for r in raycast: # Calculate with each raycast
            length = r[0]
            pos = r[1]
            part = r[2]
            side = r[3]
            angle = r[4]

            sprite_length = -1
            
            sprites_displayed = 0
            visibles_sprites = 0
            for s in sprites: # Calculate if the sprite should be displayed and how
                angle_sprite = mmath.normalize_angle(sprites_angles[s])
                length_sprite = sprites_length[s]
                fov_sprites = math.degrees(math.atan((s.get_length() / 2) / length_sprite))
                if sprite_length > length_sprite or sprite_length == -1:
                    if angle > mmath.normalize_angle(angle_sprite - fov_sprites) and angle < mmath.normalize_angle(angle_sprite + fov_sprites): # If the sprite is on the angle
                        sprites_displayed = abs(angle - (angle_sprite - fov_sprites)) / (fov_sprites * 2)
                        visibles_sprites = s
                        sprite_length = length_sprite
                    elif mmath.normalize_angle(angle_sprite + fov_sprites) < mmath.normalize_angle(angle_sprite - fov_sprites) and (angle < mmath.normalize_angle(angle_sprite + fov_sprites) or angle > mmath.normalize_angle(angle_sprite - fov_sprites)): # If the sprite is on the angle (other way)
                        sprites_displayed = mmath.normalize_angle(angle - (angle_sprite - fov_sprites)) / (fov_sprites * 2)
                        visibles_sprites = s
                        sprite_length = length_sprite

            if sprite_length > length:
                if visibles_sprites != 0: # Draw a sprites if necessary
                    height = (self.get_screen_distance() / (sprite_length + 0.000001)) # Calculate the projection height
                    final_height = height * visibles_sprites.get_height() * (self.get_commander_view_fov() / self.get_fov())

                    texture_x = math.floor(sprites_displayed * visibles_sprites.get_texture_size()[0])

                    y = -height * self.get_y_offset() * (self.get_commander_view_fov() / self.get_fov()) * ((map_size[1] - floor_offset) / (map_size[1] // 2)) # Calculate the y pos of the part (assuming y inversed)
                    y = map_size[1] - ((map_size[0] - floor_offset) + y + math.floor(final_height)) # Inverse y

                    color = (0, 0, 0)
                    for j in range(scale):
                        surface_to_return.blit(pygame.transform.scale(visibles_sprites.get_texture_column(texture_x), (1, final_height)), (i * scale + j, y, 1, final_height))
            
            if part != 0:
                height = (self.get_screen_distance() / (length + 0.000001)) # Calculate the projection height
                datas = self.game.get_map().get_parts_data(r[2])
                final_height = height * datas["height"] * (self.get_commander_view_fov() / self.get_fov()) # Calculate the real height

                y = -height * self.get_y_offset() * (self.get_commander_view_fov() / self.get_fov()) * ((map_size[1] - floor_offset) / (map_size[1] // 2)) # Calculate the y pos of the part (assuming y inversed)
                y = map_size[1] - ((map_size[0] - floor_offset) + y + math.floor(final_height)) # Inverse y

                color = (255 / (math.sqrt(length)), 255 / math.sqrt(length), 255 / (math.sqrt(length)))
                if length < 0: color = (255, 255, 255)

                test_pos_x = 0 # Calculate the relative pos on the texture
                if side == 0 or side == 2:
                    test_pos_x = abs(pos[0] - math.floor(pos[0])) # Calculate the color of the tree
                else:
                    test_pos_x = abs(pos[1] - math.floor(pos[1]))

                if part == self.game.get_map().get_elements("tree"):
                    if test_pos_x < 0.2 or test_pos_x > 0.8:
                        color = (51, 25, 0)
                    else:
                        color = (102, 51, 0)
                elif part == self.game.get_map().get_elements("brick wall"):
                    if math.floor(test_pos_x * 5) % 2 == 0:
                        color = (255, 51, 51)
                    else:
                        color = (128, 128, 128)

                pygame.draw.rect(surface_to_return, color, (i * scale, y, scale, final_height))

            if sprite_length <= length:
                if visibles_sprites != 0: # Draw a sprites if necessary
                    height = (self.get_screen_distance() / (sprite_length + 0.000001)) # Calculate the projection height
                    final_height = height * visibles_sprites.get_height() * (self.get_commander_view_fov() / self.get_fov())

                    texture_x = math.floor(sprites_displayed * visibles_sprites.get_texture_size()[0])

                    y = -height * self.get_y_offset() * (self.get_commander_view_fov() / self.get_fov()) * ((map_size[1] - floor_offset) / (map_size[1] // 2)) # Calculate the y pos of the part (assuming y inversed)
                    y = map_size[1] - ((map_size[0] - floor_offset) + y + math.floor(final_height)) # Inverse y

                    color = (0, 0, 0)
                    for j in range(scale):
                        surface_to_return.blit(pygame.transform.scale(visibles_sprites.get_texture_column(texture_x), (1, final_height)), (i * scale + j, y, 1, final_height))
            i += 1

        if self.get_view() == 1: # Add a binocualr effect
            surface_to_return.blit(self.get_binoculars(), (0, 0, surface_to_return.get_width(), surface_to_return.get_height()))

        return pygame.transform.scale(surface_to_return, (screen_size[0], screen_size[1]))
    
    def raise_commander_view(self, delta_time: float, multiplicator: float = 1) -> None:
        """Raise the commander view

        Args:
            delta_time (float): time between the last frame and this frame
            multiplicator (float, optional): value to multiplie for turning. Defaults to 1.
        """
        new_angle = self.get_commander_view_elevation() + self.get_commander_view_elevation_speed() * delta_time * multiplicator
        print(new_angle)
        if new_angle > self.get_commander_view_elevation_maximum(): new_angle = self.get_commander_view_elevation_maximum() # Adjust the angle
        if new_angle < self.get_commander_view_elevation_minimum(): new_angle = self.get_commander_view_elevation_minimum()
        self.commander_view_elevation = new_angle
        self.floor_offset = self.game.get_map().get_map_HEIGHT() // 2 + self.get_commander_view_elevation()
    
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
            result.append(self.ray_cast(angle - (-(fov / 2) + fov*((i + 1)/fov_raycast))))

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
            self.fov = self.get_commander_view_fov()
        elif self.get_view() == 1:
            self.fov = self.get_shooter_view_fov()
    
    def turn_commander_view(self, delta_time: float, multiplicator: float = 1) -> None:
        """Turn the commander view

        Args:
            delta_time (float): time between the last frame and this frame
            multiplicator (float, optional): value to multiplie for turning. Defaults to 1.
        """
        self.commander_view_angle += delta_time * self.get_commander_view_rotation_speed() * multiplicator
    
    def turn_turret(self, delta_time: float, multiplicator: float = 1) -> None:
        """Turn the turret of the player tank

        Args:
            delta_time (float): time between the last frame and this frame
            multiplicator (float, optional): value to multiplie for turning. Defaults to 1.
        """
        delta_time = delta_time / 1000
        self.turret_angle += delta_time * self.get_turret_rotation_speed() * multiplicator