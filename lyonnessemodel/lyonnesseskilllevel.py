'''
Created on Jul 22, 2012

@author: ewilde
'''
from hydramodel import hydrauser

import lyonnessemass


LYONNESSESKILLLEVEL_UNSKILLED = 0
LYONNESSESKILLLEVEL_NEOPHYTE = 1
LYONNESSESKILLLEVEL_VETERAN = 2
LYONNESSESKILLLEVEL_SKILLED = 3
LYONNESSESKILLLEVEL_MASTER = 4
LYONNESSESKILLLEVEL_SUPERLATIVE = 5

class LyonnesseSkillLevel(lyonnessemass.LyonnesseMass):
    '''
    classdocs
    '''

    def clone(self,newOwner):
        result = get_lyonnesseskilllevel(self.value, newOwner)
        
        return result


def get_lyonnesseskilllevel(value,owner=None,recursing=False):
    if not owner:
        result = LyonnesseSkillLevel.all().filter('value =',value).get()
    else:
        result = LyonnesseSkillLevel.all().ancestor(owner.key()).filter('value =',value).get()

    if not result:
        if not recursing:
            result = create_lyonnesseskilllevel(value=value,owner=owner)
        else:
            raise ValueError()

    return result


def create_lyonnesseskilllevel(value, owner=None):
    if owner == None:
        hydrauser.get_hydra_user("", True)

    strVals = ['Unskilled', 'Neophyte', 'Veteran', 'Skilled', 'Master', 'Superlative']
    for s in strVals:
        sl = LyonnesseSkillLevel( value=strVals.index(s),
                                    valName=s,
                                    parent=owner)
        sl.put()
    
    return get_lyonnesseskilllevel(value,owner,True)
