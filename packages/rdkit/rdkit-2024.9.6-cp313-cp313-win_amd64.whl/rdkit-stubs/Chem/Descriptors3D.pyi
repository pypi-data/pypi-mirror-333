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
descList: list  # value = [('PMI1', <function <lambda> at 0x000001A7630ADC60>), ('PMI2', <function <lambda> at 0x000001A7630AE3E0>), ('PMI3', <function <lambda> at 0x000001A7630AE480>), ('NPR1', <function <lambda> at 0x000001A7630AE520>), ('NPR2', <function <lambda> at 0x000001A7630AE5C0>), ('RadiusOfGyration', <function <lambda> at 0x000001A7630AE660>), ('InertialShapeFactor', <function <lambda> at 0x000001A7630AE700>), ('Eccentricity', <function <lambda> at 0x000001A7630AE7A0>), ('Asphericity', <function <lambda> at 0x000001A7630AE840>), ('SpherocityIndex', <function <lambda> at 0x000001A7630AE8E0>), ('PBF', <function <lambda> at 0x000001A7630AE980>)]
