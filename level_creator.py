import pickle, os, pygame, plibrary, library
from pygame.locals import *


map_0_data =  [[int(0), int(50)], [int(100), int(50)], [int(500), int(50)], [int(500), int(200)], [int(450), int(200)],
 [int(450), int(100)], [int(100), int(100)], [int(100), int(400)], [int(400), int(400)],
 [int(400), int(500)], [int(0), int(500)], [int(-50), int(500)]]



with open(os.path.join('Levels', f'map_0_data.p'), 'wb') as file:
 	pickle.dump(map_0_data, file)


plibrary.create_wave_data()
