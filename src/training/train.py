import os
from datetime import datetime

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split

from src.model.networks import SmashNet
from src.utils.dataset import SlippiDataset, collate_fn

# Hyperparameters
INPUT_SIZE = 13
OUTPUT_SIZE = 2  # Focusing on Joy X, Joy Y for now
HIDDEN_SIZE = 256
BATCH_SIZE = 1024  # Larger batches since we flatten frames
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-5
EPOCHS = 100
PROCESSED_DATA_DIR = "data/processed"
MODEL_SAVE_DIR = "models"


def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    print(f"Using device: {device}")

    # Load Dataset
    full_dataset = SlippiDataset(PROCESSED_DATA_DIR)
    if len(full_dataset) == 0:
        print("No processed data found. Run preprocessing first.")
        return

    # Split into Train/Val
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_subset, val_subset = random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(
        train_subset,
        batch_size=BATCH_SIZE // 16,  # subset of games, collate_fn will flatten them
        shuffle=True,
        num_workers=4,
        collate_fn=collate_fn,
    )
    val_loader = DataLoader(
        val_subset,
        batch_size=BATCH_SIZE // 16,
        shuffle=False,
        num_workers=4,
        collate_fn=collate_fn,
    )

    # Initialize Model
    model = SmashNet(INPUT_SIZE, OUTPUT_SIZE, HIDDEN_SIZE).to(device)
    optimizer = optim.AdamW(
        model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY
    )
    criterion = nn.MSELoss()

    best_val_loss = float("inf")

    print("Starting training...")
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0

        for inputs, targets in train_loader:
            # We only want the first 2 columns of targets (Joy X, Joy Y)
            targets = targets[:, :2]

            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, targets in val_loader:
                targets = targets[:, :2]
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()

        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)

        print(
            f"Epoch [{epoch + 1}/{EPOCHS}], Train Loss: {avg_train_loss:.6f}, Val Loss: {avg_val_loss:.6f}"
        )

        # Save Best Model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_path = os.path.join(MODEL_SAVE_DIR, f"best_model_{timestamp}.pt")
            torch.save(model.state_dict(), model_path)
            print(f"Saved best model with Val Loss: {best_val_loss:.6f}")


if __name__ == "__main__":
    if not os.path.exists(MODEL_SAVE_DIR):
        os.makedirs(MODEL_SAVE_DIR)
    train()
