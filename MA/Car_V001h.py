#!/usr/bin/python
#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import pygame
import pygame.camera
import sys
#from picamera import PiCamera
from time import sleep
from PIL import Image
from pylab import *

sys.path.append("/home/pi/Adafruit-Motor-HAT-Python-Library") ### ADD PATH
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


# Pygame and camera initialize
pygame.init()
pygame.display.set_caption('My Robot')
pygame.camera.init()
screen = pygame.display.set_mode((640,480),0)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(320,240))
cam.start()

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
rightMotor = mh.getMotor(1)
leftMotor = mh.getMotor(2)

# Method to relase all motors
def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def drive(direction, speed=200):
        """Method control forward speed
        direction <integer> {-1,0,1}
        speed <integer> {0:255}"""
        if direction == 1:
                leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                rightMotor.run(Adafruit_MotorHAT.FORWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == -1:
                leftMotor.run(Adafruit_MotorHAT.FORWARD)
                rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == 0:
                leftMotor.setSpeed(0)
                rightMotor.setSpeed(0)
                leftMotor.run(Adafruit_MotorHAT.RELEASE)
                rightMotor.run(Adafruit_MotorHAT.RELEASE)

def rotate(direction, speed=50):
        """Method to control steering
        direction <integer> {-1,0,1}
        speed <integer>"""
        if direction == 1:
                leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == -1:
                leftMotor.run(Adafruit_MotorHAT.FORWARD)
                rightMotor.run(Adafruit_MotorHAT.FORWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == 0:
                leftMotor.setSpeed(0)
                rightMotor.setSpeed(0)
                leftMotor.run(Adafruit_MotorHAT.RELEASE)
                rightMotor.run(Adafruit_MotorHAT.RELEASE)



# Method to convert pixel int to RGB values
def getRGB(pixelInt):
        blue = pixelInt & 255
        green = (pixelInt >> 8) & 255
        red = (pixelInt >> 16) & 255
        myArray = [red, green, blue]
        return myArray

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
        print average
        
        # standardize
        standardVal = (average - (640 / 2)) / (640 /2) 
        print standardVal

        # Compare to diction cut point
        direction = 0
        if standardVal < 0- directionCutpoint:
                direction = 1
        if standardVal > directionCutpoint:
                direction = -1

        # Return direction
        return direction

def showMidPixel(img):

        # Transform        
        pxarray = pygame.PixelArray(img)
        myPixel = pxarray[150,150]
        rgb = getRGB(myPixel)
        print rgb

def checkPixelMatch(img):
        pxarray = pygame.PixelArray(img)
        myPixel = pxarray[150,150]
        rgb = getRGB(myPixel)

        global tp

        distance = (tp[0] - rgb[0]) ** 2 + (tp[1] - rgb[1]) ** 2 +(tp[2] - rgb[2]) ** 2
        print distance
        if abs(distance < 20):
                print "Yes"
        else:
                print "no"

# Set things
currentSpeed = 0
atexit.register(turnOffMotors)

# Target pixel
tp = (100,90,30)

try:

        print('starting loop')
        done = False
        while not done:

                # Camera
                image1 = cam.get_image()
                image1 = pygame.transform.scale(image1,(640,480))
                image1 = pygame.transform.flip(image1,1,1)
                screen.blit(image1,(0,0))
                pygame.display.update()

                # print mid pixel
                # showMidPixel(image1)
                #checkPixelMatch(image1)

                # Analyze
                direction = analyzeLine(image1)
                #print "Direction: " + direction

                # Redirect based on direction
                #rotate(direction)

                # User events
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == (pygame.K_UP):
                                        drive(1)
                                        print "up"
                                if event.key == (pygame.K_DOWN):
                                        drive(-1)
                                        print "down"
                                if (event.key == pygame.K_ESCAPE):
                                        done = True
                                if (event.key == pygame.K_LEFT):
                                        rotate(1)
                                        print "left"
                                if (event.key == pygame.K_RIGHT):
                                        rotate(-1)
                                        print "right"

                        if event.type == pygame.KEYUP:
                                if event.key == (pygame.K_UP):
                                        drive(0)
                                        print "up release"
                                if event.key == (pygame.K_DOWN):
                                        drive(0)
                                        print "down release"
                                if (event.key == pygame.K_LEFT):
                                        rotate(0)
                                        print "left release"
                                if (event.key == pygame.K_RIGHT):
                                        rotate(0)
                                        print "right release"

except KeyboardInterrupt:
        pygame.quit()

cam.stop()
pygame.quit()

leftMotor.setSpeed(0)
leftMotor.run(Adafruit_MotorHAT.RELEASE)
rightMotor.setSpeed(0)
rightMotor.run(Adafruit_MotorHAT.RELEASE)
