from sheet_helper import SpriteSheet
import pygame
import constants
import images
import levels


class Player(pygame.sprite.Sprite):
    """ This class represents the sprite that the player
    controls. """
 
 
    # -- Methods
    def __init__(self, sprite):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # -- Attributes
        # Set speed vector of player
        self.r_jump = 0
        self.l_jump = 0
        self.change_x = 0
        self.change_y = 0
        # set the image for the player
        self.sprite_sheet = sprite
        self.walking_frames_r = images.right_walk(self.sprite_sheet)
        self.walking_frames_l = images.left_walk(self.sprite_sheet)
        # What direction is the player facing?
        self.direction = "R"
        self.score = 0

        # List of sprites we can bump against
        level = None
                
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()



    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame].convert_alpha()
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame].convert_alpha()
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left

            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top

            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
            #if isinstance(block, MovingPlatform):
             #   self.rect.x += block.change_x

        coin_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, True)
        for coin in coin_hit_list:
            self.score += 25


 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = self.rect.height



    def jump(self):
        """ Called when user hits 'jump' button. """
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        self.rect.x += 2
        platform_side_hit_list_r = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.x -= 2
        self.rect.x -= 2
        platform_side_hit_list_l = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.x += 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10
            self.r_jump = 0
            self.l_jump = 0

        # wall jump
        if len(platform_side_hit_list_r) > 0 and self.r_jump == 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:

            self.change_y = -10
            self.r_jump += 1
            self.l_jump = 0


        if len(platform_side_hit_list_l) > 0 and self.l_jump == 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:

            self.change_y = -10
            self.l_jump += 1
            self.r_jump = 0


    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = "L"
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def shoot_laser(self):
        pass

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, direction):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.direction = direction
        self.image = pygame.Surface([10, 4])
        self.image.fill(constants.BLACK)
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """  
        if self.direction == 'L':
            self.rect.x -= 6  
        elif self.direction == 'R':
            self.rect.x += 6

class game():

    def main():


        """ Main Program """
        pygame.init()


        # Set the height and width of the screen
        size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Side-scrolling Platformer")


        # Create the player
        player = Player(SpriteSheet('sprite_base_addon_2012_12_14.png'))
        
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
                    elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        player.jump()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    elif event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Fire a bullet if the user clicks the mouse button
                    bullet = Bullet(player.direction)
                    # Set the bullet so it is where the player is
                    bullet.rect.x = player.rect.x + 10
                    bullet.rect.y = player.rect.y + 10
            
                    # Add the bullet to the lists
                    active_sprite_list.add(bullet)
                    bullet_list.add(bullet)

            # Update the player.
            active_sprite_list.update()
            # Update items in the level
            current_level.update()

            # Calculate mechanics for each bullet
            for bullet in bullet_list:
        
                # See if it hit a block
                block_hit_list = pygame.sprite.spritecollide(bullet, player.level.platform_list, False)
        
                # For each block hit, remove the bullet and add to the score
                for block in block_hit_list:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                    player.score += 1
                    print(player.score)

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

            # IF the player falls, game done
            if player.rect.y > constants.SCREEN_HEIGHT:
                done = True

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
            font = pygame.font.SysFont(None, 25)
            text = font.render(f"Score: {player.score}", True, constants.BLACK)
            screen.blit(text, (10, 10))

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
