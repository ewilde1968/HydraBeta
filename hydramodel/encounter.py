from google.appengine.ext import db

import abstractitem


class Encounter(abstractitem.AbstractItem):
    """Models content in the application"""
    parties = db.ListProperty(db.Key, indexed=False) # Party
    challenges = db.ListProperty(db.Key, indexed=False) # Challenge
    encounterMap = db.ReferenceProperty(collection_name='encounterMap')

    def clone(self, newOwner):
        result = super(Encounter, self).clone( newOwner)

        if self.encounterMap:
            result.encounterMap = self.encounterMap.clone()

        result.parties = []
        for party in self.parties:
            result.parties.append( db.get(party).clone( result))

        result.challenges = []
        for challenge in self.challenges:
            result.challenges.append( db.get(challenge).clone( result))

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.parties) == len(other.parties):
            for i in range( len(self.parties)):
                s = self.parties[i]
                o = other.parties[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
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

        if self.encounterMap != other.encounterMap:
            return False

        return super(Encounter, self).__eq__(other)
