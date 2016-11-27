
# Import statements
import pygame
import pygame.camera
from PIL import Image
from pylab import *

class ImageAnalysis():
    """Class with methods for image analysis"""

    def __init__(self) -> None:
        """Initialize method"""
        print("Initiate ImageAnalysis")

        # Set target pixel
        self.tp = (100,90,30)
        self.distBenchmark = 800
        
    # Method to convert pixel int to RGB values
    def getRGB(pixelInt):
        blue = pixelInt & 255
        green = (pixelInt >> 8) & 255
        red = (pixelInt >> 16) & 255
        myArray = [red, green, blue]
        return myArray

    def showMidPixel(img,w,h):

        # Transform        
        pxarray = pygame.PixelArray(img)
        middlePixel = pxarray[w/2,h/2]
        rgb = getRGB(midlePixelPixel)
        print(rgb)

    def checkPixel(px):
        rgb = getRGB(px)       
        distance = (self.tp[0] - rgb[0]) ** 2 + (self.tp[1] - rgb[1]) ** 2 +(self.tp[2] - rgb[2]) ** 2
        if abs(distance < self.distBenchmark):
                return True
        else:
                return False

    def convertTrueFalse(img,w,h):
        pxarray = pygame.PixelArray(img)
        for x in range(0,w-1):
            for y in range(0,h-1):
                check = self.checkPixel(pxarray[x,y])
                if check ==True:
                    pxarray[x,y] = 0
                else:
                    pxarray[x,y] = 5000
        
        return pxarray
    

# Method to analyze image to follow line
def analyzeLine(img):

        # Set values
        tp = (100,90,30)
        distanceAllowed = 800
        directionCutpoint = 0.5

        # Transform
        pxarray = pygame.PixelArray(img)
        #print pxarray.shape
        
        # Loop through
        sum = 0
        count = 0.1
        for x in range(0,639):

                # Get current pixel
                myPixel = pxarray[x,240]
                rgb = getRGB(myPixel)
                
                # Compare to targetColor        
                distance = (tp[0] - rgb[0]) ** 2 + (tp[1] - rgb[1]) ** 2 + (tp[2] - rgb[2]) ** 2
                if (distance <= distanceAllowed):
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




