import pygame

pygame.init()

def left_walk(sprite_sheet):
    
    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    # Load all the right facing images, then flip them
    # to face left.
    a = 13
    for img in range(7):
        image = sprite_sheet.get_image(a,87,26,30)
        image = pygame.transform.flip(image, True, False)
        walking_frames_l.append(image)
        a += 64
    return walking_frames_l

def right_walk(sprite_sheet):
    walking_frames_r = []
    ##    # Load all the right facing images into a list
    a = 15
    for img in range(7):
        image = sprite_sheet.get_image(a,87,26,30)
        walking_frames_r.append(image)
        a += 64
    return walking_frames_r

def right_jump(sprite_sheet):

    jump_frames_r = []
    a = 15
    for img in range(7):
        image = sprite_sheet.get_image(a,155,28,32)
        jump_frames_r.append(image)
        a += 64
    return jump_frames_r
    pass

def attack(sprite_sheet):

    pass

def dead(sprite_sheet):
    pass


