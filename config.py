import os
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITE_CELL = (240, 217, 181)
BLACK_CELL = (181, 136, 99)
GREEN_CELL = (0, 255, 0)


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        return None
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image
