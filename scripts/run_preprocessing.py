import os
import sys

# Add the root directory to sys.path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.preprocess import run_preprocessing

if __name__ == "__main__":
    print("Starting Slippi Data Preprocessing...")
    run_preprocessing()
    print("Pre-processing complete. Ready for training.")
