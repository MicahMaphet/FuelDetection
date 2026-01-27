from imutils.video import VideoStream
import cv2
import imutils
import time

lower = (50, 25, 0)
upper = (100, 255, 255)

video = VideoStream(src=0).start()

time.sleep(1.0)

while True:
    frame = video.read()

    frame = frame

    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow("Video", frame)
    cv2.imshow("Detection", mask)

    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break
