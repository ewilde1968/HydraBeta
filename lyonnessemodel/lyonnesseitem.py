'''
Created on Jul 22, 2012

@author: ewilde
'''

from google.appengine.ext import db

from hydramodel import item


class LyonnesseItem(item.Item):
    '''
    classdocs
    '''
    damaged = db.BooleanProperty()

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.damaged != other.damaged:
            return False
        
        return super(LyonnesseItem,self).__eq__(other)

    def clone(self, newOwner):
        result = super(LyonnesseItem, self).clone( newOwner)

        result.damaged = self.damaged
        
        return result