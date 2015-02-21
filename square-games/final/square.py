import pygame
import math
import sys
import levels
from pygame import *

# resolution constant
DISPLAY = (800, 640)
# colour constants
BGCOLOUR = Color("#00404C")
WALLCOLOUR = Color("#DDDDDD")
FINISHCOLOUR = Color("#DB6A24")
PARCOLOUR = Color("#13B200")
SPIKECOLOUR = Color("#FF0000")
JUMPCOLOUR = Color("#5587B6")

# level properties
current_level = 1
current_par = 0
jump_count = 0

mixer.init()
# sounds
jumpsound = mixer.Sound("jump.wav")
finishsound = mixer.Sound("finish.wav")
highsound = mixer.Sound("high.wav")
# music
music = mixer.music.load("track.wav")
mixer.music.play(-1)

def main():
	pygame.init()
	screen = display.set_mode(DISPLAY)
	display.set_caption("Squares Game")
	timer = time.Clock()

	# direction/velocity variables
	up = down = left = right = False
	bg = Surface((32, 32))
	bg.convert()
	bg.fill(BGCOLOUR)
	entities = pygame.sprite.Group()
	player = Player(32, 32, Color("#FEFF00"))
	platforms = []

	x = y = 0

	# build level
	if current_level == 1:
		scan = levels.level1
		current_par = 0
		jump_count = 0
	elif current_level == 2:
		scan = levels.level2
		current_par = 1
		jump_count = 0
	elif current_level == 3:
		scan = levels.level3
		current_par = 2
		jump_count = 0
	elif current_level == 4:
		scan = levels.level4
		current_par = 2
		jump_count = 0
	elif current_level == 5:
		scan = levels.level5
		current_par = 6
		jump_count = 0
	elif current_level == 6:
		scan = levels.level6
		current_par = 5
		jump_count = 0
	elif current_level == 7:
		scan = levels.level7
		current_par = 1
		jump_count = 0
	else: print("you finished the game"); sys.exit(0)
	for row in scan:
		for column in row:
			if column == "O":
				oblock = Platform(x, y)
				platforms.append(oblock)
				entities.add(oblock)
			if column == "F":
				fblock = FinishBlock(x, y)
				platforms.append(fblock)
				entities.add(fblock)
			if column == "X":
				xblock = SpikeBlock(x, y)
				platforms.append(xblock)
				entities.add(xblock)
			if column == "J":
				jblock = JumpBlock(x, y)
				platforms.append(jblock)
				entities.add(jblock)
			x += 32
		y += 32
		x = 0

	entities.add(player)

	# game loop
	while True:
		timer.tick(60)
		# keypresses and quit management
		for e in pygame.event.get():
			if e.type == QUIT: sys.exit(0)
			if e.type == KEYDOWN:
				if e.key == K_ESCAPE: sys.exit(0)
				elif e.key == K_SPACE:
					up = True
					jump_count += 1
				elif e.key == K_LEFT:
					left = True
				elif e.key == K_DOWN:
					down = True
				elif e.key == K_RIGHT:
					right = True
				# restart key
				elif e.key == K_r:
					main()
			if e.type == KEYUP:
				if e.key == K_SPACE:
					up = False
				elif e.key == K_LEFT:
					left = False
				elif e.key == K_DOWN:
					down = False
				elif e.key == K_RIGHT:
					right = False
		# draw bg
		for y in range(20):
			for x in range(25):
				screen.blit(bg, (x * 32, y * 32))
		# draw other things, update player
		player.update(up, down, left, right, platforms)
		entities.draw(screen)
		# update window title
		display.set_caption("audodydactism | Par: " + str(current_par) + " | Jumps: " + str(jump_count))
		# if player is on or under par, make xblock green
		if jump_count <= current_par:
			fblock.image.fill(PARCOLOUR)
		else:
			fblock.image.fill(FINISHCOLOUR)
		# update display
		pygame.display.flip()

# most drawn types will extend this
class Entity(pygame.sprite.Sprite):
	""" Entities are pygame sprites, hand tailored for the game. """
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Player(Entity):
	def __init__(self, x, y, color):
		Entity.__init__(self)
		# velocity
		self.xvel = 0
		self.yvel = 0
		# size
		self.x = x
		self.y = y
		# colour
		self.color = color

		self.on_ground = False
		self.high_jump = False
		self.image = Surface((32, 32))
		self.image.convert()
		self.image.fill(color)
		self.rect = Rect(x, y, 32, 32)

	def update(self, up, down, left, right, platforms):
		if up:
			# check for groundedness and high-jump
			if self.high_jump and self.on_ground:
				self.yvel -= 10
				self.high_jump = False
				highsound.play()
			if self.on_ground and not self.high_jump:
				self.yvel -= 7
				jumpsound.play()
		if down:
			# player doesn't fly, this isn't currently needed
			pass
		if left:
			self.xvel = -5
		if right:
			self.xvel = 5
		if not self.on_ground:
			# accelerate if in air
			self.yvel += 0.3
			# terminal velocity
			if self.yvel > 30: self.yvel = 30
		if not(left or right):
			# keep still
			self.xvel = 0
		# move-collide x
		self.rect.left += self.xvel
		self.collide(self.xvel, 0, platforms)
		# move-manage-collide y
		self.rect.top += self.yvel
		self.on_ground = False
		self.collide(0, self.yvel, platforms)

	def collide(self, xvel, yvel, platforms):
		global finishsound
		global current_level
		for p in platforms:
			if sprite.collide_rect(self, p):
				# quit game if the collision is with an exit block
				if isinstance(p, FinishBlock):
					finishsound.play()
					current_level += 1
					main()
				# restart if collision is with spike
				if isinstance(p, SpikeBlock):
					finishsound.play()
					main()
				# jump higher if collision is with jump block
				if isinstance(p, JumpBlock):
					self.high_jump = True
				if xvel > 0: self.rect.right = p.rect.left
				if xvel < 0: self.rect.left = p.rect.right
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.on_ground = True
					self.yvel = 0
				if yvel < 0: self.rect.top = p.rect.bottom

class Platform(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = Surface((32, 32))
		self.image.convert()
		self.image.fill(WALLCOLOUR)
		self.rect = Rect(x, y, 32, 32)

class FinishBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(FINISHCOLOUR)

class SpikeBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(SPIKECOLOUR)

class JumpBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(JUMPCOLOUR)

if __name__ == '__main__':
	main()