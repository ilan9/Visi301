import pygame

class Ressources():
    def __init__(self):
        #self.rect : pygame.rect = rect # si il n'y a pas de collision on a pas besoin d'un rect
        self.quantity = 500

    def increases (self,quantity): #il faut le faire ici si on veut que les fichier monstre puisse augmenter les ressources
        self.quantity += quantity  # ou plus tard le bois et la pierre

    def reduce (self,quantity):
        self.quantity -= quantity
    