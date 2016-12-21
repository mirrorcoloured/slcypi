# Import statements
import sys
sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Tank import Tank
from ImageAnalysis import ImageAnalysis
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
robot.correctDirections(True,True,True)

# Initialize ImageAnalysis
IA = ImageAnalysis()
IA.filterLower = np.array([25,35,70])
IA.filterUpper = np.array([65,255,205])

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

# Start settings
auto = False 
done = False
viewOptions = ["noFilter","colorFilter","lineDetection","featureMatch","opticalFlow"]
viewNr = 1
startTime = time.time()

def toggleView(viewNr):
        viewNr = viewNr + 1
        if viewNr > 4:
               viewNr = 0
        print(viewOptions[viewNr])
        return(viewNr)

with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (WIDTH, HEIGHT)

                        # Image capture (previous)
                        camera.capture(stream, 'bgr', use_video_port=True)
                        previous = stream.array

                        # Create hsv required for optical flow
                        hsv = np.zeros_like(previous)
                        hsv[...,1] = 255

                while done == False:

                        # Image capture
                        camera.capture(stream, 'bgr', use_video_port=True)
                        bgr = stream.array                        
                        
                        # Image process
                        res, mask = IA.colorFilter(bgr, False, False)
                        if viewOptions[viewNr] == "noFilter":
                                res = bgr
                        if viewOptions[viewNr] == "lineDetection":
                                res = IA.edgeDetection(bgr)
                        if viewOptions[viewNr] == "featureMatch":                                
                                res = IA.featureMatch(bgr,previous):
                                previous = current
                        if viewOptions[viewNr] == "opticalFlow":
                                res = IA.opticalFlow(current,previous, hsv)
                                previous = current
                        
                        # Image transpose
                        res = cv2.transpose(res)
                        mask = np.transpose(mask)

                        # Image display
                        sface = pygame.surfarray.make_surface(res)                        
                        screen.blit(sface,(0,0))
                        pygame.display.update()            
                        
                        # User events
                        for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:

                                        # Exit on escape                                
                                        if (event.key == pygame.K_ESCAPE):
                                                done = True

                                        # View toggle
                                        if event.key == (pygame.K_v):
                                                viewNr = toggleView(viewNr)
                                                
                                        # Drive commands
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
                                        if (event.key == pygame.K_7):
                                                IA.filterUpper[0] = IA.filterUpper[0] + 5
                                                print(IA.filterUpper)
                                        if (event.key == pygame.K_u):
                                                IA.filterUpper[0] = IA.filterUpper[0] - 5
                                                print(IA.filterUpper)
                                        if (event.key == pygame.K_j):
                                                IA.filterLower[0] = IA.filterLower[0] + 5
                                                print(IA.filterLower)
                                        if (event.key == pygame.K_m):
                                                IA.filterLower[0] = IA.filterLower[0] - 5
                                                print(IA.filterLower)

                                        if (event.key == pygame.K_8):
                                                IA.filterUpper[1] = IA.filterUpper[1] + 5
                                                print(IA.filterUpper)
                                        if (event.key == pygame.K_i):
                                                IA.filterUpper[1] = IA.filterUpper[1] - 5
                                                print(IA.filterUpper)
                                        if (event.key == pygame.K_k):
                                                IA.filterLower[1] = IA.filterLower[1] + 5
                                                print(IA.filterLower)
                                        if (event.key == pygame.K_COMMA):
                                                IA.filterLower[1] = IA.filterLower[1] - 5
                                                print(IA.filterLower)

                                        if (event.key == pygame.K_9):
                                                IA.filterUpper[2] = IA.filterUpper[2] + 5
                                                print(IA.filterUpper)
                                        if (event.key == pygame.K_o):
                                                IA.filterUpper[2] = IA.filterUpper[2] - 5
                                                print(IA.filterUpper)
                                        if (event.key == pygame.K_l):
                                                IA.filterLower[2] = IA.filterLower[2] + 5
                                                print(IA.filterLower)
                                        if (event.key == pygame.K_PERIOD):
                                                IA.filterLower[2] = IA.filterLower[2] - 5
                                                print(IA.filterLower)
                                                
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
                                aRes = IA.blockAnalyze(mask)
                                print(aRes)                        
                                dir = aRes[0]
                                count = aRes[1]
                
                                # Drive         
                                if abs(dir) > 0.20:
                                        rotateSpeed = 60
                                        if abs(dir) > 0.5:
                                                rotateSpeed = 80
                                        if dir > 0:
                                                print("Rotate -1")
                                                robot.rotateSync(-1, rotateSpeed)
                                                sleep(0.05)
                                                robot.rotateSync(0)
                                        else:
                                                print("Rotate 1")
                                                robot.rotateSync(1, rotateSpeed)
                                                sleep(0.05)
                                                robot.rotateSync(0)
                                
                                if dir > -999:
                                        relCount = (1 - abs(dir)) * count
                                        if count > 800:
                                                driveSpeed = 50
                                        if count > 10000:
                                                driveSpeed = int(relCount / 10000 * 50)
                                        if driveSpeed > 45 :                                        
                                                robot.driveSync(1, driveSpeed)
                                        else:
                                                robot.driveSync(0)
                                else:
                                        robot.driveSync(0)
                                        
                        # Handle stream
                        stream.seek(0)
                        stream.truncate()

                        # Compute fps
                        lapseTime = (time.time() - startTime)
                        startTime = time.time()
                        if lapseTime > 0:
                                fps = 1.0 / lapseTime
                                print("fps: " + str(fps))

robot.stop()
pygame.quit()
