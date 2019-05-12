import pygame
import constants
from characters import Enemy


 

class Mushroom(pygame.sprite.Sprite):
    """ Item player can collect """

    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('png/Object/Mushroom_1.png')
        self.rect = self.image.get_rect()


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('png/Tiles/14.png')
        self.rect = self.image.get_rect()

class MovingPlatform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height, xend=0, xvel=0, yend=0, yvel=0):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('png/Tiles/14.png')
        self.rect = self.image.get_rect()
        # attributes to move platform
        self.xend = xend
        self.yend = yend
        self.xvel = xvel
        self.yvel = yvel
        self.moveCount = 0
        self.xpath = [self.rect.x, self.xend]
        self.ypath = [self.rect.y, self.yend]


    def draw(self, win):
        self.move()

    def move(self):
        if self.xvel > 0:
            if self.rect.x + self.xvel < self.xpath[1]:
                self.rect.x += self.xvel
            else:
                self.xvel *= -1
        else:
            if self.rect.x - self.xvel > self.xpath[0]:
                self.rect.x += self.xvel
            else:
                self.xvel *= -1

        if self.yvel > 0:
            if self.rect.y + self.yvel < self.ypath[1]:
                self.rect.y += self.yvel
            else:
                self.yvel *= -1
        else:
            if self.rect.y - self.yvel > self.ypath[0]:
                self.rect.y += self.yvel
            else:
                self.yvel *= -1


class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.platform_scene = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.collectable_list = pygame.sprite.Group()
        self.player = player
    

        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.world_shift_y = 0

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.platform_scene.update()
        self.enemy_list.update()
        self.collectable_list.update()


    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(constants.BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.platform_scene.draw(screen)
        self.collectable_list.draw(screen)



    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """


        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        objects = [
            self.platform_list,
            self.collectable_list,
            self.platform_scene,
            self.player.bullet_list,
            ]
        # Go through all the sprite lists and shift
        for obj in objects:
            for item in obj:
                item.rect.x += shift_x
                if isinstance(item, MovingPlatform):
                    item.xend += shift_x
                    item.xpath[0] += shift_x
                    item.xpath[1] += shift_x

 
        for enemy in self.enemy_list:
            enemy.end += shift_x
            enemy.rect.x += shift_x
            enemy.path[0] += shift_x
            enemy.path[1] += shift_x
        
    
    def shift_world_y(self, shift_y):
        
        # Keep track of the shift amount
        self.world_shift_y += shift_y
        # all of the object list that need to be shifted
        objects = [
            self.platform_list,
            self.collectable_list,
            self.enemy_list,
            self.player.bullet_list,
            self.platform_scene,
            ]
        # Go through all the sprite lists and shift
        for obj in objects:
            for item in obj:
                item.rect.y -= shift_y
                if isinstance(item, MovingPlatform):
                    item.yend -= shift_y
                    item.ypath[0] -= shift_y
                    item.ypath[1] -= shift_y


    
    def add_item(tiles, image, objectList, objType):
        # Go through the array above and add platforms
        for tile in tiles:                                  # tiles is a dictionary containing {image: object}
            obj = objType(tile[0], tile[1])                 # objectType(width, height)
            obj.image = image                               # object image    
            obj.rect = obj.image.get_rect()       
            obj.rect.x, obj.rect.y  = tile[2], tile[3]      # objectType.x, objType.y
            objectList.add(obj)                             # add object to objectList
    
    def add_enemy(cronies, objectList):
        # Go through the array above and add platforms
        for crony in cronies: 
                     
            obj = Enemy(x=crony[0],y=crony[1],width=crony[2],height=crony[3],end=crony[4])  
            objectList.add(obj)

    def add_movingPlatform(tiles, image, objectList):
        # Go through the array above and add platforms
        for tile in tiles:                                  # tiles is a dictionary containing {image: object}
            obj = MovingPlatform(width=tile[0],height=tile[1],xend=tile[3],xvel=tile[4],yend=tile[5],yvel=tile[7])                 # objectType(width, height)
            obj.image = image
            obj.rect = obj.image.get_rect()                               # object image
            obj.rect.x, obj.rect.y  = tile[2], tile[6]      # objectType.x, objType.y
            objectList.add(obj) 



# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """
        
        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -4000

# cronies list....[startX, Y, width, height, endX]
#####################################################################################
        cronies = [
            [305, 475, 20, 20, 600],
            [750, 375, 20, 20, 1075],
            [1310, 475, 20, 20, 1650]]
######################################################################################

# Array with [width, height, x, y] of platforms. Tile Dictionary values
######################################################################################
        ground_tiles = [[210, 70, 105, 560],

                        [210, 70, 0, 560],

                        [210, 70, 985, 560]
                        ]

        left_tiles = [
            [210, 70, 300, 500],

            [210, 70, 740, 400],

            [210, 70, 1300, 500],

            [210, 70, 1925, 350],

            [210, 70, 2700, 565]

                 ]
        center_tiles = [[210, 70, 425, 500],

                        [210, 70, 985, 400],
                        [210, 70, 865, 400],



                        #platform with collectable
                        [210, 80, 1500, 290],
                        [210, 70, 1500, 195],

                        [210, 80, 1300, 235],
                        [210, 70, 1300, 140],


                        [210, 70, 1425, 500],
                        [210, 70, 1550, 500],

                        [210, 70, 2050, 350],
                        [210, 70, 2175, 350],

                        [210, 70, 1995, 620],
                        [210, 70, 2100, 620],
                        [210, 70, 2225, 620],

                        [210, 70, 2825, 565],
                        [210, 70, 2950, 565],


                      ]


        right_tiles = [[210, 70, 550, 500],

                       [210, 70, 2300, 350],
                       [210, 70, 2350, 620],
                       [210, 70, 3075, 565]
                        ]
        # Wall at start of level
        end_tile_1 = [
                     [210, 70, -125, 560],
                     [210, 70, -125, 320],
                     [210, 70, -125, 80],

                     [210, 80, 1500, 255],

                     [210, 70, 1930, 510],
                     [210, 70, 1930, 390],

                      ]
        # Wall at start of level continued
        end_tile_2 =  [
                    [210, 70, -125, 440],
                    [210, 70, -125, 200],
                    [210, 70, -125, 0],

                    [210, 80, 1300, 200],

                    [210, 70, 1930, 630],
                    [210, 70, 1930, 350]
                        ]
# Collectable/scenery dictionary values
###################################################################################
        tree_1 = [[210, 70, 30, 259],

                  [210, 70, 850, 100]
                  ]

        sign = [[210, 70, 400, 436]
                ]

        mushroom_1 = [[210, 70, 0, 525],
                      [0, 0, 1510, 160]
                    ]
        mushroom_2 = [[0, 0, 1050, 520]
                      ]

# Moving Platforms
#####################################################################################
###  [ width, height, X, X end, X velocity, Y, Y end, Y velocity]
        movingplatform = [
            [210, 70, 500, 600, 2, 260, 260, 0],
            [210, 70, 3400, 3400, 0, 500, 200, 3]
            ]


# Dictionaries with images: objects
#####################################################################################
        tile_dict = {pygame.image.load('png/Tiles/1.png'): ground_tiles,
                     pygame.image.load('png/Tiles/13.png'): left_tiles,
                     pygame.image.load('png/Tiles/14.png'): center_tiles,
                     pygame.image.load('png/Tiles/15.png'): right_tiles,
                     pygame.image.load('png/Tiles/10.png'): end_tile_1,
                     pygame.image.load('png/Tiles/8.png'): end_tile_2
                     }

        object_dict = {pygame.image.load('png/Object/Tree_2.png'): tree_1,
                       pygame.image.load('png/Object/sign_2.png'): sign}

        collectable_dict = {pygame.image.load('png/Object/Mushroom_1.png'): mushroom_1,
                       pygame.image.load('png/Object/Mushroom_2.png'): mushroom_2,}

        moving_dict = {pygame.image.load('png/Tiles/14.png'): movingplatform}
        # got through tile_dict and add objects
        # Add platforms
        for tile in tile_dict:
            Level.add_item(tile_dict[tile], tile, self.platform_list, Platform)

        # Add backround objects such as trees, bushes, and rocks.
        for objects in object_dict:
            Level.add_item(object_dict[objects], objects, self.platform_scene, Platform)

        # Add collectables
        for collectable in collectable_dict:
            Level.add_item(collectable_dict[collectable], collectable, self.collectable_list, Mushroom)

        for tile in moving_dict:
            Level.add_movingPlatform(moving_dict[tile], tile, self.platform_list)


        # add enemies
        Level.add_enemy(cronies, self.enemy_list)
3
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000


        # Array with type of platform, and x, y location of the platform.
        left_tiles = [[210, 30, 0, 570],
                      [210, 30, 400, 420],
                      [210, 30, 1000, 520],
                      [210, 30, 1000, 280]
                        ]
        center_tiles = [[210, 30, 125, 570],
                        [210, 30, 300, 570],
                        [210, 30, 500, 750],
                      [210, 30, 650, 420],
                      [210, 30, 1064, 520],
                      [210, 30, 1184, 280]
                      ]


        Level.add_item(center_tiles,  pygame.image.load('png/Tiles/14.png'), self.platform_list, Platform)
        Level.add_item(left_tiles, pygame.image.load('png/Tiles/13.png'), self.platform_list, Platform)        