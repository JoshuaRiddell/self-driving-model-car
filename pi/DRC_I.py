#Iain Vision 0.5


from os.path import join
import numpy as np
import cv2 as cv
Kern = 5
def test():
    n = HoughVision(0)
    n.Get()
    n.Get()
    n.Thresh()
    n.CandH()
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
        lower_Y = np.array([18, 104, 102])
        upper_Y = np.array([23,159,125])       
        self.B = cv.inRange(hsv, lower_blue, upper_blue)
        self.Y = cv.inRange(hsv, lower_Y, upper_Y)
            
    def Show(self):

        cv.imshow('frame',self.frame)
        cv.imshow('Blue',self.B)
        cv.imshow('Yellow',self.Y)
        cv.imshow('Blue Canny',self.EdgeB)
        cv.imshow('Yellow Canny',self.EdgeY)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def End(self):
        self.cam.release()
        
    def CandH(self):
        self.EdgeB = cv.Canny(self.B,100,200)
        self.EdgeY = cv.Canny(self.Y,100,200)
        lineY = cv.HoughLines(self.EdgeY,1,np.pi/180,80)
        lineB = cv.HoughLines(self.EdgeB,1,np.pi/180,100)
        print('Y:')
        print(lineY)
        print('B:')
        print(lineB)
        if lineB is None:
            if lineY is None :
                print('No  Lines')
                print('panic')
                return 0 
            else:
                print('Yellow Lines')
                L2 = lineY[0]
                L2 = L2[0]
                RH = L2[0]
                TH = L2[1]
                c = np.cos(TH)
                d = np.sin(TH)
                W0 = c*RH
                Z0 = d*RH
                W1= int(W0 + 1000*(-c))
                Z1 = int(Z0 + 1000*(d))
                W2 = int(W0 - 1000*(-d))
                Z2 = int(Z0 - 1000*(c))
##                cv.line(self.frame,(W1,Z1),(W2,Z2),(0,255,0),2)
                print('GoLeft')
                return -60 
        else:
            if lineY is None:
                print('Bleu Lines')

                L1 =lineB[0]
                L1 = L1[0]
                rho = L1[0]
                theta = L1[1]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1= int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
##                cv.line(self.frame,(x1,y1),(x2,y2),(0,0,255),2)
                print('Go Right')
                return 60 
            else:
                print('All Lines')
                   
                L2 = lineY[0]
                L2 = L2[0]
                RH = L2[0]
                TH = L2[1]
                c = np.cos(TH)
                d = np.sin(TH)
                W0 = c*RH
                Z0 = d*RH
                W1= int(W0 + 1000*(-c))
                Z1 = int(Z0 + 1000*(d))
                W2 = int(W0 - 1000*(-d))
                Z2 = int(Z0 - 1000*(c))
##                cv.line(self.frame,(W1,Z1),(W2,Z2),(0,0,255),2) 
                L1 =lineB[0]
                L1 = L1[0]
                rho = L1[0]
                theta = L1[1]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1= int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
##                cv.line(self.frame,(x1,y1),(x2,y2),(0,0,255),2)
                print('gostraight')
                return 0 
       
      

    def PointThresh(self):
        YL = self.Y[self.height-50,50]
        BL = self.B[self.height-50,self.width-50]
        print(YL/255,BL/255)
        return (YL,BL)
    
