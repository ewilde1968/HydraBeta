from google.appengine.ext import db

import pdmap

class RMMap(pdmap.PDMap):
    """The base type for any entity in a gaming session"""
    restrictions = db.ListProperty(db.Key, indexed=False)

    def clone(self, newOwner):
        result = super(RMMap, self).clone( newOwner)

        result.restrictions = []
        for mask in self.restrictions:
            result.restrictions.append( db.get(mask).clone( result))

        return result

    def __eq__(self, other):
        if type(self) != type(other):
                return False

        if len(self.restrictions) == len(other.restrictions):
            for i in range( len(self.restrictions)):
                s = self.restrictions[i]
                o = other.restrictions[i]
                if not( s.key() == o.key()
                        or db.get( s.key()) == db.get( o.key())):
                    return False
        else:
            return False

        return super(RMMap, self).__eq__(other)
