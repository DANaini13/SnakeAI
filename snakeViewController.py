import threading
import time
import numpy
from random import randint
from snakeView import GameView
import math
import cocos

class SnakeModel:
	def __init__(self, x, y, bound):
		self.body = []
		self.body.append((x, y))
		self.body.append((x - 1, y))
		self.body.append((x - 2, y))
		self.dir = 1 #0:up, 1:right, 2:down, 3:left
		self.bound = bound
		self.previous = self.body
		self.preDir = self.dir

	def getPositions(self):
		return self.body

	def getDirection(self):
		return self.dir
		
	def increaseNode(self):
		self.body.append((-10, -10))

	def moveForword(self):
		self.previous = self.body
		temp = self.__moveNode(self.body[0])
		flag = True
		if not self.__checkBounds(temp):
			flag = False
		if not self.__checkSelf(temp):
			flag = False
		head = self.body[0]
		self.body[0] = temp
		self.__followNodes(head)
		return flag

	def hittingFood(self, food):
		for node in self.body:
			if node[0] == food[0] and node[1] == food[1]:
				return True
		return False

	def moveLeft(self):
		self.preDir = self.dir
		self.dir = (self.dir + 3)%4

	def moveRight(self):
		self.preDir = self.dir
		self.dir = (self.dir + 1)%4

	def __followNodes(self, head): 
		for index in range(len(self.body) - 1):
			temp = self.body[index + 1]
			self.body[index + 1] = head 
			head = temp

	def __checkBounds(self, point):
		return point[0] >= 0 and point[0] < self.bound[0] and point[1] >= 0 and point[1] < self.bound[1]

	def __checkSelf(self, point):
		for node in self.body:
			if node[0] == point[0] and node[1] == point[1]:
				return False
		return True

	def __moveNode(self, node):
		if self.dir == 0:
			return (node[0], node[1] - 1)
		elif self.dir == 1:
			return (node[0] + 1, node[1])
		elif self.dir == 2:
			return (node[0], node[1] + 1)
		else:
			return (node[0] - 1, node[1])

class SnakeViewController():
	def __init__(self, window_size = 800, block_width = 30):
		self.window_size = window_size
		self.block_width = block_width
		self.gameView = GameView(self.window_size, self.block_width)
		self.snake = SnakeModel(self.block_width/2, self.block_width/2, (block_width, block_width))
		self.lock = threading.RLock()
		self.game_over = False
		self.food = []
		self.score = 0

	def enable_keyboard_detecting(self):
		self.gameView.addKeyboardAction(self.on_key_press)

	def start_game(self):
		t = threading.Thread(target=self.__start_controller, args=())
		t.start()
		self.gameView.show()

	def moveLeft(self):
		self.lock.acquire()
		self.snake.moveLeft()
		self.lock.release()

	def moveRight(self):
		self.lock.acquire()
		self.snake.moveRight()
		self.lock.release()

	def cancelGame(self):
		self.lock.acquire()
		self.game_over = True
		self.lock.release()

	def getGameStatus(self):
		return self.game_over

	def __start_controller(self):
		time.sleep(0.02)
		self.game_over = False
		index = 0
		while not self.game_over:
			self.__update_screen()
			time.sleep(0.1)
			if not self.__moveForword():
				self.cancelGame()
			if self.food == []:
				self.food = [randint(1, self.block_width - 2), randint(1, self.block_width - 2)]
			if self.snake.hittingFood(self.food):
				self.food = []
				self.snake.increaseNode()
				self.score += 1
				#self.gameView.setScore(self.score)
			index += 1
	
	def __moveForword(self):
		self.lock.acquire()
		result = self.snake.moveForword()
		self.lock.release()
		return result

	def __update_screen(self):
		positions = self.snake.getPositions()
		for index, pos in zip(range(len(positions)), positions):
			self.gameView.setSubviewPositionWithID(index, pos)
		if self.food != []:
			self.gameView.setSubviewPositionWithID(-1, self.food)
		else:
			self.gameView.setSubviewPositionWithID(-1, (-2, -2))

	def on_key_press(self, key):
		if key == 65361:
			self.moveLeft()
		if key == 65363:
			self.moveRight()
		if key == 65307:
			self.cancelGame()