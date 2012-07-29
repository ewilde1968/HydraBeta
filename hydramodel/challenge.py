from google.appengine.ext import db

import abstractitem

class Challenge(abstractitem.AbstractItem):
    """The base type for any entity in a gaming session"""
    difficulty = db.ReferenceProperty(collection_name='difficulty')
    modifiers = db.ListProperty(db.Key, indexed=False)
    consequence = db.ReferenceProperty(collection_name='consequence')

    def clone(self, newOwner):
        result = super(Challenge, self).clone( newOwner)

        result.difficulty = self.difficulty
        result.consequence = self.consequence

        result.modifiers = []
        for modifier in self.modifiers:
            result.modifiers.append( db.get(modifier).clone( result))

        return result
    
    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if self.difficulty != other.difficulty:
            return False

        if len(self.modifiers) == len(other.modifiers):
            for i in range( len(self.modifiers)):
                s = self.modifiers[i]
                o = other.modifiers[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        if self.consequence != other.consequence:
            return False

        return super(Challenge, self).__eq__(other)
    
