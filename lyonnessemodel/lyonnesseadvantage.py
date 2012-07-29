'''
Created on Jul 22, 2012

@author: ewilde
'''
from hydramodel import hydrauser

import lyonnessemass


LYONESSEADVANTAGE_ABSURD = 0
LYONESSEADVANTAGE_HARD = 1
LYONESSEADVANTAGE_CHALLENGING = 2
LYONESSEADVANTAGE_NORMAL = 3
LYONESSEADVANTAGE_EASY = 4
LYONESSEADVANTAGE_ROUTINE = 5
LYONESSEADVANTAGE_TRIVIAL = 6


class LyonnesseAdvantage(lyonnessemass.LyonnesseMass):
    '''
    classdocs
    '''
    
    def clone(self,newOwner):
        result = get_lyonnesseadvantage(self.value, newOwner)
        
        return result
    
    
def get_lyonnesseadvantage(value, owner=None, recursing=False):
    if not owner:
        result = LyonnesseAdvantage.all().filter('value =',value).get()
    else:
        result = LyonnesseAdvantage.all().ancestor(owner.key()).filter('value =',value).get()

    if not result:
        if not recursing:
            result = create_lyonnesseadvantage(value=value,owner=owner)
        else:
            raise ValueError()

    return result


def create_lyonnesseadvantage(value, owner=None):
    if owner == None:
        hydrauser.get_hydra_user("", True)

    strVals = ['Absurd', 'Hard', 'Challenging', 'Normal', 'Easy', 'Routine', 'Trivial']
    for s in strVals:
        adv = LyonnesseAdvantage( value=strVals.index(s),
                                  valName=s,
                                  parent=owner)
        adv.put()
    
    return get_lyonnesseadvantage(value,owner,True)
