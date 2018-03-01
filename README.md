# Machine Learning Final Group Project

### Environment Requirements:
> 1. Cocos2d python 
> 2. python3.x
> 3. Numpy

### Run With Human Player:
> 1. Run ```python humanPlayer.py``` or ```python3 humanPlayer.py``` in the Terminal or CMD Tools
> 2. Press Left key to turn left, Right key to turn right
> 3. Pres ESC to exit the game

### Run With Q-Learning Robot:
Since Q-Learning Algorithm is built base on the game status, this game should be as less statuses as we can.
Following instructions will make the game contains less than 16! statuses.
(imaging this algorthm is building a state machine that describe the player logic) 

> 1. Replace the ```line24``` of the ```qLearningRobot.py``` with
   ```snakeViewController = SnakeViewController(window_size = 300, block_width = 4)```
> 2. Set the increasingSnake to ```False``` in the ```line10``` of ```snakeViewController.py```
> 3. Run ```python qLearningRobot.py``` or ```python3 qLearningRobot.py``` in the Terminal or CMD Tools
> 4. Wait for training the robot (could be really slow, small changes before epoch 100000)
> 5. Use Ctrl-C in the Terminal to stop learning