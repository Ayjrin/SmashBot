from melee import Button
from melee import controller
from melee import enums as menums
import random
from melee import GameState

class BaseAgent:
    """An agent that sees the gamestate and uses a controller"""

    button_options = [e for e in (list(menums.Button)) if e not in (menums.Button.BUTTON_START, menums.Button.BUTTON_MAIN)]
    gamestate = ""
    previous_frame_action = False

    def __init__(self, controller : controller) -> None:
        self.current_controller = controller
        self.last_button = ""


    def press_x(self):
        self.current_controller.press_button(menums.Button.BUTTON_X)

    def release_x(self):
        self.current_controller.release_button(menums.Button.BUTTON_X)

    def press_random(self):
        if self.get_gamestate().distance < 20 :
            self.last_button = menums.Button.BUTTON_X
            self.current_controller.press_button(self.last_button)
            return
        else :
            self.last_button = random.choice(BaseAgent.button_options)
            self.current_controller.press_button(self.last_button)
            return

    def release_random(self):
        self.current_controller.release_button(self.last_button)

    def random_tilt(self):
        x = random.random()
        y = (random.random())/2
        self.current_controller.tilt_analog(menums.Button.BUTTON_MAIN, x,y)


    def random_act(self):
        if not self.previous_frame_action:
            self.press_random()
            self.previous_frame_action = not self.previous_frame_action
        else:
            self.release_random()
            self.previous_frame_action = not self.previous_frame_action

    


## getter and seter for gamestate
    def set_gamestate(self, gamestate_input : GameState):
        self.gamestate = gamestate_input

    def get_gamestate(self):
        return self.gamestate