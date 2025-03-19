"""Lightning module for training and inference."""

from typing import List

import pytorch_lightning as pl
import torch
import torch.nn as nn
from torch_geometric.data import Data

from graphamole.architecture.graph_masking import GraphMaskingModel


class GraphMaskingLightningModule(pl.LightningModule):
    """PyTorch Lightning module for the GraphMaskingModel."""

    def __init__(
        self,
        hidden_dim: int,
        num_layers: int,
        node_feature_sizes: List[int],
        edge_feature_sizes: List[int],
        node_masking_rate: float = 0.15,
        edge_masking_rate: float = 0.15,
        learning_rate: float = 1e-3,
    ):
        """
        PyTorch Lightning module for the GraphMaskingModel.

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
        learning_rate
            Learning rate for the optimizer

        """
        super().__init__()
        self.save_hyperparameters()

        self.model = GraphMaskingModel(
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            node_masking_rate=node_masking_rate,
            edge_masking_rate=edge_masking_rate,
            node_feature_sizes=node_feature_sizes,
            edge_feature_sizes=edge_feature_sizes,
        )
        self.learning_rate = learning_rate
        self.node_loss_fn = nn.CrossEntropyLoss()
        self.edge_loss_fn = nn.CrossEntropyLoss()

    def forward(self, data: Data) -> dict:
        """Forward pass."""
        return self.model.forward(data)

    def encode(self, data: Data) -> torch.Tensor:
        """Encode data into molecular embeddings."""
        return self.model.encode(data)

    def training_step(self, batch: Data, batch_idx: int) -> torch.Tensor:
        """Forward pass and compute training loss."""
        outputs = self.forward(batch)
        return self._compute_loss(outputs, batch, prefix="train")

    def validation_step(self, batch: Data, batch_idx: int) -> torch.Tensor:
        """Forward pass and compute validation loss."""
        outputs = self.forward(batch)
        return self._compute_loss(outputs, batch, prefix="val")

    def test_step(self, batch: Data, batch_idx: int) -> torch.Tensor:
        """Forward pass and compute test loss."""
        outputs = self.forward(batch)
        return self._compute_loss(outputs, batch, prefix="test")

    def predict_step(self, batch: Data, batch_idx: int) -> torch.Tensor:
        """Forward pass and return molecular embeddings."""
        return self.encode(batch)

    def configure_optimizers(self) -> torch.optim.Optimizer:
        """Configure optimizer."""
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

    def _compute_loss(self, outputs: dict, batch: Data, prefix: str) -> torch.Tensor:
        """Compute and log losses."""
        loss = 0.0

        # Compute node loss if any nodes are masked.
        if outputs["node_mask"] is not None and outputs["node_mask"].any():
            node_loss = 0.0
            for i, pred in enumerate(outputs["node_pred"]):
                node_loss += self.node_loss_fn(
                    pred[outputs["node_mask"]], outputs["node_target"][outputs["node_mask"], i]
                )
            node_loss = node_loss / len(outputs["node_pred"])
            loss += node_loss
            self.log(f"{prefix}_node_loss", node_loss, batch_size=batch.num_graphs, prog_bar=True)

        # Compute edge loss if any edges are masked.
        if (
            outputs["edge_pred"] is not None
            and outputs["edge_mask"] is not None
            and outputs["edge_mask"].any()
        ):
            edge_loss = 0.0
            for i, pred in enumerate(outputs["edge_pred"]):
                edge_loss += self.edge_loss_fn(
                    pred[outputs["edge_mask"]], outputs["edge_target"][outputs["edge_mask"], i]
                )
            edge_loss = edge_loss / len(outputs["edge_pred"])
            loss += edge_loss
            self.log(f"{prefix}_edge_loss", edge_loss, batch_size=batch.num_graphs, prog_bar=True)

        self.log(f"{prefix}_loss", loss, batch_size=batch.num_graphs, prog_bar=True)

        return loss
