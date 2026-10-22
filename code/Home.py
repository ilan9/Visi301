import pygame

class Home(pygame.sprite.Sprite): # Elle doit hérite de sprite.Sprite car on veut les mettre dans un groupe
    def __init__(self,rect:pygame.rect):
        super().__init__()
        self.life = 100
        self.life_max = 100 # en fonction du level de la maison ??
        self.level = 0
        self.rect : pygame.rect = rect

    def hurt(self,damage): #Pour que la maison perde des PV
        self.life -= damage
        if self.life <= 0 :
            print("Défaite la maison n'as plus de vie !!")


    def healing(self,heal): # Pour que la maison gagne des PV
        if self.life > 0:
            self.life += heal
            self.life = min(self.life,self.life_max) # max de vie a max_life



class Wall_destructible(pygame.sprite.Sprite): # Elle doit hérite de sprite.Sprite car on veut les mettre dans un groupe
    def __init__(self, rect, layer_obj, tmx_data, group_wall:pygame.sprite.Group, group_rampart:pygame.sprite.Group):
        super().__init__()
        self.rect = rect
        self.life_max = 100
        self.life = self.life_max 
        # Ajouter le level et fdaire varier vie max

        #Pour faire disparaitre l'image associé
        self.active = True
        self.name = layer_obj.name
        self.tmx_data = tmx_data
        self.group_wall = group_wall
        self.group_rampart = group_rampart
        self.layer = layer_obj

        for layer in self.tmx_data.layers:
            if layer.name == self.name:
                self.layer_carte = layer

    def hurt(self,damage): 
            self.life -= damage
            if self.life <= 0 :
                self.dead()
            else:
                self.life -=1
    
    def healing(self,heal):
        if self.life > 0:
            self.life += heal
            self.life = min(self.life,self.life_max) # max de vie a max_life

    def dead(self):
        self.group_wall.remove(self) # Enlever du groupe qui gere les collision de passage
        self.group_rampart.remove(self) # Enlever du groupe qui gère les attaques
        self.layer_carte.visible = False
    
    def resurrect(self): # Ajouter un boutton ? un menu ? une case ? 
        self.group_wall.add(self) # Ajouter au groupe qui gere les collision de passage
        self.group_rampart.add(self) # Ajouter au groupe qui gere les attaques
        self.life = self.life_max
        for layer in self.tmx_data.layers:
            if layer.name == self.name:
                layer.visible = True
        # Non testé



class Wall(pygame.sprite.Sprite): # Elle doit hérite de sprite.Sprite car on veut les mettre dans un groupe
    def __init__(self, rect):
        super().__init__()
        self.rect = rect



