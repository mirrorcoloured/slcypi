
from ImageAnalysis import ImageAnalysis

# Pygame and camera initialize
pygame.init()
pygame.display.set_caption('My Robot')
pygame.camera.init()
screen = pygame.display.set_mode((640,480),0)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(320,240))
cam.start()

# Camera
image1 = cam.get_image()
image1 = pygame.transform.scale(image1,(640,480))
image1 = pygame.transform.flip(image1,1,1)
screen.blit(image1,(0,0))
pygame.display.update()

IA = ImageAnalysis()

IA.ShowMidPixel(image1,640,480)
