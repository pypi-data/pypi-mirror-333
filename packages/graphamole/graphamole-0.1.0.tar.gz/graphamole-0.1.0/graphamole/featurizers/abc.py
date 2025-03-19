"""Abstract base classes for featurizers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from rdkit import Chem


class TokenFeaturizer(ABC):
    """Abstract token featurizer that returns a discrete token based on a provided vocabulary."""

    def __init__(self, vocab: list, oov: bool = True):
        """
        Abstract token featurizer that returns a discrete token based on a provided vocabulary.

        Call the instance to featurize the passed atom or bond.

        Parameters
        ----------
        vocab
            List of discrete tokens.
        oov
            Whether to include an out-of-vocabulary token.

        """
        # Convert vocabulary to a list (if given as a set) and sort it.
        if isinstance(vocab, set):
            self.vocab = sorted(list(vocab))
        else:
            self.vocab = list(vocab)
        self.oov = oov
        if self.oov:
            self.vocab.append("<oov>")

    @abstractmethod
    def _featurize(self, x) -> Union[int, bool, str]:
        """Extract the raw feature from x."""
        raise NotImplementedError()

    def __call__(self, x: Union[Chem.Atom, Chem.Bond]) -> int:
        """Call the featurizer and return the index of the feature in the vocabulary."""
        feature = self._featurize(x)
        # Special handling for booleans: we assume the discrete vocabulary [False, True]
        if isinstance(feature, bool):
            bool_vocab = [False, True]
            if feature in bool_vocab:
                return bool_vocab.index(feature)
            else:
                raise ValueError(f"Boolean feature {feature} not in {bool_vocab}.")
        # For other types, look up the feature in the vocabulary.
        if feature in self.vocab:
            return self.vocab.index(feature)
        elif self.oov:
            return self.vocab.index("<oov>")
        else:
            raise ValueError(f"Feature {feature} not found in vocabulary {self.vocab}.")
