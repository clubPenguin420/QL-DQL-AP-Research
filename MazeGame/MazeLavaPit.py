import pygame

class MazeLavaPit(pygame.sprite.Sprite):
    def __init__(self, ul_x, ul_y, w, h):
        super().__init__()
        self.x = ul_x
        self.y = ul_y
        self.width = w
        self.height = h
        self.a_color = (222, 91, 16)
        self.da_color = (71, 68, 65)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.active = True

    # def update(self, player):

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.a_color, self.rect)
        else:
            pygame.draw.rect(surface, self.da_color, self.rect)