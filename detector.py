import cv2
import numpy as np
from typing import Tuple

from constants import Color, RED_LOWER1, RED_UPPER1, RED_LOWER2, RED_UPPER2
from constants import BLUE_LOWER, BLUE_UPPER, YELLOW_LOWER, YELLOW_UPPER
from constants import KNOWN_DISTANCE_CM, KNOWN_WIDTH_CM, MIN_AREA
from constants import FOV_HORIZONTAL


def mask_gamePiece(frame: cv2.Mat, color: Color):
    blur = cv2.GaussianBlur(frame, (5, 5), 0)

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    match color:
        case Color.RED:
            mask1 = cv2.inRange(hsv, RED_LOWER1, RED_UPPER1)
            mask2 = cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
            mask = cv2.bitwise_or(mask1, mask2)

        case Color.BLUE:
            mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)

        case Color.YELLOW:
            mask = cv2.inRange(hsv, YELLOW_LOWER, YELLOW_UPPER)

        case _:
            raise ValueError("Color not found, use Color.[RED, BLUE, YELLOW]")

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask


def detect_gamePiece(mask: cv2.UMat, min_area=MIN_AREA):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    locations = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            locations.append(
                {
                    "center": (center_x, center_y),
                    "boundingRect": (x, y, w, h),
                    "area": area,
                }
            )

    return sorted(locations, key=lambda cnt: cnt["area"])


def fill_and_detect_gamePiece(mask: cv2.UMat, min_area=MIN_AREA):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled_mask = np.zeros_like(mask)
    locations = []

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > min_area and len(contour) >= 5:
            cv2.drawContours(filled_mask, [contour], -1, 255, thickness=cv2.FILLED)

            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            locations.append(
                {
                    "center": (center_x, center_y),
                    "boundingRect": (x, y, w, h),
                    "area": area,
                }
            )

    return filled_mask, sorted(locations, key=lambda cnt: cnt["area"], reverse=True)


def get_yaw(frame: cv2.UMat | np.ndarray, target_center_x: float) -> float:
    frame_width: float = frame.shape[0]
    frame_center_x = frame_width // 2

    offset_x = target_center_x - frame_center_x
    yaw = (offset_x / (frame_width / 2)) * (FOV_HORIZONTAL / 2)

    return yaw


def calculate_center_distance(frame: np.ndarray, target_center):
    frame_height, frame_width = frame.shape[:2]
    frame_center_x = frame_width // 2

    piece_center_x, _ = target_center

    distance_x = piece_center_x - frame_center_x

    return {
        "distance_x": distance_x,
        "abs_distance_x": abs(distance_x),
        "direction": "right" if distance_x > 0 else "left",
    }


def display(frame: cv2.UMat | np.ndarray, x: int, y: int, w: int, h: int):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)


def calculate_distance(perceived_widthPX: float):
    return (KNOWN_WIDTH_CM * KNOWN_DISTANCE_CM) / perceived_widthPX
