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
descList: list  # value = [('PMI1', <function <lambda> at 0x7f54ed9cc0e0>), ('PMI2', <function <lambda> at 0x7f54dd8076a0>), ('PMI3', <function <lambda> at 0x7f54dd8077e0>), ('NPR1', <function <lambda> at 0x7f54dd807880>), ('NPR2', <function <lambda> at 0x7f54dd807920>), ('RadiusOfGyration', <function <lambda> at 0x7f54dd8079c0>), ('InertialShapeFactor', <function <lambda> at 0x7f54dd807a60>), ('Eccentricity', <function <lambda> at 0x7f54dd807b00>), ('Asphericity', <function <lambda> at 0x7f54dd807ba0>), ('SpherocityIndex', <function <lambda> at 0x7f54dd807c40>), ('PBF', <function <lambda> at 0x7f54dd807ce0>)]
