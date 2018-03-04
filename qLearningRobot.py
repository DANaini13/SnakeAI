from qTable import QLearningTable
from snakeViewController import SnakeViewController
import threading
import time

def start_learning():
    time.sleep(1)
    ephic = 0
    while True:
        print("ephic " + str(ephic) + " ", end="")
        observation = env.reset()
        while True:
            env.render()
            action = RL.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            RL.learn(str(observation), action, reward, str(observation_))
            observation = observation_
            if done:
                break
        ephic += 1


env = SnakeViewController(window_size = 300, block_width = 4)
env.increasingSnake = False
RL = QLearningTable(actions=["left", "right", "none"])
t = threading.Thread(target = start_learning)
t.start()
env.showGame()
