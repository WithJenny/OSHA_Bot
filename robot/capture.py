import numpy as np
import cv2 as cv
 
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
   
size = (frame_width, frame_height) 

result = cv.VideoWriter('filename.mp4',  
                         cv.VideoWriter_fourcc(*'mp4v'), 
                         10,size)
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
   
    # Display the resulting frame
    cv.imshow('frame', frame)
    result.write(frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


