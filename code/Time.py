# Gérer le temps, les phases...

import pygame

class Time:
    def __init__(self):
        self.time_start = pygame.time.get_ticks() # Recupérer l'time
        self.time = pygame.time.get_ticks() - self.time_start # Avec ce calcul on obtient le temps pendant lequel le jeu à été lancer
        self.time_phase = 30 * 1000 # Le temps d'une phase ??
        self.opacity = 80 # 0 pour le day et 150 pour la nuit
        # Pour gérer l'opacity en fonction de l'time 0 a midi mais plus sombre la nuit...

        self.phase = 1
        self.day = self.phase % 2 == 1  # day = True si phase impair sinon nuit
        self.day_phase = "Jour" #Chaine de caractère day ou nuit
        self.inv = -1 #temoin pour le calcul de opacity
        self.tem = True
        self.time_change = 1000


    def change_phase(self):
        self.phase +=1
        self.day = self.phase % 2 == 1 
        if self.day:
            self.day_phase = "Jour"
            #self.inv = self.inv*-1
        else:
            self.day_phase = "Nuit"
        
        self.tem = True
        print("laaaaaaaaaaaaaaaaa")
        print(self.tem)
        

    def update(self):
        self.time = pygame.time.get_ticks() - self.time_start
        if self.time//1000 > 15 and self.tem :
            self.tem = False
            self.inv = self.inv*-1
        if self.time > self.time_phase:
            self.change_phase()
            self.time_start = pygame.time.get_ticks()
        
        self.timer()

    def timer(self):
        if pygame.time.get_ticks() - self.time_change > 1000 :
            self.opacity += 5 * self.inv
            self.time_change = pygame.time.get_ticks()
            #print(self.opacity,self.time//1000,self.inv,self.tem)



    """
    EXPLICATION : 
    Le jour l'opacité du layer part de 75, descend jusqu'à 0 au milieu de la journée et remonte jusqu'à 75 en fin de journée
    La nuit l'opacité part de 75, monte jusqu'à 150 au milieu de la nuit et redescend jusqu'à 75 en fin de nuit
    Avec un cycle jour de 30 sec
    
    """
    # A faire messsage NUITTT !!!!