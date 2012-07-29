'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

from hydramodel import item


class LyonnesseWeapon(item.Item):
    '''
    classdocs
    '''
    # size is the wound level
    weaponSpeed = db.ReferenceProperty(collection_name='weaponSpeed')
    poisedSpeed = db.ReferenceProperty(collection_name='poisedSpeed')
    length = db.IntegerProperty()

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.weaponSpeed != other.weaponSpeed:
            return False
        
        if self.poisedSpeed != other.poisedSpeed:
            return False
        
        if self.length != other.length:
            return False
        
        return super(LyonnesseWeapon,self).__eq__(other)

    def clone(self, newOwner):
        result = super(LyonnesseWeapon, self).clone( newOwner)

        result.weaponSpeed = self.weaponSpeed.clone( newOwner)
        result.poisedSpeed = self.poisedSpeed.clone( newOwner)
        result.length = self.length
        
        return result