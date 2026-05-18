from src.utils import ab_makeData as abn
import peppi_py as pp


import torch
import torch.nn as nn
import torch.nn.functional as F
from matplotlib.pyplot import plot, xlim, ylim
import numpy


##
import pandas as pd
import os
from datetime import datetime


## Global Variableds
DATA_FOLDER = r"C:\Users\soph\PVV\Projects\Smash\shared_raw"
gameName = r'\02_32_35 [RUDE] Marth + [INFP] Marth (BF).slp'
test_path = DATA_FOLDER + r"\Slippi_Public_Dataset_v3" + gameName
inputFolder = DATA_FOLDER+ r"\Slippi_Public_Dataset_v3" +r"\\cleaned\\"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
inputColumns = ['x_pos', 'y_pos', 'x_pos.enemy', 'y_pos.enemy']
outputColumns = ['x_joy', 'y_joy']
enemySplitList = ['x_pos', 'y_pos', 'x_joy', 'y_joy', 'frameNumber', 'character']

test_size = .15
validation_size = .15
batch_size = 64
num_workers = 8
###

## functions

def inputStart(dfGood, dfBad):
   return dfGood.merge(dfBad.add_suffix(".enemy"), left_on='frameNumber', right_on='frameNumber.enemy')

def customDFtoTensor(inputPath : str):

    inputDF = pd.DataFrame(abn.make_pre_large(pp.read_slippi(inputPath)))


    Player0 = inputDF[inputDF['Player']=='0'][enemySplitList]
    Player1 = inputDF[inputDF['Player']=='1'][enemySplitList]

    preFinal = pd.concat([inputStart(Player0, Player1), inputStart(Player1, Player0)])
    preFinal['stage'] = inputDF['stage'][0]
    preFinal = preFinal.astype('float32')

    return preFinal


class GamesDataSet(torch.utils.data.Dataset):
    def __init__(self, image_folder, characterFilter = 'Marth'):
        self.games_folder = image_folder
        self.characterFilter = characterFilter
        self.games = self.filterGames()

    ## part of init
    def filterGames(self):
        games = []
        if not os.path.exists(self.games_folder):
            print(f"Warning: Folder {self.games_folder} does not exist.")
            return []
        for filename in os.listdir(self.games_folder):
            if self.characterFilter in filename:
                games.append(filename)
        print("total games: " + str(len(games)))
        return games

    def __getitem__(self, index):
        try:
            pathToGame = self.games_folder + r"\\" + self.games[index]
            if str(pathToGame).endswith('.pkl'):
                majority_df = pd.read_pickle(pathToGame)
            else:
                almonstFinal = customDFtoTensor(pathToGame)
                majority_df = almonstFinal[almonstFinal['character']==9.0]

            inputTensor = torch.tensor(majority_df[inputColumns].values)
            targetTensor = torch.tensor(majority_df[outputColumns].values)
        except:
            return None
            ## details hanlded in custon collate_fn

        return inputTensor, targetTensor

    def __len__(self):
        return len(self.games)



## concatenating together for ease
def collate_fn(batch):
    batch = list(filter(lambda x: x is not None, batch))
    if not batch:
        return None

    data = [item[0] for item in batch]
    data = torch.cat(data, dim=0)
    target = [item[1] for item in batch]
    target = torch.cat(target, dim=0)

    return [data, target]
    #return torch.utils.data.dataloader.default_collate(batch)

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


def run_training():
    ## load adta
    marthGames =  GamesDataSet(inputFolder)

    if len(marthGames) == 0:
        print("No games found for training. Check inputFolder.")
        return

    ## make data loaders
    test_amount, val_amount = int(marthGames.__len__() * test_size), int(marthGames.__len__() * validation_size)
    train_amount = marthGames.__len__() - (test_amount + val_amount)

    if train_amount <= 0:
        print("Not enough games for training split.")
        return

    train_set, val_set, test_set = torch.utils.data.random_split(marthGames, [
                train_amount,
                test_amount,
                val_amount
    ])

    train_dataloader = torch.utils.data.DataLoader(
                train_set,
                batch_size=batch_size,
                shuffle=True,
                collate_fn=collate_fn,
                num_workers=num_workers
    )

    # make model
    use_cuda = torch.cuda.is_available()
    Smash1 = Net(4,2,32)
    if use_cuda:
        Smash1 = Smash1.cuda()

    EPOCHS = 1000

    loss_list = []
    total_count = 0
    startTime = datetime.now()
    for index in range(EPOCHS):

        for batch in train_dataloader:
            if batch is None: continue
            inputTensorBegin, targetTensorBeing = batch

            inputTensor = inputTensorBegin
            targetTensor = targetTensorBeing
            if use_cuda:
                inputTensor = inputTensor.cuda()
                targetTensor = targetTensor.cuda()

            currentTensor = Smash1(inputTensor)
            lossFunction = nn.MSELoss()
            loss = lossFunction(currentTensor, targetTensor)
            loss_list.append(loss.item())
            loss.backward()
            for p in Smash1.parameters():
                p.data.add_(-0.001 * p.grad)
                p.grad.data.zero_()
            total_count = total_count + 1

            if total_count % 10 == 0:
                currentTime = datetime.now()
                print(f"{total_count} steps in {currentTime-startTime}, loss: {loss.item():.4f}")

            if total_count % 500 == 0 :
                currentTime = datetime.now()
                print(f"Checkpoint at {total_count} steps")
                torch.save(Smash1.state_dict(), f"./model_checkpoint_{total_count}.pt")

                with open("loss_list.txt", "w") as output:
                    output.write(str(loss_list))
    print("done")

if __name__ == "__main__":
    run_training()
