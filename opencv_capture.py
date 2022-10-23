import cv2
import time

video = cv2.VideoCapture('rtmp://[RTMP Server IP]:[PORT]/live/testkey')

while True:
    rc = video.grab()
    success, image = video.retrieve()
    if image is None:
        time.sleep(0.1)
        continue
    time.sleep(0.1)
