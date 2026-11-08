import pygame

class Camera():
    def __init__(self, width_map, height_map, width_window, height_window):
        self.camera = pygame.Rect(0, 0, width_map, height_map)
        self.width = width_window
        self.height = height_window

        self.posmax_x = width_map - width_window # La position maximal de la camera
        self.posmax_y = height_map - height_window 

    def update(self, cible):
        # Calcul decalage pour centrer player
        x = -cible.rect.centerx + int(self.width / 2)# 0 --> -336
        y = -cible.rect.centery + int(self.height / 2)

        # Pour cacher  la partie hors map
        if x > 0 :
            x = 0
        elif x < -self.posmax_x :
           x = -self.posmax_x

        if y > 0 :
            y = 0
        elif y < -self.posmax_y :
            y = -self.posmax_y
        
        self.camera.topleft = (x, y)


    def apply(self, pos_x,pos_y):
        # decale la tuile ou l'entite du x, y calculé dans le update  9I
        newpos_x = pos_x + self.camera.topleft[0]
        newpos_y = pos_y + self.camera.topleft[1]
        return (newpos_x,newpos_y)

    def apply_rect(self, rect):
        # Cette fonction décale un rectangle simple (pour le debug)
        return rect.move(self.camera.topleft)