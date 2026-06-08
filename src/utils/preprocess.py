import hashlib
import os

import numpy as np
import pandas as pd
import torch

from src.utils.parser import parse_slp

# Configuration for Preprocessing
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
CHARACTER_FILTER = (
    9.0  # Marth ID in peppi-py/slippi is usually 9 or similar, check constant
)
# For now, let's keep all characters and filter in the dataset if needed,
# but preprocessing everything is safer.


def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def normalize_state(df):
    """
    Normalizes the state features in the DataFrame.
    """
    # SSBM stages are roughly centered at 0,0.
    # Positions can go up to ~200.
    # We'll scale them to be roughly in the [-1, 1] range.
    pos_scale = 100.0
    df["self_x"] /= pos_scale
    df["self_y"] /= pos_scale
    df["opp_x"] /= pos_scale
    df["opp_y"] /= pos_scale

    # Percents go from 0 to 999.
    df["self_percent"] /= 100.0
    df["opp_percent"] /= 100.0

    # Stocks 0-4
    df["self_stocks"] /= 4.0
    df["opp_stocks"] /= 4.0

    return df


def add_velocities(df):
    """
    Adds self and opponent velocities by calculating differences between frames.
    Note: This will result in NaNs for the first frame of each game.
    """
    # Group by port to ensure we don't calculate velocity across different players/games
    # Since we process one game at a time, we just group by port.
    for port in df["port"].unique():
        mask = df["port"] == port
        df.loc[mask, "self_x_vel"] = df.loc[mask, "self_x"].diff().fillna(0)
        df.loc[mask, "self_y_vel"] = df.loc[mask, "self_y"].diff().fillna(0)
        df.loc[mask, "opp_x_vel"] = df.loc[mask, "opp_x"].diff().fillna(0)
        df.loc[mask, "opp_y_vel"] = df.loc[mask, "opp_y"].diff().fillna(0)

    return df


def run_preprocessing():
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.makedirs(PROCESSED_DATA_DIR)

    raw_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".slp")]
    print(f"Found {len(raw_files)} raw .slp files.")

    for filename in raw_files:
        raw_path = os.path.join(RAW_DATA_DIR, filename)

        # Check if already processed (could use hash, but filename is usually enough for local dev)
        # file_hash = get_file_hash(raw_path)
        processed_path = os.path.join(PROCESSED_DATA_DIR, f"{filename}.pt")

        if os.path.exists(processed_path):
            print(f"Skipping {filename}, already processed.")
            continue

        print(f"Processing {filename}...")
        df = parse_slp(raw_path)

        if df is None or df.empty:
            print(f"Skipping {filename}, no valid data found.")
            continue

        # Feature Engineering
        df = add_velocities(df)
        df = normalize_state(df)

        # Define Input and Output columns
        input_cols = [
            "self_x",
            "self_y",
            "self_x_vel",
            "self_y_vel",
            "self_percent",
            "self_state",
            "self_jumps",
            "opp_x",
            "opp_y",
            "opp_x_vel",
            "opp_y_vel",
            "opp_percent",
            "opp_state",
        ]
        output_cols = ["target_joy_x", "target_joy_y", "target_buttons"]

        # Convert to Tensors
        # We store metadata (like port, char, stage) separately or as part of the filename if needed
        # For now, let's just store the tensors for each player separately

        for port in df["port"].unique():
            port_df = df[df["port"] == port].copy()

            # Filter for specific character if needed (Marth is 9.0)
            if CHARACTER_FILTER and port_df["char"].iloc[0] != CHARACTER_FILTER:
                continue

            inputs = torch.tensor(port_df[input_cols].values, dtype=torch.float32)
            targets = torch.tensor(port_df[output_cols].values, dtype=torch.float32)

            data = {
                "inputs": inputs,
                "targets": targets,
                "metadata": {
                    "filename": filename,
                    "port": port,
                    "char": port_df["char"].iloc[0],
                    "stage": port_df["stage"].iloc[0],
                },
            }

            save_name = f"{filename}_port{port}.pt"
            torch.save(data, os.path.join(PROCESSED_DATA_DIR, save_name))

    print("Preprocessing complete.")


if __name__ == "__main__":
    run_preprocessing()
