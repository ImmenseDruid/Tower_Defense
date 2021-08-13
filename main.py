import pygame
import entities
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

scale = 1.5
width = int(900 * scale)
height = int(800 * scale)

pygame.init()
pygame.font.init()



screen = pygame.display.set_mode((width , height))
clock = pygame.time.Clock()






#Tower Costs

tower_costs = [55, 100]
tower_ranges = [250, 350]
tower_attack_cooldown = [1000, 2000]
#projectile settings per tower [explosion radius, pierce]
tower_projectile_settings = [[0, 2], [100, 0]]


#Images

button_background = pygame.image.load('Images/ButtonBackground.png').convert()
button_background = pygame.transform.scale(button_background, (int(button_background.get_width() * scale), int(button_background.get_height() * scale))).convert_alpha()

pathway_sprite_sheet = pygame.image.load('Images/Pathways.png').convert()
pathway_imgs = []

bullet_1_img = pygame.image.load('Images/Bullet_1.png').convert_alpha()
bullet_1_img.set_colorkey((0,0,0))
bullet_2_img = pygame.image.load('Images/Bullet_2.png').convert_alpha()
bullet_2_img = pygame.transform.scale(bullet_2_img, (8, 8))
bullet_2_img.set_colorkey((0,0,0))

balloon_base_img = pygame.image.load('Images/Balloon_1.png').convert_alpha()

nodes = [[int(0 * scale), int(50 * scale)], [int(100 * scale), int(50 * scale)], [int(500 * scale), int(50 * scale)], [int(500 * scale), int(200 * scale)], [int(450 * scale), int(200 * scale)],
 [int(450 * scale), int(100 * scale)], [int(100 * scale), int(100 * scale)], [int(100 * scale), int(400 * scale)], [int(400 * scale), int(400 * scale)],
 [int(400 * scale), int(500 * scale)], [int(0 * scale), int(500 * scale)], [int(-50 * scale), int(500 * scale)]]
pathway = []

for i in range(len(nodes)):
	if i < len(nodes) - 1:
		x = 0
		y = 0
		if nodes[i][0] < nodes[i + 1][0]:
			x = nodes[i][0]
		else:
			x = nodes[i + 1][0]
		if nodes[i][1] < nodes[i + 1][1]:
			y = nodes[i][1]
		else:
			y = nodes[i + 1][1]
		w = abs(nodes[i][0] - nodes[i + 1][0])
		h = abs(nodes[i][1] - nodes[i + 1][1])

		if w < h:
			w += int(20 * scale)
			x -= int(10 * scale)
		else:
			h += int(20 * scale)
			y -= int(10 * scale)

		pathway.append(pygame.Rect((x, y), (w, h)))

spawn = [int(-10 * scale), int(50 * scale)]


font = pygame.font.SysFont('Times New Roman', 30)
font_60 = pygame.font.SysFont('Times New Roman', 60)


tower_imgs = [[pygame.image.load('Images/Tower1.png').convert_alpha(), pygame.image.load('Images/Tower1_upgrade.png').convert_alpha(), pygame.image.load('Images/Tower1_upgrade_2.png').convert_alpha()],
 [pygame.image.load('Images/Tower_2_no_cape.png').convert_alpha(), pygame.image.load('Images/Tower_2_no_hat.png').convert_alpha(), pygame.image.load('Images/Tower_2.png').convert_alpha()]]
bullet_imgs = [bullet_1_img, bullet_2_img]
balloon_imgs = [pygame.image.load('Images/Balloon_1.png').convert_alpha(), pygame.image.load('Images/Balloon_2.png').convert_alpha(), pygame.image.load('Images/Balloon_3.png').convert_alpha(), pygame.image.load('Images/Balloon_4.png').convert_alpha()]

for i in range(len(tower_imgs)):
	for j in range(len(tower_imgs[i])):
		tower_imgs[i][j] = pygame.transform.scale(tower_imgs[i][j], (int(tower_imgs[i][j].get_width() * scale), int(tower_imgs[i][j].get_height() * scale))).convert_alpha()

for i in range(len(bullet_imgs)):
	bullet_imgs[i] = pygame.transform.scale(bullet_imgs[i], (int(bullet_imgs[i].get_width() * scale), int(bullet_imgs[i].get_height() * scale))).convert_alpha()

for i in range(len(balloon_imgs)):
	balloon_imgs[i] = pygame.transform.scale(balloon_imgs[i], (int(balloon_imgs[i].get_width() * scale), int(balloon_imgs[i].get_height() * scale))).convert_alpha()


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
		if rect.collidepoint(pos) and self.enabled:

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

		self.spawned = 0
		self.wave_spawn = 10
		self.difficulty = 1

		self.last_wave = -self.WAVE_DELAY
		

	def update(self):
		if len(self.balloon_group) == 0 and self.spawned >= self.wave_spawn:
			self.wave += 1

			self.wave_spawn = self.wave_spawn * 2
			self.spawned = 0
			self.last_wave = pygame.time.get_ticks()
			

		spawn_timer = pygame.time.get_ticks() - self.last_spawn > self.SPAWN_COOLDOWN
		wave_timer = pygame.time.get_ticks() - self.last_wave > self.WAVE_DELAY

		if not wave_timer:
			draw_text("Wave Complete", font_60, WHITE, int(300 * scale), int(scale * 300))

		if self.spawned < self.wave_spawn and spawn_timer and wave_timer:
			self.balloon_group.add(entities.Balloon(spawn[0], spawn[1], balloon_imgs, 4, nodes))
			self.spawned += 1
			self.last_spawn = pygame.time.get_ticks()
			

pathway_sheet = SpriteSheet(pathway_sprite_sheet, (10, 10))

for i in range(int(pathway_sprite_sheet.get_width() / pathway_sheet.size[0])):
	pathway_imgs.append(pathway_sheet.get_sprite(i, 0, scale))

print(len(pathway_imgs))


balloon_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
particle_group = []

button_0_img = pygame.Surface((int(48 * scale), int(48 * scale)))
button_0_img.blit(button_background, (0,0))
button_0_img.blit(tower_imgs[0][0], (0,0))


button_1_img = pygame.Surface((int(48 * scale), int(48 * scale)))
button_1_img.blit(button_background, (0,0))
button_1_img.blit(tower_imgs[1][0], (0,0))

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

def main():
	run = True
	global money, score, wm, health, pathway

	#Tower Buttons
	tower_0_button = Button(int(20 * scale), int(620 * scale), (25, 25), img = button_0_img)
	tower_1_button = Button(int(70 * scale), int(620 * scale), (25, 25), img = button_1_img)


	#Upgrade / Sell Button
	upgrade_button = Button(int(650 * scale), int(425 * scale), (200, 50), img = button_upgrade_img)
	sell_button = Button(int(650 * scale), int(525 * scale), (200, 50), img = button_sell_img)


	tower_to_place = None
	tower_selected = None
	clicked_at = None

	while run:
		clock.tick(60)
		screen.fill(GROUND)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		

		#Draw Pathway
		#for node in nodes:
		#	pygame.draw.circle(screen, WHITE, node, 10)
		
		for i in range(len(nodes)):
			if i < len(nodes) - 1:
				x = 0
				y = 0
				if nodes[i][0] < nodes[i + 1][0]:
					x = nodes[i][0]
				else:
					x = nodes[i + 1][0]
				if nodes[i][1] < nodes[i + 1][1]:
					y = nodes[i][1]
				else:
					y = nodes[i + 1][1]
				w = abs(nodes[i][0] - nodes[i + 1][0])
				h = abs(nodes[i][1] - nodes[i + 1][1])

				if w < h:
					y += pathway_imgs[0].get_height()				
					y_i = y
					while y < h + y_i - pathway_imgs[0].get_height():
						screen.blit(pathway_imgs[1], (x - pathway_imgs[0].get_width() // 2, y - pathway_imgs[0].get_height() // 2))
						y += pathway_imgs[0].get_height()
				else:
					x += pathway_imgs[0].get_width()
					x_i = x
					while x < w + x_i - pathway_imgs[0].get_width():
						screen.blit(pathway_imgs[0], (x - pathway_imgs[0].get_width() // 2, y - pathway_imgs[0].get_height() // 2))
						x += pathway_imgs[0].get_width()

				if i < len(nodes) - 2:
					current_node = nodes[i]
					next_node = nodes[i + 1]
					look_ahead_node = nodes[i + 2]

					if current_node[0] < next_node[0]:
						if next_node[0] < look_ahead_node[0]:
							#continue straight	
							screen.blit(pathway_imgs[0], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[1] < look_ahead_node[1]:
							#left -> down
							screen.blit(pathway_imgs[2], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[1] > look_ahead_node[1]:
							#left -> up
							screen.blit(pathway_imgs[3], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))

					elif current_node[0] > next_node[0]:
						if next_node[0] > look_ahead_node[0]:
							#continue straight
							screen.blit(pathway_imgs[0], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[1] < look_ahead_node[1]:
							#right -> down
							screen.blit(pathway_imgs[5], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[1] > look_ahead_node[1]:
							#right -> up
							screen.blit(pathway_imgs[4], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))

					
					if current_node[1] < next_node[1]:
						if next_node[1] < look_ahead_node[1]:
							screen.blit(pathway_imgs[1], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[0] < look_ahead_node[0]:
							#down -> Right
							screen.blit(pathway_imgs[4], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[0] > look_ahead_node[0]:
							#down -> left
							screen.blit(pathway_imgs[3], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
					elif current_node[1] > next_node[1]:
						if next_node[1] > look_ahead_node[1]:
							screen.blit(pathway_imgs[1], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[0] < look_ahead_node[0]:
							#up -> Right
							screen.blit(pathway_imgs[5], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))
						if next_node[0] > look_ahead_node[0]:
							#up -> left
							screen.blit(pathway_imgs[2], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2))

				#if nodes[i][0] < nodes[i + 1][0] and w > h:
				#	screen.blit(pathway_imgs[0], (x, y))
				#	

				#if nodes[i][0] > nodes[i + 1][0] and w > h:
				#	screen.blit(pathway_imgs[0], (x, y))
					




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
		bullet_group.draw(screen)

		for particle in particle_group:
			particle.draw(screen)


		for b in balloon_group:
			health = b.update(health, particle_group)


		#tower_group.draw(screen)

		
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
				if money >= 100:
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
				tower_group.add(entities.Tower((pos[0] - size[0] // 2, pos[1] - size[1] // 2), tower_imgs[tower_to_place], bullet_imgs[tower_to_place], tower_ranges[tower_to_place], tower_attack_cooldown[tower_to_place], tower_projectile_settings[tower_to_place]))
				money -= tower_costs[tower_to_place]
				tower_to_place = None 
				
			elif pygame.mouse.get_pressed()[2]:
				tower_to_place = None

		if tower_0_button.draw(screen):
			if money >= tower_costs[0]:
				tower_to_place = 0
		if tower_1_button.draw(screen):
			if money >= tower_costs[1]:
				tower_to_place = 1
	

		if money < tower_costs[0]:
			tower_0_button.enabled = False
		else:
			tower_0_button.enabled = True

		if money < tower_costs[1]:
			tower_1_button.enabled = False
		else:
			tower_1_button.enabled = True
			
		if money < 100:
			upgrade_button.enabled = False
		else:
			upgrade_button.enabled = True

		#for i in pathway_imgs:
		#	screen.blit(i, (10, 10))


		pygame.display.update()

if __name__ == '__main__':
	main()
