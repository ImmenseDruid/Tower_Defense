import pygame, os

from pygame.locals import *

width = 600
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Level Creator')
clock = pygame.time.Clock()


def load():
	with open(os.path.join('Levels', f'level{level}_data.p'), 'rb') as file:
		data = pickle.load(file)
		tiles.clear()
		for row in data:
			tiles.append(row)

def createNewLevel():
	
	save()


def save():
	with open(os.path.join('Levels', f'level{level}_data.p'), 'wb') as file:
		pickle.dump(tiles, file)


path = []

def main():

	found = False
	for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Levels')):
		if f'level{level}_data.p' in files:
			found = True
	if found:
		load()
	else:
		createNewLevel()

	run = True

	while run:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			if event.type == KEYDOWN:
				if event.key == ESCAPE:
					run = False


if __name__ == '__main__':
	main()
