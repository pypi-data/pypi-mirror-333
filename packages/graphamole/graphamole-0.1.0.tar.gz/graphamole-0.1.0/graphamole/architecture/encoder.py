"""Graph neural network encoders."""

from typing import Optional

import torch
import torch.nn as nn
from torch_geometric.nn import GINEConv


class GINEEncoder(nn.Module):
    """A graph neural network encoder using a stack of GINEConv layers."""

    def __init__(self, hidden_dim: int, num_layers: int = 2):
        """
        A graph neural network encoder using a stack of GINEConv layers.

        Parameters
        ----------
        hidden_dim
            Dimensionality of the hidden representations.
        num_layers
            Number of GINEConv layers to stack (default is 2).

        """
        super(GINEEncoder, self).__init__()
        self.layers = nn.ModuleList()
        for _ in range(num_layers):
            conv = GINEConv(
                nn.Sequential(
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.BatchNorm1d(hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                )
            )
            self.layers.append(conv)
        self.activation = nn.ReLU()

    def forward(
        self, x: torch.Tensor, edge_index: torch.Tensor, edge_attr: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Forward pass through the network.

        Parameters
        ----------
        x
            Node features.
        edge_index
            Graph connectivity.
        edge_attr
            Edge features.

        """
        for layer in self.layers:
            x = layer(x, edge_index, edge_attr)
            x = self.activation(x)
        return x
