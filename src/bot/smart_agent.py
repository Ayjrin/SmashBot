from melee import Button
from melee import controller
from melee import enums as menums
import random
from melee import GameState
import torch

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy




class Net(nn.Module):
    def __init__(self, input_size, output_size, layerSize):
        super(Net,self).__init__()
        self.fc1 = nn.Linear(input_size, layerSize)
        self.fc2 = nn.Linear(layerSize,layerSize)
        self.fc3 = nn.Linear(layerSize,layerSize)
        self.fc4 = nn.Linear(layerSize,layerSize)
        self.fc5 = nn.Linear(layerSize,layerSize)
        self.fc6 = nn.Linear(layerSize, output_size)

    def forward(self, x):
        x = F.sigmoid(self.fc1(x))
        x = F.sigmoid(self.fc2(x))
        x = F.sigmoid(self.fc3(x))
        x = F.sigmoid(self.fc4(x))
        x = F.sigmoid(self.fc5(x))
        x = self.fc6(x)
        return x

torch.serialization.add_safe_globals([Net])

class SmartAgent:
    """An agent that sees the gamestate and uses a controller"""

    button_options = [e for e in (list(menums.Button)) if e not in (menums.Button.BUTTON_START, menums.Button.BUTTON_MAIN)]
    gamestate = ""
    previous_frame_action = False

    def __init__(self, controller : controller, modelPath) -> None:
        self.current_controller = controller
        self.modelPath = modelPath
        self.model = self.loadModel()
        self.last_button = ""

    # only called during initlization
    def loadModel(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading model on {device}")

        try:
            # Load the state dict or model
            checkpoint = torch.load(self.modelPath, weights_only=False, map_location=device)

            # If it's a full model, we might just need its state dict
            if isinstance(checkpoint, nn.Module):
                state_dict = checkpoint.state_dict()
            else:
                state_dict = checkpoint

            Smash2 = Net(4,2,32)
            Smash2.load_state_dict(state_dict)
            Smash2.to(device)
            Smash2.eval()
            print("Successfully Loaded")
            return Smash2
        except Exception as e:
            print(f"Error loading model: {e}")
            raise


    def press_x(self):
        self.current_controller.press_button(menums.Button.BUTTON_X)

    def release_x(self):
        self.current_controller.release_button(menums.Button.BUTTON_X)

    def release_random(self):
        self.current_controller.release_button(self.last_button)

    def random_tilt(self):
        x = random.random()
        y = (random.random())/2
        print("x " + str(x) + " y " + str(y))
        self.current_controller.tilt_analog(menums.Button.BUTTON_MAIN, x,y)

    def move_Stick(self, x_in,y_in):
        x = x_in
        y = y_in
        print("x " + str(x) + " y " + str(y))
        self.current_controller.tilt_analog_unit(menums.Button.BUTTON_MAIN, x,y)


    def getModelInput(self):
        ### hardcode into start. Bot itself is "1", opponent will be 4 always
        ourX =  getattr(self.gamestate.players[1].position, 'x')
        ourY = getattr(self.gamestate.players[1].position, 'y')

        enemX = getattr(self.gamestate.players[4].position, 'x')
        enemy = getattr(self.gamestate.players[4].position, 'y')

        return torch.tensor([ourX,ourY,enemX,enemy]).to(dtype=torch.float32)

    def move(self):
        output = self.model(self.getModelInput()).detach().numpy()
        x_main = float(output[0])
        y_main = float(output[1])

        self.move_Stick(x_main, y_main)





## getter and seter for gamestate
    def set_gamestate(self, gamestate_input : GameState):
        self.gamestate = gamestate_input

    def get_gamestate(self):
        return self.gamestate
