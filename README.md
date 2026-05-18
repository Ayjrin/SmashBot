# SmashBrosBot

A bot that smashes.

## Project Structure

- `main.py`: Unified entry point for playing and training.
- `src/bot/`: Bot agents (BaseAgent for random acts, SmartAgent for AI-driven play).
- `src/training/`: Logic for training the AI model.
- `src/utils/`: Data processing utilities.
- `src/constants_and_config/`: Configuration and paths.
- `TESTS.md`: Documentation of historical tests and experiments.

## Usage

### Prerequisites

Install the required dependencies:
```bash
pip install -r Files/requirements.txt
```

### Playing the Game

To run the bot and have it play:
```bash
python main.py play --mode smart --model 8500_Model4.pt
```
- `--mode`: `smart` (uses AI) or `base` (random acts).
- `--model`: Path to the `.pt` model file (only for smart mode).

### Training the AI

To start training:
```bash
python main.py train
```
Note: Ensure you update the data paths in `src/constants_and_config/gconsants.py` or `src/training/train.py` to point to your Slippi dataset.

## Documentation
See `TESTS.md` for details on previous experiments and potential future work.
