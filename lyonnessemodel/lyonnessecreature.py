'''
Created on Jul 22, 2012

@author: ewilde
'''
from google.appengine.ext import db

from hydramodel import creature


class LyonnesseCreature(creature.Creature):
    '''
    classdocs
    '''
    strength = db.ReferenceProperty(collection_name='strength')
    agility = db.ReferenceProperty(collection_name='agility')
    speed = db.ReferenceProperty(collection_name='speed')
    durability = db.ReferenceProperty(collection_name='durability')
    maxhits = db.IntegerProperty()
    wounds = db.IntegerProperty()
    fatigue = db.IntegerProperty()
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.strength != other.strength:
            return False
        
        if self.agility != other.agility:
            return False
        
        if self.speed != other.speed:
            return False
        
        if self.durability != other.durability:
            return False
        
        if self.maxhits != other.maxhits:
            return False
        
        if self.wounds != other.wounds:
            return False
        
        if self.fatigue != other.fatigue:
            return False
        
        return super(LyonnesseCreature,self).__eq__(other)
    
    def clone(self, newOwner):
        result = super(LyonnesseCreature,self).clone(newOwner)
        
        result.strength = self.strength.clone(newOwner)
        result.agility = self.agility.clone(newOwner)
        result.speed = self.speed.clone(newOwner)
        result.durability = self.durability.clone(newOwner)
        result.maxhits = self.maxhits
        result.wounds = self.wounds
        result.fatigue = self.fatigue
        
        return result