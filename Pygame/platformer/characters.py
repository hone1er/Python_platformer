from sheet_helper import SpriteSheet
import pygame
import constants
import images


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

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            if self.score > 25:
                self.score -= 25
            else:
                self.score = 0

        coin_hit_list = pygame.sprite.spritecollide(self, self.level.collectable_list, True)
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

############################################
# Class to respresent the bullet/projectile#
############################################
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

###########################################
######Class to respresent the enemies######
###########################################
class Enemy(pygame.sprite.Sprite):
    """ This class represents the enemy . """
    def __init__(self, x, y, width, height, end):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.width = width
        self.height = height
        self.end = end
        self.vel = 2
        self.walkCount = 0
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.path = [self.rect.x, self.end]
        
 
    def draw(self,win):
        """ move the enemy """  
        self.move()
    
    def move(self):
        if self.vel > 0:
            if self.rect.x + self.vel < self.path[1]:
                self.rect.x += self.vel
            else:
                self.vel *= -1
        else:
            if self.rect.x - self.vel > self.path[0]:
                self.rect.x += self.vel
                self.walkCount = 0
            else:
                self.vel *= -1
