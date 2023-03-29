import pygame
from pygame.locals import *

class MazePlayer(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image = pygame.image.load("Assets\\Player.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)

    def update(self, action):
        pressed_keys = pygame.key.get_pressed()


        if pressed_keys[K_s]:
            if self.rect.bottom < 600:
                self.rect.move_ip(0, 15)
        elif pressed_keys[K_w]:
            if self.rect.top > 0:
                self.rect.move_ip(0, -15)
        elif pressed_keys[K_d]:
            if self.rect.right < 600:
                self.rect.move_ip(15, 0)
        elif pressed_keys[K_a]:
            if self.rect.left > 0:
                self.rect.move_ip(-15, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)