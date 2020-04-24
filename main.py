import pyxel

DisplayWidth = 160
DisplayHeight = 120
TileSize = 8

class obj():
	"""docstring for obj."""

	def __init__(self, tileX, tileY):
		self.x = 0
		self.y = 0
		self.tileX = tileX
		self.tileY = tileY


class Charactor(obj):
	"""docstring for Charactor."""
	pass


class Floor(obj):
	"""docstring for Charactor."""

	def __init__(self, tileX, tileY):
		super().__init__(tileX, tileY)
		self.y = DisplayHeight-TileSize


class App:
	def __init__(self):
		self.playerChr = Charactor(0, 16)
		self.floor = Floor(8, 0)

		pyxel.init(DisplayWidth, DisplayHeight, caption="Zero One")
		pyxel.load("assets/assets.pyxres")
		pyxel.run(self.update, self.draw)

	def update(self):
		# Quit
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		def updatePlayer():
			pass

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
