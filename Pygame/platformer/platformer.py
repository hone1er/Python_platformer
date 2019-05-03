from sheet_helper import SpriteSheet
import pygame
import constants
import images
import levels
from characters import Player, Enemy, Bullet
import os

class game():

    def main():


        """ Main Program """
        pygame.init()


        # Set the height and width of the screen
        size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Side-scrolling Platformer")


        # Create the player
        player = Player(SpriteSheet('catman.png'))
        
        # Create bullet list
        bullet_list = pygame.sprite.Group()


        # Create all the levels
        level_list = []
        level_list.append(levels.Level_01(player))
        level_list.append(levels.Level_02(player))

        # Set the current level
        current_level_no = 0
        current_level = level_list[current_level_no]

        active_sprite_list = pygame.sprite.Group()
        player.level = current_level

        player.rect.x = 340
        player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 500
        active_sprite_list.add(player)

        crony = Enemy(450, 475, 20, 20, 600)
        player.level.enemy_list.add(crony)
        




        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == None:
                    player.idle()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    elif event.key == pygame.K_RIGHT:
                        player.go_right()
                    elif event.key == pygame.K_UP:
                        player.jump()
                    elif event.key == pygame.K_SPACE:
                        # Fire a bullet if the user clicks the mouse button
                        bullet = Bullet(player.direction)
                        # Set the bullet so it is where the player is
                        bullet.rect.x = player.rect.x + 10
                        bullet.rect.y = player.rect.y + 10
                
                        # Add the bullet to the lists
                        active_sprite_list.add(bullet)
                        bullet_list.add(bullet)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    elif event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()



            # Update the player.
            active_sprite_list.update()
            # Update items in the level
            current_level.update()

            # Calculate mechanics for each bullet
            for bullet in bullet_list:
        
                # See if it hit a block
                block_hit_list = pygame.sprite.spritecollide(bullet, player.level.platform_list, False)
                enemy_hit_list = pygame.sprite.spritecollide(bullet, player.level.enemy_list, True)
        
                # For each block hit, remove the bullet and add to the score
                for block in block_hit_list:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                for enemy in enemy_hit_list:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                    player.level.enemy_list.remove(enemy)




            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                for crony in player.level.enemy_list:                    
                    crony.end -= diff
                    crony.rect.x -= diff
                    crony.path[0] -= diff
                    crony.path[1] -= diff
                current_level.shift_world(-diff)

            # If the player gets near the left side, shift the world right (+x)
            
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                for crony in player.level.enemy_list:                    
                    crony.end += diff
                    crony.rect.x += diff
                    crony.path[0] += diff
                    crony.path[1] += diff
                current_level.shift_world(diff)

            # If the player gets to the end of the level, go to the next level
            current_position = player.rect.x + current_level.world_shift
            if current_position < current_level.level_limit:
                player.rect.x = 150
                if current_level_no < len(level_list)-1:
                    current_level_no += 1
                    current_level = level_list[current_level_no]
                    player.level = current_level

            # IF the player falls, game done
            if player.rect.y > constants.SCREEN_HEIGHT:
                done = True

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
            font = pygame.font.SysFont(None, 25)
            text = font.render(f"Score: {player.score}", True, constants.BLACK)
            screen.blit(text, (10, 10))
            crony.draw(screen)
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Limit to 60 frames per second
            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.update()

        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()


if __name__ == "__main__":
    game.main()
