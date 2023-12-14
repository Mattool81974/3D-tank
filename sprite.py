# Sprite.py
#
# ---------------- File used to handle a sprite -------------------
# Contains the Player class to handle the player.
# The Player class provides the player handling.
#
#

# Import all necessary library
import math
import mmath
import os
import pygame
import random
import struct

class Sprite:
    """Class used to handle a sprite
    """

    def __init__(self, game, pos: tuple, height: float = 1, length: float = 10, texture_path = "") -> None:
        """Construct a sprite

        Args:
            game: main game object
            pos (tuple): pos of the sprite in the map
        """
        self.game = game

        self.height = height
        self.length = length
        self.pos = pos # Pos of the sprite
        self.texture = 0
        self.texture_column = []
        self.texture_size = (0, 0)
        self.texture_path = texture_path

        self.load_texture(self.get_texture_path())

    def get_height(self) -> float:
        """Return the height of the sprite

        Returns:
            float: height of the sprite
        """
        return self.height

    def get_length(self) -> float:
        """Return the length of the sprite

        Returns:
            float: length of the sprite
        """
        return self.length

    def get_pos(self) -> tuple:
        """Return the pos of the sprite

        Returns:
            tuple: pos of the sprite
        """
        return self.pos
    
    def get_texture(self) -> pygame.Surface:
        """Return the surface of the texture

        Returns:
            pygame.Surface: surface of the texture
        """
        return self.texture
    
    def get_texture_column(self, y: int) -> pygame.Surface:
        """Return a column of the texture

        Args:
            y (int): y pos of the texture

        Returns:
            pygame.Surface: column of the texture
        """
        return self.texture_column[y]
    
    def get_texture_size(self) -> tuple:
        """Return the size of the texture

        Returns:
            tuple: size of the texture
        """
        return self.texture_size
    
    def get_texture_path(self) -> str:
        """Return the path towars the sprite texture

        Returns:
            str: path towars the sprite texture
        """
        return self.texture_path
    
    def load_texture(self, texture_path: str) -> None:
        """Load the texture of the sprite

        Args:
            texture_path (str): texture of the sprite
        """
        if self.get_texture_path() != "" and os.path.exists(self.get_texture_path()):
            self.texture = pygame.image.load(self.get_texture_path())
            self.texture_column.clear()
            self.texture_size = (self.texture.get_width(), self.texture.get_height())

            for i in range(self.get_texture_size()[0]): # Cut the texture into column
                new_surface = pygame.Surface((1, self.texture_size[1]), pygame.SRCALPHA)

                for j in range(self.get_texture_size()[1]):
                    pygame.draw.rect(new_surface, self.texture.get_at((i, j)), (0, j, 1, 1))

                self.texture_column.append(new_surface)