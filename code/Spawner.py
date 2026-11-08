import pygame
import random
from Monster import Monster

def monster_spawner(group_monstre, map_with, map_height,list_wall,home,group_rampart, ressources): #ressource pour que le monstre puisse les drop
    x,y = random_spawn(map_with,map_height)

    monster = Monster(x,y,list_wall,home,group_rampart, ressources) # Creer 1 monstre
    group_monstre.add(monster) # L'ajoute au groupe

def random_spawn(max_with,max_height):
    # Randomiser le spawn mais pas dans la base
    x,y = 500,700
    while x>430 and x<1382 and y>600  and y<1470 :
        x = random.randint(0,max_with)
        y = random.randint(0,max_height)

    return x,y