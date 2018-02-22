import curses
import threading
import time
import numpy
from curses import KEY_LEFT, KEY_RIGHT
from random import randint

class Snake:
	def __init__(self, x, y, bound, window):
		self.body = []
		self.body.append((x, y))
		self.body.append((x - 1, y))
		self.body.append((x - 2, y))
		self.dir = 1 #0:up, 1:right, 2:down, 3:left
		self.bound = bound
		self.snake_win = window
		self.display()
		self.previous = self.body
		self.preDir = self.dir

	def getPositions(self):
		return self.body
		
	def increaseNode(self):
		last1 = self.body[len(self.body) - 1]
		last2 = self.body[len(self.body) - 2]
		last = (0, 0)
		if last1[0] - last2[0] == 0:
			if last1[1] > last2[1]:
				last = (last1[0], last1[0] + 1)
			else:
				last = (last1[0], last1[0] - 1)
		else:
			if last1[0] > last2[0]:
				last = (last1[0] - 1, last1[0])
			else:
				last = (last1[0] + 1, last1[0])
		self.body.append(last)

	def moveForword(self, display=True):
		self.previous = self.body
		temp = self.moveNode(self.body[0])
		flag = True
		if not self.checkBounds(temp):
			flag = False
		if not self.checkSelf(temp):
			flag = False
		if display:
			self.disappear()
		head = self.body[0]
		self.body[0] = temp
		self.followNodes(head)
		if display:
			self.display()
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

	def followNodes(self, head): 
		for index in range(len(self.body) - 1):
			temp = self.body[index + 1]
			self.body[index + 1] = head 
			head = temp

	def checkBounds(self, point):
		return point[0] > 0 and point[0] < self.bound[0] - 1 and point[1] > 0 and point[1] < self.bound[1] - 1

	def checkSelf(self, point):
		for node in self.body:
			if node[0] == point[0] and node[1] == point[1]:
				return False
		return True

	def moveNode(self, node):
		if self.dir == 0:
			return (node[0], node[1] - 1)
		elif self.dir == 1:
			return (node[0] + 1, node[1])
		elif self.dir == 2:
			return (node[0], node[1] + 1)
		else:
			return (node[0] - 1, node[1])
	
	def display(self):
		for node in self.body:
			self.snake_win.addch(node[1], node[0] * 2, '⚉',)
			#self.snake_win.addch(node[1], node[0] * 2, '#',)
			self.snake_win.addch(node[1], node[0] * 2 + 1, ' ',)
		self.snake_win.refresh()

	def disappear(self):
		for node in self.body:
			self.snake_win.addch(node[1], node[0] * 2, ' ')
			self.snake_win.addch(node[1], node[0] * 2 + 1, ' ')
		self.snake_win.refresh()

	def getSurvivalDir(self):
		self.body = self.previous
		self.dir = self.preDir
		if self.moveForword(display=False):
			return 0
		self.body = self.previous
		self.dir = self.preDir
		self.moveLeft()
		if self.moveForword(display=False):
			return 1
		self.body = self.previous
		self.dir = self.preDir
		self.moveRight()
		if self.moveForword(display=False):
			return 2
		return 0
		

class GameController:
	def __init__(self, screen_width):
		self.stdscr = curses.initscr()
		self.bg_width = screen_width
		self.snake_win = curses.newwin(self.bg_width,self.bg_width * 2, 0, 0)
		self.snake_win.keypad(1)
		self.snake_win.border(0)
		self.snake_win.nodelay(1)
		self.snake_win.addstr(0, 10, "the best snake game")
		curses.curs_set(0)
		curses.noecho()
		curses.cbreak()
		self.snake = Snake(int(self.bg_width/2), int(self.bg_width/2), (self.bg_width, self.bg_width), self.snake_win)
		self.food = []
		self.score = 0
		self.alive = True
		self.lock = threading.RLock()
	
	def __del__(self):
		curses.echo()
		curses.nocbreak()
		self.snake_win.keypad(0)
		curses.endwin()
	
	def go_left(self):
		self.lock.acquire()
		self.snake.moveLeft()
		self.lock.release()

	def go_right(self):
		self.lock.acquire()
		self.snake.moveRight()
		self.lock.release()

	def _update_score(self):
		self.snake_win.addstr(0, 45, "score: " + str(self.score))

	def start_game(self):
		self._update_score()
		t = threading.Thread(target=self._run_game, args=())
		t.start()
		return self.snake_win

	def getCurrentMap(self):
		snake = self.snake.getPositions()
		food = self.food
		result = numpy.zeros((self.bg_width, self.bg_width))
		for node in snake:
			result[node[0]][node[1]] = 0.5
		if food == []:
			return numpy.reshape(result, (self.bg_width * self.bg_width))
		result[food[0]][food[1]] = 1
		return numpy.reshape(result, (self.bg_width * self.bg_width))

	def getCurrentStatus(self):
		return self.alive
		
	def getSurvivalDir(self):
		return self.snake.getSurvivalDir()
	
	def _run_game(self):
		while(True):
			time.sleep(0.1)
			globalLock.acquire()
			if not self.snake.moveForword():
				globalLock.release()
				break
			if self.food == []:
				self.food = [randint(1, self.bg_width - 2), randint(1, self.bg_width - 2)]
				self.snake_win.addch(self.food[1], self.food[0] * 2, '⊙')
				#self.snake_win.addch(self.food[1], self.food[0] * 2, '*')
				self.snake_win.addch(self.food[1], self.food[0] * 2 + 1, ' ')
			if self.snake.hittingFood(self.food):
				self.food = []	
				self.snake.increaseNode()
				self.score += 1
				self._update_score()
			globalLock.release()
		self.alive = False

class KeyDetector:
	def __init__(self, window):
		self.win = window

	def getKey(self):
		globalLock.acquire()
		key = self.win.getch()
		globalLock.release()
		return key

def start_human_player():
	game = GameController(30)
	snake_win = game.start_game()
	keyDetector = KeyDetector(snake_win)
	while(True):
		if not game.getCurrentStatus:
			return
		key = keyDetector.getKey()
		if key == curses.KEY_LEFT:
			game.go_left()
		if key == curses.KEY_RIGHT:
			game.go_right()

globalLock = threading.RLock()
start_human_player()