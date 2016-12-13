#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import pygame
import pygame.camera
import sys
#from picamera import PiCamera
from time import sleep
from PIL import Image
from pylab import *
import MA.Tank as tank



# Pygame and camera initialize
pygame.init()
pygame.display.set_caption('My Robot')
pygame.camera.init()
screen = pygame.display.set_mode((640,480),0)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(320,240))
cam.start()

robot = tank.Tank()

try:

        print('starting loop')
        done = False
        while not done:

                # Camera
                image1 = cam.get_image()
                image1 = pygame.transform.scale(image1,(640,480))
                #image1 = pygame.transform.flip(image1,1,1)
                screen.blit(image1,(0,0))
                pygame.display.update()

                # User events
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == (pygame.K_UP):
                                        robot.drive(1)
                                        print "up"
                                if event.key == (pygame.K_DOWN):
                                        robot.drive(-1)
                                        print "down"
                                if (event.key == pygame.K_ESCAPE):
                                        done = True
                                if (event.key == pygame.K_LEFT):
                                        robot.rotate(1)
                                        print "left"
                                if (event.key == pygame.K_RIGHT):
                                        robot.rotate(-1)
                                        print "right"

                        if event.type == pygame.KEYUP:
                                if event.key == (pygame.K_UP):
                                        robot.drive(0)
                                        print "up release"
                                if event.key == (pygame.K_DOWN):
                                        robot.drive(0)
                                        print "down release"
                                if (event.key == pygame.K_LEFT):
                                        robot.rotate(0)
                                        print "left release"
                                if (event.key == pygame.K_RIGHT):
                                        robot.rotate(0)
                                        print "right release"

except KeyboardInterrupt:
        pygame.quit()

cam.stop()
pygame.quit()
