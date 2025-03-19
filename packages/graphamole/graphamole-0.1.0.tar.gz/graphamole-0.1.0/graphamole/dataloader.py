"""Utilities for data loading."""

from typing import Optional, Tuple

from torch.utils.data import random_split
from torch_geometric.data import Dataset
from torch_geometric.loader import DataLoader


def get_dataloaders(
    dataset: Dataset,
    val_fraction: float = 0.1,
    batch_size: int = 1024,
    num_workers: int = 0,
) -> Tuple[DataLoader, Optional[DataLoader]]:
    """
    Create DataLoader objects for training and validation.

    Parameters
    ----------
    dataset
        The dataset, potentially to be split into training and validation sets.
    val_fraction
        Fraction of the dataset to use for validation. Set to ``0.0`` to return only a train
        loader.
    batch_size
        Number of samples per batch.
    num_workers
        Number of worker processes for data loading.

    Returns
    -------
    tuple
        A tuple ``(train_loader, val_loader)`` where ``val_loader`` is :py:constant:`None` if no
        validation split is used.
    """
    if val_fraction:
        total_len = len(dataset)
        val_len = int(val_fraction * total_len)
        train_len = total_len - val_len
        train_dataset, val_dataset = random_split(dataset, [train_len, val_len])
    else:
        train_dataset = dataset
        val_dataset = None

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )
    val_loader = (
        DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
        )
        if val_dataset
        else None
    )

    return train_loader, val_loader
