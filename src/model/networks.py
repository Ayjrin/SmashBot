import torch
import torch.nn as nn
import torch.nn.functional as F


class SmashNet(nn.Module):
    """
    A robust MLP for Behavioral Cloning.
    Uses ReLU activations and Dropout for regularization.
    """

    def __init__(self, input_size, output_size, hidden_size=256):
        super(SmashNet, self).__init__()

        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_size),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size * 2),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_size * 2),
            nn.Dropout(0.2),
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_size),
            nn.Linear(hidden_size, output_size),
        )

    def forward(self, x):
        return self.net(x)


# Example usage/debugging
if __name__ == "__main__":
    model = SmashNet(13, 2)  # Joy X, Joy Y only for now
    test_input = torch.randn(5, 13)
    output = model(test_input)
    print(output.shape)
