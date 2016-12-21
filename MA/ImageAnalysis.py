
# Import statements
import pygame
import pygame.camera
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageAnalysis():
        """Class with methods for image analysis"""

        def __init__(self):
                """Initialize method"""
                print("Initiate ImageAnalysis")

                # Set starting values
                WITDH = 320
                HEIGHT = 240
                filterLower = np.array([5,0,0])
                filterUpper = np.array([75,255,255])
                blockAnalyseYstart = 0
                blockAnalyseYend = 100

        def featureMatch(current,previous):
                orb = cv2.ORB_create()
                cv2.ocl.setUseOpenCL(False)
                kp1, des1 = orb.detectAndCompute(current,None)
                kp2, des2 = orb.detectAndCompute(previous,None)
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1,des2)
                matches = sorted(matches, key = lambda x:x.distance)
                res = cv2.drawMatches(current,kp1,previous,kp2,matches[:10],None, flags=2)
                return(res)
        
        def edgeDetection(self, bgr):
                laplacian = cv2.Laplacian(bgr,cv2.CV_64F)
                return(laplacian)
                #sobelx = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)
                #sobely = cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=5)

        # Method to apply color filter
        def colorFilter(self, bgr, erode = False, dilate = False):
                hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, self.filterLower, self.filterUpper)
                if erode == True:
                        kernel = np.ones((5,5),np.uint8)
                        mask = cv2.erode(mask,kernel,iterations = 1)
                if dilate == True:
                        kernel = np.ones((5,5),np.uint8)
                        mask = cv2.dilate(mask,kernel,iterations = 1)
                res = cv2.bitwise_and(bgr, bgr, mask=mask)
                return(res, mask)
        
        def smooth(self,img):
                kernel = np.ones((15,15),np.float32)/225
                smoothed = cv2.filter2D(img,-1,kernel)
                return(smoothed)

        def blurring(self,img):
                blur = cv2.GaussianBlur(img,(15,15),0)
                return(blur)

        def medianBlurring(self,img):
                median = cv2.medianBlur(img,15)
                return(median)

        def bilateralBlur(self,img):
                bilateral = cv2.bilateralFilter(img,15,75,75)
                return(bilateral)

        def blockAnalyze(self,mask):
                # Assumes 320 width
                sum = 0
                count = 0
                for x in range(5):
                        #self.blockAnalyseYstart:self.blockAnalyseYend
                        blockCount = np.sum(mask[x*64:x*64+63,140:240]) / 255     
                        sum = sum + blockCount * x
                        count = count + blockCount

                if count > 0:
                        overallMean = float(sum) / count        
                        direction = (overallMean - 2) / 2
                        return direction, count
                else:
                        return -999, count


    
