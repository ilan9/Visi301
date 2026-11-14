import pygame

class Action ():
    def __init__(self,window,ressources,group_rampart,player,home):
        self.window = window
        self.ressources = ressources
        self.group_rampart = group_rampart
        self.player = player
        self.home = home

    def healing_home(self):
        if self.ressources.quantity > 10:
            self.ressources.reduce(10)
            self.home.healing(10)
        else:
            print("plus de ressources")

    def upgrade_rampart(self,rampart):
        if self.ressources.quantity > 50:
            self.ressources.reduce(50)
            rampart.life_max += 50

    def upgrade_all_rampart(self,ramparts):
            if self.ressources.quantity > 140:
                self.ressources.reduce(140)
                for rampart in ramparts:
                    rampart.life_max += 10
                    rampart.life +=10
    

    def heal_rampart(self,rampart):
        if self.ressources.quantity > 10:
            self.ressources.reduce(10)
            rampart.healing(10)