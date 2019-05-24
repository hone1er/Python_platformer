from characters import Enemy, MovingPlatform
import constants
import pygame


# Set the height and width of the screen
size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Side-scrolling Platformer")
class Mushroom(pygame.sprite.Sprite):
    """ Item player can collect """

    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('png/Object/Mushroom_1.png')
        self.rect = self.image.get_rect()


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height, z=1, explodable=True):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('png/Tiles/14.png')
        self.rect = self.image.get_rect()
        self.explodable = bool


class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.wall_list = pygame.sprite.Group()
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
        self.player.bullet_list.update()
        self.wall_list.update()
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
        self.wall_list.draw(screen)
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
            self.wall_list,
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
            self.wall_list,
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

    def add_movingPlatform(tiles, objectList):
        # Go through the array above and add platforms
        obj = MovingPlatform(width=tiles[0],height=tiles[1],xstart=tiles[2],xend=tiles[3],xvel=tiles[4],ystart=tiles[6],yend=tiles[5],yvel=tiles[7])                 # objectType(width, height)
        objectList.add(obj) 




class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -4000

        # Array with type of platform, and x, y location of the platform.
        center_tiles = [
            [125, 70, 0, 500],
            [125, 70, 125, 500],

            [125, 70, 350, 500],
            [125, 70, 475, 500],

            [125, 70, 325, 150],
            [125, 70, 450, 150],


            [125, 70, 775, 500],
            [125, 70, 900, 500]
        ]

        # Moving Platforms
#####################################################################################
###  [ width, height, X, X end, X velocity, Y, Y end, Y velocity]
        movingplatform = [
            [125, 70, 625, 625, 0, 500, 200, 3],
            [125, 70, 650, 1050, 3, 50, 50, 3]
            
            ]

        # Wall at start of level
        end_tile_1 = [
                     [125, 70, -125, 675],
                     [125, 70, -125, 565],
                     [125, 70, -125, 315],
                     [125, 70, -125, 85],
                     [125, 70, -125, -104],
                     [125, 70, -125, -300],
                     ]

        # Wall at start of level continued
        end_tile_2 =  [
                    [125, 70, -125, 440],
                    [125, 70, -125, 200],
                    [125, 70, -125, 0],
                    [125, 70, -125, -200],
                    ]
        
        ground_tiles = [[125,30,x*125,575] for x in range(abs(self.level_limit//45))]
        floor_tile = [[125, 70, x*125, 625] for x in range(len(ground_tiles))]


        mushroom_1 = [[125, 70, 25, 465],
                      [64, 64, 375, 115]
                      
                    ]
        mushroom_2 = [[0, 0, 625, 540]
                      ]

        #### wall at start of levels and ground tiles
        wall_dict = {
                pygame.image.load('png/Tiles/10.png'): end_tile_1,
                pygame.image.load('png/Tiles/8.png'): end_tile_2,
                pygame.image.load('png/Tiles/8.png'): floor_tile,
                pygame.image.load('png/Tiles/14.png'): ground_tiles,
                }

        platforms_dict = {
                pygame.image.load('png/Tiles/14.png'): center_tiles
                }

        collectable_dict = {pygame.image.load('png/Object/Mushroom_1.png'): mushroom_1,
                       pygame.image.load('png/Object/Mushroom_2.png'): mushroom_2,}
        
        for wall in wall_dict:
            Level.add_item(wall_dict[wall], wall, self.wall_list, Platform)

        for platform in platforms_dict:
            Level.add_item(platforms_dict[platform], platform, self.platform_list, Platform)
            
        for platform in movingplatform:
            Level.add_movingPlatform(platform, self.platform_list)
                # Add collectables
        for collectable in collectable_dict:
            Level.add_item(collectable_dict[collectable], collectable, self.collectable_list, Mushroom)

            


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """
        
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
        ground_tiles = [[125, 70, 105, 560],

                        [125, 70, 0, 560],

                        [125, 70, 995, 560]
                        ]

        left_tiles = [
            [125, 70, 300, 500],

            [125, 70, 740, 400],

            [125, 70, 1300, 500],

            [125, 70, 1925, 350],

            [125, 70, 2700, 565],

            [125, 70, 4500, 550]

                 ]
        center_tiles = [[125, 70, 425, 500],

                        [125, 70, 985, 400],
                        [125, 70, 865, 400],



                        #platform with collectable
                        [125, 80, 1500, 290],
                        [125, 70, 1500, 195],

                        [125, 80, 1300, 235],
                        [125, 70, 1300, 140],


                        [125, 70, 1425, 500],
                        [125, 70, 1550, 500],

                        [125, 70, 2050, 350],
                        [125, 70, 2175, 350],

                        [125, 70, 1995, 620],
                        [125, 70, 2100, 620],
                        [125, 70, 2225, 620],

                        [125, 70, 2825, 565],
                        [125, 70, 2950, 565],

                        [125, 70, 4500, 550],
                        [125, 70, 4625, 550],
                        [125, 70, 4750, 550],
                        

                      ]


        right_tiles = [[125, 70, 550, 500],

                       [125, 70, 2300, 350],
                       [125, 70, 2350, 620],
                       [125, 70, 3075, 565]
                        ]
        # Wall at start of level
        end_tile_1 = [
                     [125, 70, -125, 560],
                     [125, 70, -125, 320],
                     [125, 70, -125, 80],

                     [125, 80, 1500, 255],

                     [125, 70, 1930, 510],
                     [125, 70, 1930, 390],

                      ]
        # Wall at start of level continued
        end_tile_2 =  [
                    [125, 70, -125, 440],
                    [125, 70, -125, 200],
                    [125, 70, -125, 0],

                    [125, 80, 1300, 200],

                    [125, 70, 1930, 630],
                    [125, 70, 1930, 350]
                        ]
# Collectable/scenery dictionary values
###################################################################################
        tree_1 = [[125, 70, 30, 259],

                  [125, 70, 850, 100]
                  ]

        sign = [[125, 70, 400, 436]
                ]

        mushroom_1 = [[125, 70, 0, 525],
                      [0, 0, 1510, 160]
                    ]
        mushroom_2 = [[0, 0, 1050, 520]
                      ]

# Moving Platforms
#####################################################################################
###  [ width, height, X, X end, X velocity, Y, Y end, Y velocity]
        movingplatform = [
            [125, 70, 3400, 3400, 0, 500, 200, 3],
            [125, 70, 3600, 4200, 3, 500, 500, 0],
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

        for platform in movingplatform:
            Level.add_movingPlatform(platform, self.platform_list)

        # add enemies
        Level.add_enemy(cronies, self.enemy_list)
# Create platforms for the level

