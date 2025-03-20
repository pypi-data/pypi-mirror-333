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
descList: list  # value = [('PMI1', <function <lambda> at 0x0000023DDF9FA680>), ('PMI2', <function <lambda> at 0x0000023DE7B65000>), ('PMI3', <function <lambda> at 0x0000023DE7B65090>), ('NPR1', <function <lambda> at 0x0000023DE7B65120>), ('NPR2', <function <lambda> at 0x0000023DE7B651B0>), ('RadiusOfGyration', <function <lambda> at 0x0000023DE7B65240>), ('InertialShapeFactor', <function <lambda> at 0x0000023DE7B652D0>), ('Eccentricity', <function <lambda> at 0x0000023DE7B65360>), ('Asphericity', <function <lambda> at 0x0000023DE7B653F0>), ('SpherocityIndex', <function <lambda> at 0x0000023DE7B65480>), ('PBF', <function <lambda> at 0x0000023DE7B65510>)]
