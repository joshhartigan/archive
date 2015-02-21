import pygame
from pygame import *
import math
import sys

DISPLAY = (640, 640)
BGCOLOUR = Color("#5EEEFF")
PLAYERCOLOUR = Color("#000000")
PLATFORMCOLOUR = Color("#069400")
FINISHCOLOUR = Color("#FF8D00")

# block placement variables
bc_RED = Color("#9A2F2F")
bc_BLUE = Color("#1325CC") 
bc_YELLOW = Color("#B7C128")
bc_GREEN = Color("#005B05")
equipped = bc_RED
# sound
mixer.init()
blocksound = mixer.Sound("place.wav")

platforms = []
entities = pygame.sprite.Group()

def main():
	global equipped
	pygame.init()
	mixer.init()
	screen = display.set_mode(DISPLAY)
	display.set_caption("2d blocks")
	timer = time.Clock()

	# player directions
	up = down = left = right = False

	# background
	bg = Surface((32, 32))
	bg.convert()
	bg.fill(BGCOLOUR)

	# entities
	player = Player(32, 32)

	# x and y for level building
	x = y = 0

	# build level
	level = [
	"OOOOOOOOOOOOOOOOOOOO",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"O                  O",
	"OOOOOOOOOOOOOOOOOOOO",]
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
		# show equipped block in title
		if equipped == bc_RED:
			display.set_caption("2d blocks | Block Colour: Red")
		elif equipped == bc_BLUE:
			display.set_caption("2d blocks | Block Colour: Blue")
		elif equipped == bc_YELLOW:
			display.set_caption("2d blocks | Block Colour: Yellow")
		elif equipped == bc_GREEN:
			display.set_caption("2d blocks | Block Colour: Green")
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
				# block placement
				elif e.key == K_z:
					equipped = bc_RED
				elif e.key == K_x:
					equipped = bc_BLUE
				elif e.key == K_c:
					equipped = bc_YELLOW
				elif e.key == K_v:
					equipped = bc_GREEN
				elif e.key == K_a:
					player.place_block(equipped)
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
		for y in range(20):
			for x in range(20):
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
					print("you win.")
					sys.exit(0)
				if xvel > 0: self.rect.right = p.rect.left
				if xvel < 0: self.rect.left = p.rect.right
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.on_ground = True
					self.yvel = 0
				if yvel < 0: self.rect.top = p.rect.bottom
	def place_block(self, colour):
		blocksound.play()
		x = self.rect.right - 640 / self.rect.right - self.rect.right % 32
		y = self.rect.top
		block = PlayerBlock(x, y, colour)
		platforms.append(block)
		entities.add(block)

class Platform(Entity):
	def __init__(self, x, y, painted=False):

		Entity.__init__(self)
		self.image = Surface((32, 32))
		self.image.convert()
		self.image.fill(PLATFORMCOLOUR)
		self.rect = Rect(x, y, 32, 32)

class FinishBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(FINISHCOLOUR)

class PlayerBlock(Platform):
	def __init__(self, x, y, colour):
		Platform.__init__(self, x, y)
		self.image.fill(colour)

if __name__ == '__main__':
	main()