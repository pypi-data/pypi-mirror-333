"""Collection of featurizers for atoms and bonds."""

from __future__ import annotations

from typing import List

import numpy as np
from rdkit import Chem

from graphamole.featurizers.abc import TokenFeaturizer


class FeaturizerCollection:
    """Featurize an atom and bond using a collection of discrete token featurizers."""
    def __init__(
        self,
        atom_featurizers: List[TokenFeaturizer],
        bond_featurizers: List[TokenFeaturizer],
    ):
        """
        Featurize an atom and bond using a collection of discrete token featurizers.

        Parameters
        ----------
        atom_featurizers
            List of atom featurizers
        bond_featurizers
            List of bond featurizers

        """
        self.atom_featurizers = atom_featurizers
        self.bond_featurizers = bond_featurizers

    @property
    def node_feature_sizes(self) -> list[int]:
        """Returns a list of vocabulary sizes for each atom feature."""
        return [len(featurizer.vocab) for featurizer in self.atom_featurizers]

    @property
    def edge_feature_sizes(self) -> list[int]:
        """Returns a list of vocabulary sizes for each bond feature."""
        return [len(featurizer.vocab) for featurizer in self.bond_featurizers]

    def get_atom_features(self, atom: Chem.Atom) -> np.ndarray:
        """Extracts a tokenized feature vector for a single atom using all atom featurizers."""
        feature_vector = [featurizer(atom) for featurizer in self.atom_featurizers]
        return np.array(feature_vector, dtype=np.int64)

    def get_bond_features(self, bond: Chem.Bond) -> np.ndarray:
        """Extracts a tokenized feature vector for a single bond using all bond featurizers."""
        feature_vector = [featurizer(bond) for featurizer in self.bond_featurizers]
        return np.array(feature_vector, dtype=np.int64)
