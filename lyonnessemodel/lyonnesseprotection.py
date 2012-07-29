'''
Created on Jul 22, 2012

@author: ewilde
'''
from hydramodel import hydrauser

import lyonnessemass


LYONESSEPROTECTION_NEGLIGIBLE = 0
LYONESSEPROTECTION_TINY = 1
LYONESSEPROTECTION_LIGHT = 2
LYONESSEPROTECTION_MEDIUM = 3
LYONESSEPROTECTION_HEAVY = 4
LYONESSEPROTECTION_DEVASTATING = 5

class LyonnesseProtection(lyonnessemass.LyonnesseMass):
    '''
    classdocs
    '''

    def clone(self,newOwner):
        result = get_lyonnesseprotection(self.value, newOwner)
        
        return result


def get_lyonnesseprotection(value,owner=None,recursing=False):
    if not owner:
        result = LyonnesseProtection.all().filter('value =',value).get()
    else:
        result = LyonnesseProtection.all().ancestor(owner.key()).filter('value =',value).get()

    if not result:
        if not recursing:
            result = create_lyonnesseprotection(value=value,owner=owner)
        else:
            raise ValueError()

    return result


def create_lyonnesseprotection(value, owner=None):
    if owner == None:
        hydrauser.get_hydra_user("", True)

    strVals = ['Negligible', 'Tiny', 'Light', 'Medium', 'Heavy', 'Devastating']
    for s in strVals:
        prot = LyonnesseProtection( value=strVals.index(s),
                                    valName=s,
                                    parent=owner)
        prot.put()
    
    return get_lyonnesseprotection(value,owner,True)
