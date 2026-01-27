from collections import deque
import math
import cv2
import imutils
import time

lower = (10, 0, 0)
upper = (60, 255, 255)
pts = deque(maxlen=64)

video = cv2.VideoCapture("../videos/single_ball.webm")

time.sleep(1.0)

while True:
    frame = video.read()

    frame = frame[1]

    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] /M["m00"]))

        if (radius > 10):
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue

        thickness = int(math.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)


    cv2.imshow("Video", frame)
    cv2.imshow("Detection", mask)


    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()
