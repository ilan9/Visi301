import pygame

def upgrade_wall(direction): # Autre fichiers
    print("ameliorer le mur"+direction)

class Menu ():
    def __init__(self,window):

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
        self.list_buttons = self.create_buttons()
        


    def create_buttons(self): # Creer les bouttons aux bonnes coordonnées
        list_buttons = []
        buttons_to_create = [
            {"text": "Ameliorer mur Est", "action": lambda: upgrade_wall("Est")}, # lambda => permet de stocker des fonction et non leur resultats
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")},
            {"text": "Ameliorer mur\nNord", "action": lambda : upgrade_wall("Nord")}

            
        ] #A remplir à la main

        width,height = self.buttons_size["width"],self.buttons_size["height"]
        external_margin,internal_margin = self.buttons_size["external_margin"],self.buttons_size["internal_margin"]
        x,y = self.startx,self.starty
        cpt = 1

        for btn in buttons_to_create:
            print((x,y))
            button = Button(x,y,width,height,btn["text"],btn["action"])
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
                btn.draw(self.window)
                if btn.rect.collidepoint(pos_souris):
                    btn.action()
            pygame.display.flip()
        print("menu fermé")
                    


class Button ():
    def __init__(self,x,y,width,height,text,action):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.action = action

    def draw(self,window):
        police = pygame.font.Font(None, 20)
        pygame.draw.rect(window,(70, 45, 30), self.rect)

        lignes = self.text.split("\n")
        hauteur_l = police.get_linesize()

        y = self.rect.centery - (len(lignes)*hauteur_l)//2 + hauteur_l//2
        for i, ligne in enumerate(lignes):
            text = police.render(ligne, True, (245, 240, 225))
            y += i * hauteur_l
            texte_rect = text.get_rect(center=(self.rect.centerx,y)) #dessiner au centre
            window.blit(text, texte_rect)