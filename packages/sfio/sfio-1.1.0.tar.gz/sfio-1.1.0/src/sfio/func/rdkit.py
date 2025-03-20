import pandas as pd

from . import ERROR


class Atoms:
    """Custom internal data structure for atoms and topology"""

    def __init__(self, src, srctype):
        self.source = src
        self.source_type = srctype

        self.parse = getattr(self, f"from_{srctype}", None)
        if self.parse is None:
            ERROR(f"cannot create atoms from '{srctype}'", TypeError)

        self.df, self.topo = self.parse(src)

    def from_smiles(self, smiles):
        try:
            from rdkit.Chem import AllChem as Chem
        except ModuleNotFoundError:
            ERROR("RDKit required. Try pip install rdkit.")

        mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
        Chem.EmbedMultipleConfs(mol, 1, randomSeed=0xF00D)
        Chem.MMFFOptimizeMoleculeConfs(mol)

        atoms = {
            'index': 'GetIdx',
            'symbol': 'GetSymbol',
            'num_neigh': 'GetTotalDegree',
            'formal_charge': 'GetFormalCharge',
            'mass': 'GetMass',
            'isotope': 'GetIsotope',
            'is_aromatic': 'GetIsAromatic',
        }
        data = {k: [] for k in atoms}

        # atom attributes
        for i, atom in enumerate(mol.GetAtoms()):
            for k, func in atoms.items():
                data[k].append(getattr(atom, func)())

        # coordinates
        coord = mol.GetConformer().GetPositions()
        data['x'] = coord[:, 0]
        data['y'] = coord[:, 1]
        data['z'] = coord[:, 2]

        self.rdkitmol = mol
        atoms = pd.DataFrame(data, index=data.pop('index'))
        #        atoms.attrs['masses'] = {
        #            'id': [], 'mass': [], 'label': []
        #            for i, element in
        #        }
        topo = None
        return atoms, topo

    def savefig(self, fpath, **kwargs):
        from rdkit.Chem import Draw

        options = Draw.MolDraw2DCairo(1, 1).drawOptions()
        options.addAtomIndices = True

        kwargs.setdefault('size', (800, 800))
        kwargs.setdefault('options', options)

        Draw.MolToFile(self.rdkitmol, 'monomer.png', **kwargs)
