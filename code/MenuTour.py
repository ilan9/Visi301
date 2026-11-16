import pygame
from Menu import Button
from Acceuil import Acceuil
from Outils import draw_text_bg,draw_money

class MenuTour(Acceuil):
    def __init__(self, window,piece,name):
        super().__init__(window)

        self.window = window
        self.piece = piece
        self.name = name

        image = pygame.image.load("asset/Menu_select_tower.jpg").convert_alpha()
        self.image = pygame.transform.scale(image, (400, 300))

        self.t1 = ButtonChoice(1,"asset/turret_1.png")
        self.t2 = ButtonChoice(2,"asset/turret_2.png")
        self.level = 0

        self.selected = 1
        self.choix = self.t1
        self.carre = pygame.Rect(325,275,150,150)
        


    def changeButton(self):
        if self.selected == 1:
            self.selected = 2
            if self.level == 0:
                self.choix = self.t2
            self.carre.x = 521
        else:
            self.selected = 1
            if self.level == 0:
                self.choix = self.t1
            self.carre.x = 326
        self.window.blit(self.image,(300,200))




    def run(self):
        #Afficher l'image    
        self.menu = True
        while self.menu:
            self.window.blit(self.image,(300,200))
            draw_money(self.window,self.piece.quantity)
            draw_text_bg(self.window,(0,0,0),pygame.Rect(0,0,0,0),str(self.name),430,472)
            for event in pygame.event.get(): #Ecouter les évenements "uniques"
                if event.type == pygame.QUIT:
                    pygame.quit() # fermer la window pygame
                elif event.type == pygame.KEYDOWN: # Detecter TOUTES les touches pressées
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.changeButton()
                    elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                        self.menu = False
                    elif event.key == pygame.K_RETURN :#RETURN=ENTER   l'utilisateur fait un choix ici
                        if self.level == 0 and self.piece.quantity >= self.choix.cost[self.level]:
                            self.piece.reduce(self.choix.cost[self.level])#Payer
                            self.level+=1

                            #cree le canon ici avec self.selected ou self.choix
                            print("Le joueur a achete le canon de type :"+str(self.selected))
                        elif self.level <4:
                            if self.selected ==1:
                                self.piece.increases(self.choix.sell[self.level-1])# Rembourse en parti
                                self.level = 0
                                #Supprimer le canon
                                
                            elif self.piece.quantity >= self.choix.cost[self.level]:
                                self.piece.reduce(self.choix.cost[self.level])#Payer
                                self.level+=1

                        elif self.selected ==1:
                            self.piece.increases(self.choix.sell[self.level-1])# Rembourse en parti
                            self.level = 0
                            #Supprimer le canon
                            

            #dessin button
            if self.level == 0:
                self.window.blit(self.t1.image,(350,300))
                self.window.blit(self.t2.image,(546,300))
                if self.selected ==1:
                    draw_text_bg(self.window,(220, 38, 38),pygame.Rect(375,220,55,20),"-"+str(self.t1.cost[self.level])+"$",375,220)
                else:
                    draw_text_bg(self.window,(220, 38, 38),pygame.Rect(570,220,55,20),"-"+str(self.t2.cost[self.level])+"$",570,220)

            elif self.level <4:
                self.window.blit(self.choix.image,(350,300))
                self.window.blit(self.choix.image,(546,300))
                draw_text_bg(self.window,(255,10,10),pygame.Rect(350,350,100,20),"VENDRE"+str(self.level),360,350)

                if self.selected == 1:
                    draw_text_bg(self.window,(10, 250, 10),pygame.Rect(375,220,55,20),"+"+str(self.t2.sell[self.level-1])+"$",375,220)
                else :
                    draw_text_bg(self.window,(220, 38, 38),pygame.Rect(570,220,55,20),"-"+str(self.t1.cost[self.level])+"$",570,220)

            else:
                self.window.blit(self.choix.image,(350,300))
                draw_text_bg(self.window,(10, 250, 10),pygame.Rect(375,220,55,20),"+"+str(self.t2.sell[self.level-1])+"$",375,220)







            pygame.draw.rect(self.window,(255, 204, 0),self.carre,6) #séléctionner

            pygame.display.flip()

class ButtonChoice():
    def __init__(self,id,image):

        self.id = id
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.cost = [100,50,80,150] #Prix pour poser une tour et l'améliorer
        self.sell = [50,125,165,240]