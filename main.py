import cv2
from constants import Color
from detector import mask_gamePiece, detect_gamePiece, get_yaw

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    mask = mask_gamePiece(frame, Color.RED)
    locations = detect_gamePiece(mask)
    
    if len(locations) > 0:
        cv2.putText(frame, "len: " + str(len(locations)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0))
        cv2.putText(frame, "yaw: " + str(get_yaw(frame, locations[0]["center"][0])), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0))
    
            
    cv2.imshow('RED MASK', mask)
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cap.release()
cv2.destroyAllWindows()
 