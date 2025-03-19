"""Dataset for molecular data with featurization."""

from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np
import torch
from rdkit import Chem
from torch_geometric.data import Data, Dataset

from graphamole.featurizers import ALL_FEATURIZERS
from graphamole.featurizers.collection import FeaturizerCollection


class MoleculeDataset(Dataset):
    """PyTorch Geometric dataset for molecular data with featurization."""

    def __init__(
        self,
        smiles: Union[str, Path, List[str]],
        featurizer_collection: Optional[FeaturizerCollection] = None,
    ):
        """
        PyTorch Geometric dataset for molecular data with featurization.

        When an item is accessed, the smiles string is converted to an RDKit
        :py:class:`~rdkit.Chem.rdchem.Mol` object from which features are extracted using the
        provided :py:class:`~graphamole.featurizers.collection.FeaturizerCollection`

        Parameters
        ----------
        smiles
            Path to a text file with SMILES strings, or a list of SMILES strings.
        featurizer_collection
            Collection of featurizers for atoms and bonds. Uses all featurizers by default.

        Examples
        --------
        >>> from graphamole.data import MoleculeDataset
        >>> smiles_list = ["CCO", "CC(=O)O"]
        >>> dataset = MoleculeDataset(smiles_list)
        >>> data = dataset[0]

        """
        super().__init__()
        self.smiles = smiles
        self.featurizer_collection = featurizer_collection or ALL_FEATURIZERS

        self._smiles_list = self._load_smiles(smiles)

    def __len__(self) -> int:
        return len(self._smiles_list)

    def __getitem__(self, idx) -> Data:
        return self.get(idx)

    @staticmethod
    def _load_smiles(smiles: Union[str, Path, List[str]]) -> List[str]:
        if isinstance(smiles, (str, Path)):
            return Path(smiles).read_text().splitlines()
        elif isinstance(smiles, list):
            return smiles
        else:
            raise ValueError("Invalid input type for SMILES.")

    @staticmethod
    def _parse_smiles(smiles: str) -> Chem.Mol:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Failed to parse SMILES: {smiles}")
        return mol

    def _get_molecule_data(
        self, smiles: str
    ) -> Tuple[List[np.ndarray], List[List[int]], List[np.ndarray]]:
        mol = self._parse_smiles(smiles)
        num_atoms = mol.GetNumAtoms()

        atom_features_list = []
        edge_indices = []
        edge_features_list = []

        for atom_idx in range(num_atoms):
            atom = mol.GetAtomWithIdx(atom_idx)
            atom_features_list.append(self.featurizer_collection.get_atom_features(atom))

        for bond in mol.GetBonds():
            i = bond.GetBeginAtomIdx()
            j = bond.GetEndAtomIdx()
            edge_indices.extend([[i, j], [j, i]])  # Include both directions.
            bond_features = self.featurizer_collection.get_bond_features(bond)
            edge_features_list.extend([bond_features, bond_features])

        return atom_features_list, edge_indices, edge_features_list

    def get(self, idx: int) -> Data:
        """Return a single data object for the instance at the requested index."""
        smiles = self._smiles_list[idx]

        atom_features_list, edge_indices, edge_features_list = self._get_molecule_data(smiles)

        x = torch.tensor(np.array(atom_features_list), dtype=torch.long)
        edge_index = torch.tensor(edge_indices, dtype=torch.long).t().contiguous()
        edge_attr = torch.tensor(np.array(edge_features_list), dtype=torch.long)

        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
