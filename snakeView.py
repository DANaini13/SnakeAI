import cocos
import threading
import math

class KeyDetectLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, action):
        super(KeyDetectLayer, self).__init__()
        self.action = action
        self.keys_pressed = set()

    def on_key_press (self, key, modifiers):
        self.action(key)
        self.keys_pressed.add(key)

    def on_key_release (self, key, modifiers):
        self.keys_pressed.remove(key)


class GameView:

    def show(self):
        cocos.director.director.run(self.main_scene)

    def reset(self):
        for i in range(self.block_num * self.block_num):
            self.subviews[i].position = (-100, -100)
        self.subviews[-1].position = (-100, -100)

    def setSubviewPositionWithID(self, id, position):
        if self.subviews[id]:
            x = self.__usuable_origin()[0] + self.stride * position[0]
            y = self.__usuable_origin()[1] + self.stride * (self.block_num - 1) - self.stride * position[1]
            self.subviews[id].position = (x, y) 

    def setSubviewRotationWithID(self, id, rotation):
        if id < 0 or id > self.block_num * self.block_num:
            return
        if self.subviews[id]:
            self.subviews[id].rotation = rotation

    def addKeyboardAction(self, action):
        layer = KeyDetectLayer(action)
        self.main_scene.add(layer)

    def setScore(self, score):
        self.lock.acquire()
        if self.scoreView:
            self.scoreView.element.text = "score: " + str(score)
        else:
            self.__initScoreBoard()
        self.lock.release()

    def __init__(self, screen_width = 800, block_num = 30):
        self.screen_width = screen_width
        self.screen_height = screen_width * 1.005
        self.block_num = block_num
        self.origin_x_rate = 0.0205605096
        self.origin_y_rate = 0.0229873418
        self.width_rate = 0.9620253165
        self.stride = self.__usable_width() / self.block_num
        self.subviews = {}
        self.director = cocos.director.director
        self.lock = threading.RLock()
        self.scoreView = None
        self.director.init(
	        width = int(self.screen_width),
	        height = int(self.screen_height),
	        caption="Snake Game",
	        fullscreen=False,
            autoscale=False
        )

        self.main_scene = cocos.scene.Scene()
        self.__initSubviews()

    def __initSubviews(self):
        self.__initBackground()
        self.__initHiddenSubviews()

    def __initScoreBoard(self):
        self.scoreView = cocos.text.Label(
            "score: 0",
            font_name = "Times New Roman",
            font_size = 24,
            anchor_x = "left",
            anchor_y = "bottom",
            color = (0, 0, 0, 100),
            align = "right",
            bold = False,
            width = 150
        )
        self.scoreView.position = (self.__usuable_origin()[0] + self.__usable_width() - 150 , self.__usuable_origin()[1])
        self.main_scene.add(self.scoreView)

    def __initHiddenSubviews(self):
        headView = cocos.sprite.Sprite(
                image = "Resources/body_01.png",
                anchor = (0, 0)
        )
        headView.scale = self.__usable_width() / (headView.width * self.block_num)
        headView.position = (-headView.width, -headView.width)
        self.subviews[0] = headView
        self.main_scene.add(headView)
        previous_scale = headView.scale
        final_target = 0.2 * headView.scale
        n = self.block_num * self.block_num 
        single_refect = math.pow(final_target/headView.scale, 1/(n-1))
        for i in range(self.block_num * self.block_num - 1):
            subView = cocos.sprite.Sprite(
                image = "Resources/body_02.png",
                anchor = (0, 0)
            )
            subView.scale = previous_scale * single_refect
            previous_scale = subView.scale
            subView.position = (-subView.width, -subView.width)
            self.subviews[i + 1] = subView
            self.main_scene.add(subView)

        foodView = cocos.sprite.Sprite(
            image = "Resources/food_01.png",
            anchor = (0, 0)
        )
        foodView.scale = self.__usable_width() / (foodView.width * self.block_num)
        foodView.position = (-foodView.width, -foodView.width)
        self.subviews[-1] = foodView
        self.main_scene.add(foodView)

    def __initBackground(self):
        bgView = cocos.sprite.Sprite(
            image = "Resources/background.png",
            anchor= (0, 0)
        )
        bgView.position = (0, 0)
        bgView.scale_x = self.screen_width / bgView.width
        bgView.scale_y = self.screen_height / bgView.height
        self.main_scene.add(bgView)

    def __usable_width(self):
        return self.screen_width * self.width_rate

    def __usuable_origin(self):
        return (self.screen_width * self.origin_x_rate, self.screen_height * self.origin_y_rate)
