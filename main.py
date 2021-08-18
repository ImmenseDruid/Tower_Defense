import pygame
import entities
import random
import pickle, os
import library, plibrary
from pygame.locals import *


#colors
nyx8 = [(8, 20, 30), (15, 42, 63), (32,57, 79),
 (246, 214, 189), (195,163,138), (153,117,119),
  (129,98,113), (78,73,95)]
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREY = (150, 150, 150)
TEXT_COL = nyx8[0]
PANEL = nyx8[5]
BORDER = nyx8[6]
GROUND = nyx8[0]
PATH = nyx8[0]

scale = 1.0
music_volume, sfx_volume = 1, 1


pygame.init()
pygame.font.init()

settings = []

with open('settings_data.p', 'rb') as file:
	settings = pickle.load(file)

scale = settings[0]
music_volume = settings[1]
sfx_volume = settings[2]

width = int(900 * scale)
height = int(800 * scale)

screen = pygame.display.set_mode((width , height))
pygame.display.set_caption("Tower Defense Game")


pygame.mixer.music.set_volume(music_volume)

#Icons
icon_imgs = [pygame.image.load('Images/play_icon.png').convert_alpha(), pygame.image.load('Images/settings_icon.png').convert_alpha(), pygame.image.load('Images/level_select_icon.png').convert_alpha(), pygame.image.load('Images/quit_icon.png').convert_alpha()]


#Tower Stats
tower_ranges = [166, 233, 133, 166, 100]
tower_attack_cooldown = [1000, 2000, 1500, 1000, 750]
tower_can_see_camo = [False, True, False, True, False]
#projectile settings per tower [explosion radius, pierce, slow amount]
tower_projectile_settings = [[0, 2, 0], [100, 0, 0], [200, 0, 0], [0, 0, 0], [0, 0, 3]]



tower_costs = library.determine_pricing(tower_ranges, tower_attack_cooldown, tower_can_see_camo, tower_projectile_settings)
tower_ranges = library.scale_array(tower_ranges, scale)

#Images

button_background = pygame.image.load('Images/ButtonBackground.png').convert()
button_background = pygame.transform.scale(button_background, (int(button_background.get_width() * scale), int(button_background.get_height() * scale))).convert_alpha()

pathway_sprite_sheet = pygame.image.load('Images/Pathways.png').convert()
pathway_imgs = []

with open(os.path.join('Levels', f'map_0_data.p'), 'rb') as file:
	data = pickle.load(file)

for n in data:
	for i in range(len(n)):
		n[i] = int(n[i] * scale)

nodes = data

pathway = []

path_distance = library.calculate_path_distance(nodes)

pathway = library.create_pathway(nodes, pathway, scale)

spawn = nodes[0]


font = pygame.font.SysFont('Times New Roman', 30)
font_60 = pygame.font.SysFont('Times New Roman', 60)


tower_imgs = [[pygame.image.load('Images/Tower1.png').convert_alpha(), pygame.image.load('Images/Tower1_upgrade.png').convert_alpha(), pygame.image.load('Images/Tower1_upgrade_2.png').convert_alpha()],
 [pygame.image.load('Images/Tower_2_no_cape.png').convert_alpha(), pygame.image.load('Images/Tower_2_no_hat.png').convert_alpha(), pygame.image.load('Images/Tower_2.png').convert_alpha()],
 [pygame.image.load('Images/Tower_3.png').convert_alpha(), pygame.image.load('Images/Tower_3_upgrade.png').convert_alpha(), pygame.image.load('Images/Tower_3_upgrade_2.png').convert_alpha()],
 [pygame.image.load('Images/Tower_4.png').convert_alpha(), pygame.image.load('Images/Tower_4_upgrade.png').convert_alpha(), pygame.image.load('Images/Tower_4_upgrade_2.png').convert_alpha()],
 [pygame.image.load('Images/Tower_5.png').convert_alpha(), pygame.image.load('Images/Tower_5_upgrade.png').convert_alpha(), pygame.image.load('Images/Tower_5_upgrade_2.png').convert_alpha()]]
bullet_imgs = [pygame.image.load('Images/Bullet_1.png').convert_alpha(), pygame.transform.scale(pygame.image.load('Images/Bullet_2.png').convert_alpha(), (8, 8)),
 pygame.transform.scale(pygame.image.load('Images/Bullet_3.png').convert_alpha(), (8, 8)), pygame.transform.scale(pygame.image.load('Images/Bullet_4.png').convert_alpha(), (8, 8)),
 pygame.transform.scale(pygame.image.load('Images/Bullet_5.png').convert_alpha(), (8, 8))]
balloon_imgs = [pygame.image.load('Images/Balloon_1.png').convert_alpha(), pygame.image.load('Images/Balloon_2.png').convert_alpha(), pygame.image.load('Images/Balloon_3.png').convert_alpha(),
 pygame.image.load('Images/Balloon_4.png').convert_alpha(), pygame.image.load('Images/Balloon_5.png').convert_alpha()]

camo_img = pygame.image.load('Images/camo.png').convert_alpha()
camo_img = pygame.transform.scale(camo_img, (int(camo_img.get_width() * scale), int(camo_img.get_height() * scale))).convert_alpha()


entities.Balloon.IMGS = balloon_imgs

for i in range(len(tower_imgs)):
	for j in range(len(tower_imgs[i])):
		tower_imgs[i][j] = pygame.transform.scale(tower_imgs[i][j], (int(tower_imgs[i][j].get_width() * scale), int(tower_imgs[i][j].get_height() * scale))).convert_alpha()

for i in range(len(bullet_imgs)):
	bullet_imgs[i] = pygame.transform.scale(bullet_imgs[i], (int(bullet_imgs[i].get_width() * scale), int(bullet_imgs[i].get_height() * scale))).convert_alpha()

for i in range(len(balloon_imgs)):
	balloon_imgs[i] = pygame.transform.scale(balloon_imgs[i], (int(balloon_imgs[i].get_width() * scale), int(balloon_imgs[i].get_height() * scale))).convert_alpha()

for i in range(len(icon_imgs)):
	icon_imgs[i] = pygame.transform.scale(icon_imgs[i], (int(icon_imgs[i].get_width() * scale), int(icon_imgs[i].get_height() * scale))).convert_alpha()

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))


class SpriteSheet():
	def __init__(self, img, size = (32, 32)):
		self.sheet = img
		self.size = size

	def get_sprite(self, x, y, scale):
		 surf = pygame.Surface(self.size).convert_alpha()
		 surf.fill((200, 20, 200))
		 surf.blit(self.sheet, (0,0), ((x * self.size[0]), (y * self.size[1]), self.size[0], self.size[1]))
		 surf = pygame.transform.scale(surf, (int(self.size[0] * scale), int(self.size[1] * scale)))
		 surf.set_colorkey((200, 20, 200))
		 return surf.convert_alpha()

class Button():

	HOVER_COL = (200, 200, 200)
	CLICKED_COL = (0, 0, 0)
	ACTION_COL = (255, 255, 255)
	DISABLED_COL = (50, 0, 0)


	def __init__(self, x, y, size, color = (0, 100, 0), img = None, scale = 1):

		self.x = x
		self.y = y

		
		self.color = color

		self.clicked = False
		self.enabled = True
		self.hovered = False

		if img:
			self.img = img
			imgSize = [img.get_rect().w * scale, img.get_rect().h * scale]
			
			self.size = (imgSize[0], imgSize[1])
			surf = pygame.Surface(self.size)
			pygame.draw.rect(surf, color, pygame.Rect((0, 0), self.size))
		else:
			surf = pygame.Surface((size[0], size[1]))
			pygame.draw.rect(surf, color, pygame.Rect((0, 0), (size)))
			self.img = surf
			self.size = size

	def set_pos(self, x, y):
		self.x = x 
		self.y = y 

	def set_color(self, hover, clicked, action, base):		self.color = base

	def draw(self, screen):

		rect = pygame.Rect((self.x, self.y), self.size)
		pos = pygame.mouse.get_pos()

		
		col = self.color



		action = False

		surf = pygame.Surface((self.size[0], self.size[1]))
		#Blit image to button
		surf.blit(self.img, (self.size[0] // 2 - self.img.get_rect().w // 2 , self.size[1] // 2 - self.img.get_rect().h // 2))
		coloring_surface = pygame.Surface(self.size)

		self.hovered = rect.collidepoint(pos)


		if self.hovered and self.enabled:
			
			if pygame.mouse.get_pressed()[0] == 1:
				self.clicked = True
				col = self.CLICKED_COL
				pygame.draw.rect(coloring_surface, (0, 0, 0), ((0,0), self.size))
				
				
 
			if pygame.mouse.get_pressed()[0] == 0 and not self.clicked:
				col = self.HOVER_COL
				pygame.draw.rect(coloring_surface, (100,100,100), ((0,0), self.size))
				


			if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
				action = True
				self.clicked = False
				col = self.ACTION_COL
				pygame.draw.rect(coloring_surface, (250,250,250), ((0,0), self.size))
		

		if False:
			#Create Border
			
			pygame.draw.rect(surf, col, pygame.Rect(0, 0, self.size[0] + 4, self.size[1] + 4))

		surf.blit(coloring_surface, (0,0), special_flags = BLEND_RGB_ADD)

		if not self.enabled:
			red_coloring = pygame.Surface(self.size)
			pygame.draw.rect(red_coloring, (255, 0, 0), ((0,0), (self.size)))
			red_coloring.set_colorkey((0,0,0))
			surf.blit(red_coloring, (0,0), special_flags = BLEND_RGB_ADD)

		screen.blit(surf, (self.x, self.y))
		return action

class Wave_manager():
	SPAWN_COOLDOWN = 1000
	WAVE_DELAY = 3000
	
	def __init__(self, balloon_group):
		self.balloon_group = balloon_group
		self.last_spawn = 0
		self.wave = 1
		self.spawn_cooldown_reduction = 0
		self.spawned = 0
		self.wave_spawn = 10
		self.difficulty = 1
		self.wave_data = plibrary.get_wave_data()
		self.last_wave = -self.WAVE_DELAY
		self.endofwave = False
		self.balloon_type_idx = 0
		self.counter = 0
		
		

	def update(self):
		if self.wave < len(self.wave_data):
			if len(self.balloon_group) == 0 and self.endofwave:
				self.wave += 1
				self.spawn_cooldown_reduction = plibrary.mylerp(0, 1000, plibrary.myalerp(0, 60, self.wave))
				self.last_wave = pygame.time.get_ticks()
				self.balloon_type_idx = 0
				self.endofwave = False
				

			spawn_timer = pygame.time.get_ticks() - self.last_spawn > (self.SPAWN_COOLDOWN - self.spawn_cooldown_reduction)
			wave_timer = pygame.time.get_ticks() - self.last_wave > self.WAVE_DELAY

			if not wave_timer:
				draw_text("Wave Complete", font_60, WHITE, int(300 * scale), int(scale * 300))

			if self.wave_data:
				if spawn_timer and wave_timer and not self.endofwave:
								
					self.balloon_group.add(entities.Balloon(spawn[0], spawn[1], self.balloon_type_idx + 1, nodes, path_distance, self.wave_data[self.wave][self.balloon_type_idx][1], camo_img))
					self.last_spawn = pygame.time.get_ticks()
					
					self.counter += 1
					if self.counter >= self.wave_data[self.wave][self.balloon_type_idx][0]:
						self.counter = 0
						self.balloon_type_idx += 1

					if self.balloon_type_idx >= len(self.wave_data[self.wave]):
						self.endofwave = True
		else:
			print('Level Complete')
			
			

pathway_sheet = SpriteSheet(pathway_sprite_sheet, (10, 10))

for i in range(int(pathway_sprite_sheet.get_width() / pathway_sheet.size[0])):
	pathway_imgs.append(pathway_sheet.get_sprite(i, 0, scale))

balloon_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
particle_group = []

def create_tower_button_img(tower_img):
	img = pygame.Surface((int(48 * scale), int(48 * scale)))
	img.blit(button_background, (0,0))
	img.blit(tower_imgs[tower_img][0], (0,0))
	return img
def create_icon_button_img(icon_img):
	img = pygame.Surface((int(48 * scale), int(48 * scale)))
	img.blit(button_background, (0,0))
	img.blit(icon_imgs[icon_img], (0,0))
	return img



button_upgrade_img = pygame.image.load('Images/Button_Upgrade.png').convert()
button_upgrade_img = pygame.transform.scale(button_upgrade_img, (int(button_upgrade_img.get_width() * scale), int(button_upgrade_img.get_height() * scale))).convert_alpha()
button_sell_img = pygame.image.load('Images/Button_Sell.png').convert()
button_sell_img = pygame.transform.scale(button_sell_img, (int(button_sell_img.get_width() * scale), int(button_sell_img.get_height() * scale))).convert_alpha()

health = 100 
money = 250
score = 0 
wm = Wave_manager(balloon_group)
		
def show_info():
	draw_text(f'Wave : {wm.wave}', font, TEXT_COL, int(750 * scale), int(20 * scale))
	draw_text(f'Health : {health}', font, TEXT_COL, int(750 * scale), int(70 * scale))
	draw_text(f'Money : {money}', font, TEXT_COL, int(750 * scale), int(120 * scale))



pygame.display.set_icon(balloon_imgs[0])
clock = pygame.time.Clock()


def main():
	run = True
	global money, score, wm, health, pathway

	#Tower Buttons
	tower_buttons = [Button(int(20 * scale), int(620 * scale), (25, 25), img = create_tower_button_img(0)),
		Button(int(70 * scale), int(620 * scale), (25, 25), img = create_tower_button_img(1)),
		Button(int(120 * scale), int(620 * scale), (25, 25), img = create_tower_button_img(2)),
		Button(int(170 * scale), int(620 * scale), (25, 25), img = create_tower_button_img(3)),
		Button(int(220 * scale), int(620 * scale), (25, 25), img = create_tower_button_img(4))]

	#Upgrade / Sell Button
	upgrade_button = Button(int(650 * scale), int(425 * scale), (200, 50), img = button_upgrade_img)
	sell_button = Button(int(650 * scale), int(525 * scale), (200, 50), img = button_sell_img)

	tower_to_place = None
	tower_selected = None
	clicked_at = None

	pathway_display = library.create_array_to_display_pathway(nodes, pathway_imgs)

	while run:
		clock.tick(60)
		screen.fill(GROUND)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		#Draw Pathway
		for pic in pathway_display:
			screen.blit(pic[0], pic[1])			

		wm.update()

		pos = pygame.mouse.get_pos()
		
		if pygame.mouse.get_pressed()[0] and pos[0] < int(600 * scale) and pos[1] < int(600 * scale):	
			clicked = False	
			for tower in tower_group:
				if tower.rect.collidepoint(pos):
					tower_selected = tower
					tower.selected = True
					clicked = True
				else:
					tower.selected = False

			if not clicked:
				tower_selected = None

		if tower_selected:
			tower_selected.draw(screen)

		for t in tower_group:
			if not t.selected:
				t.draw(screen)

		for b in balloon_group:
			b.draw(screen)
			#print((id(b.camo)))
		bullet_group.draw(screen)

		for particle in particle_group:
			particle.draw(screen)

		for b in balloon_group:
			health = b.update(health, particle_group)


		tower_group.update(balloon_group, bullet_group)

		for bullet in bullet_group:
			money, score = bullet.update(balloon_group, money, score)

		for i, particle in reversed(list(enumerate(particle_group))):
			if particle.enabled:
				particle.update()
			else:
				particle_group.remove(particle)

		#Draw UI

		pygame.draw.rect(screen, PANEL, (int(600 * scale), int(0 * scale), int(300 * scale), int(600 * scale)))
		pygame.draw.rect(screen, PANEL, (int(0 * scale), int(600 * scale), int(600 * scale), int(200 * scale)))
		pygame.draw.rect(screen, BORDER, (int(600 * scale), int(0 * scale), int(300 * scale), int(600 * scale)), 10)
		pygame.draw.rect(screen, BORDER, (int(0 * scale), int(600 * scale), int(600 * scale), int(200 * scale)), 10)
		show_info()

		if tower_selected:
			if upgrade_button.draw(screen):
				if money >= 100 and tower_selected.level < tower_selected.max_level:
					tower_selected.upgrade()
					money -= 100

			if sell_button.draw(screen):
				tower_selected.kill()
				money += 100
				tower_selected = None


		#draw tower at mouse
		if tower_to_place != None:
			pos = pygame.mouse.get_pos()
			size = (tower_imgs[tower_to_place][0].get_width(), tower_imgs[tower_to_place][0].get_height())
			img = pygame.Surface(size)
			img.blit(tower_imgs[tower_to_place][0], (0,0))
			img.set_colorkey((0,0,0))
			rect = pygame.Rect(((pos[0] - size[0] // 2, pos[1] - size[1] // 2)), (size))

			collide = False
			colliding_with_pathway = rect.collidelistall(pathway)
			tower_rects = []
			for t in tower_group:
				tower_rects.append(t.rect)

			colliding_with_towers = rect.collidelistall(tower_rects)

			if colliding_with_pathway or colliding_with_towers:
				red_coloring = pygame.Surface((tower_imgs[tower_to_place][0].get_width(), tower_imgs[tower_to_place][0].get_height()))
				pygame.draw.rect(red_coloring, (255, 0, 0), ((0,0), (tower_imgs[tower_to_place][0].get_width(), tower_imgs[tower_to_place][0].get_height())))
				red_coloring.set_colorkey((0,0,0))
				img.blit(red_coloring, (0,0), special_flags = BLEND_RGB_MULT)
			
			screen.blit(img, (pos[0] - size[0] // 2, pos[1] - size[1] // 2))
			if pygame.mouse.get_pressed()[0] and not colliding_with_pathway and not colliding_with_towers and pos[0] < int(600 * scale) and pos[0] > 0 and pos[1] > 0 and pos[1] < int(600 * scale): 
				tower_group.add(entities.Tower((pos[0] - size[0] // 2, pos[1] - size[1] // 2), tower_imgs[tower_to_place], bullet_imgs[tower_to_place], tower_ranges[tower_to_place], tower_attack_cooldown[tower_to_place], tower_can_see_camo[tower_to_place],tower_projectile_settings[tower_to_place]))
				money -= tower_costs[tower_to_place]
				tower_to_place = None 
				
			elif pygame.mouse.get_pressed()[2]:
				tower_to_place = None

		for i in range(len(tower_buttons)):
			if tower_buttons[i].draw(screen):
				if money > tower_costs[i]:
					tower_to_place = i

			if tower_buttons[i].hovered:
				draw_text(f'Price : {tower_costs[i]}', font, TEXT_COL, int(750 * scale), int(300 * scale))
		
			if money < tower_costs[i]:
				tower_buttons[i].enabled = False
			else:
				tower_buttons[i].enabled = True

		if money < 100:
			upgrade_button.enabled = False
		else:
			upgrade_button.enabled = True

		
		pygame.display.update()

def level_select():
	run = True

	while run:
		clock.tick(60)
		screen.fill(GROUND)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		pygame.display.update()


def settings_menu():
	run = True
	global scale, settings, music_volume, sfx_volume
	upscale_button = Button(int(200 * scale), int(300 * scale), (25, 25), img = pygame.image.load("Images/increment_up_icon.png"))
	downscale_button = Button(int(600 * scale), int(300 * scale), (25, 25), img = pygame.image.load("Images/decrement_up_icon.png"))
	upmusic_button = Button(int(200 * scale), int(400 * scale), (25, 25), img = pygame.image.load("Images/increment_up_icon.png"))
	downmusic_button = Button(int(600 * scale), int(400 * scale), (25, 25), img = pygame.image.load("Images/decrement_up_icon.png"))
	upsfx_button = Button(int(200 * scale), int(500 * scale), (25, 25), img = pygame.image.load("Images/increment_up_icon.png"))
	downsfx_button = Button(int(600 * scale), int(500 * scale), (25, 25), img = pygame.image.load("Images/decrement_up_icon.png"))
	save_button = Button(int(300 * scale), int(600 * scale), (25, 25), img = create_icon_button_img(0))

	while run:
		clock.tick(60)
		screen.fill(GROUND)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		if upscale_button.draw(screen):
			scale += 0.1
			if scale > 2:
				scale = 2

		if downscale_button.draw(screen):
			scale -= 0.1
			if scale < .5:
				scale = .5

		if upmusic_button.draw(screen):
			music_volume += 0.1
			if music_volume > 1:
				music_volume = 1

		if downmusic_button.draw(screen):
			music_volume -= 0.1
			if music_volume < 0:
				music_volume = 0

		if upsfx_button.draw(screen):
			sfx_volume += 0.1
			if sfx_volume > 1:
				sfx_volume = 1

		if downsfx_button.draw(screen):
			sfx_volume -= 0.1
			if sfx_volume < 0:
				sfx_volume = 0

		if save_button.draw(screen):

			pygame.mixer.music.set_volume(music_volume)
			settings = [scale, music_volume, sfx_volume]
			with open( f'settings_data.p', 'wb') as file:
				pickle.dump(settings, file)


		draw_text(f'scale : {scale}', font, WHITE, int(400 * scale), int(300 * scale))
		draw_text(f'Music Volume : {music_volume}', font, WHITE, int(400 * scale), int(400 * scale))
		draw_text(f'SFX Volume : {sfx_volume}', font, WHITE, int(400 * scale), int(500 * scale))

		pygame.display.update()


def main_menu():
	run = True

	play_button = Button(int(300 * scale), int(300 * scale), (25, 25), img = create_icon_button_img(0))
	level_select_button = Button(int(300 * scale), int(350 * scale), (25, 25), img = create_icon_button_img(2))
	settings_button = Button(int(300 * scale), int(400 * scale), (25, 25), img = create_icon_button_img(1))
	quit_button = Button(int(300 * scale), int(450 * scale), (25, 25), img = create_icon_button_img(3))
	music_name = 'Mysterious'
	pygame.mixer.music.load(os.path.join("Music", f"JDB - {music_name}.ogg"))


	pygame.mixer.music.play(-1)

	while run:
		clock.tick(60)
		screen.fill(GROUND)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		if play_button.draw(screen):
			main()

		if level_select_button.draw(screen):
			level_select()

		if settings_button.draw(screen):
			settings_menu()

		if quit_button.draw(screen):
			run = False

		pygame.display.update()


if __name__ == '__main__':
	main_menu()
