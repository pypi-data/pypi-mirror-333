"""Featurizers for bond-level (edge) features."""

from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import Lipinski

from graphamole.featurizers.abc import TokenFeaturizer

DEFAULT_VOCABULARY = {
    "BondType": {"single", "double", "triple", "aromatic"},
    "Stereo": {"stereoe", "stereoz", "stereoany", "stereonone"},
    # For boolean features, we use a fixed vocabulary: [False, True]
}


class BondType(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["BondType"]
        super().__init__(vocab, oov)

    def _featurize(self, bond: Chem.Bond) -> str:
        return bond.GetBondType().name.lower()


class Stereo(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["Stereo"]
        super().__init__(vocab, oov)

    def _featurize(self, bond: Chem.Bond) -> str:
        return bond.GetStereo().name.lower()


class Conjugated(TokenFeaturizer):
    def __init__(self, oov=False):
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, bond: Chem.Bond) -> bool:
        return bond.GetIsConjugated()


class Rotatable(TokenFeaturizer):
    def __init__(self, oov=False):
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, bond: Chem.Bond) -> bool:
        mol = bond.GetOwningMol()
        bond_indices = tuple(sorted([bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()]))
        rotatable_bonds = Lipinski._RotatableBonds(mol)
        return bond_indices in rotatable_bonds
