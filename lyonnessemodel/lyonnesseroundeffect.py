'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db


class LyonnesseRoundEffect(db.Model):
    '''
    classdocs
    '''
    subject = db.ReferenceProperty(collection_name='subject')
    roundAction = db.ReferenceProperty(collection_name='roundAction')
    wounds = db.IntegerProperty()
    fatigue = db.IntegerProperty()
    moveDestination = db.ListProperty(float, indexed=False) # Locations

    def clone(self, newOwner):
        result = LyonnesseRoundEffect( parent=newOwner,
                                       subject=self.subject, # just copy key, no cloning
                                       roundAction=self.roundAction, # no cloning
                                       wounds=self.wounds,
                                       fatigue=self.fatigue)
        result.moveDestination = []
        for md in self.moveDestination:
            result.moveDestination.append( md)
            
        return result
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.roundAction != other.roundAction:
            return False
        
        if self.subject != other.subject:
            return False

        if self.wounds != other.wounds:
            return False
        
        if self.fatigue != other.fatigue:
            return False
                
        for a,b in zip(self.moveDestination, other.moveDestination):
            if a != b:
                return False
        
        return True