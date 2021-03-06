import sys
import pygame
import random
import math
from PIL import Image
from time import sleep
from bullet import Bullet
from bullet import Bullet2
from alien import Alien
from barrier import Barrier
from button import Text
from button import Picture

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            
def check_menu_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, highscore_button, back_button, highscoreText, bullets2):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_highscore_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, highscore_button, back_button, highscoreText)
            return check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bullets2)
    return True

def check_highscore_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, highscore_button, back_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if back_button.rect.collidepoint(mouse_x, mouse_y):
                return False
    return True


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, bullets2):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        bullets2.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        return False
    return True

def check_highscore_button (ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, highscore_button, back_button, highscoreText):
    button_clicked = highscore_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        highscore_menu(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, highscore_button, back_button, highscoreText)

def highscore_menu(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, highscore_button, back_button, highscoreText):
    highscore_menu = True
    while highscore_menu:
        highscore_menu = check_highscore_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, highscore_button, back_button)
        screen.fill(ai_settings.bg_color)
        back_button.draw_button()
        highscoreText.draw_text()

        pygame.display.flip()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create a new bullet and add it to the bullets group.
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        pygame.mixer.Sound('audio/shoot.wav').play()

def fire_bullet2(ai_settings, screen, alien, bullets2):
    new_bullet2 = Bullet2(ai_settings, screen, alien)
    bullets2.add(new_bullet2)

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bullets2, ufo, barriers):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    bullets2.update()
    ship_exploding = False

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet2 in bullets2.copy():
        if bullet2.rect.top > ai_settings.screen_height:
            bullets2.remove(bullet2)
        if bullet2.rect.colliderect(ship.rect):
            ship_exploding = ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo)

    list = check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bullets2, ufo, barriers)
    list.append(ship_exploding)
    if list[0] == True or list[2] == True or list[4] == True or list[6] == True or list[8] == True:
        return list

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bullets2, ufo, barriers):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.

    #collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #if collisions:
        #for aliens in collisions.values():
            #stats.score += ai_settings.greeny_points * len(aliens)
            #sb.prep_score()
    pointsTextOn = False
    pointsText = Text(ai_settings, screen, "", 0, 0, 0, 0, (0, 0, 0))

    alienBlueDeath = False
    alienBlueDeathPicture = Picture(ai_settings, screen, -100, -100, pygame.image.load('images/bluey_dead.png'))

    alienGreenDeath = False
    alienGreenDeathPicture = Picture(ai_settings, screen, -100, -100, pygame.image.load('images/greeny_dead.png'))

    alienPinkDeath = False
    alienPinkDeathPicture = Picture(ai_settings, screen, -100, -100, pygame.image.load('images/pinky_dead.png'))


    for bullet in bullets:
        for alien in aliens:
            if bullet.rect.colliderect(alien.rect):
                pygame.mixer.Sound('audio/invaderkilled.wav').play()
                if alien.alienType == "green":
                    stats.score += ai_settings.greeny_points
                    sb.prep_score()
                    alienGreenDeath = True
                    alienGreenDeathPicture = Picture(ai_settings, screen, alien.rect.x, alien.rect.y, pygame.image.load('images/greeny_dead.png'))
                if alien.alienType == "blue":
                    stats.score += ai_settings.bluey_points
                    sb.prep_score()
                    alienBlueDeath = True
                    alienBlueDeathPicture = Picture(ai_settings, screen, alien.rect.x, alien.rect.y, pygame.image.load('images/bluey_dead.png'))
                if alien.alienType == "pink":
                    stats.score += ai_settings.pinky_points
                    sb.prep_score()
                    alienPinkDeath = True
                    alienPinkDeathPicture = Picture(ai_settings, screen, alien.rect.x, alien.rect.y, pygame.image.load('images/pinky_dead.png'))
        if bullet.rect.colliderect(ufo.rect):
            pygame.mixer.Sound('audio/invaderkilled.wav').play()
            points_scored = (ai_settings.ufo_points * random.randint(1,5))
            pointsText = Text(ai_settings, screen, str(points_scored), 40, 40, ufo.rect.centerx, ufo.rect.centery, (255, 255, 255))
            pointsTextOn = True
            ufo.reset()
            stats.score += points_scored
            sb.prep_score()

    check_high_score(stats, sb)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    #for bullet2 in bullets2:
        #for barrier in barriers:
            #if bullet2.rect.colliderect(barrier):
                #bullets2.remove(bullet2)
                #img = Image.open("images/barrier.bmp")
                #pixels = img.load()
                #for i in range (img.size[0]):
                    #for j in range(img.size[1]):
                        #pixels[i,j] = (i, j, 100)
                #img.save('images/barrier2.bmp')
               # barrier.image = pygame.image.load('images/barrier2.bmp')

    barriercollision = pygame.sprite.groupcollide(barriers, bullets2, False, True)
    #if barriercollision:
        #for bullets2 in barriercollision.values():
            #bullets2.remove(bullets2)


    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        bullets.empty()
        bullets2.empty()
        ufo.reset()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

    return [pointsTextOn, pointsText, alienBlueDeath, alienBlueDeathPicture, alienGreenDeath, alienGreenDeathPicture, alienPinkDeath, alienPinkDeathPicture]

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def create_barriers(ai_settings, screen, ship, barriers):
    barrier = Barrier(ai_settings, screen)
    number_of_barriers = math.floor(ai_settings.screen_width / 240)

    for barrier_number in range (number_of_barriers):
        barrier = Barrier(ai_settings, screen)
        barrier.rect.top = ship.rect.top - 50
        barrier.rect.left = barrier_number * 240 + 80
        barriers.add(barrier)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number, index):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen, row_number, index)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 150
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height * 7)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen, 0, 0)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row
            index = (alien_number + row_number) % 2
            create_alien(ai_settings, screen, aliens, alien_number, row_number, index)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo):
    """Respond to ship being hit by alien."""
    ship_exploding = True
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        bullets2.empty()
        ufo.reset()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        highScoreFile = open("highscore.txt", "w")
        highScoreFile.write(str(stats.high_score))
        highScoreFile.close()
        stats.game_active = False
        pygame.mouse.set_visible(True)

    return ship_exploding

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo):
    """Check if the fleet is at an edge, and then update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    for alien in aliens:
        if alien.alienType == "green":
            alien.green_update()
            rint = random.randint(0,12288)
            if rint == 0:
                fire_bullet2(ai_settings, screen, alien, bullets2)
        if alien.alienType == "blue":
            alien.blue_update()
            rint = random.randint(0,12288)
            if rint == 0:
                fire_bullet2(ai_settings, screen, alien, bullets2)
        if alien.alienType == "pink":
            alien.pink_update()
            rint = random.randint(0,12288)
            if rint == 0:
                fire_bullet2(ai_settings, screen, alien, bullets2)

    rint = random.randint(0,6000)
    if rint == 0 and ufo.ufo_active == False:
        ufo.ufo_active = True

    if ufo.ufo_active:
        pygame.mixer.Sound('audio/ufo.wav').play()
        ufo.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, bullets2, ufo)

def update_barriers(ai_settings, screen, barriers, aliens, ship):
    barriers.update()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bullets2, ufo, barriers, list1, animation_clock):
    """Update images on the screen and flip to the new screen"""
    # Rewdraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    barriers.draw(screen)
    ufo.draw_ufo()

    for bullet2 in bullets2.sprites():
        bullet2.draw_bullet2()

    # list1[0] is boolean for ufo point animation, list[1] is text and rect information for ufo point animation
    if isinstance(list1, list):
        if list1[0] == True:
            list1[1].draw_text()
            animation_clock -= 1

    # list1[2] is boolean for blue alien death, list1[3] is the picture
    if isinstance(list1, list):
        if list1[2] == True:
            list1[3].draw_picture()
            animation_clock -= 1

    # list1[4] is boolean for green alien death, list1[5] is the picture
    if isinstance(list1, list):
        if list1[4] == True:
            list1[5].draw_picture()
            animation_clock -= 1

    # list1[6] is boolean for pink alien death, list1[7] is the picture
    if isinstance(list1, list):
        if list1[6] == True:
            list1[7].draw_picture()
            animation_clock -= 1

    # list1[8] is a bool for the ship exploding
    if isinstance(list1, list):
        if list1[8] == True:
            ship_exploding_1 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_1.png'))
            ship_exploding_1.draw_picture()
            pygame.display.flip()
            pygame.mixer.Sound('audio/explosion.wav').play()
            sleep(0.1)

            ship_exploding_2 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_2.png'))
            ship_exploding_2.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            ship_exploding_3 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_3.png'))
            ship_exploding_3.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            ship_exploding_4 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_4.png'))
            ship_exploding_4.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            ship_exploding_5 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_5.png'))
            ship_exploding_5.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            ship_exploding_6 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_6.png'))
            ship_exploding_6.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            ship_exploding_7 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_7.png'))
            ship_exploding_7.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            ship_exploding_8 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_8.png'))
            ship_exploding_8.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            ship_exploding_9 = Picture(ai_settings, screen, ship.rect.x, ship.rect.y,
                                            pygame.image.load('images/ship_death_9.png'))
            ship_exploding_9.draw_picture()
            pygame.display.flip()
            sleep(0.1)

            list1[8] = False

    if animation_clock <= 0:
        list1[0] = False
        list1[2] = False
        list1[4] = False
        list1[6] = False
        animation_clock = ai_settings.animation_clock

    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    #if not stats.game_active:
        #play_button.draw_button()


    # Make the most recently drawn screen visible
    pygame.display.flip()

    return animation_clock
    
def update_menu_screen(ai_settings, screen, play_button, highscore_button, spaceText, invadersText, pinkyPicture, blueyPicture, greenyPicture, oscarPicture, pinkyText, blueyText, greenyText, oscarText):
    screen.fill(ai_settings.bg_color)
    
    play_button.draw_button()
    highscore_button.draw_button()
    spaceText.draw_text()
    invadersText.draw_text()
    pinkyPicture.draw_picture()
    blueyPicture.draw_picture()
    greenyPicture.draw_picture()
    oscarPicture.draw_picture()
    pinkyText.draw_text()
    blueyText.draw_text()
    greenyText.draw_text()
    oscarText.draw_text()
    
    
    pygame.display.flip()