# Import statements
import sys
sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Tank import Tank
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Settings
WIDTH = 320
HEIGHT = 240

# Initialize Tank
robot = Tank()
robot.correctDirections(False,False,True)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (WIDTH, HEIGHT)
camera.framerate = 4
rawCapture = PiRGBArray(camera, size=(WIDTH, HEIGHT))
 
# allow the camera to warmup
time.sleep(0.1)

# Image analysis
lower = np.array([25,10,0])
upper = np.array([60,100,255])

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
# capture frames from the camera
#cv2.startWindowThread()
#cv2.namedWindow("Frame")
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame = frame.array
        print(frame.shape)
 
        # Image filter
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
        print(hsv.shape)
        mask = cv2.inRange(hsv, lower, upper)
        print(mask.shape)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        print(res.shape)        

        # show the frame
        cv2.imshow("Frame", res)
        ksey = cv2.waitKey(1) & 0xFF
 
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
        # Key events
        if key == ord("q"):
                break
        if key == ord('q'):  # Quit
                break
        if key == ord('w'):  # Start autonomous
                auto = True
        if key == ord('e'):  # Stop autonomous
                auto = False
        
        # Autonomous
        if auto == True:
        
                # Analyze line
                aRes = analyzeLine(mask, WIDTH, HEIGHT)
                print(aRes)
                dir = aRes[0]
                
                # Drive         
                if abs(pos) > 0.25:
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

cap.release()
cv2.destroyAllWindows()
