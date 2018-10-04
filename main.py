import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from button import Button2
from button import Text
from button import Picture
from ship import Ship
from alien import Ufo
from barrier import Barrier
import game_functions as gf

def run_game():
    # Initialize game and create a screen object.
    frequency = 22050
    pygame.mixer.init(frequency)
    pygame.mixer.music.load('audio/OST.mp3')
    pygame.mixer.music.play(-1)
    pygame.init()
    ufo_effect = pygame.mixer.Sound('audio/ufo.wav')
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
    highscore_button = Button2(ai_settings, screen, "High Score")
    back_button = Button2(ai_settings, screen, "Back")

    # Make a ship.
    ship = Ship(ai_settings, screen)

    # Make a ufo
    ufo = Ufo(ai_settings, screen)

    # Make a group to store bullets in.
    bullets = Group()
    bullets2 = Group()

    # Make an alien
    aliens = Group()

    # Make barriers
    barriers = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create a group of barriers
    gf.create_barriers(ai_settings, screen, ship, barriers)

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    highScoreFile = open("highscore.txt", "r")
    stats.high_score = int(highScoreFile.readline())
    highScoreFile.close()
    sb = Scoreboard(ai_settings, screen, stats)
    spaceText = Text(ai_settings, screen, "SPACE", 200, 40, ai_settings.screen_width / 2 - 50, 40, (255, 255, 255))
    invadersText = Text(ai_settings, screen, "INVADERS", 200, 40, ai_settings.screen_width/2 - 75, 80, (0, 255, 0))
    pinkyPicture = Picture(ai_settings, screen, ai_settings.screen_width / 2 - 75, 190, pygame.image.load('images/pinky_2.png'))
    pinkyText = Text(ai_settings, screen, "= 10 PTS     PINKY", 200, 40, ai_settings.screen_width / 2, 190, (255, 255, 255))
    blueyPicture = Picture(ai_settings, screen, ai_settings.screen_width / 2 - 75, 240, pygame.image.load('images/bluey_2.png'))
    blueyText = Text(ai_settings, screen, "= 20 PTS     BLUEY", 200, 40, ai_settings.screen_width / 2, 240, (255, 255, 255))
    greenyPicture = Picture(ai_settings, screen, ai_settings.screen_width / 2 - 75, 290, pygame.image.load('images/greeny_2.png'))
    greenyText = Text(ai_settings, screen, "= 40 PTS     GREENY", 200, 40, ai_settings.screen_width / 2, 290, (255, 255, 255))
    oscarPicture = Picture(ai_settings, screen, ai_settings.screen_width / 2 - 75, 340, pygame.image.load('images/oscar.png'))
    oscarText = Text(ai_settings, screen, "= ???           OSCAR", 200, 40, ai_settings.screen_width / 2, 340, (255, 255, 255))

    while True:
        highscoreText = Text(ai_settings, screen, "HIGH SCORE: " + str(stats.high_score), 200, 40, ai_settings.screen_width / 2 - 100, 40, (255, 255, 255))
        menu_loop = True
   
        while menu_loop:
            menu_loop = gf.check_menu_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, highscore_button, back_button, highscoreText, bullets2)
            gf.update_menu_screen(ai_settings, screen, play_button, highscore_button, spaceText, invadersText, pinkyPicture, blueyPicture, greenyPicture, oscarPicture, pinkyText, blueyText, greenyText, oscarText)

        # Start the main loop for the game.
        while stats.game_active:
            gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
            if stats.game_active:
                ship.update()
                gf.update_barriers(ai_settings, screen, barriers, aliens, ship)
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bullets2, ufo)
                gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo)

            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bullets2, ufo, barriers)

run_game()