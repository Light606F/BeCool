import pyxel

DisplayWidth = 160
DisplayHeight = 120
TileSize = 8

class obj():
	"""docstring for obj."""

	def __init__(self):
		self.x = 0
		self.y = 0
		self._setTile(0,0)

	def _setTile(self, x, y):
		self.tileX = x
		self.tileY = y


class Charactor(obj):
	"""docstring for Charactor."""

	def __init__(self):
		super().__init__()
		self.y = DisplayHeight-TileSize*2
		self._setTile(0, 16)

	def update(self):
		if pyxel.btn(pyxel.KEY_UP):
			self.y -= 2

		if pyxel.btn(pyxel.KEY_RIGHT):
			self.x = min( self.x+2, DisplayWidth-TileSize )

		if pyxel.btn(pyxel.KEY_LEFT):
			self.x = max( self.x-2, DisplayWidth-TileSize )

		if self.y < DisplayHeight-TileSize*2:
			self.y +=1


class Floor(obj):
	"""docstring for Charactor."""

	def __init__(self):
		super().__init__()
		self.y = DisplayHeight-TileSize
		self._setTile(8, 0)


class App:
	def __init__(self):
		self.playerChr = Charactor()
		self.floor = Floor()

		pyxel.init(DisplayWidth, DisplayHeight, caption="Zero One")
		pyxel.load("assets/assets.pyxres")
		pyxel.run(self.update, self.draw)

	def update(self):
		# Quit
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		self.playerChr.update()

	def draw(self):
		pyxel.cls(7)
		pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)

		def drawPlayer():
			pyxel.blt(
				self.playerChr.x, self.playerChr.y,
				0,
				self.playerChr.tileX, self.playerChr.tileY,
				TileSize, TileSize)

		def drawFloor():
			for i in range(0, DisplayWidth, TileSize):
				pyxel.blt(
					i, self.floor.y,
					0,
					self.floor.tileX, self.floor.tileY,
					TileSize, TileSize)

		drawFloor()
		drawPlayer()

App()
