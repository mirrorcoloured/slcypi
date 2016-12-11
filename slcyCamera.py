import picamera
import time
import cv2
import numpy
import matplotlib.pyplot as plt

class Camera(picamera.PiCamera):
    def __init__(self) -> None:
        pass
        

print('starting camera...')
cam = picamera.PiCamera()

ipath = '/home/pi/apple/imgn.jpg'

cam.resolution = (256,256) # (64,64) to (2592,1944)
cam.brightness = 70 # 0 to 100
cam.contrast = 70 # 0 to 100
#cam.image_effect = 'sketch'
cam.awb_mode = 'incandescent'
cam.exposure_mode = 'night'
cam.annotate_background = picamera.Color('blue')
cam.annotate_foreground = picamera.Color('yellow')
#cam.annotate_frame_num = 3
#cam.annotate_text = 'test text'
#cam.annotate_text_size = 72
cam.capture(ipath)
#cam.start_recording('/home/pi/apple/vid.h264')
#time.sleep(5)
#cam.stop_recording()
print('camera finished')

print('begin processing')
img = cv2.imread(ipath)
#cv2.imshow('preview',img)
b,g,r = cv2.split(img)
img = cv2.merge((r,g,b))

kernel = numpy.ones((5,5),numpy.uint8)
imgn = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

plt.subplot(121),plt.imshow(img),plt.title('original')
plt.subplot(122),plt.imshow(imgn),plt.title('OPEN')
#plt.set_xlabel('x axis')
#plt.set_ylabel('y axis')
#plt.set_title('title text')
print('finished processing')
plt.show()
