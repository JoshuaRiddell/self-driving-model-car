#Iain Vision 0.5
# from threading import Thread, Lock


from os.path import join
import numpy as np
import cv2 as cv
Kern = 5
def test():
    n = HoughVision(0)
    n.Get()
    n.Get()
    n.Thresh()
    n.Canny()
    n.PointThresh()
    n.Show()
    cv.waitKey(0)
    n.End()

class testing(object):
    'A class used for testing the Vision /Control'
    def __init__(self , camera_id):
        self.cam = cv.VideoCapture(camera_id)

    def CamTest(self):
            self.cam.set(3, 1920)
            self.cam.set(4, 1080)
            frame = self.cam.read()[1]

            while(True):   
                ret, frame = self.cam.read()
                if ret==True:
        # write the flipped frame
                    cv.imshow('frame',frame)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break

    def Exit(self):
     # Release everything if job
        self.cam.release()
        cv.destroyAllWindows()
        
class HoughVision(object):
    'Finds the boundaries for the Race Track Using the Hough Line Method'
    def __init__(self, camera_id):
        self.cam = cv.VideoCapture(camera_id)
        testframe = self.cam.read()[1]
        self.height, self.width, channels = testframe.shape
    def Get(self):
        print('Taking picture')
        self.frame = self.cam.read()[1]
        print('Picture Done!')
        
    def Thresh(self):
        frame = cv.boxFilter(self.frame, -1, (Kern, Kern))
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower_blue = np.array([11,50,50])
        upper_blue = np.array([130,255,255])
        lower_Y = np.array([16, 71, 86])
        upper_Y = np.array([110,224,186])       
        self.B = cv.inRange(hsv, lower_blue, upper_blue)
        self.Y = cv.inRange(hsv, lower_Y, upper_Y)
            
    def Show(self):
        cv.circle(self.frame , (self.width-50,self.height-50),60,(0,0,255),-1)
        cv.imshow('frame',self.frame)
        cv.imshow('Blue',self.B)
        cv.imshow('Yellow',self.Y)
        cv.imshow('Blue Canny',self.EdgeB)
        cv.imshow('Yellow Canny',self.EdgeY)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def End(self):
        self.cam.release()
        
    def Canny(self):
        self.EdgeB = cv.Canny(self.B,100,200)
        self.EdgeY = cv.Canny(self.Y,100,200)
        
    def PointThresh(self):
        YL = self.Y[self.height-50,50]
        BL = self.B[self.height-50,self.width-50]
        print(YL/255,BL/255)
        return (YL,BL)
