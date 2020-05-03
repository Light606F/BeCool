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
		if pyxel.btn(pyxel.KEY_UP):
			if self.y > DisplayHeight-TILE_SIZE*4:
				self.y -= 2
			else:
				self.y -= 1

		if pyxel.btn(pyxel.KEY_RIGHT):
			self.x = min( self.x+self.SPEED, DisplayWidth-TILE_SIZE )

		if pyxel.btn(pyxel.KEY_LEFT):
			self.x = max( self.x-self.SPEED, 0 )

		# if upper then floor
		if self.y+self.width < DisplayHeight-TILE_SIZE:
			self.y +=1

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

	def draw(self):
		for i in range(0, DisplayWidth, TILE_SIZE):
			pyxel.blt(
				i, self.y,
				0,
				self.tileX, self.tileY,
				TILE_SIZE, TILE_SIZE)


class Obstacle(Obj):
	"""docstring for Obstacle."""

	def __init__(self):
		super().__init__()
		rnd = random.randint(2,4)
		self.x = DisplayWidth-TILE_SIZE
		self.y = DisplayHeight-TILE_SIZE*rnd
		self._setTile(40, 0)

	def update(self):
		self.x -= 1


class App:
	def __init__(self):
		self.state = "start"
		self.playerChr = Charactor()
		self.floor = Floor()
		self.ceiling = Ceiling()
		self.obstacle = Obstacle()

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
			if self.obstacle.x < 0:
				self.obstacle = Obstacle()
			self.obstacle.update()
			self.playerChr.update()

			# Collision
			self.playerChr.collision(self.obstacle)

			if self.playerChr.death:
				self.state = "gameOver"
		elif self.state=="gameOver":
			if pyxel.btnp(pyxel.KEY_R):
				self.playerChr.__init__()
				self.obstacle.__init__()
				self.state = "main"

	def draw(self):
		# background
		pyxel.cls(7)

		if self.state=="start":
			self.printTextCenter(DisplayHeight/2-TEXT_HEIGHT/2-10, "ZERO ONE", pyxel.frame_count % 16)
			self.printTextCenter(DisplayHeight/2+TEXT_HEIGHT/2-10+1, "Press SPACE", 0)
			# self.printCenter()

		elif self.state=="main":
			pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)

			self.floor.draw()
			self.ceiling.draw()
			self.obstacle.draw()
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
