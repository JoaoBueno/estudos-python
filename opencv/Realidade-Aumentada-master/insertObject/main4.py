import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys

camera = cv2.VideoCapture(1)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([640,480])

try:
    while True: 

        ret, frame = camera.read()

        screen.fill([0,0,0])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0,0))
        pygame.display.update()

    for event in pygame.event.get():
        if(event.type == KEYDOWN):
            sys.exit(0)



            
except KeyboardInterrupt:
    pygame.quit()
    cv2.destroyAllWindows()