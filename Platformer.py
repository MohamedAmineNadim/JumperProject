#Jeu platformer comportant une campagne de 10 niveaux développé en utilisant la
#bibliothèque pygame
#Il y aura 3 niveaux de difficultés
#Un mode spécial débloqué à l'issu des 10 niveaux
'''
classes utilisées :
class World() : Permet de créer une instance de l'univers de jeu
class Personnage() : Permet de créer des instances de l'objet joueur
class Zombie() : Permet de créer des instances de l'objet ennemi
class Fire() : Permet de créer des instances de l'objet (obstacle) feu
class Portal() : Permet de créer des instances de l'objet portail
'''

#Initialisation de l'écran (625px*625px) et du titre du jeu
#Initialisation des images du fond d'écran du jeu
from cgi import test
import pygame
from pygame.locals import *

import World 
from World import *

#import animation
#from animation import *

test_img = Animation(0,25)

pygame.init()

#On définit certaines variables de l'environnement 
taille_cad = 25
clock = pygame.time.Clock()
larg_ecran = 625
long_ecran = 625
game_over = 3

ecran = pygame.display.set_mode((long_ecran,larg_ecran))
pygame.display.set_caption("Jumper !")
bg_img = pygame.image.load("background.png")
start_img = pygame.image.load("Spritesheets/start.png")
exit_img = pygame.image.load("Spritesheets/exit.png")
#load life images here, 3xheart or heart heart heart


#load timer (in background)
minutes = 0
seconds = 0
milliseconds = 0

cover = pygame.surface.Surface((70,25)).convert()
cover.fill((255, 255, 255))

white = pygame.surface.Surface((625,25)).convert()
white.fill((255, 255, 255))

lives_display = pygame.surface.Surface((100,25)).convert()
lives_display.fill((255,255,255))

life_img = pygame.image.load("./Spritesheets/life.png")
life_img = pygame.transform.scale(life_img, (taille_cad, taille_cad))

stopwatch = pygame.image.load("./Spritesheets/stopwatch.png")
stopwatch = pygame.transform.scale(stopwatch, (taille_cad, taille_cad))

myfont = pygame.font.SysFont("calibri", 20)





def dessin_cadrillage():
	for line in range (0,25):
		pygame.draw.line(ecran, (255,255,255), (0,line*taille_cad), (larg_ecran,line*taille_cad))
		pygame.draw.line(ecran, (255,255,255), (line*taille_cad,0), (line*taille_cad,long_ecran))


world_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,5,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13,0,0,7,6,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,13,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,14,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,7,3,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,8,1,1,5,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,7,3,3,6,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,8,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[7,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,6]
]

#Déclarations d'instances
new_world = World(world_data,taille_cad)
new_perso = Personnage(25, long_ecran-75)
new_img = Animation(0,25)

#Boutons
start_button = Button(larg_ecran//2 - 100, long_ecran//2 + 80, start_img)
exit_button = Button(larg_ecran//2 , long_ecran//2 + 80, exit_img)

ecran.blit(white,(0,0))
ecran.blit(stopwatch, (100,0))




run = True
while run:
	if (milliseconds % 2) == 0 and game_over != 0 :
		new_img.index += 1
		pass

	new_img.image = new_img.animation[new_img.index%7]
	ecran.blit(new_img.image, new_img.rect)
		
	portal_group.draw(ecran)
	#dessin_cadrillage()
	new_world.dessin(ecran)
	game_over = new_perso.dessin_Joueur(ecran,new_world, game_over)

	#Si le joueur meurt, afficher les boutons
	if game_over == 0:
		if start_button.dessin(ecran):
			#Reset la partie
			new_perso.Reset(25, long_ecran-75)
			milliseconds = 0
			seconds = 0
			ecran.blit(cover, (130,0))
			game_over = 3
		elif exit_button.dessin(ecran):
			run = False
	
	zombie_group.draw(ecran)
	if game_over != 0:
		zombie_group.update()
	
	fire_group.draw(ecran)
	fire_group.update()
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	for i in range(0, game_over):
		ecran.blit(life_img, (5+i*25, 0))
	pygame.display.update()

	if milliseconds > 1000 and new_perso.rect.y > 75:
		seconds += 1
		milliseconds -= 1000
		ecran.blit(cover, (130,0))
		ecran.blit(lives_display, (0,0))
		pygame.display.update()
		
	if seconds > 60 and game_over != 0:
		minutes += 1
		seconds -= 60
	milliseconds += clock.tick_busy_loop(65)
	timelabel = myfont.render("{}m:{}s".format(minutes, seconds), True, (0,0,0))
	ecran.blit(timelabel,(130, 0))
	pygame.display.update()


final_time = (minutes, seconds)
print("Final time : ", final_time[0], "m ", final_time[1], "s")


pygame.quit()