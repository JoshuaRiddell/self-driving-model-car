from os.path import join
import numpy as np
import cv2

cap = cv2.VideoCapture(1)

cap.set(3, 1920)
cap.set(4, 1080)

frame = cap.read()[1]

while(True):
    ret, frame = cap.read()
    if ret==True:
        # write the flipped frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()