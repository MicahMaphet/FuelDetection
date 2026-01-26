from imutils.video import VideoStream
import numpy as np
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
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kernely = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ])

    kernelx = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])

    ymask = cv2.filter2D(frame, -1, kernely)
    xmask = cv2.filter2D(frame, -1, kernelx)
    mask = xmask + ymask
    cv2.imshow("Video", frame)
    cv2.imshow("Edges", mask)

    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break
