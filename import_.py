try:
    # always import
    import sys
    import os
    import pygame
    from pygame.locals import *

except ImportError as err:
    print ("Couldn't load module. %s" % (err))
    sys.exit(2)

def load_image(name, colorkey=None):
    # Load image and return image object and it's rect
    # Accepts the image and a colorkey for transparent background. If -1, selects pixel in top left as colorkey

    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print ('Cannot load image:', name)
        raise SystemExit(message)
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    # Load sound and return sound object
    fullname = os.path.join('assets', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)
    return sound