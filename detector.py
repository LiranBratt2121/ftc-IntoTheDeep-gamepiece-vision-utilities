import cv2
import numpy as np

from constants import Color, RED_LOWER1, RED_UPPER1, RED_LOWER2, RED_UPPER2
from constants import BLUE_LOWER, BLUE_UPPER, YELLOW_LOWER, YELLOW_UPPER
from constants import KNOWN_DISTANCE_CM, KNOWN_WIDTH_CM, MIN_AREA
from constants import FOV_HORIZONTAL

def mask_gamePiece(frame: cv2.Mat, color: Color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    match color:
        case Color.RED:
            mask1 = cv2.inRange(hsv, RED_LOWER1, RED_UPPER1)
            mask2 = cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
            
            return cv2.bitwise_or(mask1, mask2)

        case Color.BLUE:
            return cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
        
        case Color.YELLOW:
            return cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)
        
        case _:
            raise ValueError("Color not found, use Color.[RED, BLUE, YELLOW]")
        

def detect_gamePiece(mask: cv2.UMat, min_area=MIN_AREA):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    locations = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            locations.append({
                "center": (center_x, center_y),
                "boundingRect": (x, y, w, h),
                "area": area
            })
    
    return sorted(locations, key=lambda cnt: cnt['area'])


def get_yaw(frame: cv2.UMat | np.ndarray, target_center_x: float) -> float:
    frame_width: float = frame.shape[0]
    frame_center_x = frame_width // 2
    
    offset_x = target_center_x - frame_center_x
    yaw = (offset_x / (frame_width / 2)) * (FOV_HORIZONTAL / 2)
    
    return yaw
   
    
def calculate_distance(perceived_widthPX: float):
    return (KNOWN_WIDTH_CM * KNOWN_DISTANCE_CM) / perceived_widthPX
            