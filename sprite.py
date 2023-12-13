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
import pygame
import random
import struct

class Sprite:
    """Class used to handle a sprite
    """

    def __init__(self, game, pos: tuple, length: float = 10) -> None:
        """Construct a sprite

        Args:
            game: main game object
            pos (tuple): pos of the sprite in the map
        """
        self.game = game

        self.length = length
        self.pos = pos # Pos of the sprite

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