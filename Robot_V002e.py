# Import statements
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Tank import Tank

# Settings
WIDTH = 320
HEIGHT = 240

# Initialize Tank
robot = Tank()
robot.correctDirections(False,False,True)

# Camera
cap = cv2.VideoCapture(0)
camcapture.set(3,WIDTH)
camcapture.set(4,HEIGHT)

# Image analysis
lower = np.array([25,10,0])
upper = np.array([60,100,255])

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


# Main loop
auto = False
while True:

        # Read image
        _, frame = cap.read()
        
        # Image filter
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Show image
        cv2.imshow('Robot',res)
        
        # Key events
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit
                break
        if cv2.waitKey(1) & 0xFF == ord('w'):  # Start autonomous
                auto = True
        if cv2.waitKey(1) & 0xFF == ord('e'):  # Stop autonomous
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
