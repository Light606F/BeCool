import pyxel
import random

DisplayWidth = 160
DisplayHeight = 120
TILE_SIZE = 8

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

	def update(self):
		if pyxel.btn(pyxel.KEY_UP):
			self.y -= 2

		if pyxel.btn(pyxel.KEY_RIGHT):
			self.x = min( self.x+self.SPEED, DisplayWidth-TILE_SIZE )

		if pyxel.btn(pyxel.KEY_LEFT):
			self.x = max( self.x-self.SPEED, 0 )

		# if upper then floor
		if self.y+self.width < DisplayHeight-TILE_SIZE:
			self.y +=1

	def collision(self, obj):
		xRightEnd = self.x+self.width-1
		objXRightEnd = obj.x+obj.width-1
		yBottomEnd = self.y+self.height-1
		objYBottomEnd = obj.y+obj.height-1

		if xRightEnd >= obj.x and objXRightEnd >= self.x:
			if yBottomEnd >= obj.y and objYBottomEnd >= self.y:
				pyxel.text(0, 0, "HIT!", 8)


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
		self.playerChr = Charactor()
		self.floor = Floor()
		self.obstacle = Obstacle()

		pyxel.init(DisplayWidth, DisplayHeight, caption="Zero One")
		pyxel.load("assets/assets.pyxres")
		pyxel.run(self.update, self.draw)

	def update(self):
		# Quit
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		if self.obstacle.x < 0:
			self.obstacle = Obstacle()
		self.obstacle.update()
		self.playerChr.update()

		# # Collision
		# self.playerChr.collision(self.obstacle)

	def draw(self):
		pyxel.cls(7)
		pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)

		self.floor.draw()
		self.obstacle.draw()
		self.playerChr.draw()

		# Collision
		self.playerChr.collision(self.obstacle)

App()
