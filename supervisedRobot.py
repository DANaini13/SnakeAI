from network import Network
from snake import GameController 
import numpy as np
import time

class Controller:
    def __init__(self, network):
        self.network = network
        self.filter_func = lambda x: 1.0/(1 + np.exp(-x))
    
    def start(self):
        while(True):
            game = GameController(30)
            game.start_game()
            while(True):
                time.sleep(0.1)
                input = game.getCurrentMap()
                output = network.get_output(input)
                result = np.argmax(output)
                if result == 1:
                    game.go_left()
                elif result == 2:
                    game.go_right()
                label = game.getCurrentStatus()
                if label == False:
                    target = np.full((3), 0.45)
                    target[result] = 0.1
                    network.train(0.1, 0.9, self.filter_func, target)
                    break
            

    
network = Network([100], 900, 3)  
controller = Controller(network)
controller.start()

