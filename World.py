import pygame
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
##Load sounds
jump_fx = pygame.mixer.Sound('./Sounds/jump.mp3')
jump_fx.set_volume(0.3)

win_fx = pygame.mixer.Sound('./Sounds/win.mp3')
win_fx.set_volume(0.3)

lose_fx = pygame.mixer.Sound('./Sounds/lose.mp3')
lose_fx.set_volume(0.3)

aurevoir_fx = pygame.mixer.Sound('./Sounds/aurevoir_henri.wav')
aurevoir_fx.set_volume(0.3)

class World():
	##############################################################################
	##Classe qui crée des instances du monde du jeu, des blocs et leur positions##
	##############################################################################

	def __init__(self, data, sizeT):
		#Fonction qui initialise le monde.


		self.tile_list = [] #Liste qui contient les blocs

		#Les images utilisés pour les blocs :
		block_top = pygame.image.load('./Spritesheets/block top.png')
		block_right = pygame.image.load('./Spritesheets/block right.png')
		block_bot = pygame.image.load('./Spritesheets/block bot.png')
		block_left = pygame.image.load('./Spritesheets/block left.png')
		block_mid = pygame.image.load('./Spritesheets/block mid.png')
		block_top_right = pygame.image.load('./Spritesheets/corner top right.png')
		block_bot_right = pygame.image.load('./Spritesheets/corner bot right.png')
		block_bot_left = pygame.image.load('./Spritesheets/corner bot left.png')
		block_top_left = pygame.image.load('./Spritesheets/corner top left.png')
		portal = pygame.image.load('./Spritesheets/portal.png')
		block_full = pygame.image.load('./Spritesheets/block_full.png')
		fire = pygame.image.load('./Spritesheets/fire.png')


		
		#On va utiliser une boucle for pour itérer à travers les éléments de la liste et attribuer à chaque numéro un bloc
		row_counter = 0 #Compteur de lignes
		for row in data:
			column_counter = 0 #Compteur de colonnes
			for tile in row :
				#Block tile
				if tile == -1:
					animation = Animation(column_counter * sizeT, row_counter * sizeT)
					bg_group.add(animation)
				if tile == 1:
					image = pygame.transform.scale(block_top,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 2:
					image = pygame.transform.scale(block_right,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 3:
					image = pygame.transform.scale(block_bot,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 4:
					image = pygame.transform.scale(block_left,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 5:
					image = pygame.transform.scale(block_top_right,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 6:
					image = pygame.transform.scale(block_bot_right,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 7:
					image = pygame.transform.scale(block_bot_left,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 8:
					image = pygame.transform.scale(block_top_left,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				if tile == 9:
					image = pygame.transform.scale(block_mid,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				#Zombie
				if tile == 10:
					zombie = Zombie(column_counter * sizeT, row_counter * sizeT-20)
					zombie_group.add(zombie)
				#Portal
				if tile == 12:
					portal = Portal(column_counter * sizeT-25, row_counter * sizeT-25)
					portal_group.add(portal)
				#Full block
				if tile == 13:
					image = pygame.transform.scale(block_full,(sizeT,sizeT))
					image_rect = image.get_rect()
					image_rect.x = column_counter*sizeT
					image_rect.y = row_counter*sizeT
					tile = (image, image_rect)
					self.tile_list.append(tile)
				#Fire
				if tile == 14:
					fire = Fire(column_counter * sizeT, row_counter * sizeT)
					fire_group.add(fire)
				column_counter += 1
			row_counter+=1


	def dessin(self,ecran):
		#Fonction qui gère l'affichage des éléments du monde
		for tile in self.tile_list:
			ecran.blit(tile[0],tile[1])
			#pygame.draw.rect(ecran,(255,255,255), tile[1],2) #Cadrillage des blocs pour tester les collisions




class Personnage():
	###########################################
	##Classe qui crée des instances du joueur##
	###########################################

	def __init__(self, x, y):
		self.Reset(x,y)

	def dessin_Joueur(self,ecran, world, game_over):
		#Cette fonction permet de définir les contrôles pour le personnage ainsi que son affichage.
		#Pour les collisions, on vérifie qu'il n'y a pas de collisions (dx, dy) avant d'ajuster la position
		#du joueur après avoir vérifié.
		dx = 0
		dy = 0
		animation_cooldown = 6
		if game_over != 0 and game_over != 10:
			#Commandes au clavier du jeu
			touche = pygame.key.get_pressed()
			if touche[pygame.K_LEFT]:
				dx -= 3
				self.cpt += 1
				self.direction = -1
			if touche[pygame.K_RIGHT]:
				dx += 3
				self.cpt += 1
				self.direction = 1
			if touche[pygame.K_SPACE] and self.saut == False and self.in_air == False:
				jump_fx.play()
				self.veloc_y -= 20
				self.saut = True
			if touche[pygame.K_SPACE] == False:
				self.saut = False

			if touche[pygame.K_RIGHT] == False and touche[pygame.K_LEFT] == False:
				self.cpt = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.animation_right[self.index%2]
				if self.direction == -1:
					self.image = self.animation_left[self.index%2]

			#Itération à travers les images (animation)
			if self.cpt > animation_cooldown:
				self.cpt = 0
				self.index += 1
				if self.direction == 1:
					self.image = self.animation_right[self.index%2]
				if self.direction == -1:
					self.image = self.animation_left[self.index%2]

			######################
			##Gestion de gravité##
			######################
			self.veloc_y += 1
			if self.veloc_y > 6:
				self.veloc_y = 6
			dy += self.veloc_y

			#############################################
			##Vérification de collisions avec les blocs##
			#############################################
			
			self.in_air = True
			for tile in world.tile_list:
				#Collisions suivant l'axe x
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#Collisions suivant l'axe y
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#On vérifie s'il y a collision en bas (au niveau des pieds du joueur - chute) ou en haut (au niveau de la tête - saut)
					if self.veloc_y < 0 :
						#saut
						dy = tile[1].bottom - self.rect.top
						self.veloc_y = 0
					elif self.veloc_y >= 0 :
						#chute
						dy = tile[1].top - self.rect.bottom
						self.in_air = False

			###############################################
			##Vérification de collisions avec les ennemis##
			###############################################

			if pygame.sprite.spritecollide(self, zombie_group, False):
				game_over -= 1
				if game_over >= 1:
					self.rect.x = 50
					self.rect.y = 500

			##########################################
			##Vérification de collisions avec le feu##
			##########################################
			
			elif pygame.sprite.spritecollide(self, fire_group, False):
				game_over -= 1
				if game_over >= 1:
					self.rect.x = 50
					self.rect.y = 500
			elif pygame.sprite.spritecollide(self, portal_group, False):
				game_over = 10

			#Ajustement de position suivant les collisions (non fatales)
			self.rect.x += dx
			self.rect.y += dy
			ecran.blit(self.image, self.rect)
			return game_over

		#Affichage du fantôme (joueur mort)
		elif game_over == 0:
			self.image = self.dead
			if self.rect.y > 50:
				self.rect.y -= 5

		elif game_over == 10:
			win_fx.play(-1, 0.0, 500)

		ecran.blit(self.image, self.rect)
		return game_over

	def Reset(self, x, y):
		#On initialise deux listes, un compteur d'index et un compteur pour déterminer la vitesse de l'animation
		#Listes contenant les images servant à l'animation selon la direction droite ou gauche
		self.animation_right = [] 
		self.animation_left = []
		self.index = 0
		self.cpt = 0

		#On ajoute les images à  la liste pour faire l'animation
		for i in range(1,3):
			joueur_img = pygame.image.load(f'./Spritesheets/character{i}.png')
			joueur_img = pygame.transform.scale(joueur_img,(35,45))
			self.animation_right.append(joueur_img)
			joueur_img = pygame.transform.flip(joueur_img, True, False)
			self.animation_left.append(joueur_img)
		dead = pygame.image.load('./Spritesheets/dead_character.png')
		dead = pygame.transform.scale(dead, (40,50))
		self.dead = dead

		#Suite de définitions d'attributs pour la classe image
		self.image = self.animation_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()-5
		self.height = self.image.get_height()-5
		self.veloc_y = 0
		self.saut = False
		self.direction = 0
		self.in_air = True



class Zombie(pygame.sprite.Sprite):
	############################################
	##Classe qui crée des instances de zombies##
	############################################

	def __init__(self,x,y):
		#Initialisation des listes contenant les animations
		pygame.sprite.Sprite.__init__(self)
		self.animation_right = []
		self.animation_left = []
		self.index = 0
		self.cpt = 0
		self.animation_cd = 8

		#Chargement des images en mémoire
		for i in range(1,3):
			zombie_img = pygame.image.load(f'./Spritesheets/zombie{i}.png')
			zombie_img = pygame.transform.scale(zombie_img,(35,45))
			self.animation_right.append(zombie_img)
			zombie_img = pygame.transform.flip(zombie_img, True, False)
			self.animation_left.append(zombie_img)
		
		self.image = self.animation_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.move_direction = 1
		self.move_counter = 0


	def update(self):
		#dessin des zombies
		self.rect.x += self.move_direction
		self.cpt += 1
		self.move_counter += 1
		if self.move_counter > 50:
			self.move_direction *= -1
			self.move_counter *= -1
		if self.cpt > self.animation_cd:
			self.cpt = 0
			self.index += 1
			if self.move_direction == 1:
				self.image = self.animation_left[self.index%2]
			if self.move_direction == -1:
				self.image = self.animation_right[self.index%2]



class Fire(pygame.sprite.Sprite):
	########################################
	##Classe qui crée des instances de feu##
	########################################

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('./Spritesheets/fire.png')
		self.image = pygame.transform.scale(img, (25,25))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.width -= 10


class Portal(pygame.sprite.Sprite):
	############################################
	##Classe qui crée des instances de portail##
	############################################

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img =  pygame.image.load('./Spritesheets/portal.png')
		self.image = pygame.transform.scale(img, (50,50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Animation(pygame.sprite.Sprite):
	#################################################
	##Classe qui gère l'animation de l'arrière plan##
	#################################################

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.animation = []
		self.index = 0
		for frame in range(0,7):
			image = pygame.image.load(f"C:\\Users\\HP Victus\\Desktop\\GIFs\\GIF_Nature{frame}.png")
			image= pygame.transform.scale(image,(800,650))
			self.animation.append(image)
		self.image = self.animation[self.index]
		self.rect=self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
class Button():
	###########################################
	##Classe qui gère les instances de bouton##
	###########################################

	def __init__(self, x, y, image):
		image = pygame.transform.scale(image, (70,30))
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def dessin(self, ecran):
		#fonctionnalités du bouton même
		action = False

		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True
		
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#dessin du bouton
		ecran.blit(self.image, self.rect)
		
		return action


#################
##Sprite groups##
#################
zombie_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()