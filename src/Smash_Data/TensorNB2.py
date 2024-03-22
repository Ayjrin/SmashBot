import Utils.ab_makeData as abn
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
    


if __name__ == "__main__":
    ## load adta
    marthGames =  GamesDataSet(inputFolder)

    ## make data loaders
    test_amount, val_amount = int(marthGames.__len__() * test_size), int(marthGames.__len__() * validation_size)

    train_set, val_set, test_set = torch.utils.data.random_split(marthGames, [
                (marthGames.__len__() - (test_amount + val_amount)), 
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
    val_dataloader = torch.utils.data.DataLoader(
                val_set,
                batch_size=batch_size,
                shuffle=True,
                collate_fn=collate_fn
    )
    test_dataloader = torch.utils.data.DataLoader(
                test_set,
                batch_size=batch_size,
                shuffle=True,
                collate_fn=collate_fn
    )

    ### trial debug

    debug_dataloader = torch.utils.data.DataLoader(
                torch.utils.data.Subset(marthGames, [0,3,4,6]),
                batch_size=1,
                shuffle=True,
                collate_fn=collate_fn,
                num_workers=2
    )

    train_dataloader2 = torch.utils.data.DataLoader(
                train_set,
                batch_size=2,
                shuffle=True,
                collate_fn=collate_fn,
    )

    # make model
    Smash1 = Net(4,2,32).cuda()



    EPOCHS = 1000

    loss_list = []
    total_count = 0
    startTime = datetime.now()
    for index in range(EPOCHS):

        for inputTensorBegin, targetTensorBeing in train_dataloader:
            inputTensor = inputTensorBegin.cuda()
            targetTensor = targetTensorBeing.cuda()

            currentTensor = Smash1(inputTensor)
            lossFunction = nn.MSELoss()
            loss = lossFunction(currentTensor, targetTensor)
            loss_list.append(loss)
            loss.backward()
            for p in Smash1.parameters():
                p.data.add_(-0.001 * p.grad)
                p.grad.data.zero_()
            total_count = total_count + 1

            if total_count % 10 == 0:
                currentTime = datetime.now()
                print()
                print(str(total_count) + " in " + str(currentTime-startTime))
                
            if total_count % 500 == 0 :

                currentTime = datetime.now()
                print()
                print(str(total_count) + " in " + str(currentTime-startTime))
                print(p.grad)
                torch.save(Smash1, "./" + str(total_count) + "_Model4.pt")

                with open("loss_list.txt", "w") as output:
                    output.write(str(loss_list))
    print("done")
