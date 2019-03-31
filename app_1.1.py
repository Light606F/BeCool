# スタート，リザルト，ゲーム中の画面および，各オブジェクトのクラスを作成
# game manager となる関数を作成，この中で描画する画面やオブジェクトを指定したい

from random import randint
import pyxel

WINDOW_HIGHT = 180
WINDOW_WIDTH = 240

CHARACTOR_HIGHT = 16
CHARACTOR_WIDTH = 16

FLOOR_HIGHT = 16
FLOOR_WIDTH = 16*4

JUMP_COUNT_MAX = 2

imgInf = {
	# (width,height,imgX,imgY,transparentColor)
	"player" : (16, 16, 0, 16, 7)
}

mapInf = {
	# (width,height,imgX,imgY,transparentColor)
	# width,heightは，タイル(8x8)の数．
	"floor" : (2*4, 2, 0, 0, 7)
}


############################################################
### Start
############################################################
class start_screen:
	def __init__(self):
		pyxel.run(self.update, self.draw)

	def update(self): # Q:quit, Space:start
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()
		elif pyxel.btnp(pyxel.KEY_S):
			game_manager()

	def draw(self): # タイトルとキーの表示
		pyxel.cls(0)
		pyxel.text(80, 80, "Super NAMAKO run", 15)
		pyxel.text(80, 150, "S:game start", 5)
		pyxel.text(80, 160, "Q:quit", 5)

############################################################
### Result
############################################################
class result_screen:
	def __init__(self):
		pyxel.run(self.update, self.draw)

	def update(self): # Q:quit, R:return
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()
		elif pyxel.btnp(pyxel.KEY_R):
			start_screen()

	def draw(self): # Game over とキーの表示
		pyxel.cls(0)
		pyxel.text(100, 80, "Game over!!", pyxel.frame_count % 16)
		pyxel.text(80, 150, "Pless R key", 5)

############################################################
### game stage
############################################################
class game_stage:
	def __init__(self, map_index):
		pass

	def update(self):
		if pyxel.btnp(pyxel.KEY_Q): # Q:quit
			pyxel.quit()
		elif pyxel.btnp(pyxel.KEY_G):
			result_screen()

	def draw(self):
		pyxel.cls(12) # 水色でスクリーンを初期化
		pyxel.text(pyxel.width-15, 0, str(pyxel.frame_count), 6)
		pyxel.text(1,1, "JUMP :SPACE\nRIGHT:->\nLEFT :<-", 6)

class body(object):
	"""
	docstring for body.

	Author : Light606F

	形のあるオブジェクトの基底となるAbstractなクラス．
	クラスobjectはPythonが元から使ってる奴のため，Bodyって名前になった．
	"""

	def __init__(self, coord, imgInf):
		self._setCoord(coord)
		self._setImage(imgInf)

	def _setCoord(self,coord):
		# object coordinates
		self._x = coord[0]
		self._y = coord[1]
		# 		self.x_coordinate = 0 # x軸初期位置
		# 		self.y_coordinate = 70 # y軸初期位置

	def _setImage(self, imgInf):
		# for image
		(w,h,imgX,imgY,tc) = imgInf
		## size
		self._w = w
		self._h = h
		## image coordinates on asset
		self._imgX = imgX
		self._imgY = imgY
		## transparent color in this image
		self._transparentColor = tc

	def draw(self):
		pyxel.blt(self._x, self._y, 0, self._imgX,self._imgY, self._w,self._h, self._transparentColor)

class movableBody(body):
	"""
	docstring for movableBody.

	Author : Light606F

	動くBodyの基底となるAbstractなクラス．
	"""

	def __init__(self, coord, imgInf, initVel):
		super().__init__(coord,imgInf)
		self._vx, self._vy = initVel
		# 		self.x_axis_vector = 0 # x軸速度
		# 		self.y_axis_vector = 0 # y軸速度

	def update(self):
		self._updateCoord()

	def _updateCoord(self):
		self._x += self._vx
		self._y += self._vy

class player(movableBody):
	"""docstring for player."""

	def __init__(self):
		coord = (0, pyxel.height - CHARACTOR_HIGHT)
		initVel = (0,0)
		super().__init__(coord, imgInf["player"], initVel)

		# 頭うった時
		self.onTop = False
		# Playerの左にオブジェクトがあたった時
		self.onLeft = False
		# Playerの右にオブジェクトがあたった時
		self.onRight = False
		# オブジェクトの上に来た時，オブジェクトに乗った時，True
		self.onUnder = True

	def update(self):
		super().update()
		self._gravity()
		self._keyActions()
		# reset jump_counter

	def draw(self):
		pyxel.blt(self._x, self._y, 0, self._imgX if abs(self._vx) > 0 else self._imgX+self._w,self._imgY, self._w,self._h, self._transparentColor)

	# ---vvv--- getter ---
	@property
	def x(self):
		return self._x
	@property
	def y(self):
		return self._y
	# ---^^^--- getter ---

	def _gravity(self):
		if self.onUnder:
			self._vy = 0
		else :
			# g = 9.80665
			# self._vy = self._vy + g*0.05
			self._vy = min(self._vy + 1, 5) # 落下速度の最大値
			print(self._vy)

	def _keyActions(self):
		# ---vvv---左右移動
		if pyxel.btn(pyxel.KEY_LEFT): # 左加速
			self._vx = max(self._vx - 0.5 , -2) # 左最大速度
		if pyxel.btnr(pyxel.KEY_LEFT): # キーを離したら vector をリセット
			self._vx = 0

		if pyxel.btn(pyxel.KEY_RIGHT): # 右加速
			self._vx = min(self._vx + 0.5 , 2) # 右最大速度 右画面端までしかいかない
		if pyxel.btnr(pyxel.KEY_RIGHT): # キーを離したら vector をリセット
			self._vx = 0
		# ---^^^---左右移動

		self._jump()

	def _jump(self): # ジャンプ処理
		if (
		pyxel.btnp(pyxel.KEY_SPACE)
		# and self.jump_counter < JUMP_COUNT_MAX
		):
			self._vy = max(self._vy - 12, -12) # ジャンプ力
			# self.jump_counter += 1

class floor(movableBody):
	def __init__(self, player):
		coord = (0, 0)
		initVel = (-1, 0)
		super().__init__(coord, mapInf["floor"], initVel)
		self._player = player

	def update(self):
		super().update()

		if self._x + 16*4 < 0:
			self._x = 240
			self._y = randint(100,160)
		else:
			self._x += self._vx # x軸移動

		self.doYouHit()

	def draw(self):
		pyxel.bltm(self._x, self._y, 0, self._imgX ,self._imgY, self._w,self._h, self._transparentColor)

	def doYouHit(self): ### player と floor の当たり判定
		if ( ### 接地判定
			self._player.x + CHARACTOR_WIDTH >= self._x # 左側
			and self._player.x <= self._x + FLOOR_WIDTH # 右側
			and self._player.y + CHARACTOR_HIGHT >= self._y # 上側
			and self._player.y <= self._y + FLOOR_HIGHT # 下側
			):
			if not self._player.y + CHARACTOR_HIGHT >= self._y : ### 上側接触
				self._player.onUnder = True # y軸速度最大で0に

			elif not self._player.y >= self._y + FLOOR_HIGHT : ### 下側接触
				self._player.onTop = True # y軸速度最小で0に

			elif not self._player.x >= self._x + FLOOR_WIDTH : ### 右側接触
				self._player.onLeft = True  # x軸速度を max(floor, player)

			elif not self._player.x + CHARACTOR_WIDTH <= self._x: ### 左側接触
				self._player.onRight = True  # x軸速度を min(floor, player)

		else: ### 非接地で接地フラグを False に
			self._player.onUnder = False
			self._player.onTop = False
			self._player.onRight = False
			self._player.onLeft = False

############################################################
### player object
############################################################
# class player:
# 	def __init__(self):
# 		self.x_coordinate = 0 # x軸初期位置
# 		self.y_coordinate = 70 # y軸初期位置
# 		self.x_axis_vector = 0 # x軸速度
# 		self.y_axis_vector = 0 # y軸速度
#
# 		self.jump_counter = 0 # ジャンプ回数カウンタ
# 		# self.on_graund = True # 接地フラグ
#
#
# 	def update(self):
# 		self.change_vector()
# 		self.jump()
#
# 		if self.x_coordinate + self.x_axis_vector < 0: # x軸移動，画面内のみ
# 			self.x_coordinate = 0
# 		elif WINDOW_WIDTH - CHARACTOR_WIDTH < self.x_coordinate + self.x_axis_vector:
# 			self.x_coordinate = WINDOW_WIDTH - CHARACTOR_WIDTH
# 		else:
# 			self.x_coordinate += self.x_axis_vector
#
# 		if self.y_coordinate >= WINDOW_HIGHT - CHARACTOR_HIGHT: # 画面下に来たら，ジャンプカウンタリセット
# 			# print("reset")
# 			self.jump_counter = 1
#
# 		self.y_coordinate += self.y_axis_vector # y軸移動
#
# 	def draw(self): # プレイヤーを描画
# 		pyxel.blt(self.x_coordinate, self.y_coordinate, 0, 0 if abs(self.x_axis_vector) > 0 else 16, 16, 16, 16, 7)
#
# 	def change_vector(self): # 速度変更
# 		# ---vvv---左右移動
# 		if pyxel.btn(pyxel.KEY_LEFT): # 左加速
# 			self.x_axis_vector = max(self.x_axis_vector - 0.5 , -2) # 左最大速度
# 		if pyxel.btnr(pyxel.KEY_LEFT): # キーを離したら vector をリセット
# 			self.x_axis_vector = 0
#
# 		if pyxel.btn(pyxel.KEY_RIGHT): # 右加速
# 			self.x_axis_vector = min(self.x_axis_vector + 0.5 , 2) # 右最大速度 右画面端までしかいかない
# 		if pyxel.btnr(pyxel.KEY_RIGHT): # キーを離したら vector をリセット
# 			self.x_axis_vector = 0
# 		# ---^^^---左右移動
#
# 		if self.on_graund:
# 			self.y_axis_vector = 0
# 		else :
# 			# g = 9.80665
# 			# self.y_axis_vector = self.y_axis_vector + g*0.05
# 			self.y_axis_vector = min(self.y_axis_vector + 1, 5) # 落下速度の最大値
# 			print(self.y_axis_vector)
#
# 		# if self.y_coordinate < WINDOW_HIGHT - CHARACTOR_HIGHT:
# 		# 	# 画面下までいったらだめ
# 		# 	# でもこれじゃ埋まっちゃう．
# 		#
# 		# 	if self.on_graund:
# 		# 		self.y_axis_vector = 0
# 		# 	else :
# 		# 		# g = 9.80665
# 		# 		# self.y_axis_vector = self.y_axis_vector + g*0.05
# 		# 		self.y_axis_vector = min(self.y_axis_vector + 1, 5) # 落下速度の最大値
# 		# 		print(self.y_axis_vector)
# 		# else:
# 		# 	self.y_axis_vector = 0
# 		# 	# self.y_coordinate = WINDOW_HIGHT - CHARACTOR_HIGHT

############################################################
### floor object
### in 座標，x軸速度ベクトル
### out
############################################################
# class floor:
	# def __init__(self, x, y, u):
		# self.x_coordinate = x # x軸初期位置
		# self.y_coordinate = y # y軸初期位置
		# self.x_axis_vector = u # x軸速度

	# ###############################
	# ### update
	# ### in 座標，x軸速度ベクトル
	# ### out 座標，x軸速度ベクトル
	# ###############################
	# def update(self, x, y, u):
		# if self.x_coordinate + 16*4 < 0:
			# self.x_coordinate = 240
			# self.y_coordinate = randint(100,160)
		# else:
			# self.x_coordinate += self.x_axis_vector # x軸移動

		# # self.x_axis_vector = - (pyxel.frame_count % 10) # 移動中に速度変更

		# return [self.x_coordinate, self.y_coordinate, self.x_axis_vector]

	# def draw(self):
		# pyxel.bltm(self.x_coordinate, self.y_coordinate, 0, 0, 0, 2*4, 2)

	# def do_you_hit(self, floor_index): # 当たり判定
		# if (
			# self.player.x_coordinate + CHARACTOR_WIDTH >= self.floor_initials[floor_index][0] # 右側
			# and self.player.x_coordinate <= self.floor_initials[floor_index][0] + FLOOR_WIDTH # 左側
			# and self.player.y_coordinate + CHARACTOR_HIGHT >= self.floor_initials[floor_index][1] # 下側
			# and self.player.y_coordinate <= self.floor_initials[floor_index][1] + FLOOR_HIGHT # 上側
			# ):
			# self.player.y_axis_vector = 0 # y軸速度0
			# self.player.jump_counter = 0 # ジャンプカウンタ0
			# self.player.on_graund = True # 接地フラグ
		# else:
			# self.player.on_graund = False

############################################################
### game manager
############################################################
class game_manager:
	def __init__(self):
		self.score = 0 # スコア初期化

		self.player_initials = [[0, 70, 0, 0, 0, True, False]] # プレイヤーのパラメータ初期値
		self.floor_initials = [[240 + 16*4, randint(100,160), -5], [240 + (120 + 16*2) + 16*4, randint(100,160), -7]] # 床のパラメータ初期値

		# インスタンス生成
		self.stage1 = game_stage(0)
		self.player = player()
		self.floor0 = floor(self.player)
		self.floor1 = floor(self.player)
		# インスタンス生成ここまで

		pyxel.run(self.update, self.draw)

	def update(self): # 更新
		self.stage1.update() # game stage 更新

		# 可動物体の更新
		# self.floor_initials[0] = self.floor0.update(*self.floor_initials[0])
		# self.floor_initials[1] = self.floor1.update(*self.floor_initials[1])
		self.player.update()
		self.floor0.update()

		# self.do_you_hit(0)
		# self.do_you_hit(1)

	def draw(self): # 描画
		self.stage1.draw()
		self.floor0.draw()
		self.floor1.draw()
		self.player.draw()

############################################################
### 実行
############################################################
pyxel.init(WINDOW_WIDTH, WINDOW_HIGHT, caption="Be cool!!") # ウィンドウを初期化
pyxel.load("./assets.pyxel")

start_screen()
