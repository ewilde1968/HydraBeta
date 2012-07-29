'''
Created on Jul 22, 2012

@author: ewilde
'''
from hydramodel import hydrauser

import lyonnessemass


LYONNESSESPEED_STATIONARY= 0
LYONNESSESPEED_CREEPING = 1
LYONNESSESPEED_PLODDING = 2
LYONNESSESPEED_DELIBERATE = 3
LYONNESSESPEED_SLOW = 4
LYONNESSESPEED_AVERAGE = 5
LYONNESSESPEED_ENERGETIC = 6
LYONNESSESPEED_QUICK = 7
LYONNESSESPEED_SWIFT = 8
LYONNESSESPEED_IMMEDIATE = 9
LYONNESSESPEED_INSTANTANEOUS = 10
LYONNESSESPEED_CHARACTERS = 11

class LyonnesseSpeed(lyonnessemass.LyonnesseMass):
    '''
    classdocs
    '''

    def clone(self,newOwner):
        result = get_lyonnessespeed(self.value, newOwner)
        
        return result


def get_lyonnessespeed(value, owner=None, recursing=False):
    if not owner:
        result = LyonnesseSpeed.all().filter('value =',value).get()
    else:
        result = LyonnesseSpeed.all().ancestor(owner.key()).filter('value =',value).get()

    if not result:
        if not recursing:
            result = create_lyonnessespeed(value=value,owner=owner)
        else:
            raise ValueError()

    return result


def create_lyonnessespeed(value, owner=None):
    if owner == None:
        hydrauser.get_hydra_user("", True)

    strVals = ['Stationary', 'Creeping', 'Plodding', 'Deliberate', 'Slow',
               'Average',
               'Energetic', 'Quick', 'Swift', 'Immediate', 'Instantaneous',
               "Character's"]
    for s in strVals:
        speed = LyonnesseSpeed( value=strVals.index(s),
                                valName=s,
                                parent=owner)
        speed.put()
    
    return get_lyonnessespeed(value,owner,True)
