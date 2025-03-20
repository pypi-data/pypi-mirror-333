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
descList: list  # value = [('PMI1', <function <lambda> at 0x00000180AB6D8040>), ('PMI2', <function <lambda> at 0x00000180AB6D8680>), ('PMI3', <function <lambda> at 0x00000180AB6D87C0>), ('NPR1', <function <lambda> at 0x00000180AB6D8860>), ('NPR2', <function <lambda> at 0x00000180AB6D8900>), ('RadiusOfGyration', <function <lambda> at 0x00000180AB6D89A0>), ('InertialShapeFactor', <function <lambda> at 0x00000180AB6D8A40>), ('Eccentricity', <function <lambda> at 0x00000180AB6D8AE0>), ('Asphericity', <function <lambda> at 0x00000180AB6D8B80>), ('SpherocityIndex', <function <lambda> at 0x00000180AB6D8C20>), ('PBF', <function <lambda> at 0x00000180AB6D8CC0>)]
