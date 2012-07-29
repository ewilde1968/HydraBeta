'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

import lyonnesseitem


def validate_cover(coverType):
    if coverType != 'Torso' and coverType != 'Head' and coverType != 'Full Body' and coverType != 'Shield':
        raise ValueError()
    
    
class LyonnesseArmor(lyonnesseitem.LyonnesseItem):
    '''
    classdocs
    '''
    cover = db.StringProperty()
    protection = db.ReferenceProperty(collection_name='protection')
        
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.cover != other.cover:
            return False
        
        if self.protection != other.protection:
            return False
        
        return super(LyonnesseArmor,self).__eq__(other)
    
    def clone(self, newOwner):
        result = super(LyonnesseArmor, self).clone( newOwner)

        result.cover = self.cover
        
        return result