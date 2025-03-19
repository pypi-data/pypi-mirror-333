"""Neural network module implementing masked graph modeling."""

from typing import List, Tuple

import torch
import torch.nn as nn
from torch_geometric.data import Data
from torch_geometric.nn import global_add_pool, global_max_pool, global_mean_pool

from graphamole.architecture.decoder import GraphDecoder
from graphamole.architecture.encoder import GINEEncoder


class GraphMaskingModel(nn.Module):
    """
    Implements Masked Graph Modeling (MGM) using generalized discrete featurization.

    The input is assumed to be tokenized features for nodes (shape [num_nodes, num_node_features])
    and for edges (shape [num_edges, num_edge_features]). The model builds embedding layers
    for each feature dimension (based on provided vocabulary sizes), sums them, and then applies full vector masking.
    The decoder now predicts the full feature vector (i.e. all feature dimensions) for each masked node/edge.

    """

    def __init__(
        self,
        hidden_dim: int,
        num_layers: int,
        node_feature_sizes: List[int],
        edge_feature_sizes: List[int],
        node_masking_rate: float = 0.15,
        edge_masking_rate: float = 0.15,
        pool_type: str = "sum",
    ):
        """
        Initialize the GraphMaskingModel.

        Parameters
        ----------
        hidden_dim
            Size of hidden representations.
        num_layers
            Number of GINEConv layers.
        node_feature_sizes
            Vocabulary sizes for each node feature dimension.
        edge_feature_sizes
            Vocabulary sizes for each edge feature dimension.
        node_masking_rate
            Fraction of nodes to mask.
        edge_masking_rate
            Fraction of edges to mask.
        pool_type
            Pool method: ``mean``, ``max``, or ``sum`` (default: ``sum``).
        """
        super(GraphMaskingModel, self).__init__()
        self.node_feature_sizes = node_feature_sizes
        self.edge_feature_sizes = edge_feature_sizes
        self.node_masking_rate = node_masking_rate
        self.edge_masking_rate = edge_masking_rate
        self.pool_type = pool_type

        # Create node embeddings for each feature.
        self.node_embeddings = nn.ModuleList(
            [nn.Embedding(vocab_size, hidden_dim) for vocab_size in self.node_feature_sizes]
        )
        # Create edge embeddings for each feature.
        self.edge_embeddings = nn.ModuleList(
            [nn.Embedding(vocab_size, hidden_dim) for vocab_size in self.edge_feature_sizes]
        )

        # Encoder applies GINEConv layers.
        self.encoder = GINEEncoder(hidden_dim, num_layers=num_layers)

        # Full vector decoder: predicts all feature dimensions.
        self.decoder = GraphDecoder(
            hidden_dim,
            node_target_dims=self.node_feature_sizes,
            edge_target_dims=self.edge_feature_sizes,
        )

        self.pool_fn = self._get_pool_fn(pool_type)

    def _get_pool_fn(self, pool_type: str) -> callable:
        """Get the global pool function."""
        if pool_type == "mean":
            return global_mean_pool
        elif pool_type == "max":
            return global_max_pool
        elif pool_type == "sum":
            return global_add_pool
        else:
            raise ValueError(f"Invalid pool type: {pool_type}")

    def _compute_node_embedding(self, x: torch.Tensor) -> torch.Tensor:
        """Sum node embeddings across all feature dimensions."""
        emb = 0
        for i in range(x.size(1)):
            emb = emb + self.node_embeddings[i](x[:, i])
        return emb

    def _compute_edge_embedding(self, edge: torch.Tensor) -> torch.Tensor:
        """Sum edge embeddings across all feature dimensions."""
        emb = 0
        for i in range(edge.size(1)):
            emb = emb + self.edge_embeddings[i](edge[:, i])
        return emb

    def _mask_all_features(
        self, x: torch.Tensor, mask_rate: float, feature_sizes: List[int]
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Randomly mask entire feature vectors at the given rate."""
        mask = torch.rand(x.size(0), device=x.device) < mask_rate
        x_masked = x.clone()
        for j, vocab_size in enumerate(feature_sizes):
            x_masked[mask, j] = vocab_size - 1
        return x_masked, mask

    def _mask_node_features(
        self, x: torch.Tensor, mask_rate: float
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Mask node features."""
        return self._mask_all_features(x, mask_rate, self.node_feature_sizes)

    def _mask_edge_features(
        self, edge: torch.Tensor, mask_rate: float
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Mask edge features."""
        return self._mask_all_features(edge, mask_rate, self.edge_feature_sizes)

    def forward(self, data: Data) -> dict:
        """
        Mask node/edge features, encode the graph, and decode to predict the masked features.

        Parameters
        ----------
        data
            PyTorch Geometric Data object containing node/edge features and graph structure.

        Returns
        -------
        dict
            Dictionary of predictions, masks, and targets.
        """
        original_node = data.x  # shape: [num_nodes, num_node_features]
        x_masked, node_mask = self._mask_node_features(original_node, self.node_masking_rate)
        x_emb = self._compute_node_embedding(x_masked)

        if hasattr(data, "edge_attr") and data.edge_attr is not None:
            original_edge = data.edge_attr
            edge_masked, edge_mask = self._mask_edge_features(
                original_edge, self.edge_masking_rate
            )
            edge_emb = self._compute_edge_embedding(edge_masked)
        else:
            original_edge, edge_mask, edge_emb = None, None, None

        h = self.encoder(x_emb, data.edge_index, edge_emb)
        node_preds, edge_preds = self.decoder(h, data.edge_index if edge_emb is not None else None)

        return {
            "node_pred": node_preds,  # list of logits for each node feature dimension
            "node_mask": node_mask,  # boolean mask for nodes
            "node_target": original_node,  # full node feature vectors (target)
            "edge_pred": edge_preds,  # list of logits for each edge feature dimension
            "edge_mask": edge_mask,  # boolean mask for edges
            "edge_target": original_edge if original_edge is not None else None,
        }

    def encode(self, data: Data) -> torch.Tensor:
        """
        Encode node (and edge) features into a pooled graph representation.

        Parameters
        ----------
        data
            PyTorch Geometric Data object containing node/edge features and graph structure.

        Returns
        -------
        torch.Tensor
            Pooled graph embedding of shape ``[num_graphs, hidden_dim]``.
        """
        x_emb = self._compute_node_embedding(data.x)
        if hasattr(data, "edge_attr") and data.edge_attr is not None:
            edge_emb = self._compute_edge_embedding(data.edge_attr)
        else:
            edge_emb = None
        h = self.encoder(x_emb, data.edge_index, edge_emb)
        h_pooled = self.pool_fn(h, data.batch)
        return h_pooled
