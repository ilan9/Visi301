import pygame
from Menu import Button
from Acceuil import Acceuil

class MenuTour(Acceuil):
    def __init__(self, window):
        super().__init__(window)

        self.window = window

        image = pygame.image.load("asset/Menu_select_tower.jpg").convert_alpha()
        self.image = pygame.transform.scale(image, (400, 300))

        self.t1 = ButtonChoice(1,"asset/turret_1.png")
        self.t2 = ButtonChoice(2,"asset/turret_2.png")

        self.selected = 1
        self.carre = pygame.Rect(350,294,120,120)
        


    def changeButton(self):
        if self.selected == 1:
            self.selected = 2
            self.carre.x = 540
        else:
            self.selected = 1
            self.carre.x = 360
        self.window.blit(self.image,(300,200))




    def run(self):
            #Afficher l'image    
            self.window.blit(self.image,(300,200))
            self.menu = True
            while self.menu:
                for event in pygame.event.get(): #Ecouter les évenements "uniques"
                    if event.type == pygame.QUIT:
                        pygame.quit() # fermer la window pygame
                    elif event.type == pygame.KEYDOWN: # Detecter TOUTES les touches pressées
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.changeButton()
                        elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                            self.menu = False
    
                #button

                self.window.blit(self.t1.image,(355,294))
                self.window.blit(self.t2.image,(545,294))
                pygame.draw.rect(self.window,(255, 204, 0),self.carre,6) #séléctionner
    
                pygame.display.flip()


class ButtonChoice():
    def __init__(self,id,image):

        self.id = id
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))