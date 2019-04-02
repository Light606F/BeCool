### run(update, draw) 実行時に，update と draw のどちらが先に実行されるのかを検証する
### 自前のカウンタ を用いるか frame_count を用いるかで結果が変わるため，それについても考察

### 結論
### run は update -> draw の順番で実行している
### frame_count は update 完了時 もしくは draw 呼び出し時に更新される

import pyxel

WINDOW_HIGHT = 180
WINDOW_WIDTH = 240

class main:
	def __init__(self):
		pyxel.init(WINDOW_WIDTH, WINDOW_HIGHT, caption="Which is faster?") # ウィンドウを初期化
		self.dt = "Draw count = {}."
		self.ut = "Update count = {}."
		self.dc = 0
		self.uc = 0
		pyxel.run(self.update, self.draw)

	def update(self): # Q:quit

		### 自前のカウンタと frame_count を切り替える
		# self.uc += 1
		self.uc = pyxel.frame_count

		print(self.ut.format(self.uc))
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

	def draw(self):
		pyxel.cls(0)

		### 自前のカウンタと frame_count を切り替える
		# self.dc += 1
		self.dc =  pyxel.frame_count

		print(self.dt.format(self.dc))
		pyxel.text(80, 80, "Which is faster, update or draw?", 15)
		
main()

# >>python whichIsFaster.py ### 自前のカウンタを用いた時
# Update count = 1.
# Draw count = 1.
# Update count = 2.
# Draw count = 2.
# Update count = 3.
# Draw count = 3.
# ...


# >>python whichIsFaster.py ### frame_count を用いた時
# Update count = 0.
# Draw count = 1.
# Update count = 1.
# Draw count = 2.
# Update count = 2.
# Draw count = 3.
# ...


### If draw is faster than update, first uptput of "Update Count" must be 0.
### If update is faster than draw, first uptput of "Update Count" must be 1.
### So, update is faster than draw.