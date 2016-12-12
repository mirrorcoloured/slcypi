import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)

# ADJUST THESE VALUES!!
lower = np.array([25,10,0])
upper = np.array([60,100,255])

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow('frame', frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    if cv2.waitKey(1) & 0xFF == ord('7'):
        lower[0] = lower[0] + 5
        print(lower[0])
    if cv2.waitKey(1) & 0xFF == ord('u'):
        lower[0] = lower[0] - 5
        print(lower[0])
    if cv2.waitKey(1) & 0xFF == ord('j'):
        upper[0] = upper[0] + 5
        print(upper[0])
    if cv2.waitKey(1) & 0xFF == ord('m'):
        upper[0] = upper[0] - 5
        print(upper[0])

    if cv2.waitKey(1) & 0xFF == ord('8'):
        lower[1] = lower[1] + 5
        print(lower[1])
    if cv2.waitKey(1) & 0xFF == ord('i'):
        lower[1] = lower[1] - 5
        print(lower[1])
    if cv2.waitKey(1) & 0xFF == ord('k'):
        upper[1] = upper[1] + 5
        print(upper[1])
    if cv2.waitKey(1) & 0xFF == ord(','):
        upper[1] = upper[1] - 5
        print(upper[1])


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
