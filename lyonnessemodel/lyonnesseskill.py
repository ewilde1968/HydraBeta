'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

from hydramodel import abstractitem


class LyonnesseSkill(abstractitem.AbstractItem):
    '''
    classdocs
    '''
    skillLevel = db.ReferenceProperty(collection_name='skillLevel')
        
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.skillLevel != other.skillLevel:
            return False
        
        return super(LyonnesseSkill,self).__eq__(other)

    def clone(self, newOwner):
        result = super(LyonnesseSkill, self).clone( newOwner)

        result.skillLevel = self.skillLevel.clone( newOwner)
        
        return result