from qTable import QLearningTable
from snakeViewController import SnakeViewController
import threading
import time
import matplotlib.pyplot as plt

### Program Args ###
block_width = 8                 # The width of the game screen (4 means this program will generate a 4x4 snake game) 
                                # Recommand 4

screen_witth = 600              # Decide the screen width of the snake game (300 mean this program will generate a snake game with 300px x 300px window)
increasingSnake = True          # Set this to True if you want the snake grows after hitting food (Recommand False for q learning)
snake_init_length = 1
show_graph = True               # Set this to Ture if you want show the graph of the training history 
                                # (Press "p" to update the graph) (Only works when the OS is focusing on the Snake game window)

fixed_food_pos = []             # Set this to a list of two numbers or empty. ([2, 2] means the snake game will only generate the food at position (2, 2))
                                # Recommand to set to not empty if you want to train less than 100 times
high_speed_training = False     # Set it to ture if you want to speed up the training. This will stop updating the game view

def start_learning():
    time.sleep(1)
    ephic = len(env.scores)
    while True:
        if ephic % 2000 == 0:
            RL.save_to_file()
            save_to_file()
        print("ephic " + str(ephic) + " ", end="")
        observation = env.reset()
        while True:
            if not high_speed_training:
                env.render()
            action = RL.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            RL.learn(str(observation), action, reward, str(observation_))
            observation = observation_
            if done:
                break
        ephic += 1

def update_plot(key):
    if key == 112:
        if len(env.scores) < 2000:
            return
        showedScores = []
        avgScores = []
        stride = len(env.scores)/1000
        temp = 0
        highest = 0
        sum = 0
        for score in env.scores:
            if temp >= stride:
                showedScores.append(highest)
                avg = sum / stride
                avgScores.append(avg)
                temp = 0
                highest = 0
                sum = 0
            temp += 1
            if highest < score:
                highest = score
            sum += score
        ax.plot(range(len(showedScores)), showedScores, "r-", lw=1)
        ax.plot(range(len(avgScores)), avgScores, "k-", lw=1)
        plt.pause(0.01)
    if key == 115:
        RL.save_to_file()
        save_to_file()

def save_to_file():
    with open("history.txt", "wt") as f:
        for score in env.scores:
            print(str(score), file=f)

RL = QLearningTable(actions=["left", "right", "none"], max_status = block_width * (block_width - 1))
env = SnakeViewController(window_size = screen_witth, block_width = block_width, snakeInitLength = 1)
if not increasingSnake:
    env.increasingSnake = False
env.fixedFoodPosition = fixed_food_pos
if show_graph:
    env.enable_keyboard_detecting(action = update_plot)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.ion()
    plt.show()
if high_speed_training:
    env.highSpeedTrainint = True
env.scores = []
with open("history.txt", "rt") as f:
    for line in f:
        env.scores.append(int(line))
        ephic = len(env.scores)

t = threading.Thread(target = start_learning)
t.start()
env.showGame()