#import numpy as np
import cv2 as cv
import os
import numpy as np
import time

capture_duration = 10
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)

result = cv.VideoWriter(
    '../videos/filename.mp4',
    cv.VideoWriter_fourcc(*'mp4v'),
    10,
    size
)
start_time = time.time()
while( int(time.time() - start_time) < capture_duration ):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv.imshow('frame', frame)
    result.write(frame)
    if cv.waitKey(1) == ord('q'):
        break

    #TODO figure out when the video should cut out

cap.release()
cv.destroyAllWindows()
