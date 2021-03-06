import pickle
import os

def sqrt(x):
	res = 0
	bit = 1 << 30

	while(bit > x):
		bit >>= 2

	while bit != 0:
		if x >= res + bit:
			x -= res + bit
			res = (res >> 1) + bit
		else:
			res >>= 1
		bit >>= 2

	return res

def pythag(x, y):
	return sqrt(x * x + y * y)

def mylerp(x, y, z):
	return (x * (1-z) + y * (z))

def limit(x, y, z):
	if z < y:
		z = y 
	if z > x:
		z = x 

	return x
def myalerp(x,y,z):
	x = limit(x, y, z)
	print(f'dummb {x} and dumber {z}')
	a = z - x
	print(a)
	b = x + y
	print(b)
	return a / b



def create_pathway(nodes, pathway, scale):	
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

			pathway.append((x,y,w,h))
	return pathway

def create_array_to_display_pathway(nodes, pathway_imgs):
	pictures = []
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
							pictures.append((pathway_imgs[1], (x - pathway_imgs[0].get_width() // 2, y - pathway_imgs[0].get_height() // 2)))
							y += pathway_imgs[0].get_height()
					else:
						x += pathway_imgs[0].get_width()
						x_i = x
						while x < w + x_i - pathway_imgs[0].get_width():
							pictures.append((pathway_imgs[0], (x - pathway_imgs[0].get_width() // 2, y - pathway_imgs[0].get_height() // 2)))
							x += pathway_imgs[0].get_width()

					if i < len(nodes) - 2:
						current_node = nodes[i]
						next_node = nodes[i + 1]
						look_ahead_node = nodes[i + 2]

						if current_node[0] < next_node[0]:
							if next_node[0] < look_ahead_node[0]:
								#continue straight	
								pictures.append((pathway_imgs[0], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[1] < look_ahead_node[1]:
								#left -> down
								pictures.append((pathway_imgs[2], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[1] > look_ahead_node[1]:
								#left -> up
								pictures.append((pathway_imgs[3], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))

						elif current_node[0] > next_node[0]:
							if next_node[0] > look_ahead_node[0]:
								#continue straight
								pictures.append((pathway_imgs[0], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[1] < look_ahead_node[1]:
								#right -> down
								pictures.append((pathway_imgs[5], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[1] > look_ahead_node[1]:
								#right -> up
								pictures.append((pathway_imgs[4], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))

						
						if current_node[1] < next_node[1]:
							if next_node[1] < look_ahead_node[1]:
								pictures.append((pathway_imgs[1], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[0] < look_ahead_node[0]:
								#down -> Right
								pictures.append((pathway_imgs[4], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[0] > look_ahead_node[0]:
								#down -> left
								pictures.append((pathway_imgs[3], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
						elif current_node[1] > next_node[1]:
							if next_node[1] > look_ahead_node[1]:
								pictures.append((pathway_imgs[1], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[0] < look_ahead_node[0]:
								#up -> Right
								pictures.append((pathway_imgs[5], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))
							if next_node[0] > look_ahead_node[0]:
								#up -> left
								pictures.append((pathway_imgs[2], (next_node[0] - pathway_imgs[0].get_width() // 2, next_node[1] - pathway_imgs[0].get_height() // 2)))

	return pictures

def determine_pricing(ranges, attack_speed, see_camo, projectile_settings):
	costs = []
	lim = len(ranges)
	for i in range(lim):
		c = ranges[i] * 0.3
		c -= attack_speed[i] * 0.022
		c += int(see_camo[i]) * 10
		c += projectile_settings[i][0] // 2
		c += projectile_settings[i][1]
		costs.append(c)

	return costs

def calculate_path_distance(nodes):
	distance = 0 
	prev_node = None
	for node in nodes:
		if prev_node:
			dx = node[0] - prev_node[0]
			dy = node[1] - prev_node[1]

			distance += pythag(dx, dy)
		
		prev_node = node

	return distance

def create_wave_data(level):
	waves = []

	for wave in range(30):
		waves.append([])
		for balloon_type in range(5):
			amount = wave * wave
			camo = False if not wave % 10 == 9 else True
			waves[wave].append([amount, camo])
			

	with open(os.path.join('waves', f'waves_map_{level}_data.p'), 'wb') as file:
		pickle.dump(waves, file)

def get_wave_data():
	waves = []
	with open(os.path.join('waves', f'waves_map_0_data.p'), 'rb') as file:
		waves = pickle.load(file)

	return waves

def scale_array(arr, scale):
	for i in range(len(n)):
		n[i] = int(n[i] * scale)

	return n


def generate_to_infinity():
	waves = []
	# 300 ~= INF if we get this far you have too much time on your hands...
	# after a few seconds of googling and determined that 999 ~= INF
	for wave in range(999):
		waves.append([])
		for balloon_type in range(5):
			amount = wave * wave
			camo = False if not wave % 5 == 0 else True
			waves[wave].append([amount, camo])

	return waves