import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from ImageAnalysis import ImageAnalysis

cap = cv2.VideoCapture(0)

IA = ImageAnalysis()

# Previous 
_, frame = cap.read()
previous = frame
hsv = np.zeros_like(previous)
hsv[...,1] = 255

while True:

    # Current
    _, frame = cap.read()
    current = frame

    # Process image
    #res = IA.featureMatch(current,previous)
    res = IA.opticalFlow(current,previous, hsv)

    # Show result
    cv2.imshow('res',res)

    # Swap images
    previous = current

    # Reduce speed
    #time.sleep(1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
