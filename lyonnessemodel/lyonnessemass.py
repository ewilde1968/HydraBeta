'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

from hydramodel import hydrauser


LYONNESSEMASS_NEGLIGIBLE = 0
LYONNESSEMASS_TINY = 1
LYONNESSEMASS_SMALL = 2
LYONNESSEMASS_AVERAGE = 3
LYONNESSEMASS_LARGE = 4
LYONNESSEMASS_HUGE = 5


class LyonnesseMass(db.Model):
    '''
    classdocs
    '''
    value = db.IntegerProperty()
    valName = db.StringProperty()
    
    def __ne__(self, other):
        return not self==other
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.value != other.value:
            return False
        
        if self.valName != other.valName:
            return False

        return True        

    def clone(self, newOwner):
        result = get_lyonnessemass(self.value, newOwner)
        
        return result


def get_lyonnessemass(value, owner=None, recursing=False):
    if not owner:
        result = LyonnesseMass.all().filter('value =',value).get()
    else:
        result = LyonnesseMass.all().ancestor(owner.key()).filter('value =',value).get()

    if not result:
        if not recursing:
            result = create_lyonnessemass(value=value,owner=owner)
        else:
            raise ValueError()

    return result


def create_lyonnessemass(value, owner=None):
    if owner == None:
        hydrauser.get_hydra_user("", True)

    strVals = ['Negligible', 'Tiny', 'Small', 'Average', 'Large', 'Huge']
    for s in strVals:
        mass = LyonnesseMass( value=strVals.index(s),
                              valName=s,
                              parent=owner)
        mass.put()
    
    return get_lyonnessemass(value,owner,True)
