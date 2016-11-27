
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
        self.tp = (170,70,20)
        self.distBenchmark = 8000
        
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
        for x in range(0,w-1):
            print(x)
            for y in range(0,h-1):
                check = self.checkPixel(pxarray[x,y])
                #print(check)
                if check ==True:
                    pxarray[x,y] = 0
                else:
                    pxarray[x,y] = 80000

        #img2 = pygame.surface.make_surface(pyarray)
        return pxarray
    

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




