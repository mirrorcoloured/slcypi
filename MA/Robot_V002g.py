# Import statements
import sys
sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Tank import Tank
import picamera
import picamera.array
import time
import pygame
from scipy import ndimage
from time import sleep

# Settings
WIDTH = 320
HEIGHT = 240

# Initialize Tank
robot = Tank()
robot.correctDirections(False,False,True)

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

# Image analysis
lower = np.array([35,0,0])
upper = np.array([120,200,255])

# Analyze line function
def analyzeLine(mask, WIDTH, HEIGHT):

        startY = 0.4
        endY = 0.6
        sum = 0
        count = 0.1
        for x in range(0,HEIGHT):
                for y in range(int(HEIGHT*startY),int(HEIGHT*endY)):
                        if mask[x,y] == True:
                                sum = sum + x
                                count = count + 1
        
        if count > 5:

                # Compute average
                average = sum / count
        
                # standardize
                direction = (average - (w / 2)) / (w /2) 
        
                return direction, count
        else:
                return -999, count

auto = False 
done = False

with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (320, 240)

                while done == False:
                        camera.capture(stream, 'bgr', use_video_port=True)
                        # stream.array now contains the image data in BGR order
                
                        # Image process
                        frame = stream.array
                        #frame = ndimage.rotate(frame, 90)
                        #frame = cv2.flip("horizontal flip",frame)
                        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
                        mask = cv2.inRange(hsv, lower, upper)
                        res = cv2.bitwise_and(frame, frame, mask=mask)        
                        sface = pygame.surfarray.make_surface(res)                        

                        # Display image
                        screen.blit(sface,(0,0))
                        pygame.display.update()            
                        
                        # User events
                        for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                        if (event.key == pygame.K_ESCAPE):
                                                done = True
                                        if event.key == (pygame.K_UP):
                                                robot.driveSync(1)
                                        if event.key == (pygame.K_DOWN):
                                                robot.driveSync(-1)
                                        if (event.key == pygame.K_LEFT):
                                                robot.rotateSync(1,45)
                                        if (event.key == pygame.K_RIGHT):
                                                robot.rotateSync(-1,45)                                        
                                        if (event.key == pygame.K_q):
                                                auto = True
                                        if (event.key == pygame.K_w):
                                                auto = False
                                                robot.driveSync(0)
                                                robot.rotateSync(0)
                                if event.type == pygame.KEYUP:
                                        if event.key == (pygame.K_UP):
                                                robot.driveSync(0)
                                        if event.key == (pygame.K_DOWN):
                                                robot.driveSync(0)
                                        if (event.key == pygame.K_LEFT):
                                                robot.rotateSync(0)
                                        if (event.key == pygame.K_RIGHT):
                                                robot.rotateSync(0)
                        # Autonomous
                        if auto == True:
                                
                                # Analyze line
                                aRes = analyzeLine(mask, WIDTH, HEIGHT)
                                print(aRes)
                                dir = aRes[0]
                
                                # Drive         
                                if abs(dir) > 0.25:
                                        if dir > 0:
                                                robot.rotateSync(-1)
                                                sleep(0.01)
                                                robot.rotateSync(0)
                                        else:
                                                robot.rotateSync(1)
                                                sleep(0.01)
                                                robot.rotateSync(0)
                                else: 
                                        robot.driveSync(1)
                                        sleep(0.1)
                                        robot.driveSync(0)

                        # Handle stream
                        stream.seek(0)
                        stream.truncate()

