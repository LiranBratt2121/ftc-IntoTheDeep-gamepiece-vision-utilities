from enum import Enum

class Color(Enum):
    RED = 'red'
    BLUE = 'blue'
    YELLOW = 'yellow'

RED_LOWER1 = (0, 100, 100)
RED_UPPER1 = (10, 255, 255)
RED_LOWER2 = (170, 100, 100)
RED_UPPER2 = (180, 255, 255)

BLUE_LOWER = (100, 100, 100)
BLUE_UPPER = (140, 255, 255)

YELLOW_LOWER = (20, 100, 100)
YELLOW_UPPER = (30, 255, 255)

MIN_AREA = 150

FOV_HORIZONTAL = 65

# Distance calculation constants in centimeters
KNOWN_DISTANCE_CM = 60
KNOWN_WIDTH_CM = 15