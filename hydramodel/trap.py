from google.appengine.ext import db

import item

class Trap(item.Item):
    """The base type for any entity in a gaming session"""
    challenges = db.ListProperty(db.Key, indexed=False)

    def clone(self, newOwner):
        result = super(Trap, self).clone( newOwner)

        result.challenges = []
        for challenge in self.challenges:
            result.challenges.append( db.get(challenge).clone( result))

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.challenges) == len(other.challenges):
            for i in range( len(self.challenges)):
                s = self.challenges[i]
                o = other.challenges[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False
        
        return super(Trap, self).__eq__(other)
