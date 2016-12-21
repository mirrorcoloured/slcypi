import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

cap = cv2.VideoCapture(0)

# Initialize image analysis
def featureMatch(current,previous):
                orb = cv2.ORB_create()
                cv2.ocl.setUseOpenCL(False)
                kp1, des1 = orb.detectAndCompute(current,None)
                kp2, des2 = orb.detectAndCompute(previous,None)
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1,des2)
                matches = sorted(matches, key = lambda x:x.distance)
                res = cv2.drawMatches(current,kp1,previous,kp2,matches[:10],None, flags=2)
                return(res)

# Previous 
_, frame = cap.read()
previous = frame

while True:

    # Current
    _, frame = cap.read()
    current = frame

    # Process image
    res = featureMatch(current, previous)

    # Show result
    cv2.imshow('res',res)

    # Swap images
    previous = current
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
