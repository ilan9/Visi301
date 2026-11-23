import pygame
import math
from Outils import decoup_image

class Defense(pygame.sprite.Sprite): # Elle doit hérite de sprite.Sprite car on veut les mettre dans un groupe
    def __init__(self, x, y, health, menu):
        super().__init__()
       
    def hurt(self, damage):
        """Cette méthode permet d'infliger des dégats à un monstre."""
        self.life -= damage
        if self.life < 0 :
            self.kill()
            
class Canon(Defense) :
    def __init__(self, x, y, health, menu):
        super().__init__(x, y, health, menu)
        self.list_images = ["asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_01_mk1.png",
                            "asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_01_mk2.png",
                            "asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_01_mk3.png",
                            "asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_01_mk4.png",
                            "asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_01_mk5.png"
                            ]
        self.im_width = 1024
        self.im_height = 128
        self.nb_frames = 8
        self.images = decoup_image(self.list_images[0], self.im_width, self.im_height, self.nb_frames, 1)
        self.current_frame = 0
        self.angle = 0
        
        #on définit le rectangle et on le centre.
        self.image = self.images[self.current_frame]     
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        self.menu = menu
        
        #gestion de l'animation
        self.is_animating = False
        self.last_time_anime = 0
        self.animation_speed = 500
        
        #cadence de tir
        self.level  = 1
        self.max_level = 5
        self.last_shoot_time = 0
        self.shoot_delay = 1500
        self.portee = 450
        
        self.type_munition = Boulet
        
    def rotate_to(self, target_pos) :
        """Cette fonction permet d'orienter un canon vers un monstre (target_pos)"""
        diffx = target_pos.rect.centerx - self.rect.centerx
        diffy = target_pos.rect.centery - self.rect.centery
        
        #pour calculer l'angle, nous disponsons de dx et dy, soit les différences x et y qui séparent le canon du monstre.
        #A l'aide de cela, nous voulons trouver la ligne qui relie directement le monstre au canon et pour cela nous nous servirons de la tangente.
        
 
        self.angle = math.atan2(-diffy, diffx)#la tangente.
        self.angle = math.degrees(self.angle) - 90 #On la convertie en degré d'angle///.
        
        center = self.rect.center
        #self.image = pygame.transform.rotate(self.images[self.current_frame], self.angle) 
        #self.rect = self.image.get_rect(center=center)
 
        self.image = pygame.transform.rotozoom(self.images[self.current_frame], self.angle, 1.0) #Devrait etre mieux mais je vois pas la diff
        self.rect = self.image.get_rect(center=center)
        
    def distance(self, target) :
        """Cette méthode permet de calculer la distance avec un monstre."""
        if target is None :
            return 99999
        
        spawn_x = self.rect.centerx
        spawn_y = self.rect.centery
        
        dx = target.rect.centerx - spawn_x
        dy = target.rect.centery - spawn_y
            
        distance = (dx**2 + dy**2)**0.5
        
        return distance
        
    def update(self, group_monster, projectiles_group):
        current_time = pygame.time.get_ticks()
        
        #Permet de tirer en respectant le délai de tir. 
        if current_time - self.last_shoot_time >= self.shoot_delay :
            cible = self.closest_monster(group_monster)
            distance = self.distance(cible)
            if cible is not None and distance < self.portee :
                self.tirer(projectiles_group, cible, self.type_munition)
                self.last_shoot_time = current_time
                
        #gestion de l'animation :
        nb_images = len(self.images)
        if self.is_animating :
            delai_frame = self.animation_speed / nb_images
            if current_time - self.last_time_anime >= delai_frame :
                self.current_frame += 1 
                self.last_time_anime = current_time
                
                if self.current_frame >= nb_images :
                    self.current_frame = 0
                    self.is_animating = False
                    
                center = self.rect.center
                self.image = pygame.transform.rotate(self.images[self.current_frame], self.angle)
                self.rect = self.image.get_rect(center=center)
        
            
            
    
    def tirer(self, projectiles_group, target, type_munition) :
            self.rotate_to(target)
            self.is_animating = True
            self.last_time_anime = pygame.time.get_ticks()
            
            spawn_x = self.rect.centerx
            spawn_y = self.rect.centery
            
            
            dx = target.rect.centerx - spawn_x
            dy = target.rect.centery - spawn_y
            
            distance = self.distance(target)
            
            if distance > 0 and distance < self.portee :
                direction_x = dx / distance
                direction_y = dy / distance
                
                
                projectile = type_munition(spawn_x, spawn_y, direction_x, direction_y)
                projectiles_group.add(projectile)
            
    def closest_monster(self, group_monster):
        """Cette méthode permet de trouver le monstre le plus proche dans un groupe de monstre, elle le renvoie."""
        posx = self.rect.centerx
        posy = self.rect.centery
    
        min_length = 9999
        closest = None #Si y'a pas de monstre
        for monster in group_monster.sprites():
            monster_x = monster.rect.centerx
            monster_y = monster.rect.centery
            
            #on calcule la norme du vecteur.
            distance = ((monster_x - posx)**2 + (monster_y - posy)**2)**0.5
            if distance < min_length :
                if monster.health >0:
                    min_length = distance
                    closest = monster
        return closest    

    def upgrade(self):
        if self.level<self.max_level:
            self.level+=1
            self.images = decoup_image(self.list_images[self.level-1], self.im_width, self.im_height, self.nb_frames, 1)
            self.shoot_delay -=250
            self.image = pygame.transform.rotate(self.images[self.current_frame], self.angle)
        
class Canon_laser(Canon) :
    def __init__(self, x, y, health,menu):
        super().__init__(x, y, health, menu)
        self.list_images = ["asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_02_mk1.png",
                            "asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_02_mk2.png",
                            "asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_02_mk3.png",
                            "asset/ground_shaker_asset/ground_shaker_asset/Red/Weapons/turret_02_mk4.png"
                            ]
        self.im_width = 1408
        self.im_height = 128
        self.nb_frames = 11
        self.images = decoup_image(self.list_images[0], self.im_width, self.im_height, self.nb_frames, 1)
        #chargement des images d'animation
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.current_frame = 0
        self.angle = 0
        
        self.max_level = 4
        self.type_munition = Laser
        
        self.shoot_delay = 4000
        self.portee = 250
    
class Projectiles(pygame.sprite.Sprite) :
    """Cette classe gère les différents types de projectiles."""
    def __init__(self, direction_x, direction_y) :
        super().__init__()
        self.direction_x = direction_x
        self.direction_y = direction_y
        
        
    def update(self) :
        self.pos_x += self.direction_x * self.velocity
        self.pos_y += self.direction_y * self.velocity
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        
        if self.rect.x < -200 or self.rect.x > 3000 or self.rect.y < -200 or self.rect.y > 3000 :
            self.kill()
            
class Boulet(Projectiles) :
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__(direction_x, direction_y)
        image = "asset/canon_animation/boulet_canon.png"
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (30, 30))
        
        self.rect = self.image.get_rect(center=(x,y))
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        
        self.velocity = 10
        self.damage = 10 
        
class Laser(Projectiles) :
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__(direction_x, direction_y)
        image = "asset/canon_animation/laser.png"
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (40, 40))
        
        self.rect = self.image.get_rect(center=(x,y))
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        
        self.velocity = 5
        self.damage = 5 