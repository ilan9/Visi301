import pygame
from ActionMenu import Action

def upgrade_wall(direction): # Autre fichiers
    print("ameliorer le mur"+direction)

class Menu ():
    def __init__(self,window,pieces,group_rampart,player,home):

        self.window = window
        self.nbr_column = 4
        self.nbr_buttons = 0
        self.buttons_size = {"width":120,
                             "height":80,
                             "external_margin":10,
                             "internal_margin":8}
        # Centrer le menu
        self.startx = self.window.get_width()//2 - 2* (self.buttons_size["width"]+self.buttons_size["internal_margin"]) + self.buttons_size["external_margin"]
        self.starty = self.window.get_height()//2 - 2* (self.buttons_size["height"]+self.buttons_size["internal_margin"]) + self.buttons_size["external_margin"]
        self.width = self.buttons_size["width"]*4 + self.buttons_size["internal_margin"]*3 + self.buttons_size["external_margin"]*2
        self.height = self.buttons_size["height"]*4 + self.buttons_size["internal_margin"]*3 + self.buttons_size["external_margin"]*2 

        self.rampart = {}
        for rampart in group_rampart:
            self.rampart[rampart.name] = rampart

        self.home = home
        self.action = Action(window,pieces,group_rampart,player,home)
        
        self.list_buttons = self.create_buttons()


    def create_buttons(self): # Creer les bouttons aux bonnes coordonnées
        list_buttons = []
        buttons_to_create = [
            {"text": "Soigner la maison\n +10 PV", "action": lambda: self.action.healing_home()}, # lambda => permet de stocker des fonction et non leur resultats
            {"text": "Ameliorer mur\nNord: -50$\n"+str(self.rampart["Mur Nord"].life)+"/"+str(self.rampart["Mur Nord"].life_max), "action": lambda : self.action.upgrade_rampart(self.rampart["Mur Nord"])},
            {"text": "Ameliorer mur\nOuest: -50$\n"+str(self.rampart["Mur Ouest"].life)+"/"+str(self.rampart["Mur Ouest"].life_max), "action": lambda : self.action.upgrade_rampart(self.rampart["Mur Ouest"])},
            {"text": "Ameliorer mur\nEst: -50$\n"+str(self.rampart["Mur Est"].life)+"/"+str(self.rampart["Mur Est"].life_max), "action": lambda : self.action.upgrade_rampart(self.rampart["Mur Est"])},
            {"text": "Ameliorer mur\nSud: -50$\n"+str(self.rampart["Mur Sud"].life)+"/"+str(self.rampart["Mur Sud"].life_max), "action": lambda : self.action.upgrade_rampart(self.rampart["Mur Sud"])},
            #Text dynamique plus bas


            
        ] #A remplir à la main

        width,height = self.buttons_size["width"],self.buttons_size["height"]
        external_margin,internal_margin = self.buttons_size["external_margin"],self.buttons_size["internal_margin"]
        x,y = self.startx,self.starty
        cpt = 1

        for btn in buttons_to_create:
            button = Button(cpt,x,y,width,height,btn["text"],btn["action"])
            list_buttons.append(button)
            x += width + internal_margin
            if cpt % self.nbr_column == 0: # Pour gérer le nombre de boutons par ligne
                y += height + internal_margin
                x = self.startx
            cpt +=1
        return list_buttons

    def open_menu(self):
        print("menu ouvert")
        open = True
        while open :
            pos_souris = 0,0
            for event in pygame.event.get(): #Ecouter les évenements "uniques"
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_e): 
                    open = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #clic gauche
                    pos_souris = event.pos #  position de la souris => (x,y)
                    # Ajouter le survol de la souris

            #dessiner les bouttons et voir si il sont cliquer
            pygame.draw.rect(self.window, (215, 205, 185), [self.startx-self.buttons_size["external_margin"], self.starty-self.buttons_size["external_margin"], self.width,self.height])
            for btn in self.list_buttons:
                if btn.id == 1:
                    btn.change_text("Soigner la maison\n"+str(self.home.life)+"/"+str(self.home.life_max)+" + 10 PV") #Text dynamique
                elif btn.id == 2:
                    btn.change_text("Ameliorer mur\nNord: -50R\n"+str(self.rampart["Mur Nord"].life)+"/"+str(self.rampart["Mur Nord"].life_max))
                elif btn.id == 3:
                    btn.change_text("Ameliorer mur\nOuest: -50R\n"+str(self.rampart["Mur Ouest"].life)+"/"+str(self.rampart["Mur Ouest"].life_max))
                elif btn.id == 4:
                    btn.change_text("Ameliorer mur\nEst: -50R\n"+str(self.rampart["Mur Est"].life)+"/"+str(self.rampart["Mur Est"].life_max))
                elif btn.id == 5:
                    btn.change_text("Ameliorer mur\nSud: -50R\n"+str(self.rampart["Mur Sud"].life)+"/"+str(self.rampart["Mur Sud"].life_max))
                btn.draw(self.window)
                if btn.rect.collidepoint(pos_souris):
                    btn.action()
            pygame.display.flip()
        print("menu fermé")
                    


class Button ():
    def __init__(self,id,x,y,width,height,text,action):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.action = action
        self.id = id

    def draw(self,window,background = (70, 45, 30),color_text = (245, 240, 225)):
        police = pygame.font.Font(None, 20)
        pygame.draw.rect(window,background, self.rect)

        lignes = self.text.split("\n")
        hauteur_l = police.get_linesize()

        y = self.rect.centery - (len(lignes)*hauteur_l)//2 + hauteur_l//2
        for i, ligne in enumerate(lignes):
            text = police.render(ligne, True, color_text)
            y += i * hauteur_l
            texte_rect = text.get_rect(center=(self.rect.centerx,y)) #dessiner au centre
            window.blit(text, texte_rect)

    def change_text(self,text):
        self.text = text