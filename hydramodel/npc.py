from google.appengine.ext import db

import creature

class NPC(creature.Creature):
    """The base type for any entity in a gaming session"""
    challenges = db.ListProperty(db.Key, indexed=False)
    morale = db.ReferenceProperty( collection_name='morale')

    def clone(self, newOwner):
        result = super(NPC, self).clone( newOwner)

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

        if self.morale != other.morale:
            return False

        return super(NPC, self).__eq__(other)
