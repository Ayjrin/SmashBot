import os

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset


class SlippiDataset(Dataset):
    """
    Loads preprocessed .pt files for training.
    """

    def __init__(self, data_dir, split_file=None):
        self.data_dir = data_dir
        if split_file:
            # Load specific files listed in a CSV/txt if we want controlled splits
            self.files = pd.read_csv(split_file)["filename"].tolist()
        else:
            # Just load everything in the directory
            self.files = [f for f in os.listdir(data_dir) if f.endswith(".pt")]

        print(f"Dataset initialized with {len(self.files)} games.")

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        file_path = os.path.join(self.data_dir, self.files[idx])
        data = torch.load(file_path)

        # Each .pt file contains 'inputs' and 'targets' tensors
        # inputs shape: (num_frames, state_dim)
        # targets shape: (num_frames, action_dim)

        return data["inputs"], data["targets"]


def collate_fn(batch):
    """
    Concatenates frames from multiple games into a single batch.
    Since games have different lengths, we flatten them into a large
    pool of frames for Behavioral Cloning (which is frame-wise).
    """
    inputs = torch.cat([item[0] for item in batch], dim=0)
    targets = torch.cat([item[1] for item in batch], dim=0)
    return inputs, targets


def get_dataloader(data_dir, batch_size=64, num_workers=4, shuffle=True):
    dataset = SlippiDataset(data_dir)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=collate_fn,
    )


if __name__ == "__main__":
    # Test loading
    pass
