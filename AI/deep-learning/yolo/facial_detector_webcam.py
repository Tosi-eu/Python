import cv2
import cvzone
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
face_model = YOLO('yolo/yolov8n-face.pt')

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (1020, 720))

    detection_result = face_model(frame, conf=0.7)

    for result in detection_result:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            width, height = x2 - x1, y2 - y1
            confidence = box.conf[0] * 100
            
            cvzone.cornerRect(frame, [x1, y1, width, height], l=9, rt=3, colorR=(255, 255, 255))
            cvzone.putTextRect(frame, text=str(confidence), pos=[x1-1, y1-1])

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
