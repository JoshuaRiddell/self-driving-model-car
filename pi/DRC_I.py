#Iain Vision 0.5
# from threading import Thread, Lock

from os.path import join
import numpy as np
import cv2 as cv
Kern = 5
def test():
    n = HoughVision(0)
    while(1):
        n.Get()
        #n.Canny
        n.Thresh()
        n.PointThresh()
    # n.Show()
        
        
class HoughVision(object):
    'Finds the boundaries for the Race Track Using the Hough Line Method'
    def __init__(self, camera_id):
        self.cam = cv.VideoCapture(camera_id)
        testframe = self.cam.read()[1]
        self.height, self.width, channels = testframe.shape
    def Get(self):
        self.frame = self.cam.read()[1]
        
    def Thresh(self):
        F = cv.boxFilter(self.frame, -1, (Kern, Kern))
        hsv = cv.cvtColor(F, cv.COLOR_BGR2HSV)
        lower_blue = np.array([104,  53,  58])
        upper_blue = np.array([112, 255, 152])
        lower_Y = np.array([ 17,  18, 103])
        upper_Y = np.array([ 32, 249, 232])
        self.B = cv.inRange(hsv, lower_blue, upper_blue)
        self.Y = cv.inRange(hsv, lower_Y, upper_Y)
            
    def Show(self):
        cv.circle(self.frame , (self.width-50,self.height-50),60,(0,0,255),-1)
        cv.imshow('frame',self.frame)
        cv.imshow('Blue',self.B)
        cv.imshow('Yellow',self.Y)
        #cv.imshow('Blue Canny',self.EdgeB)
        #cv.imshow('Yellow Canny',self.EdgeY)
        cv.waitKey(0)
#        cv.destroyAllWindows()

    def End(self):
        self.cam.release()
        
    def Canny(self):
        self.EdgeB = cv.Canny(self.B,100,200)
        self.EdgeY = cv.Canny(self.Y,100,200)
        
    def PointThresh(self):
        BL = self.B[self.height-50,50]
        YL = self.Y[self.height-50,self.width-50]
        print(YL/255,BL/255)
        return (YL,BL)

test()