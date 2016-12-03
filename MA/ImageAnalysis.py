
# Import statements
import pygame
import pygame.camera
from PIL import Image
#from pylab import *


class ImageAnalysis():
    """Class with methods for image analysis"""

    def __init__(self) -> None:
        """Initialize method"""
        print("Initiate ImageAnalysis")

        # Set target pixel
        #self.tp = (100,90,30)
        #self.tp = (180,130,70)
        self.tp = (130,110,20)
        self.distBenchmark = 1050
        
    # Method to convert pixel int to RGB values
    def getRGB(self,pixelInt):
        #print(pixelInt)
        blue = pixelInt & 255
        green = (pixelInt >> 8) & 255
        red = (pixelInt >> 16) & 255
        myArray = [red, green, blue]
        return myArray

    def showMidPixel(self,img,w,h):

        # Transform        
        pxarray = pygame.PixelArray(img)
        middlePixel = pxarray[int(w/2),int(h/2)]
        
        #middlePixel = pxarray[150,150]
        print(middlePixel)
        rgb = self.getRGB(middlePixel)
        print(rgb)

    def setTarget(self,img,w,h):
        """Method to find RGB values target.
        Target area middle of bottom quarter of camera view."""
        print("Setting target")
        pxarray = pygame.PixelArray(img)
        count = 0
        sumR = 0
        sumG = 0
        sumB = 0
        for x in range(int(w*0.4),int(w*0.6)):
            for y in range(int(h*0.75),int(h-1)):
                px = pxarray[x,y]
                rgb = self.getRGB(px)
                count = count + 1
                sumR = sumR + rgb[0]
                sumG = sumG + rgb[1]
                sumB = sumB + rgb[2]
        av = [int(sumR/count),int(sumG/count),int(sumB/count)]
        print(av)
        self.tp = av
        return av
        

    def checkPixel(self,px):
        rgb = self.getRGB(px)       
        distance = (self.tp[0] - rgb[0]) ** 2 + (self.tp[1] - rgb[1]) ** 2 +(self.tp[2] - rgb[2]) ** 2
        #print(distance)
        if distance < self.distBenchmark:
                return True
        else:
                return False

    def convertTrueFalse(self,img,w,h):
        print("Convert")
        pxarray = pygame.PixelArray(img)
        for x in range(0,int((w-1)),2):
            print(x)
            for y in range(0,int((h-1)),2):
                check = self.checkPixel(pxarray[x,y])
                #print(check)
                if check ==True:
                    pxarray[x,y] = 50000
                else:
                    pxarray[x,y] = 0

        img2 = pygame.PixelArray.make_surface(pxarray)
        return img2

    def convertRainbow(self,img,w,h):
        print("Convert")
        pxarray = pygame.PixelArray(img)
        for x in range(0,int((w-1)),2):
            print(x)
            for y in range(0,int((h-1)),2):
                rgb = self.getRGB(px)       
                distance = (self.tp[0] - rgb[0]) ** 2 + (self.tp[1] - rgb[1]) ** 2 +(self.tp[2] - rgb[2]) ** 2
                if distance <= 1000:
                    pxarray[x,y] = 80000
                else:
                    if distance <= 2000:
                        pxarray[x,y] = 70000:
                    else:
                        if distance <= 3000:
                            pxarray[x,y] = 60000
                        else:
                            if distance <= 4000:
                                pxarray[x,y] = 50000
                            else:
                                if distance <= 5000:
                                    pxarray[x,y] = 40000
                                else:
                                    if distance <= 6000:
                                        pxarray[x,y] = 30000
                                    else:
                                        if distance <= 7000:
                                            pxarray[x,y] = 20000
                                        else:
                                            if distance <= 8000:
                                                pxarray[x,y] = 10000
                                            
                            


                            
                
                check = self.checkPixel(pxarray[x,y])
                #print(check)
                
                if check ==True:
                    pxarray[x,y] = 50000
                else:
                    pxarray[x,y] = 0

        img2 = pygame.PixelArray.make_surface(pxarray)
        return img2


    def getLinePosition(self,img,w,h):
        pxarray = pygame.PixelArray(img)
        startY = 0.6
        endY = 0.9
        sum = 0
        count = 0
        for x in range(0,w):
            for y in range(int(h*startY),int(h*endY)):
                check = self.checkPixel(pxarray[x,y])
                if check ==True:
                    sum = sum + x
                    count = count + 1
        
        if count > 5:
            # Compute average
            average = sum / count
        
            # standardize
            standardVal = (average - (w / 2)) / (w /2) 
        
            return standardVal
        else:
            return -999
        

# Method to analyze image to follow line
def analyzeLine(img):

        # Settings
        directionCutpoint = 0.5

        # Transform
        pxarray = pygame.PixelArray(img)
        #print pxarray.shape
        
        # Loop through
        sum = 0
        count = 0.1
        for y in range(110,130):
                for x in range(0,321):

                        # Check
                        check = self.checkPixel(pxarray[x,y])
                        sum = sum + x
                        count = count + 1

        # Compute average
        average = sum / count
        print(average)
        
        # standardize
        standardVal = (average - (640 / 2)) / (640 /2) 
        print(standardVal)

        # Compare to diction cut point
        direction = 0
        if standardVal < 0- directionCutpoint:
                direction = 1
        if standardVal > directionCutpoint:
                direction = -1

        # Return direction
        return direction




