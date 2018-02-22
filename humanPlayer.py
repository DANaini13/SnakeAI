from snake import GameController, KeyDetector
import curses

game = GameController(30)
snake_win = game.start_game()
keyDetector = KeyDetector(snake_win)
while(True):
    key = keyDetector.getKey()
    if key == 27:
        game.cancelGame()
        break
    if key == curses.KEY_LEFT:
        game.go_left()
    if key == curses.KEY_RIGHT:
        game.go_right()