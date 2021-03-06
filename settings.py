import pygame
import math

class Settings():
    """"A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Bullet2 settings
        self.bullet2_color = 0, 255, 0
        self.bullet2_speed_factor = 2

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alient point values increase
        self.score_scale = 1.5

        # Animation clock
        self.animation_clock = 100

        self.frequency = 42050

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_drection of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.greeny_points = 40
        self.bluey_points = 20
        self.pinky_points = 10
        self.ufo_points = 100

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        pygame.mixer.quit()
        if self.frequency < 190000:
            self.frequency += 5000
        pygame.mixer.init(self.frequency)
        pygame.mixer.music.load('audio/OST.mp3')
        pygame.mixer.music.play(-1)


        #self.alien_points = int(self.alien_points * self.score_scale)