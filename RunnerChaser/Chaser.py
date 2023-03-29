import pygame
from pygame.locals import *

class Chaser(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image = pygame.image.load("Assets\\Chaser.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.active = True

    def update(self, action):
        pressed_keys = pygame.key.get_pressed()


        if pressed_keys[K_DOWN]:
            if self.rect.bottom < 600:
                self.rect.move_ip(0, 15)
        elif pressed_keys[K_UP]:
            if self.rect.top > 0:
                self.rect.move_ip(0, -15)
        elif pressed_keys[K_RIGHT]:
            if self.rect.right < 1300:
                self.rect.move_ip(15, 0)
        elif pressed_keys[K_LEFT]:
            if self.rect.left > 700:
                self.rect.move_ip(-15, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)