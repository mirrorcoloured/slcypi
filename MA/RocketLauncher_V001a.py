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

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

mh = Adafruit_MotorHAT(addr=0x60)
leftMotor = mh.getMotor(1)
rightMotor = mh.getMotor(2)
        
def turnOffMotors(self):
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

#atexit.register(turnOffMotors)

m1 = mh.getMotor(1)
m2 = mh.getMotor(2)

# Settings
WIDTH = 320
HEIGHT = 240

# Initialize ImageAnalysis
IA = ImageAnalysis()
IA.filterLower = np.array([25,35,70])
IA.filterUpper = np.array([65,255,205])

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def faceDetection(bgr):
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
                cv2.rectangle(bgr,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = bgr[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
        return(faces,bgr)

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

# Start settings
done = False

def aim(faces):
        for (x,y,w,h) in faces:
                # Compute position
                x = x + w / 2
                y = y + h / 2

                # Move

                # Shoot
                print("Poof!")

with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
                camera.resolution = (WIDTH, HEIGHT)                
                                
                while done == False:

                        # Image capture
                        camera.capture(stream, 'bgr', use_video_port=True)
                        bgr = stream.array                        
                        
                        # Image process
 #                       faces, res = faceDetection(bgr)
                        
                        # Image transpose
                        res = cv2.transpose(bgr)
                   
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

                                        # Drive commands
                                        if event.key == (pygame.K_UP):
                                                m2.run(Adafruit_MotorHAT.FORWARD)
                                                m2.setSpeed(120)
                                        if event.key == (pygame.K_DOWN):
                                                m2.run(Adafruit_MotorHAT.BACKWARD)
                                                m2.setSpeed(120)
                                        if (event.key == pygame.K_LEFT):
                                                m1.run(Adafruit_MotorHAT.FORWARD)
                                                m1.setSpeed(120)
                                        if (event.key == pygame.K_RIGHT):
                                                m1.run(Adafruit_MotorHAT.BACKWARD)
                                                m1.setSpeed(120)
                                if event.type == pygame.KEYUP:
                                        if event.key == (pygame.K_UP):
                                                m2.run(Adafruit_MotorHAT.RELEASE)
                                        if event.key == (pygame.K_DOWN):
                                                m2.run(Adafruit_MotorHAT.RELEASE)
                                        if (event.key == pygame.K_LEFT):
                                                m1.run(Adafruit_MotorHAT.RELEASE)
                                        if (event.key == pygame.K_RIGHT):
                                                m1.run(Adafruit_MotorHAT.RELEASE)
                                                
                        # Handle stream
                        stream.seek(0)
                        stream.truncate()

                        # Compute fps
                        #lapseTime = (time.time() - startTime)
                        #startTime = time.time()
                        #if lapseTime > 0:
                        #        fps = 1.0 / lapseTime
                        #        print("fps: " + str(fps))

robot.stop()
pygame.quit()
