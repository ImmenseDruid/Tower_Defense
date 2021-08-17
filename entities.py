import pygame, pickle, math
import random

def limit(x, y, z):
	if x < y:
		x = y 
	if x > z:
		x = z 
	return x

def pythag(dist1, dist2):
	return  math.sqrt(dist1 * dist1 + dist2 * dist2)

def health_to_speed(x):
	if x < 1:
		x = 1
	return x 

class Particle():
	def __init__(self, pos, v, img = None, life_time = 300):
		self.pos = pos
		self.v = v
		if img:
			self.image = img
		else:
			self.image = pygame.Surface((10, 10))
			self.image.fill((255, 255, 255))

		self.size = (self.image.get_width(), self.image.get_height())
		self.rect = pygame.Rect(self.pos, self.size)
		self.life_time = life_time
		self.time_created = pygame.time.get_ticks()
		self.enabled = True

	def update(self):
		self.pos[0] += self.v[0]
		self.pos[1] += self.v[1]

		if pygame.time.get_ticks() - self.time_created > self.life_time:
			self.enabled = False

		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

	def draw(self, screen):
		screen.blit(self.image, self.pos)




class Entity(pygame.sprite.Sprite):
	def __init__(self, x, y, img = None, size = (50, 50)):
		pygame.sprite.Sprite.__init__(self)
		
		if not img:
			img = pygame.Surface((50, 50))
			pygame.draw.rect(img, (255, 0, 0), ((0, 0), size))

		self.x = x
		self.y = y
		self.image = img

		self.size = (self.image.get_width(), self.image.get_height())
		self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
		self.enabled = True


	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))


class Tower(Entity):
	def __init__(self, pos, imgs = None, bullet_img = None, tower_range = 300, attack_speed = 1500, tower_can_see_camo = False, projectile_settings = None):
		x = pos[0]
		y = pos[1]
		if not imgs:
			size = (50, 50)
			img = pygame.Surface(size)
			pygame.draw.rect(img, (0, 255, 0), ((0, 0), size))
			imgs = [img, img, img]
		elif len(imgs) < 3:
			imgs = [imgs[0], imgs[0], imgs[0]]

		self.bullet_img = bullet_img
		self.fire_cooldown = attack_speed
		self.fired_last = 0
		self.target_aquired = False
		self.range = tower_range
		self.selected = False
		self.level = 1 
		self.max_level = len(imgs)
		self.imgs = imgs
		self.projectile_settings = projectile_settings
		self.can_see_camo = tower_can_see_camo
		img = self.imgs[self.level - 1]
		super().__init__(x, y, img)

	def update(self, enemy_group, bullet_group):
		self.target_aquired = False
		max_percent = 0
		target = None
		for e in enemy_group:
			target_x, target_y = e.rect.center
			if (e.camo and self.can_see_camo) or not e.camo:
				if pythag((target_x - self.rect.center[0]), (target_y - self.rect.center[1])) < self.range + (self.range // 10 * (self.level - 1)):
					if e.percent > max_percent:
						max_percent = e.percent
						target = e
						self.target_aquired = True
		
		if self.target_aquired:		
			target_x, target_y = target.rect.center
		


		if self.target_aquired and pygame.time.get_ticks() - self.fired_last > self.fire_cooldown - (0.25 * self.fire_cooldown * (self.level - 1)):
			pos = (target_x, target_y)

			x_dist = pos[0] - self.rect.center[0]
			y_dist = -(pos[1] - self.rect.center[1])

			self.angle = math.degrees(math.atan2(y_dist, x_dist))

			
			bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, self.bullet_img, self.projectile_settings[0])
			bullet_group.add(bullet)

			self.fired_last = pygame.time.get_ticks()

	def upgrade(self):
		self.level += 1 
		self.level = limit(self.level, 1, self.max_level)
		self.image = self.imgs[self.level - 1]


	def draw(self, screen):
		if self.selected:
			range_visualization = pygame.Surface(((self.range + (self.range // 10 * (self.level - 1)) )* 2, (self.range + (self.range // 10 * (self.level - 1))) * 2))
			
			range_visualization.fill((255, 255, 255))
			pygame.draw.circle(range_visualization, (100, 100, 100),
			 ((self.range + (self.range // 10 * (self.level - 1))), (self.range + (self.range // 10 * (self.level - 1)))), (self.range + (self.range // 10 * (self.level - 1))))

			screen.blit(range_visualization, (self.rect.center[0] - (self.range + (self.range // 10 * (self.level - 1))), self.rect.center[1] - (self.range + (self.range // 10 * (self.level - 1)))),
			 special_flags = pygame.BLEND_RGB_MULT)

		super().draw(screen)


class Bullet(Entity):
	def __init__(self, x, y, angle, img = None, explosion_radius = 0, pierce = 0, slow_amount = 0):
		if not img:
			size = (25, 25)
			img = pygame.Surface(size)
			pygame.draw.rect(img, (0, 0, 255), ((0,0), size))
		self.pierce = pierce
		self.explosion_radius = explosion_radius
		self.slow_amount = slow_amount
		self.angle = math.radians(angle)
		self.speed = 10 
		self.dx = math.cos(self.angle) * self.speed
		self.dy = -math.sin(self.angle) * self.speed
		self.life_time = 2000
		self.start_life = pygame.time.get_ticks()
		super().__init__(x, y, img, img.get_size())
		self.rect.center = (self.x, self.y)

	def update(self, balloon_group, money, score):
		self.x += self.dx 
		self.y += self.dy 
		self.rect.center = (self.x, self.y)

		if not self.enabled:
			self.kill()

		collide_list = pygame.sprite.spritecollide(self, balloon_group, False)

		for balloon in collide_list:
			balloon.damage()
			balloon.slow(self.slow_amount)
			money += 1
			score += 1
			self.pierce -= 1
			if self.explosion_radius > 0:
				money, score = self.explode(balloon_group, money, score)
			if self.pierce <= 0:
				self.kill()

		if pygame.time.get_ticks() - self.start_life > self.life_time:
			self.kill()

		return money, score
	
	def explode(self, balloon_group, money, score):
		explosion = pygame.Rect(self.x - self.explosion_radius // 2, self.y - self.explosion_radius // 2, self.explosion_radius, self.explosion_radius)
		for balloon in balloon_group:
			if explosion.colliderect(balloon.rect):
				balloon.damage()
				money += 1
				score += 1
		self.kill()
		return money, score
		



class Balloon(Entity):

	ACCEPTABLE_RANGE = 1
	IMGS = None

	def __init__(self, x, y, health, path, path_dist, camo, camo_img):
		
		
		super().__init__(x, y, self.IMGS[health - 1])
		self.path = path
		self.target_idx = 0
		self.target = self.path[0]
		self.speed = health_to_speed(health)
		self.alive = True
		self.health = health
		self.rect.center = (self.x, self.y)
		self.particles = []
		self.dx = 0 
		self.dy = 0 
		self.path_dist = path_dist
		self.distance = 0
		self.percent = 0 
		self.camo = camo
		self.camo_img = camo_img
		
	def damage(self):
		self.health -= 1
		self.speed = health_to_speed(self.health)
		self.image = self.IMGS[limit(self.health - 1, 0, len(self.IMGS) - 1)]
		for i in range(10):
			self.particles.append(Particle([self.x, self.y], [random.random() * 2 - 1 + self.dx, random.random() * 2 - 1 + self.dy]))
		if self.health <= 0:
			self.alive = False

	def slow(self, amount):
		self.speed = health_to_speed(self.health - 2)
		


	def update(self, health, particle_group):
		if not self.alive:
			self.kill()

		if not self.enabled:			
			health -= self.health
			self.kill()

		for i, p in reversed(list(enumerate(self.particles))):
			particle_group.append(p)
			self.particles.remove(p)

		if self.enabled and self.alive:

			self.dx = (self.target[0] - self.x)
			self.dy = (self.target[1] - self.y)
			self.dx = limit(self.dx, -self.speed, self.speed)
			self.dy = limit(self.dy, -self.speed, self.speed)
			if abs(self.dx) < self.ACCEPTABLE_RANGE and abs(self.dy) < self.ACCEPTABLE_RANGE:
				self.target_idx += 1
				if self.target_idx >= len(self.path):
					self.enabled = False
					self.target_idx = len(self.path) - 1

				self.target = self.path[self.target_idx]

			self.x += self.dx 
			self.y += self.dy
			self.distance += abs(self.dx)
			self.percent = self.distance / self.path_dist
			self.rect.center = [self.x, self.y]

		return health	

	def draw(self, screen):
		screen.blit(self.image, self.rect.topleft)
		if self.camo:
			screen.blit(self.camo_img, self.rect.topleft)
		for p in self.particles:
			p.draw(screen)

	

