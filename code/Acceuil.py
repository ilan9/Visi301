import pygame
from Menu import Button



class Acceuil ():
    def __init__(self,window):
        self.window = window
        self.acceuil = True

        image = pygame.image.load("asset/acceuil.jpg").convert_alpha()
        self.image = pygame.transform.scale(image, (1100, 600))

        self.play = Button(1,450,250,200,60,"JOUER",lambda : self.jouer())
        self.quit = Button(2,450,340,200,60,"QUITTER",lambda : self.quitter())

        self.background_color = (230, 240, 255, 100)
        self.text_color = (15, 20, 40)
        self.Hbackground_color = (10, 15, 30, 150)
        self.Htext_color = (200, 240, 255)

    def run(self):
        #Afficher l'image    
        self.window.blit(self.image,(0,0))
        while self.acceuil:
            #Couleur des bouttons
            play_background = self.background_color
            play_text = self.text_color
            quit_background = self.background_color
            quit_text = self.text_color

            #Detecter le clic
            for event in pygame.event.get(): #Ecouter les évenements "uniques"
                if event.type == pygame.QUIT:
                    pygame.quit() # fermer la window pygame
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #clic gauche
                    if self.play.rect.collidepoint(event.pos):
                        self.play.action()
                    elif self.quit.rect.collidepoint(event.pos):
                        self.quit.action()
            #survol
            pos_souris = pygame.mouse.get_pos()

            if self.play.rect.collidepoint(pos_souris):
                play_background = self.Hbackground_color
                play_text = self.Htext_color
            elif self.quit.rect.collidepoint(pos_souris):
                quit_background = self.Hbackground_color
                quit_text = self.Htext_color

            #button
            calque = pygame.Surface(self.window.get_size(), pygame.SRCALPHA) #Pour pouvoir gérer le parametre alpha
            self.play.draw(calque,background=play_background,color_text=play_text)
            self.quit.draw(calque,background=quit_background,color_text=quit_text)
            self.window.blit(calque, (0, 0))

            pygame.display.flip()

    def jouer(self):
        self.acceuil = False

    def quitter(self):
        self.acceuil = False
        pygame.quit()