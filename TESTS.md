# SmashBrosBot Tests

This document summarizes the tests and experiments conducted during development.

## Historical Tests (Consolidated from Notebooks)

### 1. Slippi File Parsing (`playground.ipynb`)
- **Goal:** Verify that `.slp` files can be read using the `slippi` library.
- **Outcome:** Successfully extracted frame data, character positions, and button states from sample games.
- **Key Code:** `Game(test_game).frames[400].ports[3].leader.pre.buttons`

### 2. Peppi Data Processing (`PG.ipynb`, `Initial_Notebook.ipynb`)
- **Goal:** Use `peppi_py` for faster parsing and `pandas` for data manipulation.
- **Outcome:** Created dataframes containing player positions and actions for training.
- **Key Code:** `pp.read_slippi(path)` and merging player dataframes on `frameNumber`.

### 3. Neural Network Training (`TensorNB.ipynb`, `TensorNB2.ipynb`)
- **Goal:** Train a PyTorch model to predict joystick inputs based on character positions.
- **Outcome:** Developed a 5-layer MLP (`Net`) and a custom `GamesDataSet` for batch training.
- **Status:** Initial models saved as `.pt` files (e.g., `8500_Model4.pt`).

## Potential Future Tests
- **Reinforcement Learning:** Testing Q-Learning or Policy Gradient approaches for live training.
- **Reward Function Optimization:** Experimenting with rewards for shield breaks, taunts, and avoiding hits.
- **Multi-character Support:** Training models on characters other than Marth.
- **GPU Performance:** Measuring training speedups using CUDA in different environments (Windows vs. WSL).
