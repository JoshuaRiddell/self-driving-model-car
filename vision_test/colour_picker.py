from os.path import join
import numpy as np
import time
import cv2

KERNEL_SIZE = 10

space = [[], [], []]
bounds = [np.array([0,0,0]), np.array([255,255,255])]

def mouse_click(frame, event, x, y):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[y][x]
        for i in range(3):
            space[i].append(hsv[i])

        bounds[0] = np.array([min(space[i]) for i in range(3)])
        bounds[1] = np.array([max(space[i]) for i in range(3)])

        cv2.imshow('colour', np.array([np.array([frame[y][x] for i in range(100)]) for i in range(100)]))


cv2.namedWindow('frame')
cv2.setMouseCallback('frame', lambda event, x, y, flags, param: mouse_click(frame, event, x, y))

cap = cv2.VideoCapture(1)

# cap.set(3, 1920)
# cap.set(4, 1080)

frame = cap.read()[1]

while(True):
    ret, frame = cap.read()
    frame = cv2.boxFilter(frame, -1, (KERNEL_SIZE, KERNEL_SIZE))

    thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(thresh, *bounds)

    if ret==True:
        cv2.imshow('frame',frame)
        cv2.imshow('thresh',thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()