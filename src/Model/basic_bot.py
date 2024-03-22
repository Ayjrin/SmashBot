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
from Decisions.agent import BaseAgent


def basic_bot():
    ## TODO :: Make own set-up function.
    console = melee.console.Console(path = DOLPHIN_PATH, slippi_address="127.0.0.1")
    controller = melee.Controller(port = 1, console = console)


    console.run()
    console.connect()

    controller.connect()
    agent = BaseAgent(controller)

    #if __name__ == '__main__':
    if True:

        while (True): 
            gamestate = console.step()
            agent.set_gamestate(gamestate)

            if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
                
                agent.random_act()
                agent.random_tilt()
                
            # adding a great comment
            else:
                melee.menuhelper.MenuHelper.menu_helper_simple(gamestate, controller, melee.enums.Character.MARTH, melee.enums.Stage.BATTLEFIELD, "", autostart=False,swag=True )
                break
        print("Done Running Bot!")