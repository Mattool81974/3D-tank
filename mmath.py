# MMath.py
#
# -------------------- File used to do some math ------------------
# Contains some math functions.
#
#
#

# Import all necessary library
import math

def direction_vector_from_radian(radian: float) -> tuple:
    """Return the direction vector with a norm of 1, with an radian

    Args:
        radian (float): radian to test, same as trigonometrical circle

    Returns:
        tuple: direction vector
    """
    return (math.cos(radian), math.sin(radian))

def direction_vector(angle: float) -> tuple:
    """Return the direction vector with a norm of 1, with an angle

    Args:
        angle (float): angle to test, same as trigonometrical circle

    Returns:
        tuple: direction vector
    """
    return direction_vector_from_radian((angle/180)*math.pi)

def distance2D(x0: float, y0: float, x1: float, y1: float) -> float:
    """Return the distance between 2 point

    Args:
        x0 (float): x pos of the first point
        y0 (float): y pos of the first point
        x1 (float): x pos of the second point
        y1 (float): y pos of the second point

    Returns:
        float: distance between the 2 points
    """
    return math.sqrt(pow(x1 - x0, 2) + pow(y1 - y0, 2))

def normalize_angle(angle: float) -> float:
    """Return the angle normalized (between 360 and 0)

    Args:
        angle (float): angle normalized

    Returns:
        float: angle normalized
    """
    while angle < 0: angle += 360
    while angle > 360: angle -= 360
    return angle

def vector_with_one_as_a_part(vector: tuple) -> tuple:
    """Take the vector and put his bigger coordinates to 1

    Args:
        vector (tuple): vector to modify

    Returns:
        tuple: final vector
    """
    if vector[1] == 0: return 1, 0
    elif vector[0] == 0: return 0, 1
    x_to_y = abs(vector[0]) / abs(vector[1])
    if x_to_y < 0:
        return vector[0] * (1/abs(vector[0])), vector[1] * (1/abs(vector[0]))
    return vector[0] * (1/abs(vector[1])), vector[1] * (1/abs(vector[1]))