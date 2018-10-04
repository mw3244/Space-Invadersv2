import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ai_settings, screen, row_number, index):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.green_animation_clock = ai_settings.animation_clock
        self.blue_animation_clock = ai_settings.animation_clock
        self.pink_animation_clock = ai_settings.animation_clock
        self.animation_clock_total = ai_settings.animation_clock

        self.green_images = []
        self.green_images.append(pygame.image.load('images/Greeny_1.png'))
        self.green_images.append(pygame.image.load('images/Greeny_2.png'))

        self.blue_images = []
        self.blue_images.append(pygame.image.load('images/Bluey_1.png'))
        self.blue_images.append(pygame.image.load('images/Bluey_2.png'))

        self.pink_images = []
        self.pink_images.append(pygame.image.load('images/Pinky_1.png'))
        self.pink_images.append(pygame.image.load('images/Pinky_2.png'))

        self.index = index

        # Load the alien image and set its rect attribute

        if row_number % 6 == 0 or row_number % 6 == 1:
            self.image = self.green_images[self.index]
            self.rect = self.image.get_rect()
            self.alienType = "green"

        if row_number % 6 == 2 or row_number % 6 == 3:
            self.image = self.blue_images[self.index]
            self.rect = self.image.get_rect()
            self.alienType = "blue"

        if row_number % 6 == 4 or row_number % 6 == 5:
            self.image = self.pink_images[self.index]
            self.rect = self.image.get_rect()
            self.alienType = "pink"

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)


    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def green_update(self):
        """Move the alien left or right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.green_animation_clock -= 1
        if self.green_animation_clock <= 0:
            self.index += 1
            if self.index >= len(self.green_images):
                self.index = 0
            self.green_animation_clock = self.animation_clock_total
        self.image = self.green_images[self.index]

    def blue_update(self):
        """Move the alien left or right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.blue_animation_clock -= 1
        if self.blue_animation_clock <= 0:
            self.index += 1
            if self.index >= len(self.blue_images):
                self.index = 0
            self.blue_animation_clock = self.animation_clock_total
        self.image = self.blue_images[self.index]

    def pink_update(self):
        """Move the alien left or right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.pink_animation_clock -= 1
        if self.pink_animation_clock <= 0:
            self.index += 1
            if self.index >= len(self.pink_images):
                self.index = 0
            self.pink_animation_clock = self.animation_clock_total
        self.image = self.pink_images[self.index]
    #def blitme(self):
        #"""Draw the alien at its current location."""
        #self.screen.blit(self.image, self.rect)

class Ufo():
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/oscar.png')
        self.rect = self.image.get_rect()
        self.rect.right = 0
        self.rect.top = 80
        self.ufo_active = False

    def update(self):
        self.rect.left += self.ai_settings.alien_speed_factor
        #self.rect = self.image.get_rect()
        if self.rect.left > self.ai_settings.screen_width:
            self.reset()

    def reset(self):
        self.rect.right = 0
        self.ufo_active = False

    def draw_ufo(self):
        self.screen.blit(self.image, (self.rect.left, self.rect.top))