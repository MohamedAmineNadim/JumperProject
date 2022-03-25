#Jeu platformer comportant une campagne de 10 niveaux développé en utilisant la
#bibliothèque pygame

'''
classes utilisées :
class World() : Permet de créer une instance de l'univers de jeu
class Personnage() : Permet de créer des instances de l'objet joueur
class Zombie() : Permet de créer des instances de l'objet ennemi
class Fire() : Permet de créer des instances de l'objet (obstacle) feu
class Portal() : Permet de créer des instances de l'objet portail
class Button() : Permet de créer et gérer des boutons
class Animation() : Permet de gérer l'animation de l'arrière plan
'''
###########################################################################
##Importation de toutes les librairies et tout les programmes nécessaires##
##Initialisation de l'écran (625px*625px) et du titre du jeu			 ##
##Initialisation des images du fond d'écran du jeu						 ##
###########################################################################
import pygame
from pygame.locals import *

import World 
from World import *

import Levels
from Levels import *

test_img = Animation(0,25)


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#On définit certaines variables de l'environnement 
taille_cad = 25
clock = pygame.time.Clock()
larg_ecran = 625
long_ecran = 625
game_over = 3
level = 0
max_levels = 5

#load images
ecran = pygame.display.set_mode((long_ecran,larg_ecran))
pygame.display.set_caption("Jumper !")
bg_img = pygame.image.load("background.png")
start_img = pygame.image.load("Spritesheets/start.png")
exit_img = pygame.image.load("Spritesheets/exit.png")

#load other (timer, heart, level, sounds)
minutes = 0
seconds = 0
milliseconds = 0

cover = pygame.surface.Surface((503,503)).convert()
cover.fill((220,220,220))

white = pygame.surface.Surface((625,25)).convert()
white.fill((255, 255, 255))

lives_display = pygame.surface.Surface((100,25)).convert()
lives_display.fill((255,255,255))

life_img = pygame.image.load("./Spritesheets/life.png")
life_img = pygame.transform.scale(life_img, (taille_cad, taille_cad))

stopwatch = pygame.image.load("./Spritesheets/stopwatch.png")
stopwatch = pygame.transform.scale(stopwatch, (taille_cad, taille_cad))

myfont = pygame.font.SysFont("calibri", 20, True)
msgFont = pygame.font.SysFont("calibri", 30, True)

myCol = (103, 227, 184)
msgCol = (3, 162, 160)

bg = pygame.surface.Surface((625,625)).convert()
bg.fill((180,250,250))

#Variables du monde
world_data = levels_list[level]

#if path.exists(f'lvl{level}_data'):
#	pickle_in = open(f'lvl{level}_data', 'rb')
#	world_data = pickle.load(pickle_in)

#Déclarations d'instances
new_world = World(world_data, taille_cad)
new_perso = Personnage(25, long_ecran-75)
new_img = Animation(0,25)

#Boutons
start_button = Button(larg_ecran//2 - 100, long_ecran//2 + 80, start_img)
restart_button = Button(larg_ecran//2 - 100, long_ecran//2 + 80, start_img)
exit_button = Button(larg_ecran//2 , long_ecran//2 + 80, exit_img)
main_menu = True


#Fonctions

def dessin_cadrillage():
	for line in range (0,25):
		pygame.draw.line(ecran, (255,255,255), (0,line*taille_cad), (larg_ecran,line*taille_cad))
		pygame.draw.line(ecran, (255,255,255), (line*taille_cad,0), (line*taille_cad,long_ecran))

def reset_level(level):
	new_perso.Reset(25, long_ecran-75)
	fire_group.empty()
	portal_group.empty()
	zombie_group.empty()

	world_data = levels_list[level]
	new_world = World(world_data, taille_cad)
	return new_world

def message(txt, font, txt_col, x, y):
	#Affiche un message sur l'écran aux coordonnées (x,y)
	img = font.render(txt, True, txt_col)
	ecran.blit(img, (x,y))

pygame.mixer.music.load('./Sounds/background.mp3')
pygame.mixer.music.play(-1, 0, 2000)

run = True
while run:
	lives = game_over	
	if (milliseconds % 10) == 0 and game_over != 0 :
			new_img.index += 1
			pass

	new_img.image = new_img.animation[new_img.index%7]
	ecran.blit(new_img.image, (0,0))
	
	if main_menu == True :
		clock.tick(45)
		if start_button.dessin(ecran):
			main_menu = False
		if exit_button.dessin(ecran):
			run = False
	
	else:
		final_time = (minutes, seconds, milliseconds)
		final_time = "Votre temps : " + str(final_time[0]) + "m " + str(final_time[1]) + "s !"
		if game_over == 0:
			pygame.mixer.music.pause()
			lose_fx.play(-1, 0, 500)
			ecran.blit(cover, (60,60))
			message(final_time, myfont, myCol, 210, 500)
			message("GAME OVER !", msgFont, msgCol, 210, 200)
			message("Cliquez sur START pour recommencer", myfont, msgCol, 130, 460)
			if start_button.dessin(ecran):
				#Reset la partie
				level = 0
				world_data = []
				new_world = reset_level(level)
				milliseconds = 0
				seconds = 0
				ecran.blit(white, (0,0))
				game_over = 3
			elif exit_button.dessin(ecran):
				run = False
		
		if game_over != 0 and game_over != 10:
			ecran.blit(white,(0,0))
			level_label = myfont.render("Level {}".format(level+1), True, (0,0,0))
			ecran.blit(level_label, (250,0))
			ecran.blit(stopwatch, (100,0))
			if (milliseconds % 2) == 0 and game_over != 0 :
				new_img.index += 1
				pass

			new_img.image = new_img.animation[new_img.index%7]
			ecran.blit(new_img.image, (0,25), new_img.rect)
			portal_group.draw(ecran)
			#dessin_cadrillage()
			new_world.dessin(ecran)
			game_over = new_perso.dessin_Joueur(ecran,new_world, game_over)

			#Si le joueur meurt, afficher les boutons
			
			
			zombie_group.draw(ecran)
		
			zombie_group.update()
			
			fire_group.draw(ecran)
			fire_group.update()
			
			for i in range(0, game_over):
				if game_over != 10 and game_over != 0:
					ecran.blit(life_img, (5+i*25, 0))
			pygame.display.update()

			if milliseconds > 1000 and new_perso.rect.y > 75:
				seconds += 1
				milliseconds -= 1000
				ecran.blit(white, (0,0))
				ecran.blit(lives_display, (0,0))
				pygame.display.update()
				
			if seconds > 60 and game_over != 0 and game_over != 10:
				minutes += 1
				seconds -= 60
			milliseconds += clock.tick_busy_loop(59)
			timelabel = myfont.render("{}m:{}s".format(minutes, seconds), True, (0,0,0))
			ecran.blit(timelabel,(130, 0))
			pygame.display.update()

		
		if game_over == 10:
			#Le joueur gagne et on passe au niveau suivant
			level += 1
			if level <= max_levels:
				world_data = []
				new_world = reset_level(level)
				game_over = lives
			else:
				#Restart game
				ecran.blit(cover, (60,60))
				message(final_time, myfont, myCol, 210, 500)
				message("Vous avez battu le jeu !", msgFont, msgCol, 130, 300)
				message("Cliquez sur START pour recommencer", myfont, msgCol, 130, 460)
				if restart_button.dessin(ecran):
					level = 0
					world_data = []
					new_world = reset_level(level)
					game_over = 3
				elif exit_button.dessin(ecran):
					run = False

	pygame.display.update()			
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False





pygame.quit()