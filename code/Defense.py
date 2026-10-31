import pygame
import math

class Defense(pygame.sprite.Sprite): # Elle doit hérite de sprite.Sprite car on veut les mettre dans un groupe
    def __init__(self, x, y, health) :
        super().__init__()
        self.life = health ## Une vie ??
        self.max_life = health
       
       
    def hurt(self, damage):
        self.life -= damage
        if self.life < 0 :
            self.kill()
            
class Canon(Defense) :
    def __init__(self, x, y, health):
        super().__init__(x, y, health)
        
        #chargement des images d'animation
        self.images = [
            pygame.transform.scale(pygame.image.load("asset/canon_animation/canon1.png"), (200,200)),
            pygame.transform.scale(pygame.image.load("asset/canon_animation/canon2.png"), (200,200)),
            pygame.transform.scale(pygame.image.load("asset/canon_animation/canon3.png"), (200,200)),
            pygame.transform.scale(pygame.image.load("asset/canon_animation/canon4.png"), (200,200)),
            pygame.transform.scale(pygame.image.load("asset/canon_animation/canon5.png"), (200,200)),
            pygame.transform.scale(pygame.image.load("asset/canon_animation/canon6.png"), (200,200))
        ]
        self.current_frame = 0
        self.angle = 0
        
        #on définit le rectangle et on le centre.
        self.image = self.images[self.current_frame]     
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
        #gestion de l'animation
        self.is_animating = False
        self.last_time_anime = 0
        self.animation_speed = 500
        
        #cadence de tir
        self.last_shoot_time = 0
        self.shoot_delay = 1500
        self.portee = 450
        
    def rotate_to(self, target_pos) :
        """Cette fonction permet d'orienter un canon vers un monstre (target_pos)"""
        diffx = target_pos.rect.centerx - self.rect.centerx
        diffy = target_pos.rect.centery - self.rect.centery
        
        #pour calculer l'angle, nous disponsons de dx et dy, soit les différences x et y qui séparent le canon du monstre.
        #A l'aide de cela, nous voulons trouver la ligne qui relie directement le monstre au canon et pour cela nous nous servirons de la tangente.
        
 
        self.angle = math.atan2(-diffy, diffx)#la tangente.
        self.angle = math.degrees(self.angle) - 90 #On la convertie en degré d'angle///.
        
        center = self.rect.center
        self.image = pygame.transform.rotate(self.images[self.current_frame], self.angle)
        self.rect = self.image.get_rect(center=center)
        
        
        
    def update(self, group_monster, projectiles_group):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shoot_time >= self.shoot_delay :
            cible = self.closest_monster(group_monster)
            if cible is not None :
                self.tirer(projectiles_group, cible)
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
        
            
            
    
    def tirer(self, projectiles_group, target) :
            self.rotate_to(target)
            self.is_animating = True
            self.last_time_anime = pygame.time.get_ticks()
            
            spawn_x = self.rect.centerx
            spawn_y = self.rect.centery
            
            
            dx = target.rect.centerx - spawn_x
            dy = target.rect.centery - spawn_y
            
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 0 :
                direction_x = dx / distance
                direction_y = dy / distance
                
                
                boulet = Projectiles(spawn_x, spawn_y, "asset/canon_animation/boulet_canon.png", direction_x, direction_y)
                projectiles_group.add(boulet)
            
    def closest_monster(self, group_monster):
        """Cette fonction permet de trouver le monstre le plus proche dans un groupe de monstre, elle le renvoie."""
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
        
    
class Projectiles(pygame.sprite.Sprite) :
    """Cette classe gère les différents types de projectiles."""
    def __init__(self, x, y, image, direction_x, direction_y) :
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (30, 30))
        
        self.rect = self.image.get_rect(center=(x,y))
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.velocity = 10
        self.damage = 10 
        
    def update(self) :
        self.pos_x += self.direction_x * self.velocity
        self.pos_y += self.direction_y * self.velocity
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        
        if self.rect.x < -200 or self.rect.x > 3000 or self.rect.y < -200 or self.rect.y > 3000 :
            self.kill()