import pygame
import pytmx #pour lire Tiled

from Time import Time
from Player import Player
from Camera import Camera
from Home import Home, Wall, Wall_destructible
from Spawner import monster_spawner
from Ressources import Ressources, Farm
from Defense import Canon
from Menu import Menu
from Acceuil import Acceuil
from Draw import Draw

class Game:
    def __init__(self):
        # Gestion de window pygame
        pygame.init()
        self.window_width, self.window_height = 1100,600 
        self.window = pygame.display.set_mode((self.window_width, self.window_height),pygame.FULLSCREEN | pygame.SCALED, vsync=1)
        pygame.display.set_caption("hiver")     
        self.clock = pygame.time.Clock() #.tick(60)/////// # limiter a 60 fps
        self.running = True
        
        #musique :
        pygame.mixer.music.load("asset/Solar Winds Horror Atmosphere.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        #écran d'acceuil :
        acceuil = Acceuil(self.window)
        acceuil.run()
        
        #carte :
        self.draw = Draw(self.window)
        self.load_map("Tiled/test_carte.tmx")
        
        #entités et groupes :
        self.time = Time()
        self.camera = Camera(self.map_width, self.map_height, self.window_width, self.window_height)
        self.layer_night = pygame.Surface((self.window_width*2, self.window_height*2)) #Obligé de mettre *2 pour le mode fullscreen 
        self.layer_night.fill((0,0,30))
        
        self.group_monster = pygame.sprite.Group()# Comme une liste mais les methode de monstre s'utilise direct sur group (voir update)
        self.defense_group = pygame.sprite.Group()
        self.projectiles_group = pygame.sprite.Group()
        
        self.player = Player(
            350, 350, self.map_width, self.map_height, self.group_wall, self.group_monster, self.group_wall_destructible, self.group_wood, self.group_stone, self.time
        )
        self.pieces = Ressources()
        self.menu = Menu(self.window, self.pieces, self.group_wall_destructible, self.player, self.home)
        
        #defense :
        self.defense_group.add(Canon(650, 700, 100))
        
        #spawn :
        self.last_spawn_time = 0
        self.base_spawn_delay = 1000
        
        #debug SERT A RIEN POUR L'INSTANT :
        self.debug = True
        
    def load_map(self, tmx_path) :
        self.tmx_data = pytmx.util_pygame.load_pygame("Tiled/test_carte.tmx") # charger la carte
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight

        self.group_wall = pygame.sprite.Group()
        self.group_wall_destructible = pygame.sprite.Group()
        self.group_wood = pygame.sprite.Group()
        self.group_stone = pygame.sprite.Group()
        self.wood = Ressources()
        self.stone = Ressources()
        self.home = None
        
        # Recuperer les objets sur la carte Tiled
        for layer in self.tmx_data.objects:
            if layer.type == "Wall":
                wall = Wall(pygame.Rect(layer.x,layer.y,layer.width,layer.height))
                self.group_wall.add(wall)
            elif layer.type == "Home":
                self.home = Home(pygame.Rect(layer.x,layer.y,layer.width,layer.height))
            elif layer.type == "Wall_destructible":
                wall_destructible = Wall_destructible(pygame.Rect(layer.x,layer.y,layer.width,layer.height),layer,self.tmx_data, self.group_wall, self.group_wall_destructible)
                self.group_wall_destructible.add(wall_destructible)
                self.group_wall.add(wall_destructible)
            elif layer.type == "Wood":
                farm_wood = Farm(pygame.Rect(layer.x,layer.y,layer.width,layer.height), self.wood)
                self.group_wood.add(farm_wood)
            elif layer.type == "Stone":
                farm_stone = Farm(pygame.Rect(layer.x,layer.y,layer.width,layer.height), self.stone)
                self.group_stone.add(farm_stone)
        
    def events(self) :
        for event in pygame.event.get(): #Ecouter les évenements "uniques"
            
            if event.type == pygame.QUIT:
                self.running = False # Pour quitter proprement
                
            elif event.type == pygame.KEYDOWN: # Detecter TOUTES les touches pressées
                if event.key == pygame.K_p: # Changer de phase
                    self.time.change_phase() # Cf: Time.py
                    
                elif event.key == pygame.K_F1:
                    self.running = False
                    
                elif event.key == pygame.K_m: # Faire apparaitre un monstre
                    monster_spawner(self.group_monster, self.map_width, self.map_height, self.group_wall, self.home, self.group_wall_destructible, self.pieces)
                    
                elif event.key == pygame.K_r: # Soigner la maison avec les pieces.
                    if self.pieces.quantity >= 10 :
                        self.home.healing(10)
                        self.pieces.quantity -= 10

                elif event.key == pygame.K_w: # Soigner les murs avec les pieces.
                    if self.pieces.quantity >= 10 :
                        for rampart in self.group_wall_destructible:
                            rampart.healing(2)
                        self.pieces.quantity -= 10
                    
                elif event.key == pygame.K_F11: #Mettre en plein écran
                    pygame.display.toggle_fullscreen()

                elif event.key == pygame.K_e:
                    self.menu.open_menu()
     
    def update_spawns(self, current_time):
        if self.time.phase % 2 == 0 :
            delay = self.base_spawn_delay / (1.1**(self.time.phase/2)) # Une formule pour que les monstres apparaissent de plus en plus vite en avancant dans les phases.
        
            if current_time - self.last_spawn_time  >= delay :
                monster_spawner(self.group_monster, self.map_width, self.map_height, self.group_wall, self.home, self.group_wall_destructible, self.pieces)
                self.last_spawn_time = current_time
                
    def check_collisions(self) :
        for boulet in self.projectiles_group :
            hurt_monsters = pygame.sprite.spritecollide(boulet, self.group_monster, False)
        
            for monster in hurt_monsters :
                monster.hurt(boulet.damage)
                boulet.kill()
                
    def update(self) :
        current_time = pygame.time.get_ticks()
        
        self.player.update()
        self.time.update()
        self.layer_night.set_alpha(self.time.opacity)
        self.camera.update(self.player)
        self.group_monster.update() # Update tous les monstre du groupe
        self.defense_group.update(self.group_monster, self.projectiles_group)
        self.projectiles_group.update()
        
        self.check_collisions()
        self.update_spawns(current_time)
        
    def render(self) :
        # Afficher la carte
        self.draw.map(self.tmx_data,self.camera)        

        # les entitées/sprites
        self.draw.sprite(self.layer_night,(0,0)) # Il fait plsu sombre la nuit
        self.draw.sprite(self.player.image, self.camera.apply(self.player.rect.x, self.player.rect.y))

        # les group de sprite
        self.draw.group_sprite(self.group_monster, self.camera)
        self.draw.group_sprite(self.defense_group, self.camera)
        self.draw.group_sprite(self.projectiles_group, self.camera)
        
        self.draw.text(self.home, self.group_wall_destructible, self.player, self.pieces, self.wood, self.stone, self.time, self.window_width, self.window_height)
        
        pygame.display.flip()
        
    def run(self) :
        while self.running :
            self.clock.tick(60)
            self.events()
            self.update()
            self.render()
        pygame.quit()
        
game = Game()
game.run()
        














    