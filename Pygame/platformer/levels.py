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
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for collectable in self.collectable_list:
            collectable.rect.x += shift_x

        for scenery in self.platform_scene:
            scenery.rect.x += shift_x
    
    def add_item(tiles, image, objectList, objType):
        # Go through the array above and add platforms
        for tile in tiles:                                  # tiles is a dictionary containing {image: object}
            obj = objType(tile[0], tile[1])                 # objectType(width, height)
            obj.rect.x, obj.rect.y  = tile[2], tile[3]      # objectType.x, objType.y
            obj.image = image                               # object image
            objectList.add(obj)                             # add object to objectList
    
    def add_enemy(cronies, objectList):
        # Go through the array above and add platforms
        for crony in cronies:                          
            obj = Enemy(crony[0],crony[1],crony[2],crony[3], crony[4])  
            objectList.add(obj)  


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """
        
        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -2000

# cronies list....[startX, Y, width, height, endX]
#####################################################################################
        cronies = [
            [305, 475, 20, 20, 600],
            [750, 375, 20, 20, 1075],
            [1310, 475, 20, 20, 1650]]
######################################################################################

# Array with width, height, x, and y of platforms. Tile Dictionary values
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

            [210, 70, 2700, 575]

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

                        [210, 70, 2825, 575],
                        [210, 70, 2950, 575],


                      ]


        right_tiles = [[210, 70, 550, 500],

                       [210, 70, 2300, 350]
                        ]
        # Wall at start of level
        end_tile_1 = [
                     [210, 70, -125, 560],
                     [210, 70, -125, 320],
                     [210, 70, -125, 80],

                     [210, 80, 1500, 255]

                      ]
        # Wall at start of level continued
        end_tile_2 =  [
                    [210, 70, -125, 440],
                    [210, 70, -125, 200],
                    [210, 70, -125, 0],

                    [210, 80, 1300, 200],
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

