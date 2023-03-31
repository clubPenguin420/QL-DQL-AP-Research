import pygame
from pygame.locals import *

class Runner(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image = pygame.image.load("Assets\\Player.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)

    def update(self, action):
        pressed_keys = pygame.key.get_pressed()


        if action == 1:
            if self.rect.bottom < 600:
                self.rect.move_ip(0, 15)
        elif action == 2:
            if self.rect.top > 0:
                self.rect.move_ip(0, -15)
        elif action == 3:
            if self.rect.right < 1300:
                self.rect.move_ip(15, 0)
        elif action == 4:
            if self.rect.left > 700:
                self.rect.move_ip(-15, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)