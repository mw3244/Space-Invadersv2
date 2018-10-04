import pygame
from pygame.sprite import Sprite

class Barrier(Sprite):
    def __init__(self, ai_settings, screen):
        super(Barrier, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the barrier image and get its rect.
        self.image = pygame.image.load('images/barrier.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new barrier at the bottom center of the screen.
        #self.rect.centerx = self.screen_rect.centerx
        #self.rect.bottom = self.screen_rect.bottom

    def draw_barrier(self):
        self.screen.blit(self.image, (self.rect.centerx, self.rect.centery))