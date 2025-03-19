"""Architecture for the decoder, which predicts the masked features."""

from typing import List, Optional, Tuple

import torch
import torch.nn as nn


class GraphDecoder(nn.Module):
    """Linear decoder for masked graph modeling."""

    def __init__(self, hidden_dim: int, node_target_dims: List[int], edge_target_dims: List[int]):
        """
        Linear decoder for masked graph modeling.

        The decoder predicts the full feature vector by applying a separate linear layer to the
        hidden representations for each feature dimension.

        Parameters
        ----------
        hidden_dim
            Dimensionality of the hidden representations.
        node_target_dims
            List of vocabulary sizes for node features.
        edge_target_dims
            List of vocabulary sizes for edge features.

        """
        super(GraphDecoder, self).__init__()
        self.node_decoders = nn.ModuleList([nn.Linear(hidden_dim, d) for d in node_target_dims])
        self.edge_decoders = nn.ModuleList([nn.Linear(hidden_dim, d) for d in edge_target_dims])

    def forward(
        self, h: torch.Tensor, edge_index: Optional[torch.Tensor] = None
    ) -> Tuple[List[torch.Tensor], Optional[List[torch.Tensor]]]:
        """
        Forward pass.

        Parameters
        ----------
        h
            Hidden representations.
        edge_index
            Edge indices.

        Returns
        -------
        Tuple[List[torch.Tensor], Optional[List[torch.Tensor]]]
            Node and edge predictions.
        """
        node_preds = [decoder(h) for decoder in self.node_decoders]
        if edge_index is not None:
            src = h[edge_index[0]]
            dst = h[edge_index[1]]
            edge_repr = (src + dst) / 2
            edge_preds = [decoder(edge_repr) for decoder in self.edge_decoders]
        else:
            edge_preds = None
        return node_preds, edge_preds
