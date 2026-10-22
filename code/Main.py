import pygame
import pytmx #pour lire Tiled

from Time import Time
from Player import Player
from Camera import Camera
from Home import Home, Wall, Wall_destructible
from Monster import Monster
from Spawner import monster_spawner
from Ressources import Ressources
from Defense import Canon
from Menu import Menu
from Acceuil import Acceuil



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

# Recuperer les objets sur la carte Tiled

for layer in tmx_data.objects:
    if layer.type == "Wall":
        wall = Wall(pygame.Rect(layer.x,layer.y,layer.width,layer.height))
        group_wall.add(wall)
    if layer.type == "Home":
        home = Home(pygame.Rect(layer.x,layer.y,layer.width,layer.height))
    if layer.type == "Wall_destructible":
        wall_destructible = Wall_destructible(pygame.Rect(layer.x,layer.y,layer.width,layer.height),layer,tmx_data, group_wall, group_wall_destructible)
        group_wall_destructible.add(wall_destructible)
        group_wall.add(wall_destructible) 
        

# Initialiser les éléments
time = Time()
layer_night = pygame.Surface((window_width*2, window_height*2)) #Obligé de mettre *2 pour le mode fullscreen 
layer_night.fill((0,0,30))


camera = Camera(map_width,map_height,window_width, window_height) # charge la camera
group_monster = pygame.sprite.Group()# Comme une liste mais les methode de monstre s'utilise direct sur group (voir update)
defense_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()

player = Player(50,50,map_width,map_height,group_wall,group_monster,group_wall_destructible) # charge le joueur
ressources = Ressources()
menu = Menu(window,ressources,group_wall_destructible,player,home)

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
                monster_spawner(group_monster,map_width,map_height,group_wall,home,group_wall_destructible, ressources)
                
            elif event.key == pygame.K_r: # Soigner la maison avec les ressources.
                if ressources.quantity >= 10 :
                    home.healing(10)
                    ressources.quantity -= 10

            elif event.key == pygame.K_w: # Soigner les murs avec les ressources.
                if ressources.quantity >= 10 :
                    for rampart in group_wall_destructible:
                        rampart.healing(2)
                    ressources.quantity -= 10
                
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
            monster_spawner(group_monster,map_width,map_height,group_wall,home, group_wall_destructible, ressources)
            last_spawn_time = current_time
    
    #TIRER CANOn /// ICI??? NONNN dans le update du canon dans defense.py 
    if last_shoot_time + shoot_delay <= current_time :
        canon_test.tirer(projectiles_group, group_monster)
        last_shoot_time = current_time

    # Afficher la carte
    for layer in tmx_data.visible_layers: #C'est les couches dans Tiled
        if isinstance(layer,pytmx.TiledTileLayer): #On vérifie que c'est des layer et pas des objets et que ils sont en mode visible
            for x,y,image in layer.tiles(): # On recup les coordonnées et les image de chaque tuile
                pos_x = x*tmx_data.tilewidth 
                # On multiplie leur position par leur largeur 
                pos_y = y*tmx_data.tileheight
                window.blit(image,camera.apply(pos_x,pos_y)) # On les affiche dans notre window
                

    # Dessiner la surcouche
    window.blit(layer_night,(0,0)) # le opacite de nuit
    window.blit(player.image, camera.apply(player.rect.x,player.rect.y))
    for monster in group_monster.sprites(): # Dessiner les monstres
        window.blit(monster.image,camera.apply(monster.rect.x,monster.rect.y))
    
    for defense in defense_group.sprites():
        window.blit(defense.image, camera.apply(defense.rect.x, defense.rect.y))
    
    for projectiles in projectiles_group.sprites():
        window.blit(projectiles.image, camera.apply(projectiles.rect.x, projectiles.rect.y))
        
    police = pygame.font.Font(None, 30) #Police par default taille 30
    text_phase = police.render("Phase ("+str(time.phase)+"): "+str(time.day_phase), True, (0, 0, 0)) #Ecrit mon texte avec la couleur 0,0,0
    window.blit(text_phase, (330,10)) #Dessine mon texte à la position 330,10

    pv_home = police.render("PV Maison : "+str(home.life), True, (0, 0, 0)) # PV de la maison
    window.blit(pv_home, (5,10))

    #PV mur
    y = 50
    for rampart in group_wall_destructible:
        if rampart.life > 0:
            pv_wall = police.render(rampart.name+" PV : "+str(rampart.life)+"/"+str(rampart.life_max), True, (0, 0, 0))
            window.blit(pv_wall, (5,y))
            y += 25
    
    pv_joueur = police.render("PV Joueur : "+str(player.health), True, (0, 0, 0)) # PV du joueur
    window.blit(pv_joueur, (600,10))
    
    texte_ressources = police.render("Ressources : "+str(ressources.quantity)+"R", True, (0, 0, 0)) # Qté de ressources
    window.blit(texte_ressources, (window_width-200,window_height-50))
    
    pygame.display.flip() # Met a jour l'écran

pygame.quit() # fermer la window pygame
