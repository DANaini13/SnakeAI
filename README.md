# Machine Learning Final Group Project

### Environment Requirements:
> 1. Python3.x
> 2. Cocos2d python 
> 3. Numpy and Pandas (for Robots)
> 4. TensorFlow (for Deep Q Leaning Robot Only)

### Run With Human Player:
> 1. Run ```python humanPlayer.py``` or ```python3 humanPlayer.py``` in the Terminal or CMD Tools
> 2. Press Left key to turn left, Right key to turn right
> 3. Pres ESC to exit the game

### Run With Q Learning Robot:
Since Q-Learning Algorithm is built base on the game status, this game should be as less statuses as we can.
Following instructions will make the game contains less than 43680 statuses.
(imaging this algorthm is building a state machine that describe the player logic) 

> 1. Run ```python qLearningRobot.py``` or ```python3 qLearningRobot.py``` in the Terminal or CMD Tools
> 2. Wait for training the robot (could be really slow, small changes before getting most of the statuses in Q table)
> 3. Use Ctrl-C in the Terminal to stop learning

### Run With Deep Q Learning Robot:
To be continued...