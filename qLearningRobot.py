from qTable import QLearningTable
from snakeViewController import SnakeViewController
import threading
import time

def start_learning():
    x = 0
    while True:
        time.sleep(0.2)   #waiting for the game start
        print("epoch " + str(x), end=" ")
        state = snakeViewController.reset()
        if x % 100 == 0:
            RL.print_table()
        while True:
            time.sleep(0.1)
            action = RL.choose_action(state)
            nextState, reward, done = snakeViewController.step(action)
            RL.learn(state, action, reward, nextState)
            state = nextState
            if done:
                break
        x += 1

snakeViewController = SnakeViewController(window_size = 300, block_width = 4)
snakeViewController.increasingSnake = False
RL = QLearningTable(actions=["left", "right", "none"])
t = threading.Thread(target = start_learning)
t.start()
snakeViewController.start_game()
