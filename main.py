import pyxel
import random

DisplayWidth = 160
DisplayHeight = 120
TILE_SIZE = 8
TEXT_HEIGHT = 5
TEXT_WIDTH = 3

class Obj():
	"""docstring for Obj."""

	def __init__(self):
		self.x = 0
		self.y = 0
		self.height = TILE_SIZE
		self.width = TILE_SIZE
		self._setTile(0,0)

	def _setTile(self, x, y):
		self.tileX = x
		self.tileY = y

	def draw(self):
		transClr = 2
		pyxel.blt(
			self.x, self.y,
			0,
			self.tileX, self.tileY,
			TILE_SIZE, TILE_SIZE, transClr)


class Charactor(Obj):
	"""docstring for Charactor."""

	def __init__(self):
		super().__init__()
		self.y = DisplayHeight-TILE_SIZE*2
		self.height = TILE_SIZE-1
		self.width = TILE_SIZE-1
		self._setTile(0, 16)
		self.SPEED = 2

		self.death = False

	def update(self):
		prevY = self.y
		GRAVITY = 1

		if not pyxel.btn(pyxel.KEY_SPACE):
			# USUAL

			if pyxel.btn(pyxel.KEY_UP):
				if self.y > DisplayHeight-TILE_SIZE*4:
					self.y -= GRAVITY + 2
				else:
					self.y = DisplayHeight-TILE_SIZE*4
					# anti gravity
					self.y -= GRAVITY

			# if upper then floor
			if self.y+self.width-1 < DisplayHeight-TILE_SIZE -1:
				# gravity
				self.y += GRAVITY

			if pyxel.btn(pyxel.KEY_LEFT):
				self.x = max( self.x-self.SPEED, 0 )

			elif pyxel.btn(pyxel.KEY_RIGHT):
				self.x = min( self.x+self.SPEED, DisplayWidth-TILE_SIZE )

		else:
			# if press SPACE key

			self.y = prevY

			if pyxel.btn(pyxel.KEY_UP):
				if self.y > DisplayHeight-TILE_SIZE*4:
					self.y -= 1
			elif pyxel.btn(pyxel.KEY_DOWN):
				if self.y+self.width-1 < DisplayHeight-TILE_SIZE -1:
					self.y += 1
			# if pyxel.btn(pyxel.KEY_LEFT):
			# 	self.x -= 1
			# elif pyxel.btn(pyxel.KEY_RIGHT):
			# 	self.x += 1

	def collision(self, obj):
		selfXStart = self.x
		selfYStart = self.y
		selfXEnd = self.x+self.width-1
		selfYEnd = self.y+self.height-1
		objXStart = obj.x
		objYStart = obj.y
		objXEnd = obj.x+obj.width-1
		objYEnd = obj.y+obj.height-1

		if selfXEnd >= objXStart and objXEnd >= selfXStart:
			if selfYEnd >= objYStart and objYEnd >= selfYStart:
				self.death = True


class Floor(Obj):
	"""docstring for Floor."""

	def __init__(self):
		super().__init__()
		self.y = DisplayHeight-TILE_SIZE
		self._setTile(8, 0)

	def draw(self):
		for i in range(0, DisplayWidth, TILE_SIZE):
			pyxel.blt(
				i, self.y,
				0,
				self.tileX, self.tileY,
				TILE_SIZE, TILE_SIZE)


class Ceiling(Obj):
	"""docstring for Ceiling."""

	def __init__(self):
		super().__init__()
		self.y = DisplayHeight-TILE_SIZE*5
		self._setTile(24, 0)

		self.startPoint = 0

	def draw(self):
		for i in range(self.startPoint, DisplayWidth+TILE_SIZE, TILE_SIZE):
			pyxel.blt(
				i, self.y,
				0,
				self.tileX, self.tileY,
				TILE_SIZE, TILE_SIZE)
		self.startPoint -=1
		if self.startPoint > TILE_SIZE:
			self.startPoint = 0


class Obstacle(Obj):
	"""docstring for Obstacle."""

	def __init__(self, high):
		super().__init__()
		self.x = DisplayWidth-TILE_SIZE
		self.y = DisplayHeight-TILE_SIZE*(1+high)
		self._setTile(40, 0)
		self.SPEED = 1

	def update(self):
		self.x -= self.SPEED


class App:
	def __init__(self):
		# object
		self.playerChr = Charactor()
		self.floor = Floor()
		self.ceiling = Ceiling()
		self.obstacles = []

		# valiable
		self.state = "start"
		self.countFromCreateObs = 255

		# init
		pyxel.init(DisplayWidth, DisplayHeight, caption="Zero One")
		pyxel.load("assets/assets.pyxres")
		pyxel.run(self.update, self.draw)

	def update(self):
		# Quit
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		if self.state=="start":
			if pyxel.btnp(pyxel.KEY_SPACE):
				self.state = "main"
		elif self.state=="main":
			self.updateMain()
			if self.playerChr.death:
				self.state = "gameOver"
		elif self.state=="gameOver":
			if pyxel.btnp(pyxel.KEY_R):
				self.playerChr.__init__()
				self.obstacles.clear()
				self.state = "main"

	def updateMain(self):
		# obstacle
		## create
		# Ensure space to move player
		self.countFromCreateObs +=1
		if self.countFromCreateObs > TILE_SIZE + TILE_SIZE + 10:
			# create or not
			rnd = random.random()
			if rnd < 0.05:
				# if create
				# how many 1or2
				num = random.randint(1,2)
				if num==1:
					place = random.randint(1,3)
					self.obstacles.append(Obstacle(place))
				elif num==2:
					place = [1,2,3]
					place.remove(random.randint(1,3))
					for i in place:
						self.obstacles.append(Obstacle(i))
				else:
					print("ERR")
					exit(1)
				self.countFromCreateObs = 0

		## update & prepare remove
		obsRm = []
		for o in self.obstacles:
			if o.x < 0:
				obsRm.append(o)
				continue

			## update
			o.update()

		## remove
		for o in obsRm:
			self.obstacles.remove(o)

		# player
		self.playerChr.update()

		## collision
		for o in self.obstacles:
			self.playerChr.collision(o)

	def draw(self):
		# background
		pyxel.cls(7)

		if self.state=="start":
			self.printTextCenter(DisplayHeight/2-TEXT_HEIGHT/2-10, "ZERO ONE", pyxel.frame_count % 16)
			self.printTextCenter(DisplayHeight/2+TEXT_HEIGHT/2-10+1, "Press SPACE", 0)
			# self.printCenter()

		elif self.state=="main":
			pyxel.text(1,1, "ARROW KEY : move\nSPACE : stop", 0)
			pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)

			self.floor.draw()
			self.ceiling.draw()
			for o in self.obstacles:
				o.draw()
			self.playerChr.draw()

			# # Collision
			# if self.playerChr.death:
			# 	pyxel.text(0, 0, "HIT!", 8)
		elif self.state=="gameOver":
			self.printTextCenter(DisplayHeight/2-TEXT_HEIGHT/2-10, "GAME OVER", 0)
			self.printTextCenter(DisplayHeight/2+TEXT_HEIGHT/2-10+1, "Press R to RESTART", 0)

	def printTextCenter(self, height, text, col):
		x = DisplayWidth/2 - len(text)/2*TEXT_WIDTH
		pyxel.text(x, height, text, col)

	def printCenter(self):
		pyxel.line(DisplayWidth/2,0,DisplayWidth/2,DisplayHeight, 8)
		pyxel.line(0,DisplayHeight/2,DisplayWidth,DisplayHeight/2, 8)


if __name__ == "__main__":
	App()
