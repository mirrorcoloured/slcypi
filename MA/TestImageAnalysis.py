
from ImageAnalysis import ImageAnalysis
import pygame
import pygame.camera
import sys
#from picamera import PiCamera
from time import sleep
from PIL import Image
#from pylab import *


# Pygame and camera initialize
pygame.init()
pygame.display.set_caption('My Robot')
pygame.camera.init()
screen = pygame.display.set_mode((320,240),0)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(320,240))
cam.start()


IA = ImageAnalysis()


done = False
while not done:

                # Camera
                image1 = cam.get_image()
                #image1 = pygame.transform.scale(image1,(640,480))
                image1 = pygame.transform.flip(image1,1,1)
                screen.blit(image1,(0,0))
                pygame.display.update()

                IA.showMidPixel(image1,320,240)

                # Convert
                pxarray = IA.convertTrueFalse(image1,320,240)

                image1 = pygame.PixelArray.make_surface(pxarray)
                screen.blit(image1,(0,0))
                pygame.display.update()

                IA.showMidPixel(image1,320,240)

                sleep(3)
                # User events
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if (event.key == pygame.K_ESCAPE):
                                        done = True
         
pygame.quit()





