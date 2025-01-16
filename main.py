import cv2
from constants import Color
from detector import (
    calculate_center_distance,
    display,
    display_angle,
    display_rotated,
    fill_and_detect_gamePiece,
    mask_gamePiece,
)


cap = cv2.VideoCapture(0)
print("Initialized capture device")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    for color in [Color.BLUE]:
        current_frame = frame.copy()
        mask = mask_gamePiece(current_frame, color)
        filled_mask, locations = fill_and_detect_gamePiece(mask)

        if len(locations) > 0:
            target = locations[0]
            display(current_frame, *target["boundingRect"])

            if len(target["rotatedRectPoints"]) > 0:
                display_rotated(current_frame, target["rotatedRectPoints"])
                display_angle(current_frame, target["angle"])

            center_distance = calculate_center_distance(current_frame, target["center"])

            distance_text = (
                f"Distance X: {center_distance['distance_x']} px "
                f"({center_distance['direction']})"
            )

            cv2.putText(
                current_frame,
                distance_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        cv2.imshow(f"Mask - {color}", filled_mask)
        cv2.imshow(f"Frame - {color}", current_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
