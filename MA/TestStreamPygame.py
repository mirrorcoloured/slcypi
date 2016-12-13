import cv2
import picamera
import picamera.array
import pygame

WIDTH = 320
HEIGHT = 240

# Initialize Pygame
pygame.init()
pygame.display.set_caption('My Robot')
screen = pygame.display.set_mode((WIDTH,HEIGHT),0)

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)

        while True:
            camera.capture(stream, 'bgr', use_video_port=True)
            # stream.array now contains the image data in BGR order

            frame = stream.array
            sface = pygame.surfarray.make_surface(frame)                        
            
            screen.blit(sface,(0,0))
            pygame.display.update()            
                        

            #cv2.imshow('frame', stream.array)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            # reset the stream before the next capture
            stream.seek(0)
            stream.truncate()

        cv2.destroyAllWindows()
