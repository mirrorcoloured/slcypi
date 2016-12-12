#!/usr/bin/python
# Use pi camera directly instead of via pygame.camere
# 4.2 Capturing to a stream

import io
import sys
sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH
from ImageAnalysis import ImageAnalysis
from Tank import Tank
import time
from time import sleep
import atexit
import pygame
#import pygame.camera
import picamera
import picamera.array
import cv2
import numpy as np
from PIL import Image

# Settings
WIDTH = 320
HEIGHT = 240

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

# Initialize Tank
robot = Tank()
robot.correctDirections(False,False,True)

# Initialize image analysis
IA = ImageAnalysis()
followLine = False

# Initialize camera
with picamera.PiCamera() as camera:
        camera.resolution = (WIDTH, HEIGHT)
        camera.start_preview()
        time.sleep(2)
        output = np.empty((320 * 240 * 3,), dtype=np.uint8)
        
        try:
                print('starting loop')
                done = False
                while not done:
                        
                        # Capture image
                        camera.capture(output, 'bgr', use_video_port=True)

                        # Convert to surface
                        newoutput = np.reshape(output, (240,320,3))            
                        sface = pygame.surfarray.make_surface(newoutput)
                        sface = pygame.transform.rotate(sface,270)
                        sface = pygame.transform.flip(sface, True, False)
            
                        # Display
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
                                        if (event.key == pygame.K_s):
                                                # Set target
                                                rgb = IA.setTarget(sface,WIDTH,HEIGHT)
                                                sface.fill(rgb)
                                                screen.blit(sface,(0,0))
                                                pygame.display.update()
                                                sleep(5)
                                        if (event.key ==pygame.K_a):
                                                # Analyze
                                                sface = IA.convertTrueFalse(sface,WIDTH,HEIGHT)                
                                                screen.blit(sface,(0,0))
                                                pygame.display.update()
                                                sleep(5)
                                        if (event.key ==pygame.K_r):
                                                # Analyze - rainbow
                                                sface = IA.convertRainbow(sface,WIDTH,HEIGHT)                
                                                screen.blit(sface,(0,0))
                                                pygame.display.update()
                                                sleep(5)
                                        if (event.key==pygame.K_c):
                                                pos = IA.getLinePosition(sface,WIDTH,HEIGHT)
                                                print(pos)
                                        if (event.key == pygame.K_q):
                                                followLine = True
                                        if (event.key == pygame.K_w):
                                                followLine = False
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
                        if followLine == True:
                                pos = IA.getLinePosition(sface,WIDTH,HEIGHT)
                                print(pos)
                                if abs(pos) >0.25:
                                        if pos > 0:
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
                                
        except KeyboardInterrupt:
                pygame.quit()

robot.stop()
camera.stop_preview()
pygame.quit()
