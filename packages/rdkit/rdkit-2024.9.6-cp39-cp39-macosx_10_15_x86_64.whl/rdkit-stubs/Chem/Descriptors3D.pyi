"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x1081791f0>), ('PMI2', <function <lambda> at 0x10d6e3700>), ('PMI3', <function <lambda> at 0x10d6e3790>), ('NPR1', <function <lambda> at 0x10d6e3820>), ('NPR2', <function <lambda> at 0x10d6e38b0>), ('RadiusOfGyration', <function <lambda> at 0x10d6e3940>), ('InertialShapeFactor', <function <lambda> at 0x10d6e39d0>), ('Eccentricity', <function <lambda> at 0x10d6e3a60>), ('Asphericity', <function <lambda> at 0x10d6e3af0>), ('SpherocityIndex', <function <lambda> at 0x10d6e3b80>), ('PBF', <function <lambda> at 0x10d6e3c10>)]
