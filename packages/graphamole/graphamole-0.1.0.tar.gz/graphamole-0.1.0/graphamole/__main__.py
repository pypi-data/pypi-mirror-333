"""Graphamole command-line interface."""

from __future__ import annotations

import logging
import random
from multiprocessing import cpu_count
from typing import Optional

import pytorch_lightning as pl
import torch
import typer
import wandb
from pytorch_lightning.loggers import WandbLogger

from graphamole.data import MoleculeDataset
from graphamole.dataloader import get_dataloaders
from graphamole.lightning import GraphMaskingLightningModule

LOGGER = logging.getLogger(__name__)
CLI_APP = typer.Typer(
    pretty_exceptions_show_locals=False,
)


@CLI_APP.command()
def train(
    smiles_path: str,
    model_path: Optional[str] = None,
    val_fraction: float = 0.2,
    batch_size: int = 1024,
    max_epochs: int = 5,
    devices: int = 1,
    num_workers: Optional[int] = None,
    hidden_dim: int = 512,
    num_layers: int = 5,
    learning_rate: float = 1e-3,
    use_wandb: bool = False,
    wandb_project: Optional[str] = None,
    wandb_entity: Optional[str] = None,
):
    """Train or finetune a Graphamole embedder using masked graph modeling."""
    torch.set_float32_matmul_precision("medium")
    torch.manual_seed(42)
    random.seed(42)

    if not num_workers:
        num_workers = cpu_count() // 2 - 1

    if use_wandb:
        wandb.init(project=wandb_project, entity=wandb_entity)
        # Override hyperparameters from wandb sweeps if available
        if hasattr(wandb, "config"):
            hidden_dim = wandb.config.get("hidden_dim", hidden_dim)
            num_layers = wandb.config.get("num_layers", num_layers)
            learning_rate = wandb.config.get("learning_rate", learning_rate)

    LOGGER.info("Reading SMILES file...")
    dataset = MoleculeDataset(smiles_path)

    train_loader, val_loader = get_dataloaders(
        dataset,
        val_fraction=val_fraction,
        batch_size=batch_size,
        num_workers=num_workers,
    )

    if model_path:
        lightning_model = GraphMaskingLightningModule.load_from_checkpoint(
            model_path,
            learning_rate=learning_rate,
        )
    else:
        lightning_model = GraphMaskingLightningModule(
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            node_feature_sizes=dataset.featurizer_collection.node_feature_sizes,
            edge_feature_sizes=dataset.featurizer_collection.edge_feature_sizes,
            node_masking_rate=0.15,
            edge_masking_rate=0.15,
            learning_rate=learning_rate,
        )

    if use_wandb:
        logger = WandbLogger()
        logger.experiment.watch(lightning_model)
    else:
        logger = None

    LOGGER.info("Fitting model...")
    trainer = pl.Trainer(
        devices=devices,
        max_epochs=max_epochs,
        logger=logger,
        enable_checkpointing=False,
        val_check_interval=0.5,
    )
    trainer.fit(lightning_model, train_dataloaders=train_loader, val_dataloaders=val_loader)

    LOGGER.info("Saving model...")
    model_filename = wandb.run.name if use_wandb else "model"
    trainer.save_checkpoint(f"{model_filename}.ckpt")

    if use_wandb:
        wandb.finish()


@CLI_APP.command()
def embed(
    smiles_path: str,
    model_path: str,
    output_path: str,
    num_workers: Optional[int] = None,
    devices: int = 1,
    use_lightning_trainer: bool = True,
):
    """Embed molecules using a trained Graphamole model."""
    torch.set_float32_matmul_precision("medium")
    torch.manual_seed(42)
    random.seed(42)

    if not num_workers:
        num_workers = cpu_count() // 2 - 1

    LOGGER.info("Reading SMILES file...")
    dataset = MoleculeDataset(smiles_path)

    LOGGER.info("Loading model...")
    lightning_model = GraphMaskingLightningModule.load_from_checkpoint(model_path)

    LOGGER.info("Embedding molecules...")
    if use_lightning_trainer:
        trainer = pl.Trainer(
            devices=devices,
            logger=None,
            enable_checkpointing=False,
        )
        embeddings = trainer.predict(lightning_model, dataset)
    else:
        embeddings = lightning_model.encode(dataset)

    LOGGER.info("Saving embeddings...")
    torch.save(embeddings, output_path)


def main():
    logging.basicConfig()
    CLI_APP()


if __name__ == "__main__":
    main()
