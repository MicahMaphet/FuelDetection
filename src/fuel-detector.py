import os
import subprocess
import cv2
import imutils
import time

lower = (10, 100, 50)
upper = (60, 220, 225)

video = cv2.VideoCapture("../videos/sim_balls.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
shape = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
tmp_file = "/tmp/corrupted_fuel_video.mp4"
writer = cv2.VideoWriter(tmp_file, fourcc, fps, shape)

time.sleep(1.0)

while True:
    ret, frame = video.read()

    frame = frame

    if not ret or frame is None:
        break

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    for contour in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        M = cv2.moments(contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] /M["m00"]))

        if (radius > 20):
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)


    writer.write(frame)
    cv2.imshow("Video", frame)
    cv2.imshow("Detection", mask)


    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()
video.release()
writer.release()

subprocess.run(["ffmpeg", "-i", tmp_file, "output.mp4"])
os.remove(tmp_file)
