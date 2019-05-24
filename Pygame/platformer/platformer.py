from characters import Player, Enemy, Bullet
from sheet_helper import SpriteSheet
from levels import screen, size
import constants
import images
import levels
import pygame
import os




class Game:
    def main(self):

        """ Main Program """
        pygame.init()


        # Create the player
        player = Player(SpriteSheet('catman.png'))
        # Create all the levels
        level_list = []
        level_list.append(levels.Level_01(player))
        level_list.append(levels.Level_02(player))


        # Set the current level & player position
        current_level_no = 0
        current_level = level_list[current_level_no]

        active_sprite_list = pygame.sprite.Group()
        player.level = current_level
        player.rect.x = 340
        player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 500
        active_sprite_list.add(player)


        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        start_ticks=pygame.time.get_ticks() #starter tick

        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == None:
                    player.idle()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        player.go_left()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player.go_right()
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        player.jump()
                    elif event.key == pygame.K_SPACE:
                        if len(player.bullet_list) < 4:
                            # Fire a bullet if the user clicks the mouse button
                            bullet = Bullet(player)
                            # Set the bullet so it is where the player is
                            bullet.rect.x = player.rect.x + 10
                            bullet.rect.y = player.rect.y + 10
                            # Add the bullet to the lists
                            player.bullet_list.add(bullet)

                # set what happens when player lets the key up
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()


            # Update the player.
            active_sprite_list.update()
            player.bullet_list.update()
            # Update items in the level
            current_level.update()
                        
            
            ydiff = 0
            diff = 0
            # if the player gets near the top, shift the world up (ydiff)
            if player.rect.top <= 20:
                ydiff = player.rect.top - 20
                player.rect.top = 20
                current_level.shift_world_y(ydiff)

            # if the player gets near the bottom, shift the world down (ydiff)
            if player.rect.bottom >= 550:
                ydiff = player.rect.bottom - 550
                player.rect.bottom = 550
                current_level.shift_world_y(ydiff)

            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shift_world(-diff)

            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                current_level.shift_world(diff)
                
            # If the player gets to the end of the level, go to the next level
            current_position = player.rect.x + current_level.world_shift
            if current_position < current_level.level_limit:
                player.rect.x = 150
                if current_level_no < len(level_list)-1:
                    current_level_no += 1
                    current_level = level_list[current_level_no]
                    player.level = current_level
                    player.stop()

            # IF the player falls, game done
            if player.rect.y + player.level.world_shift_y + 75 > constants.SCREEN_HEIGHT:
                done = True

            seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
            player.bullet_list.draw(screen)
            font = pygame.font.SysFont(None, 25)
            showscore = font.render(f"Score: {player.score}", True, constants.BLACK)
            showclock = font.render(f"Time: {round(seconds,2)}", True, constants.BLACK)
            screen.blit(showscore, (10, 10))
            screen.blit(showclock, (constants.SCREEN_WIDTH/2, 10))
            for crony in player.level.enemy_list:
                crony.draw(screen)
            for platform in player.level.platform_list:
                try:
                    platform.draw(screen)
                except:
                    pass
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            # Limit to 60 frames per second
            clock.tick(60)
            # Go ahead and update the screen with what we've drawn.
            pygame.display.update()
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()


#####################################################################################################
                    ####      ####     #########  #########   ####  ####    ####
                  #### ###   ### ###   ###        #### ####   ####  ####    ####
                 ####   ### ###  ####  ########   ####  ####  ####  ####    ####
                ####    #####     #### ###        ####    ### ####  ############
                ####              #### #########  ####     #######  ############
####################################################################################################

#used in message_display()
def text_objects(text, font):
    textSurface = font.render(text, True, constants.BLACK)
    return textSurface, textSurface.get_rect()  

#create a button.
def button(msg,x,y,w,h,ic,ac, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,ac, (x,y,w,h))
        if click[0] == 1 and action!=None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    smallText = pygame.font.SysFont('cambria',20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)),(y+(h/2)))
    screen.blit(textSurf, textRect) 

def quit_game():
    pygame.quit()
    quit()
    
#start screen
def game_intro(game):


    clock = pygame.time.Clock()

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((50,70,220))
        largeText = pygame.font.Font('freesansbold.ttf', 65)
        TextSurf, TextRect = text_objects("Welcome to Catman", largeText)
        TextRect.center = ((constants.SCREEN_WIDTH/2),(constants.SCREEN_HEIGHT/2))
        screen.blit(TextSurf, TextRect)
            
        button("START",300,500,100,50,constants.GREEN,constants.BLUE,game.main)
        button("EXIT",600,500,100,50,constants.RED,constants.BLUE,quit_game)

        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    game = Game()
    #game_intro(game)
    game.main()