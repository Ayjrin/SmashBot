## Smashbot
A bot that smashes
## People
Vlad is the goat
## Log

## 03-19-2025
- Did a bunch of working getting the actual loss working\
- Concatenating batches
- Not sure about training parameter time
- Need to implement test validation set
- Need to clean up functions
- Can only run multithreaded dataloader on a .py (no notebook, sadge)


## 03-09-2025


https://stackoverflow.com/questions/76447608/run-python-script-using-another-python-interpreter-through-the-subuprocess-modul 
should do this probably
https://stackoverflow.com/questions/67456368/pytorch-getting-runtimeerror-found-dtype-double-but-expected-float

- Good Link: https://stackoverflow.com/questions/49433936/how-do-i-initialize-weights-in-pytorch

## END
     Got the NN hooked up; NN gradient doesn't work, probably an issue with set up? Could be too low learning rate
     Need to get GPU set up; tho GPU is playable
     Have some data processing done, need some more (it is VERY bad and inefficient atm)

## 01-12-2025
- Losing my mind; seems that the command works, but gets overriden for tensorflow-probability. Also, installs a tensorflow that is too old? 
Wants tensorflow 2.18 when we default to 2.17, for whatever reason



- [Getting Tensorflow GPU for WSL](https://www.reddit.com/r/CUDA/comments/1egt346/best_setup_for_working_with_cuda_windows_vs_linux/)
- Following this guide : https://www.tensorflow.org/install/pip#windows-wsl2
    - Not sure if things need to be done in conda environment or not; I will assume not for logistics of drivers
    - the environment.yaml does however mention a bunch of cuda stuff, I wonder if this is environment specific. Worth verifying
    - Installation woes [conda](https://discuss.ai.google.dev/t/tensorflow-not-detecting-gpu-in-ubuntu-20-04-while-using-conda/30441/3) and
    (tensorflow[-and-cuda])[https://github.com/tensorflow/tensorflow/issues/62498]
    - Potential solution here : https://discuss.ai.google.dev/t/tensorflow-2-13-0-does-not-find-gpu-with-cuda-12-1/21446
    - Check this for installing directly? https://github.com/tensorflow/tensorflow/issues/61993 \ 

'''
{
conda create -n rapids-24.12 -c rapidsai -c conda-forge -c nvidia  \
rapids=24.12 python=3.10 'cuda-version>=12.0,<=12.5' \
tensorflow
}
'''

- Still need to figure out the fundamental issue with imitation learning not being parsed--found the core bug of file locations, still not sure what causes it

## 01-05-2025
- Got more of Vlad's library working.
- Got most of slippi-ai installed in WSL; need to rebuilt pypeppi 0.6.0 and install the wheel directly there (again)
- Still getting this same invalid issue with the .slps? Asked in the discord.
- Perhaps the RL training is enough with the IL pre-tuning? 
- train_rl.sh seems to work, however; when modifying it to work locally, it says it will not work on windows.
- Worth doing on WSL at this point? 
- tried getting WSL to get dolphin on it, no luck
- Getting dolphin on it is a pain; should we get the headless version of it? 


## 01-03-2025

- Much work done in SF, fighitng to specifics of Peppi
- installed WLS2 (Ubuntu 18.04)--VSCode says need to change for remote connection, not sure if true
- Is this better to run the project in regardless?
- Boto3Store issue from Vlad's code persisits on Run for selfplay RL
- question: pip install -e . : do I need to do this to update in place? 
- workflow: to get the project to work, we have to install it as a package itself, but that means modifying it means reinstalling it? 
    - does it use the binaries?

- Day End: Botostore rename not working as a package, but it is working on install.
    - Worth understanding the development environment generally, so investing in
    -  



### 12-12-2024
- Finally got py_peppi to build and install.
- Maturin build --release on .6; vlad uses .4, worth looking into.

### 08-12-2024
- Next : Ensure 0.7.0 is good, and can use in different environments. 

- Peppi built locally--maturin, cool

- Getting rust to install so I can build locally.
- Conda environments can be more than just python
- Worth looking into how to build older versions of git repos


### 07-12-2024

#### Life
- Bugs just keep happen; how to evaluate these 3 hours. 

#### A python installation deluge
- Why can't I just gitclone and run scripts directly?
    - Must I append to sys.path all the time? 
    - PATH, PYTHONPATH, sys.path
    - git clone and hit run on a file, shouldn't be impossible?
    - requirements, pyproject.toml, setup.cfg, etc?

#### Peppi headache
- peppi-py issues with install; maturin dependency. Perhaps built instead from source (seems to work)
- https://github.com/hohav/peppi-py



### 04-12-2024
resources: 
- https://github.com/vladfi1/slippi-ai;  https://pypi.org/project/peppi-py/; 
- Question: Should I use the default speedup (fizzi gecko codes) or headless?


### 03-12-2024
-Everything on github now


Ideas:

For annoyance: Optimize on Shield Break, Taunting, and Returns to scale (increasing, but capped) on not being hit.

How to train? Q-Learning vs Policy-Gradient? Especially for timeframe. 

Question: Expected Reward--does, say, it know a lower shield on the enemy means more likely to achieve shield break? 


###
Need to import some things specifically, such as gamestate packages

### 7th September 2024
 - Slippi vs Peppi for parsing?
 - Initial Random Forrest--would like to avoid PD, but want a pre-processed dataframe format
 - Initial Imitation NN : Simply One Layer Deep Predictive Easiest (Perhaps Start Here)

Relevant Docs:
- https://peppi-py.readthedocs.io/en/latest/index.html
- slippi wiki https://github.com/project-slippi/slippi-wiki/blob/master/SPEC.md
- Vlad's Libmelee (Speedup!) https://github.com/vladfi1/libmelee?tab=readme-ov-file
- Phillip : https://github.com/vladfi1/DeepSmash/tree/master
