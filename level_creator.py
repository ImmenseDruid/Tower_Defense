import pickle, os, pygame, plibrary, library
from pygame.locals import *


map_data =  [[int(600), int(50)], [int(600 - 100), int(50)], [int(600 - 500), int(50)], [int(600 - 500), int(200)], [int(600 - 450), int(200)],
 [int(600 - 450), int(100)], [int(600 - 100), int(100)], [int(600 - 100), int(400)], [int(600 - 400), int(400)],
 [int(600 - 400), int(500)], [int(600 - 0), int(500)], [int(600 + 50), int(500)]]

level = 1

with open(os.path.join('Levels', f'map_{level}_data.p'), 'wb') as file:
 	pickle.dump(map_data, file)


plibrary.create_wave_data(level)
