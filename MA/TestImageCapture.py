
import time
import picamera
import numpy as np
import cv2

import pygame

# Settings
WIDTH = 320
HEIGHT = 240

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 24
    time.sleep(2)
    output = np.empty((320 * 240 * 3,), dtype=np.uint8)
    camera.capture(output, 'rgb', use_video_port=True)
    #camera.capture(output, 'rgb')
    print(type(output))
    
    done = False
    while not done:

            # Capture image
            camera.capture(output, 'rgb', use_video_port=True)

            # Convert to surface
            #print(output.shape)
            newoutput = np.reshape(output, (240,320,3))            
            #print(newoutput.shape)            
            sface = pygame.surfarray.make_surface(newoutput)
            sface = pygame.transform.rotate(sface,270)
            
            # Display
            screen.blit(sface,(0,0))
            pygame.display.update()            

            # Capture key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE):
                        done = True
                        
pygame.quit()
