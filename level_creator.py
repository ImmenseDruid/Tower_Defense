import pickle, os, pygame, plibrary, library
from pygame.locals import *


path_data =  [[int(600), int(50)], [int(600 - 100), int(50)], [int(600 - 500), int(50)], [int(600 - 500), int(200)], [int(600 - 450), int(200)],
 [int(600 - 450), int(100)], [int(600 - 100), int(100)], [int(600 - 100), int(400)], [int(600 - 400), int(400)],
 [int(600 - 400), int(500)], [int(600 - 0), int(500)], [int(600 + 50), int(500)]]


pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Courier New', 30)
font_60 = pygame.font.SysFont('Courier New', 60)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))

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

def create_level_data(level, data):
	with open(os.path.join('Levels', f'map_{level}_data.p'), 'wb') as file:
		pickle.dump(data, file)

	plibrary.create_wave_data(level)

def load_map_data(level):
	data = []
	with open(os.path.join('Levels', f'map_{level}_data.p'), 'rb') as file:
		data = pickle.load(file)
	return data

def load_wave_data(level):
	data = []
	with open(os.path.join('waves', f'waves_map_{level}_data.p'), 'rb') as file:
		data = pickle.load(file)
	return data

def load_level_data(level):
	wave_data = load_wave_data(level)
	map_data = load_map_data(level)

	return wave_data, map_data

def main():
	run = True

	width = 900
	height = 800
	screen = pygame.display.set_mode((width, height))
	current_level = 3
	selected_node = None
	m1_clicked = False

	found = False
	for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Levels')):
		if f'map_{current_level}_data.p' in files:
			found = True
	if found:
		load_map_data(current_level)
	else:
		create_level_data(current_level, path_data)

	wave_data, map_data = load_level_data(current_level)

	save_img = pygame.Surface((100, 50))
	save_img.fill((0,0,0))
	save_img.blit(font.render("Save", True, (255,255,255)), (0,0))
	save_button = Button(650, 650, (100, 50), img = save_img)

	while run:
		screen.fill((100, 100, 100))

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			if event.type == MOUSEBUTTONDOWN:				
				if event.button == 1:
					pos = event.pos

					for i, node in enumerate(map_data):
						if library.pythag(abs(pos[0] - node[0]), abs(pos[1] - node[1])) < 20:
							selected_node = i
							break
			if event.type == MOUSEBUTTONUP:				
				if event.button == 1:
					selected_node = None


		if selected_node is not None:
			pos = pygame.mouse.get_pos()
			
			if pos[0] > 600 or pos[1] > 600:
				selected_node = None
			else:
				map_data[i] = list(pygame.mouse.get_pos())
	

		for node in map_data:
			pygame.draw.circle(screen, (0,0,0), node, 20)

		pygame.draw.lines(screen, (0,0,0), False, map_data)

		if save_button.draw(screen):
			for i in range(len(map_data)):
				map_data[i] = list(map_data[i])

			create_level_data(current_level, map_data)

		pygame.display.update()




if __name__ == "__main__":
	main()
