"""Featurizers for atom-level (node) features."""

from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import Lipinski

from graphamole.featurizers.abc import TokenFeaturizer

# fmt: off
DEFAULT_VOCABULARY = {
    "AtomType": {
        'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe',
        'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb',
        'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba',
        'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
        'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
        'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md',
        'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn'
    },
    "Hybridization": {"s", "sp", "sp2", "sp3", "sp3d", "sp3d2", "unspecified"},
    "CIPCode": {"R", "S", "None"},
    "FormalCharge": {-3, -2, -1, 0, 1, 2, 3, 4},
    "TotalNumHs": {0, 1, 2, 3, 4},
    "TotalValence": {0, 1, 2, 3, 4, 5, 6, 7, 8},
    "NumRadicalElectrons": {0, 1, 2, 3},
    "Degree": {0, 1, 2, 3, 4, 5, 6, 7, 8},
    "RingSize": {0, 3, 4, 5, 6, 7, 8},
    # For boolean features, we use a fixed vocabulary: [False, True]
}
# fmt: on


class AtomType(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the atom type (e.g. Na or Mg)."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["AtomType"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> str:
        return atom.GetSymbol()


class Hybridization(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the atom orbital hybridization state."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["Hybridization"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> str:
        return atom.GetHybridization().name.lower()


class CIPCode(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the atom Cahn-Ingold-Prelog (CIP) code."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["CIPCode"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> str:
        if atom.HasProp("_CIPCode"):
            return atom.GetProp("_CIPCode")
        return "None"


class FormalCharge(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the atom formal charge."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["FormalCharge"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> int:
        return atom.GetFormalCharge()


class TotalNumHs(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the total number of hydrogens on the atom."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["TotalNumHs"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> int:
        return atom.GetTotalNumHs()


class TotalValence(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the total valence of the atom."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["TotalValence"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> int:
        return atom.GetTotalValence()


class NumRadicalElectrons(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the number of radical electrons on the atom."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["NumRadicalElectrons"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> int:
        return atom.GetNumRadicalElectrons()


class Degree(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the atom degree."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["Degree"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> int:
        return atom.GetDegree()


class RingSize(TokenFeaturizer):
    def __init__(self, vocab=None, oov=True):
        """Tokenize the size of the smallest ring containing the atom; 0 if not in a ring."""
        if vocab is None:
            vocab = DEFAULT_VOCABULARY["RingSize"]
        super().__init__(vocab, oov)

    def _featurize(self, atom: Chem.Atom) -> int:
        if atom.IsInRing():
            mol = atom.GetOwningMol()
            ring_info = mol.GetRingInfo()
            ring_sizes = [len(ring) for ring in ring_info.AtomRings() if atom.GetIdx() in ring]
            if ring_sizes:
                return min(ring_sizes)
            else:
                return 0
        else:
            return 0


# Boolean features are tokenized using the fixed vocabulary [False, True].
class ChiralCenter(TokenFeaturizer):
    def __init__(self, oov=False):
        """Tokenize whether the atom is a chiral center."""
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, atom: Chem.Atom) -> bool:
        return atom.HasProp("_ChiralityPossible")


class Aromatic(TokenFeaturizer):
    def __init__(self, oov=False):
        """Tokenize whether the atom is part of an aromatic system."""
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, atom: Chem.Atom) -> bool:
        return atom.GetIsAromatic()


class Hetero(TokenFeaturizer):
    def __init__(self, oov=False):
        """Tokenize whether the atom is a heteroatom (i.e., not carbon or hydrogen)."""
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, atom: Chem.Atom) -> bool:
        mol = atom.GetOwningMol()
        hetero_atoms = [i[0] for i in Lipinski._Heteroatoms(mol)]
        return atom.GetIdx() in hetero_atoms


class HydrogenDonor(TokenFeaturizer):
    def __init__(self, oov=False):
        """Tokenize whether the atom is a hydrogen donor."""
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, atom: Chem.Atom) -> bool:
        mol = atom.GetOwningMol()
        donors = [i[0] for i in Lipinski._HDonors(mol)]
        return atom.GetIdx() in donors


class HydrogenAcceptor(TokenFeaturizer):
    def __init__(self, oov=False):
        """Tokenize whether the atom is a hydrogen acceptor."""
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, atom: Chem.Atom) -> bool:
        mol = atom.GetOwningMol()
        acceptors = [i[0] for i in Lipinski._HAcceptors(mol)]
        return atom.GetIdx() in acceptors


class Ring(TokenFeaturizer):
    def __init__(self, oov=False):
        """Tokenize whether the atom is in a ring."""
        super().__init__(vocab=[False, True], oov=oov)

    def _featurize(self, atom: Chem.Atom) -> bool:
        return atom.IsInRing()
