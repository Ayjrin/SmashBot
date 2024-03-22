from melee import Button
from melee import controller
from melee import enums as menums
import random
from melee import GameState



global_button = ""
button_options = [e for e in (list(menums.Button)) if e not in (menums.Button.BUTTON_START, menums.Button.BUTTON_MAIN)]

#button_options = (list(menums.Button).remove(menums.Button.BUTTON_MAIN))

def press_random(in_controller : controller):
    global_button = random.choice(button_options)
    in_controller.press_button(global_button)
    print(global_button)

def release_random(in_controller : controller):
    in_controller.release_button(global_button)

