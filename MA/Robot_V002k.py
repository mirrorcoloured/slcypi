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
viewOptions = ["noFilter","colorFilter","lineDetection"]
viewNr = 1
startTime = time.time()

def toggleView(viewNr):
        viewNr = viewNr + 1
        if viewNr > 2:
               viewNr = 0
        return(viewNr)

with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (WIDTH, HEIGHT)

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

                                        if (event.key == pygame.K_8):
                                                upper[1] = upper[1] + 5
                                                print(upper)
                                        if (event.key == pygame.K_i):
                                                upper[1] = upper[1] - 5
                                                print(upper)
                                        if (event.key == pygame.K_k):
                                                lower[1] = lower[1] + 5
                                                print(lower)
                                        if (event.key == pygame.K_COMMA):
                                                lower[1] = lower[1] - 5
                                                print(lower)

                                        if (event.key == pygame.K_9):
                                                upper[2] = upper[2] + 5
                                                print(upper)
                                        if (event.key == pygame.K_o):
                                                upper[2] = upper[2] - 5
                                                print(upper)
                                        if (event.key == pygame.K_l):
                                                lower[2] = lower[2] + 5
                                                print(lower)
                                        if (event.key == pygame.K_PERIOD):
                                                lower[2] = lower[2] - 5
                                                print(lower)
                                                
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
                                        rotateSpeed = 50
                                        if abs(dir) > 0.5:
                                                rotateSpeed = 70
                                        if dir > 0:
                                                print("Rotate -1")
                                                #robot.driveSync(0)
                                                robot.rotateSync(-1, rotateSpeed)
                                                sleep(0.05)
                                                robot.rotateSync(0)
                                        else:
                                                print("Rotate 1")
                                                #robot.driveSync(0)
                                                robot.rotateSync(1, rotateSpeed)
                                                sleep(0.05)
                                                robot.rotateSync(0)
                                #else: 
                                        ##robot.rotateSync(0)
                                        #robot.driveSync(1)
                                        #sleep(0.1)
                                        #robot.driveSync(0)
                                if dir > -999:
                                        relCount = (1 - abs(dir)) * count
                                        driveSpeed = int(relCount / 1200 * 50)
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
