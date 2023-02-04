import cv2
import tracker

# Create tracker object
tracker = tracker.EuclideanDistTracker()

cap = cv2.VideoCapture("2.3gp")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=100,detectShadows=False)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract Region of interest
    #roi = frame[340: 720,500: 800]

    # 1. Object Detection
    frame = cv2.resize(frame, (640, 480));
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2)))
    mask = cv2.dilate(mask,None,iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 1000:
            #cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)


            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("frame", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()