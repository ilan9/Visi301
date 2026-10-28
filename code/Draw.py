import pygame
import pytmx

class Draw():
    def __init__(self,window):
        self.window = window
        self.police = pygame.font.Font(None, 30) #Police par default taille 30

    def text_value(self,text,value,x,y,symbole="",color = (0,0,0)):
        string = text + str(value) + symbole
        info = self.police.render(string,True,color)
        self.window.blit(info,(x,y))

    def map(self,tmx_data,camera):
        for layer in tmx_data.visible_layers: #C'est les couches dans Tiled et on vérifie ils sont en mode visible
            if isinstance(layer,pytmx.TiledTileLayer): #On vérifie que c'est des layer et pas des objets
                for x,y,image in layer.tiles(): # On recup les coordonnées et les image de chaque tuile
                    pos_x = x*tmx_data.tilewidth 
                    # On multiplie leur position par leur largeur 
                    pos_y = y*tmx_data.tileheight
                    self.window.blit(image,camera.apply(pos_x,pos_y)) # On les affiche dans notre window

    def sprite(self,sprite,xy):
        self.window.blit(sprite,(xy))

    def group_sprite(self,group,camera):
        for sprite in group.sprites():
            self.window.blit(sprite.image,camera.apply(sprite.rect.x,sprite.rect.y))