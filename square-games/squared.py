#!/usr/bin/env python

import pygame
from pygame import *
import math
import sys
import random

DISPLAY = (320, 320)
BGCOLOUR = Color("#000000")
PLAYERCOLOUR = Color("#0098FF")
PLATFORMCOLOUR = Color("#DDDDDD")
FINISHCOLOUR = Color("#00AB14")
PAINTEDCOLOUR = Color("#85E7FF")

# sound
mixer.init()
blipsound = mixer.Sound("blip.wav")

def main():
	pygame.init()
	screen = display.set_mode(DISPLAY)
	display.set_caption("squared")
	timer = time.Clock()

	# player directions
	up = down = left = right = False

	# background
	bg = Surface((32, 32))
	bg.convert()
	bg.fill(BGCOLOUR)

	# entities
	entities = pygame.sprite.Group()
	player = Player(32, 32)
	platforms = []

	# x and y for level building
	x = y = 0

	# build level
	level = [
	"OOOOOOOOOO",
	"O        O",
	"OO       O",
	"O O      O",
	"O        O",
	"OOOOO  OOO",
	"O        O",
	"O        O",
	"OX       O",
	"OOOOOOOOOO",]
	for row in level:
		for column in row:
			if column == "O":
				block = Platform(x, y)
				platforms.append(block)
				entities.add(block)
			elif column == "X":
				xblock = FinishBlock(x, y)
				platforms.append(xblock)
				entities.add(xblock)
			x += 32
		y += 32
		x = 0
	# register player
	entities.add(player)

	# game loop
	while True:
		timer.tick(60)
		# keypress and quit
		for e in pygame.event.get():
			if e.type == QUIT: sys.exit(0)
			if e.type == KEYDOWN:
				if e.key == K_ESCAPE: sys.exit(0)
				elif e.key == K_SPACE:
					up = True
				elif e.key == K_DOWN:
					down = True
				elif e.key == K_LEFT:
					left = True
				elif e.key == K_RIGHT:
					right = True				
			if e.type == KEYUP:
				if e.key == K_SPACE:
					up = False
				elif e.key == K_DOWN:
					down = False
				elif e.key == K_LEFT:
					left = False
				elif e.key == K_RIGHT:
					right = False
		# draw background
		for y in range(10):
			for x in range(10):
				screen.blit(bg, (x*32, y*32))
		# draw other things, update player
		player.update(up, down, left, right, platforms)
		entities.draw(screen)
		# update display
		pygame.display.flip()

class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Player(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		# velocity
		self.xvel = 0
		self.yvel = 0
		# is player on ground?
		self.on_ground = False
		# shape / colour
		self.image = Surface((32, 32))
		self.image.convert()
		self.image.fill(PLAYERCOLOUR)
		self.rect = Rect(x, y, 32, 32)
	# motion and collision updating
	def update(self, up, down, left, right, platforms):
		if up:
			# check for groundedness
			if self.on_ground: self.yvel -= 7
		if down:
			pass
		if left:
			self.xvel = -5
		if right:
			self.xvel = 5
		if not self.on_ground:
			# accelerate if in air
			# (realistic gravity)
			self.yvel += 0.3
			# terminal velocity
			if self.yvel > 30: self.yvel = 30
		if not(left or right):
			self.xvel = 0
		# move x, collide x
		self.rect.left += self.xvel
		self.collide(self.xvel, 0, platforms)
		# move y, collide y, acknowledge non-groundedness
		self.rect.top += self.yvel
		self.on_ground = False
		self.collide(0, self.yvel, platforms)
	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if sprite.collide_rect(self, p):
				# if collision with xblock
				if isinstance(p, FinishBlock):
					sys.exit(0)
				if xvel > 0: self.rect.right = p.rect.left
				if xvel < 0: self.rect.left = p.rect.right
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.on_ground = True
					self.yvel = 0
				if yvel < 0: self.rect.top = p.rect.bottom
				# experimental
				if p.rect.top == self.rect.bottom and not p.painted:
					p.paint()
					p.painted = True
					blipsound.play()


class Platform(Entity):
	def __init__(self, x, y, painted=False):
		# experiment
		self.painted = False

		Entity.__init__(self)
		self.image = Surface((32, 32))
		self.image.convert()
		self.image.fill(PLATFORMCOLOUR)
		self.rect = Rect(x, y, 32, 32)
	# experiment
	def paint(self):
		self.image.fill(PAINTEDCOLOUR)

class FinishBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(FINISHCOLOUR)

if __name__ == '__main__':
	main()