from google.appengine.ext import db

import abstractitem

class Party(abstractitem.AbstractItem):
    """The base type for any entity in a gaming session"""
    members = db.ListProperty(db.Key, indexed=False)
    partyMorale = db.ReferenceProperty( collection_name='partyMorale')

    def clone(self, newOwner):
        result = super(Party, self).clone( newOwner)

        result.members = []
        for member in self.members:
            result.members.append( db.get(member).clone( result))

        result.partyMorale = self.partyMorale

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.members) == len(other.members):
            for i in range( len(self.members)):
                s = self.members[i]
                o = other.members[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        if self.partyMorale != other.partyMorale:
            return False

        return super(Party, self).__eq__(other)
