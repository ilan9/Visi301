import pygame
from Outils import decoup_image

class Player(pygame.sprite.Sprite) :
    def __init__(self,x,y,border_x,border_y,list_wall, group_monster, group_rampart,group_wood,group_stone,time):
        super().__init__()
        self.health = 500
        self.max_health = 500
        self.last_time_hit = 0 #la dernière fois que le joueur a attaqué pour la gestion des coups.
        self.cooldown = 1000
        self.velocity = 3
        self.damage = 5

        self.monster_atq = {}
        
        image = self.image = pygame.image.load('asset/ranais.png') #L'image de notre joueur
        
        #La taille du joueur :
        self.image_height = 40
        self.image_width = 27
        self.image = pygame.transform.scale(image, (self.image_width, self.image_height)) #Ne doit pas etre supprimé mais jsp pk
        
        #Son ID_BoX ///////////
        self.rect = self.image.get_rect()
        
        #La position de départ de notre joueur :
        self.rect.x = x
        self.rect.y = y
        self.border_x = border_x
        self.border_y = border_y

        #Element extérieur
        self.group_monster = group_monster
        self.list_wall = list_wall
        self.group_rampart = group_rampart
        self.group_wood = group_wood
        self.wood_cooldown = 0
        self.group_stone = group_stone
        self.stone_cooldown = 0
        self.time = time

        #Animation
        self.anim_type = "left"
        self.anim_jump = False
        self.anim_progress = 0
        self.anim_time = pygame.time.get_ticks()
        self.cooldown_anim = 100
        self.anim = {"left":decoup_image("asset/player/move/left.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height),
                     "right":decoup_image("asset/player/move/right.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height),
                     "up":decoup_image("asset/player/move/up.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height),
                     "down":decoup_image("asset/player/move/down.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height),
                     "jump_left":decoup_image("asset/player/jump/left.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height),
                     "jump_right":decoup_image("asset/player/jump/right.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height),
                     "jump_up":decoup_image("asset/player/jump/up.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height),
                     "jump_down":decoup_image("asset/player/jump/down.png",256,32,8,1,marge_x=12,change_size=True,scale_x=self.image_width,scale_y=self.image_height)
                     }
        self.image = self.anim[self.anim_type][self.anim_progress]

    def update(self) :
        key = pygame.key.get_pressed()
        velocity_x = 0
        velocity_y = 0
        last_posx = self.rect.x
        last_posy = self.rect.y
            
        if key[pygame.K_LEFT] and self.rect.x > 0 : ############ METTRE EN PARAM7TRE PLUTOT
            velocity_x -= self.velocity
            self.anim_type = "left"
                
        if key[pygame.K_RIGHT] and self.rect.x < self.border_x - self.image_width :############ METTRE EN PARAM7TRE PLUTOT
            velocity_x += self.velocity
            self.anim_type = "right"
                
        if key[pygame.K_DOWN] and self.rect.y < self.border_y - self.image_height :############ METTRE EN PARAM7TRE PLUTOT
            velocity_y += self.velocity
            self.anim_type = "down"
                
        if key[pygame.K_UP] and self.rect.y > 0 :############ METTRE EN PARAM7TRE PLUTOT
            velocity_y -= self.velocity 
            self.anim_type = "up"

        if velocity_x != 0 and velocity_y != 0:
            self.rect.x += velocity_x * 0.707 #Pour que les déplacement soit moins rapide en diagonnal
            self.rect.y += velocity_y * 0.707
        else:
            self.rect.x += velocity_x
            self.rect.y += velocity_y


        # test collision avec les murs, si ils se chevauche on annule le dernier mouv du joueur
        #if pygame.sprite.spritecollideany(self,self.list_wall):
        #    self.rect.x = last_posx
        #    self.rect.y = last_posy

        #Sauter par dessus les remparts
        if self.collision_group(self.group_rampart): 
            if not self.anim_jump:
                self.anim_progress = 2
            self.anim_jump = True

        # Attaquer les monstres
        self.attack_monster()

        if velocity_x != 0 or velocity_y != 0:
            self.play_animations()

        # Zone de farm
        if self.time.day: #Si il fait jour le joueur peut récupérer des ressources
            self.farm_time(self.group_wood,self.wood_cooldown,self.cooldown)
            self.farm_time(self.group_stone,self.stone_cooldown,self.cooldown)
        
            
            
    def attack_monster(self):
        colliding_monsters = pygame.sprite.spritecollide(self, self.group_monster, False)
        for monster in colliding_monsters :
            #On attaque le monstre qu'une fois par seconde
            if monster in self.monster_atq:
                if pygame.time.get_ticks() - self.monster_atq[monster] > self.cooldown:
                    self.monster_atq.pop(monster)
            else:
                monster.hurt(self.damage)
                self.hurt(5) # Le joueur prends des dégats si il attaque le monstre
                self.monster_atq[monster] = pygame.time.get_ticks()


    def attack_1_persecond(self, element): # PAs utilisé pour l'instant
        actual_time = pygame.time.get_ticks()
        if actual_time - self.last_time_hit > self.cooldown :
            element.hurt(self.damage)
            self.last_time_hit = actual_time
        
    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead()
    
    def dead(self):
        print("Le joueur est mort !!!")
        # Respawn dans 30 sec ??
    
    def play_animations(self):
        if pygame.time.get_ticks() - self.anim_time > self.cooldown_anim:
            if self.anim_jump :
                self.anim_type = "jump_"+self.anim_type
            if self.anim_progress == 7:
                self.anim_progress = 0
                if self.anim_jump and self.anim_type[0] == "j":
                    self.anim_type = self.anim_type[5:]
                    self.anim_jump = False
            else:
                self.anim_progress +=1
            self.image = self.anim[self.anim_type][self.anim_progress]
            self.anim_time = pygame.time.get_ticks()

    def collision_group(self,group): #Renvoi un booléen en fonction de la collision avec un group
        return pygame.sprite.spritecollideany(self,group)

    def farm_time(self,group,group_cooldown,cooldown):
        if self.collision_group(group):
            if pygame.time.get_ticks()-group_cooldown > cooldown:
                element = next(iter(group),None) # Renvoie un élement du group, pas forcément le premier
                self.wood_cooldown= pygame.time.get_ticks() #Ne peut pas farm 2 ressources en 1 sec
                self.stone_cooldown = pygame.time.get_ticks()
                if element:
                    element.ressources.increases(1)