from qTable import QLearningTable
from snakeViewController import SnakeViewController
import threading
import time
import matplotlib.pyplot as plt
from tkinter import *

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

total = 1000
counter = Counter()
block_width = 4
env = SnakeViewController(window_size = 300, block_width = block_width)
env.increasingSnake = False
env.enable_keyboard_detecting(action = update_plot)
RL = QLearningTable(actions=["left", "right", "none"], max_status = block_width * (block_width - 1))
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.ion()
plt.show()
t = threading.Thread(target = start_learning)
t.start()
env.showGame()