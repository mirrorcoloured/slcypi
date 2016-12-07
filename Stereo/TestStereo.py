import numpy as np
import cv2
from matplotlib import pyplot as plt
 
imgL = cv2.imread('imL.png',0)
imgR = cv2.imread('imR.png',0)

print imgL.shape, imgR.shape

# Print class
print(type(imgL).__name__)

# Show image DOESNT WORK
plt.imshow(imgL,'gray')
plt.show()

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()
