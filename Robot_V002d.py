#!/usr/bin/python
# Use pi camera directly instead of via pygame.camera

import io
import sys
sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH
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
#from pylab import *
from Tank import Tank

from ImageAnalysis import ImageAnalysis

# Settings
WIDTH = 320
HEIGHT = 240

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

#pygame.camera.init()
#cam_list = pygame.camera.list_cameras()
#cam = pygame.camera.Camera(cam_list[0],(WIDTH,HEIGHT))
#cam.start()

# Initialize Tank
robot = Tank()
robot.correctDirections(False,False,True)

# Initialize image analysis
IA = ImageAnalysis()
followLine = False

# Initialize camera
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.resolution = (WIDTH, HEIGHT)
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        #image = stream.array

        try:
                print('starting loop')
                done = False
                while not done:

                        # Camera
        
                        #image1 = stream.array
                        #image1 = Image.fromarray(image1, 'RGB')
                        #print(type(image1))
                        #image1 = pygame.numpy.array.make_surface(image1)

                        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
                        image1 = cv2.imdecode(data, 1)
                        #image1 = image1[:, :, ::-1]
                        
                        screen.blit(image1,(0,0))
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
                                                rgb = IA.setTarget(image1,WIDTH,HEIGHT)
                                                image1.fill(rgb)
                                                screen.blit(image1,(0,0))
                                                pygame.display.update()
                                                sleep(5)
                                        if (event.key ==pygame.K_a):
                                                # Analyze
                                                image1 = IA.convertTrueFalse(image1,WIDTH,HEIGHT)                
                                                screen.blit(image1,(0,0))
                                                pygame.display.update()
                                                sleep(5)
                                        if (event.key ==pygame.K_r):
                                                # Analyze - rainbow
                                                image1 = IA.convertRainbow(image1,WIDTH,HEIGHT)                
                                                screen.blit(image1,(0,0))
                                                pygame.display.update()
                                                sleep(5)
                                        if (event.key==pygame.K_c):
                                                pos = IA.getLinePosition(image1,WIDTH,HEIGHT)
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
                                pos = IA.getLinePosition(image1,WIDTH,HEIGHT)
                                print(pos)
                                if abs(pos) >0.25:
                                        if pos > 0:
                                                robot.rotateSync(-1)
                                                sleep(0.025)
                                                robot.rotateSync(0)
                                        else:
                                                robot.rotateSync(1)
                                                sleep(0.025)
                                                robot.rotateSync(0)
                                else:
                                        robot.driveSync(1)
                                        sleep(0.5)
                                        robot.driveSync(0)
                                
        except KeyboardInterrupt:
                pygame.quit()

robot.stop()
camera.stop_preview()
pygame.quit()
