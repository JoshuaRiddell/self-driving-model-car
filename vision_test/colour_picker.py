from os.path import join
import numpy as np
import time
import cv2

def mouse_click(event, x, y, flags, param):
    

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_click)

cap = cv2.VideoCapture(1)

cap.set(3, 1920)
cap.set(4, 1080)

frame = cap.read()[1]

while(True):
    ret, frame = cap.read()
    frame = cv2.boxFilter(frame, -1, (10,10))
    if ret==True:
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()