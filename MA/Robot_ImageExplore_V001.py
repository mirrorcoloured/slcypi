# Import statements
import sys
sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
import cv2
import numpy as np
import matplotlib.pyplot as plt
import picamera
import picamera.array
import time
import pygame
from scipy import ndimage
from time import sleep

# Settings
WIDTH = 160
HEIGHT = WIDTH * 0.75

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

# Filter settings
lower = np.array([25,0,0])
upper = np.array([40,255,255])

def applyColorFilter(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        return(res)

def smooth(img):
        kernel = np.ones((15,15),np.float32)/225
        smoothed = cv2.filter2D(img,-1,kernel)
        return(smoothed)

def blurring(img):
        blur = cv2.GaussianBlur(img,(15,15),0)
        return(blur)

def medianBlurring(img):
        median = cv2.medianBlur(img,15)
        return(median)

def bilateralBlur(img):
        bilateral = cv2.bilateralFilter(img,15,75,75)
        return(bilateral)

doApplyColorFilter = False
doSmooth = False

done = False
startTime = time.time()
print(startTime)
with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (WIDTH, HEIGHT)

                while done == False:
                        
                        camera.capture(stream, 'bgr', use_video_port=True)
                        frame = stream.array

                        if doApplyColorFilter == True:
                                frame = applyColorFilter(frame)
                        if doSmooth == True:
                                frame = smooth(frame)
                   
                        # Display image
                        res = cv2.transpose(res)
                        sface = pygame.surfarray.make_surface(res)                        
                        screen.blit(sface,(0,0))
                        pygame.display.update()            
                        
                        # User events
                        for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:

                                        # Adjust hue
                                        if (event.key == pygame.K_ESCAPE):
                                                done = True
                                        if (event.key == pygame.K_7):
                                                upper[0] = upper[0] + 5
                                                print(upper)
                                        if (event.key == pygame.K_u):
                                                upper[0] = upper[0] - 5
                                                print(upper)
                                        if (event.key == pygame.K_j):
                                                lower[0] = lower[0] + 5
                                                print(lower)
                                        if (event.key == pygame.K_m):
                                                lower[0] = lower[0] - 5
                                                print(lower)

                                        # Select filter
                                        if (event.key == pygame.K.q):
                                                if doApplyColorFilter == True:
                                                        doApplyColorFilter = False
                                                else:
                                                        doApplyColorFilter = True

                                        if (event.key == pygame.K.w):
                                                if doSmooth == True:
                                                        doSmooth = False
                                                else:
                                                        doSmooth = True  
                                        
                        # Handle stream
                        stream.seek(0)
                        stream.truncate()

                        # Compute fps
                        lapseTime = (time.time() - startTime)
                        startTime = time.time()
                        if lapseTime > 0:
                                fps = 1.0 / lapseTime
                                print("fps: " + str(fps))

