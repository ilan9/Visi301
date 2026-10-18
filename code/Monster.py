import pygame
from Outils import decoup_image

class Monster(pygame.sprite.Sprite) :
    def __init__(self,x,y,group_wall,home, group_rampart, ressources ):
        super().__init__()
        self.health = 10
        self.max_health = 10
        self.last_time_hit = 0 #la dernière fois que le monstre a attaqué pour la gestion des coups.
        self.velocity = 0.6
        self.damage = 1
        self.cooldown = 1000 #1s entre chaque coup 
        
        image = self.image = pygame.image.load('asset/zombie.png') #L'image de nos monstres
    
        #La taille du monstre :
        self.image_height = 64 * 1.5
        self.image_width = 384/6 * 1.5
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        
        #Son ID_BoX ///////////
        self.rect = self.image.get_rect()

        self.group_wall = group_wall
        self.home = home # l'objectif du monstre
        self.group_rampart = group_rampart
        self.ressources = ressources
        
        #La position de départ de notre monstre :
        self.rect.x = x
        self.rect.y = y
        self.motion_x,self.motion_y = self.motion_calcul()
        self.posfin_x = x # Pour le calcul du mouvement car rect ne peut stocker que des int 
        self.posfin_y = y


        #Animations
        reverse = self.motion_x > 0 # Pour l'orientation de l'image
        self.anim = {"walk":decoup_image("asset/zombie_animation/Zombie_Default_Walk.png",384,64,6,1,reverse),
                     "attack":decoup_image("asset/zombie_animation/Zombie_Default_Attack.png",384,64,6,1,reverse),
                     "hurt":decoup_image("asset/zombie_animation/Zombie_Default_Hurt.png",384,64,6,1, reverse),
                     "dead":decoup_image("asset/zombie_animation/Zombie_Default_Dead.png",384,64,6,1,reverse)
                     }

        self.anim_time = 0
        self.cooldown_anim = 1000/6
        self.anim_type = "walk"
        self.anmimation_in_progress = False
        self.anim_progress = 0
        self.image = self.anim[self.anim_type][self.anim_progress]


    def motion_calcul(self):# Calcul du mouvement du monstre 1 seul fois 
        posstart_x = self.rect.x
        posstart_y = self.rect.y
        posfin_x = self.home.rect.x
        posfin_y = self.home.rect.y

        distance_x = posfin_x - posstart_x
        distance_y = posfin_y - posstart_y
        distance_norm = (distance_x**2 + distance_y**2) ** 0.5 # pythagore
        return distance_x/distance_norm,distance_y/distance_norm




    def update(self):

        if self.anim_type != "hurt" and self.anim_type != "dead": #Si il subit des dégats ou si il meurt, il arrete momentanément de bouger
            last_posx = self.rect.x
            last_posy = self.rect.y

            self.posfin_x += self.motion_x * self.velocity #On crée ces variable temporaire car rect 
            self.posfin_y += self.motion_y * self.velocity # ne peut pas prendre de float et ca creerai un décalage
            self.rect.x = self.posfin_x
            self.rect.y = self.posfin_y

        if not self.anmimation_in_progress: #Si il n'y a pas d'animatione en cours il marche
            self.anim_type = "walk"
            self.anmimation_in_progress = True


        rampart = pygame.sprite.spritecollideany(self,self.group_rampart)# SI il est dans un mur_destructible on l'attaque
        if rampart:
            self.attack(rampart)
            

        if pygame.sprite.spritecollideany(self,self.group_wall):# SI il est dans un mur on le replace a sa position précédente
            self.rect.x = last_posx
            self.rect.y = last_posy
            self.posfin_x = self.rect.x
            self.posfin_y = self.rect.y


        if pygame.sprite.collide_rect(self,self.home):
            if self.home.life > 0:
                self.attack(self.home)

        # collision avec le joueur est dans joueur

        self.play_animations()
    

    def attack(self, element):
        if self.anim_type == "walk" :# Animation moins prioritaire
            self.anim_type = "attack" 
            self.anim_progress = 0
            self.anmimation_in_progress = True


        actual_time = pygame.time.get_ticks()
        if actual_time - self.last_time_hit > self.cooldown :
            element.hurt(self.damage)
            self.last_time_hit = actual_time
            #si il attaque il peut aussi "glisser le long du mur donc on recalcule la direction jusqu'à la maison"
            self.motion_x,self.motion_y = self.motion_calcul()
            
            
    def hurt(self, damage):
        # Se blesse lui
        if self.anim_type == "walk" or self.anim_type == "attack": # Animation prioritaire
            self.anim_type = "hurt"
            self.anim_progress = 0
            self.anmimation_in_progress = True

        self.health -= damage
        if self.health <= 0:
            self.dead_anim()

    def dead_anim(self):
        if self.anim_type != "dead":
            self.anim_type = "dead" # Animation encore plus prioritaire
            self.anim_progress = 0
            self.anmimation_in_progress = True

    def dead(self):
        self.kill()
        self.ressources.increases(5)
    

    def play_animations(self):
        if self.anmimation_in_progress:
            if pygame.time.get_ticks() - self.anim_time > self.cooldown_anim:
                if self.anim_progress == 5:
                    if self.anim_type == "dead": # si l'animation de mort est fini on le tue
                        self.dead()
                    self.anim_progress = 0
                    self.anmimation_in_progress = False
                else:
                    self.anim_progress +=1
                self.anim_time = pygame.time.get_ticks()
        if self.anim_type == "hurt":
            #print (self.anim_progress)
            pass
        self.image = self.anim[self.anim_type][self.anim_progress]