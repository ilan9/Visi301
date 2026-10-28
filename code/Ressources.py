import pygame

class Ressources():
    def __init__(self):
        
        #self.rect : pygame.rect = rect # si il n'y a pas de collision on a pas besoin d'un rect
        self.quantity = 0

    def increases (self,quantity): #il faut le faire ici si on veut que les fichier monstre puisse augmenter les ressources
        self.quantity += quantity  # ou plus tard le bois et la pierre

    def reduce (self,quantity):
        self.quantity -= quantity


class Farm(pygame.sprite.Sprite):

    def __init__(self,rect,ressources):
        super().__init__()
        self.rect = rect
        self.ressources = ressources

    def increase_quantity(self,quantity):
        self.ressources.increases(quantity)

    def reduce_quantity(self,quantity):
        self.ressources.reduce(quantity)
