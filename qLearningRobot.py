from qTable import QLearningTable
from snakeViewController import SnakeViewController
import threading
import time
import matplotlib.pyplot as plt
from tkinter import *

### Program Args ###
total = 10000                   # Training times.
block_width = 4                 # The width of the game screen (4 means this program will generate a 4x4 snake game) 
                                # Recommand 4

screen_witth = 300              # Decide the screen width of the snake game (300 mean this program will generate a snake game with 300px x 300px window)
increasingSnake = False         # Set this to True if you want the snake grows after hitting food (Recommand False for q learning)
show_graph = False              # Set this to Ture if you want show the graph of the training history 
                                # (Press "p" to update the graph) (Only works when the OS is focusing on the Snake game window)

fixed_food_pos = []             # Set this to a list of two numbers or empty. ([2, 2] means the snake game will only generate the food at position (2, 2))
                                # Recommand to set to not empty if you want to train less than 100 times



class Counter:
    def __init__(self):
        self.counter = 0
        self.lock = threading.RLock()
    
    def increate(self):
        self.lock.acquire()
        self.counter += 1
        self.lock.release()

    def getCounter(self):
        return self.counter

def start_learning():
    time.sleep(1)
    for _ in range(total):
        print("ephic " + str(counter.getCounter()) + " ", end="")
        observation = env.reset()
        while True:
            env.render()
            action = RL.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            RL.learn(str(observation), action, reward, str(observation_))
            observation = observation_
            if done:
                break
        counter.increate()

def update_plot(key):
    if key == 112:
        lines = ax.plot(range(counter.getCounter()), env.scores, "r-", lw=1)
        plt.pause(0.01)

counter = Counter()
RL = QLearningTable(actions=["left", "right", "none"], max_status = block_width * (block_width - 1))
env = SnakeViewController(window_size = screen_witth, block_width = block_width)
if not increasingSnake:
    env.increasingSnake = False
env.fixedFoodPosition = fixed_food_pos
if show_graph:
    env.enable_keyboard_detecting(action = update_plot)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.ion()
    plt.show()
t = threading.Thread(target = start_learning)
t.start()
env.showGame()