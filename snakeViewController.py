import threading
import time
import numpy
from random import randint
from snakeView import GameView
import math
import cocos


class SnakeModel:
	def __init__(self, x, y, bound, initLength):
		self.body = []
		for offset in range(initLength):
			self.body.append((x - offset, y))
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

	increasingSnake = True
	# the snake will become longer when hitting food you this variable was setting to True.

	fixedFoodPosition = []
	# set it to a list that contains x and y if you want the food position be fixed.

	scores = []

	updatePlotFunction = None

	def __init__(self, window_size = 800, block_width = 30, snakeInitLength = 3):
		self.window_size = window_size
		self.block_width = block_width
		self.gameView = GameView(self.window_size, self.block_width)
		self.snake = SnakeModel(self.block_width/2, self.block_width/2, (block_width, block_width), snakeInitLength)
		self.lock = threading.RLock()
		self.game_over = False
		self.food = []
		self.score = 0
		self.previous = 0
		self.snakeInitLength = snakeInitLength

	def enable_keyboard_detecting(self, action = None):
		if action == None:
			self.gameView.addKeyboardAction(self.on_key_press)
		else:
			self.gameView.addKeyboardAction(action)

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

	def resetGame(self):
		self.cancelGame()
		self.lock.acquire()
		self.food = []
		self.score = 0
		self.snake = SnakeModel(self.block_width/2, self.block_width/2, (self.block_width, self.block_width), self.snakeInitLength)
		self.__update_screen()
		self.game_over = False
		self.lock.release()

	def getGameStatus(self):
		return self.game_over

	def __start_controller(self):
		self.lock.acquire()
		self.game_over = False
		self.lock.release()
		index = 0
		while not self.game_over:
			self.__update_screen()
			time.sleep(0.1)
			if not self.__moveForword():
				print("score is: " + str(self.score))
				self.cancelGame()
			self.__refresh_food()
			if self.snake.hittingFood(self.food):
				self.food = []
				if self.increasingSnake:
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
			self.resetGame()
	
	def __refresh_food(self):
		if self.food == []:
			if self.fixedFoodPosition == []:
				self.food = [randint(0, self.block_width - 1), randint(0, self.block_width - 1)]
				while self.snake.hittingFood(self.food):
					self.food = [randint(0, self.block_width - 1), randint(0, self.block_width - 1)]
			else:
				self.food = self.fixedFoodPosition

	#===========================prog mark: API for Reinforcement Learning============================#

	def showGame(self):
		self.gameView.show()	

	def render(self):
		self.__update_screen()

	def reset(self):
		self.gameView.reset()
		self.resetGame()
		return self.__get_state()

	def step(self, action):
		time.sleep(0.1)
		reward = 0
		if action == "left":
			self.moveLeft()
		if action == "right":
			self.moveRight()
		if not self.__moveForword():
			self.cancelGame()
			state = "Dead"
			reward = -1
			print("score is: " + str(self.score))
			self.scores.append(self.score)
			return self.__get_state(), reward, self.game_over
		self.__refresh_food()
		if self.snake.hittingFood(self.food):	
			self.food = []
			if self.increasingSnake:
				self.snake.increaseNode()
			self.score += 1
			reward = self.score / (self.block_width * self.block_width)
		state = self.__get_state()
		return state, reward, self.game_over

	def get_status(self):
		return self.__get_state()

	def __get_state(self):
		state = ""
		if self.increasingSnake:
			for position in self.snake.getPositions():
				state += str(position)
		else:
			state += str(self.snake.getPositions()[0])
		if self.food != []:
			state += "-" + str(self.food)
		else:
			state = "Target"
		if self.game_over:
			state = "dead"
		return state
	