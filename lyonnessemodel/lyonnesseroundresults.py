'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db


class LyonnesseRoundResults(db.Model):
    '''
    classdocs
    '''
    effects = db.ListProperty(db.Key,indexed=False)
    roundLogEntry = db.ReferenceProperty(collection_name='roundLogEntry')

    def clone(self, newOwner):
        result = LyonnesseRoundResults(parent=newOwner)
        
        if self.roundLogEntry:
            result.roundLogEntry = self.roundLogEntry.clone( newOwner)

        result.effects = []
        for e in self.effects:
            newEffect = db.get(e).clone( newOwner)
            newEffect.put()
            result.effects.append( newEffect.key())
        
        return result
    
    def __ne__(self, other):
        return not self==other
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.roundLogEntry != other.roundLogEntry:
            return False
        
        for a, b in zip( self.effects, other.effects):
            if a != b and db.get(a) != db.get(b):
                return False

        return True