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
descList: list  # value = [('PMI1', <function <lambda> at 0x10b95ac20>), ('PMI2', <function <lambda> at 0x11130add0>), ('PMI3', <function <lambda> at 0x11130ae60>), ('NPR1', <function <lambda> at 0x11130aef0>), ('NPR2', <function <lambda> at 0x11130af80>), ('RadiusOfGyration', <function <lambda> at 0x11130b010>), ('InertialShapeFactor', <function <lambda> at 0x11130b0a0>), ('Eccentricity', <function <lambda> at 0x11130b130>), ('Asphericity', <function <lambda> at 0x11130b1c0>), ('SpherocityIndex', <function <lambda> at 0x11130b250>), ('PBF', <function <lambda> at 0x11130b2e0>)]
