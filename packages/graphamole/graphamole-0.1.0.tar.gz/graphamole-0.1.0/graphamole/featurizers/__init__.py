"""
Extract features from RDKit atom and bond objects.

Each featurizer is a callable that takes an RDKit atom or bond object as input
and returns a discrete token based on a predefined vocabulary. Individual featurizers should be
combined in a ``FeaturizerCollection`` to extract all added features for an atom or bond.

For example:

.. code-block:: python

    from rdkit import Chem
    from graphamole.featurizers import atom, bond, collection

    # Example atom and bond
    atom = Chem.Atom(6)  # Carbon atom
    bond = Chem.BondType.SINGLE  # Single bond

    # Create a collection of atom and bond featurizers
    featurizer_collection = collection.FeaturizerCollection(
        atom_featurizers=[atom.AtomType(), atom.Hybridization(), atom.CIPCode()],
        bond_featurizers=[bond.BondType(), bond.Stereo()],
    )

    # Extract all atom features
    atom_features = featurizer_collection.get_atom_features(atom)

    # Extract all bond features
    bond_features = featurizer_collection.get_bond_features(bond)


"""

from graphamole.featurizers import atom, bond, collection

ALL_FEATURIZERS = collection.FeaturizerCollection(
    atom_featurizers=[
        atom.AtomType(),
        atom.Hybridization(),
        atom.CIPCode(),
        atom.FormalCharge(),
        atom.TotalNumHs(),
        atom.TotalValence(),
        atom.NumRadicalElectrons(),
        atom.Degree(),
        atom.RingSize(),
        atom.ChiralCenter(),
        atom.Aromatic(),
        atom.Hetero(),
        atom.HydrogenDonor(),
        atom.HydrogenAcceptor(),
        atom.Ring(),
    ],
    bond_featurizers=[
        bond.BondType(),
        bond.Stereo(),
        bond.Conjugated(),
        bond.Rotatable(),
    ],
)
