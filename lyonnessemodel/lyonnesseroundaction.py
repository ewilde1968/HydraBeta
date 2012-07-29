'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db


LYONNESSEROUNDACTION_ATTACK = 0
LYONNESSEROUNDACTION_HOLDFIRE = 1
LYONNESSEROUNDACTION_FLEE = 2

class LyonnesseRoundAction(db.Model):
    '''
    classdocs
    '''
    creature = db.ReferenceProperty(collection_name='creature')
    target = db.ReferenceProperty(collection_name='target')
    moveDestination = db.ListProperty(float, indexed=False) # Location
    action = db.IntegerProperty()
    strengthEffort = db.BooleanProperty()
    agilityEffort = db.BooleanProperty()
    speedEffort = db.BooleanProperty()
    poised = db.BooleanProperty()
    advantage = db.ReferenceProperty(collection_name='advantage')
    repeat = db.BooleanProperty()

    def clone(self, newOwner):
        result = LyonnesseRoundAction( parent=newOwner,
                                       creature=self.creature, # do not clone, just a reference
                                       target=self.target, # do not clone, just a reference
                                       action=self.action,
                                       strengthEffort=self.strengthEffort,
                                       agilityEffort=self.agilityEffort,
                                       speedEffort=self.speedEffort,
                                       poised=self.poised,
                                       advantage=self.advantage,
                                       repeat=self.repeat)

        result.moveDestination = []
        for md in self.moveDestination:
            result.moveDestination.append(md)
            
        result.put()
        
        return result
    
    def __ne__(self, other):
        return not self==other
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.action != other.action:
            return False
        
        if self.advantage != other.advantage:
            return False
        
        if self.agilityEffort != other.agilityEffort:
            return False
        
        if self.creature != other.creature:
            return False
        
        if self.poised != other.poised:
            return False
        
        if self.repeat != other.repeat:
            return False
        
        if self.speedEffort != other.speedEffort:
            return False
        
        if self.strengthEffort != other.strengthEffort:
            return False
        
        if self.target != other.target:
            return False
        
        for a,b in zip(self.moveDestination, other.moveDestination):
            if a != b:
                return False
        
        return True