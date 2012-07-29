from google.appengine.ext import db

import item

class Creature(item.Item):
    """The base type for any entity in a gaming session"""
    talents = db.ListProperty(db.Key, indexed=False)
    relations = db.ListProperty(db.Key, indexed=False)

    def clone(self, newOwner):
        result = super(Creature, self).clone( newOwner)

        result.talents = []
        for talent in self.talents:
            result.talents.append( db.get(talent).clone( result))

        result.relations = []
        for relation in self.relations:
            result.relations.append( db.get(relation).clone( result))

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.talents) == len(other.talents):
            for i in range( len(self.talents)):
                s = self.talents[i]
                o = other.talents[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        if len(self.relations) == len(other.relations):
            for i in range( len(self.relations)):
                s = self.relations[i]
                o = other.relations[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        return super(Creature, self).__eq__(other)
    
