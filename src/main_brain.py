import melee as melee

import melee.enums
import melee.gamestate
from melee import PlayerState
from melee import enums
from melee import GameState
from melee import Menu
from melee import console
from melee import Button
from melee import Controller

from constants_and_config.gconsants import DOLPHIN_PATH
from Decisions.smartAgent import SmartAgent



console = melee.console.Console(path = DOLPHIN_PATH, slippi_address="127.0.0.1")
controller = melee.Controller(port = 1, console = console)


console.run()
console.connect()

controller.connect()
agent = SmartAgent(controller, modelPath='8500_Model4.pt')

if __name__ == '__main__':
    x = 0
    while (True): 
        gamestate = console.step()
        agent.set_gamestate(gamestate)
        

        if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
            x = x + 1
            print(x)
            #agent.random_act()
            #agent.random_tilt()
            
            agent.move()


            
        # adding a great comment
        else:
            melee.menuhelper.MenuHelper.menu_helper_simple(gamestate, controller, melee.enums.Character.MARTH, melee.enums.Stage.FINAL_DESTINATION, "", autostart=False,swag=True )
    print("done with everythin")

