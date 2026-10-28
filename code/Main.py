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



# Gestion de window pygame
pygame.init()
debug = True

#musique :
pygame.mixer.music.load("asset/Solar Winds Horror Atmosphere.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

window_width, window_height = 1100,600 
window = pygame.display.set_mode((window_width, window_height),pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("hiver")

pygame.time.Clock().tick(60) # limiter a 60 fps

acceuil = Acceuil(window)
acceuil.run()


tmx_data = pytmx.util_pygame.load_pygame("Tiled/test_carte.tmx") # charger la carte
map_width = tmx_data.width*tmx_data.tilewidth
map_height = tmx_data.width*tmx_data.tilewidth

group_wall = pygame.sprite.Group()
group_wall_destructible = pygame.sprite.Group()
group_wood = pygame.sprite.Group()
group_stone = pygame.sprite.Group()
wood = Ressources()
stone = Ressources()

# Recuperer les objets sur la carte Tiled

for layer in tmx_data.objects:
    if layer.type == "Wall":
        wall = Wall(pygame.Rect(layer.x,layer.y,layer.width,layer.height))
        group_wall.add(wall)
    elif layer.type == "Home":
        home = Home(pygame.Rect(layer.x,layer.y,layer.width,layer.height))
    elif layer.type == "Wall_destructible":
        wall_destructible = Wall_destructible(pygame.Rect(layer.x,layer.y,layer.width,layer.height),layer,tmx_data, group_wall, group_wall_destructible)
        group_wall_destructible.add(wall_destructible)
        group_wall.add(wall_destructible)
    elif layer.type == "Wood":
        farm_wood = Farm(pygame.Rect(layer.x,layer.y,layer.width,layer.height),wood)
        group_wood.add(farm_wood)
    elif layer.type == "Stone":
        farm_stone = Farm(pygame.Rect(layer.x,layer.y,layer.width,layer.height),stone)
        group_stone.add(farm_stone)
        

# Initialiser les éléments
layer_night = pygame.Surface((window_width*2, window_height*2)) #Obligé de mettre *2 pour le mode fullscreen 
layer_night.fill((0,0,30))
time = Time()
camera = Camera(map_width,map_height,window_width, window_height) # charge la camera
group_monster = pygame.sprite.Group()# Comme une liste mais les methode de monstre s'utilise direct sur group (voir update)
defense_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()

player = Player(350,350,map_width,map_height,group_wall,group_monster,group_wall_destructible,group_wood,group_stone,time) # charge le joueur
pieces = Ressources()
menu = Menu(window,pieces,group_wall_destructible,player,home)

canon_test = Canon(650, 700, 100)
defense_group.add(canon_test)

last_spawn_time = 0
last_shoot_time = 0
base_spawn_delay = 1000
current_spawn_delay = 1000
shoot_delay = 1500

# window pygame reste ouverte
quit = False
while not quit: #Pour garder la window ouverte
    for event in pygame.event.get(): #Ecouter les évenements "uniques"
        if event.type == pygame.QUIT:
            quit = True
            # Pour quitter proprement
        elif event.type == pygame.KEYDOWN: # Detecter TOUTES les touches pressées
            if event.key == pygame.K_p: # Changer de phase
                time.change_phase() # Cf: Time.py
            elif event.key == pygame.K_F1:
                quit = True
            elif event.key == pygame.K_m: # Faire apparaitre un monstre
                monster_spawner(group_monster,map_width,map_height,group_wall,home,group_wall_destructible, pieces)
                
            elif event.key == pygame.K_r: # Soigner la maison avec les pieces.
                if pieces.quantity >= 10 :
                    home.healing(10)
                    pieces.quantity -= 10

            elif event.key == pygame.K_w: # Soigner les murs avec les pieces.
                if pieces.quantity >= 10 :
                    for rampart in group_wall_destructible:
                        rampart.healing(2)
                    pieces.quantity -= 10
                
            elif event.key == pygame.K_F11: #Mettre en plein écran
                pygame.display.toggle_fullscreen()
                

            elif event.key == pygame.K_e:
                menu.open_menu()

    
    
    # Mise à jour des éléments
    player.update()
    time.update()
    layer_night.set_alpha(time.opacity)
    camera.update(player)
    group_monster.update() # Update tous les monstre du groupe
    defense_group.update()
    projectiles_group.update()
    
    #collision monstres, boulets
    for boulet in projectiles_group :
        hurt_monsters = pygame.sprite.spritecollide(boulet, group_monster, False)
        
        for monster in hurt_monsters :
            monster.hurt(boulet.damage)
            boulet.kill()
               
    #GESTION DE LA PHASE NUIT ///// ICI ???? NONNN dans time si possible
    current_time = pygame.time.get_ticks()
    if time.phase % 2 == 0 :
        current_spawn_delay = base_spawn_delay / 1.1**(time.phase/2) # Une formule pour que les monstres apparaissent de plus en plus vite en avancant dans les phases.
        
        if last_spawn_time + current_spawn_delay <= current_time :
            monster_spawner(group_monster,map_width,map_height,group_wall,home, group_wall_destructible, pieces)
            last_spawn_time = current_time
    
    #TIRER CANOn /// ICI??? NONNN dans le update du canon dans defense.py 
    if last_shoot_time + shoot_delay <= current_time :
        canon_test.tirer(projectiles_group, group_monster)
        last_shoot_time = current_time


    # DESSIN
    draw = Draw(window)

    # Afficher la carte
    draw.map(tmx_data,camera)        

    # les entitées/sprites
    draw.sprite(layer_night,(0,0)) # Il fait plsu sombre la nuit
    draw.sprite(player.image,camera.apply(player.rect.x,player.rect.y))

    # les group de sprite
    draw.group_sprite(group_monster,camera)
    draw.group_sprite(defense_group,camera)
    draw.group_sprite(projectiles_group,camera)
    
    #Phase
    draw.text_value("Phase ("+str(time.phase)+"): ",time.day_phase,window_width//2-60,10)

    #PV 
    draw.text_value("PV Maison : ",home.life,5,10)
    y = 50
    for rampart in group_wall_destructible:
        if rampart.life > 0:
            draw.text_value(rampart.name+" PV : "+str(rampart.life)+"/",rampart.life_max,5,y)
            y += 25

    draw.text_value("PV Joueur : ",player.health,window_width-180,10)

    #Ressources
    draw.text_value("Pièces : ",pieces.quantity,window_width-200,window_height-50,"$")
    draw.text_value("Bois : ",wood.quantity,window_width-200,window_height-100)
    draw.text_value("Pierre : ",stone.quantity,window_width-200,window_height-130)
    
    pygame.display.flip() # Met a jour l'écran

pygame.quit() # fermer la window pygame
