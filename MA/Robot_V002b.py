#!/usr/bin/python

import sys
sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH
import time
from time import sleep
import atexit
import pygame
import pygame.camera
from PIL import Image
#from pylab import *
from Tank import Tank
from ImageAnalysis import ImageAnalysis

# Settings
WIDTH = 320
HEIGHT = 240

# Pygame and camera initialize
pygame.init()
pygame.display.set_caption('My Robot')
pygame.camera.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(WIDTH,HEIGHT))
cam.start()

robot = Tank()
robot.correctDirections(False,False,True)

IA = ImageAnalysis()
followLine = False

try:
        print('starting loop')
        done = False
        while not done:

                # Camera
                #sleep(5) # Sleep such that camera will get current image 
                image1 = cam.get_image()
                #image1 = pygame.transform.scale(image1,(640,480))
                #image1 = pygame.transform.flip(image1,1,1)
                screen.blit(image1,(0,0))
                pygame.display.update()
                
                # User events
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == (pygame.K_UP):
                                        robot.driveSync(1)
                                if event.key == (pygame.K_DOWN):
                                        robot.driveSync(-1)
                                if (event.key == pygame.K_ESCAPE):
                                        done = True
                                if (event.key == pygame.K_LEFT):
                                        robot.rotateSync(1,45)
                                if (event.key == pygame.K_RIGHT):
                                        robot.rotateSync(-1,45)
                                if (event.key == pygame.K_q):
                                        followLine = True
                                        #robot.driveSync(1,50)
                                        #sleep(1)
                                        #robot.driveSync(1,40)
                                if (event.key == pygame.K_w):
                                        followLine = False
                                        robot.driveSync(0)
                                        robot.rotateSync(0)
                                                                        
                                if (event.key == pygame.K_s):

                                    # Set target
                                    rgb = IA.setTarget(image1,WIDTH,HEIGHT)
                                    image1.fill(rgb)
                                    screen.blit(image1,(0,0))
                                    pygame.display.update()
                                    sleep(5)
                                if (event.key ==pygame.K_r):

                                    # Analyze
                                    image1 = IA.convertRainbow(image1,WIDTH,HEIGHT)                
                                    screen.blit(image1,(0,0))
                                    pygame.display.update()
                                    sleep(5)
                                if (event.key ==pygame.K_a):

                                    # Analyze
                                    image1 = IA.convertTrueFalse(image1,WIDTH,HEIGHT)                
                                    screen.blit(image1,(0,0))
                                    pygame.display.update()
                                    sleep(5)
                                if (event.key==pygame.K_c):
                                    pos = IA.getLinePosition(image1,WIDTH,HEIGHT)
                                    print(pos)
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
                        if abs(pos) >0.5:
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
                                sleep(0.01)
                                robot.driveSync(0)
 
                        
except KeyboardInterrupt:
        pygame.quit()

robot.stop()
cam.stop()
pygame.quit()
