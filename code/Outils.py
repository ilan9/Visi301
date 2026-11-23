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


def draw_text_bg(window,color_bg,bg_rect:pygame.Rect,text,x,y,color_text=(255,255,255),bg=True):
    if bg:
        pygame.draw.rect(window,color_bg,bg_rect)
    info = pygame.font.Font(None, 30).render(text,True,color_text)
    window.blit(info,(x,y))

def draw_money(window,money):
    draw_text_bg(window,(38, 43, 52),pygame.Rect(1000,525,100,75),str(money)+"$",1015,553,(235, 242, 250))
    pygame.draw.rect(window,(130, 142, 160),pygame.Rect(1000,525,100,75),2)

def distance(tab, player_x, player_y):
    """Cette méthode permet de trouver l'élément le plus proche."""
    min_length = 99999999
    closest = None #Sécurité
    for element in tab:
        #on calcule la norme du vecteur.
        distance = ((element.x - player_x)**2 + (element.y - player_y)**2)**0.5
        if distance < min_length :
            min_length = distance
            closest = element
    return closest   