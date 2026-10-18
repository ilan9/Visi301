import pygame

def decoup_image(chemin_image_animation, witdh,height,nbrimage_x, nbrimage_y, reverse = False, marge_x = 0, marge_y = 0, change_size = False, scale_x = 0, scale_y=0):
    witdh_img = (witdh-(marge_x*nbrimage_x) )// nbrimage_x
    height_img = (height-(marge_y*nbrimage_y)) // nbrimage_y
    images = pygame.image.load(chemin_image_animation)
    animation = []
    for nbimgy in range(nbrimage_y):
        for nbimgx in range (nbrimage_x):
            x = (witdh_img+marge_x) * nbimgx
            y = (height_img+marge_y) * nbimgy
            img = images.subsurface((x, y, witdh_img, height_img))
            if reverse :
                img = pygame.transform.flip(img,True,False)
            if change_size:
                img = pygame.transform.scale(img,(scale_x,scale_y))
            animation.append(img)
    return animation