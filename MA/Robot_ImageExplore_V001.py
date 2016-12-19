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
HEIGHT = 120

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

# Filter settings
lower = np.array([25,0,0])
upper = np.array([40,255,255])

def blockAnalyze(mask):
        # Assume 320,240 image
        mask = np.transpose(mask)
        sum = 0
        count = 0
        for x in range(5):
                blockCount = np.sum(mask[x*64:x*64+63,0:100]) / 255     
                sum = sum + blockCount * x
                count = count + blockCount

        if count > 0:
                overallMean = float(sum) / count        
                direction = (overallMean - 2) / 2
                return direction, count
        else:
                return -999, count

                                  
# Analyze line function
def analyzeLine(mask, WIDTH, HEIGHT):

        startY = 0.4
        endY = 0.6
        sum = 0
        count = 0.1
        for x in range(0,WIDTH):
                for y in range(int(HEIGHT*startY),int(HEIGHT*endY)):
                        if mask[y,x] == 255:
                                sum = sum + x
                                count = count + 1
        
        if count > 5:

                # Compute average
                average = sum / count
        
                # standardize
                direction = (average - (WIDTH / 2)) / (WIDTH /2) 
        
                return direction, count
        else:
                return -999, count

done = False
startTime = time.time()
print(startTime)
with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (320, 240)

                while done == False:
                        
                        camera.capture(stream, 'bgr', use_video_port=True)
                        # stream.array now contains the image data in BGR order
                
                        # Image process
                        frame = stream.array                        
                        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        mask = cv2.inRange(hsv, lower, upper)
                        res = cv2.bitwise_and(frame, frame, mask=mask)
                        res = cv2.transpose(res)
                        sface = pygame.surfarray.make_surface(res)                        

                        # Display image
                        screen.blit(sface,(0,0))
                        pygame.display.update()            
                        
                        # User events
                        for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
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
                        #        if event.type == pygame.KEYUP:
                        #aRes = blockAnalyze(mask)
                        #print(aRes)  
                        
                        # Handle stream
                        stream.seek(0)
                        stream.truncate()

                        # Compute fps
                        lapseTime = (time.time() - startTime)
                        startTime = time.time()
                        if lapseTime > 0:
                                fps = 1.0 / lapseTime
                                print("fps: " + str(fps))

