from enum import Enum

class Color(Enum):
    RED = 'red'
    BLUE = 'blue'
    YELLOW = 'yellow'

RED_LOWER1 = (0, 100, 100)
RED_LOWER1 = (0, 120, 70)  # Improved lower red range for better detection
RED_UPPER1 = (10, 255, 255)  # Kept upper red consistent
RED_LOWER2 = (170, 120, 70)  # Improved second lower red range
RED_UPPER2 = (180, 255, 255)  # Kept second upper red consistent

BLUE_LOWER = (90, 120, 70)  # Shifted to a more inclusive blue range
BLUE_UPPER = (130, 255, 255)  # Upper range for typical blue hues

YELLOW_LOWER = (15, 120, 70)  # Adjusted yellow range for better contrast
YELLOW_UPPER = (35, 255, 255)  # Broader range for yellows


MIN_AREA = 150

FOV_HORIZONTAL = 65

# Distance calculation constants in centimeters
KNOWN_DISTANCE_CM = 60
KNOWN_WIDTH_CM = 15
