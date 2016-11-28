
from ImageAnalysis import ImageAnalysis
import pygame
import pygame.camera
import sys
#from picamera import PiCamera
from time import sleep
from PIL import Image
#from pylab import *

# Settings
WIDTH = 320
HEIGHT = 240

# Pygame and camera initialize
pygame.init()
pygame.display.set_caption('My Robot')
pygame.camera.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(WIDTH,HEIGHT))
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

                # User events
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if (event.key == pygame.K_s):

                                    # Set target
                                    rgb = IA.setTarget(image1,WIDTH,HEIGHT)
                                    image1.fill(rgb)
                                    screen.blit(image1,(0,0))
                                    pygame.display.update()
                                    sleep(5)
                                if (event.key ==pygame.K_a):

                                    # Analyze
                                    image1 = IA.convertTrueFalse(image1,WIDTH,HEIGHT)                
                                    screen.blit(image1,(0,0))
                                    pygame.display.update()
                                    sleep(5)
                                if (event.key==pygame.K_c):
                                    pos = IA.getLinePosition(image1,w,h)
                                    print(pos)
                                if (event.key == pygame.K_ESCAPE):
                                        done = True
         
pygame.quit()





