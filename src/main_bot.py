import melee
from constants_and_config.gconsants import DOLPHIN_PATH
from melee.console import Console
from Decisions.agent import BaseAgent



console = melee.console.Console(path = DOLPHIN_PATH, slippi_address="127.0.0.1", fullscreen=False, overclock=True)
controller = melee.Controller(port = 1, console = console)
controller4 = melee.Controller(port = 4, console = console)

console.run()
console.connect()

controller.connect()
controller4.connect()
agent = BaseAgent(controller)
agent2 = BaseAgent(controller4)

if __name__ == '__main__':

    while (True): 
        gamestate = console.step()
        agent.set_gamestate(gamestate)
        agent2.set_gamestate(gamestate)
        

        # If In game
        if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
            
            agent.random_act()
            agent.random_tilt()
            agent2.random_act()
            agent2.random_tilt()

            print(gamestate.players[1].position)
            print(getattr(gamestate.players[1].position, 'x'))
        
        ## If not in game
        else:
            melee.menuhelper.MenuHelper.menu_helper_simple(gamestate, controller, melee.enums.Character.MARTH, melee.enums.Stage.FINAL_DESTINATION, "", autostart=True,swag=True )
            melee.menuhelper.MenuHelper.menu_helper_simple(gamestate, controller4, melee.enums.Character.MARTH, melee.enums.Stage.FINAL_DESTINATION, "", autostart=True,swag=True )